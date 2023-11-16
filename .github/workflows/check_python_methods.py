from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import markdownify
import urllib.parse
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--local', action='store_true', required=False)

args = parser.parse_args()

services = ["motion", "navigation", "sensors", "slam", "vision", "mlmodel"]
components = ["arm", "base", "board", "camera", "encoder", "gantry", "generic", "gripper",
              "input", "movement_sensor", "power_sensor", "sensor"]
app_apis = ["data_client", "app_client"]
robot_apis = ["robot"]

ignore_apis = [
    'viam.app.app_client.RobotPart.from_proto',
    'viam.app.app_client.LogEntry.from_proto',
    'viam.app.app_client.Fragment.from_proto',
    'viam.app.app_client.RobotPartHistoryEntry.from_proto',
    'viam.app.app_client.AppClient.get_rover_rental_parts',
    'viam.app.data_client.DataClient.create_filter' # deprecated
]

def is_unimplemented(obj):
   if obj.find(class_="property"):
       return "abstract" in obj.find(class_="property").text
   else:
       return False

def make_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def html_to_markdown(base_url, html):
    for url in html.find_all('a'):
        url["href"] = urllib.parse.urljoin(base_url,url.get('href'))

    return markdownify.markdownify(str(html)).strip()

def get_param_details(item):
    param, desc = item.split(" – ")
    if "** (" in param:
        param_name, param_type = param.split("** (")
        param_type = param_type[:-1].replace("*","")
        param_name = param_name.replace("**","")
        return f"- {param_name} ({param_type}): {desc}\n".format(param_name=param_name, param_type=param_type, desc=desc)
    else:
        param_name = param.replace("**","")
        return "- {param_name}: {desc}\n".format(param_name=param_name, desc=desc)

