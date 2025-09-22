---
title: "The Micro-RDK and viam-micro-server"
linkTitle: "viam-micro-server"
weight: 40
type: docs
images: ["/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
description: "Set up the Espressif ESP32 for development with `viam-micro-server`."
date: "2024-09-03"
aliases:
  - /architecture/viam-micro-server/
# updated: ""  # When the content was last entirely checked
# SMEs: Nicolas M., Gautham V., Andrew M.
---

[The Micro-RDK](https://github.com/viamrobotics/micro-rdk/) is the lightweight version of Viam's [Robot Development Kit (RDK)](https://github.com/viamrobotics/rdk/tree/main) designed for embedded systems (ESP32 microcontrollers) that do not have the resources to run the fully-featured [`viam-server`](/operate/reference/viam-server/).

Microcontrollers do not have full operating systems like single-board computers and general-purpose computers.
As a result, microcontrollers only run one program at a time.
To change the logic that runs on a microcontroller, you must flash the microcontroller with new firmware.

`viam-micro-server` is the pre-built firmware built from the Micro-RDK and a [default set](/operate/install/setup-micro/#about-esp32-microcontroller-setup) of {{< glossary_tooltip term_id="module" text="modules" >}}, provided as a quick starting point.
For most use cases, you will [build your own firmware](/operate/install/setup-micro/#build-and-flash-custom-firmware) from the Micro-RDK instead of using `viam-micro-server`.

## Hardware requirements

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

## Support

[Client API](/dev/reference/apis/) usage with the Micro-RDK currently supports the following {{< glossary_tooltip term_id="resource" text="resources" >}}:

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/components/base/" %}}
{{% relatedcard link="/dev/reference/apis/components/board/" %}}
{{% relatedcard link="/dev/reference/apis/components/camera/" %}}
{{% relatedcard link="/dev/reference/apis/components/encoder/" %}}
{{% relatedcard link="/dev/reference/apis/components/movement-sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/motor/" %}}
{{% relatedcard link="/dev/reference/apis/components/sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/servo/" %}}
{{% relatedcard link="/dev/reference/apis/components/generic/" %}}
{{% relatedcard link="/dev/reference/apis/services/data/" %}}
{{< /cards >}}

## Next steps

To use the Micro-RDK with existing modules, follow the ESP32 setup guide.
To create your own modules, follow the Modules for ESP32 guide.

{{< cards >}}
{{% card link="/operate/install/setup-micro/" %}}
{{% card link="/operate/modules/other-hardware/micro-module/" %}}
{{< /cards >}}
