---
title: "Manage Machines"
linkTitle: "Machines"
weight: 10
type: "docs"
description: "A machine is an organizational concept, consisting of either one or multiple parts working closely together to complete tasks."
tags: ["fleet management", "cloud", "app"]
images: ["/manage/control.gif"]
aliases:
  - /fleet/robots/
  - /manage/fleet/machines/
---

A _machine_ is an organizational concept, consisting of either one <em>{{< glossary_tooltip term_id="part" text="part" >}}</em>, or multiple _parts_ working closely together to complete tasks.
The machine represents the configuration and entry point for one or more computers (and the components they control) coupled into one logical grouping of parts that work together to complete tasks.
A machine usually reflects a physical device, from a camera collecting images, to a wheeled rover, or an articulated arm on a factory floor.
A machine always has a main part that receives client requests, and any number of other parts.

## Add a new machine

Add a new machine by providing a name in the **New machine** field and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add Machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

Click the name of a machine to go to that machine's page, where you'll find a variety of tools for working with your machine.

## Navigating the machine page

The banner at the top of the machine page displays the machine's location, name, and a dropdown list of all {{< glossary_tooltip term_id="part" text="parts" >}} of that machine.

If you've connected your physical machine running `viam-server` to its instance in the Viam app, the banner also displays when the machine was last online, which version of `viam-server` it is running, the host name, the IP address or addresses, and its operating system.

![The machine page with menu tabs](/fleet/app-usage/machine-page.png)

For each machine in your fleet, you start by setting up the machine on the **Setup** tab:

### Setup

The **Setup** tab contains information for starting an instance of `viam-server` on your machine's computer.

Once you select the correct **Architecture** for your system in the upper left of the tab, follow the instructions on the page to connect and set up your machine.

{{% alert title="Tip" color="tip" %}}
More in-depth information on installing `viam-server` can be found in our [Install Guide](/get-started/installation/#install-viam-server).
{{% /alert %}}

### Configuration

When a machine or a {{< glossary_tooltip term_id="part" text="machine part" >}} that is managed with the Viam app first comes online, it requests its configuration from the [Viam app](https://app.viam.com).
Once the machine has a configuration, it caches it locally and can use the configuration for up to 60 days.
The machine checks for new configurations every 15 seconds and changes its configuration automatically when a new configuration is available.

After connecting your machine, go to the **Config** tab, and start adding {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, and other {{< glossary_tooltip term_id="resource" text="resources" >}}.

For more information, see the [configuration documentation](/build/configure/#the-config-tab).

{{< alert title="Tip" color="tip" >}}
If you are managing a large fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your machine](/build/configure/).
{{< /alert >}}

### History

The configuration of your machine and the code it runs are kept separate to make debugging easier.
The **History** tab shows timestamped changes to your machine's configuration.

If you want to revert changes that you made, you can load a previous configuration by clicking the **Load config** button next to the respective configuration.

{{<gif webm_src="/manage/load-prev-config.webm" mp4_src="/manage/load-prev-config.mp4" alt="Load a previous config from the UI" max-width="800px">}}

You can also change your timestamp format to ISO or Local depending on your preference.

### Logs

To make debugging issues with your machines easier, each machine automatically sends its logs to the cloud.
You can access your logs from the **Logs** tab in the [Viam app](https://app.viam.com) and filter your logs for specific keywords or log levels:

{{<gif webm_src="/manage/log-filtering.webm" mp4_src="/manage/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can also change your timestamp format to ISO or Local depending on your preference.

### Control

Once you have configured components and services for your machine, you can visually test and remotely operate them from the **Control** tab in the [Viam app](https://app.viam.com).
For example, if you have configured a base with wheels, you can control your machine's movement with an arrow pad and fields to change base’s speed.
If you have configured a camera component, a window in the **Control** tab displays the camera output.

If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the machine uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).
For local communication between [parts](/build/configure/parts-and-remotes/#machine-parts) Viam uses gRPC or WebRTC.

{{<gif webm_src="/manage/control.webm" mp4_src="/manage/control.mp4" alt="Using the control tab" max-width="800px">}}

<br>

You can also access the control interface using the [Viam mobile app](/fleet/#the-viam-mobile-app), which you can find on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).
The Viam mobile app gives you the ability to search through the machines in your fleet, ordered by location, and control the specific machine or machine component that you need.
You can watch the live camera feed, adjust the component or machine's runtime parameters, and switch between controllable components just as you would in the Viam app. 

{{<gif webm_src="/manage/mobile-app-control.webm" mp4_src="/manage/mobile-app-control.mp4" alt="Using the control interface under the locations tab on the Viam mobile app" max-width="300px">}}

### Code Sample

To start programming your machine, go to the **Code sample** tab which contains boilerplate code snippets you can copy and paste into your SDK code to connect to your machine.

{{% snippet "show-secret.md" %}}

For more information on the SDKs, see [Program your Machine with Viam's SDKs](/build/program/apis/).

There is also a JSON stub you can copy if you wish to have your machine communicate with another machine as a [remote](/build/configure/parts-and-remotes/).

### Security

Your machine and the Viam app communicate securely using [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection) with unique secrets.

The **Security** tab allows you to access, generate, and delete the **Machine part secret keys** and the **Machine part API keys** of your machine.

![The Security tab of a machine's page noting the Machine part API keys dropdown menu, with the clipboard icon on the far right and the Generate Key button underneath the dropdown.](/fleet/app-usage/machine-secrets.png)

You can copy a secret by clicking on the clipboard icon.

{{% snippet "secret-share.md" %}}

## Delete a machine

You can delete a machine by navigating to its page in [the Viam app](https://app.viam.com) and selecting **Sure?** and **Delete machine** in the lower left corner of the page.

{{< imgproc alt="The delete machine button and the confirmation checkbox (Sure?) next to it." src="/fleet/app-usage/delete.png" resize="300x" >}}
