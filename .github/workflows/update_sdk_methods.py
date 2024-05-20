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
## NOTE: The team has decided to always write all sdk languages each run, to support
##       writing per-proto include files. For current recommended usage, always omit
##       any sdk langs to run against all.
## Use 'verbose' to enable DEBUG output.
## Use 'map' to generate a proto map template file:
parser = argparse.ArgumentParser()

parser.add_argument('sdk_language', type=str, nargs='?', help="A comma-separated list of the sdks to run against. \
                     Can be one of: go, python, flutter. Omit to run against all sdks.")
parser.add_argument('-m', '--map', action='store_true', help="Generate initial mapping CSV file from upstream protos. \
                     In this mode, only the initial mapping file is output, no markdown.")
parser.add_argument('-v', '--verbose', action='store_true', help="Run in verbose mode. Writes a debug file containing \
                     the complete data object from parse() to /tmp/update_sdk_methods_debug.txt. \
                     Also prints high-level status updates to STDOUT. \
                     Deletes previous debug file when run again.")

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

if args.verbose:
    print('\nVERBOSE MODE: See /tmp/update_sdk_methods_debug.txt for debug output.')
    print('              Note: This file is deleted at the start of each new verbose run.')
    print('              Try, in a separate terminal window:\n')
    print('              DURING RUN: tail -f /tmp/update_sdk_methods_debug.txt')
    print('              AFTER RUN: less /tmp/update_sdk_methods_debug.txt\n')

## This script must be run within the 'docs' git repo. Here we check
## to make sure this is the case, and get the root of our git-managed
## repo to use later in parse() and write_markdown():
process_result = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], \
                     stdout=subprocess.PIPE, \
                     stderr=subprocess.PIPE)
stdout, stderr = process_result.communicate()

if process_result.returncode == 0:
    gitroot = stdout.decode().rstrip()
else:
    print("ERROR: You must run this script within a cloned copy of the 'docs' git repo!")
    print("Exiting ...")
    exit(1)

## Build path to sdk_protos_map.csv file that contains proto-to-methods mapping, used in write_markdown():
proto_map_file = os.path.join(gitroot, '.github/workflows/sdk_protos_map.csv')

## Check to see if we have a locally-staged version of the Go SDK Docs (RDK repo). If so,
## scrape our code samples (and only code samples!) from that URL instead. This check just
## establishes whether the URL is up or not; if detected as up here, it is scraped in parse().
## TODO: Consider if we need to consider other ports besides '8080', i.e. if multiple stage attempts,
##   or if port was already in use by another service when pkgsite command was issues
##   (8080 a very common web services default port)
## NOTE: To stage the Go SDK docs (RDK repo):
##   - Clone https://github.com/viamrobotics/rdk
##   - Make your changes (add code samples as needed)
##   - Run, from within the repo: go install golang.org/x/pkgsite/cmd/pkgsite@latest; pkgsite -open

is_go_sdk_staging_available = False

## Check to see if pkgsite (Go SDK docs local builder process) is running, and get its PID if so:
process_result = subprocess.run(["ps -ef | grep pkgsite | grep -v grep | awk {'print $2'}"], shell=True, text = True, capture_output=True)
pkgsite_pid = process_result.stdout.rstrip()

if pkgsite_pid != '':
    process_result = subprocess.run(["lsof -Pp " + pkgsite_pid + " | grep LISTEN | awk {'print $9'} | sed 's%.*:%%g'"], shell=True, text = True, capture_output=True)
    pkgsite_port = process_result.stdout
    is_go_sdk_staging_available = True
    if args.verbose:
        print('DEBUG: Detected local staged Go SDK docs URL, using that for Go code samples.')

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
              "input_controller", "motor", "movement_sensor", "power_sensor", "sensor", "servo"]
