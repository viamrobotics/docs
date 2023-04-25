---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "Configure, control, debug, and manage your robots from the cloud at app.viam.com on your own or with a team."
tags: ["fleet management", "cloud", "app"]
no_list: true
aliases:
    - "/manage/fleet-management"
    - "/manage/app-usage"
    - "/product-overviews/fleet-management/"
---

The [Viam app](https://app.viam.com) provides fleet management allowing you to work alone or in collaboration with others on one or more robots.

## Work with groups of robots

With Viam, you can organize {{< glossary_tooltip term_id="robot" text="robots" >}} into {{< glossary_tooltip term_id="location" text="locations" >}} and {{< glossary_tooltip term_id="organization" text="organizations" >}}.

For example, you may have separate organizations for your robots at home and at work:

{{<gif webm_src="../img/organizations.webm" mp4_src="../img/organizations.mp4" alt="An organization for personal robots and one for work robots.">}}

Inside an organization, you can organize robots into one or more locations:

![An image of two locations, New York, and Chicago, in one organization, Good Robots](../img/locations.png)

If you are managing a large fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your robots](../configuration), allowing you to use the same configuration for multiple robots.

## Use Viam for collaboration

To facilitate collaboration, you can add collaborators to organizations, and share locations across multiple organizations. Soon you will also be able to assign [permissions](#permissions) to collaborators.

When you create a Viam account, Viam automatically creates an organization for you.
You can use this organization or add another organization as your collaboration hub by inviting collaborators to your organization.

{{< alert title="Caution" color="caution" >}}
Currently, everyone you invite to your organization, has complete access to everything in that organization.
This includes the permissions to delete robots and locations, as well as the ability to remove you from the organization.

[Permissions](#permissions) are coming soon.
{{< /alert >}}

You can also share locations across different organizations **that you are also part of**.

### Permissions

_Coming soon._

Role Based Access Control (RBAC) ia a way to enforce security in the [Viam app](https://app.viam.com) by assigning organization members roles that confer permissions:

- **Owner**: Can see and edit [every tab on the robot page](robots/#navigating-the-robot-page).
  Can manage users in the app.
- **Operator**: Can see and use only the [remote control tab](robots/#control).
  Cannot see or edit the [**setup**](robots/#setup), [**config**](robots#configuration), [**history**](robots/#history), [**logs**](robots/#logs), [**code sample**](robots/#code-sample), or [**security**](robots/#security) tabs.

A user can have one or more roles, granting the user the respective permissions of each role.

## Collaborate on your robots

Viam is built in a way that allows you to change configurations, deploy packages, check logs, and control your robots both when you are close to your robot, as well as remotely.

Robot [configuration](robots/#configuration) and Robot [code](#control-with-code) is intentially kept separate, allowing you to keep track of versioning and debug issues separately.

### Configuration

Everyone who has access to the location the robot is in, can change the robot's configuration.
When you or your collaborators change a robot's configuration, the robot will automatically reconfigure itself within 15 seconds.
You can see configuration changes from yourself or your collaborators on the [History tab](robots/#history).
You can also revert to an earlier configuration from the History tab.

{{< alert title="Note" color="note" >}}
Configuration may require physical access to the robot.
{{< /alert >}}

### Package Deployment

_Coming soon._

You and your collaborators can deploy control logic, [modular resources](/program/extend/modular-resources/), sidecar [processes](../configuration/#processes), or [machine learning models](../../services/ml/) to your fleet of robots without manually copying files by uploading it to Viam's cloud and deploying it to your fleet.

### Remote control

Everyone who has access to the location the robot is in, can remotely control the robot using the [**control** tab](robots/#control).
This allows you to visually test and remotely operate robot components and services
If you are remotely controlling the robot, it is recommended that you or your collaborators install a [camera](/components/camera), so you can monitor the robot as you control it.

### Control with code

Everyone who has access to the location the robot is in, can obtain the robot address and secret needed to send API calls to the robot.
You can also share the robot address and location secret without granting location access in the Viam app.

With the robot address and the location secret, you can write code, collaborate on your code using tools like GitHub and run your code on the robot from anywhere in the world.
If you are remotely controlling the robot, it is recommended that you or your collaborators install a [camera](/components/camera), so you can monitor the robot as you control it.

{{% alert title="Caution" color="caution" %}}
Be cautious when sharing location secret keys in your code or messages.

Do not make a secret key publicly available, as anyone who has the secret key can access your location, compromising the security of your system.

It is good practice to note _where_ and _when_ you share a location secret key.
{{% /alert %}}

### Logs

Each robot automatically sends logs to the cloud where you can view them from the [**logs** tab](robots/#logs).
If you are collaborating on a robot and controlling it using the [**control** tab](robots/#control) or [code](#control-with-code), everyone who has access to the location the robot is in, can see the robot's logs.
