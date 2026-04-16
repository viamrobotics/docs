---
linkTitle: "Configure hardware"
title: "Configure hardware"
weight: 35
layout: "docs"
type: "docs"
no_list: true
description: "Understand how Viam represents hardware, add components to your machine, and configure them."
manualLink: "/hardware/configure-hardware/"
aliases:
  - /hardware-components/
  - /hardware/
---

Viam represents every piece of hardware on your machine as a **component**
with a standardized API. A camera is a camera whether it connects over USB,
Ethernet, or CSI. A motor is a motor whether it's a brushed DC motor on
GPIO pins or a stepper on a CAN bus. Your application code calls the same
methods regardless of the underlying hardware.

This means you can swap hardware without rewriting code, reuse
configurations across a fleet of identical machines, and test your
application logic against fake components before the physical hardware
arrives.

This section covers how to add hardware to your machine, configure it, and
verify it works.

{{< cards >}}
{{% card link="/hardware/configure-hardware/" %}}
{{% card link="/hardware/common-components/" %}}
{{% card link="/hardware/component-types/" %}}
{{% card link="/hardware/machine-configuration/" %}}
{{% card link="/hardware/multi-machine/" %}}
{{% card link="/hardware/fragments/" %}}
{{% card link="/build-modules/overview/" %}}
{{< /cards >}}
