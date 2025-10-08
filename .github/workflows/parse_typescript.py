from parser_utils import make_soup
from markdownify import markdownify as md
from urllib.parse import urljoin

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
    "world_state_store": "WorldStateStore"
}

## Ignore these specific APIs if they error, are deprecated, etc:
typescript_ignore_apis = [
    'getRoverRentalRobots' # internal use
]

## Use these URLs for data types that are built-in to the language:
typescript_datatype_links = {}

class TypeScriptParser:
    def __init__(self, proto_map_file, typescript_staging_url = None):
        self.proto_map_file = proto_map_file
        self.sdk_url = "https://ts.viam.dev"

        if typescript_staging_url:
            self.scrape_url = typescript_staging_url
            self.staging = True
        else:
            self.scrape_url = "https://ts.viam.dev"
            self.staging = False
        self.typescript_methods = {}


    def parse(self, type, viam_resources, args):
        self.typescript_methods[type] = {}

        # Skip resources not supported in TypeScript
        unsupported_resources = [
            "base_remote_control", "pose_tracker", "mlmodel"
        ]

        for resource in viam_resources:

            ## Determine URL form for TypeScript depending on type (like 'component').
            ## TODO: Handle resources with 0 implemented methods for this SDK better.

            # Initialize TypeScript methods dictionary if it doesn't exist
            self.typescript_methods[type][resource] = {}

            if resource in unsupported_resources:
                if args.verbose:
                    print(f'DEBUG: Skipping unsupported TypeScript resource: {resource}')
                continue

            url = f"{self.scrape_url}/classes/{resource.capitalize()}Client.html"
            if resource in typescript_resource_overrides:
                url = f"{self.scrape_url}/classes/{typescript_resource_overrides[resource]}Client.html"

            # if args.verbose:
            #     print(f'DEBUG: Parsing TypeScript URL: {url}')

            ## Scrape each parent method tag and all contained child tags for TypeScript by resource.
            ## TODO: Handle resources with 0 implemented methods for this SDK better.
            soup = make_soup(url)
            if not soup:
                print(f"DEBUG: No soup for {url}")
                continue

            for a in soup.find_all('a'):
                if a.get('href') and not a.get('href').startswith('http'):
                    a['href'] = urljoin(url, a.get('href'))

            top_level_sections = soup.find_all(class_='tsd-member-group')
            methods = []
            properties = []

            for section in top_level_sections:
                if 'Methods' in section.find('h2').text:
                    methods.extend(section.find_all('section', class_='tsd-panel tsd-member'))
                if 'Properties' in section.find('h2').text:
                    properties.extend(section.find_all('section', class_='tsd-panel tsd-member'))
                if resource == 'robot':
                    if section.find('h2').text.strip() in ['App/Cloud', 'ComponentConfig', 'Discovery', "Frame System", "Operations", "Resources", "Sessions", "Modules"]:
                        new_methods = section.find_all('section', class_='tsd-panel tsd-member')
                        methods.extend(new_methods)

            for property in properties:
                property_name = property.find('h3').span.text
                if property_name == 'callOptions':
                    continue
                code_sample = resource + "." + property_name + "\n"
                property_description = ""

                if property.find('div', class_="tsd-comment"):
                    property_description = md(str(property.find('div', class_="tsd-comment"))).strip()
                    if (len(property_description.split('\n')) > 1):
                        property_description = property_description.replace('\n', '\n  ').rstrip()

                return_type = property.find('span', class_="tsd-signature-type").text
                # Remove extra whitespace
                return_type = " ".join(return_type.split())
                return_object = {
                    'return_description': property_description,
                    'return_type': return_type,
                    'return_usage': property.find('span', class_="tsd-signature-type").text
                }

                self.typescript_methods[type][resource][property_name] = {
                    'method_description': "",
                    'method_link': property.find('a', class_='tsd-anchor-icon')["href"],
                    'parameters': {},
                    'proto': '',
                    'return': return_object
                }

                if code_sample:
                    self.typescript_methods[type][resource][property_name]["code_sample"] = code_sample

            for method in methods:
                method_name = method.find('h3').span.text

                param_object = {}
                if method.find('div', class_="tsd-parameters"):
                    parameters = method.find('div', class_="tsd-parameters")
                    parameter_list = parameters.find('ul', class_="tsd-parameter-list").children

                    for param in parameter_list:
                        param_name = param.find('span', class_="tsd-kind-parameter").text
                        param_description = ''
                        if param.find('div', class_="tsd-comment"):
                            param_description = md(str(param.find('div', class_="tsd-comment"))).strip()
                            if (len(param_description.split('\n')) > 1):
                                param_description = param_description.replace('\n', '\n  ').rstrip()

                        signature = method.find(class_='tsd-signature').text
                        param_type = md(str(param.find(class_="tsd-signature-type"))).strip()

                        if param_description:
                            param_usage = "%s (%s) - %s" % (param_name, param_type, param_description)
                        else:
                            param_usage = "%s (%s)" % (param_name, param_type)

                        param_object[param_name] = {
                            'optional': param_name + '?' in signature, # todo
                            'param_description': param_description,
                            'param_type':param_type,
                            'param_usage': param_usage
                        }

                returns = md(str(method.find('h4', class_="tsd-returns-title"))).replace("#### Returns ", "").strip().replace('\\', '')
                returns = " ".join(returns.split())
                return_description = ""
                if method.find('h4', class_="tsd-returns-title").next_sibling:
                    if not method.find('h4', class_="tsd-returns-title").next_sibling.get('class'):
                        return_description = md(str(method.find('h4', class_="tsd-returns-title").next_sibling)).strip()
                    else:
                        return_description = None
                else:
                    return_description = None

                return_object = {
                    'return_description': return_description,
                    'return_type': returns,
                    'return_usage': returns
                }

                method_description = ""
                if method.find('li', class_="tsd-description"):
                    if method.find('li', class_="tsd-description").find('div', class_="tsd-comment"):
                        method_description = method.find('li', class_="tsd-description").find('div', class_="tsd-comment").text.strip()

                code_sample = ""
                if method.find('div', class_='tsd-tag-example'):
                    code_sample_full = method.find('div', class_='tsd-tag-example').find('pre')
                    code_sample_full.find('button').decompose()
                    code_sample_draft = md(str(code_sample_full)).replace('```', "").strip()
                    code_sample = ""
                    for line in code_sample_draft.split('\n'):
                        code_sample = code_sample + line.rstrip() + "\n"

                self.typescript_methods[type][resource][method_name] = {
                    'method_description': method_description,
                    'method_link': method.find('a', class_='tsd-anchor-icon')["href"],
                    'parameters': param_object,
                    'proto': '', # method_name ?
                    'return': return_object
                }

                if code_sample:
                    self.typescript_methods[type][resource][method_name]["code_sample"] = code_sample


        return self.typescript_methods
