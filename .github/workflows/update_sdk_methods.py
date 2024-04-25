from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
import sys
import os
import markdownify
import subprocess
import urllib.parse
import urllib.error
import re as regex
import argparse


## Set the full list of SDK languages we scrape here:
sdks_supported = ["go", "python", "flutter"]

## Parse arguments passed to update_sdk_methods.py.
## You can either provide the specific sdk languages to run against
## as a comma-separated list, or omit entirely to run against all sdks_supported.
## You can also use 'map' to generate a proto map template file:
parser = argparse.ArgumentParser()

parser.add_argument('sdk_language', type=str, nargs='?', help="A comma-separated list of the sdks to run against. \
                     Can be one of: go, python, flutter. Omit to run against all sdks.")
parser.add_argument('-m', '--map', action='store_true', help="Generate initial mapping CSV file from upstream protos. \
                     In this mode, only the initial mapping file is output, no markdown.")

## Quick sanity check of provided sdk languages. If all is well,
## assemble sdks array to iterate through:
args = parser.parse_args()
if args.map:
    ## We check for args.map again in both proto_map() and run().
    sdks = sdks_supported
elif args.sdk_language is not None:
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

## This script must be run within the 'docs' git repo. Here we check
## to make sure this is the case, and get the root of our git-managed
## repo to use later in parse() and write_markdown():
process = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], \
                     stdout=subprocess.PIPE, \
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

if process.returncode == 0:
    gitroot = stdout.decode().rstrip()
else:
    print("ERROR: You must run this script within a cloned copy of the 'docs' git repo!")
    print("Exiting ...")
    exit(1)

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
    "dataset": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/dataset/v1/dataset_grpc.pb.go",
        "name": "DatasetServiceClient",
        "methods": []
    },
    "datasync": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/datasync/v1/data_sync_grpc.pb.go",
        "name": "DataSyncServiceClient",
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
## {resource}.{methodname} to exclude a specific method, or
## interface.{interfacename} to exclude an entire Go interface:
go_ignore_apis = [
    'interface.NavStore', # motion service interface
    'interface.LocalRobot', # robot interface
    'interface.RemoteRobot', # robot interface
    'robot.RemoteByName', # robot method
    'robot.ResourceByName', # robot method
    'robot.RemoteNames', # robot method
    'robot.ResourceNames', # robot method
    'robot.ResourceRPCAPIs', # robot method
    'robot.ProcessManager', # robot method
    'robot.OperationManager', # robot method
    'robot.SessionManager', # robot method
    'robot.PackageManager', # robot method
    'robot.Logger' # robot method
]

## Use these URLs for data types (for params, returns, and errors raised) that are
## built-in to the language or provided by a non-Viam third-party package:
## TODO: Not currently using these in parse(), but could do a simple replace()
##       or could handle in markdownification instead. TBD. Same with other SDK lang link arrays:
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
    'viam.app.app_client.AppClient.create_organization', # unimplemented
    'viam.app.app_client.AppClient.delete_organization', # unimplemented
    'viam.app.app_client.AppClient.list_organizations_by_user', # unimplemented
    'viam.app.app_client.AppClient.get_rover_rental_robots', # internal use
    'viam.app.app_client.AppClient.get_rover_rental_parts', # internal use
    'viam.app.app_client.AppClient.share_location', # unimplemented
    'viam.app.app_client.AppClient.unshare_location', # unimplemented
    'viam.app.data_client.DataClient.configure_database_user', # unimplemented
    'viam.app.data_client.DataClient.create_filter', # deprecated
    'viam.app.data_client.DataClient.delete_tabular_data_by_filter', # deprecated
    'viam.app.ml_training_client.MLTrainingClient.submit_training_job', # unimplemented
    'viam.components.input.client.ControllerClient.reset_channel', # GUESS ?
    'viam.robot.client.RobotClient.transform_point_cloud', # unimplemented
    'viam.robot.client.RobotClient.get_component', # GUESS ?
    'viam.robot.client.RobotClient.get_service', # GUESS ?
    'viam.app.app_client.AppClient.create_organization_invite' # Currently borked: https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_organization_invite
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

