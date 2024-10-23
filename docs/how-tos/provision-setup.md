---
title: "Configure provisioning with viam-agent"
linkTitle: "Setup for provisioning"
weight: 68
type: "docs"
description: "Install and configure viam-agent for provisioning one or many machines."
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Intermediate"
date: "2024-08-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

The provisioning subsystem is a feature of `viam-agent`, which you can install as part of your manufacturing process. `agent-provisioning` will then perform the rest of the first-time setup for your machine once an end user sets up the machine.

This is useful when deploying a fleet of machines directly from the factory to a customer, or when bundling proprietary software on your Viam machine.

This guide will show you how to install and configure `viam-agent`.

{{< alert title="In this page" color="tip" >}}

1. [Decide on the provisioning method](#decide-on-the-provisioning-method)
1. [Configure `agent-provisioning`](#configure-agent-provisioning)
1. [Install `viam-agent`](#install-viam-agent)

{{< /alert >}}

## Prerequisites

{{% expand "One or more physical devices with supported operating system" %}}

To find out more about supported systems, see [`viam-server` Platform requirements](/installation/viam-server-setup/#platform-requirements) and [`viam-micro-server` Platform requirements](/installation/viam-micro-server-setup/#platform-requirements).

If you are flashing a Raspberry Pi using the Raspberry Pi Imager, flash a 64-bit image to your SD card and customize at least the hostname when prompted by the Raspberry Pi Imager.

When you customize the hostname or other settings, the Raspberry Pi Imager creates `firstrun.sh` which is required to set up provisioning.

Eject and reinsert the card to make sure it's mounted with the newly written contents.

{{% /expand%}}

## Decide on the provisioning method

You can choose to let your end users complete machine setup by using a captive web portal or a mobile app.

If you choose to have a mobile app experience, you can use the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app) or create your own custom mobile app using the [Flutter SDK](https://flutter.viam.dev/viam_protos.provisioning.provisioning/ProvisioningServiceClient-class.html) or the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/src/app/provisioning-client.ts) to connect to `viam-agent` and provision your machines.

If you choose to use the Viam mobile app, you must provide a {{< glossary_tooltip term_id="fragment" text="fragment" >}} for provisioning.
If you do not yet have a fragment, follow the steps to [Create a configuration fragment](/how-tos/one-to-many/) and make a note of the fragment ID.

If you choose to use the captive web portal, you can optionally create a machine in advance and provide its machine cloud credentials file at <FILE>/etc/viam.json</FILE>.

You can get the machine cloud credentials by clicking the copy icon next to **Machine cloud credentials** in the part status dropdown to the right of your machine's name on the top of the page.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

{{% expand "Want to create a machine and obtain its machine cloud credentials programmatically?" %}}

You can use the [Fleet Management API](/appendix/apis/fleet/) to create machines, and obtain their machine cloud credentials:

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

{{% tablestep link="/fleet/provision/#configuration" %}}
**Configure provisioning**

If you are using the captive portal, this step is optional.
If you are using a mobile app, you must create a provisioning configuration file, specifying at least a `fragment_id`.

Create a file called <FILE>viam-provisioning.json</FILE> with the following format and customize the [attributes](/fleet/provision/#configuration):

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "<NAME>", # your company name
  "model": "<NAME>", # the machine's model
  "fragment_id": "<ID>", # the fragment id, required for mobile app
  "hotspot_prefix": "<PREFIX>", # machine creates a hotspot during setup
  "disable_dns_redirect": true, # disable if using a mobile app
  "hotspot_password": "<PASSWORD>" # password for the hotspot
}
```

{{% /tablestep %}}
{{< /table >}}

## Install `viam-agent`

`viam-agent` is a self-updating service manager that maintains the lifecycle for several Viam services and keeps them updated.
If you intend to use `viam-agent` to keep your device's Viam software up-to-date or to use its provisioning plugin to let end users set up their own machines, you need to use `viam-agent` and install it on the machine before sending it to the user.

The following instructions will preinstall `viam-agent` into an image.

**Only use the following method for offline pre-installs with images. For live systems, follow the instructions on a machine's setup tab to [install `viam-server` with `viam-agent`](/installation/viam-server-setup/).**

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
If you created a <FILE>viam-provisioning.json</FILE>, specify its location when prompted.

{{% expand "Using a Raspberry Pi?" %}}

{{< alert title="Important" color="note" >}}

You must have flashed a 64-bit image to your SD card and customized at least the hostname when prompted by the Raspberry Pi Imager.

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

If you need to test the GRPC components of the provisioning service, there is a CLI client available.
Get the code from the [`agent-provisioning` repo](https://github.com/viamrobotics/agent-provisioning) and run `go run ./cmd/client/` for info.

## Next Steps

With provisioning configured, you can now direct the end user to follow the setup steps:

{{< cards >}}
{{% card link="/how-tos/provision/" %}}
{{< /cards >}}
