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
aliases:
  - "/build/provision/"
  - /how-tos/provision-setup/
  - /fleet/provision/
  - /how-tos/provision/
# updated: ""  # When the tutorial was last entirely checked
# SMEs: James, Ale
cost: "0"
---

You can install [`viam-agent`](/manage/reference/viam-agent/) as part of your manufacturing process and provision machines with a pre-defined configuration as they come online.
When the end user sets the machine up, they provide network access and `viam-agent` installs `viam-server` and your latest software.

If you're looking for a full tutorial, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).

## Provisioning flow

To prepare a device, you will follow these steps:

1. You create a machine configuration template: a _{{< glossary_tooltip term_id="fragment" text="fragment" >}}_ on Viam.
1. You create a defaults file specifying the provisioning method and the fragment.
1. You flash the SD card for the single-board computer with an operating system.
1. You install `viam-agent` with the `preinstall` script on the SD card providing the defaults file.

Once a customer receives your machine, they will plug the machine in and turn it on.

The next steps depend on the provisioning method:

{{< tabs >}}
{{% tab name="Bluetooth + WiFi provisioning (recommended)" %}}

1. `viam-agent` starts Bluetooth Low Energy (BLE) and accepts connections.
1. The customer installs an app you provide on a mobile device.
1. The customer uses the app to connect to the machine over Bluetooth.
1. Using the app, the customer provides the machine WiFi credentials to the machine to connect to a WiFi network.
1. The machine connects to the internet and sets itself up based on the specified fragment.

{{% /tab %}}
{{% tab name="WiFi hotspot provisioning" %}}

1. `viam-agent` starts a WiFi hotspot.
1. The customer uses a mobile device to connect to the machine's temporary WiFi network.
1. Using a {{< glossary_tooltip term_id="captive-web-portal" text="captive web portal" >}} or a mobile app, the customer provides WiFi credentials to connect to a WiFi network.
1. The machine connects to the internet and sets itself up based on the specified fragment.

{{% /tab %}}
{{% tab name="Bluetooth provisioning" %}}

1. `viam-agent` starts Bluetooth Low Energy (BLE) and accepts connections.
1. The customer installs an app you provide on a mobile device.
1. The customer uses the app to connect to the machine over Bluetooth and shares the mobile device's internet connection with the machine for setup.
1. The machine uses the mobile-devices internet to set itself up based on the specified fragment.

{{% /tab %}}
{{< /tabs >}}

## Provision a device

The following instructions will preinstall `viam-agent` into an image.

**Only use the following method for offline pre-installs with images. For live systems, follow the instructions on a machine's setup tab to install `viam-server` with `viam-agent`.**

{{< table >}}
{{% tablestep start=1 %}}
**Create a fragment**

