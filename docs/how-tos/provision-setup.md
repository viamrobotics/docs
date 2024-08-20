---
title: "Configure provisioning with viam-agent"
linkTitle: "Setup for provisioning"
weight: 68
type: "docs"
description: "Install and configure viam-agent for provisioning one or many machines."
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
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

To find out more about supported systems, see [Compatibility](/installation/#compatibility).

If you are flashing a Raspberry Pi using the Raspberry Pi Imager, flash a 64-bit image to your SD card and customize at least the hostname when prompted.

Eject and reinsert the card to make sure it's mounted with the newly written contents.

{{% /expand%}}

## Decide on the provisioning method

You can choose to let your end users complete machine setup by using a captive web portal or a mobile app.

If you choose to have a mobile app experience, you can use the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app) or create your own custom mobile app using the [Flutter SDK](https://flutter.viam.dev/viam_protos.provisioning.provisioning/ProvisioningServiceClient-class.html) or the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/src/app/provisioning-client.ts) to connect to `viam-agent` and provision your machines.

If you choose to use the Viam mobile app, you must provide a {{< glossary_tooltip term_id="fragment" text="fragment" >}} for provisioning.
If you do not yet have a fragment, follow the steps to [Create a configuration fragment](/how-tos/one-to-many/) and make a note of the fragment ID.

If you choose to use the captive web portal, you can optionally create a machine already and provide its credentials configuration file at <FILE>/etc/viam.json</FILE>.

You can get the `viam-server` machine credentials by clicking the copy icon next to **Viam server config** in the part status dropdown to the right of your machine's name on the top of the page.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

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
  "hotspot_password": "<PASSWORD>", # password for the hotspot
}
```

{{% /tablestep %}}
{{< /table >}}

## Install `viam-agent`

`viam-agent` is a self-updating service manager that maintains the lifecycle for several Viam services and keeps them updated.
If you intend to use `viam-agent` to keep your device's Viam software up-to-date or to use its provisioning plugin to let end users set up their own machines, you need to use `viam-agent` and install it on the machine before sending it to the user.

You can [install `viam-agent` on live systems](/installation/) or preinstall it:

{{< tabs >}}
{{% tab name="Preinstall on an SD card (or other image)" %}}

Viam provides a preinstall script that works with images to add `viam-agent`.

{{< alert title="Support notice" color="note" >}}
Please note this script works only under POSIX (MacOS and Linux) at the moment.
{{< /alert >}}

{{< table >}}
{{< tablestep >}}
**1. Download the preinstall script**

Run the following commands to download the preinstall script and make the script executable:

```sh {class="command-line" data-prompt="$"}
wget https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{< /tablestep >}}
{{< tablestep >}}
**2. Run the preinstall script**

Run the preinstall script without options and it will attempt to auto-detect a mounted root filesystem (or for Raspberry Pi, bootfs) and also automatically determine the architecture.

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh
```

Follow the instructions.
If you created a <FILE>viam-provisioning.json</FILE>, specify its location when prompted.

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

If you get an error, run the script for the target system's architecture:

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

If this command fails because the script cannot detect your mountpoint, you can specify it directly:

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh /path/to/rootfs
```

{{< /tablestep >}}
{{< /table >}}

{{% /tab %}}
{{% tab name="Manual install" %}}

{{< table >}}
{{< tablestep >}}
**1. Create and download files**

Run the following commands to create directories for the provisioning binaries, then download the binaries and make them executable:

{{< tabs >}}
{{% tab name="x86_64" %}}

```sh {class="command-line" data-prompt="$"}
mkdir -p /opt/viam/bin/ /opt/viam/tmp/
curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/viam-agent-stable-x86_64 -o /opt/viam/bin/viam-agent-stable-x86_64
curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent-provisioning/viam-agent-provisioning-stable-x86_64 -o /opt/viam/bin/viam-agent-provisioning-stable-x86_64
chmod 755 /opt/viam/tmp/viam-agent*
```

{{% /tab %}}
{{% tab name="aarch64" %}}

```sh {class="command-line" data-prompt="$"}
mkdir -p /opt/viam/bin/ /opt/viam/tmp/
curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/viam-agent-stable-aarch64 -o /opt/viam/bin/viam-agent-stable-aarch64
curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent-provisioning/viam-agent-provisioning-stable-aarch64 -o /opt/viam/bin/viam-agent-provisioning-stable-aarch64
chmod 755 /opt/viam/tmp/viam-agent*
```

{{% /tab %}}
{{< /tabs >}}

{{< /tablestep >}}
{{< tablestep >}}
**2. Symlink the binaries**

Symlink the agent binary to `bin/viam-agent` and the provisioning binary to `bin/agent-provisioning`:

{{< tabs >}}
{{% tab name="x86_64" %}}

```sh {class="command-line" data-prompt="$"}
ln -s /opt/viam/bin/viam-agent-stable-x86_64 bin/viam-agent
ln -s /opt/viam/bin/viam-agent-provisioning-stable-x86_64 bin/agent-provisioning
```

{{% /tab %}}
{{% tab name="aarch64" %}}

```sh {class="command-line" data-prompt="$"}
ln -s /opt/viam/bin/viam-agent-stable-aarch64 bin/viam-agent
ln -s /opt/viam/bin/viam-agent-provisioning-stable-aarch64 bin/agent-provisioning
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
Use relative symlinks, especially if working on a mounted image (that is not a booted system).
{{< /alert >}}

{{< /tablestep >}}
{{< tablestep >}}
**3. Create the systemd service file**

Copy the systemd [service file](https://github.com/viamrobotics/agent/blob/main/subsystems/viamagent/viam-agent.service) from the agent repo to `/etc/systemd/system/viam-agent.service`.

Then, symlink the service file to <FILE>/etc/systemd/system/multi-user.target.wants/viam-agent.service</FILE>

```sh {class="command-line" data-prompt="$"}
curl -fsSL https://github.com/viamrobotics/agent/raw/main/subsystems/viamagent/viam-agent.service -o /etc/systemd/system/viam-agent.service
ln -s /etc/systemd/system/viam-agent.service /etc/systemd/system/multi-user.target.wants/viam-agent.service
```

{{< alert title="Note" color="note" >}}
Use relative symlinks, especially if working on a mounted image (that is not a booted system).
{{< /alert >}}

{{< /tablestep >}}
{{< tablestep >}}
**4. Ensure NetworkManager is installed**

Make sure NetworkManager version 1.42 or newer is installed and enabled in `systemd`.

{{< /tablestep >}}
{{< tablestep >}}

If you create a provisioning file, the file must be at <file>/etc/viam-provisioning.json</file> on the machine that will be provisioned.
If you follow the installation instructions in the next section

{{< /tablestep >}}
{{< /table >}}

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

If you need to test the GRPC components of the provisioning service, there is a CLI client available.
Get the code from the [`agent-provisioning` repo](https://github.com/viamrobotics/agent-provisioning) and run `go run ./cmd/client/` for info.

## Next Steps

With provisioning configured, you can now direct the end user to follow the setup steps:

{{< cards >}}
{{% card link="/how-tos/provision/" %}}
{{< /cards >}}
