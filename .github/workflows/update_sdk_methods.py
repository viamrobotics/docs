from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import markdownify
import urllib.parse
import urllib.error
import re as regex
import argparse


## Set the full list of SDK langauges we scrape here:
sdks_supported = ["go", "python", "flutter"]

## Parse arguments passed to update_sdk_methods.py.
## You can either provide the specific sdk languages to run against
## as a comma-separated list, or omit entirely to run againt all sdks_supported:
parser = argparse.ArgumentParser()

parser.add_argument('sdk_language', type=str, nargs='?', help="A comma-separated list of the sdks to run against. \
                     Can be one of: go, python, flutter. Omit to run against all sdks.")

## Quick sanity check of provided sdk languages. If all is well,
## assemble sdks array to iterate through:
args = parser.parse_args()
if args.sdk_language is not None:
    sdk_langs = [s.strip() for s in args.sdk_language.split(",")]

    sdks = []
    for sdk_lang in sdk_langs:
    
        if sdk_lang not in sdks_supported:
            print("ERROR: Unsupported SDK language: " + sdk_lang)
            print("Exiting ...")
            exit(1)
        else:
            sdks.append(sdk_lang)
else:
    sdks = sdks_supported

## Array mapping language to its root URL:
sdk_url_mapping = {
    "go": "https://pkg.go.dev",
    "python": "https://python.viam.dev",
    "cpp": "https://cpp.viam.dev",
    "typescript": "https://ts.viam.dev",
    "flutter": "https://flutter.viam.dev"
}

## Arrays of resources to scrape, by type:
## type = ["array", "of", "resources"]
components = ["arm", "base", "board", "camera", "encoder", "gantry", "generic_component", "gripper",
              "input_controller", "motor", "movement_sensor", "power_sensor", "sensor"]
services = ["generic_service", "mlmodel", "motion", "navigation", "slam", "vision"]
app_apis = ["app", "data", "mltraining"]
robot_apis = ["robot"]

## Dictionary of proto API names, with empty methods array, to be filled in for later use by get_proto_apis():
proto_map = {
    "arm": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/arm/v1/arm_grpc.pb.go",
        "name": "ArmServiceClient",
        "methods": []
    },
    "base": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/base/v1/base_grpc.pb.go",
        "name": "BaseServiceClient",
        "methods": []
    },
    "board": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/board/v1/board_grpc.pb.go",
        "name": "BoardServiceClient",
        "methods": []
    },
    "camera": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/camera/v1/camera_grpc.pb.go",
        "name": "CameraServiceClient",
        "methods": []
    },
    "encoder": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/encoder/v1/encoder_grpc.pb.go",
        "name": "EncoderServiceClient",
        "methods": []
    },
    "gantry": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/gantry/v1/gantry_grpc.pb.go",
        "name": "GantryServiceClient",
        "methods": []
    },
    "generic_component": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/generic/v1/generic_grpc.pb.go",
        "name": "GenericServiceClient",
        "methods": []
    },
    "gripper": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/gripper/v1/gripper_grpc.pb.go",
        "name": "GripperServiceClient",
        "methods": []
    },
    "input_controller": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/inputcontroller/v1/input_controller_grpc.pb.go",
        "name": "InputControllerServiceClient",
        "methods": []
    },
    "motor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/motor/v1/motor_grpc.pb.go",
        "name": "MotorServiceClient",
        "methods": []
    },
    "movement_sensor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/movementsensor/v1/movementsensor_grpc.pb.go",
        "name": "MovementSensorServiceClient",
        "methods": []
    },
    "power_sensor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/powersensor/v1/powersensor_grpc.pb.go",
        "name": "PowerSensorServiceClient",
        "methods": []
    },
    "sensor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/sensor/v1/sensor_grpc.pb.go",
        "name": "SensorServiceClient",
        "methods": []
    },
    "generic_service": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/generic/v1/generic_grpc.pb.go",
        "name": "GenericServiceClient",
        "methods": []
    },
    "mlmodel": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/mlmodel/v1/mlmodel_grpc.pb.go",
        "name": "MLModelServiceClient",
        "methods": []
    },
    "motion": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/motion/v1/motion_grpc.pb.go",
        "name": "MotionServiceClient",
        "methods": []
    },
    "navigation": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/navigation/v1/navigation_grpc.pb.go",
        "name": "NavigationServiceClient",
        "methods": []
    },
    "slam": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/slam/v1/slam_grpc.pb.go",
        "name": "SLAMServiceClient",
        "methods": []
    },
    "vision": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/vision/v1/vision_grpc.pb.go",
        "name": "VisionServiceClient",
        "methods": []
    },
    "app": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/v1/app_grpc.pb.go",
        "name": "AppServiceClient",
        "methods": []
    },
    "data": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/data/v1/data_grpc.pb.go",
        "name": "DataServiceClient",
        "methods": []
    },
    "robot": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/robot/v1/robot_grpc.pb.go",
        "name": "RobotServiceClient",
        "methods": []
    },
    "mltraining": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/mltraining/v1/ml_training_grpc.pb.go",
        "name": "MLTrainingServiceClient",
        "methods": []
    }
}

