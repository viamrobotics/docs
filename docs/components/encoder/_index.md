---
title: "Encoder Component"
linkTitle: "Encoder"
weight: 50
type: "docs"
description: "A special type of sensor that measures rotation of a motor or joint."
tags: ["encoder", "components"]
icon: "img/components/encoder.png"
no_list: true
# SME: Rand
---

An encoder is a device that can detect angular position, as well as direction and speed of rotation of a motor or a joint.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be positioned on a passive joint or other rotational object to keep track of the joint angle.

The encoder component supports:

- [Quadrature encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which output two phases that can be used together to detect how far something has turned and in which direction.
  Each phase output goes to a different pin on the board.
- Single phase or single pin "pulse output" encoders which give relative position but not direction.
- Absolute encoders which provide angular measurements directly.

Both encoders are incremental and do not indicate absolute positions.
Therefore, the component can only determine the position relative to the starting position.

Most robots with an encoder (quadrature or single phase) need at least the following hardware:

- A [board component](/components/board/) that can run a `viam-server` instance.
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.
- Some sort of rotary robot part (like a motor, joint or dial) for which you want to measure movement

## Configuration

To configure am encoder as a component of your robot, first configure the [board](/components/board/) controlling the encoder.
If you are configuring an encoded motor, you must also configure the [motor](/components/motor/) first.

The configuration of your encoder component depends on your encoder model.
For configuration information, click on one of the following models:

| Model | Description |
| ----- | ----------- |
| [`AM5-AS5048`](am5) | The `AM5-AS5048` encoder uses an I2C or SPI interface to connect. |
| [`arduino`](arduino) | An encoder using an arduino board. |
| [`fake`](fake) | An encoder model for testing. |
| [`incremental`](incremental) | A two phase encoder. |
| [`single`](single) | A single pin "pulse output" encoder which returns its relative position but no direction. |
