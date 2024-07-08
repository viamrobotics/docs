---
title: "Base Component"
linkTitle: "Base"
weight: 10
type: "docs"
no_list: true
description: "A moving platform that the other parts of a mobile robot attach to."
tags: ["base", "components"]
icon: true
images: ["/icons/components/base.svg"]
modulescript: true
aliases:
  - "/components/base/"
hide_children: true
# SMEs: Steve B
---

A base is the platform that the other parts of a mobile robot attach to.

By configuring a base component, organizing individual components to produce coordinated movement, you gain an interface to control the movement of the whole physical base of the robot without needing to send separate commands to individual motors.

![A robot comprised of a wheeled base (motors, wheels and chassis) as well as some other components. The wheels are highlighted to indicate that they are part of the concept of a 'base', while the non-base components are not highlighted. The width and circumference are required attributes when configuring a base component.](/components/base/base-trk-rover-w-arm.png)

Most mobile robots with a base need at least the following hardware:

- A [board](/components/board/).
- Some sort of actuators to move the base.
  Usually [motors](/components/motor/) attached to wheels or propellers.
- A power supply for the board.
- A power supply for the actuators.
- Some sort of chassis to hold everything together.

## Related services

{{< cards >}}
{{< relatedcard link="/services/base-rc/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/navigation/" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:base" type="base">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Base](/build/micro-rdk/base/) for supported model information.

## Control your base with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a wheeled base called `"my_base"` configured as a component of your machine.
If your base has a different name, change the `name` in the code.

Be sure to import the base package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.base import Base
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/base"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The base component supports the following methods:

{{< readfile "/static/include/components/apis/generated/base-table.md" >}}

{{< readfile "/static/include/components/apis/generated/base.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/configure/configure-rover" %}}
{{% card link="/tutorials/get-started/try-viam-sdk" %}}
{{% card link="/tutorials/services/webcam-line-follower-robot" %}}
{{< /cards >}}