## Language-specific resource name overrides:
##   "proto_resource_name" : "language-specific_resource_name"
##   "as-it-appears-in-type-array": "as-it-is-used-per-sdk"
## Note: Always remap generic component and service, for all languages,
##       as this must be unique for this script, but is non-unique across sdks.
go_resource_overrides = {
    "generic_component": "generic",
    "input_controller": "input",
    "movement_sensor": "movementsensor",
    "power_sensor": "powersensor",
    "generic_service": "generic"
}

## Ignore these specific APIs if they error, are deprecated, etc:
go_ignore_apis = []

## Use these URLs for data types (for params, returns, and errors raised) that are
## built-in to the language or provided by a non-Viam third-party package:
## TODO: Not currently using these in parse(), but could do a simple replace()
##       or could handle in markdownification instead. TBD.
go_datatype_links = {
    "context": "https://pkg.go.dev/context",
    "map": "https://go.dev/blog/maps",
    "bool": "https://pkg.go.dev/builtin#bool",
    "int": "https://pkg.go.dev/builtin#int",
    "float64": "https://pkg.go.dev/builtin#float64",
    "image": "https://pkg.go.dev/image#Image",
    "r3.vector": "https://pkg.go.dev/github.com/golang/geo/r3#Vector",
    "string": "https://pkg.go.dev/builtin#string",
    "*geo.Point": "https://pkg.go.dev/github.com/kellydunn/golang-geo#Point",
    "primitive.ObjectID": "https://pkg.go.dev/go.mongodb.org/mongo-driver/bson/primitive#ObjectID",
    "error": "https://pkg.go.dev/builtin#error"
}

## Language-specific resource name overrides:
python_resource_overrides = {
    "generic_component": "generic",
    "input_controller": "input",
    "generic_service": "generic",
    "data": "data_client",
    "app": "app_client",
    "data": "data_client",
    "mltraining": "ml_training_client"
}

## Ignore these specific APIs if they error, are deprecated, etc:
python_ignore_apis = [
    'viam.app.app_client.AppClient.create_organization',
    'viam.app.app_client.AppClient.delete_organization',
    'viam.app.app_client.AppClient.list_organizations_by_user',
    'viam.app.app_client.AppClient.get_rover_rental_parts',
    'viam.app.app_client.AppClient.share_location',
    'viam.app.app_client.AppClient.unshare_location',
    'viam.app.data_client.DataClient.configure_database_user',
    'viam.app.data_client.DataClient.create_filter',
    'viam.app.ml_training_client.MLTrainingClient.submit_training_job',
    'viam.robot.client.RobotClient.transform_point_cloud'
]

## Use these URLs for data types that are built-in to the language:
python_datatype_links = {
    "str": "https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str",
    "int": "https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex",
    "float": "https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex",
    "bytes": "https://docs.python.org/3/library/stdtypes.html#bytes-objects",
    "bool": "https://docs.python.org/3/library/stdtypes.html#boolean-type-bool",
    "list": "https://docs.python.org/3/library/stdtypes.html#typesseq-list",
    "tuple": "https://docs.python.org/3/library/stdtypes.html#tuples",
    "datetime": "https://docs.python.org/3/library/datetime.html"
}

## Inject these URLs, relative to 'docs', into param descriptions that contain exact matching key text:
## This is an example, for https://docs.viam.com/mobility/frame-system/#transformpose, that the
## markdownification step could use to linkify matching text when it goes to write param_desc markdown.
## Otherwise we have to overwrite param_desc with verbatim upstream copy, which would overwrite
## any docs-site-only links presently in our copy.
python_param_description_links = {
    "additional transforms": "/mobility/frame-system/#additional-transforms"
}

