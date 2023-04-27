---
title: "Examples of configuring modular resources"
linkTitle: "Examples"
description: "Tutorials and repositories with examples of configuring modular resources."
weight: 10
type: "docs"
no_list: true
image: "/tutorials/img/intermode/rover_outside.png"
imageAlt: "A large black intermode rover controlled with CANBUS protocol chilling outside in the snow."
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
---

The easiest way to familiarize yourself with creating and using modular resources is to:

1. Follow one of these example [tutorials](#tutorials) or clone one of these example [repositories](#repositories).
2. Control the custom resource on [the Viam app's](https://app.viam.com) [__CONTROL__ tab](/manage/fleet/#remote-control).
3. Control the custom resource programmatically with a [Viam SDK](/program/sdk-as-client/).
4. Experiment by changing the resource's behavior.

## Tutorials

{{< cards >}}
    {{% card link="/program/extend/modular-resources/examples/add-rplidar-module" size="small" %}}
    {{% card link="/tutorials/custom/controlling-an-intermode-rover-canbus/" size="small" %}}
{{< /cards >}}

## Repositories

Detailed, working examples of various types of modular resources are included in [Viam's GitHub](https://github.com/viamrobotics) with [the RDK](https://github.com/viamrobotics/rdk/tree/main/examples/customresources), [the Python SDK](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/module), and [Viam Labs](https://github.com/viam-labs/wifi-sensor).
