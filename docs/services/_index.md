---
title: "Services"
linkTitle: "Services"
weight: 420
type: docs
description: "Services are built-in software packages that make it easier to add complex capabilities such as motion planning or object detection to your machine."
images: ["/general/services.png"]
aliases:
  - "/services/"
menuindent: true
no_list: true
---

Services are built-in software packages that make it easier to add complex capabilities such as motion planning or object detection to your machine.

In the following diagram, the machine is comprised of various hardware components including a GPS and a camera, and software (`viam-server`) running on a single-board computer.
Some of that software is the low-level code that communicates directly with the hardware [components](/components/), while some pieces of that software (the _services_) add higher-level functionality.
In this case, the vision service is configured to run computer vision models on output from the camera component.
The navigation service can take the raw output from the GPS component output and determine geographical location, and the data service captures data from any or all of the components, for example storing images from the camera.

{{< imgproc src="/viam/machine-services.png" alt="Machine components" resize="650x" class="aligncenter" >}}
<br>

Many built-in services run locally within `viam-server`, but you can think of them as discrete building blocks that you can mix and match however you want; you can run your machine using none, some, or all of them, depending on your use case.
To use a given service, add it to your machine's configuration.

[Configuring](/configure/#services) services on your machine indicates to `viam-server` which software packages you want to use with your machine, and how to integrate that software with your [components](/components/) and other services.
Services take many forms, so their configuration and usage varies widely.
For example, when you [configure data capture](/services/data/capture/), you indicate which types of data you want to capture, from which components.
When you configure the [frame system](/services/frame-system/), you indicate how the components relate to each other spatially.
Find more information in the documentation for each service below.

Viam provides built-in support for the following service types.
You can also add support for additional service types using [{{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}](/registry/).

{{< cards >}}
{{% card link="/services/data/" %}}
{{% card link="/services/vision/" %}}
{{% card link="/services/ml/deploy/" customTitle="Machine Learning" %}}
{{% card link="/services/motion/" %}}
{{% card link="/services/frame-system/" %}}
{{% card link="/services/navigation/" %}}
{{% card link="/services/slam/" %}}
{{% card link="/services/base-rc/" %}}
{{% card link="/services/generic/" %}}
{{< /cards >}}