## Language-specific resource name overrides:
flutter_resource_overrides = {
    "generic_component": "generic",
    "movement_sensor": "movementsensor",
    "power_sensor": "powersensor",
    "generic_service": "generic",
    "mltraining": "ml_training"
}

## Ignore these specific APIs if they error, are deprecated, etc:
flutter_ignore_apis = []

## Use these URLs for data types that are built-in to the language:
flutter_datatype_links = {}

## Fetch canonical Proto method names.
## Required by Flutter parsing, not used by Python or Go parsing yet (see comments in parse())
def get_proto_apis():
    for api in proto_map.keys():
        api_url = proto_map[api]["url"]
        api_name = proto_map[api]["name"]

        api_page = urlopen(api_url)
        api_html = api_page.read().decode("utf-8")

        ## protos are presented in plaintext, so we must match by expected raw text:
        proto_regex = 'type ' + regex.escape(api_name) + '[^{]*\{([^}]+)\}'
        search = regex.search(proto_regex, api_html)
        match_output = search.group()
        split = match_output.splitlines()

        for line in split:
            line = line.strip()
            if line[0].isupper():
                separator = "("
                line = line.split(separator, 1)[0]
                ## Append to proto_map for use later:
                proto_map[api]["methods"].append(line)
   
    return proto_map

## bs4 scraper wrapper used frequently in parse():
def make_soup(url):
   try:
       page = urlopen(url)
       html = page.read().decode("utf-8")
       return BeautifulSoup(html, "html.parser")
   except urllib.error.HTTPError as err:
       print(f'An HTTPError was thrown: {err.code} {err.reason} for URL: {url}')

## Fetch sdk documentations for each language in sdks array, by language, by type, by resource, by method.
def parse(type, names):

