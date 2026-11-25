import re as regex
import zlib
from urllib.request import urlopen, Request

from parser_utils import make_soup
from markdownify import markdownify as md

## Language-specific resource name overrides:
python_resource_overrides = {
    "generic_component": "generic",
    "input_controller": "input",
    "generic_service": "generic",
    "data": "data_client",
    "app": "app_client",
    "billing": "billing_client",
    "data": "data_client",
    ## Python bundles Dataset and Datasync protos in with Data,
    ## while Flutter does not. HACK:
    "dataset": "data_client",
    "data_sync": "data_client",
    "mltraining": "ml_training_client"
}

## Ignore these specific APIs if they error, are deprecated, etc:
python_ignore_apis = [
    'viam.app.app_client.AppClient.get_rover_rental_robots', # internal use
    'viam.app.app_client.AppClient.get_rover_rental_parts', # internal use
    'viam.app.data_client.DataClient.create_filter', # deprecated
    'viam.app.data_client.DataClient.delete_tabular_data_by_filter', # deprecated
    'viam.components.input.client.ControllerClient.reset_channel', # GUESS ?
    'viam.robot.client.RobotClient.transform_point_cloud', # unimplemented
    'viam.robot.client.RobotClient.get_component', # GUESS ?
    'viam.robot.client.RobotClient.get_service', # GUESS ?
    'viam.components.board.client.BoardClient.write_analog', # Currently borked: https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.write_analog
    'viam.components.board.client.StreamWithIterator.next', # No content upstream
    'viam.robot.client.ViamChannel.close', # channel-specific close
    'viam.robot.client.SessionsClient.reset', # session-specific reset
    'viam.app.app_client.APIKeyAuthorization.resource_id', # dataclass attribute, not an AppClient method
    'viam.app.app_client.APIKeyAuthorization.resource_type', # dataclass attribute, not an AppClient method
    'viam.app.app_client.APIKeyAuthorization.role' # dataclass attribute, not an AppClient method
]

## Use these URLs for data types that are not otherwise captured by parse(), such as:
## - Well-known built-in data types that are not scrapeable (like 'int')
## - Viam-specific data types, even if scrapeable, that are part of a multiple-data-type return
##   (like list_organization_members : Tuple[List[viam.proto.app.OrganizationMember], List[viam.proto.app.OrganizationInvite]]
## Data type links defined here will be used instead of scraped links if both exist:
python_datatype_links = {
    ## Built-in data types:
    "str": "https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str",
    "int": "https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex",
    "float": "https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex",
    "bytes": "https://docs.python.org/3/library/stdtypes.html#bytes-objects",
    "bool": "https://docs.python.org/3/library/stdtypes.html#boolean-type-bool",
    "datetime.datetime": "https://docs.python.org/3/library/datetime.html",
    "datetime.timedelta": "https://docs.python.org/3/library/datetime.html#timedelta-objects",
    ## Third-party data types:
    "numpy.typing.NDArray": "https://numpy.org/doc/stable/reference/typing.html#numpy.typing.NDArray",
    ## Viam-specific data types:
    "viam.proto.app.OrganizationMember": "https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember",
    "viam.proto.app.OrganizationInvite": "https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite",
    "viam.components.arm.KinematicsFileFormat.ValueType": "https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.KinematicsFileFormat",
    "viam.media.video.NamedImage": "https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.NamedImage",
    "viam.proto.common.ResponseMetadata": "https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResponseMetadata",
    "viam.proto.component.encoder.PositionType.ValueType": "https://python.viam.dev/autoapi/viam/gen/component/encoder/v1/encoder_pb2/index.html#viam.gen.component.encoder.v1.encoder_pb2.PositionType",
    "viam.components.movement_sensor.movement_sensor.MovementSensor.Accuracy": "https://python.viam.dev/autoapi/viam/components/movement_sensor/movement_sensor/index.html#viam.components.movement_sensor.movement_sensor.MovementSensor.Accuracy",
    "viam.services.vision.vision.Vision.Properties": "https://python.viam.dev/autoapi/viam/services/vision/vision/index.html#viam.services.vision.vision.Vision.Properties"
}

