---
title: "Motor Component"
linkTitle: "Motor Component"
weight: 80
type: "docs"
description: "Explanation of motor types, configuration, and usage in Viam."
---
Note: Information on hobby servos (i.e., servomotors) is located in the <a href="../servo">Servo Component Document</a>.

Electric motors are the most common form of actuator in robotics.
The majority of motors used in robotics require a direct current (DC) input.
This page covers how to wire, configure and control various types of DC motor with Viam.

## General Hardware Requirements
A common motor control setup comprises the following:

- A computing device with general purpose input/output (GPIO) pins such as a Raspberry Pi or other single-board computer, or a desktop computer outfitted with a GPIO peripheral
    - Note: there are other ways to interface with motors such as Serial, CAN bus and EtherCAT that require special motor controllers and are beyond the scope of this document
- A DC motor
- An appropriate motor driver
    - Takes GPIO signals from the computer and sends the corresponding signals and power to the motor
    - Selected based on the type of motor (i.e. brushed, brushless or stepper) and its power requirements
- An appropriate power supply
    - Note that the logic side of the driver may be powered by 3.3V from the Pi or other device, but the motor power side should not be powered by the computer’s GPIO pins.
    The motor driver should be connected to an independent power supply that can provide the peak current required by the motor.

**Caution: Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.**