## TODO:
## - Unify returned method object form. Currently returning raw method usage for Go, and by-param, by-return (and by-raise)
##   breakdown for each method for Python and Flutter. Let's chat about which is useful, and which I should throw away.
##   Raw usage is I think how check_python_methods.py currently does it. Happy to convert Flutter and Py to dump raw usage,
##   if you don't need the per-param,per-return,per-raise stuff.
## - Currently manually adding param details for 'extra' and 'timeout' params for Python. There might be more like this,
##   that need this same manual treatment, that I haven't found yet.
## - Edge cases (like bad sdk language, or Go App API DNE) just print for now, need to make into errors.

    ## This parent dictionary will contain all dictionaries:
    ## all_methods[sdk][type][resource]
    all_methods = {}

    ## Iterate through each sdk (like 'python') in sdks array:
    for sdk in sdks:

        ## Build empty dict to house methods:
        if sdk == "go":
            go_methods = {}
            go_methods[type] = {}
        elif sdk == "python":
            python_methods = {}
            python_methods[type] = {}
        elif sdk == "flutter":
            flutter_methods = {}
            flutter_methods[type] = {}
        else:
            print("unsupported language!")

        ## Determine SDK URL based on resource type:
        sdk_url = sdk_url_mapping[sdk]

        ## Iterate through each resource (like 'arm') in type (like 'components') array:
        for resource in names:

            ## Determine URL form for Go depending on type (like 'component'):
            if sdk == "go":
                if type in ("component", "service") and resource in go_resource_overrides:
                    url = f"{sdk_url}/go.viam.com/rdk/{type}s/{go_resource_overrides[resource]}"
                elif type in ("component", "service"):
                    url = f"{sdk_url}/go.viam.com/rdk/{type}s/{resource}"
                elif type == "robot" and resource in go_resource_overrides:
                    url = f"{sdk_url}/go.viam.com/rdk/{type}/{go_resource_overrides[resource]}"
                elif type == "robot":
                    url = f"{sdk_url}/go.viam.com/rdk/{type}"
                elif type == "app":
                    print("GO SDK has no APP API!")
                go_methods[type][resource] = {}

            ## Determine URL form for Python depending on type (like 'component'):
            elif sdk == "python":
                if type in ("component", "service") and resource in python_resource_overrides:
                    url = f"{sdk_url}/autoapi/viam/{type}s/{python_resource_overrides[resource]}/client/index.html"
                elif type in ("component", "service"):
                    url = f"{sdk_url}/autoapi/viam/{type}s/{resource}/client/index.html"
                elif type == "app" and resource in python_resource_overrides:
                    url = f"{sdk_url}/autoapi/viam/{type}/{python_resource_overrides[resource]}/index.html"
                elif type == "app":
                    url = f"{sdk_url}/autoapi/viam/{type}/{resource}/index.html"
                else: # robot
                    url = f"{sdk_url}/autoapi/viam/{type}/client/index.html"
                python_methods[type][resource] = {}

            ## Determine URL form for Flutter depending on type (like 'component'):
            elif sdk == "flutter":
                if resource in flutter_resource_overrides:
                    url = f"{sdk_url}/viam_protos.{type}.{flutter_resource_overrides[resource]}/{proto_map[resource]['name']}-class.html"
                else:
                    url = f"{sdk_url}/viam_protos.{type}.{resource}/{proto_map[resource]['name']}-class.html"
                flutter_methods[type][resource] = {}
            ## If an invalid langauge was provided:
            else:
                print("unsupported language!")

            ## Scrape each parent method tag and all contained child tags for Go by resource:
            if sdk == "go" and type != "app":

                soup = make_soup(url)

                ## Get a raw dump of all go methods by interface for each resource:
                go_methods_raw = soup.find_all(
                    lambda tag: tag.name == 'div'
                    and tag.get('class') == ['Documentation-declaration']
                    and "type" in tag.pre.text
                    and "interface {" in tag.pre.text)

                # some resources have more than one interface:
                for resource_interface in go_methods_raw:

                    ## Determine the interface name, which we need for the method_link:
                    interface_name = resource_interface.find('pre').text.splitlines()[0].removeprefix('type ').removesuffix(' interface {')
                    #print(interface_name)

                    ## Loop through each method found for this interface:
                    for tag in resource_interface.find_all('span', attrs={"data-kind" : "method"}):

                        ## Create new empty dictionary for this specific method, to be appended to ongoing go_methods dictionary,
                        ## in form: go_methods[type][resource][method_name] = this_method_dict
                        this_method_dict = {}

                        tag_id = tag.get('id')
                        method_name = tag.get('id').split('.')[1]

                        ## Determine method proto, placeholder for now:
                        this_method_dict["proto"] = ""

                        ## Extract the raw text from resource_interface matching method_name.
                        ## Split by method span, throwing out remainder of span tag, catching cases where
                        ## id is first attr or data-kind is first attr, and slicing to omit the first match,
                        ## which is the opening of the method span tag, not needed:
                        this_method_raw1 = regex.split(r'id="' + tag_id + '"', str(resource_interface))[1].removeprefix('>').removeprefix(' data-kind="method">').lstrip()

                        ## Then, omit all text that begins a new method span, and additionally remove trailing
                        ## element closers for earlier tags we spliced into (pre and span):
                        this_method_raw2 = regex.split(r'<span .*data-kind="method".*>', this_method_raw1)[0].removesuffix('}</pre>\n</div>').removesuffix('</span>').rstrip()

                        method_description = ""

                        ## Get method description, if any comment spans are found:
                        if tag.find('span', class_='comment'):

                            ## Iterate through all comment spans, splitting by opening comment tag, and
                            ## omitting the first string, which is either the opening comment tag itself,
                            ## or the usage of this method, if the comment is appended to the end of usage line:
                            for comment in regex.split(r'<span class="comment">', this_method_raw2)[1:]:
                             
                                comment_raw = regex.split(r'</span>.*', comment.removeprefix('//'))[0].lstrip()
                                method_description = method_description + comment_raw

                        ## Write comment field as appended comments if found, or empty string if none.
                        this_method_dict["description"] = method_description

                        ## Get full method usage string, by omitting all comment spans:
                        method_usage_raw = regex.sub(r'<span class="comment">.*</span>', '', this_method_raw2)
                        this_method_dict["usage"] = regex.sub(r'</span>', '', method_usage_raw).lstrip().rstrip()

                        ## Not possible to link to the specific functions, so we link to the parent resource instead:
                        this_method_dict["link"] = url + '#' + interface_name

                        ## We have finished collecting all data for this method. Write the this_method_dict dictionary
                        ## in its entirety to the go_methods dictionary by type (like 'component'), by resource (like 'arm'),
                        ## using the method_name as key:
                        go_methods[type][resource][method_name] = this_method_dict
                
                ## We have finished looping through all scraped Go methods. Write the go_methods dictionary
                ## in its entirety to the all_methods dictionary using "go" as the key:
                all_methods["go"] = go_methods


            elif sdk == "go" and type == "app":
               print("Go has no APP API!")

            ## Scrape each parent method tag and all contained child tags for Python by resource:
            elif sdk == "python":
                soup = make_soup(url)
                python_methods_raw = soup.find_all("dl", class_="py method")

                ## Loop through scraped tags and select salient data:
                for tag in python_methods_raw:

                    ## Create new empty dictionary for this specific method, to be appended to ongoing python_methods dictionary,
                    ## in form: python_methods[type][resource][method_name] = this_method_dict
                    this_method_dict = {}

                    id = tag.find("dt", class_="sig sig-object py").get("id")

                    if not id.endswith(".from_robot") and not id.endswith(".get_resource_name") \
                    and not id.endswith(".get_operation") and not id.endswith(".from_proto") \
                    and not id.endswith("__") and not id.endswith("HasField") \
                    and not id.endswith("WhichOneof") and not id in python_ignore_apis:

                        ## Determine method name, but don't save to dictionary as value; we use it as a key instead:
                        method_name = id.rsplit('.',1)[1]

                        ## Experimental attempt to match to proto. ~66% accurate so far, needs more work:
                        #method_proto_raw = method_name.split("_")
                        #method_proto=""
                        #for method_part in method_proto_raw:
                        #    method_part = method_part[0].upper() + method_part[1:]
                        #    method_proto += method_part
                        #print(method_proto)

                        #if method_proto not in proto_map[resource]["methods"]:
                        #    try_method_proto = method_proto[3:]
                        #    print(try_method_proto)

                        #    if try_method_proto not in proto_map[resource]["methods"]:
                        #        print("WARNING: " + method_proto + " NOT FOUND!!!")

                        ## Also experimenting with, __mapping__ object, example:
                        ## https://python.viam.dev/_modules/viam/gen/component/arm/v1/arm_grpc.html#ArmServiceBase.__mapping__

                        ## Determine method proto, placeholder for now:
                        this_method_dict["proto"] = ""

                        ## Determine method description, stripping newlines:
                        this_method_dict["description"] = tag.find('dd').p.text.replace("\n", " ")

                        ## Determine method direct link, no need to parse for it, it's inferrable: 
                        this_method_dict["method_link"] = url + "#" + id

                        ## Assemble array of all tags which contain parameters for this method:
                        ## METHODOLOGY: tag: em, class: sig-param, and not * or **kwargs:
                        parameter_tags = tag.find_all(
                            lambda tag: tag.name == 'em'
                            and tag.get('class') == ['sig-param']
                            and not regex.search('\*', tag.text))

                        ## Create new empty dictionary for this_method_dict named "parameters",
                        ## and new empty dictionary this_method_parameters_dict to house all parameter
                        ## keys for this method, to allow for multiple parameters:
                        this_method_dict["parameters"] = {}
                        this_method_parameters_dict = {}

                        # Iterate through each parameter found for this method:
                        for parameter_tag in parameter_tags:

                            ## Determine parameter name, but don't save to dictionary as value; we use it as a key instead:
                            param_name = parameter_tag.find('span', class_="pre").text

                            ## Determine parameter type. delete_fragment() is missing a data type upstream, so
                            ## we provide it manually here for now. Expect an upstream PR!
                            if method_name != "delete_fragment":
                                param_type = parameter_tag.find_all('span', class_='n')[1].text
                                this_method_parameters_dict["param_type"] = param_type
                            else:
                                ## Missing data type for viam.app.app_client.AppClient.delete_fragment :: fragment_id should be str:
                                param_type = "str"
                                this_method_parameters_dict["param_type"] = param_type

                            ## Determine if this parameter is optional, and strip off ' | None' syntax if so:
                            if param_type.endswith(' | None'):
                                this_method_parameters_dict["optional"] = True
                                param_type = param_type.replace(' | None', "")
                                this_method_parameters_dict["param_type"] = param_type
                            else:
                                this_method_parameters_dict["optional"] = False

                            ## Determine if this parameter has a parameter type link. Include if so, otherwise omit:
                            if parameter_tag.find('a', class_="reference internal"):
                                param_type_link_raw = parameter_tag.find('a', class_="reference internal").get("href")
                                ## Parameter type link is an anchor link:
                                if param_type_link_raw.startswith('#'):
                                    this_method_parameters_dict["param_type_link"] = url + param_type_link_raw
                                ## Parameter type link is a relative link:
                                elif param_type_link_raw.startswith('../../'):
                                    this_method_parameters_dict["param_type_link"] = sdk_url + "/autoapi/viam/" + param_type_link_raw.replace('../../', '')

                            ## Determine if this parameter has a description, if method contains a "Parameters" section. Otherwise omit.
                            ## NOTE: We can't just use the initial param content as found above, because it does not contain descriptions,
                            ## and we can't just use this "Parameters" section, because it does not always contain things like `extra` and `timeout`.
                            ## METHODOLOGY: Find parent <p> tag around matching <strong>param_name</strong> tag which contains this data.
                            ##   Determining by <strong> tags allows matching parameters regardless whether they are
                            ##   presented in <p> tags (single param) or <li> tags (multiple params):
                            for strong_tag in tag.find_all('strong'):
                                if strong_tag.text == param_name:
                                    this_method_parameters_dict["param_description"] = regex.split(r" – ", strong_tag.parent.text)[1]
                                    ## ALTERNATIVE: Get full desc, including type info.
                                    ## Might be useful for alternate approach to markdownification, if desired!
                                    ## Not currently used:
                                    param_desc_raw = strong_tag.parent.text

                                ## 'Extra' params do not appear in "Parameters" section, adding manually:
                                elif strong_tag.text == "extra":
                                    this_method_parameters_dict["param_description"] = "Extra options to pass to the underlying RPC call."

                                ## 'Timeout' params do not appear in "Parameters" section, adding manually:
                                elif strong_tag.text == "timeout":
                                    this_method_parameters_dict["param_description"] = "An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call."

                                ## Unable to determine parameter description, not timeout or extra.
                                ## Usually a non-param, but if we are missing expected param descriptions, expand this section to catch them.
                                else:
                                    ## No-op:
                                    pass

                            ## Add all values for this parameter to this_method_dict by param_name:
                            this_method_dict["parameters"][param_name] = this_method_parameters_dict

                        ## Get single tag containing the return for this method:
                        ## While a few methods have "multiple returns" (example: list_organization_members), they are treated as a single
                        ## return as far as the HTML elements go, so treating them as singular here as well:
                        return_tag = tag.find('span', class_='sig-return')

                        ## Create new empty dictionary for this_method_dict named "return":
                        this_method_dict["return"] = {}

                        ## Parse return for this method:
                        ## METHODOLOGY: Some methods explicitly state that they return "None", others just omit the field.
                        ##   Either way, ensure we only write a return to this_method_dict if an actual return is present:
                        if return_tag and return_tag.find('span', class_='pre').text != "None":

                            return_type = return_tag.find('span', class_="sig-return-typehint").text

                            ## ALTERNATIVE: Get full return, including type info and html links if present.
                            ## Might be useful for alternate approach to markdownification, if desired!
                            ## Not currently used:
                            return_type_raw = return_tag.find('span', class_="sig-return-typehint")

                            ## Add return_type to this_method_dict by explicit key name:
                            this_method_dict["return"]["return_type"] = return_type

                            ## Get return description from "Returns" section if present:
                            if tag.find(string="Returns"):

                                ## METHODOLOGY: Return description is always in <dd> tag with class either 'field-odd' or 'field-even',
                                ##   but this is the same as "Parameters" description. Returns differ by not being enclosed in <strong> tags:
                                return_description_raw = tag.find_all(
                                       lambda tag: tag.name == 'dd'
                                       and not tag.find_next('p').strong
                                       and (tag.get('class') == ['field-odd']
                                       or tag.get('class') == ['field-even']))

                                ## Append to ongoing this_method_dict, stripping both leading and trailing newlines:
                                this_method_dict["return"]["return_description"] = return_description_raw[0].p.text.lstrip().rstrip()

                        ## If method has a "Raises" section, determine method errors raised:
                        if tag.find(string="Raises"):

                            ## Create new empty dictionary for this_method_dict named "raises",
                            ## and new empty dictionary this_method_raises_dict to house all errors raised
                            ## keys for this method, to allow for multiple errors raised:
                            this_method_dict["raises"] = {}
                            this_method_raises_dict = {}

                            ## Iterate through all <strong> tags in method tag:
                            for strong_tag in tag.find_all('strong'):
                                ## Determine if this <strong> tag is preceeded by a <dt> tag containing the text "Raises". Otherwise omit.
                                ## METHODOLOGY: Find previous <dt> tag before matching <strong>param_name</strong> tag which contains this data.
                                ##   Determining by <strong> tags allows matching parameters regardless whether they are
                                ##   presented in <p> tags (single error raised) or <li> tags (multiple errors raised):
                                if strong_tag.find_previous('dt').text == "Raises:":

                                    ## Split contained text at " - " to get first half, which is just the error name:
                                    raises_name = regex.split(r" – ", strong_tag.parent.text)[0]

                                     ## ALTERNATIVE: Get full error raised, including type info and html links if present.
                                     ## Might be useful for alternate approach to markdownification, if desired!
                                     ## Not currently used:
                                    raises_desc_raw = strong_tag.parent.text

                                    ## Determine error raised description, and append to this_method_raises_dict by explicit key name:
                                    this_method_raises_dict["raises_description"] = regex.split(r" – ", strong_tag.parent.text)[1]

                                    ## Add all values for this raised error to this_method_dict by raises_name:
                                    this_method_dict["raises"][raises_name] = this_method_raises_dict

                        ## Determine if a code sample is provided for this method:
                        if tag.find('div', class_="highlight"):

                            ## Fetch code sample raw text, preserving newlines but stripping all formatting.
                            ## This string should be suitable for feeding into any python formatter to get proper form:
                            this_method_dict["code_sample"] = tag.find('div', class_="highlight").pre.text

                        ## We have finished collecting all data for this method. Write the this_method_dict dictionary
                        ## in its entirety to the python_methods dictionary by type (like 'component'), by resource (like 'arm'),
                        ## using the method_name as key:
                        python_methods[type][resource][method_name] = this_method_dict
                
                ## We have finished looping through all scraped Python methods. Write the python_methods dictionary
                ## in its entirety to the all_methods dictionary using "python" as the key:
                all_methods["python"] = python_methods

            ## Scrape each parent method tag and all contained child tags for Flutter by resource:
            ## TODO: Better code comments for Flutter
            elif sdk == "flutter":
                soup = make_soup(url)
                ## Limit matched class to exactly 'callable', i.e. not 'callable inherited', remove the constructor (proto id) itself, and remove '*_Pre' methods from Robot API:
                flutter_methods_raw = soup.find_all(
                    lambda tag: tag.name == 'dt'
                    and tag.get('class') == ['callable']
                    and not regex.search(proto_map[resource]['name'], tag.text)
                    and not regex.search('_Pre', tag.text))

                ## Loop through scraped tags and select salient data:
                for tag in flutter_methods_raw:

                    this_method_dict = {}

                    method_name = tag.get('id')

                    ## Temporary placeholder for mapping to proto:
                    this_method_dict["proto"] = ""

                    this_method_dict["method_link"] = tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                    ## Flutter SDK puts all parameter detail on a separate params page that we must additionally make_soup on:
                    parameters_link = tag.find("span", class_="type-annotation").a['href'].replace("..", sdk_url)
                    parameters_soup_raw = make_soup(parameters_link)
                    parameters_soup = parameters_soup_raw.find_all(
                        lambda tag: tag.name == 'dt'
                        and tag.get('class') == ['property']
                        and not regex.search('info_', tag.text))

                    this_method_dict["parameters"] = {}
                    this_method_parameters_dict = {}
                    this_method_dict["returns"] = {}
                    this_method_returns_dict = {}

                    # Parse parameters:
                    for parameter_tag in parameters_soup:

                        param_name = parameter_tag.get('id')
                        this_method_parameters_dict["param_link"] = parameter_tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                        parameter_type_raw = parameter_tag.find("span", class_="signature")

                        if not parameter_type_raw.find("a"):
                            this_method_parameters_dict["param_type"] = parameter_type_raw.string[2:]
                        elif len(parameter_type_raw.find_all("a")) == 1:
                            this_method_parameters_dict["param_type"] = parameter_type_raw.find("a").text
                            this_method_parameters_dict["param_type_link"] = parameter_type_raw.a['href'].replace("..", sdk_url)
                        elif len(parameter_type_raw.find_all("a")) == 2:
                            this_method_parameters_dict["param_type"] = parameter_type_raw.find("a").text
                            this_method_parameters_dict["param_type_link"] = parameter_type_raw.a['href'].replace("..", sdk_url)
                            this_method_parameters_dict["param_subtype"] = parameter_type_raw.find("span", class_="type-parameter").text
                            this_method_parameters_dict["param_subtype_link"] = parameter_type_raw.find("span", class_="type-parameter").a['href'].replace("..", sdk_url)

                        this_method_dict["parameters"][param_name] = this_method_parameters_dict

                    # Parse returns:
                    if tag.find("span", class_="type-parameter").a:

                        returns_link = tag.find("span", class_="type-parameter").a['href'].replace("..", sdk_url)
                        returns_soup_raw = make_soup(returns_link)
                        returns_soup = returns_soup_raw.find_all(
                            lambda tag: tag.name == 'dt'
                            and tag.get('class') == ['property']
                            and not regex.search('info_', tag.text))

                        for return_tag in returns_soup:
                            return_name = return_tag.get('id')
                            this_method_returns_dict["return_link"] = return_tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                            return_type_raw = return_tag.find("span", class_="signature")

                            if not return_type_raw.find("a"):
                                this_method_returns_dict["return_type"] = return_type_raw.string[2:]
                            elif len(return_type_raw.find_all("a")) == 1:
                                this_method_returns_dict["return_type"] = return_type_raw.find("a").text
                                this_method_returns_dict["return_type_link"] = return_type_raw.a['href'].replace("..", sdk_url)
                            elif len(return_type_raw.find_all("a")) == 2:
                                this_method_returns_dict["return_type"] = return_type_raw.find("a").text
                                this_method_returns_dict["return_type_link"] = return_type_raw.a['href'].replace("..", sdk_url)
                                this_method_returns_dict["return_subtype"] = return_type_raw.find("span", class_="type-parameter").text
                                this_method_returns_dict["return_subtype_link"] = return_type_raw.find("span", class_="type-parameter").a['href'].replace("..", sdk_url)

                            this_method_dict["returns"][return_name] = this_method_returns_dict

                    else:
                        return_name = return_tag.get('id')
                        this_method_returns_dict["return_type"] = tag.find("span", class_="type-parameter").string

                    flutter_methods[type][resource][method_name] = this_method_dict

                all_methods["flutter"] = flutter_methods

            else:
                print("unsupported language!")

    return all_methods