## Inject these URLs, relative to 'docs', into param/return/raises descriptions that contain exact matching key text.
## write_markdown() uses override_description_links via link_description() when it goes to write out descriptions.
## Currently only used for method descriptions, but see commented-out code for usage as optional consideration.
## NOTE: I am assuming we want to link matching text across all SDKs and methods. If not, this array
## will need additional field(s): ( method | sdk ) to narrow match.
## NOTE 2: I omitted links to the SDKs (like for 'datetime', and 'dataclass' since these can be
## separately handled uniformly (perhaps with the {sdk}_datatype_links array for example).
## EXAMPLES: The first two items in this dict correspond to these docs examples:
## EXAMPLE 1: https://docs.viam.com/mobility/frame-system/#transformpose
## EXAMPLE 2: https://docs.viam.com/mobility/motion/#moveonmap
override_description_links = {
    "additional transforms": "/mobility/frame-system/#additional-transforms",
    "SLAM service": "/mobility/slam/",
    "frame": "/mobility/frame-system/",
    "Viam app": "https://app.viam.com/",
    "organization settings page": "/fleet/organizations/",
    "image tags": "/data/dataset/#image-tags",
    "API key": "/fleet/cli/#authenticate",
    "in configuration": "/components/board/#digital_interrupts",
    "board model": "/components/board/#supported-models",
    "AnalogReaders": "/components/board/#analogs",
    "DigitalInterrupts": "/components/board/#digital_interrupts"
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
flutter_ignore_apis = [
    'getRoverRentalRobots' # internal use
]

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

    ## Only generate proto mapping template file if 'map' was passed as argument:
    if args.map:

        ## Writing template file with extra '.template' at the end to avoid accidentally clobbering
        ## the prod file if we've already populated it. When ready, change the filename to exactly
        ## sdk_protos_map.csv for this script to use it for proto mapping:
        proto_map_file_template = os.path.join(gitroot, '.github/workflows/sdk_protos_map.csv.template')
        output_file = open('%s' % proto_map_file_template, "w")

        output_file.write('## RESOURCE, PROTO, PYTHON METHOD, GO METHOD, FLUTTER METHOD\n')

        for api in proto_map.keys():
            output_file.write('\n## ' + api.title() + '\n')
            for proto in proto_map[api]['methods']:

                output_file.write(api + ',' + proto + ',\n')

    return proto_map

## Fetch URL content via BS4, used in parse():
def make_soup(url):
   try:
       page = urlopen(url)
       html = page.read().decode("utf-8")
       return BeautifulSoup(html, "html.parser")
   except urllib.error.HTTPError as err:
       print(f'An HTTPError was thrown: {err.code} {err.reason} for URL: {url}')

## Link matching text, used in write_markdown():
## NOTE: Currently does not support formatting for link titles
## (EXAMPLE: bolded DATA tab here: https://docs.viam.com/build/program/apis/data-client/#binarydatabyfilter)
def link_description(format_type, full_description, link_text, link_url):

    ## Supports 'md' link styling or 'html' link styling.
    ## The latter in case you want to link raw method usage:
    if format_type == 'md':
        new_linked_text = '[' + link_text + '](' + link_url + ')'
        linked_description = regex.sub(link_text, new_linked_text, full_description)
    elif format_type == 'html':
        new_linked_text = '<a href="' + link_url + '">' + link_text + '</a>'
        linked_description = regex.sub(link_text, new_linked_text, full_description)

    return linked_description

## Fetch sdk documentations for each language in sdks array, by language, by type, by resource, by method.
def parse(type, names):

## TODO:
## - Unify returned method object form. Currently returning raw method usage for Go, and by-param, by-return (and by-raise)
##   breakdown for each method for Python and Flutter. Let's chat about which is useful, and which I should throw away.
##   Raw usage is I think how check_python_methods.py currently does it. Happy to convert Flutter and Py to dump raw usage,
##   if you don't need the per-param,per-return,per-raise stuff.
## - Currently manually adding param details for 'extra' and 'timeout' params for Python. There might be more like this,
##   that need this same manual treatment, that I haven't found yet.

    ## This parent dictionary will contain all dictionaries:
    ## all_methods[sdk][type][resource]
    all_methods = {}

    ## Build path to sdk_protos_map.csv file that contains proto-to-methods mapping, needed during per-sdk looping:
    proto_map_file = os.path.join(gitroot, '.github/workflows/sdk_protos_map.csv')

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
                    ## TODO: Currently ignoring app client for go SDK, but GO does have app > data > Sync.
                    ##       Need to fix this code so that we permit app type, but only if not app resource.
                    pass
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
            ## If an invalid language was provided:
            else:
                pass
                #print("unsupported language!")

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

                    ## Exclude unwanted Go interfaces:
                    check_interface_name = 'interface.' + interface_name
                    if not check_interface_name in go_ignore_apis:

                        ## Loop through each method found for this interface:
                        for tag in resource_interface.find_all('span', attrs={"data-kind" : "method"}):

                            ## Create new empty dictionary for this specific method, to be appended to ongoing go_methods dictionary,
                            ## in form: go_methods[type][resource][method_name] = this_method_dict
                            this_method_dict = {}

                            tag_id = tag.get('id')
                            method_name = tag.get('id').split('.')[1]

                            ## Exclude unwanted Go methods:
                            check_method_name = resource + '.' + method_name
                            if not check_method_name in go_ignore_apis:

                                ## Look up method_name in proto_map file, and return matching proto:
                                with open(proto_map_file, 'r') as f:
                                    for row in f:
                                        if not row.startswith('#') \
                                        and row.startswith(resource) \
                                        and row.split(',')[3] == method_name:
                                            this_method_dict["proto"] = row.split(',')[1]

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
                                this_method_dict["method_link"] = url + '#' + interface_name

                                ## We have finished collecting all data for this method. Write the this_method_dict dictionary
                                ## in its entirety to the go_methods dictionary by type (like 'component'), by resource (like 'arm'),
                                ## using the method_name as key:
                                go_methods[type][resource][method_name] = this_method_dict
                
                ## We have finished looping through all scraped Go methods. Write the go_methods dictionary
                ## in its entirety to the all_methods dictionary using "go" as the key:
                all_methods["go"] = go_methods


            elif sdk == "go" and type == "app":
               ##Go SDK has no APP API!
               pass

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

                        ## Look up method_name in proto_map file, and return matching proto:
                        with open(proto_map_file, 'r') as f:
                            for row in f:
                                #print(row)
                                if not row.startswith('#') \
                                and row.startswith(resource) \
                                and row.split(',')[2] == method_name:
                                    this_method_dict["proto"] = row.split(',')[1]

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
                            type_name = parameter_tag.find('span', class_="pre").text

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
                            ## METHODOLOGY: Find parent <p> tag around matching <strong>type_name</strong> tag which contains this data.
                            ##   Determining by <strong> tags allows matching parameters regardless whether they are
                            ##   presented in <p> tags (single param) or <li> tags (multiple params):
                            for strong_tag in tag.find_all('strong'):
                                if strong_tag.text == type_name:
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

                            ## Add all values for this parameter to this_method_dict by type_name:
                            this_method_dict["parameters"][type_name] = this_method_parameters_dict

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
                                ## Determine if this <strong> tag is preceded by a <dt> tag containing the text "Raises". Otherwise omit.
                                ## METHODOLOGY: Find previous <dt> tag before matching <strong>type_name</strong> tag which contains this data.
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
                    #print('METHODNAME: ' + method_name)

                    if not method_name in flutter_ignore_apis:

                        ## Look up method_name in proto_map file, and return matching proto:
                        with open(proto_map_file, 'r') as f:
                            for row in f:
                                ## Because Flutter is the final entry in the mapping CSV, we must also rstrip() to
                                ## strip the trailing newline (\n) off the row itself:
                                row = row.rstrip()

                                if not row.startswith('#') \
                                and row.startswith(resource) \
                                and row.split(',')[4] == method_name:
                                    this_method_dict["proto"] = row.split(',')[1]                

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

                            type_name = parameter_tag.get('id')
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

                            this_method_dict["parameters"][type_name] = this_method_parameters_dict

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


# Parse usage string
def parse_method_usage(usage_string):

    # Splitting the usage string by comma to separate parameters and removing unwanted substrings
    parameters = list(filter(None, (param.strip() for param in usage_string.replace("\n\t\t", "").replace("\n\t,", "").replace("\n\t", "").split(','))))

    print("Parameters")
    print(parameters)

    parsed_usage_string = []

    for param in parameters:
        # Splitting each parameter by space to separate parameter name and type
        print("Param")
        print(param)
        parts = param.split()
        print(f"PARTS: {parts} for param {param}")
        
        type_name = parts[-1].strip('` ')  # Remove backticks and spaces
        print(f"type_name: {type_name}")

        param_type = ' '.join(parts[:-1]).strip('() ')  # Remove parentheses and spaces
        print(f"param_type: {param_type}")

        # Extracting the type link from the type string
        type_link = regex.search(r'<a href="([^"]+)">', param_type)
        print(f"type_link extracted: {type_link}")
        if type_link:
            param_type_link = type_link.group(1)
            print(f"param type link DEBUG DEBUG {param_type_link}")
        else:
            param_type_link = None

        # print("PARAM NAME")
        # print(type_name)
        # print("PARAM TYPE")
        # print(param_type)
        # print("PARAM TYPE LINK")
        # print(param_type_link)

        parsed_usage_string.append((type_name, param_type, param_type_link))

    # print("PARSED USAGE STRING:")
    # print(parsed_usage_string)
    return parsed_usage_string

# Format usage string
def format_method_usage(parsed_usage_string):
    formatted_output = []
    for type_name, param_type, param_type_link in parsed_usage_string:

        print(f"Param name: {type_name}")

        # Extracting param name from html
        matches = regex.findall(r'>(.*?)<', type_name)

        if matches:
            # Extracted content between ">" and "<"
            type_name = matches[0]
            print("Extracted param name:", type_name)
        else:
            # passing for now
            pass 

        # Extracting the parameter type from the param_type string
        # print(f"Type name pre extraction: {param_type}")
        param_name = regex.search(r'\w+(?=\s*<)', param_type)
        if param_name:
            param_name = param_name.group()
            # print(f"Type name detected: {param_name}")
        else:
            param_name = param_type.strip('<>')
            # print(f"Type name STRIPPED: {param_name}")
        
        # Creating the parameter type link based on the extracted type name
        print(f"CREATING PARAMETER TYPE LINK from param type link {param_type_link}")
        if param_type_link:
            # type_link = regex.search(r'<a href="([^"]+)">', param_type_link)
            # print(type_link)
            # if type_link:
                # param_type_link = type_link.group(1).replace('<a href="', "").replace('">', "").replace('>', "")
            print(f"type_link stripped: {param_type_link}")
            param_type_link = f"https://pkg.go.dev{param_type_link}#{param_name}"
        else:
            print("No param type link")

        if param_type_link:
            formatted_output.append(f"- `{param_name}` [({type_name})]({param_type_link}):")
        else:
            formatted_output.append(f"- `{param_name}` [({type_name})](<INSERT PARAM TYPE LINK>)")

    print("FORMATTED OUTPUT")
    print(formatted_output)
    return formatted_output

## write_markdown() takes the data object returned from parse(), and writes out the markdown
## for each method in that object. Here's an example of how I envision the data object being used.
## Of course, feel free to adapt and change as you like!
def write_markdown(type, methods):

    ## Temporary loop approach switcher:
    LOOP_BY = 'sdk'
    #LOOP_BY = 'proto'

    ## Generate special version of type var that matches how we refer to it in MD filepaths.
    ## This means pluralizing components and services, and taking no action for app and robot:
    if type in ['component', 'service']:
        type_filepath_name = type + 's'
    else:
        type_filepath_name = type

    ## Determine the necessary directory structure to support automated file writes:
    relative_generated_path = 'static/include/' + type_filepath_name + '/apis/generated/'
    full_generated_path = os.path.join(gitroot, relative_generated_path)
    overrides_path = os.path.join(full_generated_path, 'overrides')

    ## .../overrides/protos
    protos_override_path = os.path.join(overrides_path, 'protos')
    ## .../overrides/methods
    methods_override_path = os.path.join(overrides_path, 'methods')
    
    ## Create any of the above that don't presently exist
    ## (with parents=True, we only have to create final dirs in the
    ## path, and all earlier dirs will be created):
    ## CHOICE: Do we auto-create these dirs? Or require the user to do so as-needed?
    ## Up to us. I prefer to create everything for the user, much easier for all to use.
    ## - If auto: user doesn't need to know about folder structure at all, and can
    ##   just dump overrides in the dir already ready for them, easy to infer.
    ## - If not: no giant nested folder structure of empty dirs, to be committed to
    ##   our repo as empty. However, if not, we must instruct users of this script:
    ##   - To override a proto with custom leading MD content, place a file here:
    ##     docs/static/include/{type}/apis/generated/overrides/protos/{protoname}.md
    ##   - To override a method with custom leading MD content, place a file here:
    ##     docs/static/include/{type}/apis/generated/overrides/methods/{resource}/{sdk}/{methodname}.before.md
    ##     OR JUST:
    ##     docs/static/include/{type}/apis/generated/overrides/methods/{resource}/{sdk}/{methodname}.md
    ##   - To override a proto with custom trailing MD content, place a file here:
    ##     docs/static/include/{type}/apis/generated/overrides/methods/{resource}/{sdk}/{methodname}.after.md
    Path(protos_override_path).mkdir(parents=True, exist_ok=True)
    Path(methods_override_path).mkdir(parents=True, exist_ok=True)

    ## We can either loop by SDK, or by method proto name.
    ## Here is by SDK:
    if LOOP_BY == 'sdk':

        for sdk in methods.keys():
            #print(sdk)

            ## Determine where to write the file for this loop. Suggesting:
            ## docs/static/include/{type}/apis/generated/{sdk}.md
            #relative_path = 'static/include/' + type_filepath_name + '/apis/generated/'
            #print(relative_path)
            filename = sdk + '.md'

            full_path_to_file = os.path.join(full_generated_path, filename)
            output_file = open('%s' % full_path_to_file, "w") 

            ## Loop through each resource, such as 'arm'. run() already calls parse() in
            ## scope limited to 'type', so we don't have to loop by type:
            for resource in methods[sdk][type].keys():
                #print(resource)

                ## Create any missing method override subdirectories for this sdk/resource pass
                ## if not already present:
                resource_sdk_override_path = os.path.join(methods_override_path, resource, sdk)
                Path(resource_sdk_override_path).mkdir(parents=True, exist_ok=True)

                ## I've included some dumb plaintext output like this to help during scripting. Feel free to remove:
                # output_file.write('\n\n#!#!#!#!#!#!#!#!#!#!#!# RESOURCE: ' + resource + ' #!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#\n\n')

                ## Loop for each method in resource object:
                for method in methods[sdk][type][resource].keys():

                    # output_file.write('\n\n################# METHOD: ' + method + ' ##################################\n\n')

                    # output_file.write('METHOD NAME: ')
                    # output_file.write(method + '\n')

                    output_file.write('### ')
                    ## Get proto and save to variable; we also need it later:
                    ## HACK: Allowing for empty strings (for Go SDK docs that include methods that
                    ## TODO: Be better than this.
                    if 'proto' in methods[sdk][type][resource][method]:
                        proto = methods[sdk][type][resource][method]['proto']
                    else:
                        output_file.write('<NO PROTO FOUND, USING METHOD NAME> ')
                        proto = method

                    output_file.write(proto + '\n\n')

                    ## Here are some options for adding DOCS-side content on top of the scraped data.
                    ## It gets tricky, and we are greatly limited in our ability to edit _within_ scraped
                    ## content data, but some of the following options may solve some near-term problems
                    ## with upstream SDK quality until we have a chance to submit PRs to improve it.

                    ## Add additional MD content as an include, to be included directly under the proto header
                    ## This data is applicable to all language implementations of this proto (i.e. _not_ 
                    ## SDK-specific). Example: The `Usage` alert here: https://docs.viam.com/components/camera/#getimages
                   
                    ## Check for proto overrides.
                    ## Not sure how to handle this yet, but we currently check for this override
                    ## once per sdk per resource, but we only need to check once really.
     
                    # SG: turning off proto overrides bc method headers -- protos originally? I think?

                    # proto_override_filename = proto + '.md'

                    # ## .../overrides/protos/{proto}
                    # proto_override_filepath = os.path.join(protos_override_path, proto_override_filename)
                    # if os.path.isfile(proto_override_filepath):
                    #     output_file.write('PROTO OVERRIDE: ')
                    #     output_file.write(method + '\n')

                    #     for line in open(proto_override_filepath, 'r', encoding='utf-8'):
                    #        output_file.write(line)

                    ## Check for method overrides.
                    ## This check supports additional filename switches, to control whether this
                    ## override is to be placed either before the auto-gen stuff, or after.
                    ## Appending filename with .before (or omitting) places MD content before
                    ## the auto-gen content for this method (i.e. before params,returns, etc).
                    ## Appending filename with .after places MD content after the auto-gen content
                    ## for this method (i.e. after params and code samples).
                    ## EXAMPLE (before): https://docs.viam.com/components/camera/#getimage (Go tab)
                    ## EXAMPLE (after): https://docs.viam.com/mobility/motion/#getpose (Py tab)

                    has_after_override = 0

                    ## .../overrides/methods/{resource}/{sdk}/{method}.before|after.md
                    for method_override_filename in os.listdir(resource_sdk_override_path):
                        if method in method_override_filename:
                            method_override_file_path = os.path.join(resource_sdk_override_path, method_override_filename)
                            if method_override_filename.endswith('.after.md'):

                                ## Because we are writing out MD content in the same general loop as we are getting it
                                ## from the passed data object, we have to delay this 'after' write until later.
                                ## If you wanted to fetch all data first, and then afterwards loop through it all
                                ## separately, you could do this all together. For this implementation of this mock writer
                                ## function, I'm just noting in has_after_override that I need to come back
                                ## to this later in the writer loop:
                                has_after_override = 1
                            
                            ## Just being painfully explicit that we accept 'before' or nothing to control injecting
                            ## before the auto-gen content (such as params, returns, etc).
                            ## Also, we must use two discrete if statements (not if .. elif), so that we can
                            ## support both overrides if present (I didn't see any existing examples, but we might
                            ## want to!):
                            if not method_override_filename.endswith('.after.md') and \
                                (method_override_filename.endswith('.before.md') or \
                                method_override_filename.endswith('.md')):

                            #    output_file.write('METHOD OVERRIDE BEFORE: ')

                               for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                   output_file.write(line)

                    ## In the event we want to structure our method object such that omitted keys are permissable,
                    ## we can use if logic to take action only if present:
                    ## ALTERNATE: I dump empty strings to missing method object keys instead, and always write
                    ## the keys themselves. I will happily change the method object to whichever you prefer,
                    ## I think the object is currently a mix of both, which is the only non-acceptable option lol.
                    ## I will be correcting so the data object is identical between sdk langs. For now, you can
                    ## work on python only using 'update_sdk_methods.py python':
                    ## EXAMPLE: Go methods do not have descriptions, so I wrote an empty string "" to this key in
                    ## the passed data object. This means we can access this field outside of this if statement (i.e.
                    ## regardless of sdk), but also that if we blindly just output its contents to the markdown,
                    ## it will result in blank output for this field. Up to us to decide how to handle missing
                    ## data upstream:
                    if 'description' in methods[sdk][type][resource][method]:
                    
                        ## Check if method description contains any matching string in override_description_links.
                        ## If match, add link to text in description:

                        method_description = methods[sdk][type][resource][method]['description']

                        for override_text in override_description_links.keys():

                            if override_text in methods[sdk][type][resource][method]['description']:
                                # output_file.write('METHOD DESCRIPTION WITH LINK OVERRIDE: ')
                                method_description = link_description('md', methods[sdk][type][resource][method]['description'], override_text, override_description_links[override_text])

                        # output_file.write('METHOD DESCRIPTION: ')
                        output_file.write(method_description + '\n\n')

                    ## CHOICE: Do we want to fetch the raw usage or do we want to iterate through each param, return, error?
                    ##         Here is an example of raw usage, which I am fetching for the GO SDK:
                    if 'usage' in methods[sdk][type][resource][method]:

                        method_usage = methods[sdk][type][resource][method]['usage']

                        print("USAGE STRING:")
                        print(method_usage)

                        usage_string = method_usage.split('(')
                        print("SPLIT USAGE STRING")
                        print(usage_string)

                        if len(usage_string) == 3:
                            parameters = usage_string[1]
                            returns = usage_string[2]

                        else:
                            usage_string = usage_string[1].split(') ')
                            print("SPLIT USAGE STRING WITH ONE RETURN")
                            print(usage_string)

                            if usage_string[0] != '':
                                parameters = usage_string[0]
                                if len(usage_string) == 2:
                                    returns = usage_string[1]
                            else:
                                returns = usage_string[1]

                        if parameters:

                            # Parse and format parameters
                            output_file.write('**Parameters:**\n\n')

                            parsed_parameters = parse_method_usage(parameters)
                            formatted_parameters = format_method_usage(parsed_parameters)

                            for line in formatted_parameters:
                                output_file.write(line + '\n')

                        if returns:

                            # Parse and format returns
                            output_file.write('\n**Returns:**\n\n')

                            parsed_returns = parse_method_usage(returns)
                            formatted_returns = format_method_usage(parsed_returns)

                            for line in formatted_returns:
                                output_file.write(line + '\n')

                        ## OPTION: If we need to link within usage, which includes HTML tags, we can also use link_description(),
                        ## passing the 'html' argument. However, it will happily link matching text within existing HTML
                        ## tags, like a tag link targets, so I am commenting out for current usage, which is Go-only, and
                        ## doesn't really need it. An option if we standardize on usage, in which case I will augment
                        ## link_description() to ignore a tag links and similar:
                        #for override_text in override_description_links.keys():

                        #    if override_text in methods[sdk][type][resource][method]['usage']:
                        #        output_file.write('METHOD USAGE WITH LINK OVERRIDE: ')
                        #        method_usage = link_description('html', methods[sdk][type][resource][method]['usage'], override_text, override_description_links[override_text])

                        # output_file.write('METHOD USAGE: ')
                        # output_file.write(method_usage + '\n')

                    ## CHOICE: Do we want to fetch the raw usage or do we want to iterate through each param, return, error?
                    ##         Here is an example of a dict of parameters, which I am fetching for the Python and Flutter SDKs:
                    if 'parameters' in methods[sdk][type][resource][method]:

                        output_file.write('\n**Parameters:**\n\n')

                        # sg: Is parameter type being overriden? Doesn't always look accurate (ex. extra for python SDK is marked float-- looks like it's all picking up as float)
                        for parameter in methods[sdk][type][resource][method]['parameters'].keys():
                            output_file.write(f'- `{parameter}` [({methods[sdk][type][resource][method]["parameters"][parameter]["param_type"]})]')
                            
                            # Ideally we could update at least Python SDK with type links?
                            if 'param_type_link' in methods[sdk][type][resource][method]['parameters'][parameter]:
                                # Check for subtype
                                if 'param_subtype' in methods[sdk][type][resource][method]['parameters'][parameter]:
                                    output_file.write(f"({methods[sdk][type][resource][method]['parameters'][parameter]['param_type_link']})")
                                    if 'param_subtype_link' in methods[sdk][type][resource][method]['parameters'][parameter]:
                                        output_file.write(f"<[{methods[sdk][type][resource][method]['parameters'][parameter]['param_subtype']}]")
                                        output_file.write(f"({methods[sdk][type][resource][method]['parameters'][parameter]['param_subtype_link']})>")
                                    else:
                                        output_file.write(f"<{methods[sdk][type][resource][method]['parameters'][parameter]['param_subtype']}>")
                                else:
                                    output_file.write(f"({methods[sdk][type][resource][method]['parameters'][parameter]['param_type_link']})")
                            # SG: Haven't found any sub-types without param type links-- they are all in flutter SDK-- could expand this logic if popped up or grabbing more subtypes?
                            else:
                                output_file.write('(<INSERT PARAM TYPE LINK>)')

                            output_file.write(':')

                            if 'optional' in methods[sdk][type][resource][method]['parameters'][parameter]:
                                if str(methods[sdk][type][resource][method]['parameters'][parameter]['optional']) == "True":
                                    output_file.write(' Optional.')
                                                      
                            # line break for parameters list
                            output_file.write('\n')

                    ## Not fetching returns for Go (only 'usage'), only fetching one return for Python, and fetching all returns for Flutter.
                    ## I must standardize this approach first to be able to reliably output return data per method, but here's what should work
                    ## for the Python data object, I think.
                    ## As you explore options between the three approaches, I will standardize all languages to use the one you decide on.
                    ## EXAMPLE: if we go with raw usage, as presently returned for Go, I will do away with return looping for Python and
                    ## Flutter, and convert those to return raw usage as well.
                    if 'return' in methods[sdk][type][resource][method]:
                    
                        output_file.write('\n**Returns:**\n\n')
                       
                        print(methods[sdk][type][resource][method]["return"].keys())
                        # output_file.write(f'- `{methods[sdk][type][resource][method]["return"]}` [({methods[sdk][type][resource][method]["return"]["return_type"]})]')

                        ## TODO: Check for 'return' as name like in flutter SDK

                        if "return_type" in methods[sdk][type][resource][method]["return"]:
                            
                            # Check for subtype
                            if 'return_subtype' in methods[sdk][type][resource][method]["return"]:

                                if 'return_subtype_link'in methods[sdk][type][resource][method]["return"]:
                                    output_file.write(f"([{methods[sdk][type][resource][method]['return']['return_type']}]")

                                    if 'return_type_link' in methods[sdk][type][resource][method]["return"]:
                                        output_file.write(f"({methods[sdk][type][resource][method]['return']['return_type_link']}))")
                                        output_file.write(f"<[{methods[sdk][type][resource][method]['return']['return_subtype']}]")
                                        output_file.write(f"({methods[sdk][type][resource][method]['return']['return_subtype_link']})>")
                                    else:
                                        output_file.write(f"(<INSERT RETURN TYPE LINK>)))")
                                        output_file.write(f"<[{methods[sdk][type][resource][method]['return']['return_subtype']}]")
                                        output_file.write(f"({methods[sdk][type][resource][method]['return']['return_subtype_link']})>")
                                else:
                                    output_file.write(f"([{methods[sdk][type][resource][method]['return']['return_type']}]")

                                    if 'return_type_link' in methods[sdk][type][resource][method]['return']:
                                        output_file.write(f"({methods[sdk][type][resource][method]['return']['return_type_link']}))")
                                        output_file.write(f"<[{methods[sdk][type][resource][method]['return']['return_subtype']}]")
                                    else:
                                        output_file.write(f"(<INSERT RETURN TYPE LINK>)))")
                            
                            else:
                                output_file.write(f"([{methods[sdk][type][resource][method]['return']['return_type']}]")
                                if 'return_type_link' in methods[sdk][type][resource][method]['return']:
                                    output_file.write(f"({methods[sdk][type][resource][method]['return']['return_type_link']}))")
                                else:
                                    output_file.write(f"(<INSERT RETURN TYPE LINK>)))")
                            
                    #     # Check for subtype
                    #     if 'return_subtype' in methods[sdk][type][resource][method]['parameters'][parameter]:
                    #             output_file.write(f"({methods[sdk][type][resource][method]['parameters'][parameter]['param_type_link']})")
                    #             if 'param_subtype_link' in methods[sdk][type][resource][method]['parameters'][parameter]:
                    #                 output_file.write(f"<[{methods[sdk][type][resource][method]['parameters'][parameter]['param_subtype']}]")
                    #                 output_file.write(f"({methods[sdk][type][resource][method]['parameters'][parameter]['param_subtype_link']})>")
                    #             else:
                    #                 output_file.write(f"<{methods[sdk][type][resource][method]['parameters'][parameter]['param_subtype']}>")
                    #         else:
                    #             output_file.write(f"({methods[sdk][type][resource][method]['parameters'][parameter]['param_type_link']})")
                    #     # SG: Haven't found any sub-types without param type links-- they are all in flutter SDK-- could expand this logic if popped up or grabbing more subtypes?
                    #     else:
                    #         output_file.write('(<INSERT PARAM TYPE LINK>)')

                    #     output_file.write(':')
    
                    #    if 'return_description' in methods[sdk][type][resource][method]['return']:
                    #        output_file.write('    RETURN DESCRIPTION: ')
                    #        output_file.write(methods[sdk][type][resource][method]['return']['return_description'] + '\n')
                    #    if 'return_link' in methods[sdk][type][resource][method]['return']:
                    #        output_file.write('    RETURN LINK: ')
                    #        output_file.write(methods[sdk][type][resource][method]['return']['return_link'] + '\n')
                    #    if 'return_type_link' in methods[sdk][type][resource][method]['return']:
                    #        output_file.write('    RETURN TYPE LINK: ')
                    #        output_file.write(methods[sdk][type][resource][method]['return']['return_type_link'] + '\n')
                    #    if 'param_subtype' in methods[sdk][type][resource][method]['return']:
                    #        output_file.write('    RETURN SUBTYPE: ')
                    #        output_file.write(methods[sdk][type][resource][method]['return']['return_subtype'] + '\n')
                    #    if 'param_subtype_link' in methods[sdk][type][resource][method]['return']:
                    #        output_file.write('    RETURN SUBTYPE LINK: ')
                    #        output_file.write(methods[sdk][type][resource][method]['return']['return_subtype_link'] + '\n')


                    # Output the method link
                    output_file.write(f'\nFor more information, see the [{sdk.capitalize()} SDK Docs]({methods[sdk][type][resource][method]["method_link"]}).\n\n')

                    ## Same thing with errors raised ('raises') here.

                    ## If the method has a code sample, print it here:
                    if 'code_sample' in methods[sdk][type][resource][method]:

                        # output_file.write('CODE SAMPLE: \n')
                        # output_file.write(methods[sdk][type][resource][method]['code_sample'] + '\n')
                        output_file.write(f'```{sdk}\n' + methods[sdk][type][resource][method]['code_sample'] + '```\n\n')

                    ## If we detected an 'after' method override file earlier, write it out here:
                    if has_after_override:
                        output_file.write('METHOD OVERRIDE AFTER: ')

                        for line in open(method_override_file_path, 'r', encoding='utf-8'):
                            output_file.write(line)


    elif LOOP_BY == 'proto':
        ## TODO: finish impl
        pass

    ## - For looping by proto method: I don't have automated mapping working yet (and it might not be possible for all languages).
    ##   Barring automated determination, we can always manually map all ~250 methods per language, joy.
    ##   This approach would use a different loop structure, I can help create!

## Main run function:
## - proto_map()        Fetch canonical proto methods from upstream, used for mapping in `parse()`
## - parse()            Get methods for each defined type & resource, return data object for each
## - write_markdown()   Write out salient fields from passed data object to specific MD files
def run():

    proto_map = get_proto_apis()

    # If generating the mapping template file, skip all other functionality:
    if not args.map:

        component_methods = parse("component", components)
        write_markdown("component", component_methods)
        #print(component_methods)

        service_methods = parse("service", services)
        write_markdown("service", service_methods)
        #print(service_methods)

        app_methods = parse("app", app_apis)
        write_markdown("app", app_methods)
        #print(app_methods)

        robot_methods = parse("robot", robot_apis)
        write_markdown("robot", robot_methods)
        #print(robot_methods)

run()

sys.exit(1)
