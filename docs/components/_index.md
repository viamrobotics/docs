---
title: "Components"
linkTitle: "Components"
weight: 500
type: docs
description: "In-depth information on the various components available within the Viam system."
images: ["/icons/components.png"]
aliases:
  - "/components/"
---

Viam provides support for a wide variety of hardware.
A _component_ represents a physical piece of hardware in your {{< glossary_tooltip term_id="machine" text="machine" >}}, and the software that directly supports that hardware.

{{< imgproc src="/viam/machine-components.png" alt="Diagram with various components and services on a smart machine. This machine employs the vision, navigation, and data capture services, which run within viam-server on the machine's single board computer." resize="650x" class="aligncenter" >}}
<br>

Viam groups categories of hardware together, with a [standardized API](/build/program/apis/#component-apis) for all _{{< glossary_tooltip term_id="model" text="models" >}}_ in each grouping.
For example, [`xarm7`](/components/arm/xarm7/) and [`ur5e`](/components/arm/ur5e/) are different arm models, which provide software support for xArm7 arms and UR5e arms, respectively.
Though the hardware is different, you use the same Viam SDK commands to control both models, for example [`MoveToPosition`](/components/arm/#movetoposition).

You need to [configure](/build/#step-2-configure) a component to represent each piece of hardware your machine controls.
Configuration is the process of editing the file that indicates to `viam-server` what hardware is available to it, how to communicate with that hardware, and how the pieces of hardware relate to each other (for example, which board a motor is connected to).

Viam provides built-in support for the following component types.
You can also add support for additional component types using [{{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}](/registry/).

If you are connecting components to a microcontroller instead of a 64-bit single-board computer, find component configuration information in the [micro-RDK documentation](/build/micro-rdk/).
