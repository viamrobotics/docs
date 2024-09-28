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
  - /micro-rdk/encoder/
  - /build/micro-rdk/encoder/
hide_children: true
# SME: Rand
---

Encoders provide an API for getting the position of a motor or a joint in ticks or degrees.

If you have hardware or software that provides the position of a motor, use an _encoder_ component.

Encoder components are often used in conjunction with a motor, and are sometimes even built directly into motors.
Encoder can also be mounted on a passive joint or other rotating object to keep track of the joint angle.

The encoder component supports:

- [Incremental encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which can measure the speed and direction of rotation in relation to a given reference point like a starting point.
  These encoders output two phases.
  Based on the sequence and timing of these phases, it is determined how far something has turned and in which direction.
  Each phase output goes to a different pin on the board.
- Single phase or single pin "pulse output" encoders, which measure the position relative to the starting position but not the direction.
- Absolute encoders, which provide the absolute position of a rotating shaft, without requiring a reference point.

## Available models

To use an encoder, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows you the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:encoder" type="encoder" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`incremental`](incremental-micro-rdk/) | A two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point |
| [`single`](single-micro-rdk/) | A single pin "pulse output" encoder which returns its relative position but no direction |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [encoder API](/appendix/apis/components/encoder/), which supports the following methods:

{{< readfile "/static/include/components/apis/generated/encoder-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/components/motor/encoded-motor/" noimage="true" %}}
{{< /cards >}}

You can also use the encoder component with the following services:

- [data management service](/services/data/): to capture and sync the sensor's data
- [motion service](/services/motion/): to move machines or components of machines
- [navigation service](/services/navigation/): to navigate with GPS