If you do not yet have a {{< glossary_tooltip term_id="fragment" text="fragment" >}}, follow the steps to [Create a fragment](/manage/fleet/reuse-configuration/#create-a-fragment) and make a note of the fragment ID.

{{% /tablestep %}}
{{% tablestep %}}
**Create the defaults file**

If you would like to use a {{< glossary_tooltip term_id="captive-web-portal" text="captive web portal" >}}, skip this and the next step.

Create a defaults file called <FILE>viam-defaults.json</FILE> to configure the provisioning experience for the users setting up their machines.
You will later pass this file to a script, so you can save it anywhere.
The script will save the file is at <file>/etc/viam-defaults.json</file> on the machine.

You must at least specify a `fragment_id`.

{{< tabs >}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "manufacturer": "<NAME>", # your company name
    "model": "<NAME>", # the machine's model
    "fragment_id": "<ID>", # the fragment id, required for mobile app
    "hotspot_interface": "<INTERFACE>", # the interface to use for hotspot/provisioning/wifi management
    "hotspot_prefix": "<PREFIX>", # machine creates a hotspot with prefix-hostname during setup
    "disable_captive_portal_redirect": false, # set to true if using a mobile app
    "hotspot_password": "<PASSWORD>", # password for the hotspot
    "disable_bt_provisioning": false, # set to true to disable Bluetooth provisioning
    "disable_wifi_provisioning": false, # set to true to disable WiFi hotspot provisioning
    "bluetooth_trust_all": false, # set to true to accept all Bluetooth pairing requests (which is only needed for Bluetooth tethering) without requiring an unlock command from a mobile app.
    "turn_on_hotspot_if_wifi_has_no_internet": false, # set to true if networks without internet should not be accepted.
    "offline_before_starting_hotspot_minutes": "3m30s",
    "user_idle_minutes": "2m30s",
    "retry_connection_timeout_minutes": "15m"
  }
}
```

{{% /tab %}}
{{% tab name="Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "manufacturer": "Skywalker",
    "model": "C-3PO",
    "fragment_id": "2567c87d-7aef-41bc-b82c-d363f9874663",
    "hotspot_interface": "wlan0",
    "hotspot_prefix": "skywalker-setup",
    "disable_captive_portal_redirect": false,
    "hotspot_password": "skywalker123",
    "disable_bt_provisioning": false,
    "disable_wifi_provisioning": false,
    "bluetooth_trust_all": false,
    "turn_on_hotspot_if_wifi_has_no_internet": false,
    "offline_before_starting_hotspot_minutes": "3m30s",
    "user_idle_minutes": "2m30s",
    "retry_connection_timeout_minutes": "15m"
  }
}
```

This file configures some basic metadata, specifies a fragment to use to configure the machine, and provides the WiFi hotspot network name and password to use on startup.
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
| `hotspot_interface` | string | Optional | The interface to use for hotspot/provisioning/wifi management. Example: `"wlan0"`. Default: first discovered 802.11 device. |
| `hotspot_prefix` | string | Optional | `viam-agent` will prepend this to the hostname of the device and use the resulting string for the provisioning hotspot SSID or the Bluetooth device name(`<hotspot_prefix>-<hostname>`).  Default: `"viam-setup"`. |
| `hotspot_password` | string | Optional | The Wifi password for the provisioning hotspot. Be aware that if you do not set a custom password this may be a security risk. Default: `"viamsetup"`. |
| `disable_captive_portal_redirect` | boolean | Optional | By default, all DNS lookups are redirected to the "sign in" portal, which can cause mobile devices to automatically display the portal. When set to true, only DNS requests for domains ending in .setup, like `viam.setup` are redirected, preventing the portal from appearing unexpectedly, especially convenient when using a mobile app for provisioning. Default: `false`. |
| `disable_bt_provisioning` | boolean | Optional | When set to true, disables Bluetooth provisioning. The machine will not advertise Bluetooth services for provisioning. Default: `false`. |
| `disable_wifi_provisioning` | boolean | Optional | When set to true, disables WiFi hotspot provisioning. The machine will not create a WiFi hotspot for provisioning. Default: `false`. |
| `turn_on_hotspot_if_wifi_has_no_internet` | boolean | Optional | By default, the device connects to a single prioritized WiFi network (provided during provisioning) and is considered online even if the global internet is not reachable. When `turn_on_hotspot_if_wifi_has_no_internet` is true and the primary network lacks internet connectivity, the device will try all configured networks and only mark itself as online if it successfully connects to the internet. Default: `false`. |
| `offline_before_starting_hotspot_minutes` | integer | Optional | Will only enter provisioning mode (hotspot) after being disconnected longer than this time. It may be useful to increase this on flaky connections, or when part of a system where the device may start quickly, but the wifi/router may take longer to be available. Default: `2` (2 minutes). |
| `user_idle_minutes` | integer | Optional | Amount of time before considering a user (using the captive web portal or provisioning app) idle, and resuming normal behavior. Used to avoid interrupting provisioning mode (for example for network tests/retries) when a user might be busy entering details. Default: `5` (5 minutes). |
| `retry_connection_timeout_minutes` | integer | Optional | Provisioning mode will exit after this time, to allow other unmanaged (for example wired) or manually configured connections to be tried. Provisioning mode will restart if the connection/online status doesn't change. Default: `10` (10 minutes). |
| `wifi_power_save` | boolean | Optional | Boolean, which, if set, will explicitly enable or disable power save for all WiFi connections managed by NetworkManager. If not set, the system default applies. Default: `NULL`.  |
| `device_reboot_after_offline_minutes` | integer | Optional | If set, `viam-agent` will reboot the device after it has been offline (and in hotspot mode) for the specified duration. Default: `0` (disabled). |

