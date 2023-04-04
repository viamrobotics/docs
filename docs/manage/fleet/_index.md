---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "Configure, control, debug, and manage your robots from the cloud at app.viam.com."
tags: ["fleet management", "cloud", "app"]
---

Viam's fleet management system allows you to configure, control, debug, and manage your robots from the cloud at [https://app.viam.com](https://app.viam.com).

All communication happens securely over HTTPS using secret tokens that are in the robot's configuration.

Whether you have one robot, or millions, you can manage them with Viam and organize them into organizations and locations.

### Locations

{{< readfile "/static/include/manage/locations.md" >}}

For information on how to manage locations, see [Locations](locations).

<!-- IMAGE -->

### Organization

{{< readfile "/static/include/manage/organizations.md" >}}

{{<gif webm_src="../img/organizations.webm" mp4_src="../img/organizations.mp4" alt="An organization for personal robots and one for work robots.">}}

For information on how to manage organizations, see [Organizations](organizations).

## Configuration

When a robot or a robot part first comes online, it requests its configuration from the [Viam app](https://app.viam.com).
Once the robot has a configuration, it caches it locally and can use the configuration for up to 60 days.
The robot checks for new configurations every 15 seconds and changes its configuration automatically when a new configuration is available.

## Logs

Each robot automatically sends logs to the cloud where you can view them from the **LOGS** tab.

## Remote control

If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the robot uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).

For local communication between [parts](../parts-and-remotes) you can use gRPC or WebRTC.
