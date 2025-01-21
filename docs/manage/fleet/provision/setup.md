---
linkTitle: "Provision devices"
title: "Provision devices using viam-agent"
weight: 68
type: "docs"
description: "Provision a machine as it first comes online with a pre-defined configuration - in the factory or when the machine is taken into service."
tags: ["fleet management", "viam-server", "viam-agent"]
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Intermediate"
date: "2024-08-21"
prev: "/manage/fleet/reuse-configuration/"
next: "/manage/fleet/provision/end-user-setup/"
aliases:
  - "/build/provision/"
  - /how-tos/provision-setup/
  - fleet/provision/
# updated: ""  # When the tutorial was last entirely checked
# SMEs: James, Ale
cost: "0"
---

You can install [`viam-agent`](/manage/reference/viam-agent/) as part of your manufacturing process and provision machines with a pre-defined configuration as they come online.
When the end user sets the machine up, they provide network access and `viam-agent` installs `viam-server` and your latest software.

Consider a company that sells machines that monitor weather conditions on a maritime craft and provide navigation advice based on those readings.
The machines use the data management service to regularly capture and upload a stream of sensor readings.
To parse the readings and provide tailored guidance to a ship's captain, the company writes their own proprietary application.

By having the end customer set up the machine, the company:

- eliminates per-device setup and individualization at the factory
- allows for tailored configurations per customer as needed
- allows customer to provide their own WiFi credentials

This guide will show you how to install and configure `viam-agent`.

## Prerequisites

{{% expand "One or more physical devices with supported operating system" %}}

To find out more about supported systems, see [`viam-server` Platform requirements](/operate/get-started/setup/#supported-systems) and [`viam-micro-server` hardware requirements](/operate/reference/viam-micro-server/#hardware-requirements).

If you are flashing a Raspberry Pi using the Raspberry Pi Imager, flash a 64-bit image to your SD card and customize at least the hostname when prompted by the Raspberry Pi Imager.

When you customize the hostname or other settings, the Raspberry Pi Imager creates `firstrun.sh` which is required to set up provisioning.

Eject and reinsert the card to make sure it's mounted with the newly written contents.

{{% /expand%}}

{{< alert title="Support Notice" color="note" >}}

Provisioning is supported and tested on Ubuntu 22.04, Debian 11 (Bullseye), and 12 (Bookworm) but should work on most distros using NetworkManager v1.30 (or newer) as well.
For Bullseye, the installation of `viam-agent` changes the network configuration to use NetworkManager.

{{< /alert >}}

## Decide on the provisioning method

You can choose to let your end users complete machine setup by using a captive web portal or a mobile app.

If you choose to have a mobile app experience, you can use the [Viam mobile app](/manage/troubleshoot/teleoperate/default-interface/#viam-mobile-app) or create your own custom mobile app using the [Flutter SDK](https://flutter.viam.dev/viam_protos.provisioning.provisioning/ProvisioningServiceClient-class.html) or the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/src/app/provisioning-client.ts) to connect to `viam-agent` and provision your machines.

The Viam mobile app allows end users to create a new machine in the app, and `agent-provisioning` will then install `viam-server` and run it with a provided configuration.
If you choose to use the Viam mobile app, you must provide a {{< glossary_tooltip term_id="fragment" text="fragment" >}} for provisioning.
If you do not yet have a fragment, follow the steps to [Create a configuration fragment](/manage/fleet/reuse-configuration/) and make a note of the fragment ID.

{{< alert title="Tip" color="tip" >}}
If you are not using Flutter or TypeScript and would like to use provisioning, please [contact us](mailto:support@viam.com).
{{< /alert >}}

If you choose to use the captive web portal, you can optionally create a machine in advance and provide its machine cloud credentials file at <FILE>/etc/viam.json</FILE>.

You can get the machine cloud credentials by clicking the copy icon next to **Machine cloud credentials** in the part status dropdown to the right of your machine's name on the top of the page.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

{{% expand "Want to create a machine and obtain its machine cloud credentials programmatically?" %}}

You can use the [Fleet Management API](/dev/reference/apis/fleet/) to create machines, and obtain their machine cloud credentials:

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import requests

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.app.app_client import APIKeyAuthorization

# Replace "<API-KEY>" (including brackets) with your API key
API_KEY = "<API-KEY>"
# Replace "<API-KEY-ID>" (including brackets) with your API key ID
API_KEY_ID = "<API-KEY-ID>"
# The id of the location to create the machine in
LOCATION_ID = ""
# The name for the machine to create
MACHINE_NAME = ""


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        payload=API_KEY,
      ),
      auth_entity=API_KEY_ID
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "cloud"
    # to run fleet management API methods on
    cloud = viam_client.app_client
    new_machine_id = await cloud.new_robot(
        name=MACHINE_NAME, location_id=LOCATION_ID)
    print("Machine created: " + new_machine_id)
    list_of_parts = await cloud.get_robot_parts(
        robot_id=new_machine_id)
    print("Part id: " + list_of_parts[0].id)

    org_list = await cloud.list_organizations()
    print(org_list[0].id)

    auth = APIKeyAuthorization(
        role="owner",
        resource_type="robot",
        resource_id=new_machine_id
    )
    api_key, api_key_id = await cloud.create_key(
        org_list[0].id, [auth], "test_provisioning_key")
    print(api_key, api_key_id)

    headers = {
        'key_id': api_key_id,
        'key': api_key
    }
    params = {
        "client": 'true',
        "id": list_of_parts[0].id
    }
    res = requests.get(
        'https://app.viam.com/api/json1/config',
        params=params,
        headers=headers,
        timeout=10
    )
    print(res.text)

    with open("viam.json", "w") as text_file:
        text_file.write(res.text)

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /expand%}}