## TODO:
## This is where we define our markdownify function.
## TODO TODO: Better mock up of this function from andf!!!!
## - Separated from `parse()`, with goal of being as language-agnostic as possible: parse per-language (for now) with markdownify universal.
## - Accepts a dict-of-dicts object as param, writes resulting markdown, returns nothing (besides maybe debug status)
##
## Fun pseudocode (i.e. you don't have to map dict[index] to var explicitly, you can just use them inline in the markdownification steps directly):
##
## ## Iterate by types, like 'component':
## for type in passed_methods.keys():
##     ## Iterate by resource, like 'arm':
##     for resource in type.keys():
##         ## Iterate by method, like 'doCommand'
##         for method in resource.keys()
##             method_link = method[1]
##             ## Iterate by parameter, like 'command':
##             for parameter in method[parameters].keys()
##                 parameter_name = parameter
##                 parameter_link = parameter[param_link]
##                 parameter_type_link = parameter[param_type_link]
##                 ## Determine if this param type has subtypes, like map(string):
##                 if param-has-subtypes:
##                     param_subtype = parameter[param_subtype]
##                     param_subtype_link = parameter[param_subtype_link]
##             if method-has-returns:
##                 for return in method[returns].keys()
##                     return_name = return
##                     return_link = return[return_link]
##                     return_type = return[return_type]
##                     return_type_link = return[return_type_link]
##                     if param-has-subtypes:
##                         return_subtype = return[return_subtype]
##                         return_subtype_link = return[return_subtype_link]



## TODO:
## Consider restructuring existing `docs` repo to support easier inline-replace of content.
## ANDF investigating
## Requirements:
## - Must support arbitrary manual copy in addition to automated content, example:
##   https://docs.viam.com/components/camera/#getimages



## Temporary holding main function to:
## - Fetch canonical proto methods from upstream, used for mapping in `parse()`
## - Get methods for each defined type & resource
## - Simple print for each dict during script development
def run():

    proto_map = get_proto_apis()

    component_methods = parse("component", components)
    ## Here's where we would markdownify(component_methods)
    print(component_methods)

    service_methods = parse("service", services)
    ## Here's where we would markdownify(service_methods)
    print(service_methods)

    app_methods = parse("app", app_apis)
    ## Here's where we would markdownify(app_methods)
    print(app_methods)

    robot_methods = parse("robot", robot_apis)
    ## Here's where we would markdownify(robot_methods)
    print(robot_methods)

run()

sys.exit(1)
