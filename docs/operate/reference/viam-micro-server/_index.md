---
title: "viam-micro-server"
linkTitle: "viam-micro-server"
weight: 90
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

`viam-micro-server` is the lightweight version of [`viam-server`](/operate/reference/viam-server/) which can run on resource-limited embedded systems (ESP32) that cannot run the fully-featured `viam-server`.
`viam-micro-server` is built from the open-source [Micro-RDK](https://github.com/viamrobotics/micro-rdk/).

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

To use `viam-micro-server`, follow the installation guide.
If you want to access camera functionality, extend the functionality of `viam-micro-server`, or customize it see the development setup guide.

{{< cards >}}
{{% card link="/operate/get-started/setup/" %}}
{{% card link="/operate/get-started/other-hardware/micro-module/" %}}
{{< /cards >}}
