---
title: "Resource APIs with Viam's SDKs"
linkTitle: "For Resources"
weight: 40
type: "docs"
description: "Using built-in resource API methods to control the components and services on your robot with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

These methods provide a wrapper for your gRPC client requests to the endpoints the resource API provides for communication between your application and the robot server (`viam-server`) instance on the computer controlling your robot, providing you a convenient interface for accessing information about and controlling the {{< glossary_tooltip term_id="resource" text="resources" >}} you have [configured](/manage/configuration/) on your robot programmatically.

## Resource API

The Resource API is the base set of methods that all Resource APIs provide for users across the SDKs.

In the Python SDK this is a class that provides base requirements for all child resources: [the `ResourceBase` class](https://python.viam.dev/autoapi/viam/resource/base/index.html).
In the Go and TypeScript SDKs, each resource implements these methods within its own interface.

### FromRobot

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The `name` of the resource.

**Returns:**

- `robot` [(RobotClient)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient): The robot.
- `name` [(str)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): The "name" of the resource.

``` python
my_arm = Arm.from_robot(robot, "my_arm")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/resource/base/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `r` [(RobotClient)](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/robot#Robot): The robot.
- `name` [(string)](https://pkg.go.dev/builtin#string): The "name" of the resource.

**Returns:**

- [(Resource)](https://pkg.go.dev/go.viam.com/rdk@v0.2.47/resource#Name): Your named resource. For example, an [Arm](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
my_arm = arm.FromRobot(robot, "my_arm")
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#FromRobot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

In the TypeScript SDK, the equivalent of the `FromRobot` is defined in each resource API's client constructor.

For example, a component with [type `arm`](https://ts.viam.dev/classes/ArmClient.html) and name `my_arm` belonging to a robot `robot` is instantiated as follows:

**Parameters:**

- `client` [(RobotClient)](https://ts.viam.dev/classes/RobotClient.html): The robot.
- `name` [(string)](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html): The `name` of the resource.

**Returns:**

- [(Resource)](https://ts.viam.dev/interfaces/Resource.html): Your named resource. For example, an [ArmClient](https://ts.viam.dev/classes/ArmClient.html).

```typescript
const myArmClient = new VIAM.ArmClient(robot, "my_arm");
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/interfaces/Arm.html).

{{% /tab %}}
{{< /tabs >}}

### Name

{{% alert title="Note" color="note" %}}

An equivalent for `Name` is not currently provided by the TypeScript SDK.

{{% /alert %}}

Get the [`ResourceName`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName) of a resource with the configured `name`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The `name` of the resource.

**Returns:**

- `name` [(`proto.common.ResourceName`)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): The [`ResourceName`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName) of the resource, including string fields for the `namespace`, `type`, `subtype`, and `name`.

``` python
my_arm_name = my_arm.get_resource_name("my_arm")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/resource/base/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

Get the [`Name`](https://pkg.go.dev/go.viam.com/rdk/resource#Name) of the resource.

**Parameters:**

- None

**Returns:**

- `name` [(Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The [`Name`](https://pkg.go.dev/go.viam.com/rdk/resource#Name) of the resource, including fields for the `API` with `Type` and `SubtypeName`, and string `Remote` and `Name`.

``` go
MyArmName := MyArm.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

