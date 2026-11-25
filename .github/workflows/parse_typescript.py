import json
import os
import re
import shutil
import subprocess
import tempfile

## Language-specific resource name overrides:
typescript_resource_overrides = {
    "generic_component": "GenericComponent",
    "generic_service": "GenericService",
    "input_controller": "InputController",
    "movement_sensor": "MovementSensor",
    "power_sensor": "PowerSensor",
    "vision": "Vision",
    "robot": "",
    "data": "Data",
    "dataset": "Data",
    "data_sync": "Data",
    "data_manager": "DataManager",
    "mltraining": "MlTraining",
    "world_state_store": "WorldStateStore",
    "audio_in": "AudioIn",
    "audio_out": "AudioOut"
}

## Ignore these specific APIs if they error, are deprecated, etc:
typescript_ignore_apis = [
    'getRoverRentalRobots' # internal use
]

## Use these URLs for data types that are built-in to the language:
typescript_datatype_links = {}

## Pinned so that the TypeDoc JSON schema the parser reads doesn't change under us.
TYPEDOC_VERSION = "0.28.19"
SDK_PACKAGE = "@viamrobotics/sdk"

## TypeDoc "kind" numbers, and the folder TypeDoc puts each kind's HTML page in.
## Escaped so that Markdown doesn't read a type argument like <FieldMask> as an HTML tag.
LT = "\\<"

KIND_NAMESPACE = 4
KIND_METHOD = 2048
KIND_PROPERTY = 1024
KIND_REFERENCE = 4194304
KIND_FOLDERS = {
    4: "modules",
    8: "enums",
    32: "variables",
    64: "functions",
    128: "classes",
    256: "interfaces",
    2097152: "types",
}


def run_typedoc(workdir, version="latest"):
    """Install the published SDK and run TypeDoc on its type declarations.

    Returns the path to the JSON model. Requires node and npm. Uses the SDK
    as published to npm (default: the latest release) rather than a docs site,
    so the model has the full text of every type.
    """
    with open(os.path.join(workdir, "package.json"), "w") as f:
        f.write('{"name": "sdk-docs-model", "private": true, "type": "module"}')
    subprocess.run(
        ["npm", "install", "--silent", "--no-audit", "--no-fund",
         f"{SDK_PACKAGE}@{version}", f"typedoc@{TYPEDOC_VERSION}", "typescript@^6.0.3"],
        cwd=workdir, check=True)
    entry = f"node_modules/{SDK_PACKAGE}/dist/main.d.ts"
    ## 'strict' matters: without it TypeScript drops '| undefined' from types.
    with open(os.path.join(workdir, "tsconfig.json"), "w") as f:
        json.dump({
            "compilerOptions": {"strict": True, "target": "ESNext", "module": "ESNext",
                                "moduleResolution": "bundler", "skipLibCheck": True},
            "files": [entry]}, f)
    out = os.path.join(workdir, "api.json")
    subprocess.run(
        ["npx", "--no-install", "typedoc", "--tsconfig", "tsconfig.json", "--entryPoints", entry,
         "--skipErrorChecking", "--json", out, "--pretty", "false", "--disableSources",
         "--logLevel", "Error", "--externalPattern", f"**/node_modules/!({SDK_PACKAGE.split('/')[0]})/**"],
        cwd=workdir, check=True)
    with open(os.path.join(workdir, "node_modules", SDK_PACKAGE, "package.json")) as f:
        print("TypeScript SDK version used for API model: " + json.load(f)["version"])
    return out


def indent_continuation(text):
    """Put continuation lines of a multi-line description at a uniform two-space indent."""
    lines = text.split("\n")
    return "\n  ".join([lines[0]] + [l.strip() for l in lines[1:]]).rstrip() if len(lines) > 1 else text


