---
linkTitle: "Control package"
title: "Control package"
weight: 60
type: "docs"
layout: "docs"
description: "The control package implements PID feedback control loops for encoded motors, sensor-controlled bases, and custom components."
date: "2022-01-01"
no_list: true
aliases:
  - /operate/reference/controls-package/
  - /internals/controls-package/
---

[Encoded motors](/reference/components/motor/encoded-motor/) and [sensor-controlled bases](/reference/components/base/sensor-controlled/) use a control loop implemented by `viam-server`.
You can configure the `control_parameters` attribute for both component types to adjust the control loop.

If you need to change or customize the control loops beyond the configurable parameters, or you want to add a control loop to a different component, you can use the `control` package from the RDK to [build your own PID control loop](#creating-and-using-a-pid-control-loop).

The control package implements feedback control on an endpoint, which is usually the hardware you are trying to control.
With the control package, you can design a control loop that monitors a process variable (PV) and compares it with a set point (SP).
The control loop generates a control action to reduce the error value between the SP and PV (_SP - PV_) to zero.

Control loops are represented in a diagrammatic style known as a block diagram.
Each block represents a transfer function of a component.
The control loop is broken down into successive "blocks" connected by their dependencies.

## Creating and using a PID control loop

A PID control loop computes a correction for the error value between SP and PV using three terms:

- A _proportional_ term that is the current error
- An _integral_ term that is the total cumulative error
- A _derivative_ term that is the rate of change of the error

By tuning the coefficients on each of these terms, you can adjust how your system converges towards the target value, how quickly it reaches the target, and how much it overshoots.

The following functions are available for creating and using a control loop:

<!-- prettier-ignore -->
| Function | Description |
| -------- | ----------- |
| [`SetupPIDControlConfig`](#setuppidcontrolconfig) | Creates a [`PIDLoop`](#pidloop) that contains all the necessary attributes to run a control loop based on the specified [`Options`](#options). |
| [`TunePIDLoop`](#tunepidloop) | Runs auto-tuning to find optimal PID values for the loop. |
| [`StartControlLoop`](#startcontrolloop) | Starts the control loop in a background thread. |
| [`CreateConstantBlock`](#createconstantblock) | Creates a control block of type `constant`. All control loops need at least one constant block representing the set point. |
| [`UpdateConstantBlock`](#updateconstantblock) | Updates the value of a constant block to the new set point. |
| [`CreateTrapzBlock`](#createtrapzblock) | Creates a control block of type `trapezoidalVelocityProfile`. Control loops that control position (for example, encoded motors) need a trapezoidal velocity profile block. |
| [`UpdateTrapzBlock`](#updatetrapzblock) | Updates the attributes of a trapezoidal velocity profile block to a new max velocity. |

### SetupPIDControlConfig

Creates a [`PIDLoop`](#pidloop) object, which contains all the attributes related to a control loop that a controlled component needs, including the control config.
If all PID values are zero and `NeedsAutoTuning` is set, the loop runs auto-tuning on creation.

**Parameters:**

- `pidVals` [(`[]PIDConfig`)](#pidconfig): The P, I, and D values for the control loop. If all are zero and `NeedsAutoTuning` is true, the loop auto-tunes and logs the calculated values.
- `componentName` [(`string`)](https://pkg.go.dev/builtin#string): The name of the component that the PID loop controls.
- `options` [(`Options`)](#options): Optional parameters to customize the control loop.
- `c` [(`Controllable`)](#controllable): An interface that contains the functions to move the controlled component.
- `logger` (`logging.Logger`): The logger of the controlled component.

**Returns:**

- [(`*PIDLoop`)](#pidloop): A pointer to a struct containing all relevant control loop attributes.
- [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

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

pidLoop, err := control.SetupPIDControlConfig(pidVals, "motor_name", options, motor, motor.logger)
```

### TunePIDLoop

Runs auto-tuning on the control loop to determine optimal PID values.
Tuning runs in a background goroutine.
When tuning completes, the component logs the calculated PID values and returns a `TunedPIDErr` prompting you to copy the values into your config.

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A context for the tuning operation.
- `cancelFunc` [(`CancelFunc`)](https://pkg.go.dev/context#CancelFunc): A cancel function to stop tuning.

**Returns:**

- [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
cancelCtx, cancelFunc := context.WithCancel(context.Background())
err := pidLoop.TunePIDLoop(cancelCtx, cancelFunc)
```

### StartControlLoop

Starts running the PID control loop in a background thread to monitor and adjust the inputs to the controlled component.

**Parameters:**

- None

**Returns:**

- [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
err := pidLoop.StartControlLoop()
```

### CreateConstantBlock

Creates a new control block of type `constant`.

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A context for the operation.
- `name` [(`string`)](https://pkg.go.dev/builtin#string): The name of the constant block.
- `constVal` [(`float64`)](https://pkg.go.dev/builtin#float64): The value of the new set point.

**Returns:**

- [(`BlockConfig`)](#blockconfig): The config for the newly created block.

```go
constBlock := control.CreateConstantBlock(context.Background(), "set_point", 10.0)
```

### UpdateConstantBlock

Creates a new constant block and updates the running control loop to use it.

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A context for the operation.
- `name` [(`string`)](https://pkg.go.dev/builtin#string): The name of the constant block.
- `constVal` [(`float64`)](https://pkg.go.dev/builtin#float64): The value of the new set point.
- `loop` (`*Loop`): The running control loop to update.

**Returns:**

- [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
err := control.UpdateConstantBlock(context.Background(), "set_point", 10.0, loop)
```

### CreateTrapzBlock

Creates a new control block of type `trapezoidalVelocityProfile`.

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A context for the operation.
- `name` [(`string`)](https://pkg.go.dev/builtin#string): The name of the trapezoidal block.
- `maxVel` [(`float64`)](https://pkg.go.dev/builtin#float64): The max velocity for the controlled component.
- `dependsOn` [(`[]string`)](https://pkg.go.dev/builtin#string): The names of the other control blocks that this block depends on. Usually the set point and the endpoint.

**Returns:**

- [(`BlockConfig`)](#blockconfig): The config for the newly created block.

```go
trapzBlock := control.CreateTrapzBlock(
  context.Background(), "trapz", 4000.0, []string{"set_point", "endpoint"},
)
```

### UpdateTrapzBlock

Creates a new trapezoidal velocity profile block and updates the running control loop to use it.

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A context for the operation.
- `name` [(`string`)](https://pkg.go.dev/builtin#string): The name of the trapezoidal block.
- `maxVel` [(`float64`)](https://pkg.go.dev/builtin#float64): The max velocity for the controlled component. Must be non-zero.
- `dependsOn` [(`[]string`)](https://pkg.go.dev/builtin#string): The names of the other control blocks that this block depends on.
- `loop` (`*Loop`): The running control loop to update.

**Returns:**

- [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
err := control.UpdateTrapzBlock(
  context.Background(), "trapz", 4000.0, []string{"set_point", "endpoint"}, loop,
)
```

## Data types

### PIDLoop

`PIDLoop` contains all the attributes for setting up a PID control loop.
[`SetupPIDControlConfig`](#setuppidcontrolconfig) creates this struct for you.

```go
type PIDLoop struct {
  BlockNames   map[string][]string
  PIDVals      []PIDConfig
  TunedVals    *[]PIDConfig
  ControlConf  *Config
  ControlLoop  *Loop
  Options      Options
  Controllable Controllable
}
```

| Field          | Type                  | Description                                                    |
| -------------- | --------------------- | -------------------------------------------------------------- |
| `BlockNames`   | `map[string][]string` | Maps block type names to the names of all blocks of that type. |
| `PIDVals`      | `[]PIDConfig`         | The PID values for the control loop.                           |
| `TunedVals`    | `*[]PIDConfig`        | Stores auto-tuned PID values after tuning completes.           |
| `ControlConf`  | `*Config`             | The full control loop configuration.                           |
| `ControlLoop`  | `*Loop`               | The running control loop instance, or `nil` if not started.    |
| `Options`      | `Options`             | The options used to create this loop.                          |
| `Controllable` | `Controllable`        | The component interface being controlled.                      |

### PIDConfig

`PIDConfig` holds the PID values for a control loop.
For 2-dimensional control loops (such as a sensor-controlled base which controls both linear and angular velocity), the `Type` field is required and must be either `"linear_velocity"` or `"angular_velocity"`.
For 1-dimensional control loops (such as an encoded motor), the `Type` field is not necessary.

```go
type PIDConfig struct {
  Type string  `json:"type,omitempty"`
  P    float64 `json:"p"`
  I    float64 `json:"i"`
  D    float64 `json:"d"`
}
```

### Controllable

`Controllable` is an interface that any component must implement to be controlled by a control loop.
Encoded motors and sensor-controlled bases already implement this interface.

- `State()` gets the current state of the endpoint (controlled component) and passes that information to the next iteration of the control loop.
- `SetState()` takes the output from the latest iteration of the control loop and sets the state of the endpoint.

For example, in an encoded motor, `State()` measures the current position of the motor so the next iteration knows how far it is from the goal.
The control loop calculates the next power percentage, and `SetState()` applies that power to the motor.

```go
type Controllable interface {
  SetState(ctx context.Context, state []*Signal) error
  State(ctx context.Context) ([]float64, error)
}
```

### Options

`Options` contains optional parameters for customizing a control loop.
All fields have defaults, so you only need to set the ones you want to change.

<!-- prettier-ignore -->
| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `PositionControlUsingTrapz` | `bool` | `false` | Adds a `trapezoidalVelocityProfile` block for position control. |
| `SensorFeedback2DVelocityControl` | `bool` | `false` | Adds linear and angular blocks for sensor-controlled base velocity control. |
| `DerivativeType` | `string` | `"backward1st1"` | The finite difference method for the derivative block. Options: `"backward1st1"`, `"backward1st2"`, `"backward1st3"`. |
| `UseCustomConfig` | `bool` | `false` | Set to `true` to use `CompleteCustomConfig` instead of the auto-generated config. |
| `CompleteCustomConfig` | `Config` | `Config{}` | A custom control config. Only used when `UseCustomConfig` is `true`. |
| `NeedsAutoTuning` | `bool` | `false` | Set to `true` when all PID values are 0 and the loop should auto-tune. Set automatically when all PID values are 0. |
| `LoopFrequency` | `float64` | `50.0` | The frequency (Hz) at which the control loop runs. |
| `ControllableType` | `string` | `"motor_name"` | The type of component. Set to `"base_name"` when controlling a base. |

```go
type Options struct {
  PositionControlUsingTrapz           bool
  SensorFeedback2DVelocityControl     bool
  DerivativeType                      string
  UseCustomConfig                     bool
  CompleteCustomConfig                Config
  NeedsAutoTuning                     bool
  LoopFrequency                       float64
  ControllableType                    string
}
```

The built-in control loop setup works with encoded motors and sensor-controlled bases.
To use a different setup, set `UseCustomConfig` to `true` and `CompleteCustomConfig` to your custom `Config`.
See [Control blocks](#control-blocks) for how to build individual blocks.

### BlockConfig

`BlockConfig` is the configuration for an individual control block.
You need to build `BlockConfig` structs when using the `UseCustomConfig` option.
Each block type requires different attributes, documented in [Control blocks](#control-blocks).

```go
type BlockConfig struct {
  Name      string             `json:"name"`
  Type      controlBlockType   `json:"type"`
  Attribute utils.AttributeMap `json:"attributes"`
  DependsOn []string           `json:"depends_on"`
}
```

### Config

`Config` is the top-level control loop configuration containing a list of blocks and a loop frequency.

```go
type Config struct {
  Blocks    []BlockConfig `json:"blocks"`
  Frequency float64       `json:"frequency"`
}
```

## Control blocks

The following example is a block diagram of a control loop that controls the speed of a motor.
The motor has an encoder that reports its position.
The position is derived to get speed, then filtered to remove noise.
The error (_SP - PV_) is fed into the PID controller, which outputs a correction through a gain block to the endpoint.

```text
+-------------+       +----------+       +----------+       +----------+
|  SetPoint   +------>|   Sum    +------>|   PID    +------>| Endpoint |
| (constant)  |       |          |       |          |       |  (motor) |
+-------------+       +-----^----+       +----------+       +----+-----+
                             |                                    |
                       +-----+----+       +----------+            |
                       |  Filter  |<------+ Derive   |<-----------+
                       |          |       |          |
                       +----------+       +----------+
```

The `frequency` field in the control config sets how often the loop runs (in Hz).
Higher frequencies produce smaller errors at each step and smoother control.

### Common block fields

All blocks share these fields:

- `name`: A unique name used to reference the block in `depends_on` lists.
- `type`: The block type (see supported types below).
- `attributes`: Type-specific configuration.
- `depends_on`: List of block names this block takes input from.

### Gain

Multiplies the input signal by a constant gain value: `S_out = S_in * gain`.

```json
{
  "name": "gain",
  "type": "gain",
  "attributes": {
    "gain": 0.00392156862
  },
  "depends_on": ["PID"]
}
```

The default gain of `0.00392156862` (1/255) scales the PID output to a 0-1 PWM range for standard 8-bit PWM boards.

### Constant

Outputs a constant signal value, typically used as the set point: `S_out = constant_val`.

```json
{
  "name": "set_point",
  "type": "constant",
  "attributes": {
    "constant_val": 0.0
  }
}
```

### Endpoint

Represents the physical hardware being controlled.
The endpoint reads state from the hardware and applies control outputs to it.

Set the attribute key to `"motor_name"` for motors or `"base_name"` for bases.

```json
{
  "name": "endpoint",
  "type": "endpoint",
  "attributes": {
    "motor_name": "my-motor"
  },
  "depends_on": ["gain"]
}
```

### PID

The PID block computes a correction from the error signal using proportional, integral, and derivative terms:

`u(t) = Kp * e(t) + Ki * integral(e(t)) * dt + Kd * (de(t)/dt)`

Where Kp, Ki, and Kd are the PID gains, e(t) is the error at time t, and dt is the time between steps.

The `PIDSets` attribute takes an array of [`PIDConfig`](#pidconfig) objects.
Use one PID set for single-axis control (encoded motor) or two for dual-axis control (sensor-controlled base with linear and angular velocity).

```json
{
  "name": "PID",
  "type": "PID",
  "attributes": {
    "PIDSets": [{ "p": 1.0, "i": 0.5, "d": 0.0 }],
    "limit_up": 255.0,
    "limit_lo": -255.0,
    "int_sat_lim_up": 255.0,
    "int_sat_lim_lo": -255.0,
    "tune_ssr_value": 2.0,
    "tune_method": "ziegerNicholsPI",
    "tune_step_pct": 0.35
  },
  "depends_on": ["sum"]
}
```

<!-- prettier-ignore -->
| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `PIDSets` | `[]*PIDConfig` | Array of PID gain configurations. One per axis of control. |
| `limit_up` | `float64` | Maximum PID output value. Default: `255.0`. |
| `limit_lo` | `float64` | Minimum PID output value. Default: `0.0`. |
| `int_sat_lim_up` | `float64` | Upper integral anti-windup limit. Default: `255.0`. |
| `int_sat_lim_lo` | `float64` | Lower integral anti-windup limit. Default: `0.0`. |
| `tune_ssr_value` | `float64` | Threshold for detecting steady state during auto-tuning. Sensible range: 1.0 to 2.0. |
| `tune_method` | `string` | Auto-tuning method. Default: `"ziegerNicholsPID"`. See [tuning methods](#tuning-methods). |
| `tune_step_pct` | `float64` | Step size as a fraction of the output range for auto-tuning relay tests. |

#### Tuning methods

To auto-tune, set all PID values to 0.
The control loop records the step response and uses the relay method to estimate the ultimate gain (Ku) and oscillation period (Tu), then calculates gains using the selected method:

| Method                       | Description                            |
| ---------------------------- | -------------------------------------- |
| `ziegerNicholsPI`            | Ziegler-Nichols PI tuning              |
| `ziegerNicholsPID`           | Ziegler-Nichols PID tuning (default)   |
| `ziegerNicholsPD`            | Ziegler-Nichols PD tuning              |
| `ziegerNicholsSomeOvershoot` | Ziegler-Nichols with reduced overshoot |
| `ziegerNicholsNoOvershoot`   | Ziegler-Nichols with no overshoot      |
| `cohenCoonsPI`               | Cohen-Coons PI tuning                  |
| `cohenCoonsPID`              | Cohen-Coons PID tuning                 |
| `tyreusLuybenPI`             | Tyreus-Luyben PI tuning                |
| `tyreusLuybenPID`            | Tyreus-Luyben PID tuning               |

### Encoder to RPM

Converts encoder counts to RPM using the pulses-per-revolution value of the encoder.

```json
{
  "name": "encoder_to_rpm",
  "type": "encoderToRpm",
  "attributes": {
    "PulsesPerRevolution": 14
  },
  "depends_on": ["endpoint"]
}
```

### Sum

Sums input signals according to a `sum_string` that specifies the sign of each input.
Each character is `+` or `-`, one per dependency in order.

```json
{
  "name": "sum",
  "type": "sum",
  "attributes": {
    "sum_string": "+-"
  },
  "depends_on": ["set_point", "endpoint"]
}
```

In this example, the output is `set_point - endpoint`, computing the error between the desired and actual values.

### Trapezoidal velocity profile

Position control of a motor can use a trapezoidal velocity profile generator.
When a new set point arrives, this block generates a velocity profile with three phases: acceleration, constant speed, and deceleration.

The profile is dynamically adjusted during deceleration to keep the end position within the position window.
The block also acts as a deadband controller when the target position is reached, preventing the motor from moving outside the window.

```json
{
  "name": "trapz",
  "type": "trapezoidalVelocityProfile",
  "attributes": {
    "max_vel": 4000.0,
    "max_acc": 30000.0,
    "pos_window": 10.0,
    "kpp_gain": 0.45
  },
  "depends_on": ["set_point", "endpoint"]
}
```

<!-- prettier-ignore -->
| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `max_vel` | `float64` | Maximum velocity. |
| `max_acc` | `float64` | Maximum acceleration. |
| `pos_window` | `float64` | Deadband window around the target position. |
| `kpp_gain` | `float64` | Proportional gain for position error in the deadband controller. |

### Derivative

Computes the derivative of the input signal using a finite difference method.

```json
{
  "name": "derivative",
  "type": "derivative",
  "attributes": {
    "derive_type": "backward1st1"
  },
  "depends_on": ["endpoint"]
}
```

| Attribute     | Type     | Description                                                                                                                                              |
| ------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `derive_type` | `string` | The finite difference method. Options: `"backward1st1"`, `"backward1st2"`, `"backward1st3"`. Higher orders use more past samples for smoother estimates. |

### Filter

Applies a digital filter to the input signal to remove noise.
Supports FIR (finite impulse response) and IIR (infinite impulse response) filters.

```json
{
  "name": "filter",
  "type": "filter",
  "attributes": {
    "filter_type": "lowpass"
  },
  "depends_on": ["derivative"]
}
```

## Examples

### Using SetupPIDControlConfig

Set up and tune a control loop using [`SetupPIDControlConfig`](#setuppidcontrolconfig):

```go
// Set the options for your component
options := control.Options{
  LoopFrequency: 100.0,
}

// Create PID values. All zeros triggers auto-tuning.
controlParams := []control.PIDConfig{{
  Type: "",
  P:    0.0,
  I:    0.0,
  D:    0.0,
}}

// Enable auto-tuning if all PID values are 0
if controlParams[0].NeedsAutoTuning() {
  options.NeedsAutoTuning = true
}

// Create the control config and tune if necessary
pidLoop, err := control.SetupPIDControlConfig(
  controlParams, "component", options, component, component.logger,
)
if err != nil {
  return err
}

// Useful attributes after setup
controlLoopConfig := pidLoop.ControlConf
loop := pidLoop.ControlLoop
blockNames := pidLoop.BlockNames
```

### Using a custom control config

Set up a control loop with a custom block configuration using the `UseCustomConfig` and `CompleteCustomConfig` options:

```go
// Create a custom control config
controlConfig := control.Config{
  Blocks: []control.BlockConfig{
    {
      Name: "set_point",
      Type: "constant",
      Attribute: rdkutils.AttributeMap{
        "constant_val": 0.0,
      },
    },
    {
      Name: "sum",
      Type: "sum",
      Attribute: rdkutils.AttributeMap{
        "sum_string": "+-",
      },
      DependsOn: []string{"set_point", "endpoint"},
    },
    {
      Name: "PID",
      Type: "PID",
      Attribute: rdkutils.AttributeMap{
        "int_sat_lim_lo": -255.0,
        "int_sat_lim_up": 255.0,
        "PIDSets":        []*control.PIDConfig{{P: 1.0, I: 0.5, D: 0.0}},
        "limit_lo":       -255.0,
        "limit_up":       255.0,
        "tune_method":    "ziegerNicholsPI",
        "tune_ssr_value": 2.0,
        "tune_step_pct":  0.35,
      },
      DependsOn: []string{"sum"},
    },
    {
      Name: "gain",
      Type: "gain",
      Attribute: rdkutils.AttributeMap{
        "gain": 0.00392156862,
      },
      DependsOn: []string{"PID"},
    },
    {
      Name: "endpoint",
      Type: "endpoint",
      Attribute: rdkutils.AttributeMap{
        "motor_name": "my-motor",
      },
      DependsOn: []string{"gain"},
    },
  },
  Frequency: 100.0,
}

// Set the options to use the custom config
options := control.Options{
  UseCustomConfig:      true,
  CompleteCustomConfig: controlConfig,
}

// Create PID parameters for auto-tuning
controlParams := []control.PIDConfig{{
  Type: "",
  P:    0.0,
  I:    0.0,
  D:    0.0,
}}

if controlParams[0].NeedsAutoTuning() {
  options.NeedsAutoTuning = true
}

// Create and configure the PID loop
pidLoop, err := control.SetupPIDControlConfig(
  controlParams, "my-motor", options, component, component.logger,
)
if err != nil {
  return err
}

// Useful attributes after setup
controlLoopConfig := pidLoop.ControlConf
loop := pidLoop.ControlLoop
blockNames := pidLoop.BlockNames
```
