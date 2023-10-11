---
title: "Extend Viam with Modular Resources"
linkTitle: "Modular Resources"
weight: 50
type: "docs"
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Use the Viam module system to implement modular resources that can be included in any Viam-powered robot."
no_list: true
aliases:
  - "/program/extend/modular-resources/"
  - "/extend/modular-resources/"
  - "/extend/"
---

Viam's [Robot Development Kit (RDK)](/internals/rdk/) provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware [components](/components/).
- High-level functionality exposed as [services](/services/).

However, if you want to work with a new hardware component that is not already supported by Viam, or want to introduce a new software service or service model to support additional functionality on your smart machine, you can extend Viam by adding a _modular resource_ to your smart machine.

Modular resources are defined in _modules_, which are easy to create and add to your robot.
A module can provide one or more modular resources.

With modular resources, you can:

- **Implement a custom component:** If your robot has specialty hardware, such as an unsupported [motor](/components/motor/), and you want to control it using Viam, you can write a driver to support your hardware by implementing the corresponding component API.

- **Implement a custom service:** If your robot makes use of a specialty algorithm or data model when working with services such as [SLAM](/services/slam/), [Vision](/services/vision/), or [Motion planning](/services/motion/), you can implement your own algorithm or model against the corresponding service API.

- **Implement fully custom logic:** If your robot runs specialty or proprietary logic, and you want to use Viam to manage and control that logic, such as when managing a software development lifecycle, you can implement your own custom logic by wrapping the [generic API](/components/generic/).

You can add support for modular resources to your robot by adding a module from the Viam registry.

## The Viam Registry

The [Viam registry](https://app.viam.com/registry) allows hardware and software engineers to collaborate on their robotics projects by writing and sharing custom modules with each other.
You can add a module from the Viam registry directly from your robot's **Configuration** tab in [the Viam app](https://app.viam.com/), using the **+ Create component** button.

The code behind any modular resource can be packaged as a {{< glossary_tooltip term_id="module" text="module" >}} and uploaded to the Viam registry.
Once the module has been uploaded to the Registry, you can [deploy the module](/modular-resources/configure/) to any robot in your organization from [the Viam app](https://app.viam.com/).

### Uploading to the Viam Registry

After you finish programming your module, you can [upload your module to the Viam registry](/modular-resources/upload/) to make it available for deployment to robots.
As part of the upload process, you decide whether your module is _private_ (visible only to other members of your [organization](/manage/fleet/organizations/)), or _public_ (visible to all Viam users).

You can see details about each module in the [Viam registry](https://app.viam.com/registry) on its module details page.
See the [Odrive module](https://app.viam.com/module/viam/odrive) for an example.
Public modules also display the number of times a module has been deployed to a robot.

When you make changes to your module, you can [uploaded the newer version](/modular-resources/upload/#update-an-existing-module) with a new version number, and the Viam registry will track each version that you upload.

### Deploying to a Robot

Once you [upload a module to the Viam registry](/modular-resources/upload/), you can [deploy the module](/modular-resources/configure/) to any robot in your organization from [the Viam app](https://app.viam.com/).
Navigate to your robot's **Configuration** tab, click the **+ Create component** button, then start typing the name of the module you would like to deploy.

By default, a newly-created module is _private_, meaning that the module will only appear for users within your [organization](/manage/fleet/organizations/), but you can later [update your module](/modular-resources/upload/#update-an-existing-module) to set it to be _public_, which makes your module available to all Viam users.

When you deploy a module to your robot, you can [choose how to update that module](/modular-resources/configure/#configure-version-update-management-for-a-registry-module) when new versions become available.

## Get Started

To get started working with modular resources:

- Learn the [key concepts](/modular-resources/key-concepts/) behind Viam's modular resources that make the module system possible.

- [Create your own module](/modular-resources/create/) implementing at least one modular resource.

- [Upload your module to the Viam registry](/modular-resources/upload/) to share with the community, or just to your own organization.

- Browse the [Viam registry](https://app.viam.com/registry) to see modules uploaded by other users.

- [Deploy a module](/modular-resources/configure/) to your robot from the Registry.

- Browse the [modular resources tutorials](/modular-resources/examples/) for examples of deploying and using custom modular resources on your robot.

Once you have deployed a modular resource, you can test the custom resource using the [Control tab](/manage/fleet/#remote-control) and [program](/program/) it with Viam's Go or Python SDKs.

## Related tutorials

{{< cards >}}
{{% card link="/modular-resources/examples/rplidar" %}}
{{% card link="/modular-resources/examples/odrive" %}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{< /cards >}}