services = ["base_remote_control", "data_manager", "generic_service", "mlmodel", "motion", "navigation", "slam", "vision"]
app_apis = ["app", "billing", "data", "dataset", "data_sync", "mltraining"]
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
    "servo": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/servo/v1/servo_grpc.pb.go",
        "name": "ServoServiceClient",
        "methods": []
    },
    "data_manager": {
        "url": "https://github.com/viamrobotics/api/blob/main/service/datamanager/v1/data_manager_grpc.pb.go",
        "name": "DataManagerServiceClient",
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
    "billing": {
        "url": "https://github.com/viamrobotics/api/blob/main/app/v1/billing_grpc.pb.go",
        "name": "BillingServiceClient",
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
    "data_sync": {
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
    "generic_service": "generic",
    "base_remote_control": "baseremotecontrol",
    "data_manager": "datamanager"
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
    #'robot.ResourceNames', # robot method
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
    'viam.app.app_client.AppClient.create_organization_invite', # Currently borked: https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.create_organization_invite
    'viam.components.board.client.BoardClient.write_analog' # Currently borked: https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.write_analog
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
    ## Viam-specific data types:
    "viam.proto.app.OrganizationMember": "https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationMember",
    "viam.proto.app.OrganizationInvite": "https://python.viam.dev/autoapi/viam/proto/app/index.html#viam.proto.app.OrganizationInvite",
    "viam.components.arm.KinematicsFileFormat.ValueType": "https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.KinematicsFileFormat",
    "viam.media.video.NamedImage": "https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.NamedImage",
    "viam.proto.common.ResponseMetadata": "https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResponseMetadata",
    "viam.proto.component.encoder.PositionType.ValueType": "https://python.viam.dev/autoapi/viam/gen/component/encoder/v1/encoder_pb2/index.html#viam.gen.component.encoder.v1.encoder_pb2.PositionType"
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

## Map sdk language to specific code fence formatting syntax for that language:
code_fence_fmt = {
    'python': 'python',
    'go': 'go',
    'flutter': 'dart'
}

## Fetch canonical Proto method names.
## Required by Flutter parsing, and for generating the initial mapping file if -m was passed:
def get_proto_apis():
    for api in proto_map.keys():
        api_url = proto_map[api]["url"]
        api_name = proto_map[api]["name"]

        api_page = urlopen(api_url)
        api_html = api_page.read().decode("utf-8")

        ## Protos are presented in plaintext, so we must match by expected raw text:
        proto_regex = 'type ' + regex.escape(api_name) + r'[^{]*\{([^}]+)\}'
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

## Link any matching data types to their reference links, based on {sdk}_datatype_links[] array,
## used in parse() for both param and return data types. Handles data types syntax that includes
## multiple data types (and therefore requires multiple data type links), such as
## ListOrganizationMembers: Tuple[List[viam.proto.app.OrganizationMember], List[viam.proto.app.OrganizationInvite]
## DESIGN DECISION: Ignore well-known, usually leading (containing) data types like List, Tuple, Dict.
## NOTE: Only used in PySDK parsing, for now (but should work for all with minor tweak to support per-language links array):
def link_data_types(sdk, data_type_string):

    linked_data_type_string = ""

    ## If the passed data_type_string matches exactly to a data type defined in python_datatype_links, use that:
    if data_type_string in python_datatype_links.keys():
       linked_data_type_string = '[' + data_type_string + '](' + python_datatype_links[data_type_string] + ')'
    else:

        ## Assemble all encountered data types that match to python_datatype_links keys into array.
        ## This match is a little too greedy, and will match, say, 'int' to 'JointPositions'. To counter
        ## this, we additionally check for leading and trailing alphanumeric characters further in:
        matching_data_types = list(key for key in python_datatype_links if key in data_type_string)

        if len(matching_data_types) > 0:

            ## Ugly hack to allow us to append within the for loop below, sorry:
            linked_data_type_string = data_type_string

            for data_type_found in matching_data_types:

                ## Discard string matches that are substrings of other data type strings:
                if not regex.search(r'[A-Za-z0-9]' + data_type_found, data_type_string) and not regex.search(data_type_found + r'[A-Za-z0-9]', data_type_string):

                    data_type_linked = '[' + data_type_found + '](' + python_datatype_links[data_type_found] + ')'
                    linked_data_type_string = regex.sub(data_type_found, data_type_linked, linked_data_type_string)
                else:
                    ## If we get here, this data_type is actually a substring of another data type. Take no action:
                    pass

    ## If we didn't find any matching links, return an empty string so we can know to look elsewhere,
    ## otherwise return linked data type string:
    if linked_data_type_string == data_type_string:
        return ""
    else:
        return linked_data_type_string


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

## Fetch SDK documentation for each language in sdks array, by language, by type, by resource, by method.
def parse(type, names):

## TODO:
## - Unify returned method object form. Currently returning raw method usage for Go, and by-param, by-return (and by-raise)
##   breakdown for each method for Python and Flutter. Let's chat about which is useful, and which I should throw away.
##   Raw usage is I think how check_python_methods.py currently does it. Happy to convert Flutter and Py to dump raw usage,
##   if you don't need the per-param,per-return,per-raise stuff.

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

            ## Determine URL form for Flutter depending on type (like 'component').
            ## TEMP: Manually exclude Base Remote Control Service (Go only):
            ## TODO: Handle resources with 0 implemented methods for this SDK better.
            elif sdk == "flutter" and resource != 'base_remote_control':
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
                                        and row.startswith(resource + ',') \
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
                                this_method_dict["usage"] = regex.sub(r'</span>', '', method_usage_raw).replace("\t", "  ").lstrip().rstrip()

                                ## Not possible to link to the specific functions, so we link to the parent resource instead:
                                this_method_dict["method_link"] = url + '#' + interface_name

                                ## Check for code sample for this method.
                                ## If we detected that a local instance of the Go SDK docs is available, use that.
                                ## Otherwise, use the existing scraped 'soup' object from the live Go SDK docs instead.
                                if is_go_sdk_staging_available:

                                    staging_url = regex.sub('https://pkg.go.dev', 'http://localhost:8080', url)
                                    staging_soup = make_soup(staging_url)

                                    ## Get a raw dump of all go methods by interface for each resource:
                                    go_code_samples_raw = staging_soup.find_all(
                                        lambda code_sample_tag: code_sample_tag.name == 'p'
                                        and method_name + " example:" in code_sample_tag.text)
                                else:

                                    ## Get a raw dump of all go methods by interface for each resource:
                                    go_code_samples_raw = soup.find_all(
                                        lambda code_sample_tag: code_sample_tag.name == 'p'
                                        and method_name + " example:" in code_sample_tag.text)

                                ## Determine if a code sample is provided for this method:
                                if len(go_code_samples_raw) == 1:

                                    ## Fetch code sample raw text, preserving newlines but stripping all formatting.
                                    ## This string should be suitable for feeding into any python formatter to get proper form:
                                    this_method_dict["code_sample"] = go_code_samples_raw[0].find_next('pre').text.replace("\t", "  ")

                                elif len(go_code_samples_raw) > 1:
                                
                                    ## In case we want to support multiple code samples per method down the line,
                                    ## this is where to process (and: update write_markdown() accordingly to enable looping
                                    ## through possible code sample data objects). For now we just continue to fetch just the
                                    ## first-discovered (i.e., at index [0]):
                                    this_method_dict["code_sample"] = go_code_samples_raw[0].find_next('pre').text.replace("\t", "  ")

                                ## We have finished collecting all data for this method. Write the this_method_dict dictionary
                                ## in its entirety to the go_methods dictionary by type (like 'component'), by resource (like 'arm'),
                                ## using the method_name as key:
                                go_methods[type][resource][method_name] = this_method_dict

                        ## Go SDK docs for each interface omit inherited functions. If the resource being considered inherits from
                        ## resource.Resource (currently all components and services do, and no app or robot interfaces do), then add
                        ## the three inherited methods manually: Reconfigure(), DoCommand(), Close()
                        ## (Match only to instances that are preceded by a tab char, or we'll catch ResourceByName erroneously):
                        if '\tresource.Resource' in resource_interface.text:
                            go_methods[type][resource]['Reconfigure'] = {'proto': 'Reconfigure', \
                                'description': 'Reconfigure must reconfigure the resource atomically and in place. If this cannot be guaranteed, then usage of AlwaysRebuild or TriviallyReconfigurable is permissible.', \
                                'usage': 'Reconfigure(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, deps <a href="#Dependencies">Dependencies</a>, conf <a href="#Config">Config</a>) <a href="/builtin#error">error</a>', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                            go_methods[type][resource]['DoCommand'] = {'proto': 'DoCommand', \
                                'description': 'DoCommand sends/receives arbitrary data.', \
                                'usage': 'DoCommand(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, cmd map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                            go_methods[type][resource]['Close'] = {'proto': 'Close', \
                                'description': 'Close must safely shut down the resource and prevent further use. Close must be idempotent. Later reconfiguration may allow a resource to be "open" again.', \
                                'usage': 'Close(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>) <a href="/builtin#error">error</a>', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}

                        ## Similarly, if the resource being considered inherits from resource.Actuator (Servo, for example),
                        ## then add the two inherited methods manually: IsMoving() and Stop():
                        if '\tresource.Actuator' in resource_interface.text:
                            go_methods[type][resource]['IsMoving'] = {'proto': 'IsMoving', \
                                'description': 'IsMoving returns whether the resource is moving or not', \
                                'usage': 'IsMoving(<a href="/context">context</a>.<a href="/context#Context">Context</a>) (<a href="/builtin#bool">bool</a>, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Actuator'}
                            go_methods[type][resource]['Stop'] = {'proto': 'Stop', \
                                'description': 'Stop stops all movement for the resource', \
                                'usage': 'Stop(<a href="/context">context</a>.<a href="/context#Context">Context</a>, map[<a href="/builtin#string">string</a>]interface{}) <a href="/builtin#error">error</a>', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Actuator'}

                        ## Similarly, if the resource being considered inherits from resource.Shaped (Base, for example),
                        ## then add the one inherited method manually: Geometries():
                        if '\tresource.Shaped' in resource_interface.text:
                            go_methods[type][resource]['Geometries'] = {'proto': 'GetGeometries', \
                                'description': 'Geometries returns the list of geometries associated with the resource, in any order. The poses of the geometries reflect their current location relative to the frame of the resource.', \
                                'usage': 'Geometries(<a href="/context">context</a>.<a href="/context#Context">Context</a>, map[<a href="/builtin#string">string</a>]interface{}) ([]<a href="/go.viam.com/rdk/spatialmath">spatialmath</a>.<a href="/go.viam.com/rdk/spatialmath#Geometry">Geometry</a>, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Shaped'}

                        ## Similarly, if the resource being considered inherits from resource.Sensor (Movement Sensor, for example),
                        ## then add the one inherited method manually: Readings():
                        if '\tresource.Sensor' in resource_interface.text:
                            go_methods[type][resource]['Readings'] = {'proto': 'GetReadings', \
                                'description': 'Readings return data specific to the type of sensor and can be of any type.', \
                                'usage': 'Readings(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, extra map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Sensor'}

                ## We have finished looping through all scraped Go methods. Write the go_methods dictionary
                ## in its entirety to the all_methods dictionary using "go" as the key:
                all_methods["go"] = go_methods

            elif sdk == "go" and type == "app":
               ##Go SDK has no APP API!
               pass

            ## Scrape each parent method tag and all contained child tags for Python by resource.
            ## TEMP: Manually exclude Base Remote Control Service (Go only) and Data Manager Service (Go + Flutter only).
            ## TODO: Handle resources with 0 implemented methods for this SDK better.
            elif sdk == "python" and resource != 'base_remote_control' and resource != 'data_manager':
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
                                and row.startswith(resource + ',') \
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

                                ## Determine if this parameter is optional, and strip off ' | None' syntax if so:
                                if param_type.endswith(' | None'):
                                    this_method_parameters_dict["optional"] = True
                                    param_type = param_type.replace(' | None', "")
                                    #this_method_parameters_dict["param_type"] = param_type
                                else:
                                    this_method_parameters_dict["optional"] = False

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
                                    this_method_parameters_dict["param_type"] = "Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]"

                                else:

                                    ## First, check python_datatype_links array for manually-mapped data type links.
                                    ## These will override all other ways of determining data type links:
                                    linked_param_type = ""
                                    linked_param_type = link_data_types('python', param_type)

                                    ## If link_data_types() returns a linked data type string, use that.
                                    ## Otherwise, check the scraped parameter_tag for the link:
                                    if linked_param_type != "":
                                        this_method_parameters_dict["param_type"] = linked_param_type
                                    elif parameter_tag.find('a', class_="reference internal"):
                                        param_type_link_raw = parameter_tag.find('a', class_="reference internal").get("href")

                                        ## Parameter type link is an anchor link:
                                        if param_type_link_raw.startswith('#'):
                                            this_method_parameters_dict["param_type"] = '[' + param_type + '](' + url + param_type_link_raw + ')'
                                        ## Parameter type link is a relative link, in one of three forms:
                                        elif param_type_link_raw.startswith('../../../'):
                                            this_method_parameters_dict["param_type"] = '[' + param_type + '](' + sdk_url + "/autoapi/viam/" + param_type_link_raw.replace('../../../', '')+ ')'
                                        elif param_type_link_raw.startswith('../../'):
                                            this_method_parameters_dict["param_type"] = '[' + param_type + '](' + sdk_url + "/autoapi/viam/" + param_type_link_raw.replace('../../', '')+ ')'
                                        elif param_type_link_raw.startswith('../'):
                                            this_method_parameters_dict["param_type"] = '[' + param_type + '](' + sdk_url + "/autoapi/viam/" + param_type_link_raw.replace('../', '')+ ')'

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

                                            ## Some params provide data type links in Parameters section only, not initial usage.
                                            ## Get that here if soL
                                            if strong_tag.parent.find('a', class_="reference internal"):
                                                param_type_link_raw = strong_tag.parent.find('a', class_="reference internal").get("href")
                                                ## Parameter type link is an anchor link:
                                                if param_type_link_raw.startswith('#'):
                                                    this_method_parameters_dict["param_type"] = '[' + param_type + '](' + url + param_type_link_raw + ')'
                                                ## Parameter type link is a relative link, beginning with 1 - 3 instances of '../'
                                                ## Convert to an absolute link:
                                                elif param_type_link_raw.startswith('../'):
                                                    this_method_parameters_dict["param_type"] = '[' + param_type + '](' + sdk_url + "/autoapi/viam/" + param_type_link_raw.replace('../', '')+ ')'

                                            ## Unable to determine parameter description, neither timeout or extra, nor matching to any
                                            ## param in initial method usage string. Usually this means a non-param (like error raised),
                                            ## but if we are missing expected param descriptions, expand this section to catch them.
                                            else:
                                                ## No-op:
                                                pass

                                this_method_dict["parameters"][param_name] = this_method_parameters_dict

                        ## Get single tag containing the return for this method:
                        return_tag = tag.find('span', class_='sig-return')

                        ## Parse return for this method:
                        ## METHODOLOGY: Some methods explicitly state that they return "None", others just omit the field.
                        ##   Either way, ensure we only write a return to this_method_dict if an actual return is present:
                        if return_tag and return_tag.find('span', class_='pre').text != "None":

                            ## Create new empty dictionary for this_method_dict named "return":
                            this_method_dict["return"] = {}

                            ## OPTION: Get return_type by explicit key name:
                            return_type = return_tag.find('span', class_="sig-return-typehint").text
                            this_method_dict["return"]["return_type"] = return_type

                            linked_return_type = ""
                            linked_return_type = link_data_types('python', return_type)

                            if linked_return_type != "":
                                this_method_dict["return"]["return_type"] = linked_return_type
                            elif return_tag.find('a', class_="reference internal"):

                                ## TODO: Only grabbing the first link encountered, but a few methods return a tuple of two linked data types.
                                ## Handling those via link_data_types() with manual entries in python_datatype_links for now,
                                ## But there's room for a more elegant solution:
                                return_type_link_raw = return_tag.find('a', class_="reference internal").get("href")

                                ## Return type link is an anchor link:
                                if return_type_link_raw.startswith('#'):
                                    this_method_dict["return"]["return_type"] = '[' + return_type + '](' + url + return_type_link_raw + ')'
                                ## Return type link is a relative link, beginning with 1 - 3 instances of '../'
                                ## Convert to an absolute link:
                                elif return_type_link_raw.startswith('../'):
                                    this_method_dict["return"]["return_type"] = '[' + return_type + '](' + sdk_url + "/autoapi/viam/" + return_type_link_raw.replace('../', '')+ ')'

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

                                ## Append to ongoing this_method_dict, stripping newlines:
                                this_method_dict["return"]["return_description"] = return_description_raw[0].p.text.replace("\n", " ")

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
                                ## METHODOLOGY: Find previous <dt> tag before matching <strong>param_name</strong> tag which contains this data.
                                ##   Determining by <strong> tags allows matching parameters regardless whether they are
                                ##   presented in <p> tags (single error raised) or <li> tags (multiple errors raised):
                                if strong_tag.find_previous('dt').text == "Raises:":

                                    ## Split contained text at " - " to get first half, which is just the error name:
                                    raises_name = regex.split(r" – ", strong_tag.parent.text)[0]

                                    ## OPTION: Get full error raised usage, including type info and html links if present.
                                    ## NOTE: Errors raised (py) don't seem to have any links, just some monospace formatting:
                                    ## NOTE: Currently unused.
                                    this_method_raises_dict["raises_usage"] = str(strong_tag.parent).replace("\n", " ")

                                    ## OPTION: Determine error raised description, stripping any newlines:
                                    this_method_raises_dict["raises_description"] = regex.split(r" – ", strong_tag.parent.text)[1].replace("\n", " ")

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

            ## Scrape each parent method tag and all contained child tags for Flutter by resource.
            ## TEMP: Manually exclude Base Remote Control Service (Go only).
            ## TODO: Handle resources with 0 implemented methods for this SDK better.
            elif sdk == "flutter" and resource != 'base_remote_control':
                soup = make_soup(url)
                ## Limit matched class to exactly 'callable', i.e. not 'callable inherited', remove the constructor (proto id) itself, and remove '*_Pre' methods from Robot API:
                flutter_methods_raw = soup.find_all(
                    lambda tag: tag.name == 'dt'
                    and tag.get('class') == ['callable']
                    and not regex.search(proto_map[resource]['name'], tag.text)
                    and not regex.search('_Pre', tag.text))

                ## Loop through scraped tags and select salient data:
                for tag in flutter_methods_raw:

                    ## Create new empty dictionary for this specific method, to be appended to ongoing flutter_methods dictionary,
                    ## in form: flutter_methods[type][resource][method_name] = this_method_dict
                    this_method_dict = {}

                    method_name = tag.get('id')

                    if not method_name in flutter_ignore_apis:

                        ## Look up method_name in proto_map file, and return matching proto:
                        with open(proto_map_file, 'r') as f:
                            for row in f:
                                ## Because Flutter is the final entry in the mapping CSV, we must also rstrip() to
                                ## strip the trailing newline (\n) off the row itself:
                                row = row.rstrip()

                                if not row.startswith('#') \
                                and row.startswith(resource + ',') \
                                and row.split(',')[4] == method_name:
                                    this_method_dict["proto"] = row.split(',')[1]

                        ## Determine method link:
                        this_method_dict["method_link"] = tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                        ## Flutter SDK puts all parameter detail on a separate params page that we must additionally make_soup on:
                        parameters_link = tag.find("span", class_="type-annotation").a['href'].replace("..", sdk_url)
                        parameters_soup_raw = make_soup(parameters_link)
                        parameters_soup = parameters_soup_raw.find_all(
                            lambda tag: tag.name == 'dt'
                            and tag.get('class') == ['property']
                            and not regex.search('info_', tag.text))

                        this_method_dict["parameters"] = {}
                        this_method_dict["returns"] = {}

                        # Parse parameters:
                        for parameter_tag in parameters_soup:

                            ## Create new empty dictionary this_method_parameters_dict to house all parameter
                            ## keys for this method, to allow for multiple parameters. Also resets the
                            ## previous parameter's data when looping through multiple parameters:
                            this_method_parameters_dict = {}

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

                                ## Create new empty dictionary this_method_returns_dict to house all return
                                ## keys for this method, to allow for multiple returns. Also resets the
                                ## previous return's data when looping through multiple returns:
                                this_method_returns_dict = {}

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

                ## We have finished looping through all scraped Flutter methods. Write the flutter_methods dictionary
                ## in its entirety to the all_methods dictionary using "flutter" as the key:
                all_methods["flutter"] = flutter_methods

            else:
                ## Good code would never get here.
                ## This code gets here when facing a resource with 0 implemented methods for
                ## the SDK we're looping for.
                ## TODO: Fix so resources with 0 implemented methods for an SDK are silently
                ## skipped without requiring manual exclusion in parse().
                pass

    return all_methods


# Parse usage string, used in write_markdown():
def parse_method_usage(usage_string):

    # Splitting the usage string by comma to separate parameters and removing unwanted substrings
    parameters = list(filter(None, (param.strip() for param in usage_string.replace("\n\t\t", "").replace("\n\t,", "").replace("\n\t", "").split(','))))

    parsed_usage_string = []

    for param in parameters:
        # HACKY: Hardcoding ctx, extra, and error bc they are all the same and parsing from usage string
        # has proven difficult

        # Splitting each parameter by space to separate parameter name and type
        parts = param.split()

        if 'ctx' in param:
            type_name = "ctx"
            param_type = "Context"
            param_type_link = "https://pkg.go.dev/context#Context"
        elif 'extra' in param:
            type_name = "extra"
            param_type = "map[string]interface\{\}"
            param_type_link = "https://go.dev/blog/maps"
        elif param == '<a href="/builtin#error">error</a>':
            type_name = ""
            param_type = "error"
            param_type_link = "https://pkg.go.dev/builtin#error"
        else:
            type_name = parts[-1].strip('` ')  # Remove backticks and spaces
            param_type = ' '.join(parts[:-1]).strip('() ')  # Remove parentheses and spaces

            # Extracting the type link from the type string
            type_link = regex.search(r'href="([^"]+)">', type_name)
            if type_link:
                param_type_link = type_link.group(1)
            else:
                param_type_link = None

        parsed_usage_string.append((type_name, param_type, param_type_link))

    return parsed_usage_string

# Format usage string, used in write_markdown():
def format_method_usage(parsed_usage_string):
    formatted_output = []
    for type_name, param_type, param_type_link in parsed_usage_string:

        return_string = ""

        if type_name == "ctx":
            return_string += f"- `{type_name}` [({param_type})]({param_type_link}): A Context carries a deadline, a cancellation signal, and other values across API boundaries."
            formatted_output.append(return_string)
        elif type_name == "extra":
            return_string += f"- `{type_name}` [({param_type})]({param_type_link}): Extra options to pass to the underlying RPC call."
            formatted_output.append(return_string)
        elif param_type == "error":
            return_string += f"- [({param_type})]({param_type_link}): An error, if one occurred."
            formatted_output.append(return_string)
        else:
            # Extracting param name from html
            matches = regex.findall(r'>(.*?)<', type_name)

            if matches:
                # Extracted content between ">" and "<"
                type_name = matches[0]

            return_string += f"- "

            # Extracting the parameter type from the param_type string
            # print(f"Type name pre extraction: {param_type}")
            param_name = regex.search(r'\w+(?=\s*<)', param_type)
            if param_name:
                param_name = param_name.group()
                return_string += f"`{param_name}` "

            # Creating the parameter type link based on the extracted type name
            # print(f"CREATING PARAMETER TYPE LINK from param type link {param_type_link}")
            if param_type_link:
                # print(f"type_link stripped: {param_type_link}")
                param_type_link = f"https://pkg.go.dev{param_type_link}"
                return_string += f"[({type_name})]({param_type_link}):"
            else:
                return_string += f"[({type_name})](<INSERT PARAM TYPE LINK>):"

            formatted_output.append(return_string)

    return formatted_output

## write_markdown() takes the data object returned from parse(), and writes out the markdown
## for each method in that object:
def write_markdown(type, names, methods):

    ## Generate special version of type var that matches how we refer to it in MD filepaths.
    ## This means pluralizing components and services, and taking no action for app and robot:
    if type in ['component', 'service']:
        type_filepath_name = type + 's'
    else:
        type_filepath_name = type

    ## Set 'generated' folder structure and 'override' directories:
    relative_generated_path = 'static/include/' + type_filepath_name + '/apis/generated/'
    path_to_generated = os.path.join(gitroot, relative_generated_path)
    relative_override_path = 'static/include/' + type_filepath_name + '/apis/overrides/'
    path_to_overrides = os.path.join(gitroot, relative_override_path)
    path_to_protos_override = os.path.join(path_to_overrides, 'protos')
    path_to_methods_override = os.path.join(path_to_overrides, 'methods')

    ## Create any missing directories, or take no action if already present:
    Path(path_to_generated).mkdir(parents=True, exist_ok=True)
    Path(path_to_protos_override).mkdir(parents=True, exist_ok=True)
    Path(path_to_methods_override).mkdir(parents=True, exist_ok=True)

    ## NOTE: To use the above override directories:
    ## To override a proto with custom leading MD content, place a file here:
    ##    docs/static/include/{type}/apis/overrides/protos/{resource}.{protoname}.md
    ## To override a method with custom leading MD content, place a file here:
    ##    docs/static/include/{type}/apis/overrides/methods/{sdk}.{resource}.{methodname}.before.md
    ##      OR JUST:
    ##    docs/static/include/{type}/apis/overrides/methods/{sdk}.{resource}.{methodname}.md
    ## To override a method with custom trailing MD content, place a file here:
    ##    docs/static/include/{type}/apis/overrides/methods/{sdk}.{resource}.{methodname}.after.md

    ## Loop through each resource, such as 'arm'. run() already calls parse() in
    ## scope limited to 'type', so we don't have to loop by type:
    for resource in names:

        ## Switch to identify the first method encountered for each resource, to help with
        ## knowing when we are at the top of the include file, or whether to to double newline
        ## between protos:
        is_first_method_in_this_resource = True

        ## Determine where to write output for this resource:
        resource_filename = resource + '.md'
        full_path_to_file = os.path.join(path_to_generated, resource_filename)
        output_file = open('%s' % full_path_to_file, "w")

        ## Determine where to write API protos list table for this resource:
        resource_protos_table_filename = resource + '-table.md'
        full_path_to_table_file = os.path.join(path_to_generated, resource_protos_table_filename)
        table_file = open('%s' % full_path_to_table_file, "w")

        ## Loop through mapping file, and determine which sdk methods to document for each proto:
        with open(proto_map_file, 'r') as f:
            for row in f:
                if not row.startswith('#') \
                and row.startswith(resource + ','):
                    proto = row.split(',')[1]
                    py_method_name = row.split(',')[2]
                    go_method_name = row.split(',')[3]
                    flutter_method_name = row.split(',')[4].rstrip()

                    ## Allow setting protos with 0 sdk method maps, to allow us to disable writing MD
                    ## for specific protos as needed, if needed:
                    if py_method_name or go_method_name or flutter_method_name:

                        ## We have at least one implemented method for this proto, so begin writing output markdown for this resource.
                        ## Write proto as H3, with leading newlines if appending to ongoing {resource}.md file:
                        if is_first_method_in_this_resource:
                            output_file.write('### ' + proto + '\n\n')
                        else:
                            output_file.write('\n### ' + proto + '\n\n')

                        ## NOTE: This is where proto descriptions could go if we scraped them. However:
                        ## - Some protos do not have descriptions.
                        ## - DOCS provides vastly better descriptions in some cases.
                        ## - DOCS descriptions are often deeply linked to DOCS content.
                        ## We use the proto override system instead to provide these proto descriptions.
                        ## TODO: Consider adding/enhancing proto descriptions to viamrobotics/api,
                        ## and adding descriptions scraping to get_proto_apis().

                        proto_override_filename = resource + '.' + proto + '.md'

                        ## .../overrides/protos/{resource}.{proto}
                        proto_override_file = os.path.join(path_to_protos_override, proto_override_filename)
                        if os.path.isfile(proto_override_file):

                            for line in open(proto_override_file, 'r', encoding='utf-8'):
                               output_file.write(line)

                            output_file.write('\n')

                        ## We have at least one implemented method for this proto, so begin writing table list markdown for this resource.
                        ## Add proto name to table_file listing, with standard first three lines.
                        ## We write this here, depending on is_first_method_in_this_resource, in case we have a resource with 0 implemented protos
                        ## down the line, to avoid blank table_files:
                        if is_first_method_in_this_resource:
                            table_file.write('<!-- prettier-ignore -->\n')
                            table_file.write('Method Name | Description\n')
                            table_file.write('----------- | -----------\n')

                        ## Determine what the anchor link structure should be for this resource. Each type has its own standard:
                        if type == 'component':
                            this_proto_anchor_link = '/' + type_filepath_name + '/' + resource + '/#' + proto.lower()
                        elif type == 'service' and resource in ['base_remote_control', 'motion', 'navigation', 'slam']:
                            this_proto_anchor_link = '/mobility/' + resource.replace('base_remote_control', 'base_rc') + '/#' + proto.lower()
                        elif type == 'service' and resource == 'data_manager':
                            this_proto_anchor_link = '/data/#' + proto.lower()
                        elif type == 'service' and resource == 'generic_service':
                            this_proto_anchor_link = '/registry/advanced/generic/#' + proto.lower()
                        elif type == 'service' and resource in ['mlmodel', 'vision']:
                            this_proto_anchor_link = '/ml/' + resource.replace('mlmodel', 'deploy') + '/#' + proto.lower()
                        elif type == 'app' and resource == 'app':
                            this_proto_anchor_link = '/build/program/apis/fleet/#' + proto.lower()
                        elif type == 'app' and resource in ["billing", "mltraining"]:
                            this_proto_anchor_link = '/build/program/apis/' + resource.replace('mltraining','ml-training') + '-client/#' + proto.lower()
                        elif type == 'app' and resource in ["data", "dataset", "data_sync"]:
                            this_proto_anchor_link = '/build/program/apis/data-client/#' + proto.lower()
                        elif type == 'robot':
                            this_proto_anchor_link = '/build/program/apis/' + resource + '/#' + proto.lower()

                        ## Fetch just the first sentence from the proto_override_file (first text string terminated by '.\n', ignoring hugo
                        ## shortcodes like alerts ('{{%.*%}}.*{{% \[a-b].* %}}'), which precede some override files' (proto descriptions'
                        ## first sentence:
                        with open(proto_override_file, 'r') as f:
                            file_contents = f.read().strip()
                            file_contents = regex.sub(r'\{\{\%.*\%\}\}.*\{\{\% \/[a-b].* \%\}\}', '', file_contents, flags=regex.DOTALL)
                            search_result = file_contents.split('.\n', 1)[0].strip().replace("\n", " ")

                        ## If the proto description is missing a trailing period, or we stripped it off during the above matching, append
                        ## (restore) the period character:
                        if not search_result.endswith('.'):
                            proto_description_first_sentence = search_result + '.'
                        else:
                            proto_description_first_sentence = search_result

                        ## Write out this proto's entry to this resource's table_file:
                        table_file.write('[`' + proto + '`](' + this_proto_anchor_link + ') | ' + proto_description_first_sentence + '\n')

                        ## Begin the per-language markdown writing to output_file with the opening tabset declaration:
                        output_file.write('{{< tabs >}}\n')

                        if py_method_name:
                            output_file.write('{{% tab name="Python" %}}\n\n')

                            ## Check for method overrides.
                            ## This check supports additional filename switches, to control whether this
                            ## override is to be placed either before the auto-gen stuff, or after.
                            ## Appending filename with .before (or omitting) places MD content before
                            ## the auto-gen content for this method (i.e. before params,returns, etc).
                            ## Appending filename with .after places MD content after the auto-gen content
                            ## for this method (i.e. after params and code samples).

                            has_after_override = 0

                            ## .../overrides/methods/{resource}.{sdk}.{method}.before|after.md
                            for method_override_filename in os.listdir(path_to_methods_override):
                                if method_override_filename.startswith('python.' + resource + '.' + py_method_name):
                                    method_override_file_path = os.path.join(path_to_methods_override, method_override_filename)
                                    if method_override_filename.endswith('.after.md'):

                                        ## Because we are writing out MD content in the same general loop as we are getting it
                                        ## from the passed data object, we have to delay this 'after' write until later.
                                        ## If you wanted to fetch all data first, and then afterwards loop through it all
                                        ## separately, you could do this all together. For this implementation of this mock writer
                                        ## function, I'm just noting in has_after_override that I need to come back
                                        ## to this later in the writer loop:
                                        has_after_override = 1

                                    ## Just being painfully explicit that we accept '.before' or nothing to control injecting
                                    ## before the auto-gen content (such as params, returns, etc), or exactly '.after' to control
                                    ## injecting after the auto-gen content:
                                    if not method_override_filename.endswith('.after.md') and \
                                        (method_override_filename.endswith('.before.md') or \
                                        method_override_filename.endswith('.md')):

                                        for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                            output_file.write(line)

                            output_file.write('**Parameters:**\n\n')

                            if 'parameters' in methods['python'][type][resource][py_method_name]:

                                for parameter in methods['python'][type][resource][py_method_name]['parameters'].keys():

                                    param_data = methods['python'][type][resource][py_method_name]['parameters'][parameter]

                                    param_type = param_data.get("param_type")
                                    param_description = param_data.get("param_description")
                                    optional = param_data.get("optional")

                                    output_file.write(f'- `{parameter}` ({param_type})')

                                    if optional:
                                        output_file.write(' (optional)')
                                    else:
                                        output_file.write(' (required)')

                                    output_file.write(':')

                                    if param_description:
                                        output_file.write(f" {param_description}")
                                    else:
                                        output_file.write(": <INSERT PARAM DESCRIPTION>\n")

                                    # line break for parameters list
                                    output_file.write('\n')

                            # Handle case where no parameters are found
                            else:
                                output_file.write("- None.\n")

                            output_file.write('\n**Returns:**\n\n')

                            if 'return' in methods['python'][type][resource][py_method_name]:

                                return_data = methods['python'][type][resource][py_method_name]["return"]
                                return_type = return_data.get("return_type")
                                return_description = return_data.get("return_description")

                                if return_type:
                                    output_file.write(f"- ({return_type})")

                                    if return_description:
                                        output_file.write(f": {return_description}\n")
                                    else:
                                        output_file.write(": <INSERT RETURN DESCRIPTION>\n")
                            # Handle case where no returns are found
                            else:
                                output_file.write("- None.\n")

                            # Output the method link
                            output_file.write(f'\nFor more information, see the [Python SDK Docs]({methods["python"][type][resource][py_method_name]["method_link"]}).\n\n')

                            ## If the method has a code sample, print it here:
                            if 'code_sample' in methods['python'][type][resource][py_method_name]:

                                output_file.write('```' + code_fence_fmt['python'] + ' {class="line-numbers linkable-line-numbers"}\n')
                                output_file.write(methods['python'][type][resource][py_method_name]['code_sample'])
                                output_file.write('```\n\n')

                            ## If we detected an 'after' method override file earlier, write it out here:
                            if has_after_override:

                                for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                    output_file.write(line)

                                output_file.write('\n')

                            # Close tabs
                            output_file.write("{{% /tab %}}\n")
                            if not go_method_name and not flutter_method_name:
                                output_file.write("{{< /tabs >}}\n")

                        if go_method_name:
                            output_file.write('{{% tab name="Go" %}}\n\n')

                            ## Check for method overrides.
                            ## This check supports additional filename switches, to control whether this
                            ## override is to be placed either before the auto-gen stuff, or after.
                            ## Appending filename with .before (or omitting) places MD content before
                            ## the auto-gen content for this method (i.e. before params,returns, etc).
                            ## Appending filename with .after places MD content after the auto-gen content
                            ## for this method (i.e. after params and code samples).

                            has_after_override = 0

                            ## .../overrides/methods/{resource}.{sdk}.{method}.before|after.md
                            for method_override_filename in os.listdir(path_to_methods_override):
                                if method_override_filename.startswith('go.' + resource + '.' + go_method_name):
                                    method_override_file_path = os.path.join(path_to_methods_override, method_override_filename)
                                    if method_override_filename.endswith('.after.md'):

                                        ## Because we are writing out MD content in the same general loop as we are getting it
                                        ## from the passed data object, we have to delay this 'after' write until later.
                                        ## If you wanted to fetch all data first, and then afterwards loop through it all
                                        ## separately, you could do this all together. For this implementation of this mock writer
                                        ## function, I'm just noting in has_after_override that I need to come back
                                        ## to this later in the writer loop:
                                        has_after_override = 1

                                    ## Just being painfully explicit that we accept '.before' or nothing to control injecting
                                    ## before the auto-gen content (such as params, returns, etc), or exactly '.after' to control
                                    ## injecting after the auto-gen content:
                                    if not method_override_filename.endswith('.after.md') and \
                                        (method_override_filename.endswith('.before.md') or \
                                        method_override_filename.endswith('.md')):

                                        for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                            output_file.write(line)

                                        output_file.write('\n')

                            if 'usage' in methods['go'][type][resource][go_method_name]:

                                method_usage = methods['go'][type][resource][go_method_name]['usage']

                                usage_string = method_usage.split('(')

                                parameters = ''

                                if len(usage_string) == 3:
                                    parameters = usage_string[1]
                                    returns = usage_string[2]

                                else:
                                    usage_string = usage_string[1].split(') ')

                                    if usage_string[0] != '':
                                        parameters = usage_string[0]
                                        if len(usage_string) == 2:
                                            returns = usage_string[1]
                                    else:
                                        returns = usage_string[1]

                                output_file.write('**Parameters:**\n\n')

                                if len(parameters) > 0:
                                    # Parse and format parameters
                                    parsed_parameters = parse_method_usage(parameters)
                                    formatted_parameters = format_method_usage(parsed_parameters)

                                    for line in formatted_parameters:
                                        output_file.write(line + '\n')
                                # Handle case where no parameters are found
                                else:
                                    output_file.write("- None.\n")

                                output_file.write('\n**Returns:**\n\n')
                                if returns:
                                    # Parse and format returns

                                    parsed_returns = parse_method_usage(returns)
                                    formatted_returns = format_method_usage(parsed_returns)

                                    for line in formatted_returns:
                                        output_file.write(line + '\n')
                                # Handle case where no returns are found
                                else:
                                    output_file.write("- None.\n")

                            # Output the method link
                            output_file.write(f'\nFor more information, see the [Go SDK Docs]({methods["go"][type][resource][go_method_name]["method_link"]}).\n\n')

                            ## If the method has a code sample, print it here:
                            if 'code_sample' in methods['go'][type][resource][go_method_name]:

                                output_file.write('```' + code_fence_fmt['go'] + ' {class="line-numbers linkable-line-numbers"}\n')
                                output_file.write(methods['go'][type][resource][go_method_name]['code_sample'])
                                output_file.write('```\n\n')

                            ## If we detected an 'after' method override file earlier, write it out here:
                            if has_after_override:

                                for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                    output_file.write(line)

                                output_file.write('\n')

                            output_file.write("{{% /tab %}}\n")
                            if not flutter_method_name:
                                output_file.write("{{< /tabs >}}\n")

                        if flutter_method_name:
                            output_file.write('{{% tab name="Flutter" %}}\n\n')

                            ## Check for method overrides.
                            ## This check supports additional filename switches, to control whether this
                            ## override is to be placed either before the auto-gen stuff, or after.
                            ## Appending filename with .before (or omitting) places MD content before
                            ## the auto-gen content for this method (i.e. before params,returns, etc).
                            ## Appending filename with .after places MD content after the auto-gen content
                            ## for this method (i.e. after params and code samples).

                            has_after_override = 0

                            ## .../overrides/methods/{resource}.{sdk}.{method}.before|after.md
                            for method_override_filename in os.listdir(path_to_methods_override):
                                if method_override_filename.startswith('flutter.' + resource + '.' + flutter_method_name):
                                    method_override_file_path = os.path.join(path_to_methods_override, method_override_filename)
                                    if method_override_filename.endswith('.after.md'):

                                        ## Because we are writing out MD content in the same general loop as we are getting it
                                        ## from the passed data object, we have to delay this 'after' write until later.
                                        ## If you wanted to fetch all data first, and then afterwards loop through it all
                                        ## separately, you could do this all together. For this implementation of this mock writer
                                        ## function, I'm just noting in has_after_override that I need to come back
                                        ## to this later in the writer loop:
                                        has_after_override = 1

                                    ## Just being painfully explicit that we accept '.before' or nothing to control injecting
                                    ## before the auto-gen content (such as params, returns, etc), or exactly '.after' to control
                                    ## injecting after the auto-gen content:
                                    if not method_override_filename.endswith('.after.md') and \
                                        (method_override_filename.endswith('.before.md') or \
                                        method_override_filename.endswith('.md')):

                                        for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                            output_file.write(line)

                            output_file.write('**Parameters:**\n\n')
                            if 'parameters' in methods['flutter'][type][resource][flutter_method_name]:

                                for parameter in methods['flutter'][type][resource][flutter_method_name]['parameters'].keys():

                                    param_data = methods['flutter'][type][resource][flutter_method_name]['parameters'][parameter]

                                    param_type = param_data.get("param_type")
                                    param_subtype = param_data.get("param_subtype")
                                    param_type_link = param_data.get("param_type_link")
                                    param_subtype_link = param_data.get("param_subtype_link")
                                    param_description = param_data.get("param_description")
                                    optional = param_data.get("optional")

                                    output_file.write(f'- `{parameter}` [({param_type})]')

                                    # Ideally we could update at least Python SDK with type links?
                                    if param_type_link:
                                        # Check for subtype
                                        if param_subtype:
                                            output_file.write(f"({param_type_link})")
                                            if param_subtype_link:
                                                output_file.write(f"<[{param_subtype}]")
                                                output_file.write(f"({param_subtype_link})>")
                                            else:
                                                output_file.write(f"<{param_subtype}>")
                                        else:
                                            output_file.write(f"({param_type_link})")
                                    # SG: Haven't found any sub-types without param type links-- they are all in flutter SDK--
                                    # could expand this logic if popped up or grabbing more subtypes?
                                    else:
                                        output_file.write('(<INSERT PARAM TYPE LINK>)')

                                    if optional:
                                        output_file.write(' (optional)')
                                    else:
                                        output_file.write(' (required)')

                                    output_file.write(':')

                                    if param_description:
                                        output_file.write(f" {param_description}")

                                    # line break for parameters list
                                    output_file.write('\n')

                            # Handle case where no parameters are found
                            else:
                                output_file.write("- None.\n")

                            output_file.write('\n**Returns:**\n\n')
                            if 'return' in methods['flutter'][type][resource][flutter_method_name]:

                                return_data = methods['flutter'][type][resource][flutter_method_name]["return"]
                                return_type = return_data.get("return_type")
                                return_subtype = return_data.get("return_subtype")
                                return_type_link = return_data.get("return_type_link")
                                return_link = return_data.get("return_type_link") # TODO: handle this
                                return_subtype_link = return_data.get("return_subtype_link")
                                return_description = return_data.get("return_description")

                                if return_type:
                                    output_file.write(f"- [({return_type})]")

                                    if return_type_link:
                                        output_file.write(f"({return_type_link})")
                                    else:
                                        output_file.write("(INSERT RETURN TYPE LINK)")

                                    if return_subtype:
                                        output_file.write(f"<[{return_subtype}]")
                                        if return_subtype_link:
                                            output_file.write(f"({return_subtype_link})>")
                                        else:
                                            output_file.write("(<INSERT RETURN SUBTYPE LINK>)")
                                    else:
                                        pass

                                    if return_description:
                                        output_file.write(f": {return_description}")
                                    else:
                                        output_file.write(": <INSERT RETURN DESCRIPTION>")
                            else:
                                # Handle case where no parameters are found
                                output_file.write("- None.\n")

                            # Output the method link
                            output_file.write(f'\nFor more information, see the [Flutter SDK Docs]({methods["flutter"][type][resource][flutter_method_name]["method_link"]}).\n\n')

                            ## If the method has a code sample, print it here:
                            if 'code_sample' in methods['flutter'][type][resource][flutter_method_name]:

                                output_file.write('```' + code_fence_fmt['flutter'] + ' {class="line-numbers linkable-line-numbers"}\n')
                                output_file.write(methods['flutter'][type][resource][flutter_method_name]['code_sample'])
                                output_file.write('```\n\n')

                            ## If we detected an 'after' method override file earlier, write it out here:
                            if has_after_override:

                                for line in open(method_override_file_path, 'r', encoding='utf-8'):
                                    output_file.write(line)

                                output_file.write('\n')

                            output_file.write("{{% /tab %}}\n")
                            output_file.write("{{< /tabs >}}\n")

                    ## After this loop, we will be working with additional methods appended to the same {resource}.md include file.
                    ## This switch tells us at the start of the loop for this same resource that we should double-newline the next
                    ## proto encountered:
                    is_first_method_in_this_resource = False

## Main run function:
## - proto_map()        Fetch canonical proto methods from upstream, used for Flutter mapping in `parse()`
## - parse()            Get methods for each defined type & resource, return data object for each, by SDK
## - write_markdown()   Write out salient fields from passed data object to specific MD files
def run():

    if args.verbose:
        print('DEBUG: Now fetching upstream PROTOs')
    proto_map = get_proto_apis()
    if args.verbose:
        print('DEBUG: Completed fetching upstream PROTOs!')

    ## If generating the mapping template file, skip all other functionality.
    ## Otherwise, continue as normal:
    if not args.map:

        ## If running in verbose mode:
        if args.verbose:
            debug_filepath = os.path.join('/tmp/', 'update_sdk_methods_debug.txt')
            ## Delete debug file from last run:
            if os.path.isfile(debug_filepath):
                os.remove(debug_filepath)
            debug_file = open('%s' % debug_filepath, "w")

        ## Parse components:
        if args.verbose:
            print('DEBUG: Now parsing upstream COMPONENT methods for: ' + str(sdks))
        component_methods = parse("component", components)
        if args.verbose:
            print('DEBUG: Completed parsing upstream COMPONENT methods!')
            debug_file.write(str(component_methods))
            print('DEBUG: Now writing markdown for COMPONENT methods for: ' + str(sdks))
        write_markdown("component", components, component_methods)
        if args.verbose:
            print('DEBUG: Completed writing markdown for COMPONENT methods!')

        ## Parse services:
        if args.verbose:
            print('DEBUG: Now parsing upstream SERVICE methods for: ' + str(sdks))
        service_methods = parse("service", services)
        if args.verbose:
            print('DEBUG: Completed parsing upstream SERVICE methods!')
            debug_file.write(str(service_methods))
            print('DEBUG: Now writing markdown for SERVICE methods for: ' + str(sdks))
        write_markdown("service", services, service_methods)
        if args.verbose:
            print('DEBUG: Completed writing markdown for SERVICE methods!')

        ## Parse app client:
        if args.verbose:
            print('DEBUG: Now parsing upstream APP methods for: ' + str(sdks))
        app_methods = parse("app", app_apis)
        if args.verbose:
            print('DEBUG: Completed parsing upstream APP methods!')
            debug_file.write(str(app_methods))
            print('DEBUG: Now writing markdown for APP methods for: ' + str(sdks))
        write_markdown("app", app_apis, app_methods)
        if args.verbose:
            print('DEBUG: Completed writing markdown for APP methods!')

        ## Parse robot client:
        if args.verbose:
            print('DEBUG: Now parsing upstream ROBOT methods for: ' + str(sdks))
        robot_methods = parse("robot", robot_apis)
        if args.verbose:
            print('DEBUG: Completed parsing upstream ROBOT methods!')
            debug_file.write(str(robot_methods))
            print('DEBUG: Now writing markdown for ROBOT methods for: ' + str(sdks))
        write_markdown("robot", robot_apis, robot_methods)
        if args.verbose:
            print('DEBUG: Completed writing markdown for ROBOT methods!')

run()

sys.exit(1)
