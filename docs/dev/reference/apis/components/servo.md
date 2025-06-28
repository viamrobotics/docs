---
title: "Servo API"
linkTitle: "Servo"
weight: 140
type: "docs"
description: "Give commands for controlling the angular position of a servo precisely or getting its current status."
icon: true
images: ["/icons/components/servo.svg"]
date: "2022-10-10"
aliases:
  - /appendix/apis/components/servo/
# updated: ""  # When the content was last entirely checked
---

The servo API allows you to give commands to your [servo components](/operate/reference/components/servo/) for controlling the angular position of a hobby servo precisely or getting its current status.

Industrial servos should use the [motor API](/dev/reference/apis/components/motor/) which provides more features than the servo API.

The servo component supports the following methods:

{{< readfile "/static/include/components/apis/generated/servo-table.md" >}}

## API

{{< readfile "/static/include/components/apis/generated/servo.md" >}}
