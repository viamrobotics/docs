import re as regex

from parser_utils import make_soup


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
    "data_manager": "datamanager",
    "data": "DataClient",
    "dataset": "DataClient"
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


class GoParser:
    def __init__(self, proto_map_file, go_staging_url = None):
        self.proto_map_file = proto_map_file
        self.sdk_url = "https://pkg.go.dev"

        if go_staging_url:
            self.scrape_url = go_staging_url
            self.staging = True
        else:
            self.scrape_url = "https://pkg.go.dev"
            self.staging = False
        self.go_methods = {}


    def parse(self, type, viam_resources):
        self.go_methods[type] = {}

        for resource in viam_resources:

            ## Determine URL form for Go depending on type (like 'component'):
            if type in ("component", "service") and resource in go_resource_overrides:
                url = f"{self.scrape_url}/go.viam.com/rdk/{type}s/{go_resource_overrides[resource]}"
            elif type in ("component", "service"):
                url = f"{self.scrape_url}/go.viam.com/rdk/{type}s/{resource}"
            elif type == "robot" and resource in go_resource_overrides:
                url = f"{self.scrape_url}/go.viam.com/rdk/{type}/{go_resource_overrides[resource]}"
            elif type == "robot":
                url = f"{self.scrape_url}/go.viam.com/rdk/{type}"
            elif type == "app":
                url = f"{self.scrape_url}/go.viam.com/rdk/{type}"
                print(url)

            self.go_methods[type][resource] = {}


            ## Scrape each parent method tag and all contained child tags for Go by resource:
            ## Skip Go: App (Go has no App client) and the generic component and service, which
            ## require explicit in-script workaround (DoCommand neither inherited (from resource.Resource)
            ## nor explicitly defined in-interface (not in Go docs, only in un-doc'd code):
            if resource != "generic_component" and resource != "generic_service":

                soup = make_soup(url)

                ## Get a raw dump of all go methods by interface for each resource:
                if type == "app":
                    ## For app resources, look for client type definitions instead of interfaces
                    go_methods_raw = soup.find_all(
                        lambda tag: tag.name == 'div'
                        and tag.get('class') == ['Documentation-declaration']
                        and tag.pre.text.startswith('func (')
                        and any(client in tag.pre.text for client in ["DataClient", "AppClient", "BillingClient", "MLTrainingClient"]))
                else:
                    go_methods_raw = soup.find_all(
                        lambda tag: tag.name == 'div'
                        and tag.get('class') == ['Documentation-declaration']
                        and tag.pre.text.startswith('type')
                        and "interface {" in tag.pre.text)

                if type == "app":
                    ## For app resources, process function definitions directly
                    for func_div in go_methods_raw:
                        ## Extract method name from function definition
                        func_text = func_div.find('pre').text
                        if 'DataClient' in func_text:
                            method_name = func_text.split(') ')[1].split('(')[0]

                            ## Create new empty dictionary for this specific method
                            this_method_dict = {}

                            ## Check if this method is mapped to the current resource in the CSV file
                            method_mapped_to_resource = False
                            with open(self.proto_map_file, 'r') as f:
                                for row in f:
                                    if not row.startswith('#') \
                                    and row.startswith(resource + ',') \
                                    and row.split(',')[4] == method_name:
                                        method_mapped_to_resource = True
                                        break

                            ## Only include methods that are mapped to this resource
                            if method_mapped_to_resource:

                                ## Exclude unwanted Go methods:
                                check_method_name = resource + '.' + method_name
                                if not check_method_name in go_ignore_apis:

                                    ## Debug: Print found methods for app resources
                                    if type == "app":
                                        print(f"Found method: {method_name} for resource: {resource}")

                                    ## Look up method_name in proto_map file, and return matching proto:
                                    with open(self.proto_map_file, 'r') as f:
                                        for row in f:
                                            if not row.startswith('#') \
                                            and row.startswith(resource + ',') \
                                            and row.split(',')[4] == method_name:
                                                this_method_dict["proto"] = row.split(',')[1]

                                ## Extract method description
                                method_description = ""
                                if func_div.find('p'):
                                    method_description = func_div.find('p').text.replace("\n", " ")
                                this_method_dict["description"] = method_description

                                ## Extract method usage
                                this_method_dict["usage"] = func_text.replace("\t", "  ").lstrip().rstrip()

                                ## Set method link
                                if self.staging:
                                    this_method_dict["method_link"] = str(url + '#DataClient.' + method_name).replace(self.scrape_url, 'https://pkg.go.dev')
                                else:
                                    this_method_dict["method_link"] = url + '#DataClient.' + method_name

                                ## Store the method
                                self.go_methods[type][resource][method_name] = this_method_dict

                else:
                    # some resources have more than one interface:
                    for resource_interface in go_methods_raw:

                        ## Determine the interface name, which we need for the method_link:
                        interface_name = resource_interface.find('pre').text.splitlines()[0].removeprefix('type ').removesuffix(' interface {')

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

                                ## Debug: Print found methods for app resources
                                if type == "app":
                                    print(f"Found method: {method_name} for resource: {resource}")

                                ## Look up method_name in proto_map file, and return matching proto:
                                with open(self.proto_map_file, 'r') as f:
                                    for row in f:
                                        if not row.startswith('#') \
                                        and row.startswith(resource + ',') \
                                        and row.split(',')[4] == method_name:
                                            this_method_dict["proto"] = row.split(',')[1]

                                ## Extract the raw text from resource_interface matching method_name.
                                ## Split by method span, throwing out remainder of span tag, catching cases where
                                ## id is first attr or data-kind is first attr, and slicing to omit the first match,
                                ## which is the opening of the method span tag, not needed:
                                split_result = regex.split(r'id="' + tag_id + '"', str(resource_interface))
                                if len(split_result) > 1:
                                    this_method_raw1 = split_result[1].removeprefix('>').removeprefix(' data-kind="method">').lstrip()
                                else:
                                    continue

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
                                method_usage_raw2 = regex.sub(r'</span>', '', method_usage_raw).replace("\t", "  ").lstrip().rstrip()
                                ## Some Go params use versioned links, some omit the version (to use latest).
                                ## Standardize on using latest for all cases. This handles parameters and returns:
                                this_method_dict["usage"] = regex.sub(r'/rdk@v[0-9\.]*/', '/rdk/', method_usage_raw2, flags=regex.DOTALL)

                                ## Not possible to link to the specific functions, so we link to the parent resource instead.
                                ## If we are scraping from a local staging instance, replace host and port with upstream link target URL:
                                if self.staging:
                                    this_method_dict["method_link"] = str(url + '#' + interface_name).replace(self.scrape_url, 'https://pkg.go.dev')
                                else:
                                    this_method_dict["method_link"] = url + '#' + interface_name

                                ## Check for code sample for this method.
                                go_code_samples_raw = soup.find_all(
                                    lambda code_sample_tag: code_sample_tag.name == 'p'
                                    and code_sample_tag.text.startswith(method_name)
                                    and code_sample_tag.text.endswith(method_name + ' example:\n'))

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
                                self.go_methods[type][resource][method_name] = this_method_dict

                        ## If this Go interface inherits from another interface, also fetch data for those inherited methods:
                        if '\tresource.' in resource_interface.text:

                            resource_url = f"{self.scrape_url}/go.viam.com/rdk/resource"
                            resource_soup = make_soup(resource_url)

                            ## If the resource being considered inherits from resource.Resource (currently all components and services do,
                            ## and no app or robot interfaces do), then add the three inherited methods manually: Reconfigure(), DoCommand(), Close()
                            if '\tresource.Resource' in resource_interface.text:
                                self.go_methods[type][resource]['Reconfigure'] = {'proto': 'Reconfigure', \
                                    'description': 'Reconfigure must reconfigure the resource atomically and in place. If this cannot be guaranteed, then usage of AlwaysRebuild or TriviallyReconfigurable is permissible.', \
                                    'usage': 'Reconfigure(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, deps <a href="#Dependencies">Dependencies</a>, conf <a href="#Config">Config</a>) <a href="/builtin#error">error</a>', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "Reconfigure example:" in code_sample_tag.text)
                                if code_sample:
                                    self.go_methods[type][resource]['Reconfigure']['code_sample'] = code_sample[0].find_next('pre').text.replace("\t", "  ")
                                self.go_methods[type][resource]['DoCommand'] = {'proto': 'DoCommand', \
                                    'description': 'DoCommand sends/receives arbitrary data.', \
                                    'usage': 'DoCommand(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, cmd map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "DoCommand example:" in code_sample_tag.text)
                                if code_sample:
                                    if type == "component":
                                        self.go_methods[type][resource]['DoCommand']['code_sample'] = 'my' + resource.title().replace("_", "")+ ', err := ' + resource + '.FromRobot(machine, "my_' + resource + '")\n\ncommand := map[string]interface{}{"cmd": "test", "data1": 500}\nresult, err := my' + resource.title().replace("_", "") + '.DoCommand(context.Background(), command)\n'
                                        if resource == "generic_component":
                                            self.go_methods[type][resource]['DoCommand']['code_sample'] = 'myGenericComponent, err := generic.FromRobot(machine, "my_generic_component")\n\ncommand := map[string]interface{}{"cmd": "test", "data1": 500}\nresult, err := myGenericComponent.DoCommand(context.Background(), command)\n'
                                    else:
                                        self.go_methods[type][resource]['DoCommand']['code_sample'] = 'my' + resource.title().replace("_", "")+ 'Svc, err := ' + resource.replace("_","") + '.FromRobot(machine, "my_' + resource + '_svc")\n\ncommand := map[string]interface{}{"cmd": "test", "data1": 500}\nresult, err := my' + resource.title().replace("_", "") + 'Svc.DoCommand(context.Background(), command)\n'
                                        if resource == "slam":
                                            self.go_methods[type][resource]['DoCommand']['code_sample'] = 'mySLAMService, err := slam.FromRobot(machine, "my_slam_svc")\n\ncommand := map[string]interface{}{"cmd": "test", "data1": 500}\nresult, err := mySLAMService.DoCommand(context.Background(), command)\n'

                                self.go_methods[type][resource]['Close'] = {'proto': 'Close', \
                                    'description': 'Close must safely shut down the resource and prevent further use. Close must be idempotent. Later reconfiguration may allow a resource to be "open" again.', \
                                    'usage': 'Close(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>) <a href="/builtin#error">error</a>', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "Close example:" in code_sample_tag.text)
                                if code_sample:
                                    if type == "component":
                                        self.go_methods[type][resource]['Close']['code_sample'] = 'my' + resource.title().replace("_", "") + ', err := ' + go_resource_overrides.get(resource, resource) + '.FromRobot(machine, "my_' + resource + '")\n\nerr = my' + resource.title().replace("_", "") + '.Close(context.Background())\n'
                                    else:
                                        if resource == "base_remote_control":
                                            self.go_methods[type][resource]['Close']['code_sample'] = 'baseRCService, err := baseremotecontrol.FromRobot(machine, "my_baseRCService_svc")\n\nerr := baseRCService.Close(context.Background())\n'
                                        elif resource == "data_manager":
                                            self.go_methods[type][resource]['Close']['code_sample'] = 'data, err := datamanager.FromRobot(machine, "my_data_manager")\n\nerr := data.Close(context.Background())\n'
                                        elif resource == "navigation":
                                            self.go_methods[type][resource]['Close']['code_sample'] = 'my_nav, err := navigation.FromRobot(machine, "my_nav_svc")\n\nerr := my_nav.Close(context.Background())\n'
                                        elif resource == "mlmodel":
                                            self.go_methods[type][resource]['Close']['code_sample'] = 'my_mlmodel, err := mlmodel.FromRobot(machine, "my_ml_model")\n\nerr := my_mlmodel.Close(context.Background())\n'
                                        else:
                                            self.go_methods[type][resource]['Close']['code_sample'] = 'my' + resource.title().replace("_", "") + 'Svc, err := ' + resource + '.FromRobot(machine, "my_' + resource + '_svc")\n\nerr = my' + resource.title().replace("_", "") + 'Svc.Close(context.Background())\n'

                            ## Similarly, if the resource being considered inherits from resource.Actuator (Servo, for example),
                            ## then add the two inherited methods manually: IsMoving() and Stop():
                            if '\tresource.Actuator' in resource_interface.text:
                                self.go_methods[type][resource]['IsMoving'] = {'proto': 'IsMoving', \
                                    'description': 'IsMoving returns whether the resource is moving or not', \
                                    'usage': 'IsMoving(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>) (<a href="/builtin#bool">bool</a>, <a href="/builtin#error">error</a>)', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Actuator'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "IsMoving example:" in code_sample_tag.text)
                                if code_sample:
                                    self.go_methods[type][resource]['IsMoving']['code_sample'] = code_sample[0].find_next('pre').text.replace("\t", "  ")
                                self.go_methods[type][resource]['Stop'] = {'proto': 'Stop', \
                                    'description': 'Stop stops all movement for the resource', \
                                    'usage': 'Stop(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, extra map[<a href="/builtin#string">string</a>]interface{}) <a href="/builtin#error">error</a>', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Actuator'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "Stop example:" in code_sample_tag.text)
                                if code_sample:
                                    self.go_methods[type][resource]['Stop']['code_sample'] = code_sample[0].find_next('pre').text.replace("\t", "  ")

                            ## Similarly, if the resource being considered inherits from resource.Shaped (Base, for example),
                            ## then add the one inherited method manually: Geometries():
                            if '\tresource.Shaped' in resource_interface.text:
                                self.go_methods[type][resource]['Geometries'] = {'proto': 'GetGeometries', \
                                    'description': 'Geometries returns the list of geometries associated with the resource, in any order. The poses of the geometries reflect their current location relative to the frame of the resource.', \
                                    'usage': 'Geometries(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, extra map[<a href="/builtin#string">string</a>]interface{}) (<a href="/go.viam.com/rdk/spatialmath#Geometry">[]spatialmath.Geometry</a>, <a href="/builtin#error">error</a>)', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Shaped'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "Geometries example:" in code_sample_tag.text)
                                if code_sample:
                                    self.go_methods[type][resource]['Geometries']['code_sample'] = code_sample[0].find_next('pre').text.replace("\t", "  ").replace('myArm', 'my{}'.format(resource.title().replace('_', ''))).replace('my_arm', 'my_{}'.format(resource)).replace('arm', resource)

                            ## Similarly, if the resource being considered inherits from resource.Sensor (Movement Sensor, for example),
                            ## then add the one inherited method manually: Readings():
                            if '\tresource.Sensor' in resource_interface.text:
                                self.go_methods[type][resource]['Readings'] = {'proto': 'GetReadings', \
                                    'description': 'Readings return data specific to the type of sensor and can be of any type.', \
                                    'usage': 'Readings(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, extra map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Sensor'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "Readings example:" in code_sample_tag.text)
                                if code_sample:
                                    self.go_methods[type][resource]['Readings']['code_sample'] = code_sample[0].find_next('pre').text.replace("\t", "  ")

                            ## Similarly, if the resource being considered inherits from framesystem.InputEnabled (Arm, for example),
                            ## then add the one inherited method manually: Kinematics():
                            if '\tframesystem.InputEnabled' in resource_interface.text:
                                self.go_methods[type][resource]['Kinematics'] = {'proto': 'GetKinematics', \
                                    'description': 'Kinematics returns the kinematics model of the resource.', \
                                    'usage': 'Kinematics(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, extra map[<a href="/builtin#string">string</a>]interface{}) (<a href="/go.viam.com/rdk/referenceframe#Model">referenceframe.Model</a>, <a href="/builtin#error">error</a>)', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#InputEnabled'}
                                code_sample = resource_soup.find_all(lambda code_sample_tag: code_sample_tag.name == 'p' and "Kinematics example:" in code_sample_tag.text)
                                if code_sample:
                                    self.go_methods[type][resource]['Kinematics']['code_sample'] = code_sample[0].find_next('pre').text.replace("\t", "  ")

                ## For SLAM service only, additionally fetch data for two helper methods defined outside of the resource's interface:
                if resource == 'slam':

                    ## Fetch PointCloudMapFull:
                    pointcloudmapfull_method_raw = soup.find_all(
                        lambda tag: tag.name == 'div'
                        and tag.get('class') == ['Documentation-declaration']
                        and "PointCloudMapFull" in tag.pre.text)

                    self.go_methods[type][resource]['PointCloudMapFull'] = {}
                    self.go_methods[type][resource]['PointCloudMapFull']['proto'] = 'PointCloudMapFull'
                    self.go_methods[type][resource]['PointCloudMapFull']['description'] = pointcloudmapfull_method_raw[0].pre.find_next('p').text
                    self.go_methods[type][resource]['PointCloudMapFull']['usage'] = str(pointcloudmapfull_method_raw[0].pre).removeprefix('<pre>func ').removesuffix('</pre>')
                    self.go_methods[type][resource]['PointCloudMapFull']['method_link'] = 'https://pkg.go.dev/go.viam.com/rdk/services/slam#PointCloudMapFull'

                    ## Fetch InternalStateFull:
                    internalstatefull_method_raw = soup.find_all(
                        lambda tag: tag.name == 'div'
                        and tag.get('class') == ['Documentation-declaration']
                        and "InternalStateFull" in tag.pre.text)

                    self.go_methods[type][resource]['InternalStateFull'] = {}
                    self.go_methods[type][resource]['InternalStateFull']['proto'] = 'InternalStateFull'
                    self.go_methods[type][resource]['InternalStateFull']['description'] = internalstatefull_method_raw[0].pre.find_next('p').text
                    self.go_methods[type][resource]['InternalStateFull']['usage'] = str(internalstatefull_method_raw[0].pre).removeprefix('<pre>func ').removesuffix('</pre>')
                    self.go_methods[type][resource]['InternalStateFull']['method_link'] = 'https://pkg.go.dev/go.viam.com/rdk/services/slam#InternalStateFull'


            ## Assemble workaround data object for DoCommand for Go generic component and service.
            ## Using code sample and method_link from resource.Resource, because these cannot be found
            ## in Go docs for these resources:
            elif resource == "generic_component" or resource == "generic_service":

                self.go_methods[type][resource]['DoCommand'] = {}
                self.go_methods[type][resource]['DoCommand'] = {'proto': 'DoCommand', \
                                    'description': 'DoCommand sends/receives arbitrary data.', \
                                    'usage': 'DoCommand(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, cmd map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                    'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource', \
                                    'code_sample': 'my' + resource.title().replace("_", "") + ', err := generic.FromRobot(machine, "my_' + resource.lower() + '")\n\ncommand := map[string]interface{}{"cmd": "test", "data1": 500}\nresult, err := my' + resource.title().replace("_", "") + '.DoCommand(context.Background(), command)\n'}
                if resource == "generic_service":
                    self.go_methods[type][resource]['DoCommand']['code_sample'] = 'myGenericService, err := generic.FromRobot(machine, "my_generic_service")\n\ncommand := map[string]interface{}{"cmd": "test", "data1": 500}\nresult, err := myGenericService.DoCommand(context.Background(), command)\n'

        return self.go_methods

