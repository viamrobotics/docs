#!/usr/bin/env python3
"""Report where the docs mention API elements that viamrobotics/api marks deprecated.

Parses every .proto file under --proto-dir for `option deprecated = true` (RPCs and
messages) and `[deprecated = true]` (fields and enum values), maps each deprecated RPC
to its per-SDK method names through sdk_protos_map.csv, and greps docs/ and static/
for every name.

For each deprecated RPC that the generated API reference documents (it has at least one
SDK method in sdk_protos_map.csv), update_sdk_methods.py renders a deprecation notice
from a hand-written override file:

    static/include/<app|components|services|robot>/apis/overrides/protos/<resource>.<Proto>.deprecated.md

The proto has no machine-readable "use X instead", so that file is where the replacement
is named. With --strict, this script exits non-zero when a documented deprecated RPC has
no such file, so a newly deprecated RPC can't keep rendering as a normal method.

Usage:
    git clone --depth 1 https://github.com/viamrobotics/api /tmp/api
    python3 .github/workflows/check_deprecated_protos.py --proto-dir /tmp/api/proto [--strict] [--output report.md]
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict

GITROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROTO_MAP_FILE = os.path.join(GITROOT, '.github/workflows/sdk_protos_map.csv')

## Directories scanned for mentions. The generated reference files and the per-method
## override files are reported separately, because they're the reference entry itself
## rather than a page recommending the method:
SEARCH_DIRS = ['docs', 'static']
REFERENCE_PATH_PARTS = ('/apis/generated/', '/apis/overrides/')

## Field and enum value names too generic to grep for usefully (for example `id`, `name`,
## `secret`). Only names containing an underscore are searched.
def is_searchable_field(name):
    return '_' in name

## The static/include/ directory update_sdk_methods.py uses for each resource's overrides
## (its `type_filepath_name`: components and services are pluralized, app and robot aren't):
APP_RESOURCES = {'app', 'billing', 'data', 'dataset', 'data_sync', 'mltraining'}


def resource_type_dir(resource):
    if resource in APP_RESOURCES:
        return 'app'
    if resource == 'robot':
        return 'robot'
    if resource in COMPONENT_RESOURCES:
        return 'components'
    return 'services'


COMPONENT_RESOURCES = {
    'arm', 'audio_in', 'audio_out', 'base', 'board', 'button', 'camera', 'encoder', 'gantry',
    'generic_component', 'gripper', 'input_controller', 'motor', 'movement_sensor',
    'power_sensor', 'sensor', 'servo', 'switch',
}


def snake_to_camel(name, upper=False):
    parts = name.split('_')
    first = parts[0].capitalize() if upper else parts[0]
    return first + ''.join(p.capitalize() for p in parts[1:])


def strip_comment(line):
    ## Good enough for proto: '//' never appears inside the string literals these files use
    ## in option values that matter here.
    return line.split('//', 1)[0]


def parse_proto(path, rel_path):
    """Return lists of deprecated rpcs, messages, and fields/enum values in one proto file."""
    rpcs, messages, fields = [], [], []
    ## Stack of (kind, name) for each open brace; kind is 'service', 'message', 'enum',
    ## 'rpc', 'oneof', or 'other' (option bodies and similar).
    stack = []
    with open(path, encoding='utf-8') as f:
        for lineno, raw in enumerate(f, 1):
            line = strip_comment(raw).strip()
            if not line:
                continue

            opener = re.match(r'(service|message|enum|oneof)\s+(\w+)\s*\{', line)
            rpc = re.match(r'rpc\s+(\w+)\s*\(', line)
            opens, closes = line.count('{'), line.count('}')

            if opener:
                stack.append((opener.group(1), opener.group(2)))
                opens -= 1
            elif rpc and line.endswith('{'):
                stack.append(('rpc', rpc.group(1)))
                opens -= 1
            elif re.match(r'option\s+deprecated\s*=\s*true\s*;', line) and stack:
                kind, name = stack[-1]
                service = next((n for k, n in reversed(stack) if k == 'service'), None)
                if kind == 'rpc':
                    rpcs.append({'service': service, 'name': name, 'file': rel_path, 'line': lineno})
                elif kind == 'message':
                    messages.append({'name': name, 'file': rel_path, 'line': lineno})
            elif re.search(r'\[[^\]]*\bdeprecated\s*=\s*true[^\]]*\]', line):
                ## Field (`type name = N [...]`) or enum value (`NAME = N [...]`):
                m = re.match(r'(?:(?:repeated|optional)\s+)?(?:map<[^>]+>\s+|[\w.]+\s+)?(\w+)\s*=\s*\d+', line)
                if m:
                    parent = next((n for k, n in reversed(stack) if k in ('message', 'enum')), None)
                    fields.append({'parent': parent, 'name': m.group(1), 'file': rel_path, 'line': lineno})

            ## Any other braces (option bodies like `{get: "..."}`, multi-line options) are
            ## tracked as anonymous scopes so the stack stays aligned:
            net = opens - closes
            for _ in range(max(net, 0)):
                stack.append(('other', None))
            for _ in range(max(-net, 0)):
                if stack:
                    stack.pop()
    return rpcs, messages, fields


def parse_all_protos(proto_dir):
    rpcs, messages, fields = [], [], []
    for root, _, files in os.walk(proto_dir):
        for name in sorted(files):
            if not name.endswith('.proto'):
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, proto_dir)
            r, m, f = parse_proto(path, rel)
            rpcs += r
            messages += m
            fields += f
    return rpcs, messages, fields


def load_proto_map():
    """Return {(resource, proto): {'python': ..., 'go': ..., 'flutter': ..., 'typescript': ...}}."""
    rows = {}
    with open(PROTO_MAP_FILE, encoding='utf-8') as f:
        for row in csv.reader(f):
            if not row or row[0].startswith('#'):
                continue
            row = [c.strip() for c in row] + [''] * 7
            resource, proto = row[0], row[1]
            rows[(resource, proto)] = {
                'python': row[3], 'go': row[4], 'flutter': row[5], 'typescript': row[6],
            }
    return rows


def candidate_resources(rpc, proto_map):
    """Resources in sdk_protos_map.csv that this proto file's RPC could belong to."""
    path_parts = rpc['file'].split(os.sep)
    ## viam/<area>/<name>/v1/<file>.proto, or viam/app/v1/<file>.proto for the core app protos:
    if len(path_parts) >= 4 and path_parts[2] == 'v1':
        key = os.path.splitext(path_parts[3])[0]
    else:
        key = path_parts[2] if len(path_parts) > 2 else ''
    key = key.replace('_', '')
    if key == 'robot' and path_parts[1] == 'app':
        key = 'app'

    matches = []
    for resource, proto in proto_map:
        if proto != rpc['name']:
            continue
        norm = resource.replace('_', '')
        if norm in (key, key + 'component', key + 'service') or (key, norm) == ('datasync', 'datasync'):
            matches.append(resource)
    return matches


