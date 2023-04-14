---
title: "Encoder Component"
linkTitle: "Encoder"
weight: 50
type: "docs"
description: "A special type of sensor that measures rotation of a motor or joint."
tags: ["encoder", "components"]
icon: "/components/img/components/encoder.png"
no_list: true
# SME: Rand
---

An encoder is a type of sensor that can detect speed and direction of rotation of a motor or a joint.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be positioned on a passive joint or other rotating object to keep track of the joint angle.

The encoder component supports:

- [Incremental encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which can measure the speed and direction of rotation in relation to a given reference point like a starting point.
  These encoders output two phases.
  Based on the sequence and timing of these phases, it is determined how far something has turned and in which direction.
  Each phase output goes to a different pin on the board.
- Single phase or single pin "pulse output" encoders, which measure the position relative to the starting position but not the direction.
- Absolute encoders, which provide the absolute position of a rotating shaft, without requiring a reference point.

Most robots with an encoder need at least the following hardware:

- A [board component](/components/board/) that can run a `viam-server` instance.
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.
- Some sort of rotary robot part (like a motor, joint or dial) for which you want to measure movement

## Configuration

To configure an encoder as a component of your robot, first configure the [board](/components/board/) controlling the encoder.
If you are configuring an encoded motor, you must also configure the [motor](/components/motor/) first.

The configuration of your encoder component depends on your encoder model.
For configuration information, click on one of the following models:

| Model | Description |
| ----- | ----------- |
| [`AMS-AS5048`](ams-as5048) | The `AMS-AS5048` encoder is an absolute encoder that which can connect using an I2C interface. |
| [`fake`](fake) | An encoder model for testing. |
| [`incremental`](incremental) | A two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point. |
| [`single`](single) | A single pin "pulse output" encoder which returns its relative position but no direction. |

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/configure/scuttlebot" size="small" %}}
{{< /cards >}}
