---
title: "Services"
linkTitle: "Services"
weight: 600
type: docs
description: "Services are built-in software packages that make it easier to add complex capabilities such as motion planning or object detection to your machine."
images: ["/general/services.png"]
aliases:
  - "/services/"
---

Services are built-in software packages that make it easier to add complex capabilities such as motion planning or object detection to your machine.

In the following diagram, the machine is comprised of various hardware components including a GPS and a camera, and software (`viam-server`) running on a single-board computer.
Some of that software is the low-level code that communicates directly with the hardware [components](/components/), while some pieces of that software (the _services_) add higher-level functionality.
In this case, the vision service is configured to run computer vision models on output from the camera component.
The navigation service can take the raw output from the GPS component output and determine geographical location, and the data service captures data from any or all of the components, for example storing images from the camera.

{{< imgproc src="/viam/machine-components.png" alt="Machine components" resize="1000x" style="max-width:650px" class="aligncenter" >}}
<br>

Many built-in services run locally within `viam-server`, but you can think of them as discrete building blocks that you can mix and match however you want; you can run your machine using none, some, or all of them, depending on your use case.
To use a given service, add it to your machine's configuration.

[Configuring](/build/#step-2-configure) services on your machine indicates to `viam-server` which software packages you want to use with your machine, and how to integrate that software with your [components](/components/) and other services.
Services take many forms, so their configuration and usage varies widely.
For example, when you [configure data capture](/data/capture/), you indicate which types of data you want to capture, from which components.
When you configure the [frame system](/mobility/frame-system/), you indicate how the components relate to each other spatially.
Find more information in the documentation for each service below.

Viam provides built-in support for the following service types.
You can also add support for additional service types using [{{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}](/registry/).

{{< cards >}}
{{% card link="/data/" %}}
{{% card link="/mobility/motion/" %}}
{{% card link="/mobility/frame-system/" %}}
{{% card link="/mobility/base-rc/" %}}
{{% card link="/ml/deploy/" customTitle="Machine Learning" %}}
{{% card link="/mobility/navigation/" %}}
{{% card link="/mobility/slam/" %}}
{{% card link="/ml/vision/" %}}
{{% card link="/registry/advanced/generic/" %}}
{{< /cards >}}