## Type-string tokens that are never linked: typing/collections generics and literals.
## DESIGN DECISION: Ignore well-known, usually leading (containing) data types like List, Tuple, Dict.
python_unlinked_types = {
    "List", "list", "Dict", "dict", "Tuple", "tuple", "Set", "set", "Sequence", "Mapping", "Iterable", "Iterator",
    "AsyncIterator", "AsyncGenerator", "Generator", "Optional", "Union", "Callable", "Awaitable", "Type", "Self",
    "Any", "None", "collections.abc.Mapping", "typing.Any", "typing.Optional",
}

## Matches one (possibly dotted) identifier in a type string, like `viam.proto.common.ResourceName` or `List`:
type_token_pattern = regex.compile(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*')


def shorten_data_type(t):
    if '.' in t:
        return '.'.join(t.split('.')[-2:])
    else:
        return t


class PythonParser:
    def __init__(self, proto_map_file, python_staging_url = None):
        self.proto_map_file = proto_map_file
        self.sdk_url = "https://python.viam.dev"

        if python_staging_url:
            self.scrape_url = python_staging_url
            self.staging = True
        else:
            self.scrape_url = "https://python.viam.dev"
            self.staging = False
        self.python_methods = {}
        self.object_index = None


    ## Load the Sphinx object inventory (objects.inv) of the Python SDK docs site, mapping each documented
    ## Python name (like `viam.components.arm.arm.Arm.TrajectoryPoint`) to its page anchor URL.
    ## Used to link types the signature itself leaves unlinked. For example, the SDK annotates arm methods with
    ## `viam.components.arm.Arm.Properties`, a re-export path Sphinx does not document, so the signature has no link
    ## even though the type is documented under its defining module:
    def load_object_index(self):
        if self.object_index is not None:
            return self.object_index
        self.object_index = {}
        try:
            req = Request(self.scrape_url + '/objects.inv', headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req, timeout=30).read()
            ## Header is four text lines, followed by a zlib-compressed body:
            pos = 0
            for _ in range(4):
                pos = data.index(b'\n', pos) + 1
            for line in zlib.decompress(data[pos:]).decode('utf-8').splitlines():
                match = regex.match(r'^(\S+)\s+py:(\w+)\s+-?\d+\s+(\S+)', line)
                if match and match.group(2) in ('class', 'type', 'data', 'exception', 'attribute'):
                    name, uri = match.group(1), match.group(3)
                    self.object_index[name] = self.sdk_url + '/' + uri.replace('$', name)
        except Exception as err:
            ## Fail the run rather than continue: without the index, every link that comes from it silently
            ## disappears from the regenerated pages, and the script would still exit 0.
            self.object_index = None
            raise RuntimeError(f'Could not load {self.scrape_url}/objects.inv ({type(err).__name__}: {err}). '
                               'Python type links depend on it; discard any generated output and rerun.') from err
        if not self.object_index:
            self.object_index = None
            raise RuntimeError(f'{self.scrape_url}/objects.inv contained no Python objects. '
                               'Python type links depend on it; discard any generated output and rerun.')
        return self.object_index


    ## Find the documented anchor for a dotted type name that the signature did not link:
    def resolve_type_link(self, name):
        index = self.load_object_index()
        if name in index:
            return index[name]

        ## Protobuf enums are annotated as `<Enum>.ValueType`, but the site documents the enum itself:
        if name.endswith('.ValueType') and name[:-len('.ValueType')] in index:
            return index[name[:-len('.ValueType')]]

        ## Match on the trailing segments: `viam.components.arm.Arm.Properties` -> `viam.components.arm.arm.Arm.Properties`.
        ## Qualified names must share their leading lowercase (package) segments; bare class names must match exactly one entry.
        segments = name.split('.')
        class_start = next((i for i, seg in enumerate(segments) if seg[:1].isupper()), None)
        if class_start is None:
            return None
        package = '.'.join(segments[:class_start]) + '.' if class_start > 0 else ''
        tail = '.' + '.'.join(segments[class_start:])
        candidates = [url for key, url in index.items() if key.startswith(package) and key.endswith(tail)]
        if len(candidates) == 1:
            return candidates[0]

        ## The reverse case: the annotation names the defining module (`viam.components.audio_out.audio_out.AudioInfo`)
        ## but the site documents the type at the package level (`viam.components.audio_out.AudioInfo`).
        ## Retry with the last module segment dropped:
        if class_start >= 2:
            shorter = '.'.join(segments[:class_start - 1] + segments[class_start:])
            if shorter in index:
                return index[shorter]
        return None


    ## Link each data type in a type string separately, leaving containers (List, Tuple, Mapping...) as plain text.
    ## Link sources, in priority order:
    ##   1. python_datatype_links: manually-mapped types (built-ins, and Viam types the site does not link),
    ##   2. anchors: links scraped from this signature or parameter description, matched by the type's exact text,
    ##   3. the site's objects.inv, for types the signature leaves unlinked.
    ## Returns the type string with Markdown links inserted. A type with no known link is left as plain text.
    def link_type(self, type_string, anchors):
        def link_token(match):
            token = match.group(0)
            if token in python_unlinked_types:
                return token
            if token in python_datatype_links:
                return '[' + shorten_data_type(token) + '](' + python_datatype_links[token] + ')'
            href = anchors.get(token)
            if href is None and ('.' in token or token[:1].isupper()):
                href = self.resolve_type_link(token)
            if href:
                return '[' + token + '](' + href + ')'
            return token

        return type_token_pattern.sub(link_token, type_string)


    ## `ValueTypes` as written in the hand-written do_command `command` type, linked when the site documents it:
    def link_value_types(self):
        url = self.resolve_type_link('viam.utils.ValueTypes')
        return '[ValueTypes](' + url + ')' if url else 'ValueTypes'


    ## Collect {link text: URL} for every internal reference link inside a scraped tag:
    def collect_anchors(self, *tags):
        anchors = {}
        for tag in tags:
            if tag is None:
                continue
            for link in tag.find_all('a', class_='reference internal'):
                href = link.get('href')
                text = link.text.strip()
                if href and text:
                    ## When staging locally, point at the public site rather than localhost:
                    if self.staging:
                        href = href.replace(self.scrape_url, self.sdk_url)
                    anchors.setdefault(text, href)
        return anchors


    def parse(self, type, viam_resources):
        self.python_methods[type] = {}

        for resource in viam_resources:
            self.python_methods[type][resource] = {}

            url = f"{self.scrape_url}/autoapi/viam/{type}s/{resource}/client/index.html"

            ## Determine URL form for Python depending on type (like 'component'):
            if type in ("component", "service") and resource in python_resource_overrides:
                url = f"{self.scrape_url}/autoapi/viam/{type}s/{python_resource_overrides[resource]}/client/index.html"
            elif resource == "world_state_store":
                url = f"{self.scrape_url}/autoapi/viam/services/worldstatestore/index.html"
            elif type in ("component", "service"):
                url = f"{self.scrape_url}/autoapi/viam/{type}s/{resource}/client/index.html"
            elif type == "app" and resource in python_resource_overrides:
                url = f"{self.scrape_url}/autoapi/viam/{type}/{python_resource_overrides[resource]}/index.html"
            elif type == "app":
                url = f"{self.scrape_url}/autoapi/viam/{type}/{resource}/index.html"
            else: # robot
                url = f"{self.scrape_url}/autoapi/viam/{type}/client/index.html"

            if resource == 'base_remote_control' or resource == 'data_manager':
                continue

            soup = make_soup(url)

            if soup:
                python_methods_raw = soup.find_all("dl", class_=["py method", "py property"])
            else:
                python_methods_raw = []

            ## Loop through scraped tags and select salient data:
            for tag in python_methods_raw:

                ## Create new empty dictionary for this specific method, to be appended to ongoing python_methods dictionary,
                ## in form: python_methods[type][resource][method_name] = this_method_dict
                this_method_dict = {}

                id = tag.find("dt", class_="sig sig-object py").get("id")

                if not id.endswith(".get_operation") \
                and not id.endswith(".from_proto") and not id.endswith(".to_proto") \
                and not id.endswith(".from_string") and not id.endswith("__") \
                and not id.endswith("HasField") and not id.endswith("WhichOneof") \
                and not id in python_ignore_apis:

                    ## Determine method name, but don't save to dictionary as value; we use it as a key instead:
                    method_name = id.rsplit('.',1)[1]

                    ## Look up method_name in proto_map file, and return matching proto:
                    with open(self.proto_map_file, 'r') as f:
                        for row in f:
                            if not row.startswith('#') \
                            and row.startswith(resource + ',') \
                            and row.split(',')[3] == method_name:
                                this_method_dict["proto"] = row.split(',')[1]

                    ## Determine method description, stripping newlines. If not present, skip:
                    if tag.find('dd').p:
                        this_method_dict["description"] = tag.find('dd').p.text.replace("\n", " ")

                    ## Determine method direct link, no need to parse for it, it's inferrable.
                    ## If we are scraping from a local staging instance, replace host and port with upstream link target URL:
                    if self.staging:
                        this_method_dict["method_link"] = str(url + "#" + id).replace(self.scrape_url, 'https://python.viam.dev')
                    else:
                        this_method_dict["method_link"] = url + "#" + id

                    ## Assemble array of all tags which contain parameters for this method:
                    ## METHODOLOGY: tag: em, class: sig-param, and not * or **kwargs:
                    parameter_tags = tag.find_all(
                        lambda tag: tag.name == 'em'
                        and tag.get('class') == ['sig-param']
                        and not regex.search(r'\*', tag.text))

                    if len(parameter_tags) != 0:

                        ## Create new empty dictionary for this_method_dict named "parameters":
                        this_method_dict["parameters"] = {}

                        # Iterate through each parameter found for this method:
                        for parameter_tag in parameter_tags:
                            ## Create new empty dictionary this_method_parameters_dict to house all parameter
                            ## keys for this method, to allow for multiple parameters. Also resets the
                            ## previous parameter's data when looping through multiple parameters:
                            this_method_parameters_dict = {}

                            ## Determine parameter name, but don't save to dictionary as value; we use it as a key instead:
                            param_name = parameter_tag.find('span', class_="pre").text

                            ## Determine parameter type:
                            param_type = parameter_tag.find_all('span', class_='n')[1].text

                            param_default = parameter_tag.select_one('span.default_value')
                            if param_default:
                                param_default = param_default.text
                            else:
                                param_default = None

                            ## A parameter is optional if and only if its signature gives it a default value
                            ## (for example `= False`, `= 0`, `= None`, `= ''`), whether positional or keyword-only.
                            ## A parameter typed `X | None` with no default is still required: the caller must pass it.
                            this_method_parameters_dict["optional"] = param_default is not None

                            ## Strip off ' | None' syntax for display, regardless of whether the parameter is optional:
                            if param_type.endswith(' | None'):
                                param_type = param_type.replace(' | None', "")

                            ## 'Extra' params do not appear in "Parameters" section (Except for PySDK > Motion Service),
                            ## so we must populate this param's content manually:
                            if param_name == 'extra':

                                this_method_parameters_dict["param_description"] = "Extra options to pass to the underlying RPC call."
                                this_method_parameters_dict["param_usage"] = "extra (Mapping[str, Any]) - Extra options to pass to the underlying RPC call."
                                this_method_parameters_dict["param_type"] = "Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]"

                            ## 'Timeout' params do not appear in "Parameters" section (Except for PySDK > Motion Service),
                            ## so we must populate this param's content manually:
                            elif param_name == 'timeout':

                                this_method_parameters_dict["param_description"] = "An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call."
                                this_method_parameters_dict["param_usage"] = "timeout (float) - An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call."
                                this_method_parameters_dict["param_type"] = "[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)"

                            ## Initial method usage syntax and Parameters section do not agree on param_type for do_command.
                            ## Manually override with correct values, for param 'command' only:
                            elif method_name == 'do_command' and param_name == 'command':

                                this_method_parameters_dict["param_description"] = "The command to execute"
                                this_method_parameters_dict["param_usage"] = "command (Mapping[str, ValueTypes]) – The command to execute"
                                this_method_parameters_dict["param_type"] = "Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), " + self.link_value_types() + "]"

                            else:

                                ## Link each data type in the type string separately (see link_type()). Link sources are the
                                ## manual python_datatype_links, then any links scraped from this parameter's signature or from
                                ## its entry in the "Parameters" section, then the site's objects.inv:
                                parameter_entry_tags = [strong_tag.parent for strong_tag in tag.find_all('strong') if strong_tag.text == param_name]
                                anchors = self.collect_anchors(parameter_tag, *parameter_entry_tags)
                                this_method_parameters_dict["param_type"] = self.link_type(param_type, anchors)

                                ## Get parameter usage and description, if method contains a "Parameters" section. Otherwise omit.
                                ## NOTE: We can't just use the initial param content as found above, because it does not contain descriptions,
                                ## and we can't just use this "Parameters" section, because it does not (usually) contain things like `extra` and `timeout`.
                                ## METHODOLOGY: Find parent <p> tag around matching <strong>param_name</strong> tag which contains this data.
                                ##   Determining by <strong> tags allows matching parameters regardless whether they are
                                ##   presented in <p> tags (single param) or <li> tags (multiple params):
                                for strong_tag in tag.find_all('strong'):
                                    ## We have to explicitly exclude extra and timeout from this loop also,
                                    ## because Python Motion service includes them explicitly as well:
                                    if param_name != 'extra' and \
                                        param_name != 'timeout' and \
                                        strong_tag.text == param_name:

                                        ## OPTION: Get just the parameter description, stripping all newlines:
                                        this_method_parameters_dict["param_description"] = regex.split(r" – ", strong_tag.parent.text)[1].replace("\n", " ")

                                        ## OPTION: Get full parameter usage string, stripping all newlines:
                                        ## NOTE: Currently unused.
                                        this_method_parameters_dict['param_usage'] = strong_tag.parent.text.replace("\n", " ")

                                        ## NOTE: Data type links from this Parameters entry were already collected above.

                            this_method_dict["parameters"][param_name] = this_method_parameters_dict


                    ## Parse return for this method:
                    ## METHODOLOGY: Some methods explicitly state that they return "None", others just omit the field.
                    ##   Either way, ensure we only write a return to this_method_dict if an actual return is present:
                    ## Get single tag containing the return for this method:
                    return_tag = tag.find('span', class_='sig-return')
                    if return_tag and return_tag.find('span', class_='pre').text != "None":

                        ## Create new empty dictionary for this_method_dict named "return":
                        this_method_dict["return"] = {}

                        ## OPTION: Get return_type by explicit key name:
                        return_type = return_tag.find('span', class_="sig-return-typehint").text
                        this_method_dict["return"]["return_type"] = return_type

                        ## Link each data type in the return type separately (see link_type()), using links scraped
                        ## from the return signature, then the manual python_datatype_links and the site's objects.inv:
                        this_method_dict["return"]["return_type"] = self.link_type(return_type, self.collect_anchors(return_tag))

                        ## OPTION: Get full return usage, including type info and html links if present, stripping all newlines:
                        ## NOTE: Currently unused.
                        this_method_dict["return"]["return_usage"] = str(return_tag.find('span', class_="sig-return-typehint")).replace("\n", " ")

                        ## Get return description from "Returns" section if present:
                        if tag.find(string="Returns"):

                            ## METHODOLOGY: Return description is always in <dd> tag with class either 'field-odd' or 'field-even',
                            ##   but this is the same as "Parameters" description. Returns differ by not being enclosed in <strong> tags:
                            return_description_raw = tag.find_all(
                                    lambda tag: tag.name == 'dd'
                                    and not tag.find_next('p').strong
                                    and (tag.get('class') == ['field-odd']
                                    or tag.get('class') == ['field-even']))

                            description_md = md(str(return_description_raw[0])).strip()
                            ## markdownify renders the <dd> wrapper as a Markdown definition, prefixing ':   ',
                            ## which would otherwise show up in the page as a stray ': :   ' after the type:
                            description_md = regex.sub(r'^:\s+', '', description_md)
                            description_md_stripped = description_md.replace("\n\n", "\n").replace("> *", "    *")
                            this_method_dict["return"]["return_description"] = description_md_stripped

                    ## If method has a "Raises" section, determine method errors raised:
                    if tag.find(string="Raises"):

                        ## Create new empty dictionary for this_method_dict named "raises",
                        ## and new empty dictionary this_method_raises_dict to house all errors raised
                        ## keys for this method, to allow for multiple errors raised:
                        this_method_dict["raises"] = {}

                        ## Iterate through all <strong> tags in method tag:
                        for strong_tag in tag.find_all('strong'):

                            ## Create new empty dictionary this_method_raises_dict to house all raises (errors)
                            ## keys for this method, to allow for multiple errors raised. Also resets the
                            ## previous error's data when looping through multiple errors:
                            this_method_raises_dict = {}

                            ## Determine if this <strong> tag is preceded by a <dt> tag containing the text "Raises". Otherwise omit.
                            ## METHODOLOGY: Find previous <dt> tag before matching <strong>param_name</strong> tag which contains this data.
                            ##   Determining by <strong> tags allows matching parameters regardless whether they are
                            ##   presented in <p> tags (single error raised) or <li> tags (multiple errors raised):
                            if strong_tag.find_previous('dt').text == "Raises:":

                                ## Split contained text at " - " to get first half, which is just the error name:
                                raises_name = regex.split(r" – ", strong_tag.parent.text)[0]

                                ## Process remaining data fields depending on whether the error data type is linked or not.
                                ## If the error includes a linked data type:
                                if strong_tag.parent.name == 'a':

                                    ## OPTION: Get full error raised usage, including type info and html links if present.
                                    ## NOTE: Currently unused.
                                    raises_usage = str(strong_tag.parent.parent).replace("\n", " ")
                                    raises_link = strong_tag.parent.get('href')

                                    ## Replace the scraped relative link with a full URL, in one of two forms:
                                    ## Scraped link is an anchor link:
                                    if raises_link.startswith('#'):
                                        this_method_raises_dict["raises_usage"] = regex.sub(r'href=".*"', 'href="' + url + raises_link + '"', raises_usage)
                                    ## Scraped link is a relative link:
                                    elif raises_link.startswith('../'):
                                        this_method_raises_dict["raises_usage"] = regex.sub(r'href=".*"', 'href="' + self.sdk_url + '/autoapi/viam/' + raises_link.replace('../', '') + '"', raises_usage)

                                    ## OPTION: Determine error raised description, stripping any newlines:
                                    this_method_raises_dict["raises_description"] = regex.split(r" – ", strong_tag.parent.parent.text)[1].replace("\n", " ")

                                ## If the error does not include a linked data type:
                                else:
                                    ## OPTION: Get full error raised usage:
                                    ## NOTE: Currently unused.
                                    this_method_raises_dict["raises_usage"] = str(strong_tag.parent).replace("\n", " ")

                                    ## OPTION: Determine error raised description, stripping any newlines:
                                    this_method_raises_dict["raises_description"] = regex.split(r" – ", strong_tag.parent.text)[1].replace("\n", " ")

                                ## Add all values for this raised error to this_method_dict by raises_name:
                                this_method_dict["raises"][raises_name] = this_method_raises_dict

                    #  This code is for properties, not methods
                    if tag.get("class") == ["py property"]:
                        return_elems = tag.find('dl', class_='field-list simple')
                        if return_elems:
                            return_elems_children = list(return_elems.children)
                            if return_elems_children and len(return_elems_children) > 7:
                                return_description = return_elems_children[3].text
                                return_type = md(str(return_elems_children[7])).strip()
                                this_method_dict["return"] = {}
                                this_method_dict["return"]["return_type"] = return_type
                                this_method_dict["return"]["return_description"] = return_description

                    ## Determine if a code sample is provided for this method:
                    if tag.find('div', class_="highlight"):

                        ## Fetch code sample raw text, preserving newlines but stripping all formatting.
                        ## This string should be suitable for feeding into any python formatter to get proper form:
                        this_method_dict["code_sample"] = tag.find('div', class_="highlight").pre.text

                    # For do_command, update the code sample to be more specific:
                    if method_name == "do_command":
                        if type == "service":
                            this_method_dict["code_sample"] = this_method_dict["code_sample"].replace("  # replace SERVICE with the appropriate class", "")
                            service_class = resource.title() + "Client"
                            if resource == "mlmodel":
                                service_class = "MLModelClient"
                            elif resource == "generic_service":
                                service_class = "Generic"
                            elif resource == "slam":
                                service_class = "SLAMClient"
                            this_method_dict["code_sample"] = this_method_dict["code_sample"].replace("SERVICE", service_class)
                            this_method_dict["code_sample"] = this_method_dict["code_sample"].replace("# Can be used with any resource, using the motion service as an example\n", "")
                            if not resource == "generic_service":
                                this_method_dict["code_sample"] = this_method_dict["code_sample"].replace("service", "my_{}_svc".format(resource))
                            if not resource in ["motion"]:
                                this_method_dict["code_sample"] = this_method_dict["code_sample"].replace("SERVICE", service_class).replace("builtin", "my_{}_svc".format(resource))
                        else:
                            if resource == "generic_component":
                                this_method_dict["code_sample"] = 'my_generic_component = Generic.from_robot(robot=machine, name="my_generic_component")\n' + this_method_dict["code_sample"].replace("component", "my_generic_component")
                            else:
                                this_method_dict["code_sample"] = 'my_{} = {}.from_robot(robot=machine, name="my_{}")\n'.format(resource, resource.title().replace("_", ""), resource) + this_method_dict["code_sample"].replace("component", "my_{}".format(resource))

                    # For get_geometries, update the code sample to be more specific:
                    if method_name == "get_geometries":
                        if type == "service":
                            if resource == "generic_service":
                                this_method_dict["code_sample"] = 'my_{} = {}.from_robot(robot=machine, name="my_{}")\n'.format(resource, resource.title(), resource) + this_method_dict["code_sample"].replace("component", "my_{}".format(resource))
                            else:
                                this_method_dict["code_sample"] = 'my_{} = {}.from_robot(robot=machine, name="my_{}_svc")\n'.format(resource, resource.title(), resource) + this_method_dict["code_sample"].replace("component", "my_{}_svc".format(resource))
                        else:
                            if resource == "generic_component":
                                this_method_dict["code_sample"] = 'my_generic_component = Generic.from_robot(robot=machine, name="my_generic_component")\n' + this_method_dict["code_sample"].replace("component", "my_generic_component")
                            elif resource == "input_controller":
                                this_method_dict["code_sample"] = 'my_controller = Controller.from_robot(robot=machine, name="my_controller")\n' + this_method_dict["code_sample"].replace("component", "my_controller")
                            else:
                                this_method_dict["code_sample"] = 'my_{} = {}.from_robot(robot=machine, name="my_{}")\n'.format(resource, resource.title().replace("_", ""), resource) + this_method_dict["code_sample"].replace("component", "my_{}".format(resource))

                    # For close, update the code sample to be more specific:
                    if method_name == "close":
                        if type == "service":
                            if resource == "generic_service":
                                this_method_dict["code_sample"] = 'my_{} = Generic.from_robot(robot=machine, name="my_{}")\nawait my_{}.close()\n'.format(resource, resource, resource)
                            elif resource == "mlmodel":
                                this_method_dict["code_sample"] = 'my_{}_svc = MLModelClient.from_robot(robot=machine, name="my_{}_svc")\nawait my_{}_svc.close()\n'.format(resource, resource, resource)
                            elif resource == "slam":
                                this_method_dict["code_sample"] = 'my_{}_svc = SLAMClient.from_robot(robot=machine, name="my_{}_svc")\nawait my_{}_svc.close()\n'.format(resource, resource, resource)
                            else:
                                this_method_dict["code_sample"] = 'my_{}_svc = {}Client.from_robot(robot=machine, name="my_{}_svc")\nawait my_{}_svc.close()\n'.format(resource, resource.title(), resource, resource)
                        elif type == "component":
                            if resource == "generic_component":
                                this_method_dict["code_sample"] = 'my_generic_component = Generic.from_robot(robot=machine, name="my_generic_component")\nawait my_generic_component.close()\n'
                            elif resource == "input_controller":
                                this_method_dict["code_sample"] = 'my_controller = Controller.from_robot(robot=machine, name="my_controller")\nawait my_controller.close()\n'
                            else:
                                this_method_dict["code_sample"] = 'my_{} = {}.from_robot(robot=machine, name="my_{}")\nawait my_{}.close()\n'.format(resource, resource.title().replace("_", ""), resource, resource)

                    # For get_resource_name, update the code sample to be more specific:
                    if method_name == "get_resource_name":
                        if type == "service":
                            service_class = resource.title().replace('_','') + "Client"
                            if resource == "mlmodel":
                                service_class = "MLModelClient"
                            elif resource == "generic_service":
                                service_class = "Generic"
                            elif resource == "slam":
                                service_class = "SLAMClient"
                            if resource == "generic_service":
                                this_method_dict["code_sample"] = 'my_{}_name = {}.get_resource_name("my_{}")\n'.format(resource, service_class ,resource)
                            else:
                                this_method_dict["code_sample"] = 'my_{}_svc_name = {}.get_resource_name("my_{}_svc")\n'.format(resource, service_class ,resource)
                        else:
                            if resource == "input_controller":
                                this_method_dict["code_sample"] = 'my_input_controller_name = Controller.get_resource_name("my_input_controller")\n'
                            elif resource == "generic_component":
                                this_method_dict["code_sample"] = 'my_generic_component_name = Generic.get_resource_name("my_generic_component")\n'
                            else:
                                this_method_dict["code_sample"] = 'my_{}_name = {}.get_resource_name("my_{}")\n'.format(resource, resource.title().replace('_','') ,resource)

                    ## We have finished collecting all data for this method. Write the this_method_dict dictionary
                    ## in its entirety to the python_methods dictionary by type (like 'component'), by resource (like 'arm'),
                    ## using the method_name as key:

                    self.python_methods[type][resource][method_name] = this_method_dict

        ## We have finished looping through all scraped Python methods. Write the python_methods dictionary
        ## in its entirety to the all_methods dictionary using "python" as the key:
        return self.python_methods

