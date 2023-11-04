---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "Configure, control, debug, and manage your smart machines from the cloud at app.viam.com on your own or with a team."
tags: ["fleet management", "cloud", "app"]
no_list: true
aliases:
  - "/manage/fleet-management"
  - "/manage/app-usage"
  - "/product-overviews/fleet-management/"
  - "/fleet"
---

The [Viam app](https://app.viam.com) provides fleet management allowing you to work on any number of smart machines alone or in collaboration with others.
You can manage your fleet of smart machines from the Viam app or using the [cloud API](/program/apis/cloud/).

## Work with groups of smart machines

With Viam, you can organize {{< glossary_tooltip term_id="robot" text="robots" >}} into {{< glossary_tooltip term_id="location" text="locations" >}} and {{< glossary_tooltip term_id="organization" text="organizations" >}}.

For example, you may have separate organizations for your robots at home and at work:

<!-- this is a very small gif - conversion to mp4 caused issues -->
<img src="/manage/organizations.gif" alt="An organization for personal robots and one for work robots.">

Inside an organization, you can organize robots into one or more locations:

![An image of two locations, New York, and Chicago, in one organization, Good Robots](/manage/locations.png)

If you are managing a fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your robots](../configuration/), allowing you to use the same configuration for multiple robots.

## Use Viam for collaboration

To facilitate collaboration, you can add collaborators to organizations, assign [permissions](#permissions) to collaborators, and share locations across multiple organizations.

When you create a Viam account, Viam automatically creates an organization for you.
You can use this organization as your collaboration hub by inviting collaborators to your organization.
You can also add additional organizations as desired at any time.

{{< alert title="Caution" color="caution" >}}
Everyone you invite as an owner to your organization has complete access to everything in that organization.
This includes the permissions to delete robots and locations, as well as the ability to remove you from the organization.
{{< /alert >}}

You can also share locations across different organizations **that you are part of**.

### Permissions

Role Based Access Control (RBAC) is a way to enforce security in the [Viam app](https://app.viam.com) by assigning organization members roles that confer permissions.
Permissions are added at the organization level and apply to everything in an org.

- **Owner**: Can see and edit [every tab on the robot page](robots/#navigating-the-robot-page).
  Can manage users in the app.
- **Operator**: Can see and use only the [remote control tab](robots/#control).
  Cannot see or edit the [**Setup**](robots/#setup), [**Config**](robots/#configuration), [**History**](robots/#history), [**Logs**](robots/#logs), [**Code sample**](robots/#code-sample), or [**Security**](robots/#security) tabs.

To view the roles each organization member has, click on the organization drop down in the top navigation bar and click on **Settings**.

If you have the **Owner** role, you can [invite new users](organizations/#invite-users-to-your-organization) and change the roles assigned to organization members using the role drop down for the respective user.

![Example permissions overview](/manage/rbac.png)

## Collaborate on your robots

Viam is built in a way that allows you to change configurations, deploy packages, check logs, and control your robots both when you are close to your robot, as well as remotely.

Robot [configuration](robots/#configuration) and robot [code](#control-with-the-sdks) is intentionally kept separate, allowing you to keep track of versioning and debug issues separately.

### Configuration

Everyone who has access to the location the robot is in, can change the robot's [configuration](robots/#configuration).

{{< alert title="Simultaneous config edits" color="caution" >}}
If you edit a config while someone else edits the same config, the person who saves last will overwrite any prior changes that aren't reflected in the new config.

Before editing a config, we recommend you refresh the page to ensure you have all the latest changes.
{{< /alert >}}

{{< alert title="Tip" color="tip" >}}
For some configuration aspects you may require physical access to the robot so you can see how components are connected.
{{< /alert >}}

#### Reconfiguration

When you or your collaborators change a robot's configuration, the robot will automatically reconfigure itself within 15 seconds.
You can see configuration changes made by yourself or by your collaborators on the [History tab](robots/#history).
You can also revert to an earlier configuration from the History tab.

### Package deployment

_Coming soon._

You and your collaborators can deploy control logic, {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, sidecar [processes](../configuration/#processes), or [machine learning models](../../services/ml/) to your fleet of robots without manually copying files by uploading it to Viam's cloud and deploying it to your fleet.

### Remote control

Everyone who has access to the robot can remotely control it on the app's [**Control** tab](robots/#control).
This allows you to visually test and remotely operate robot components and services.

You can also control a robot using the [Viam mobile app](#the-viam-mobile-app).

### Control with the SDKs

Everyone who has access to the robot's location can obtain the robot's remote address and location secret from the app's **Code sample** tab, which are both needed to send API calls to the robot from the [Viam SDKs](/program/apis/).
You can share the robot's remote address and location secret without granting location access in the app.

As long as each collaborator has access to these tokens for a robot, members of your team can write code, use tools like GitHub, and execute code to control the robot from anywhere in the world.

Toggle **Include secret** above the code on the **Code Sample** tab of your robot's page to display or hide the robot's location secret.
The robot's remote address is displayed on both the **Control** and **Code sample** tabs of your robot's page in the app, ending with `viam.cloud`.

{{% snippet "secret-share.md" %}}

### Logging

Each robot automatically sends logs to the cloud where you can view them from the [**Logs** tab](robots/#logs).
If you are collaborating on a robot and controlling it using the [**Control** tab](robots/#control) or [SDK code](#control-with-the-sdks), everyone who has access to the location the robot is in can see the robot's logs.

### Deployment

You and your collaborators can deploy [control logic](/program/apis/), [modular resources](/registry/), sidecar [processes](../configuration/#processes), or [machine learning models](/services/ml/) to your fleet of robots without manually copying files by uploading it to Viam's cloud and deploying it to your fleet.

## The Viam mobile app

{{<gif webm_src="/manage/mobile-app-octagon.webm" mp4_src="/manage/mobile-app-octagon.mp4" alt="GIF of red button being pressed and cannon of confetti bot spraying confetti" class="alignright" max-width="200px">}}

<br>

In addition to the [Viam app](https://app.viam.com), the fully featured web application where you can access all fleet management tools, there is a Viam mobile app.
The mobile app is a convenient way to see if your robot is online, access the [control interface](/manage/fleet/robots/#control), and check robot [logs](/manage/fleet/robots/#logs).

You can find the mobile app on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).
