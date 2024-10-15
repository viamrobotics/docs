---
title: "Manage Machines"
linkTitle: "Machines"
weight: 10
type: "docs"
description: "A machine is an organizational concept, consisting of either one or multiple parts working closely together to complete tasks."
tags: ["fleet management", "cloud", "app"]
images: ["/fleet/app-usage/create-machine.png"]
aliases:
  - /fleet/robots/
  - /manage/fleet/machines/
  - /fleet/machines/
---

A _machine_ is an organizational concept, consisting of either one <em>{{< glossary_tooltip term_id="part" text="part" >}}</em>, or multiple _parts_ working closely together to complete tasks.
The machine represents the configuration and entry point for one or more computers (and the components they control) coupled into one logical grouping of parts that work together to complete tasks.
A machine usually reflects a physical device, from a camera collecting images, to a wheeled rover, or an articulated arm on a factory floor.
A machine always has a main part that receives client requests, and any number of other parts.

## Add a new machine

Add a new machine in the [Viam app](https://app.viam.com) by clicking **+ Add machine**, providing a name in the **New machine** field and clicking **Add machine** again.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add Machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

Click the name of a machine to go to that machine's page, where you'll find a variety of tools for working with your machine.

## Navigating the machine page

Next to the machine name, there is an indicator of the machine's status.
Click on the **status** dropdown to open a menu with information about each {{< glossary_tooltip term_id="part" text="part" >}} of your machine.
Once you connect to the `viam-server` instance on a part, this display includes its OS, Host, `viam-server` version, IP addresses, and what time it was last online or remote address (if live):

![The machine page with part menu expanded](/fleet/app-usage/machine-page.png)

### Set up a new machine

<!-- TODO R2D2: might need screenshot and needs to be revisited once setup construction is finished -->

To connect to the `viam-server` instance on a part, follow the setup instructions.
Open the part status dropdown menu in the top left corner of the page, next to the machine's name.
Click **View setup instructions** to open the setup instructions.

Select your system's architecture and select the version of the {{< glossary_tooltip term_id="RDK" text="RDK" >}} to use.
Then, follow the instructions on the page to connect and set up your machine.

{{% alert title="Tip" color="tip" %}}
If your machine is controlled by a microcontroller, install the [**viam-micro-server**](/installation/viam-micro-server-setup/#install-viam-micro-server) instead of full `viam-server`.
{{% /alert %}}

More in-depth information on installing `viam-server` can be found in our [Installation Guide](/installation/viam-server-setup/#install-viam-server).

Once all parts of your machine are set up and connected to the app, the part status display at the top left corner of the page turns green.
Now, you can manage your machine with one of four tabs: **CONFIGURE**, **CONTROL**, **LOGS**, and **CONNECT**:

{{<imgproc src="/fleet/app-usage/parts-live.png" resize="400x" declaredimensions=true alt="The machine page with all parts live">}}

### CONFIGURE

The configuration of a machine describes the {{< glossary_tooltip term_id="resource" text="resources" >}} that it has access to.
When a {{< glossary_tooltip term_id="part" text="machine part" >}} that is managed with the Viam app first comes online, it requests its configuration from the [Viam app](https://app.viam.com).
Once the machine has a configuration, it caches it locally and can use the configuration for up to 60 days.
The machine checks for new configurations every 15 seconds and changes its configuration automatically when a new configuration is available.

After connecting your machine, go to the **CONFIGURE** tab, and start adding {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, and other {{< glossary_tooltip term_id="resource" text="resources" >}}.

<!-- TODO R2D2: need to check that this works once page is set up -->

The Viam app keeps a record of your configuration changes, allowing you to revert to earlier configurations if needed.
To see the history of the configuration of a machine part, click on **History** on the right side of its card on the **CONFIGURE** tab.

For more information, see the [configuration documentation](/configure/#the-configure-tab).

{{< alert title="Tip" color="tip" >}}
If you are managing a large fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your fleet](/fleet/fragments/).
{{< /alert >}}

### CONTROL

Once you have configured components and services for your machine, you can visually test and remotely operate them from the **CONTROL** tab in the [Viam app](https://app.viam.com) or the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app).

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="Using the control tab" max-width="800px">}}

You can also switch between different machine parts by selecting the part from the **Machine part** dropdown menu.

{{< imgproc src="/fleet/app-usage/control-machine-part-dropdown.png" alt="The expanded Machine part dropdown menu with the main part selected on the Control tab." resize="650x" class="aligncenter" >}}

For more information, see [Control machines](/fleet/control/).

### LOGS

To make debugging issues with your machines easier, each machine automatically sends its logs to the cloud.
You can access your logs from the **LOGS** tab in the [Viam app](https://app.viam.com) and filter your logs for specific keywords or log levels:

{{<gif webm_src="/fleet/log-filtering.webm" mp4_src="/fleet/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can click on the part names in the left-hand menu to switch logs between parts. You can also change your timestamp format to ISO or Local depending on your preference.

To view logs in the Viam mobile app:

1. Select an organization clicking on the menu icon in the top left corner and tapping an organization.
2. Tap the **Locations** tab and tap on a location and then on a machine.
3. Click the menu button marked "**...**" in the upper right corner.
4. Click **View Logs**.

### CONNECT

#### Code sample

To start programming your machine, go to the **CONNECT** tab and select the **Code sample** page.
This has sample code snippets you can copy and paste into your control code to connect to your machine.

{{% snippet "show-secret.md" %}}

For more information on the SDKs, see [Write control code with Viam's SDKs](/appendix/apis/).

#### Configure as remote part

On the **CONNECT** tab, there is also a page called **Configure as remote part**.
This page has instructions for how to configure a {{< glossary_tooltip term_id="part" text="part" >}} of your machine as a [remote part](/architecture/parts/) of another machine.

#### API keys

Your machine and the Viam app communicate securely using [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection) with unique secrets.
The **API keys** page of the **CONNECT** tab allows you to access, generate, and delete your [API keys](/cloud/rbac/#api-keys), which grant access to organizations, locations, and machines.

![The Security tab of a machine's page noting the Machine part API keys dropdown menu, with the clipboard icon on the far right and the Generate Key button underneath the dropdown.](/fleet/app-usage/machine-secrets.png)

Copy an API key or API key ID by clicking on the clipboard icon.
Click **Show details** and **Access settings** to go to your organization settings page, where you can modify the access your API keys provide.

{{% snippet "secret-share.md" %}}

## Delete a machine

To delete a machine, click on the **...** menu in the top right hand corner of its page, select **Delete machine**, and confirm that you're sure.

{{< imgproc alt="The delete machine button and the confirmation checkbox (Sure?) next to it." src="/fleet/app-usage/delete.png" resize="300x" >}}
