from parser_utils import make_soup
from markdownify import markdownify as md
from urllib.parse import urljoin

## Language-specific resource name overrides:
typescript_resource_overrides = {
    "generic_component": "GenericComponent",
    "generic_service": "GenericService",
    "movement_sensor": "MovementSensor",
    "power_sensor": "PowerSensor",
    "vision": "Vision",
    "robot": "Robot",
    "data": "Data",
    "dataset": "Data",
    "data_sync": "Data",
    "data_manager": "DataManager",
    "mltraining": "MlTraining"
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
            "base_remote_control", "input_controller", "pose_tracker",
            "mlmodel"
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

            for a in soup.find_all('a'):
                if a.get('href') and not a.get('href').startswith('http'):
                    a['href'] = urljoin(url, a.get('href'))

            top_level_sections = soup.find_all(class_='tsd-member-group')
            methods = []

            for section in top_level_sections:
                if 'Methods' in section.find('h2').text:
                    methods = section.find_all('section', class_='tsd-panel tsd-member')
                if resource == 'robot':
                    if section.find('h2').text.strip() in ['App/Cloud', 'ComponentConfig', 'Discovery', "Frame System", "Operations", "Resources", "Sessions"]:
                        methods.extend(section.find_all('section', class_='tsd-panel tsd-member'))


            for method in methods:
                method_name = method.find('h3').text

                param_object = {}
                if method.find('div', class_="tsd-parameters"):
                    parameters = method.find('div', class_="tsd-parameters").find_all('li')

                    for param in parameters:
                        param_name = param.find('span', class_="tsd-kind-parameter").text
                        param_description = ''
                        if param.find('div', class_="tsd-comment"):
                            param_description = param.find('div', class_="tsd-comment").text
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
                return_description = md(str(method.find('h4', class_="tsd-returns-title").next_sibling)).strip()

                return_object = {
                    'return_description': return_description,
                    'return_type': returns,
                    'return_usage': returns
                }

                method_description = ""
                if method.find('li', class_="tsd-description"):
                    if method.find('li', class_="tsd-description").find('div', class_="tsd-comment"):
                        method_description = method.find('li', class_="tsd-description").find('div', class_="tsd-comment").text.strip()

                self.typescript_methods[type][resource][method_name] = {
                    'method_description': method_description,
                    'method_link': method.find('a', class_='tsd-anchor-icon')["href"],
                    'parameters': param_object,
                    'proto': '', # method_name ?
                    'return': return_object
                }
                    # 'code_sample': "", # No code samples yet method.find('pre').text
                # print(self.typescript_methods[type][resource][method_name])
                # print()


        return self.typescript_methods
