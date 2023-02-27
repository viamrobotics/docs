---
title: "Encoder Component"
linkTitle: "Encoder"
weight: 50
type: "docs"
description: "A special type of sensor that measures rotation of a motor or joint."
tags: ["encoder", "components"]
icon: "img/components/encoder.png"
# SME: Rand
---
An encoder is a device that is used to sense angular position, direction and/or speed of rotation.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be positioned on a passive joint or other rotational object to keep track of the joint angle.

## Hardware Requirements

- A [board](/components/board/) (like a Raspberry Pi)
- An encoder (quadrature or single phase)
- Some sort of rotary robot part (like a motor, joint or dial) for which you want to measure movement

## Mechanism

Viam supports [quadrature encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which output two phases that can be used together to detect how far something has turned and in which direction.
Each phase output goes to a different pin on the board.
Viam also supports single pin "pulse output" encoders which give relative position but not direction.

In either case position can only be determined relative to the starting position; these encoders are incremental and do not indicate absolute position.
Absolute encoders are another type of hardware that is not natively supported in Viam as of August 19, 2022.

## Viam Configuration

Configuring an encoder requires configuring two pins on the board to which the encoder is wired, as well as configuring the [board component](/components/board/).
In the case of an encoded motor, the motor must be configured as well, per [the motor component topic](/components/motor/#dc-motor-with-encoder).

### Required Attributes

Besides `type` ("encoder"), `model` ("incremental" for a two phase encoder) and `name` (of your choosing), encoder requires the following:

Attribute Name | Type | Description
-------------- | ---- | ---------------
`board` | string | The name of the board to which the encoder is wired.
`pins` | object | A struct holding the names of the pins wired to the encoder.

The `pins` struct contains:

Name  | Type | Description
---- | ---- | ----
`a` | string | Pin number of one of the pins to which the encoder is wired. Use pin number, not GPIO number.
`b` | string | Required for two phase encoder. Pin number for the second board pin to which the encoder is wired.

Viam also supports a model of encoder called "single" that requires only one pin (`i`).
However, the incremental model is recommended as encoders with two signal wires are more accurate.

### Example Config

The following example shows the configuration of a board and an encoder.

```json-viam {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {}
    },
    {
      "name": "myEncoder",
      "type": "encoder",
      "model": "incremental",
      "attributes": {
        "board": "local",
        "pins": {
          "a": "13",
          "b": "11"
        }
      }
    }
  ]
}
```