DoCommand sends commands containing arbitrary data to the resource.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(`Mapping[str, viam.utils.ValueTypes]`)](https://python.viam.dev/autoapi/viam/utils/index.html#viam.utils.ValueTypes): The command to execute.
- `timeout` [(`Optional[float]`)](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(`Mapping[str, viam.utils.ValueTypes]`)](https://python.viam.dev/autoapi/viam/utils/index.html#viam.utils.ValueTypes): The result of the executed command.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/resource/base/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](<https://go.dev/blog/maps>): The command to execute.

**Returns:**

- [(map[string]interface{})](<https://go.dev/blog/maps>): The result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` [(StructType)](https://ts.viam.dev/types/StructType.html): The command to execute.

**Returns:**

- [(StructType)](https://ts.viam.dev/types/StructType.html): The result of the executed command.

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/interfaces/Resource.html).

{{% /tab %}}
{{< /tabs >}}

## Component APIs

These APIs provide interfaces for controlling and getting information from various components of a robot.
Built-in API methods are defined for every model of each component type.
Documentation on using these methods in your SDK code is found on each [component page](/components/) as follows:

### Arm

The arm component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [GetEndPosition](/components/arm/#getendposition) | Get the current position of the arm as a Pose. |
| [MoveToPosition](/components/arm/#movetoposition) | Move the end of the arm to the desired Pose. |
| [MoveToJointPositions](/components/arm/#movetojointpositions) | Move each joint on the arm to the desired position. |
| [JointPositions](/components/arm/#jointpositions) | Get the current position of each joint on the arm. |
| [Stop](/components/arm/#stop) | Stop the arm from moving. |
| [IsMoving](/components/arm/#ismoving) | Get if the arm is currently moving. |
| [DoCommand](/components/arm/#docommand) | Send or receive model-specific commands. |

### Base

The base component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [MoveStraight](/components/base/#movestraight)  | Move the base in a straight line across the given distance at the given velocity. |
| [Spin](/components/base/#spin) | Move the base to the given angle at the given angular velocity. |
| [SetPower](/components/base/#setpower) | Set the relative power (out of max power) for linear and angular propulsion of the base. |
| [SetVelocity](/components/base/#setvelocity) | Set the linear velocity and angular velocity of the base. |
| [Stop](/components/base/#stop) | Stop the base. |
| [DoCommand](/components/base/#docommand) | Send or receive model-specific commands. |

### Board

The board component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [AnalogReaderByName](/components/board/#analogreaderbyname) | Get an [`AnalogReader`](/components/board/#analogs) by `name`. |
| [DigitalInterruptByName](/components/board/#digitalinterruptbyname) | Get a [`DigitalInterrupt`](/components/board/#digital_interrupts) by `name`. |
| [GPIOPinByName](/components/board/#gpiopinbyname) | Get a `GPIOPin` by its [pin number](/appendix/glossary/#term-pin-number). |
| [AnalogReaderNames](/components/board/#analogreadernames) | Get the `name` of every [`AnalogReader`](/components/board/#analogs). |
| [DigitalInterruptNames](/components/board/#digitalinterruptnames) | Get the `name` of every [`DigitalInterrupt`](/components/board/#digital_interrupts). |
| [Status](/components/board/#status) | Get the current status of this board. |
| [ModelAttributes](/components/board/#modelattributes) | Get the attributes related to the model of this board. |
| [SetPowerMode](/components/board/#setpowermode) | Set the board to the indicated power mode. |

### Camera

| Method Name | Description |
| ----------- | ----------- |
| [GetImage](/components/camera/#getimage) | Return an image from the camera. |
| [GetPointCloud](/components/camera/#getpointcloud) | Return a point cloud from the camera. |
| [GetProperties](/components/camera/#getproperties) | Return the camera intrinsic and camera distortion parameters, as well as whether the camera supports returning point clouds. |

### Encoder

Method Name | Description
----------- | -----------
[Position](/components/encoder/#position) | Get the current position of the encoder.
[ResetPosition](/components/encoder/#resetposition) | Reset the position to zero.
[GetProperties](/components/encoder/#getproperties) | Get the supported properties of this encoder.

### Gantry

| Method Name | Description |
| ----------- | ----------- |
[Position](/components/gantry/#position) | Get the current positions of the axes of the gantry in mm. |
[MoveToPosition](/components/gantry/#movetoposition) | Move the axes of the gantry to the desired positions. |
[Lengths](/components/gantry/#lengths) | Get the lengths of the axes of the gantry in mm. |
[Stop](/components/gantry/#stop) | Stop the gantry from moving. |
[IsMoving](/components/gantry/#ismoving) | Get if the gantry is currently moving. |

### Gripper

Method Name | Description
----------- | -----------
[`Open`](/components/gripper/#open) | Open the gripper.
[`Grab`](/components/gripper/#grab) | Close the gripper until it grabs something or closes completely.
[`Stop`](/components/gripper/#stop) | Stop the gripper's movement.
[`IsMoving`](/components/gripper/#ismoving) | Report whether the gripper is currently moving.

### Input Controller

| Method Name | Description |
| ----------- | ----------- |
| [Controls](/components/input-controller/#controls) | Get a list of input `Controls` that this Controller provides. |
| [Events](/components/input-controller/#events) | Get the current state of the Controller as a map of the most recent [Event](/components/input-controller/#event-object) for each [Control](/components/input-controller/#control-field). |
| [RegisterControlCallback](/components/input-controller/#registercontrolcallback) | Define a callback function to execute whenever one of the [`EventTypes`](/components/input-controller/#eventtype-field) selected occurs on the given [Control](/components/input-controller/#control-field). |

### Motor

Method Name | Description
----------- | -----------
[SetPower](/components/motor/#setpower) | Set the power to send to the motor as a portion of max power.
[GoFor](/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified RPM.
[GoTo](/components/motor/#goto) | Send the motor to a specified position (in terms of revolutions from home) at a specified speed.
[ResetZeroPosition](/components/motor/#resetzeroposition) | Set the current position to be the new zero (home) position.
[GetPosition](/components/motor/#getposition) | Report the position of the motor based on its encoder. Not supported on all motors.
[GetProperties](/components/motor/#getproperties) | Return whether or not the motor supports certain optional features.
[Stop](/components/motor/#stop) | Cut power to the motor off immediately, without any gradual step down.
[IsPowered](/components/motor/#ispowered) | Return whether or not the motor is currently on, and the amount of power to it.
[IsMoving](/components/motor/#ismoving) | Return whether the motor is moving or not.

### Movement Sensor

Method Name | Description |
----------- | ----------- |
[GetPosition](/components/movement-sensor/#getposition) | Get the current latitude, longitude and altitude. |
[GetLinearVelocity](/components/movement-sensor/#getlinearvelocity) | Get the current linear velocity as a 3D vector. |
[GetAngularVelocity](/components/movement-sensor/#getangularvelocity) | Get the current angular velocity as a 3D vector. |
[GetLinearAcceleration](/components/movement-sensor/#getlinearacceleration) | Get the current linear acceleration as a 3D vector. |
[GetCompassHeading](/components/movement-sensor/#getcompassheading) | Get the current compass heading in degrees. |
[GetOrientation](/components/movement-sensor/#getorientation) | Get the current orientation. |
[GetProperties](/components/movement-sensor/#getproperties) | Get the supported properties of this sensor. |
[GetAccuracy](/components/movement-sensor/#getaccuracy) | Get the accuracy of the various sensors. |
[GetReadings](/components/movement-sensor/#getreadings) | Obtain the measurements/data specific to this sensor. |

### Sensor

| Method Name | Description |
| ----------- | ----------- |
| [Readings](/components/sensor/#readings) | Get the measurements or readings that this sensor provides. |

### Servo

| Method Name | Description |
| ----------- | ----------- |
| [Move](/components/servo/#move) | Move the servo to the desired angle. |
| [Position](/components/servo/#position) | Get the current angle of the servo. |
| [Stop](/components/servo/#stop) | Stop the servo. |

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a robot.
Built-in API methods are defined for each service implementation.
Documentation on using these methods in your SDK code is found on [service pages](/services/) as follows:

### Motion

Method Name | Description
----------- | -----------
[`Move`](/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`MoveSingleComponent`](/services/motion/#movesinglecomponent) | Move a single component "manually."
[`GetPose`](/services/motion/#getpose) | Get the current location and orientation of a component.

### SLAM

Method Name | Description
----------- | -----------
`Position` | Get current position of the specified component in the SLAM Map.
`PointCloudMap`| Get the point cloud map.
`InternalState` | Get the internal state of the SLAM algorithm required to continue mapping/localization.

### MLModel

Method Name | Description
----------- | -----------
`Infer` | Take an already ordered input tensor as an array, make an inference on the model, and return an output tensor map.
`Metadata`| Get the metadata (such as name, type, expected tensor/array shape, inputs, and outputs) associated with the ML model.

### Vision

Method Name | Description |
----------- | ----------- |
`DetectionsFromCamera` | Get a list of detections in the next image given a camera and a detector. |
`Detections`| Get a list of detections in the given image using the specified detector. |
`ClassificationsFromCamera` | Get a list of classifications in the next image given a camera and a classifier. |
`Classifications` | Get a list of detections in the given image using the specified detector. |
`ObjectPointClouds`| Returns a list of the 3D point cloud objects and associated metadata in the latest picture obtained from the specified 3D camera (using the specified segmenter). |

## Signaling APIs

### GPIO Pins

In addition to the [Board API](#board), the [board component](/components/board/) supports the following methods for interfacing with GPIO Pins on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Set](/components/board/#set) | Set the output of this pin to high/low. |
| [Get](/components/board/#get) | Get if this pin is active (high). |
| [PWM](/components/board/#pwm) | Get the pin’s pulse-width modulation duty cycle. |
| [SetPWM](/components/board/#pwmfreq) | Set the pin’s pulse-width modulation duty cycle. |
| [PWMFreq](/components/board/#pwmfreq) | Get the pulse-width modulation frequency of this pin. |
| [SetPWMFreq](/components/board/#setpwmfreq) | Set the pulse-width modulation frequency of this pin. |

### Analog-to-Digital Converters (ADCs)

In addition to the [Board API](#board), the [board component](/components/board/) supports the following methods for interfacing with [ADCs](/components/board/#analogs) on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Read](/components/board/#read) | Read the current integer value of the digital signal output by the ADC. |

### Digital Interrupts

In addition to the [Board API](#board), the [board component](/components/board/) supports the following methods for interfacing with [digital interrupts](/components/board/#digital_interrupts)  on a board:

| Method Name | Description |
| ----------- | ----------- |
| [Value](/components/board/#value) | Get the current value of this interrupt. |
| [Tick](/components/board/#tick) | Record an interrupt. |
| [AddCallback](/components/board/#addcallback) | Add a channel as a callback for [Tick()](/components/board/#tick). |
| [AddPostProcessor](/components/board/#addpostprocessor) | Add a PostProcessor function for [Value()](/components/board/#value). |
