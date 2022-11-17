---
title: "Encoder Component"
linkTitle: "Encoder"
weight: 50
type: "docs"
description: "Explanation of encoder configuration and usage in Viam."
# SME: Rand
---
An encoder is a device that is used to sense angular position, direction and/or speed of rotation.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be positioned on a passive joint or other rotational object to keep track of the joint angle.

## Hardware Requirements

- A [board](../board/) (like a Raspberry Pi)
- An encoder (quadrature or single phase)
- Some sort of rotary robot part (like a motor, joint or dial) for which you want to measure movement

## Mechanism

Viam supports <a href="https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs" target="_blank">quadrature encoders</a>[^qe], which output two phases that can be used together to detect how far something has turned and in which direction.
Each phase output goes to a different pin on the board.
Viam also supports single pin “pulse output” encoders which give relative position but not direction.

[^qe]:quadrature encoders: <a href="https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs</a>

In either case position can only be determined relative to the starting position; these encoders are incremental and do not indicate absolute position.
Absolute encoders are another type of hardware that is not natively supported in Viam as of August 19th, 2022.

## Viam Configuration

Configuring an encoder requires configuring digital interrupts on the board (for additional information, see [Board > Digital Interrupts](../board/#digital-interrupts)) to which the encoder will be wired, and configuring the encoder itself.
In the case of an encoded motor, the motor must be configured as well, per [the motor component topic](../motor/#dc-motor-with-encoder).

### Required Attributes

Besides `type` ("encoder"), `model` ("incremental" for a two phase encoder) and `name` (of your choosing), encoder requires the following:

Attribute Name | Type | Description
-------------- | ---- | ---------------
`board` | string | The name of the board to which the encoder is wired.
`pins` | object | A struct holding the names of the interrupts you configured in the board component.

The `pins` struct contains:

Name  | Type | Description
---- | ---- | ----
`a` | string | Should match name of first digital interrupt you configured.
`b` | string | Required for two phase encoder. Should match name of second digital interrupt you configured.

Viam also supports a model of encoder called "single" that requires only one pin (`i`) and one corresponding digital interrupt.
However, the incremental model is recommended as encoders with two signal wires are more accurate.

### Example Config
The following example shows the configuration of a board with the necessary digital interrupts, and an encoder.

```json-viam
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "encoderA",
            "pin": "13"
          },
          {
            "name": "encoderB",
            "pin": "11"
          }
        ]
      }
    },
    {
      "name": "myEncoder",
      "type": "encoder",
      "model": "incremental",
      "attributes": {
        "board": "local",
        "pins": {
          "a": "encoderA",
          "b": "encoderB"
        }
      }
    }
  ]
}
```