class TypeDocModel:
    """Reads a TypeDoc JSON model and renders its types as Markdown."""

    def __init__(self, path, sdk_url):
        with open(path) as f:
            data = json.load(f)
        self.sdk_url = sdk_url
        self.by_id = {}
        self.parent = {}
        self._index(data, None)
        self.top = {c["name"]: c for c in data["children"]}
        ## TypeDoc only shows a namespace prefix (appApi.Location) on names that are
        ## ambiguous across namespaces, so find those.
        counts = {}
        for ns in data["children"]:
            if ns["kind"] == KIND_NAMESPACE:
                for c in ns.get("children", []):
                    counts[c["name"]] = counts.get(c["name"], 0) + 1
        self.ambiguous = {n for n, k in counts.items() if k > 1 or n in self.top}

    def _index(self, node, parent):
        if isinstance(node, dict):
            if "id" in node:
                self.by_id[node["id"]] = node
                if parent is not None:
                    self.parent[node["id"]] = parent
                parent = node["id"]
            for v in node.values():
                self._index(v, parent)
        elif isinstance(node, list):
            for v in node:
                self._index(v, parent)

    def qualified_name(self, node_id):
        node = self.by_id[node_id]
        name = node["name"]
        pid = self.parent.get(node_id)
        while pid is not None and self.by_id[pid].get("kind") == KIND_NAMESPACE:
            name = self.by_id[pid]["name"] + "." + name
            pid = self.parent.get(pid)
        return name

    def namespace_prefix(self, node_id):
        """The dotted namespace chain a node lives in (for example 'appApi'), or ''."""
        names = []
        pid = self.parent.get(node_id)
        while pid is not None and self.by_id[pid].get("kind") == KIND_NAMESPACE:
            names.insert(0, self.by_id[pid]["name"])
            pid = self.parent.get(pid)
        return ".".join(names)

    def url(self, node_id):
        node = self.by_id[node_id]
        folder = KIND_FOLDERS.get(node["kind"])
        if folder is None:
            return None
        return f"{self.sdk_url}/{folder}/{self.qualified_name(node_id)}.html"

    def client(self, name):
        node = self.top.get(name)
        if node is not None and node["kind"] == KIND_REFERENCE:
            node = self.by_id.get(node["target"], node)
        return node

    def type_md(self, t):
        """Render a TypeDoc type as Markdown, linking types defined in the SDK."""
        if t is None:
            return ""
        k = t["type"]
        if k == "intrinsic":
            return t["name"]
        if k == "literal":
            v = t["value"]
            if v is None:
                return "null"
            if isinstance(v, bool):
                return str(v).lower()
            return json.dumps(v) if isinstance(v, str) else str(v)
        if k == "reference":
            name = t["name"]
            link = None
            if isinstance(t.get("target"), int) and t["target"] in self.by_id:
                link = self.url(t["target"])
                if name in self.ambiguous:
                    prefix = self.namespace_prefix(t["target"])
                    if prefix:
                        ns = self.sdk_url + "/modules/" + prefix + ".html"
                        text = "[" + prefix + "](" + ns + ")." + ("[" + name + "](" + link + ")" if link else name)
                        return text + self._type_args(t)
            text = f"[{name}]({link})" if link else name
            return text + self._type_args(t)
        if k == "array":
            e = t["elementType"]
            inner = self.type_md(e)
            wrap = e["type"] in ("union", "intersection", "conditional") or (
                e["type"] == "reflection" and e["declaration"].get("signatures"))
            return ("(" + inner + ")[]") if wrap else inner + "[]"
        if k == "union":
            return " | ".join(self.type_md(x) for x in t["types"])
        if k == "intersection":
            return " & ".join(self.type_md(x) for x in t["types"])
        if k == "tuple":
            return "[" + ", ".join(self.type_md(x) for x in t.get("elements", [])) + "]"
        if k == "named-tuple-member":
            return t["name"] + ("?" if t.get("isOptional") else "") + ": " + self.type_md(t["element"])
        if k == "optional":
            return self.type_md(t["elementType"]) + "?"
        if k == "rest":
            return "..." + self.type_md(t["elementType"])
        if k == "typeOperator":
            return t["operator"] + " " + self.type_md(t["target"])
        if k == "indexedAccess":
            return self.type_md(t["objectType"]) + "[" + self.type_md(t["indexType"]) + "]"
        if k == "query":
            return "typeof " + self.type_md(t["queryType"])
        if k == "predicate":
            return ("asserts " if t.get("asserts") else "") + t["name"] + (
                " is " + self.type_md(t["targetType"]) if t.get("targetType") else "")
        if k == "templateLiteral":
            return "`" + t["head"] + "".join("${" + self.type_md(a) + "}" + b for a, b in t["tail"]) + "`"
        if k == "conditional":
            return (f"{self.type_md(t['checkType'])} extends {self.type_md(t['extendsType'])} ? "
                    f"{self.type_md(t['trueType'])} : {self.type_md(t['falseType'])}")
        if k == "mapped":
            return "{ [" + t["parameter"] + " in " + self.type_md(t["parameterType"]) + "]: " + self.type_md(t["templateType"]) + " }"
        if k == "reflection":
            d = t["declaration"]
            if d.get("signatures"):
                s = d["signatures"][0]
                ps = ", ".join(p["name"] + ("?" if p["flags"].get("isOptional") else "") + ": " + self.type_md(p.get("type"))
                               for p in s.get("parameters", []))
                return f"({ps}) => {self.type_md(s.get('type'))}"
            parts = [c["name"] + ("?" if c["flags"].get("isOptional") else "") + ": " + self.type_md(c.get("type"))
                     for c in d.get("children", [])]
            for ix in d.get("indexSignatures", []):
                p = ix["parameters"][0]
                parts.append("[" + p["name"] + ": " + self.type_md(p["type"]) + "]: " + self.type_md(ix.get("type")))
            return "{ " + "; ".join(parts) + " }" if parts else "{}"
        print(f"WARNING: unhandled TypeDoc type kind '{k}'")
        return f"<{k}>"

    def _type_args(self, t):
        if t.get("typeArguments"):
            return LT + ", ".join(self.type_md(a) for a in t["typeArguments"]) + ">"
        return ""

    def comment_md(self, parts):
        """Render TypeDoc comment parts (text, code, inline tags) as Markdown."""
        out = ""
        for p in parts or []:
            if p["kind"] == "inline-tag" and p.get("tag") == "@link":
                target = p.get("target")
                if isinstance(target, str):
                    ## {@link https://example.com Some text}
                    out += f"[{p['text']}]({target})"
                    continue
                link = self.url(target) if isinstance(target, int) and target in self.by_id else None
                out += f"[`{p['text']}`]({link})" if link else f"`{p['text']}`"
            else:
                out += p["text"]
        return out

    def block_tag(self, signature, tag):
        for bt in (signature.get("comment") or {}).get("blockTags", []):
            if bt["tag"] == tag:
                return bt["content"]
        return None


