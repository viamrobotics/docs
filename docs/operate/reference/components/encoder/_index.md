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
date: "2024-10-21"
# SME: Rand
---

The encoder component provides an API for getting the position of a motor or a joint in ticks or degrees.

If you have hardware or software that provides the position of a motor or joint, use an encoder component.

Encoder components are often used in conjunction with a motor, and are sometimes even built directly into motors.
Encoders can also be mounted on a passive joint or other rotating object to keep track of the joint angle.

The encoder component supports:

- [Incremental encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which can measure the speed and direction of rotation in relation to a given reference point like a starting point.
  These encoders output two phases.
  Based on the sequence and timing of these phases, it is determined how far something has turned and in which direction.
  Each phase output goes to a different pin on the board.
- Single phase or single pin "pulse output" encoders, which measure the position relative to the starting position but not the direction.
- Absolute encoders, which provide the absolute position of a rotating shaft, without requiring a reference point.

## Configuration

To use an encoder, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your encoder.

The following list shows the available encoder models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:encoder" type="encoder" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`incremental`](incremental-micro-rdk/) | A two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point |
| [`single`](single-micro-rdk/) | A single pin "pulse output" encoder which returns its relative position but no direction |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [encoder API](/dev/reference/apis/components/encoder/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/encoder-table.md" >}}

## Troubleshooting

If your encoder is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your encoder model's documentation to ensure you have configured all required attributes.
1. Check that all wires are securely attached to the correct pins.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the encoder there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/operate/reference/components/motor/encoded-motor/" noimage="true" %}}
{{< /cards >}}

You can also use the encoder component with the following services:

- [Data management service](/data-ai/capture-data/capture-sync/): To capture and sync the encoder's data
- [Motion service](/operate/reference/services/motion/): To move machines or components of machines
- [Navigation service](/operate/reference/services/navigation/): To navigate with GPS
