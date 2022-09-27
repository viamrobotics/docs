---
title: "Encoder Component"
linkTitle: "Encoder Component"
weight: 50
type: "docs"
description: "Explanation of encoder types, configuration, and usage in Viam."
---
An encoder is a device that is used to sense angular position, direction and/or speed of rotation.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be positioned on a passive joint or other rotational object to keep track of the joint angle.

## Hardware Requirements
- A [board](../board) (like a Raspberry Pi)
- An encoder (quadrature or single phase)
- Some sort of rotary robot part (like a motor, joint or dial) for which you want to measure movement

## Mechanism
Viam supports [quadrature encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs)[^qe], which output two phases that can be used together to detect how far something has turned and in which direction.
Each phase output goes to a different pin on the board.
Viam also supports single pin “pulse output” encoders which give relative position but not direction.
[^qe]:quadrature encoders[https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs)

In either case position can only be determined relative to the starting position; these encoders are incremental and do not indicate absolute position.
Absolute encoders are another type of hardware that is not natively supported in Viam as of August 19th, 2022.

## Viam Configuration
Configuring an encoder requires configuring digital interrupts on the board [(see "Board > Digital Interrupts," for more information)](../board#digital-interrupts) to which the encoder will be wired, and configuring the encoder itself.
In the case of an encoded motor, the motor must be configured as well, per [the motor component doc](../motor#dc-motor-with-encoder).

### Example Config
The following example shows the configuration of a board with the necessary digital interrupts, and an encoder.

```JSON
{
  "components": [
    {
      "type": "board",
      "model": "pi",
      "name": "local",
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
      "type": "encoder",
      "model": "hall",
      "name": "myEncoder",
      "depends_on": [
        "local"
      ],
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

### Required Attributes
Besides `type` ("encoder"), `model` ("hall" for a two phase encoder) and `name` (of your choosing), encoder requires the following:

Attribute Name | Type | Meaning/Purpose
-------------- | ---- | ---------------
`pins` | object | A struct holding the names of the interrupts you configured in the board component.
-- `a` | string | Should match name of first digital interrupt you configured.
-- `b` | string | Required for two phase encoder. Should match name of second digital interrupt you configured.