class TypeScriptParser:
    _model = None  # shared TypeDoc model, built on first parse()

    def __init__(self, proto_map_file, typescript_staging_url = None, typedoc_json = None):
        self.proto_map_file = proto_map_file
        self.sdk_url = "https://ts.viam.dev"

        ## Optionally read a prebuilt TypeDoc JSON model (for example, set
        ## TYPESCRIPT_TYPEDOC_JSON to its path) instead of installing the SDK from npm.
        self.typedoc_json = typedoc_json or os.environ.get("TYPESCRIPT_TYPEDOC_JSON")
        self.typescript_methods = {}


    def parse(self, type, viam_resources, args):
        self.typescript_methods[type] = {}

        ## Skip resources not supported in TypeScript
        unsupported_resources = [
            "base_remote_control", "pose_tracker", "mlmodel"
        ]

        ## update_sdk_methods.py calls parse() once per resource type, so build the model once per run.
        model = TypeScriptParser._model
        if model is None:
            tmpdir = None
            try:
                path = self.typedoc_json
                if not path:
                    tmpdir = tempfile.mkdtemp(prefix="sdk-typedoc-")
                    path = run_typedoc(tmpdir)
                model = TypeScriptParser._model = TypeDocModel(path, self.sdk_url)
            finally:
                if tmpdir:
                    shutil.rmtree(tmpdir, ignore_errors=True)

        for resource in viam_resources:

            ## Initialize TypeScript methods dictionary if it doesn't exist
            self.typescript_methods[type][resource] = {}

            if resource in unsupported_resources:
                if args.verbose:
                    print(f'DEBUG: Skipping unsupported TypeScript resource: {resource}')
                continue

            ## App-layer SDK clients (app, billing, data, mltraining, ...) are
            ## interfaces in TypeDoc; component/service clients remain classes.
            if resource in typescript_resource_overrides:
                client_name = typescript_resource_overrides[resource] + "Client"
            else:
                client_name = resource.capitalize() + "Client"
            client = model.client(client_name)
            if client is None:
                print(f"DEBUG: No TypeDoc entry for {client_name}")
                continue
            page = f"{self.sdk_url}/{KIND_FOLDERS[client['kind']]}/{client['name']}.html"

            ## Only the Methods and Properties groups are documented. The robot client also
            ## files methods under category groups (TypeDoc lists them in `groups`):
            keep = ["Methods", "Properties"]
            if resource == 'robot':
                keep += ["App/Cloud", "ComponentConfig", "Discovery", "Frame System",
                         "Operations", "Resources", "Sessions", "Modules"]
            allowed = {i for g in client.get("groups", []) if g["title"] in keep for i in g["children"]}

            for member in client.get("children", []):
                if member["id"] not in allowed:
                    continue
                name = member["name"]
                if name == 'callOptions':
                    continue
                ## Inherited members (the robot client's event-emitter methods) aren't part of the documented API.
                if member["flags"].get("isInherited"):
                    continue
                link = f"{page}#{name.lower()}"

                if member["kind"] == KIND_PROPERTY:
                    description = model.comment_md((member.get("comment") or {}).get("summary")).strip()
                    description = indent_continuation(description)
                    self.typescript_methods[type][resource][name] = {
                        'method_description': "",
                        'method_link': link,
                        'parameters': {},
                        'proto': '',
                        'return': {
                            'return_description': description,
                            'return_type': model.type_md(member.get("type")),
                            'return_usage': model.type_md(member.get("type")),
                        },
                        'code_sample': resource + "." + name + "\n",
                    }
                elif member["kind"] == KIND_METHOD:
                    sig = member["signatures"][0]
                    if len(member["signatures"]) > 1:
                        print(f"WARNING: typescript {resource} {name} has {len(member['signatures'])} overloads; documenting only the first")
                    param_object = {}
                    for param in sig.get("parameters", []):
                        param_description = model.comment_md((param.get("comment") or {}).get("summary")).strip()
                        param_description = indent_continuation(param_description)
                        param_type = model.type_md(param.get("type"))
                        param_name = param["name"]
                        if param_description:
                            param_usage = "%s (%s) - %s" % (param_name, param_type, param_description)
                        else:
                            param_usage = "%s (%s)" % (param_name, param_type)
                        param_object[param_name] = {
                            'optional': bool(param["flags"].get("isOptional")),
                            'param_description': param_description,
                            'param_type': param_type,
                            'param_usage': param_usage,
                        }

                    return_type = model.type_md(sig.get("type"))
                    returns = model.block_tag(sig, "@returns")
                    return_description = model.comment_md(returns).strip() if returns else None
                    ## Some doc comments write "@returns - Description"; drop the dash.
                    if return_description and return_description.startswith("- "):
                        return_description = return_description[2:]

                    entry = {
                        'method_description': model.comment_md((sig.get("comment") or {}).get("summary")).strip(),
                        'method_link': link,
                        'parameters': param_object,
                        'proto': '',
                        'return': {
                            'return_description': return_description,
                            'return_type': return_type,
                            'return_usage': return_type,
                        },
                    }

                    example = model.block_tag(sig, "@example")
                    if example:
                        ## The example's first code block is the sample; text after it is prose.
                        code = next((p["text"] for p in example if p["kind"] == "code"), None)
                        if code:
                            m = re.match(r"```[^\n]*\n(.*?)```", code, re.S)
                            body = m.group(1) if m else code
                            entry['code_sample'] = "".join(line.rstrip() + "\n" for line in body.strip().split("\n"))

                    self.typescript_methods[type][resource][name] = entry

        return self.typescript_methods