def search_names(names):
    """Grep SEARCH_DIRS for whole-word matches of any name. Return {name: [(path, lineno, text)]}."""
    names = sorted({n for n in names if n})
    if not names:
        return {}
    pattern = re.compile(r'(?<![\w])(' + '|'.join(re.escape(n) for n in names) + r')(?![\w])')
    hits = defaultdict(list)
    for top in SEARCH_DIRS:
        for root, _, files in os.walk(os.path.join(GITROOT, top)):
            for name in files:
                if not name.endswith(('.md', '.html', '.yaml', '.json')):
                    continue
                path = os.path.join(root, name)
                rel = os.path.relpath(path, GITROOT)
                try:
                    with open(path, encoding='utf-8') as f:
                        for lineno, line in enumerate(f, 1):
                            for m in pattern.finditer(line):
                                hits[m.group(1)].append((rel, lineno, line.strip()))
                except UnicodeDecodeError:
                    continue
    return hits


def is_reference_file(rel_path):
    return any(part in '/' + rel_path for part in REFERENCE_PATH_PARTS)


def deprecated_override_path(resource, proto):
    return os.path.join(
        GITROOT, 'static/include', resource_type_dir(resource), 'apis/overrides/protos',
        resource + '.' + proto + '.deprecated.md')


def format_hits(hits, limit=None):
    lines = []
    shown = hits if limit is None else hits[:limit]
    for path, lineno, text in shown:
        if len(text) > 160:
            text = text[:157] + '...'
        lines.append(f'  - [{path}:{lineno}]({path}#L{lineno}): `{text.replace("`", "")}`')
    if limit is not None and len(hits) > limit:
        lines.append(f'  - ...and {len(hits) - limit} more')
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--proto-dir', required=True, help='Path to the proto/ directory of a viamrobotics/api checkout.')
    parser.add_argument('--output', help='Write the Markdown report here instead of stdout.')
    parser.add_argument('--strict', action='store_true',
                        help='Exit 1 if a documented deprecated RPC has no .deprecated.md override.')
    args = parser.parse_args()

    rpcs, messages, fields = parse_all_protos(args.proto_dir)
    proto_map = load_proto_map()

    ## Every proto name used by any non-deprecated RPC, to flag names shared with a live method
    ## (robot GetStatus vs. component GetStatus, for example):
    deprecated_keys = set()
    for rpc in rpcs:
        for resource in candidate_resources(rpc, proto_map):
            deprecated_keys.add((resource, rpc['name']))
    live_proto_names = {proto for (resource, proto) in proto_map if (resource, proto) not in deprecated_keys}

    out = ['# Deprecated API audit', '']
    out.append(f'Source: `{os.path.abspath(args.proto_dir)}`. '
               f'Found {len(rpcs)} deprecated RPCs, {len(messages)} deprecated messages, '
               f'and {len(fields)} deprecated fields or enum values.')
    out.append('')
    out.append('Mentions inside the generated API reference and its override files are listed '
               'separately from other pages, because they are the reference entry itself.')
    out.append('')

    missing_overrides = []

    out.append('## Deprecated RPCs')
    out.append('')
    for rpc in sorted(rpcs, key=lambda r: (r['file'], r['line'])):
        resources = candidate_resources(rpc, proto_map)
        sdk_names = {rpc['name']}
        documented = False
        for resource in resources:
            for sdk, method in proto_map[(resource, rpc['name'])].items():
                if method:
                    sdk_names.add(method)
                    documented = True
        ambiguous = rpc['name'] in live_proto_names

        out.append(f'### {rpc["service"]}.{rpc["name"]}')
        out.append('')
        out.append(f'- Proto: `{rpc["file"]}:{rpc["line"]}`')

        ## A name shared with a live RPC, on a service the reference doesn't document, only
        ## turns up the live method (sensors service DoCommand vs. every resource's DoCommand):
        if ambiguous and not documented:
            out.append(f'- **Ambiguous name, not searched**: a non-deprecated RPC elsewhere is also called '
                       f'`{rpc["name"]}`, and this service is not in the generated reference. '
                       f'Search for mentions of the service itself by hand.')
            out.append('')
            continue

        hits = search_names(sdk_names)
        all_hits = sorted({h for n in sdk_names for h in hits.get(n, [])})
        ref_hits = [h for h in all_hits if is_reference_file(h[0])]
        page_hits = [h for h in all_hits if not is_reference_file(h[0])]

        out.append(f'- Names searched: {", ".join(f"`{n}`" for n in sorted(sdk_names))}')
        if ambiguous:
            out.append(f'- **Ambiguous name**: a non-deprecated RPC elsewhere is also called `{rpc["name"]}`. '
                       'Triage each mention by context.')
        if resources and documented:
            for resource in resources:
                override = deprecated_override_path(resource, rpc['name'])
                rel = os.path.relpath(override, GITROOT)
                if os.path.isfile(override):
                    out.append(f'- Deprecation note: `{rel}`')
                else:
                    out.append(f'- **Missing deprecation note**: `{rel}`')
                    missing_overrides.append(rel)
        else:
            out.append('- Not in the generated API reference (no SDK method mapped in `sdk_protos_map.csv`).')
        out.append(f'- Reference entries: {len(ref_hits)} lines in {len({h[0] for h in ref_hits})} files')
        out.append(f'- Other pages: {len(page_hits)} lines in {len({h[0] for h in page_hits})} files')
        out += format_hits(page_hits)
        out.append('')

    out.append('## Deprecated messages')
    out.append('')
    out.append('Messages are listed for completeness. Request and response messages of deprecated '
               'RPCs are covered by the RPC entries above.')
    out.append('')
    for msg in sorted(messages, key=lambda m: (m['file'], m['line'])):
        out.append(f'- `{msg["name"]}` (`{msg["file"]}:{msg["line"]}`)')
    out.append('')

    out.append('## Deprecated fields and enum values')
    out.append('')
    out.append('Fields are searched by their proto name plus camelCase variants. Names without an '
               'underscore (`id`, `name`, `secret`) are too generic to search and are only listed. '
               'Field names often collide with SDK parameters and config attributes that are not '
               'deprecated, so treat these mentions as leads, not findings.')
    out.append('')
    fields_by_name = defaultdict(list)
    for field in sorted(fields, key=lambda f: (f['file'], f['line'])):
        fields_by_name[field['name']].append(field)
    for name in sorted(fields_by_name):
        locations = ', '.join(f'`{f["parent"]}` (`{f["file"]}:{f["line"]}`)' for f in fields_by_name[name])
        if not is_searchable_field(name):
            out.append(f'- `{name}` in {locations}: not searched')
            continue
        names = {name}
        if not name.isupper():
            names |= {snake_to_camel(name), snake_to_camel(name, upper=True)}
        hits = search_names(names)
        all_hits = sorted({h for n in names for h in hits.get(n, [])})
        page_hits = [h for h in all_hits if not is_reference_file(h[0])]
        ref_count = len(all_hits) - len(page_hits)
        out.append(f'- `{name}` in {locations}: {len(page_hits)} page mentions, {ref_count} reference mentions')
        out += ['  ' + l for l in format_hits(page_hits, limit=5)]
    out.append('')

    report = '\n'.join(out) + '\n'
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
    else:
        sys.stdout.write(report)

    if missing_overrides:
        print(f'{len(missing_overrides)} documented deprecated RPC(s) have no deprecation note:', file=sys.stderr)
        for path in missing_overrides:
            print('  ' + path, file=sys.stderr)
        if args.strict:
            sys.exit(1)


if __name__ == '__main__':
    main()
