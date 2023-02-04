---
title: "Configure a motor with an encoder"
linkTitle: "Encoded Motors"
weight: 90
type: "docs"
description: "How to configure an encoded motor."
# SMEs: Rand, James
---

Some motors come with encoders integrated with or attached to them.
Other times, you may add an encoder to a motor.
See the [encoder component documentation](/components/encoder/) for more information on encoders.

Viam supports motors with encoders within model `gpio`.
Configuration of an encoder requires configuring the encoder [per the encoder documentation](/components/encoder) in addition to the [standard “gpio” model attributes](/components/motor/gpio/).
Here’s an example config file:

![motor-encoded-dc-json](/components/img/motor/motor-encoded-dc-json.png)

[Click here for the raw JSON.](/components/example-configs/motor-encoded-config.json)

#### Required Attributes

In addition to the required [attributes for a non-encoded motor](/components/motor/gpio/#required-attributes), encoded DC motors require the following:

Name | Type | Description
-------------- | ---- | ---------------
`encoder` | string | Should match name of the encoder you configure as an `encoder` component.
`ticks_per_rotation` | string | Number of ticks in a full rotation of the encoder (and motor shaft).

#### Optional Attributes

In addition to the optional attributes listed in the [non-encoded DC motor section](/components/motor/gpio/#optional-attributes), encoded motors have the following additional options:

Name | Type | Description
-------------- | ---- | ---------------
`ramp_rate` | float | How fast to ramp power to motor when using RPM control. 0.01 ramps very slowly; 1 ramps instantaneously. Range is (0, 1]. Default is 0.2.

## Wiring Example

Here's an example of an encoded DC motor wired with [the MAX14870 Single Brushed DC Motor Driver Carrier](https://www.pololu.com/product/2961).
This wiring example corresponds to the [example config above]().

![motor-encoded-dc-wiring](/components/img/motor/motor-encoded-dc-wiring.png)
