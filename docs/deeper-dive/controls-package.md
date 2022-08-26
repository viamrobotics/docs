# Control Package
## Introduction
The control package implements feedback control on an endpoint (plant). Users can design a control loop that monitors a process variable (PV) and compares it with a set point (SP). 
The difference between SP-PV is called the error. It is used to generate a control action to reduce this error to zero.
Control loops are usually represented by a diagrammatic style knows as block diagram, in this representation the control loop is broken down into successive blocks or mathematical operations.

## Example
In the following example we define a control loop to control the speed of a motor. The motor has an encoder that reports the position of the motor. To obtain the speed, we must derive its position. Since measuring the position and deriving it to get the speed introduces some error, we need to apply a filter to remove that noise. We then calculate our error, SP - PV (in this particular case PV is the speed of the motor), and feed it into our PID. The PID controller does some mathematical magic gives us a value (for example, PWM) that we can feed into our endpoint.
An important attribute of the control loop is the frequency at which it runs, basically the higher the frequency the better the control. That is, with more frequent steps, the resulting error is smaller, which translates into smaller corrections at each step of the control loop.

``` asciidoc

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

``` json
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

  * `name` - Name is unique and should be used for dependencies
  * `type` - Type of the block (see supported blocks)
  * `attributes` - The attributes of the block
  * `depends_on` - The list of blocks that this block depends on

### Gain
The Gain block multiplies a signal by the set gain. S_out = S_in * Gain
``` json
{
    "name": "Gain",
    "type": "gain",
    "attributes":{
        "gain":0.00392156862
    },
    "depends_on":["PID"]
}
```

### Constant
The Constant block outputs a constant signal. S_out = Cte
``` json
{
    "name": "SetPoint",
    "type": "constant",
    "attributes":{
        "constant_val": 0.0
    }
}
```
### Endpoint
The Endpoint is a special type of block that is used to represent a plant. 
For now only DC motors with an encoder are supported as an endpoint. 
The motor\_name attribute is unused for now and one should pass a Controllable interface when creating the loop.
``` json
{
    "name": "Endpoint",
    "type": "endpoint",
    "attributes":{
    "motor_name":"m-j1"
    },
    "depends_on":[""]
}
```
### PID
PID (or Proportional Integral Derivative ) is a wildly used method to control a process variable. 
The PID takes an error which is equal to SP - PV, and calculate a value that can be feed back into the endpoint.
The mathematical form of a PID is:

u(t) = Kp\*e(t) + Ki\*int(e(t))\*dt + Kd\*(de(t)/dt) 

Where:

* Kp, Ki, and Kd are the PID gains
* e(t) is the error at time t
* dt the time elapsed between two successive steps.

Finding the proper gains for a PID controller can be quite difficult, there are two main approaches that one can use:

1. **Manual Tuning** - In this case the user tries different gains values and using some visual feedback adjust them until a stable control can be achieve. 
In most cases this is not a suitable way to estimate gains.
2. **System Identification** - With System Identification we attempt the find the characteristics of plant and deduce the gains. 
Our current implementation record the step response of the plant and using the relay method estimate the ultimate gain Ku and oscillation period Tu of the plant.
Several methods to calculate Kp, Ki and Kd are implemented.

``` json
{
    "name": "PID",
    "type": "PID",
    "attributes":{
        "kP":0.0, # Set each gains to 0 to start the tuning process
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
``` json
{
    "name": "Derivative",
    "type": "encoderToRpm",
    "attributes":{
    "PulsesPerRevolution" : 14
    },
    "depends_on":["Endpoint"]
}
```
### Sum
Sum blocks sums a number of Signals following a set sum\_string
``` json
{
    "name": "Sum",
    "type" : "sum",
    "attributes":{
        "sum_string":"+-"
    },
    "depends_on":["SetPoint","Filter"]
}
```
### Trapezoidal Velocity Profile Generator
Position control of a motor can be achieve using the Trapezoidal Velocity Profile generator. 
On receipt of a newly, submitted set point, this block generates a velocity profile given the constraints set in the configuration. 
This profile can be divided in 3 phases : Acceleration, Constant Speed, and Deceleration, the generated profile is also dynamically adjusted during the deceleration phase ensuring the end position remains in the position window.
The block also works as deadband controller when target position is reached preventing the motor moving outside the position window
``` json
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
