---
title: "viam-micro-server"
linkTitle: "viam-micro-server"
weight: 90
type: docs
images: ["/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
description: "Set up the Espressif ESP32 for development with `viam-micro-server`."
date: "2024-09-03"
# updated: ""  # When the content was last entirely checked
# SMEs: Nicolas M., Gautham V., Andrew M.
---

`viam-micro-server` is the lightweight version of [`viam-server`](/architecture/viam-server/) which can run on resource-limited embedded systems (ESP32) that cannot run the fully-featured `viam-server`.
`viam-micro-server` is built from the [micro-RDK](https://github.com/viamrobotics/micro-rdk/tree/main).

## Hardware requirements

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

## Support

[Client API](/appendix/apis/) usage with the micro-RDK currently supports the following {{< glossary_tooltip term_id="resource" text="resources" >}}:

{{< cards >}}
{{% relatedcard link="/components/base/" %}}
{{% relatedcard link="/components/board/" %}}
{{% relatedcard link="/components/camera/" %}}
{{% relatedcard link="/components/encoder/" %}}
{{% relatedcard link="/components/movement-sensor/" %}}
{{% relatedcard link="/components/motor/" %}}
{{% relatedcard link="/components/sensor/" %}}
{{% relatedcard link="/components/servo/" %}}
{{% relatedcard link="/components/generic/" %}}
{{% relatedcard link="/services/data/" %}}
{{< /cards >}}

Click on each supported resource to see available models, API methods, and configuration info.

## Next steps

To use `viam-micro-server`, follow the installation guide.
If you want to access camera functionality, extend the functionality of `viam-micro-server, or customize it see the development setup guide.

{{< cards >}}
{{% card link="/installation/viam-server-setup/" %}}
{{% card link="/installation/viam-micro-server-dev/" %}}
{{< /cards >}}
