---
title: "Manage machines with Viam's machine management API"
linkTitle: "Machine management"
weight: 20
type: "docs"
description: "How to use the machine API to monitor and manage your machines."
tags: ["robot state", "sdk", "apis", "robot api"]
aliases:
  - /program/apis/robot/
  - /build/program/apis/robot/
  - /appendix/apis/robot/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The _machine API_ allows you to connect to your machine from within a supported [Viam SDK](/dev/reference/apis/), retrieve status information, and send commands remotely.

The machine API is supported for use with the [Viam Python SDK](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient), the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#RobotClient), and the [Viam C++ SDK](https://cpp.viam.dev/classviam_1_1sdk_1_1RobotClient.html).

The machine API supports the following methods:

{{< readfile "/static/include/robot/apis/generated/robot-table.md" >}}

## Establish a connection

To use the machine management API, navigate to the **CONNECT** tab of one of your machines to get sample code.

## API

{{< readfile "/static/include/robot/apis/generated/robot.md" >}}
