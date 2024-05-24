import re as regex
import subprocess


from automation_lang_specifics.shared_tools import make_soup


## Language-specific resource name overrides:
##   "proto_resource_name" : "language-specific_resource_name"
##   "as-it-appears-in-type-array": "as-it-is-used-per-sdk"
## Note: Always remap generic component and service, for all languages,
##       as this must be unique for this script, but is non-unique across sdks.
GO_RESOURCE_OVERRIDES = {
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
GO_IGNORE_APIS = [
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
GO_DATATYPE_LINKS = {
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

class GoParser():
    def __init__(self, verbose):
        self.verbose = verbose
        self.is_go_sdk_staging_available = False
        self.go_methods = {}

        ## Check to see if pkgsite (Go SDK docs local builder process) is running, and get its PID if so:
        process_result = subprocess.run(["ps -ef | grep pkgsite | grep -v grep | awk {'print $2'}"], shell=True, text = True, capture_output=True)
        pkgsite_pid = process_result.stdout.rstrip()

        if pkgsite_pid != '':
            process_result = subprocess.run(["lsof -Pp " + pkgsite_pid + " | grep LISTEN | awk {'print $9'} | sed 's%.*:%%g'"], shell=True, text = True, capture_output=True)
            pkgsite_port = process_result.stdout
            self.is_go_sdk_staging_available = True
            if self.verbose:
                print('DEBUG: Detected local staged Go SDK docs URL, using that for Go code samples.')

    def parse(self, sdk_url, type, resources, proto_map_file):
        self.go_methods[type] = {}

        for resource in resources:
            ## Determine URL form for Go depending on type (like 'component'):
            if type in ("component", "service") and resource in GO_RESOURCE_OVERRIDES:
                url = f"{sdk_url}/go.viam.com/rdk/{type}s/{GO_RESOURCE_OVERRIDES[resource]}"
            elif type in ("component", "service"):
                url = f"{sdk_url}/go.viam.com/rdk/{type}s/{resource}"
            elif type == "robot" and resource in GO_RESOURCE_OVERRIDES:
                url = f"{sdk_url}/go.viam.com/rdk/{type}/{GO_RESOURCE_OVERRIDES[resource]}"
            elif type == "robot":
                url = f"{sdk_url}/go.viam.com/rdk/{type}"
            elif type == "app":
                pass
            self.go_methods[type][resource] = {}

            ## Scrape each parent method tag and all contained child tags for Go by resource:
            if type != "app":

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
                    if not check_interface_name in GO_IGNORE_APIS:

                        ## Loop through each method found for this interface:
                        for tag in resource_interface.find_all('span', attrs={"data-kind" : "method"}):

                            ## Create new empty dictionary for this specific method, to be appended to ongoing go_methods dictionary,
                            ## in form: go_methods[type][resource][method_name] = this_method_dict
                            this_method_dict = {}

                            tag_id = tag.get('id')
                            method_name = tag.get('id').split('.')[1]

                            ## Exclude unwanted Go methods:
                            check_method_name = resource + '.' + method_name
                            if not check_method_name in GO_IGNORE_APIS:

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
                                if self.is_go_sdk_staging_available:

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
                                self.go_methods[type][resource][method_name] = this_method_dict

                        ## Go SDK docs for each interface omit inherited functions. If the resource being considered inherits from
                        ## resource.Resource (currently all components and services do, and no app or robot interfaces do), then add
                        ## the three inherited methods manually: Reconfigure(), DoCommand(), Close()
                        ## (Match only to instances that are preceded by a tab char, or we'll catch ResourceByName erroneously):
                        if '\tresource.Resource' in resource_interface.text:
                            self.go_methods[type][resource]['Reconfigure'] = {'proto': 'Reconfigure', \
                                'description': 'Reconfigure must reconfigure the resource atomically and in place. If this cannot be guaranteed, then usage of AlwaysRebuild or TriviallyReconfigurable is permissible.', \
                                'usage': 'Reconfigure(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, deps <a href="#Dependencies">Dependencies</a>, conf <a href="#Config">Config</a>) <a href="/builtin#error">error</a>', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                            self.go_methods[type][resource]['DoCommand'] = {'proto': 'DoCommand', \
                                'description': 'DoCommand sends/receives arbitrary data.', \
                                'usage': 'DoCommand(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, cmd map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}
                            self.go_methods[type][resource]['Close'] = {'proto': 'Close', \
                                'description': 'Close must safely shut down the resource and prevent further use. Close must be idempotent. Later reconfiguration may allow a resource to be "open" again.', \
                                'usage': 'Close(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>) <a href="/builtin#error">error</a>', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Resource'}

                        ## Similarly, if the resource being considered inherits from resource.Actuator (Servo, for example),
                        ## then add the two inherited methods manually: IsMoving() and Stop():
                        if '\tresource.Actuator' in resource_interface.text:
                            self.go_methods[type][resource]['IsMoving'] = {'proto': 'IsMoving', \
                                'description': 'IsMoving returns whether the resource is moving or not', \
                                'usage': 'IsMoving(<a href="/context">context</a>.<a href="/context#Context">Context</a>) (<a href="/builtin#bool">bool</a>, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Actuator'}
                            self.go_methods[type][resource]['Stop'] = {'proto': 'Stop', \
                                'description': 'Stop stops all movement for the resource', \
                                'usage': 'Stop(<a href="/context">context</a>.<a href="/context#Context">Context</a>, map[<a href="/builtin#string">string</a>]interface{}) <a href="/builtin#error">error</a>', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Actuator'}

                        ## Similarly, if the resource being considered inherits from resource.Shaped (Base, for example),
                        ## then add the one inherited method manually: Geometries():
                        if '\tresource.Shaped' in resource_interface.text:
                            self.go_methods[type][resource]['Geometries'] = {'proto': 'GetGeometries', \
                                'description': 'Geometries returns the list of geometries associated with the resource, in any order. The poses of the geometries reflect their current location relative to the frame of the resource.', \
                                'usage': 'Geometries(<a href="/context">context</a>.<a href="/context#Context">Context</a>, map[<a href="/builtin#string">string</a>]interface{}) ([]<a href="/go.viam.com/rdk/spatialmath">spatialmath</a>.<a href="/go.viam.com/rdk/spatialmath#Geometry">Geometry</a>, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Shaped'}

                        ## Similarly, if the resource being considered inherits from resource.Sensor (Movement Sensor, for example),
                        ## then add the one inherited method manually: Readings():
                        if '\tresource.Sensor' in resource_interface.text:
                            self.go_methods[type][resource]['Readings'] = {'proto': 'GetReadings', \
                                'description': 'Readings return data specific to the type of sensor and can be of any type.', \
                                'usage': 'Readings(ctx <a href="/context">context</a>.<a href="/context#Context">Context</a>, extra map[<a href="/builtin#string">string</a>]interface{}) (map[<a href="/builtin#string">string</a>]interface{}, <a href="/builtin#error">error</a>)', \
                                'method_link': 'https://pkg.go.dev/go.viam.com/rdk/resource#Sensor'}

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
                    self.go_methods[type][resource]['PointCloudMapFull']['usage'] = pointcloudmapfull_method_raw[0].pre.text.removeprefix('func ')
                    self.go_methods[type][resource]['PointCloudMapFull']['method_link'] = 'https://pkg.go.dev/go.viam.com/rdk/services/slam#PointCloudMapFull'

                    ## Fetch InternalStateFull:
                    internalstatefull_method_raw = soup.find_all(
                        lambda tag: tag.name == 'div'
                        and tag.get('class') == ['Documentation-declaration']
                        and "InternalStateFull" in tag.pre.text)

                    self.go_methods[type][resource]['InternalStateFull'] = {}
                    self.go_methods[type][resource]['InternalStateFull']['proto'] = 'InternalStateFull'
                    self.go_methods[type][resource]['InternalStateFull']['description'] = internalstatefull_method_raw[0].pre.find_next('p').text
                    self.go_methods[type][resource]['InternalStateFull']['usage'] = internalstatefull_method_raw[0].pre.text.removeprefix('func ')
                    self.go_methods[type][resource]['InternalStateFull']['method_link'] = 'https://pkg.go.dev/go.viam.com/rdk/services/slam#InternalStateFull'

                ## We have finished looping through all scraped Go methods. Write the self.go_methods dictionary
                ## in its entirety to the all_methods dictionary using "go" as the key:

            else: # if type == "app"
                ##Go SDK has no APP API!
                pass

        return self.go_methods[type]
