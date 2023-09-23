---
title: "Control Package"
linkTitle: "Control Package"
weight: 10
type: "docs"
description: "The Control Package implements feedback control on an endpoint."
# SME: Nicolas Menard, Rand
---

## Introduction

The control package implements feedback control on an endpoint (plant).
With the control package, users can design a control loop that monitors a process variable (PV) and compares it with a set point (SP).
The control package will generate a control action to reduce the error value between the SP and PV (_SP-PV_) to zero.

Control loops are usually represented in a diagrammatic style known as a block diagram.
Each block represents a transfer function of a component.
In this representation, the control loop is broken down into successive "blocks".

## Example

The following example is a block diagram of a control loop defined to control the speed of a motor.
The motor has an encoder that reports the position of the motor.

Measuring the reported position and deriving it to get the speed introduces some error, so you must apply a filter to remove the noise.

Then, calculate the error (_SP-PV_) (in this particular case PV is the speed of the motor) and feed it into your PID.

The PID controller applies a correction to a control function, and outputs the result of this correction to the endpoint block.

An important attribute of the control loop is the frequency at which it runs.
The higher the frequency, the better the control.
With more frequent steps the resulting error is smaller, which translates into smaller corrections at each step of the control loop.

```asciidoc

+-------------+            +------------+              +----------+        +----------+
|             |            |            |              |          |        |          |
|   SetPoint  +----------->|   Sum      +------------->|  PID     +------->| Endpoint |
|             |            |            |              |          |        |          |
|             |            |            |              |          |        |          |
+-------------+            +------------+              +----------+        +-----+----+
                                 ^                                               |
                                 |                                               |
                           +-----+------+              +----------+              |
                           |            |              |          |              |
                           |  Filter    |<-------------+ Derive   |<-------------+
                           |            |              |          |
                           |            |              |          |
                           +------------+              +----------+

```

```json
"control_config": {
          "frequency": 100,
          "blocks": [
            {
              "name": "set_point",
              "type": "constant",
              ....
            },
            {
              "name": "endpoint",
              "type": "endpoint",
              ...
              "depends_on":["PID"]
            },
            {
              "name" : "Filter",
              "type": "filter",
              ...
              },
              "depends_on":["Derivative"]
            },
            {
              "name": "Derivative",
              "type": "derivative",
              ....
              "depends_on":["endpoint"]
            },
            {
              "name": "PID",
              "type": "PID",
              ...
              "depends_on":["Sum"]
            },
            {
              "name": "Sum",
              "type" : "sum",
              ...
              "depends_on":["set_point","Filter"]
            }
          ]
        }
```

## Blocks

Blocks are configured similarly and share some common fields:

- `name` - Name is unique and should be used for dependencies
- `type` - Type of the block (see supported blocks)
- `attributes` - The attributes of the block
- `depends_on` - The list of blocks that this block depends on

### Gain

The Gain block multiplies a signal by the set gain. S_out = S_in \* Gain

```json
{
  "name": "Gain",
  "type": "gain",
  "attributes": {
    "gain": 0.00392156862
  },
  "depends_on": ["PID"]
}
```

### Constant

The Constant block outputs a constant signal. S_out = Cte

```json
{
  "name": "SetPoint",
  "type": "constant",
  "attributes": {
    "constant_val": 0.0
  }
}
```

### Endpoint

The Endpoint is a special type of block that is used to represent a plant.
For now, only DC motors with an encoder are supported as an endpoint in the control package.
The _motor_name_ attribute is unused for now, and one should pass a Controllable interface when creating the loop.

```json
{
  "name": "Endpoint",
  "type": "endpoint",
  "attributes": {
    "motor_name": "m-j1"
  },
  "depends_on": [""]
}
```

### PID

PID (Proportional Integral Derivative) is a widely used method to control a process variable.
The PID takes as input the error (equal to _SP - PV_), and calculates a value that can be fed back into the endpoint.
The mathematical form of a PID is:

u(t) = Kp\*e(t) + Ki\*int(e(t))\*dt + Kd\*(de(t)/dt)

Where:

- Kp, Ki, and Kd are the PID gains
- e(t) is the error at time t
- dt the time elapsed between two successive steps.

Finding the proper gains for a PID controller can be quite difficult.
There are two main approaches that one can use:

1. **Manual Tuning** - With this approach, the user tries different gains values and, using some visual feedback, adjusts them until a stable control can be achieved. In most cases this is not a suitable way to estimate gains.
2. **System Identification** - With this approach, the user attempts to measure quantitative plant data and estimate the proper gains values from these characteristics.

The following implementation records the step response of the plant and uses the relay method to estimate the ultimate gain (_Ku_) and oscillation period (_Tu_) of the plant.

Several methods to calculate Kp, Ki and Kd are implemented.

```json
{
    "name": "PID",
    "type": "PID",
    "attributes":{
        "kP":0.0, # Set each gain to 0 to start the tuning process
        "kI":0.0,
        "kD":0.0,
        "limit_up":255.0, # Maximum value of the PID
        "limit_lo":-255.0,
        "tune_ssr_value": 2.0, # Value used to detect steady state  1.0 - 2.0 is a sensible range
        "tune_method":"ziegerNicholsSomeOvershoot", # method to calculate the gains
        "tune_step_pct":0.35, # Size of the step
        "int_sat_lim_up":255.0, # Anti wind-up
        "int_sat_lim_lo":-255.0
    },
    "depends_on":[""]
}
```

### Encoder to RPM

Encoder to RPM converts encoder counts to rpm using ticks per rotation.

```json
{
  "name": "Derivative",
  "type": "encoderToRpm",
  "attributes": {
    "PulsesPerRevolution": 14
  },
  "depends_on": ["Endpoint"]
}
```

### Sum

Sum blocks sum a number of Signals following a set sum_string.

```json
{
  "name": "Sum",
  "type": "sum",
  "attributes": {
    "sum_string": "+-"
  },
  "depends_on": ["SetPoint", "Filter"]
}
```

### Trapezoidal Velocity Profile Generator

Position control of a motor can be achieved using the Trapezoidal Velocity Profile generator.

On receipt of a newly submitted set point, this block generates a velocity profile given the constraints set in the configuration.

This velocity profile is divided into three phases: Acceleration, Constant Speed, and Deceleration.

The generated profile is dynamically adjusted during the deceleration phase, ensuring the end position remains in the position window.

The block also works as a deadband controller when the target position is reached, preventing the motor from moving outside of the position window.

```json
"name":"trapz",
              "type":"trapezoidalVelocityProfile",
              "attributes":{
                "max_vel" : 4000.0,
                "max_acc" : 30000,
                "pos_window" : 10,
                "kpp_gain" : 0.45
              },
              "depends_on":["set_point","endpoint"]
}
```
