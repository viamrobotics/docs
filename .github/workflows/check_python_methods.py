from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

services = ["motion", "navigation", "sensors", "slam", "vision", "mlmodel"]
components = ["arm", "base", "board", "camera", "encoder", "gantry", "generic", "gripper", 
              "input", "movement_sensor", "power_sensor", "sensor"]
app_apis = ["data_client", "app_client"]
robot_apis = ["robot"]


def make_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")
    

def parse(type, names):

    sdk_methods_missing = []
    sdk_methods_found = []

    for service in names:

        # Parse the Python doc's sites service client page
        if type == "app":
            soup = make_soup(f"https://python.viam.dev/autoapi/viam/{type}/{service}/index.html")
        elif type == "robot":
            soup = make_soup(f"https://python.viam.dev/autoapi/viam/{type}/client/index.html")
        else:
            soup = make_soup(f"https://python.viam.dev/autoapi/viam/{type}/{service}/client/index.html")

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
        py_methods_sdk_docs = soup.find_all("dt", class_="sig sig-object py")
        py_methods_sdk_docs_filtered = []

        # Get ids and filter list
        for tag in py_methods_sdk_docs:
            id = tag.get('id')

            if not id.endswith("Client") and not id.endswith(".client") \
            and not id.endswith("SUBTYPE") and not id.endswith(".from_robot") \
            and not id.endswith(".get_resource_name") and not id.endswith(".get_operation") \
            and not id.endswith(".LOGGER") and not id.endswith("__"):
                py_methods_sdk_docs_filtered.append(id)
    
        # Parse the Docs site's service page
        if type == "app" or type == "robot":
            soup2 = make_soup(f"https://docs.viam.com/program/apis/{service}/")
        else:
            soup2 = make_soup(f"https://docs.viam.com/{type}/{service}/")

        # Find all links on Docs site soup
        all_links = soup2.find_all('a')

        # Go through ids in filtered list and check if it matches text in href in a link on Docs site
        for id in py_methods_sdk_docs_filtered:
            found = 0

            # Separating out just the method name
            id_split = id.split("Client.")
            if len(id_split) > 1:
                id_split = id_split[1]
            else: 
                id_split = id

            print(f"SPLIT ID {id_split}")
            for link in all_links:
                
                href = link.get('href')

                if href:
                    if id_split in href:
                        print(f"Found a link containing '{id}' in href: {href}")
                        sdk_methods_found.append(id)
                        found += 1
                        break

            if not found and id != "viam.components.generic.client.do_command":
                sdk_methods_missing.append(id)
        

    print(f"\n SDK methods missing for type {type}: {sdk_methods_missing}")
    print(f"\n SDK methods found for type {type}: {sdk_methods_found}")

    return sdk_methods_missing

total_sdk_methods_missing = []      

total_sdk_methods_missing.extend(parse("services", services))
total_sdk_methods_missing.extend(parse("components", components))
# total_sdk_methods_missing.extend(parse("app", app_apis))
# total_sdk_methods_missing.extend(parse("robot", robot_apis))

if total_sdk_methods_missing:
        print(f"\n Total SDK methods missing: {total_sdk_methods_missing}")
        sys.exit(1)