{{% /expand%}}
{{% /tablestep %}}
{{% tablestep %}}
**Configure Networks**

If a machine connects to a network during setup and you know in advance which WiFi a machine will connect to, this step allows you to add credentials for it.

If you do not know the network in advance, skip this step.
In this case the end user will have to provide network details later in the process.

If you know in advance that the machine should be able to connect to multiple networks, we recommend that you add WiFi settings in the operating system (for example, directly in NetworkManager).
If that is not possible, you can add networks with the `additional_networks` field.
`viam-agent` will then try to connect to each specified network in order of `priority` from highest to lowest.

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`:

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "manufacturer": "Skywalker",
    "model": "C-3PO",
    "fragment_id": "2567c87d-7aef-41bc-b82c-d363f9874663",
    "hotspot_interface": "wlan0",
    "hotspot_prefix": "skywalker-setup",
    "disable_captive_portal_redirect": false,
    "hotspot_password": "skywalker123",
    "disable_bt_provisioning": false,
    "disable_wifi_provisioning": false,
    "turn_on_hotspot_if_wifi_has_no_internet": false,
    "offline_before_starting_hotspot_minutes": "3m30s",
    "user_idle_minutes": "2m30s",
    "retry_connection_timeout_minutes": "15m",
    "turn_on_hotspot_if_wifi_has_no_internet": true
  },
  "additional_networks": {
    "testNet1": {
      "priority": 30,
      "psk": "myFirstPassword",
      "ssid": "fallbackNetOne",
      "type": "wifi"
    },
    "testNet2": {
      "priority": 10,
      "psk": "mySecondPassword",
      "ssid": "fallbackNetTwo",
      "type": "wifi"
    }
  }
}
```

<!-- prettier-ignore -->
| Name       | Type   | Description |
| ---------- | ------ | ----------- |
| `type`     | string | The type of the network. Options: `"wifi"`|
| `ssid`     | string | The network's SSID. |
| `psk`      | string | The network password/pre-shared key. |
| `priority` | int    | Priority to choose the network with. Values between -999 and 999. Default: `0`. |

{{% /tablestep %}}
{{% tablestep %}}
**Create a machine in advance**

If you are using a mobile app for provisioning, skip this step.

If you provision devices using a captive web portal, you can create a machine in advance.
You can either provide its machine cloud credentials to the preinstall script you will run in the next steps, or provide them using the captive web portal.

You can get the machine cloud credentials by clicking the copy icon next to **Machine cloud credentials** in the part status dropdown to the right of your machine's name on the top of the page.
Paste the machine cloud credentials into a file on your hard drive called <FILE>viam.json</FILE>.
You will pass the file to the preinstall script later, so you can store it anywhere.
The script will save the file is at <file>/etc/viam.json</file> on the machine.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Machine part info dropdown" class="shadow" >}}

{{< expand "Want to create a machine and obtain its machine cloud credentials programmatically?" >}}

You can use the [Fleet Management API](/dev/reference/apis/fleet/) to create machines, and obtain their machine cloud credentials:

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import requests

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.app.app_client import APIKeyAuthorization

# TODO: Replace "<API-KEY>" (including brackets) with your API key
API_KEY = "<API-KEY>"
# TODO: Replace "<API-KEY-ID>" (including brackets) with your API key ID
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
    viam_client = await connect()
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

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep %}}
**Flash an operating system to the SD card of the single-board computer**

{{< tabs >}}
{{% tab name="Raspberry Pi" %}}

