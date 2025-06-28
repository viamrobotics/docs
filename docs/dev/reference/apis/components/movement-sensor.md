---
title: "Movement sensor API"
linkTitle: "Movement sensor"
weight: 110
type: "docs"
description: "Give commands for getting the current GPS location, linear velocity and acceleration, angular velocity and acceleration and heading."
icon: true
images: ["/icons/components/imu.svg"]
date: "2022-10-10"
aliases:
  - /appendix/apis/components/movement-sensor/
# updated: ""  # When the content was last entirely checked
---

The movement sensor API allows you to give commands to your [movement sensor components](/operate/reference/components/movement-sensor/) for getting a GPS location, linear velocity and acceleration, angular velocity and acceleration and heading.

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

<!-- IMPORTANT: This resource uses a manual table file. Automation does not update this file! -->
<!-- Please be sure to update this manual file if you are updating movement-sensor! -->

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

## API

{{< readfile "/static/include/components/apis/generated/movement_sensor.md" >}}
