from parser_utils import make_soup
from markdownify import markdownify as md


## Language-specific resource name overrides:
flutter_resource_overrides = {
    "generic_component": "Generic",
    "generic_service": "GenericServiceClient",
    "movement_sensor": "MovementSensor",
    "power_sensor": "PowerSensor",
    "vision": "VisionClient",
    "robot": "RobotClient",
    "data": "DataClient",
    "dataset": "DataClient",
    "data_sync": "DataClient",
    "discovery": "DiscoveryClient"
}

## Ignore these specific APIs if they error, are deprecated, etc:
flutter_ignore_apis = [
    'getRoverRentalRobots', # internal use
    'noSuchMethod', # generic method
    'toString', # generic method
    'operator ==', # generic method
    'fromRobot',
    'disableDebugLogging',
    'enableDebugLogging'
]

## Use these URLs for data types that are built-in to the language:
flutter_datatype_links = {}

class FlutterParser:
    def __init__(self, proto_map_file, flutter_staging_url = None):
        self.proto_map_file = proto_map_file
        self.sdk_url = "https://flutter.viam.dev"

        if flutter_staging_url:
            self.scrape_url = flutter_staging_url
            self.staging = True
        else:
            self.scrape_url = "https://flutter.viam.dev"
            self.staging = False
        self.flutter_methods = {}


    def parse(self, type, viam_resources, args):
        self.flutter_methods[type] = {}

        # Skip resources not supported in Flutter
        unsupported_resources = [
            "base_remote_control", "encoder", "input_controller",
            "data_manager", "mlmodel", "motion",
            "navigation", "slam", "switch", "app", "billing", "mltraining"
        ]

        for resource in viam_resources:

            ## Determine URL form for Flutter depending on type (like 'component').
            ## TODO: Handle resources with 0 implemented methods for this SDK better.

            # Initialize Flutter methods dictionary if it doesn't exist
            self.flutter_methods[type][resource] = {}

            if resource in unsupported_resources:
                if args.verbose:
                    print(f'DEBUG: Skipping unsupported Flutter resource: {resource}')
                continue
            elif resource in flutter_resource_overrides:
                url = f"{self.scrape_url}/viam_sdk/{flutter_resource_overrides[resource]}-class.html"
                # if args.verbose:
                #     print(f'DEBUG: Parsing Flutter URL: {url}')
            else:
                url = f"{self.scrape_url}/viam_sdk/{resource.capitalize()}-class.html"

            ## Scrape each parent method tag and all contained child tags for Flutter by resource.
            ## TEMP: Manually exclude Base Remote Control Service (Go only).
            ## TODO: Handle resources with 0 implemented methods for this SDK better.
            if resource not in unsupported_resources:

                soup = make_soup(url)
                if not soup:
                    print(f"DEBUG: No soup for {url}")
                    continue

                if resource in flutter_resource_overrides:
                    flutter_resource = flutter_resource_overrides[resource]
                else:
                    flutter_resource = resource.capitalize()
                ## Limit matched class to either 'callable' or 'callable inherited' and remove the constructor (proto id) itself:
                flutter_methods_raw = soup.find_all(
                    lambda tag: tag.name == 'dt'
                    and not tag.get('id') == flutter_resource
                    and tag.has_attr("class")
                    and "callable" in tag.get("class"))

                ## Loop through scraped tags and select salient data:
                for tag in flutter_methods_raw:

                    ## Create new empty dictionary for this specific method, to be appended to ongoing flutter_methods dictionary,
                    ## in form: flutter_methods[type][resource][method_name] = this_method_dict
                    this_method_dict = {}

                    method_name = tag.get('id')

                    if method_name.endswith(".new"):
                        continue

                    if not method_name in flutter_ignore_apis:

                        ## Look up method_name in proto_map file, and return matching proto:
                        with open(self.proto_map_file, 'r') as f:
                            for row in f:
                                ## Because Flutter is the final entry in the mapping CSV, we must also rstrip() to
                                ## strip the trailing newline (\n) off the row itself:
                                row = row.rstrip()

                                if not row.startswith('#') \
                                and row.startswith(resource + ',') \
                                and row.split(',')[5] == method_name:
                                    this_method_dict["proto"] = row.split(',')[1]

                        ## Determine method link:
                        method_link = tag.find("span", class_="name").a['href'].replace("..", self.sdk_url)
                        this_method_dict["method_link"] = method_link

                        ## While some method info is available to us on this current Flutter SDK page, the code sample is only found on the
                        ## method_link page. So we scrape that page for everything:
                        method_soup = make_soup(method_link)

                        ## Method description and code samples are both found within the same section tag:
                        desc_or_code_sample = method_soup.find('section', class_ = 'desc markdown')

                        if desc_or_code_sample:
                            if desc_or_code_sample.p:
                                this_method_dict["method_description"] = desc_or_code_sample.p.text
                            if desc_or_code_sample.pre:
                                this_method_dict["code_sample"] = desc_or_code_sample.pre.text

                        parameter_tags = method_soup.find_all(
                            lambda tag: tag.name == 'span'
                            and tag.get('class') == ['parameter'])

                        ## Parse parameters, if any are found:
                        if len(parameter_tags) != 0:

                            ## Create new empty dictionary for this_method_dict named "parameters":
                            this_method_dict["parameters"] = {}

                            optional = False

                            # If there is a curly brace before the parameter list all parameters are optional
                            prev = parameter_tags[0].find_previous('section')
                            if prev:
                                if "{<ol" in str(prev):
                                    optional = True

                            for parameter_tag in parameter_tags:

                                ## Create new empty dictionary this_method_parameters_dict to house all parameter
                                ## keys for this method, to allow for multiple parameters. Also resets the
                                ## previous parameter's data when looping through multiple parameters:
                                this_method_parameters_dict = {}

                                ## Parse for param name and usage string, convert to string (for markdownify):
                                param_name = parameter_tag.find('span', class_ = 'parameter-name').text
                                param_usage = str(parameter_tag.find('span', class_ = 'type-annotation')).replace('>>', '>\\>')

                                ## Markdownify parameter usage and replace relative links with absolute:
                                formatted_param_usage = md(param_usage, strip=['wbr']).replace("../../", "https://flutter.viam.dev/")
                                this_method_parameters_dict["param_usage"] = formatted_param_usage

                                # if a parameter is optional the previous parameter has a curly brace before it
                                this_method_parameters_dict["optional"] = optional

                                this_method_dict["parameters"][param_name] = this_method_parameters_dict

                                if parameter_tag.text.endswith("{"):
                                    optional = True

                        return_tags = method_soup.find_all(
                            lambda tag: tag.name == 'span'
                            and tag.get('class') == ['returntype'])

                        if len(return_tags) != 0:

                            ## Create new empty dictionary for this_method_dict named "return":
                            this_method_dict["return"] = {}

                            for return_tag in return_tags:

                                ## Create new empty dictionary this_method_returns_dict to house all return
                                ## keys for this method, to allow for multiple returns. Also resets the
                                ## previous return's data when looping through multiple returns:
                                this_method_return_dict = {}

                                # Parse return usage string, convert to string (for markdownify):
                                return_usage = str(return_tag)

                                ## Markdownify return usage and replace relative links with absolute:
                                formatted_return_usage = md(return_usage, strip=['wbr']).replace("../../", "https://flutter.viam.dev/")
                                this_method_return_dict["return_usage"] = formatted_return_usage.replace('>>', '>\\>').replace("dart-core/Future-class.html", "dart-async/Future-class.html").replace("dart-core/Stream-class.html","dart-async/Stream-class.html")

                                # Parse return type:
                                if return_tag.find('span', class_ = 'type-parameter'):
                                    return_type = return_tag.find('span', class_ = 'type-parameter').text
                                else:
                                    return_type = return_tag.text

                                this_method_dict["return"][return_type] = this_method_return_dict

                        self.flutter_methods[type][resource][method_name] = this_method_dict

            elif type == "app":
                ##Flutter SDK has no APP API!
                pass

        return self.flutter_methods

