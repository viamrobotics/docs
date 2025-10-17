---
linkTitle: "Set up a computer or SBC"
title: "Set up a computer or SBC"
weight: 20
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Install the software that drives hardware and connects your device to the cloud."
aliases:
  - /installation/viam-server-setup/
  - /how-tos/configure/
  - /installation/prepare/
  - /installation/macos-install/
  - /installation/linux-install/
  - /installation/install/
  - /installation/install/linux-install/
  - /installation/install/macos-install
  - /getting-started/installation/
  - /getting-started/macos-install/
  - /getting-started/linux-install/
  - /installation/
  - /get-started/installation/
  - /operate/get-started/setup/
date: "2025-10-16"
---

Get started by installing [`viam-server`](/operate/reference/viam-server/), the open-source software that drives your hardware and connects your device to the cloud.

## Prerequisites

If you're using Viam with a single-board computer (SBC) that does not yet have a 64-bit Linux operating system installed, start by flashing an OS.
For convenience, we provide operating system installation instructions for some popular SBCs:

{{< expand "SBC setup instructions" >}}
If your SBC or other computer already has a supported operating system installed, you can skip this step.

{{< cards >}}
{{% card link="/operate/reference/prepare/rpi-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/odroid-c4-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/orange-pi-3-lts/" class="small" %}}
{{% card link="/operate/reference/prepare/orange-pi-zero2/" class="small" %}}
{{% card link="/operate/reference/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/pumpkin/" class="small" %}}
{{% card link="/operate/reference/prepare/sk-tda4vm/" class="small" %}}
{{< /cards >}}
{{< /expand >}}

Check if your system can run `viam-server` by running the following command in your terminal:

{{< tabs >}}
{{% tab name="Linux" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
arch=$(uname -m); bits=$(getconf LONG_BIT); [[ ("$arch" == "x86_64" || "$arch" == "aarch64") && "$bits" == "64" ]] && echo "✅ Your system can run viam-server" || echo "❌ Your system cannot run viam-server"
```

`viam-server` can run on Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures.

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
bash -c '[[ "$(uname -s)" == "Darwin" && ("$(uname -m)" == "x86_64" || "$(uname -m)" == "arm64") ]] && echo "✅ Your system can run viam-server" || echo "❌ Your system cannot run viam-server"'
```

{{% alert title="Note for Intel Mac users" color="note" %}}
`viam-server` can run on Macs with Intel processors, but not all {{< glossary_tooltip term_id="module" text="modules" >}} support Intel Macs.
{{% /alert %}}

{{% /tab %}}
{{% tab name="Windows" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
(Get-WmiObject -Class Win32_OperatingSystem).OSArchitecture -eq "64-bit" -and (wsl --status 2>$null) -ne $null ? "✅ Your system can run viam-server" : "❌ Your system needs WSL for viam-server"
```

{{% alert title="Windows note" color="note" %}}
`viam-server` can run on Windows Subsystem for Linux (WSL), but WSL itself does not currently support exposing many types of Windows hardware to the embedded Linux kernel.
This means that some hardware, such as a connected webcam, may not be available to `viam-server` with WSL, even though it is fully supported for native Linux systems.

- Native: Use native if you are using a WSL version prior to WSL 2 or need native USB support
- WSL: Use WSL if you are using Python modules or other Linux dependencies

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

For 32-bit microcontrollers, see [Set up an ESP32](/operate/install/setup-micro/).

## Install `viam-server`

Install `viam-server` on the computer or single-board computer (SBC) that is directly connected to your hardware (for example sensors, cameras, or motors).

1. Make sure your computer or SBC is powered on and connected to the internet.

1. Create a Viam account on [app.viam.com](https://app.viam.com).
   You can configure and manage devices and data collection in the web UI.

1. Create a new [_{{< glossary_tooltip term_id="machine" text="machine" >}}_](/operate/hello-world/quickstart/#machines) using the **Add machine** button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. On your machine's page, click **View setup instructions** and follow the steps for your operating system.
   The app provides commands to install `viam-server` and connect it to the cloud with your machine's unique credentials.

1. After you install `viam-server`, a secure connection is automatically established between your machine and Viam.
   When you update your machine's configuration, `viam-server` automatically gets the updates.

   You are ready to [configure supported hardware](/operate/modules/configure-modules/) on your machine.

## Try an example

{{< readfile "/static/include/install/try-example.md" >}}

{{% hiddencontent %}}

## Installation methods: `viam-agent` versus manual

`viam-agent` is a service manager that automatically updates `viam-server` and includes tools for [provisioning your devices](/manage/fleet/provision/setup/), networking, and configuring operating system settings.

When you set up a Linux device with Viam, you can use `viam-agent`, or to manually install only `viam-server`.
Using `viam-agent` is generally recommended when installing `viam-server`.

When you set up a native Windows device with Viam, you must use the [Viam Agent installer](https://storage.googleapis.com/packages.viam.com/apps/viam-agent/viam-agent-stable.msi).

`viam-agent` is not available for macOS, Windows Subsystem for Linux (WSL), or microcontrollers.
Use manual install for those systems.
{{% /hiddencontent %}}

{{% hiddencontent %}}

## Running `viam-agent` or `viam-server` in a docker container

We do not recommend running `viam-server` or `viam-agent` in Docker.
If you need to use Docker reach out to [support](mailto:support@viam.com).

{{% /hiddencontent %}}

### How the machine gets its configuration

The machine setup steps copy your machine's credentials to your machine.
When you turn on your machine, `viam-server` starts up and uses the provided credentials to fetch its configuration from Viam.
Once the machine has a configuration, it caches it locally (in a file at <FILE>~/.viam/cached_cloud_config\_\<PART-ID\>.json</FILE>) and can use the config for up to 60 days.
Since the configuration is cached locally, your machine does not need to stay connected to Viam after it has obtained its configuration file.

If it is online, the machine checks for new configurations every 15 seconds and changes its config automatically when a new config is available.
All communication happens securely over HTTPS using secret tokens that are in the machine's config.

## Manage your installation

On Linux installs, by default `viam-server` or `viam-agent` and `viam-server` will start automatically when your system boots.
On macOS installs, `viam-server` does not start automatically on boot.
You can change this behavior if desired.

To learn how to run, update, or uninstall `viam-agent`, see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/).

For manual installs of only `viam-server`, see [Manage `viam-server`](/operate/reference/viam-server/manage-viam-server/).
