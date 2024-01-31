---
title: "Modular Resource Examples"
linkTitle: "Examples"
childTitleEndOverwrite: "Modular Resource Example"
description: "Tutorials and repositories with modular resources configuration examples."
weight: 70
type: "docs"
no_list: true
image: "/tutorials/intermode/rover_outside.png"
imageAlt: "A large black intermode rover controlled with CANBUS protocol chilling outside in the snow."
images: ["/tutorials/intermode/rover_outside.png"]
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
aliases:
  - "/program/extend/modular-resources/examples/"
  - "/extend/modular-resources/examples/"
  - "/modular-resources/examples/"
---

To familiarize yourself with creating and using {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, follow one of these example [tutorials](#tutorials) or clone one of these example [repositories](#repositories).
Once you have created a modular resource, you can test your modular resource using the [CONTROL tab](/fleet/#remote-control) and program it using the [Viam SDKs](/build/program/apis/).

## Tutorials

{{< cards >}}
{{% card link="/registry/examples/custom-arm/" %}}
{{% card link="/registry/examples/tflite-module/" customTitle="Add a TensorFlow Lite Modular Service"  %}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{% card link="/tutorials/custom/controlling-an-intermode-rover-canbus/" %}}
{{< /cards >}}

## Repositories

Detailed, working examples of various types of modular resources are included with [the RDK](https://github.com/viamrobotics/rdk/tree/main/examples/customresources), [the Python SDK](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/), and [Viam Labs](https://github.com/viam-labs/wifi-sensor).