## Configure `agent-provisioning`

{{< table >}}

{{% tablestep link="/manage/fleet/provision/setup/#configure-agent-provisioning" %}}
**1. Configure provisioning**

If you are using the captive portal, this step is optional.
If you are using a mobile app, you must create a provisioning configuration file, specifying at least a `fragment_id`.

Create a file called <FILE>viam-provisioning.json</FILE> with the following format and customize the [attributes](/manage/fleet/provision/setup/#configure-agent-provisioning):

{{< tabs >}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "<NAME>", # your company name
  "model": "<NAME>", # the machine's model
  "fragment_id": "<ID>", # the fragment id, required for mobile app
  "hotspot_prefix": "<PREFIX>", # machine creates a hotspot during setup
  "disable_dns_redirect": true, # disable if using a mobile app
  "hotspot_password": "<PASSWORD>", # password for the hotspot
  "networks" : []
}
```

{{% /tab %}}
{{% tab name="Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "Skywalker",
  "model": "C-3PO",
  "fragment_id": "2567c87d-7aef-41bc-b82c-d363f9874663",
  "hotspot_prefix": "skywalker-setup",
  "disable_dns_redirect": true,
  "hotspot_password": "skywalker123",
  "roaming_mode": false,
  "offline_timeout": "3m30s",
  "user_timeout": "2m30s",
  "fallback_timeout": "15m"
}
```

This file configures some basic metadata, specifies a [fragment](/manage/fleet/reuse-configuration/#modify-fragment-settings-on-a-machine) to use to configure the machine, and provides the WiFi hotspot network name and password to use on startup.
It also configures timeouts to control how long `viam-agent` waits for a valid local WiFi network to come online before creating its hotspot network, and how long to keep the hotspot active before terminating it.

{{% /tab %}}
{{< /tabs >}}

{{% expand "Click to view attribute information" %}}

<!-- prettier-ignore -->
| Name       | Type   | Required? | Description |
| ---------- | ------ | --------- | ----------- |
| `manufacturer` | string | Optional | Purely informative. May be displayed on captive portal or provisioning app. Default: `"viam"`. |
| `model` | string | Optional | Purely informative. May be displayed on captive portal or provisioning app. Default: `"custom"`. |
| `fragment_id` | string | Optional | The `fragment_id` of the fragment to configure machines with. Required when using the Viam mobile app for provisioning. The Viam mobile app uses the fragment to configure the machine. |
| `hotspot_interface` | string | Optional | The interface to use for hotspot/provisioning/wifi management. Default: first discovered 802.11 device. |
| `hotspot_prefix` | string | Optional | `viam-agent` will prepend this to the hostname of the device and use the resulting string for the provisioning hotspot SSID. Default: `"viam-setup"`. |
| `hotspot_password` | string | Optional | The Wifi password for the provisioning hotspot. Default: `"viamsetup"`. |
| `disable_dns_redirect` | boolean | Optional | By default, ALL DNS lookups using the provisioning hotspot will redirect to the device. This causes most phones/mobile devices to automatically redirect the user to the captive portal as a "sign in" screen. When disabled, only domains ending in .setup (ex: viam.setup) will be redirected. This generally avoids displaying the portal to users and is mainly used in conjunction with a mobile provisioning application workflow. Default: `false`. |
| `roaming_mode` | boolean | Optional | By default, the device will only attempt to connect to a single wifi network (the one with the highest priority), provided during initial provisioning/setup using the provisioning mobile app or captive web portal. Wifi connection alone is enough to consider the device as "online" even if the global internet is not reachable. If the primary network configured during provisioning cannot be connected to and roaming mode is enabled, the device will attempt connections to all configured networks in `networks`, and only consider the device online if the internet is reachable. Default: `false`. |
| `offline_timeout` | boolean | Optional | Will only enter provisioning mode (hotspot) after being disconnected longer than this time. Useful on flaky connections, or when part of a system where the device may start quickly, but the wifi/router may take longer to be available. Default: `"2m"` (2 minutes). |
| `user_timeout` | boolean | Optional | Amount of time before considering a user (using the captive web portal or provisioning app) idle, and resuming normal behavior. Used to avoid interrupting provisioning mode (for example for network tests/retries) when a user might be busy entering details. Default: `"5m"` (5 minutes). |
| `fallback_timeout` | boolean | Optional | Provisioning mode will exit after this time, to allow other unmanaged (for example wired) or manually configured connections to be tried. Provisioning mode will restart if the connection/online status doesn't change. Default: `"10m"` (10 minutes). |
| `networks` | array | Optional | Add additional networks the machine can connect to for provisioning. We recommend that you add WiFi settings in the operating system (for example, directly in NetworkManager) rather than in this file, or in the corresponding machine config in the Viam app, if networks aren't needed until after initial provisioning. See [Networks](/manage/reference/viam-agent/#networks). Default: `[]`. |
| `wifi_power_save` | boolean | Optional | If set, will explicitly enable or disable power save for all WiFi connections managed by NetworkManager.  |
| `device_reboot_after_offline_minutes` | integer | Optional | If set, `viam-agent` will reboot the device after it has been offline for the specified duration. Default: `0` (disabled). |

{{% /expand%}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Configure Networks (optional)**

During the provisioning process, a machine connects to a network to install `viam-server`.
If you provide an app to your end user or are asking them to use the Viam mobile app, the user will provide network details through that app.

If you know in advance which other networks a machine should be able to connect to, we recommend that you add WiFi settings in the operating system (for example, directly in NetworkManager).

However, if you want to add additional networks to the provisioning configuration you can add them to the `networks` field value.

{{< alert title="Important" color="note" >}}
You must enable `roaming_mode` in the [`agent-provisioning` configuration](/manage/fleet/provision/setup/#configure-agent-provisioning) of the machine to allow the machine to connect to the specified networks after provisioning.
{{< /alert >}}

If `roaming_mode` is enabled, `agent-provisioning` will try to connect to each specified network in order of `priority` from highest to lowest.

<!-- prettier-ignore -->
| Name       | Type   | Description |
| ---------- | ------ | ----------- |
| `type`     | string | The type of the network. Options: `"wifi"`|
| `ssid`     | string | The network's SSID. |
| `psk`      | string | The network pass key. |
| `priority` | int    | Priority to choose the network with. Values between -999 and 999. Default: `0`. |

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`:

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "Skywalker",
  "model": "C-3PO",
  "fragment_id": "2567c87d-7aef-41bc-b82c-d363f9874663",
  "hotspot_prefix": "skywalker-setup",
  "disable_dns_redirect": true,
  "hotspot_password": "skywalker123",
  "roaming_mode": false,
  "offline_timeout": "3m30s",
  "user_timeout": "2m30s",
  "fallback_timeout": "15m",
  "roaming_mode": true,
  "networks": [
    {
      "type": "wifi",
      "ssid": "otherNetworkOne",
      "psk": "myFirstPassword",
      "priority": 30
    },
    {
      "type": "wifi",
      "ssid": "otherNetworkTwo",
      "psk": "mySecondPassword",
      "priority": 10
    }
  ]
}
```

{{% /tablestep %}}
{{< /table >}}

## Install `viam-agent`

`viam-agent` is a self-updating service manager that maintains the lifecycle for several Viam services and keeps them updated.

The following instructions will preinstall `viam-agent` into an image.

**Only use the following method for offline pre-installs with images. For live systems, follow the instructions on a machine's setup tab to install `viam-server` with `viam-agent`.**

{{< alert title="Support notice" color="note" >}}
Please note this script works only under POSIX (MacOS and Linux) at the moment.
{{< /alert >}}

{{< table >}}
{{% tablestep %}}
**1. Download the preinstall script**

Run the following commands to download the preinstall script and make the script executable:

```sh {class="command-line" data-prompt="$"}
wget https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{% /tablestep %}}
{{% tablestep %}}
**2. Run the preinstall script**

Run the preinstall script without options and it will attempt to auto-detect a mounted root filesystem (or for Raspberry Pi, bootfs) and also automatically determine the architecture.

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh
```

Follow the instructions.
If you created a <FILE>viam-provisioning.json</FILE>, specify its location as an environment variable or when prompted.

You can set optional arguments by defining the following environment variables:

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `VIAM_JSON_PATH` | The path to the machine credentials <FILE>viam.json</FILE> file to be copied to the machine. The script will also prompt you for this file if not provided. |
| `PROVISIONING_PATH` | The path to the <FILE>viam-provisioning.json</FILE> file. The script will also prompt you for this file if not provided. |
| `VIAM_AGENT_PATH` | The path to a beta or local build of `viam-agent`. Used for testing. |

<br>

{{% expand "Using a Raspberry Pi?" %}}

{{< alert title="Important: Required customization" color="note" >}}

You **must customize at least the hostname** when prompted by the Raspberry Pi Imager.

{{< imgproc alt="Raspberry Pi Imager window showing gear-shaped settings icon is selected." src="/installation/rpi-setup/advanced-options-yes.png" resize="800x" declaredimensions=true >}}

When you customize the hostname or other settings, the Raspberry Pi Imager creates `firstrun.sh` which is required to set up provisioning.

If you do not customize anything, `firstrun.sh` is not present on the device and the `preinstall.sh` script fails.

{{< /alert >}}

For Raspberry Pis, the script will automatically perform the required next steps, it will:

- create a tarball
- update `firstrun.sh`.
- extract the tarball to the mounted root filesystem

```sh {class="command-line" data-prompt="$" data-output="2-40"}
sudo ./preinstall.sh


Found Raspberry Pi bootfs mounted at /Volumes/bootfs


A Raspberry Pi boot partition has been found mounted at /Volumes/bootfs
This script will modify firstrun.sh on that partition to install Viam agent.
Continue pre-install? (y/n): y
Path to custom viam-provisioning.json (leave empty to skip):
Creating tarball for install.
a opt
a opt/viam
a opt/viam/cache
a opt/viam/bin
a opt/viam/bin/viam-agent
a opt/viam/bin/agent-provisioning
a opt/viam/cache/viam-agent-provisioning-factory-aarch64
a opt/viam/cache/viam-agent-factory-aarch64
a etc
a usr
a usr/local
a usr/local/lib
a usr/local/lib/systemd
a usr/local/lib/systemd/system
a usr/local/lib/systemd/system/viam-agent.service
a usr/local/lib/systemd/system/multi-user.target.wants
a usr/local/lib/systemd/system/multi-user.target.wants/viam-agent.service


Install complete! You can eject/unmount and boot the image now.
```

{{% /expand%}}

{{% expand "Error: no valid image found at mountpoints (or manually provided path)" %}}

If you get this error, you can run the script for the target system's architecture.
It will create a tarball for the system's architecture which you will then need to manually extract.

{{< tabs >}}
{{% tab name="arm64" %}}

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh --aarch64
```

{{% /tab %}}
{{% tab name="x86_64" %}}

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh --x86_64
```

{{% /tab %}}
{{< /tabs >}}

To extract the tarball, run:

```sh {class="command-line" data-prompt="$"}
sudo tar -xJvpf $TARBALL -C <PATH_TO_ROOT_FS>
```

{{% /expand%}}

{{% expand "Refusing to install to unknown/unset ROOTFS" %}}

If your root file system cannot be detected, you can specify it directly:

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh /path/to/rootfs
```

{{% /expand %}}

{{% /tablestep %}}
{{< /table >}}

## Troubleshooting

### Device not detecting networks

Some systems can't scan for WiFi networks while in hotspot mode, meaning they won't automatically detect networks coming online or into range until the `fallback_timeout` expires.
The `fallback_timeout` causes your device to exit hotspot mode, at which point your device will be able to detect newly available networks.
If your device does not connect to your network, adjust the `fallback_timeout` value in the [`agent-provisioning` configuration](/manage/fleet/provision/setup/#configure-agent-provisioning).

### Test GRPC components of the provisioning service

If you need to test the GRPC components of the provisioning service, there is a CLI client available.
Get the code from the [`agent-provisioning` repo](https://github.com/viamrobotics/agent-provisioning) and run `go run ./cmd/client/` for info.

## End user setup experience

End users receive a machine, and use either a captive web portal or mobile app to complete the machine setup.

The following steps show you the end user experience using the mobile app or the captive web portal and how your configuration influences it.

For a guide you can give to end users for setting up their machine, see [Setup machine](/manage/fleet/provision/end-user-setup/).

{{< tabs >}}
{{% tab name="Mobile app" min-height="703px" %}}

{{<video webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with viam-agent." poster="/platform/provisioning-demo.jpg" class="alignright" max-width="400px" style="margin-left: 2rem">}}

1. Open the app and follow any instructions there until the app directs you to turn on the machine.

   - If you are using the Viam mobile app, create a new machine or click on an existing machine that has not yet been set up and follow the instructions.

1. When you power on the machine that has `viam-agent` installed and `agent-provisioning` configured, `viam-agent` creates a WiFi hotspot.

   - The [`agent-provisioning` configuration](/manage/fleet/provision/setup/#configure-agent-provisioning) is at <file>/etc/viam-provisioning.json</file> on your machine.

1. You then use your mobile device or computer and connect to the WiFi hotspot.

   - By default, the hotspot network is named `viam-setup-HOSTNAME`, where `HOSTNAME` is replaced with the hostname of your machine.
     The WiFi password for this hotspot network is `viamsetup` by default.
     You can customize these values in the [`agent-provisioning` configuration](/manage/reference/viam-agent/#configuration).

1. If you as the end user have a provisioning mobile app, go back to the app to complete setup.
   In the mobile app, you will be prompted to provide the network information for the machine.

   - If your device is not detecting networks, see [Troubleshooting](/manage/fleet/provision/setup/#device-not-detecting-networks).

1. The machine will then disable the hotspot network and attempt to connect using the provided network information.
   If `viam-agent` cannot establish a connection using the provided network information, the machine will create the hotspot again and continue going through steps (2-5) until a connection is successfully established.
1. If the connection is successful, `viam-agent` installs `viam-server`.

   - `agent-provisioning` will use the provided network if it can connect, even if that network does not have internet access.
     Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
     If you want `agent-provisioning` to require that a WiFi network be connected to the internet in order to connect to it, enable roaming mode.

1. `viam-agent` then starts `viam-server` with the provided configuration and the machine becomes **live**.

{{% /tab %}}
{{% tab name="Captive web portal" %}}

1. When you, as the end user, power on the machine that has `viam-agent` installed and `agent-provisioning` configured, `agent-provisioning` creates a WiFi hotspot.

   - The [`agent-provisioning` configuration](/manage/fleet/provision/setup/#configure-agent-provisioning) is at <file>/etc/viam-provisioning.json</file>.
   - If a machine already exists, a machine cloud credentials file, if provided, is at <file>/etc/viam.json</file>.

1. You as the end user then use your mobile device or computer and connect to the WiFi hotspot.

   - By default, the hotspot network is named `viam-setup-HOSTNAME`, where `HOSTNAME` is replaced with the hostname of your machine.
     The WiFi password for this hotspot network is `viamsetup` by default.
     You can customize these values in the [`agent-provisioning` configuration](/manage/reference/viam-agent/#configuration).

1. Once connected to the hotspot, you will be redirected to a sign-in page.
   If you are using a laptop or are not redirected, try opening [http://viam.setup/](http://viam.setup/) in a browser.

1. In the captive web portal, you will then be prompted to provide the network information for the machine.

   - If there is no machine cloud credentials file at <file>/etc/viam.json</file>, the captive portal will also require you to paste a machine cloud credentials file.
     This is the JSON object which contains your machine part secret key and cloud app address, which your machine's `viam-server` instance needs to connect to the Viam app.

     To copy a machine cloud credentials file:

     - Navigate to your machine's page on the [Viam app](https://app.viam.com).
     - Select the part status dropdown to the right of your machine's name on the top of the page.
       {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="machine cloud credentials button on the machine part info dropdown">}}
     - Click the copy icon next to **Machine cloud credentials**.
     - Paste the machine cloud credentials when prompted.

1. The machine will then disable the hotspot network and attempt to connect using the provided network information.
   If `viam-agent` cannot establish a connection using the provided network information, the machine will create the hotspot again and continue going through steps (2-5) until a connection is successfully established.
1. If the connection is successful, `viam-agent` installs `viam-server`.

   - `agent-provisioning` will use the provided network if it can connect, even if that network does not have internet access.
     Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
     If you want `agent-provisioning` to require that a WiFi network be connected to the internet in order to connect to it, enable roaming mode.

1. `viam-agent` then starts `viam-server` with the provided configuration and the machine becomes **live**.

{{% /tab %}}
{{< /tabs >}}
