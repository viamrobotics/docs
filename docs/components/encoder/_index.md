---
title: "Encoder Component"
linkTitle: "Encoder"
childTitleEndOverwrite: "Encoder Component"
weight: 50
type: "docs"
description: "A special type of sensor that measures rotation of a motor or joint."
tags: ["encoder", "components"]
icon: true
images: ["/icons/components/encoder.svg"]
no_list: true
modulescript: true
aliases:
  - "/components/encoder/"
hide_children: true
# SME: Rand
---

An encoder is a type of sensor that can detect speed and direction of rotation of a motor or a joint.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be mounted on a passive joint or other rotating object to keep track of the joint angle.

The encoder component supports:

- [Incremental encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which can measure the speed and direction of rotation in relation to a given reference point like a starting point.
  These encoders output two phases.
  Based on the sequence and timing of these phases, it is determined how far something has turned and in which direction.
  Each phase output goes to a different pin on the board.
- Single phase or single pin "pulse output" encoders, which measure the position relative to the starting position but not the direction.
- Absolute encoders, which provide the absolute position of a rotating shaft, without requiring a reference point.

Most machines with an encoder need at least the following hardware:

- A [board component](/components/board/) that can run a `viam-server` instance.
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.
- Some sort of rotary machine part (like a motor, joint or dial) for which you want to measure movement.

## Related services

{{< cards >}}
{{< relatedcard link="/services/motion/" >}}
{{< relatedcard link="/services/navigation/" >}}
{{< relatedcard link="/services/data/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:encoder" type="encoder">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Encoder](/build/micro-rdk/encoder/) for supported model information.

## Control your encoder with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have an encoder called `"my_encoder"` configured as a component of your machine.
If your encoder has a different name, change the `name` in the code.

Be sure to import the encoder package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.encoder import Encoder
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/encoder"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The encoder component supports the following methods:

{{< readfile "/static/include/components/apis/generated/encoder-table.md" >}}

{{< readfile "/static/include/components/apis/generated/encoder.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

{{< cards >}}
{{% card link="/tutorials/configure/configure-rover/" %}}
{{% card link="/components/motor/encoded-motor/" %}}
{{< /cards >}}