If you are flashing a Raspberry Pi using the Raspberry Pi Imager, flash a 64-bit image to your SD card and **customize at least the hostname** when prompted by the Raspberry Pi Imager.

When you customize the hostname or other settings, the Raspberry Pi Imager creates `firstrun.sh` which is required to set up provisioning.

{{% /tab %}}
{{% tab name="Other" %}}

See [`viam-server` Platform requirements](/operate/get-started/setup/#prerequisite-make-sure-you-have-a-supported-operating-system) and [`viam-micro-server` hardware requirements](/operate/get-started/setup-micro/#supported-microcontrollers).

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Support Notice" color="note" >}}

Provisioning is supported and tested on Ubuntu 22.04, Debian 11 (Bullseye), and 12 (Bookworm) but should work on most distros using NetworkManager v1.30 (or newer) as well.
For Bullseye, the installation of `viam-agent` changes the network configuration to use NetworkManager.

{{< /alert >}}

{{% /tablestep %}}
{{% tablestep %}}
**Mount the SD card**

Still using the computer used for flashing the SD card, eject and reinsert the card to make sure it's mounted with the newly written operating system.

{{% /tablestep %}}
{{% tablestep %}}
**Download the preinstall script**

Run the following commands to download the preinstall script and make the script executable:

{{< tabs >}}
{{% tab name="wget" %}}

```sh {class="command-line" data-prompt="$"}
wget https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{% /tab %}}
{{% tab name="curl" %}}

```sh {class="command-line" data-prompt="$"}
curl -O https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Support notice" color="note" >}}
Please note this script works only under POSIX (macOS and Linux) at the moment.
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep %}}
**Run the preinstall script**

