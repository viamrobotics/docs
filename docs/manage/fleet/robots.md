---
title: "Manage Robots"
linkTitle: "Robots"
weight: 10
type: "docs"
description: "A robot is an organizational concept, consisting of either one or multiple parts working closely together to complete tasks."
tags: ["fleet management", "cloud", "app"]
---

A robot is an organizational concept, consisting of either one <em>{{< glossary_tooltip term_id="part" text="part" >}}</em>, or multiple _parts_ working closely together to complete tasks.
The robot represents the configuration and entry point for one or more computers (and the components they control) coupled into one logical grouping of parts that work together to complete tasks.
A robot usually reflects a physical device, from a camera collecting images, to a wheeled rover, or an articulated arm on a factory floor.
A robot always has a main part that receives client requests, and any number of other parts.

## Add a new robot

Add a new robot by providing a name in the **New Robot** field and clicking **Add robot**.

![The 'First Location' page on the Viam app with a new robot name in the New Robot field and the Add robot button next to the field highlighted.](../../img/app-usage/create-robot.png)

Click the name of a robot to go to that robot's page, where you'll find a variety of tools for working with your robot.

## Navigating the robot page

The banner at the top of the robot page displays the robot's location, name, and a drop down list of all parts of that robot.
The first part you create is the _main part_ but you can create additional parts in the drop down.

![The robot page for an example robot with the parts drop down open.](../../img/app-usage/part-drop-down.png)
To delete a part or make it the main part, use the buttons in the top right of the **config** tab.

![The CONFIG tab of a robot's page noting the location of the Make main part and Delete Part buttons.](../../img/app-usage/part-mgmt.png)

If you've connected your robot to a machine running `viam-server`, the banner also displays when the robot was last online, which version of `viam-server` it is running, the host name, the IP address or addresses, and its operating system.

For each robot in your fleet, you start by setting up the robot on the **setup** tab:

### Setup

The **setup** tab contains information for starting an instance of `viam-server` on your robot's computer.

Once you select the correct **Mode** and **Architecture** for your system in the upper left of the tab, follow the instructions on the page to connect and set up your robot.

{{% alert title="Tip" color="tip" %}}
More in-depth information on installing `viam-server` can be found in our [Install Guide](/installation#install-viam-server).
{{% /alert %}}

### Configuration

After connecting your robot, go to the **config** tab, and start adding robot {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, and other robot resources.

For more information, see the [configuration documentation](../../configuration/#the-config-tab).

{{< alert title="Tip" color="tip" >}}
If you are managing a large fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your robot](../../configuration).
{{< /alert >}}

### Logs

Each robot automatically sends logs to the cloud which you can view on the **logs** tab.

### History

The configuration of your robot and the code it runs are kept separate to make debugging easier.
The **history** tab shows a timestamped diff view of your robot's configuration changes.

### Code Sample

To start programming your robot, go to the **code sample** tab which contains boilerplate code snippets you can copy and paste into your SDK code to connect to your robot.

For more information on the SDKs, see [Program your Robot with Viam's SDKs](../../../program/sdk-as-client/).

There is also a JSON stub you can copy if you wish to have your robot communicate with another robot as a [remote](../../parts-and-remotes/).

{{%  snippet "secret-share.md" %}}

### Control

Once you have configured components and services for your robot, you can visually test and remotely operate them from the **control** tab in the [Viam app](https://app.viam.com).
For example, if you have configured a base with wheels, you can control your robot's movement with an arrow pad and fields to change base’s speed.
If you have configured a camera component, a window in the **control** tab displays the camera output.

If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the robot uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).
For local communication between [parts](../../parts-and-remotes#robot-parts) Viam uses gRPC or WebRTC.

### Security

Your robot and the Viam app communicate securely by using unique secrets.
The **security** tab allows you to access and change the **Robot Part Secret Keys** of your robot.

![The SECURITY tab of a robot`s page noting the Robot Part Secret Keys drop-down menu, with the clipboard icon on the far right and the Generate Key button underneath the drop-down.](../../img/app-usage/robot-secrets.png)

Copy the secret key by clicking on the clipboard icon.
Click on the **Generate Key** button to generate a new key.

{{% alert title="Caution" color="caution" %}}
Be cautious when sharing robot part secret keys in your code or messages.

Do not make a secret key publicly available, as any entity who has this token has access to your robot, compromising the security of your system.

Note _where_ and _when_ you share a robot part secret key.
After generating a new secret key, remember that it's best practice to update all references to the key in your code as soon as possible, even though Viam supports flexible key rotation with up to two keys in use at one time.
{{% /alert %}}

## Delete a robot

You can delete a robot by checking the **Sure?** box in the lower left of the robot page and clicking **Delete robot**.

![The DELETE ROBOT button and the confirmation checkbox (Sure?) next to it.](../../img/app-usage/delete.png)