def parse(type, names):

    sdk_methods_missing = []
    sdk_methods_found = []
    methods_dict = {}

    for service in names:

        # Parse the Python doc's sites service client page
        if type == "app":
            url = f"https://python.viam.dev/autoapi/viam/{type}/{service}/index.html"
        elif type == "robot":
            url = f"https://python.viam.dev/autoapi/viam/{type}/client/index.html"
        else:
            url = f"https://python.viam.dev/autoapi/viam/{type}/{service}/client/index.html"

        soup = make_soup(url)

        # Hacky because they're not the same on SDK docs and Docs site
        if service == "mlmodel":
            service = "ml"

        if service == "input":
            service = "input-controller"

        if service == "movement_sensor":
            service = "movement-sensor"

        if service == "power_sensor":
            service = "power-sensor"

        if service == "data_client":
            service = "data-client"

        if service == "app_client":
            service = "cloud"

        # Find all python methods objects on Python docs site soup
        py_methods_sdk_docs = soup.find_all("dl", class_="py method")
        py_methods_sdk_docs_filtered_ids = []
        py_methods_sdk_docs_undocumented_ids = []

        # Get ids and filter list
        for tag in py_methods_sdk_docs:
            tag_sigobject = tag.find("dt", class_="sig sig-object py")
            id = tag_sigobject.get('id')

            if not id.endswith("Client") and not id.endswith(".client") \
            and not id.endswith("SUBTYPE") and not id.endswith(".from_robot") \
            and not id.endswith(".get_resource_name") and not id.endswith(".get_operation") \
            and not id.endswith(".LOGGER") and not id.endswith("__") \
            and not id in ignore_apis:
                if is_unimplemented(tag_sigobject):
                    py_methods_sdk_docs_undocumented_ids.append(id)
                else:
                    py_methods_sdk_docs_filtered_ids.append(id)


            # Get methods information
            method_text = []

            # Descriptions
            description = tag.find("dd")
            if description:
                for elem in description.find_all("p", recursive=False):
                    method_text.append(html_to_markdown(url, elem) + "\n")
            method_text.append("\n")

            # Description extras: Parameters, returns, raises
            extras = description.find("dl")
            if (extras):
                extras_fields = extras.find_all("dt")
                extras_values_wrapper = extras.find_all("dd")

                description_extras = dict()

                for i in range(len(extras_fields)):
                    extras_values = extras_values_wrapper[i].findChildren()[0]
                    field = extras_fields[i].text
                    description_extras[field] = extras_values

                # Parameters
                method_text.append("**Parameters:**\n\n")
                no_parameters = True
                if "Parameters:" in description_extras:
                    no_parameters = False
                    extras_values = description_extras["Parameters:"]

                    # if values are a list
                    if (extras_values.name == "ul"):
                        for li in extras_values.findChildren("li", recursive=False):
                            item = html_to_markdown(url, li)
                            try:
                                method_text.append(get_param_details(item))
                            except ValueError:
                                print(f"WARNING: Failed to extract value for \"{item}\" from {url}#{id}")
                    # if values are not a list
                    else:
                        item = html_to_markdown(url, extras_values)
                        method_text.append(get_param_details(item))

                param_element = tag_sigobject.find_all("em", class_="sig-param")
                if param_element:
                    for element in param_element:
                        if element.text == "extra: Optional[Dict[str, Any]] = None":
                            no_parameters = False
                            method_text.append("- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.\n")
                        if element.text == "timeout: Optional[float] = None":
                            no_parameters = False
                            method_text.append("- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.\n")
                if no_parameters:
                    method_text.append("- None.\n")

                method_text.append("\n")

                # Returns
                method_text.append("**Returns:**\n\n")
                if "Returns:" in description_extras:
                    # Return type
                    if "Return type:" in description_extras:
                        return_type = html_to_markdown(url, description_extras["Return type:"]).strip()
                        return_info = html_to_markdown(url, description_extras["Returns:"])

                        method_text.append("- (`{return_type}`): {return_info}\n".format(return_type=return_type, return_info=return_info))

                else:
                    method_text.append("- None.\n")

                method_text.append("\n")

                # Raises
                if "Raises:" in description_extras:
                    method_text.append("**Raises:**\n\n")

                    extras_values = description_extras["Raises:"]

                    # if values are a list
                    if (extras_values.name == "ul"):
                        for li in extras_values.findChildren("li", recursive=False):
                            method_text.append("- {li_item}\n".format(li_item=li.text))
                        method_text.append("\n")
                    # if values are not a list
                    else:
                        method_text.append("- {extra_values}\n\n".format(extra_values=extras_values.text))
            else:
                method_text.append("**Parameters:**\n\n")
                method_text.append("- None.\n\n")
                method_text.append("**Returns:**\n\n")
                method_text.append("- None.\n\n")


            method_text.append(f"For more information, see the [Python SDK Docs]({url}#{id}).")

            # Join all text together and add to methods list
            method_text = ''.join(method_text)
            methods_dict[id] = method_text + "\n"


        # Parse the Docs site's service page
        if args.local:
            if type == "app" or type == "robot":
                with open(f"dist/program/apis/{service}/index.html") as fp:
                    soup2 = BeautifulSoup(fp, 'html.parser')
            else:
                with open(f"dist/{type}/{service}/index.html") as fp:
                    soup2 = BeautifulSoup(fp, 'html.parser')
        else:
            if type == "app" or type == "robot":
                soup2 = make_soup(f"https://docs.viam.com/program/apis/{service}/")
            else:
                soup2 = make_soup(f"https://docs.viam.com/{type}/{service}/")

        # Find all links on Docs site soup
        all_links = soup2.find_all('a')

        # Go through ids in filtered list and check if it matches text in href in a link on Docs site
        for id in py_methods_sdk_docs_filtered_ids:
            found = 0

            # Separating out just the method name
            id_split = id.split("Client.")
            if len(id_split) > 1:
                id_split = id_split[1]
            # Hacky but was causing an issue
            elif id == "viam.components.generic.client.do_command":
                id_split = "do_command"
            else:
                id_split = id

            for link in all_links:

                href = link.get('href')

                if href:
                    if id_split in href:
                        # print(f"Found a link containing '{id}' in href: {href}")
                        sdk_methods_found.append(id)
                        found += 1
                        break

            if not found and id != "viam.components.board.client.DigitalInterruptClient.add_callback" \
            and id != "viam.components.board.client.DigitalInterruptClient.add_post_processor" \
            and id != "viam.components.input.client.ControllerClient.reset_channel":
                sdk_methods_missing.append(id)


    print(f"SDK methods missing for type {type}: {sdk_methods_missing}\n\n")
    print(f"SDK methods unimplemented for type {type}: {py_methods_sdk_docs_undocumented_ids}\n\n")
    print(f"SDK methods found for type {type}: {sdk_methods_found}\n\n")

    return sdk_methods_missing, methods_dict

def print_method_information(missing_methods, methods_dict):
    for method in missing_methods:
        print(f"Method: {method}\n\n{methods_dict.get(method)}")
        print("---\n")


total_sdk_methods_missing = []

missing_services, services_dict = parse("services", services)
missing_components, components_dict = parse("components", components)
missing_app_apis, app_apis_dict = parse("app", app_apis)
missing_robot_apis, robot_apis_dict = parse("robot", robot_apis)

total_sdk_methods_missing.extend(missing_services)
total_sdk_methods_missing.extend(missing_components)
total_sdk_methods_missing.extend(missing_app_apis)
total_sdk_methods_missing.extend(missing_robot_apis)

if total_sdk_methods_missing:
    print(f"Total SDK methods missing: {total_sdk_methods_missing} \n\nMissing Method Information:\n")
    print_method_information(missing_services, services_dict)
    print_method_information(missing_components, components_dict)
    print_method_information(missing_app_apis, app_apis_dict)
    print_method_information(missing_robot_apis, robot_apis_dict)
    # sys.exit(1)