Run the preinstall script.
It will attempt to auto-detect a mounted root filesystem (or for Raspberry Pi, bootfs) and also automatically determine the architecture.

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh
```

Follow the instructions.
If you created a <FILE>viam-defaults.json</FILE> file or a <FILE>viam.json</FILE> file, specify their locations when prompted.

{{% expand "Optional environment variables for the preinstall script" %}}

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `VIAM_JSON_PATH` | The path to the machine cloud credentials file (<FILE>viam.json</FILE>) to be copied to the machine. The script will also prompt you for this file if not provided. |
| `DEFAULTS_PATH` | The path to the <FILE>viam-defaults.json</FILE> file. The script will also prompt you for this file if not provided. |
| `VIAM_AGENT_PATH` | The path to a beta or local build of `viam-agent`. Used for testing. |

{{% /expand%}}

<br>
Troubleshooting:

{{% expand "Using a Raspberry Pi?" %}}

{{< alert title="Important: Required customization" color="note" >}}

You **must customize at least the hostname** when prompted by the Raspberry Pi Imager.

{{< imgproc alt="Raspberry Pi Imager window showing gear-shaped settings icon is selected." src="/installation/rpi-setup/advanced-options-yes.png" resize="800x" declaredimensions=true class="shadow" >}}

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
Path to custom viam-agent binary (leave empty to download default):
Path to custom viam-defaults.json (leave empty to skip):
Path to custom viam.json (leave empty to skip)
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
{{% tablestep %}}
**Set up more devices**

Unless you provided a machine cloud credentials file (<FILE>viam.json</FILE>) to the machine, you can clone SD cards to speed up the provisioning process.

{{% /tablestep %}}
{{< /table >}}

## Use a mobile app for provisioning

You can create your own custom mobile provisioning app using the [Flutter SDK](https://flutter.viam.dev/viam_protos.provisioning.provisioning/ProvisioningServiceClient-class.html) or the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/src/app/provisioning-client.ts).
Alternatively you can use the [Viam mobile app](/manage/troubleshoot/teleoperate/default-interface/#viam-mobile-app).

### Custom Flutter apps

If you are building your own app to provide provisioning functionality you have three options for provisioning.
You can support any number of these options.

<!-- prettier-ignore -->
| Provisioning method | Description | Package |
| ------------------- | ----------- | ------- |
| **Bluetooth with WiFi** | Ask the user to connect to the machine over Bluetooth. The user then provides network credentials for an internet-connected WiFi network, through which machine setup can then occur. Recommended, if available. | [Example](https://github.com/viamrobotics/viam_flutter_provisioning/) |
| **WiFi** | Ask the user to connect to the machine's temporary WiFi hotspot. The user then provides network credentials for an internet-connected WiFi network, through which machine setup can then occur. Slower than Bluetooth with WiFi but faster than Bluetooth tethering. | [Example](https://github.com/viamrobotics/viam_flutter_hotspot_provisioning_widget) |
 | **Bluetooth tethering** | Ask the user to connect to the machine over Bluetooth. The user shares their mobile device's internet with the machine over Bluetooth. Slowest provisioning method. | [Example](https://github.com/viamrobotics/viam_flutter_bluetooth_provisioning_widget/) |

### The Viam mobile app

The Viam mobile app allows end users to create a new machine in the app, and `viam-agent` will then install `viam-server` and run it with the configuration provided by the `fragment_id` in the defaults file.
If you choose to use the Viam mobile app, you must provide a {{< glossary_tooltip term_id="fragment" text="fragment" >}} for provisioning.

{{< alert title="Tip" color="tip" >}}
If you are not using Flutter or TypeScript and would like to use provisioning, please [contact us](mailto:support@viam.com).
{{< /alert >}}

{{<video webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with viam-agent." poster="/platform/provisioning-demo.jpg" class="" max-width="400px" style="margin-left: 2rem">}}

## Change WiFi network or credentials

If you want to change the WiFi network or the network credentials on a device that is already setup, you can enter provisioning again using the force provisioning mode.

If you can manually `SSH` into a machine you can follow these steps:

1. Add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json).
   The `ViamShellDanger` fragment contains the latest version of the shell service, which you must add to your machine before you can use the `viam machines part shell` command.

1. Open a shell on your machine:

   ```sh {class="command-line" data-prompt="$" data-output="2-10"}
   viam machines part shell --part <PART-ID>
   ```

1. On the machine, create an empty file at <FILE>/opt/viam/etc/force_provisioning_mode</FILE>:

   ```sh {class="command-line" data-prompt="$" data-output="3-10"}
   touch /opt/viam/etc/force_provisioning_mode
   ```

1. The machine will immediately enter provisioning mode until the machine receives the new credentials or the `retry_connection_timeout_minutes` limit, by default 10 minutes, expires.

If you provide a provisioning app, instead program functionality that adds an empty file at <FILE>/opt/viam/etc/force_provisioning_mode</FILE>.

## Troubleshooting

### Can I re-provision a machine that was already provisioned?

You cannot re-run the `preinstall.sh` script.
Once a device is set up for provisioning and has a <FILE>viam-provisioning.json</FILE> file on it, it will attempt to provision the machine when it comes online.
If you have not yet connected the device to a network and setup has not completed, you can still make changes to the <FILE>viam-provisioning.json</FILE> file on the device.

Once a machine has completed the provisioning flow, you cannot re-run the final setup steps without first manually removing the machine cloud credentials file (<FILE>/etc/viam.json</FILE>).

### Device not detecting networks

Some systems can't scan for WiFi networks while in hotspot mode, meaning they won't automatically detect networks coming online or into range until the `retry_connection_timeout_minutes` expires.
The `retry_connection_timeout_minutes` causes your device to exit hotspot mode, at which point your device will be able to detect newly available networks.
If your device does not connect to your network, adjust the `retry_connection_timeout_minutes` value in the defaults file.

### Device not connecting or showing as offline

Check if other devices on the network can connect to the internet without problems.
If other devices are fine, try restarting your device and [check for other logs](/manage/troubleshoot/troubleshoot/#check-logs).

### Test GRPC components of the provisioning service

If you need to test the GRPC components of the provisioning service, there is a CLI client available.
Get the code from the [`agent` repo](https://github.com/viamrobotics/agent/tree/main/cmd/provisioning-client) and run `go run ./cmd/provisioning-client/` for info.