## Brushed DC Motor
### Mechanism
DC motors use magnetic fields to convert direct (one-way) electrical current into mechanical torque.
[Brushed DC motors](https://en.wikipedia.org/wiki/Brushed_DC_electric_motor)[^bdcm] use an electrical contact called a “brush” to route current to the right place at a given moment to create continuous rotation.
Increasing the input current increases the output motor torque (and also speed, assuming a constant load).
Switching the direction of the input current changes the direction of motor rotation.

[^bdcm]: Brushed DC motors: [https://en.wikipedia.org/wiki/Brushed_DC_electric_motor](https://en.wikipedia.org/wiki/Brushed_DC_electric_motor)

### Brushed DC Motor Drivers
A motor driver is a physical chip or power amplification circuit that converts input signals from a computing device into a high power output capable of actuating a motor.
There are three common ways for the computing device to communicate with a brushed DC motor driver chip.
The driver data sheet will specify which one to use.

#### Pins

- PWM/DIR: One digital input (such as a GPIO pin) sends a [pulse width modulation](https://en.wikipedia.org/wiki/Pulse-width_modulation)[^pwm] (PWM) signal to the driver to control speed while another digital input sends a high or low signal to control the direction.
- A/B: One digital input is set to high and another set to low turns the motor in one direction and vice versa, while speed is controlled via PWM through one or both pins.
- A/B + PWM: Three pins: an A and B to control direction and a separate PWM pin to control speed.

[^pwm]: Pulse Width Modulation (PWM):  [https://en.wikipedia.org/wiki/Pulse-width_modulation](https://en.wikipedia.org/wiki/Pulse-width_modulation)

---

**Note:**
    Often, instead of buying just the tiny motor driver chip itself, you’ll purchase a motor driver carrier board which consists of the chip containing the logic gates, attached to a small breakout board which gives you places to attach the necessary wires.
    In this article we’ll refer to this whole motor driver board as a motor driver.
    Note that in RDK, “board” refers to the device with GPIO pins (such as a Raspberry Pi, or a GPIO peripheral attached to a desktop computer) that sends signals to the motor drivers and other devices.
    In the config file, “motor” technically refers to the motor driver for a given motor.

---

### Wiring
Brushed DC motors are relatively simple to wire.
Taking a 12V brushed DC motor controlled by a Raspberry Pi via [this motor driver](https://www.pololu.com/product/4038) as an example, the wiring diagram would look like this:  
  
![brushed-dc-wiring](../img/motor-brushed-dc-wiring.png)  

The signal wires in the diagram run from two GPIO pins on the Pi to the DIR and PWM pins on the motor driver.
Refer to a Raspberry Pi pinout schematic to locate generic GPIO pins and determine their pin numbers for configuration.

### Viam Configuration
A brushed DC motor without an encoder should be configured with “gpio” as the model.
Most motor types require a “board” attribute, and also need to depend on that same board.
For example:  

![motor-gpio-json](../img/motor-gpio-json.png)  
[Click here for the raw JSON.](../example-configs/motor-gpio-config.json)

#### Required Attributes - Non-Encoded DC Motor
Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
`board  ` | string | --        | Name of board on which it depends
`max_rpm` | float | --         | This is an estimate of the maximum RPM the motor will run at with full power under no load. The go_for method calculates how much power to send to the motor as a percentage of `max_rpm`. If unknown, it can be set to zero but this will render the “GoFor” method unusable.
`pins` | object | --  | A structure that holds pin configuration information

Nested within `pins` (note that only two or three of these are required depending on your motor driver; see [Pins](#pins) above for more information):

Name | Type | Description |
---- | ---- | ----- |
`a` | string | See [Pins](#pins). Pin number such as "36." Viam uses board pin numbers, not GPIO numbers.
`b` | string | See [Pins](#pins). Pin number such as "36." Viam uses board pin numbers, not GPIO numbers.
`dir` | string | See [Pins](#pins). Pin number such as "36." Viam uses board pin numbers, not GPIO numbers.
`pwm` | string | See [Pins](#pins). Pin number such as "36." Viam uses board pin numbers, not GPIO numbers.

#### Optional Attributes
Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
`min_power_pct` | float | 0.0 | Sets a limit on minimum power percentage sent to the motor 
`max_power_pct` | float | 1.0 | Range is 0.06 to 1.0; sets a limit on maximum power percentage sent to the motor  
`pwm_freq` | uint | 800 | Sets the PWM pulse frequency in Hz.  Many motors operate optimally in the kHz range.
`dir_flip` | bool | False | Flips the direction of the signal sent if there is a DIR pin  
`en_high` / `en_low` | string | -- | Some drivers have optional enable pins that enable or disable the driver chip. If your chip requires a high signal to be enabled, add `en_high` with the pin number to the pins section. If you need a low signal use `en_low`.

## Brushless DC Motor

### Mechanism
A brushless DC motor (BLDC motor) uses an electronic system to switch its electromagnets on and off at the correct times, instead of the physical brush used in brushed motors.
BLDCs function similarly to brushed motors, but they are more durable and efficient because they don’t contain a brush that wears out as it rubs on the spinning components.
The relative position of the magnets must be known by the driver so that the right coils can be powered at any given moment.
Some motors have a built-in set of Hall effect sensors for this purpose, and others detect forces in the unpowered coils for a “sensorless” configuration.

### Brushless DC Motor Drivers
Brushless DC motor drivers work in much the same way as brushed DC motor drivers.
They typically require a PWM/DIR input or a A/B and PWM input to set the motor power and direction.
The key difference between a brushed and brushless motor driver is on the motor output side.
Brushless motors typically have three power connections (commonly referred to as A, B and C; or sometimes Phase 1, 2 and 3) and 3 sensor connections (commonly referred to as Hall A, Hall B and Hall C) running between the motor and driver.

### Wiring and Configuration
The configuration file of a BLDC motor with Viam is the same as that of a brushed motor.
Only the output side of the driver board is different, i.e. more wires connect the driver to the motor.

![motor-brushless-dc-wiring](../img/motor-brushless-dc-wiring.png)  

## DC Motor With Encoder

Some motors come with encoders integrated or attached to them.
Other times, you may add an encoder to a motor.
See the [Encoder Component Doc](../encoder) for more information on encoders.

### Wiring

Here's an example of an encoded DC motor wired with [this motor driver](https://www.pololu.com/product/2961).

![motor-encoded-dc-wiring](../img/motor-encoded-dc-wiring.png)  

### Viam Configuration

Viam supports a brushed or brushless DC motor with a quadrature encoder within model “gpio.”
Configuration of an encoder requires configuring the encoder [per this document](../encoder) in addition to the [standard “gpio” model attributes](motor#required-attributes---non-encoded-dc-motor). Additionally, the encoder name must be added in the motor's `depends_on` field.
Here’s an example config file:  

![motor-encoded-dc-json](../img/motor-encoded-dc-json.png)  

[Click here for the raw JSON.](../example-configs/motor-encoded-config.json)

#### Required Attributes - Encoded DC Motor
In addtion to the required [attributes of a non-encoded motor](#required-attributes---non-encoded-dc-motor), encoded DC motors require the following:

Name | Type | Description
-------------- | ---- | ---------------
`encoder` | string | Should match name of the encoder you configure as an `encoder` component.
`ticks_per_rotation` | string | Number of ticks in a full rotation of the encoder (and motor shaft).

#### Optional Attributes
In addition to the optional attributes [listed in the non-encoded DC motor section](#optional-attributes), encoded motors have the following additional options:  

Name | Type | Description
-------------- | ---- | ---------------
`ramp_rate` | float | How fast to ramp power to motor when using RPM control. 0.01 ramps very slowly; 1 ramps instantaneously. Range is (0, 1]. Default is 0.2.

## Stepper Motor

### Mechanism
A stepper motor, though it is technically a type of brushless DC motor, differs from what we generally think of as a DC motor in wiring, control and purpose.
Whereas DC motors are designed for continuous rotation, sometimes at high speeds, stepper motors are for precise open loop control (without feedback) and turn in discrete increments.
Stepper motors have many electromagnets arranged such that each rotation is broken down into many (often 200) steps.
These steps can be further subdivided into half steps and even smaller micro steps by controlling current to the motor windings with PWM.

### Wiring
Typically, a stepper motor will have an even number of wires.
Each pair of wires makes a loop through a coil of the motor.
In the case of a four wire (bi-polar) stepper, one pair of wires may be labeled A1 and A2 and the other B1 and B2.
Refer to the motor data sheet for correct wiring.

![motor-gpiostepper-wiring](../img/motor-gpiostepper-wiring.png)  

In this particular example the enable pin on the upper left corner of the driver is connected to ground to pull it low for our purposes.

### Viam Configuration
Viam supports steppers controlled in one of two ways: a basic stepper driver chip that takes step and DIR input via GPIO and simply moves one step per pulse (for these, use model "gpiostepper"), or more advanced chips (e.g., TMC5072, DMC4000) that have their own microcontrollers that conveniently handle things like speed and acceleration control.
Here’s an example of a basic stepper driver config:  

![motor-gpiostepper-json](../img/motor-gpiostepper-json.png)  
[Click here for the raw JSON.](../example-configs/motor-gpiostepper-config.json)

#### Required Attributes for Steppers

Name | Type | Description
-------------- | ---- | ---------------
`board` | string | Should match name of board on which motor depends.
`pins` | object | A structure containing "step" and "dir" pin numbers; see example JSON above.
`ticks_per_rotation` | integer | Number of full steps in a rotation. 200 (equivalent to 1.8 degrees per step) is very common.

#### Optional Attributes

Name | Type | Description
-------------- | ---- | ---------------
`stepper_delay` | uint | Time in microseconds to remain high for each step. Default is 20.

## Implementation
[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/motor/client/index.html)