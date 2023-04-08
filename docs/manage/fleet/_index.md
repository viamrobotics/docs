---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "Configure, control, debug, and manage your robots from the cloud at app.viam.com."
tags: ["fleet management", "cloud", "app"]
aliases:
    - /manage/fleet-management
    - /manage/app-usage
---

The [Viam app](https://app.viam.com) provides fleet management allowing you to:

- manage your robots and access to them with [locations](#locations), [organizations](#organization), and [permissions](#permissions)
- [configure](#configuration) individual or groups of robots
- [deploy code and machine learning models](#package-deployment) to robots
- [remotely control](#remote-control) and [debug](#logs) robots

All communication happens securely over HTTPS using secret tokens that are in a robot's configuration.

## Locations

{{< readfile "/static/include/manage/locations.md" >}}

![An image of two locations, New York, and Chicago, in one organization, Good Robots](../img/locations.png)

For information on how to manage locations, see [Locations](locations).

## Organization

{{< readfile "/static/include/manage/organizations.md" >}}

{{<gif webm_src="../img/organizations.webm" mp4_src="../img/organizations.mp4" alt="An organization for personal robots and one for work robots.">}}

For information on how to manage organizations, see [Organizations](organizations).

## Permissions

_Coming soon._

Role Based Access Control (RBAC) ia a way to enforce security in the [Viam app](https://app.viam.com) by assigning users roles that confer permissions:

- **Owner**: Can see and edit [every tab on the robot page](robots/#navigating-the-robot-page).
- **Operator**: Can see and use only the [remote control tab](robots/#control).
  Cannot see or edit the [**SETUP**](robots/#setup), [**CONFIG**](robots/#config), [**HISTORY**](robots/#history), [**LOGS**](robots/#logs), [**CODE SAMPLE**](robots/#code-sample), or [**SECURITY**](robots/#security) tabs.

A user can have one or more roles, granting the user the respective permissions of each role.

## Configuration

When a robot or a {{< glossary_tooltip term_id="part" text="robot part" >}} that is managed with the Viam app first comes online, it requests its configuration from the [Viam app](https://app.viam.com).
Once the robot has a configuration, it caches it locally and can use the configuration for up to 60 days.
The robot checks for new configurations every 15 seconds and changes its configuration automatically when a new configuration is available.

{{< alert title="Tip" color="tip" >}}
If you are managing a large fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your robot](../configuration).
{{< /alert >}}

## Package Deployment

_Coming soon._

Deploy control logic, [modular resources](/program/extend/modular-resources/), sidecar [processes](../configuration/#processes), or [machine learning models](../ml/deploy-model/), to your fleet of robots without manually copying files by uploading it to Viam's cloud and deploying it to your fleet.

## Remote control

The **CONTROL** tab in the [Viam app](https://app.viam.com) allows you to visually test and remotely operate robot components and services.
All communication to the robot uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).
If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the robot uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).

For local communication between [parts](../parts-and-remotes) Viam uses gRPC or WebRTC.

## Logs

Each robot automatically sends logs to the cloud where you can view them from the **LOGS** tab.
