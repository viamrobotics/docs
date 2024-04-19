---
title: "Control Package"
linkTitle: "Control Package"
weight: 10
type: "docs"
description: "The Control Package implements feedback control on an endpoint."
# SME: Nicolas Menard, Rand, Martha
---

[Encoded motors](/components/motor/gpio/encoded-motor/) and [sensor controlled bases](/components/base/sensor-controlled/) use a control loop that is implemented by `viam-server`.
You can configure the `control_parameters` attribute for both components to adjust the control loop.
However, if you want to change or customize the control loops on these components beyond the configurable parameter, or you want to add a control loop to a different component, you can use the controls package to [build your own PID control loop](/internals/controls-package/#creating-and-using-a-pid-control-loop).

The control package implements feedback control on an endpoint, which is usually the hardware you are trying to control.
With the control package, users can design a control loop that monitors a process variable (PV) and compares it with a set point (SP).
The control package will generate a control action to reduce the error value between the SP and PV (_SP-PV_) to zero.

Control loops are usually represented in a diagrammatic style known as a block diagram.
Each block represents a transfer function of a component.
In this representation, the control loop is broken down into successive "blocks".

## Creating and Using a PID Control Loop

A PID control loop is a commonly used method of controls.
A PID control loop computes a correction for the error value between SP and PV using three terms:

- A _proportional_ term that is the current error
- An _integral_ term that is the total cumulative error
- A _derivative_ term that is the rate of change of the error

By tuning the coefficients on each of these terms, you can adjust how your base converges towards the target value, how quickly the system reaches the target value, and how much the system overshoots when approaching the target value.

The following functions are available for creating and using a control loop:

<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`SetupPIDControlConfig`](/internals/controls-package/#setuppidcontrolconfig) | Creates a [PIDLoop](/internals/controls-package/#pidloop) object that contains all the necessary attributes to run a control loop based on the specified [Options](/internals/controls-package/#options).
[`TunePIDLoop`](/internals/controls-package/#tunepidloop) | Automatically tunes the system and logs the calculated PID values for the loop.
[`StartControlLoop`](/internals/controls-package/#startcontrolloop) | Starts the control loop in a background thread.
[`CreateConstantBlock`](/internals/controls-package/#createconstantblock) | Creates a control block of type `constant`, all control loops need at least one constant block representing the set point.
[`UpdateConstantBlock`](/internals/controls-package/#updateconstantblock) | Updates the value of a constant block to the new set point.
[`CreateTrapzBlock`](/internals/controls-package/#createtrapzblock) | Creates a control block of type `trapezoidalVelocityProfile`. Control loops that control position (for example, control loops for encoded motors), need a trapezoidal velocity profile block.
[`UpdateTrapzBlock`](/internals/controls-package/#updatetrapzblock) | Updates the attributes of a trapezoidal velocity profile block to the new desired max velocity.

### SetupPIDControlConfig

Creates a [PIDLoop](/internals/controls-package/#pidloop) object, which contains all the attributes related to a control loop that a controlled component needs, including, most importantly, the control config.

**Parameters:**

- `pidVals` [([]PIDConfig)](/internals/controls-package/#pidconfig): The P, I, and D values for the control loop, if all are zero the loop will auto-tune and log the calculated PID values.
- `componentName` [(string)](https://pkg.go.dev/builtin#string): The name of the component that the PID loop controls.
- `options` [(Options)](/internals/controls-package/#options): All the desired optional parameters to customize the control loop.
- `c` [(Controllable)](/internals/controls-package/#controllable): An interface that contains the necessary functions to move the controlled component.
- `logger` (Logger): The logger of the controlled component to log any issues with the control loop setup.

**Returns:**

- [(PIDLoop)](/internals/controls-package/#pidloop): A struct containing all relevant control loop attributes.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
pidVals := []control.PIDConfig{{
  Type: "",
  P: 1.0,
  I: 2.0,
  D: 0.0,
}}

options := control.Options{
  PositionControlUsingTrapz: true,
  LoopFrequency:             100.0,
}

pidLoop, err := control.SetupPIDControlLoop(pidVals, "motor_name", options, motor, motor.logger)
```

### TunePIDLoop

Tunes the provided loop to determine the best PID values.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cancelFunc` [(CancelFunc)](https://pkg.go.dev/context#CancelFunc): A CancelFunc tells an operation to abandon its work.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
// add necessary attributes to the PIDLoop struct
pidLoop := &control.PIDLoop{}

cancelCtx, cancelFunc := context.WithCancel(context.Background())
err := pidLoop.TunePIDLoop(cancelCtx, cancelFunc)
```

### StartControlLoop

Starts running the PID control loop to monitor and adjust the inputs to the controlled component.

**Parameters:**

- None

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
// add necessary attributes to the PIDLoop struct
pidLoop := &control.PIDLoop{}

err := pidLoop.StartControlLoop()
```

### CreateConstantBlock

Creates a new control block of type `constant`.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name` [(string)](https://pkg.go.dev/builtin#string): The desired name of the constant block.
- `constVal` [(float64)](https://pkg.go.dev/builtin#float64): The value of the new set point.

**Returns:**

[(BlockConfig)](/internals/controls-package/#blockconfig): The config for the newly created block.

```go
constBlock := control.CreatConstantBlock(context.Background(), "set_point", 10.0)
```

### UpdateConstantBlock

Creates a new control block of type `constant`, and then updates the control loop to use this new block.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name` [(string)](https://pkg.go.dev/builtin#string): The name of the constant block.
- `constVal` [(float64)](https://pkg.go.dev/builtin#float64): The value of the new set point.
- `loop` (`*Loop`): The control loop to be updated with the newly created constant block.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
err := control.UpdateConstantBlock(context.Background(), "set_point", 10.0, loop)
```

### CreateTrapzBlock

Creates a new control block of type `trapezoidalVelocityProfile`.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name` [(string)](https://pkg.go.dev/builtin#string): The name of the trapezoidal block.
- `maxVel` [(float64)](https://pkg.go.dev/builtin#float64): The max velocity for the controlled component to move at.
- `dependsOn` [([]string)](https://pkg.go.dev/builtin#string): An array of strings containing the names of the other control blocks that the new trapezoidal block depends on. Usually the set point and the end point.

**Returns:**

[(BlockConfig)](/internals/controls-package/#blockconfig): The config for the newly created block.

```go
trapzBlock := control.CreateTrapzBlock(context.Background(), "set_point", 10.0, []string{"set_point", "endpoint"})
```

### UpdateTrapzBlock

Creates a new control block of type `trapezoidalVelocityProfile`, and then updates the control loop to use this new block.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `name` [(string)](https://pkg.go.dev/builtin#string): The name of the trapezoidal block.
- `maxVel` [(float64)](https://pkg.go.dev/builtin#float64): The max velocity for the controlled component to move at.
- `dependsOn` [([]string)](https://pkg.go.dev/builtin#string): An array of strings containing the names of the other control blocks that the new trapezoidal block depends on. Usually the set point and the end point.
- `loop` (`*Loop`): The control loop to be updated with the newly created trapezoidal block.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
err := control.UpdateTrapzBlock(context.Background(), "set_point", 10.0, []string{"set_point", "endpoint"}, loop)
```

### PIDLoop

`PIDLoop` is a struct containting all the attributes for setting up a PID control loop. [`SetupPIDControlConfig`](/internals/controls-package/#setuppidcontrolconfig) will create this object for you.

```go
type PIDLoop struct {
  BlockNames   map[string][]string
  PIDVals      []PIDConfig
  ControlConf  Config
  ControlLoop  *Loop
  Options      Options
  Controllable Controllable
}
```

### PIDConfig

`PIDConfig` is a struct containing the PID values for a control loop. With 2-dimensional control loops (such as a `sensor-controlled` base which controls both linear and angular velocity), the `"type"` type field is required and must be either `"linear_velocity"` or `"angular_velocity"`. For 1-dimensional control loops (such as an encoded motor), the `"type"` field is not necessary.

```go
type PIDConfig struct {
  Type string
  P    float64
  I    float64
  D    float64
}
```

### Controllable

`Controllable` is an interface that contains the two functions that any component needs to be controlled by a control loop. For any components other than an encoded motor and a sensor controlled base, these functions must be implemented on the component.

- `State()` gets the current state of the endpoint (controlled component) and passes that information on to the next iteration of the control loop
- `SetState()` takes the information from the latest iteration of the control loop and sets the state of the endpoint (controlled component) to the calculated value.

For example, in an encoded motor, `State()` measures the current position of the motor, so that the next iteration of the control loop knows how far it is from the goal position, or how much error remains. Then the control loop calculates what the next power percentage should be in order to get the motor to its goal position and velocity, and `SetState()` sets that power on the motor.

```go
type Controllable interface {
  SetState(ctx context.Context, state []*Signal) error
  State(ctx context.Context) ([]float64, error)
}
```

### Options

`Options` is a struct that contains all of the optional parameters that you can use to customize a control loop during the setup. Since they are all optional, the only options you must set are those that you wish to change from the default.

<!-- prettier-ignore -->
| Name | Type | Description |
| ---- | ---- | ----------- |
| `PositionControlUsingTrapz` | bool | Adds a trapezoidalVelocityProfile block to the control config to allow for position control of a component. <br> Default: false |
| `SensorFeedback2DVelocityControl` | bool | Adds linear and angular blocks to a control config in order to use the sensorcontrolled base component for velocity control. <br> Default: false |
| `DerivativeType` | string | The type of derivative to be used for the derivative block of a control config. <br> Default: `"backward1st1"` |
| `UseCustomConfig` | bool | Use this if the necessary config cannot be created using the control loop setup functions. <br> Default: false |
| `CompleteCustomConfig` | control.Config | The custom control config to be used instead of the config created by the control loop setup functions. <br> Default: control.Config{} |
| `NeedsAutoTuning` | bool | True when the loop needs to be auto-tuned. This will be set to true automatically if all PID values are 0. <br> Default: false |
| `LoopFrequency` | float64 | The frequency at which the control loop should run. <br> Default: 50 Hz |
| `ControllableType` | string | The type of component the control loop will be set up for, currently a base or motor. <br> Default: `"motor_name"` |

```go
type Options struct {
  PositionControlUsingTrapz bool
  SensorFeedback2DVelocityControl bool
  DerivativeType string
  UseCustomConfig bool
  CompleteCustomConfig Config
  NeedsAutoTuning bool
  LoopFrequency float64
  ControllableType string
}
```

The built in control loop setup is only structured to work with an encoded motor or a sensor controlled base. If you wish to use a different setup, you can use the options by setting `UseCustomConfig` to `true` and `CompleteCustomConfig` to your custom control loop config of type `control.Config`.
The [Control Blocks](/internals/controls-package/#control-blocks) section details the different options for control blocks and how to create a `control.Config`.

### BlockConfig

`BlockConfig` is a struct for the configuration of an individual control block.
You have to build individual BlockConfigs if you use the `UseCustomConfig` option.
Each block type requires different attributes, which are outlined in the [Control Blocks](/internals/controls-package/#control-blocks) section.

```go
type BlockConfig struct {
  Name      string
  Type      controlBlockType
  Attribute utils.AttributeMap
  DependsOn []string
}
```

## Control Blocks

The following example is a block diagram of a control loop defined to control the speed of a motor.
The motor has an encoder that reports the position of the motor.

Measuring the reported position and deriving it to get the speed introduces some error, so you may apply a filter to remove the noise.

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
For now, only DC motors with an encoder, and a base with a linear and angular movement sensor are supported as an endpoint in the control package.
You should change the _motor_name_ attribute to _base_name_ when using a base.

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

Several methods to calculate Kp, Ki and Kd are implemented:

- ziegerNicholsPI
- ziegerNicholsPID
- ziegerNicholsPD
- ziegerNicholsSomeOvershoot
- ziegerNicholsNoOvershoot
- cohenCoonsPI
- cohenCoonsPID
- tyreusLuybenPI
- tyreusLuybenPID

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

### Trapezoidal velocity profile generator

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

## Example

If you want to configure a control loop outside of the standard encoded motor or sensor-controlled base setup, you can create a custom config and tune it manually.

### Using SetupPIDControlConfig

The following is an example of how to manually set up and tune a control loop using the function [`SetupPIDControlConfig`](/internals/controls-package/#setuppidcontrolconfig):

```go
// set the necessary options for a component
options := control.Options{
  LoopFrequency:             100.0,
}

// create the controlParams from the PID valules
// in this example, all 0 PID values will result in auto-tuning
controlParams := []control.PIDConfig{{
  Type: "",
  P:    0.0,
  I:    0.0,
  D:    0.0,
}}

// auto tune motor if all ControlParameters are 0
if controlParams[0].NeedsAutoTuning() {
  options.NeedsAutoTuning = true
}

// use SetupPIDControlConfig to create the control config and tune the component if necessary
pidLoop, err := control.SetupPIDControlConfig(convertedControlParams, "comopnent", options, component, component.logger)
if err != nil {
  return err
}

// some attributes that may be of use after setup
controlLoopConfig := pidLoop.ControlConf
loop := pidLoop.ControlLoop
blockNames := pidLoop.BlockNames
```

### Using a Custom Control Config

The following is an example of how to manually set up and tune a control loop using the `UseCustomConfig` and `CompleteCustomConfig` options:

```go
// create a custom control config
controlConfig := control.Config {
  Blocks: []BlockConfig{
    {
      Name: "set_point",
      Type: blockConstant,
      Attribute: rdkutils.AttributeMap{
        "constant_val": 0.0,
      },
    },
    {
      Name: "sum",
      Type: blockSum,
      Attribute: rdkutils.AttributeMap{
        "sum_string": "+-",
      },
      DependsOn: []string{"set_point", "endpoint"},
    },
    {
      Name: "PID",
      Type: blockPID,
      Attribute: rdkutils.AttributeMap{
        "int_sat_lim_lo": -255.0,
        "int_sat_lim_up": 255.0,
        "kD":             pidVals.D,
        "kI":             pidVals.I,
        "kP":             pidVals.P,
        "limit_lo":       -255.0,
        "limit_up":       255.0,
        "tune_method":    "ziegerNicholsPI",
        "tune_ssr_value": 2.0,
        "tune_step_pct":  0.35,
      },
      DependsOn: []string{"sum"},
    },
    {
      Name: "endpoint",
      Type: blockEndpoint,
      Attribute: rdkutils.AttributeMap{
        controllableType: endpointName,
      },
      DependsOn: []string{"gain"},
    },
  },
  Frequency: 100.0,
}

// set the necessary options for your component
options := control.Options{
  UseCustomConfig:           true,
  CompleteCustomConfig:      controlConfig,
}

// create PID control parameters
controlParams := []control.PIDConfig{{
  Type: "",
  P:    0.0,
  I:    0.0,
  D:    0.0,
}}

// auto tune motor if all ControlParameters are 0
if controlParams[0].NeedsAutoTuning() {
  options.NeedsAutoTuning = true
}

// create PIDLoop struct
pidLoop = &control.PIDLoop{
  PIDVals:      controlParams,
  ControlConf:  controlConf,
  Options:      options,
  Controllable: component,
  logger:       component.logger,
}

// assign BlockNames
pidLoop.BlockNames = make(map[string][]string, len(pidLoop.ControlConf.Blocks))
for _, b := range pidLoop.ControlConf.Blocks {
  pidLoop.BlockNames[string(b.Type)] = append(pidLoop.BlockNames[string(b.Type)], b.Name)
}

// run tuning method on the component
cancelCtx, cancelFunc := context.WithCancel(context.Background())
err := pidLoop.TunePIDLoop(cancelCtx, cancelFunc)

// some attributes that may be of use after setup
controlLoopConfig := pidLoop.ControlConf
loop := pidLoop.ControlLoop
blockNames := pidLoop.BlockNames
```
