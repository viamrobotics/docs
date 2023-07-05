---
title: "Modular Resource Configuration Examples"
linkTitle: "Examples"
childTitleEndOverwrite: "Modular Resource Example"
description: "Tutorials and repositories with modular resources configuration examples."
weight: 10
type: "docs"
no_list: true
image: "/tutorials/img/intermode/rover_outside.png"
imageAlt: "A large black intermode rover controlled with CANBUS protocol chilling outside in the snow."
images: ["/tutorials/img/intermode/rover_outside.png"]
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
aliases:
    - "/program/extend/modular-resources/examples/"
---

To familiarize yourself with creating and using modular resources, follow one of these example [tutorials](#tutorials) or clone one of these example [repositories](#repositories).
Once you have created a modular resource, you can test your custom resource using the [Control tab](/manage/fleet/#remote-control) and program it using the [Viam SDKs](/program/apis/).

## Tutorials

{{< cards >}}
    {{% card link="/extend/modular-resources/examples/rplidar" custom="Add an RPlidar camera as a Modular Resource" %}}
    {{% card link="/extend/modular-resources/examples/odrive" custom="Add an ODrive motor as a Modular Resource" %}}
    {{% card link="/tutorials/custom/controlling-an-intermode-rover-canbus/" %}}
{{< /cards >}}

## Repositories

Detailed, working examples of various types of modular resources are included in [Viam's GitHub](https://github.com/viamrobotics) with [the RDK](https://github.com/viamrobotics/rdk/tree/main/examples/customresources), [the Python SDK](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/module), and [Viam Labs](https://github.com/viam-labs/wifi-sensor).
