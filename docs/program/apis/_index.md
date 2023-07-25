---
title: "Interact with Resources with Viam's client SDKs"
linkTitle: "APIs"
weight: 20
type: "docs"
description: "Access and control your robot or fleet with the SDKs' client libraries for the resource and robot APIs."
icon: "/services/icons/sdk.svg"
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api"]
aliases:
  - "/program/sdks/"
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [Application Programming Interface (API)](https://en.wikipedia.org/wiki/API) described through [protocol buffers](https://developers.google.com/protocol-buffers).
You can think of this as a description of how you can interact with that resource.
Different models of resources implement the same API, which [Viam SDKs expose](/internals/robot-to-robot-comms/), allowing you to control different models of resource types with a consistent interface.

The API methods provided by the SDKs for each of these resource APIs wrap gRPC client requests to the robot when you execute your program, providing you a convenient interface for accessing information about and controlling the {{< glossary_tooltip term_id="resource" text="resources" >}} you have [configured](/manage/configuration/) on your robot.

## ResourceBase Methods

In the Python SDK, [the `ResourceBase` class](https://python.viam.dev/autoapi/viam/resource/base/index.html) defines a basic set of API methods that all child resources should provide for users.
In the other SDKs, resource APIs implement but do not inherit these base requirements.

`ResourceBase` methods include:

### FromRobot

Get a resource configured on a robot by `"name"`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot` [(RobotClient)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient): The robot.
- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The `name` of the resource.

**Returns:**

- [(Resource)](https://python.viam.dev/autoapi/viam/resource/base/index.html): The named resource if it exists on your robot.
For example, an [arm](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

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

- [(Resource)](https://pkg.go.dev/go.viam.com/rdk@v0.2.47/resource#Name): The named resource if it exists on your robot.
For example, an [arm](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

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

- [(Resource)](https://ts.viam.dev/interfaces/Resource.html): The named resource if it exists on your robot.
For example, an [ArmClient](https://ts.viam.dev/classes/ArmClient.html).

```typescript
const myArmClient = new VIAM.ArmClient(robot, "my_arm");
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/interfaces/Arm.html).

{{% /tab %}}
{{< /tabs >}}

### Name

{{% alert title="Info" color="info" %}}

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
| [Kinematics](/components/arm/#kinematics) | Get the kinematics information associated with the arm. |
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
| [GPIOPinByName](/components/board/#gpiopinbyname) | Get a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}. |
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

### Base Remote Control

Method Name | Description
----------- | -----------
[`Close`](/services/base-rc/#close) | Close out of all remote control related systems.
[`ControllerInputs`](/services/base-rc/#controllerinputs) | Get a list of inputs from the controller that is being monitored for that control mode.

### Data Manager

Method Name | Description
----------- | -----------
[`Sync`](/services/data/#sync) | Sync data stored on the robot to the cloud.

### Navigation

Method Name | Description
----------- | -----------
[`Mode`](/services/navigation/#mode) | Get the mode the service is operating in.
[`SetMode`](/services/navigation/#setmode) | Set the mode the service is operating in.
[`Location`](/services/navigation/#location) | Get the current location of the robot.
[`Waypoints`](/services/navigation/#waypoints) | Get an array of waypoints currently in the service's data storage.
[`AddWaypoint`](/services/navigation/#addwaypoint) | Add a waypoint to the service's data storage.
[`RemoveWaypoint`](/services/navigation/#removewaypoint) | Remove a waypoint from the service's data storage.

### Sensors

Method Name | Description
----------- | -----------
[`Sensors`](/services/sensors/#sensors) | Returns a list of names of the available sensors.
[`Readings`](/services/sensors/#readings) | Returns a list of readings from a given list of sensors.

### Motion

Method Name | Description
----------- | -----------
[`Move`](/services/motion/#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`MoveSingleComponent`](/services/motion/#movesinglecomponent) | Move a single component "manually."
[`GetPose`](/services/motion/#getpose) | Get the current location and orientation of a component.
[`MoveOnMap`](/services/motion/#moveonmap) | Move a component to a `Pose` in respect to the origin of a [SLAM](/services/slam/) map.
[`MoveOnGlobe`](/services/motion/#moveonglobe) | Move a component to a specific latitude and longitude, using a [Movement Sensor](/components/movement-sensor/) to determine the location.

### SLAM

Method Name | Description
----------- | -----------
[`GetPosition`](/services/slam/#getposition) | Get the current position of the specified source component in the point cloud SLAM map.
[`GetPointCloudMap`](/services/slam/#getpointcloudmap) | Get the point cloud SLAM map.
[`GetInternalState`](/services/slam/#getinternalstate) | Get the internal state of the SLAM algorithm required to continue mapping/localization.
[`GetLatestMapInfo`](/services/slam/#getlatestmapinfo) | Get the timestamp of the last update to the point cloud SLAM map.

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

## Robot API

The Robot API is the designated interface for a robot, the root of all robotic parts.
To interact with the Robot API with Viam's SDKs, instantiate a `RobotClient` ([gRPC](https://grpc.io/) client) and use that class for all interactions.

### DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` [(List [viam.proto.robot.DiscoveryQuery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery): A list of [tuples of API and model](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [(List[viam.proto.robot.Discovery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Discovery): The list of discovered component configurations corresponding to `queries`.

``` python
# Define a new discovery query.
q = robot.DiscoveryQuery(subtype=acme.API, model="some model")

# Define a list of discovery queries.
qs = [q]

# Get component configurations with these queries.
component_configs = await robot.discover_components(qs)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.discover_components)

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `qs` [([]resource.DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/resource#DiscoveryQuery): A list of [tuples of API and model](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [([]resource.Discovery)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/resource#Discovery): The search query `qs` and the corresponding list of discovered component configurations as an interface called `Results`.
`Results` may be comprised of primitives, a list of primitives, maps with string keys (or at least can be decomposed into one), or lists of the forementioned type of maps.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
// Define a new discovery query.
q := resource.NewDiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define a list of discovery queries.
qs := []resource.DiscoverQuery{q}

// Get component configurations with these queries.
component_configs, err := robot.DiscoverComponents(ctx.Background(), qs)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `queries` [(DiscoveryQuery[])](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html): An array of [tuples of API and model](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html#constructor) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [(Discovery[])](https://ts.viam.dev/classes/robotApi.Discovery.html): List of discovered component configurations.

```typescript
// Define a new discovery query.
const q = new proto.DiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define an array of discovery queries.
let qs:  proto.DiscoveryQuery[] = [q]

// Get the array of discovered component configurations.
const componentConfigs = await robot.discoverComponents(queries);
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

### FrameSystemConfig

Get the configuration of the Frame System of a given robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` [(Optional[List[viam.proto.common.Transform]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): A optional list of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- `frame_system` [(List[FrameSystemConfig])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig): The configuration of a given robot’s frame system.

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the robot.
frame_system = await robot.get_frame_system_config()
print(f"Frame System Configuration: {frame_system}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(framesystem.Config)](https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#Config): The configuration of the given robot’s frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Print the Frame System configuration
frameSystem, err := robot.FrameSystemConfig(context.Background(), nil)
fmt.Println(frameSystem)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `transforms` [(Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): An optional array of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- [(FrameSystemConfig[])](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html): An array of individual parts that make up a robot's frame system.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#frameSystemConfig).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the Frame System configuration.
console.log('FrameSytemConfig:', await robot.frameSystemConfig());
```

{{% /tab %}}
{{< /tabs >}}

### Status

Get the status of the resources on the robot.
You can provide a list of ResourceNames for which you want statuses.
If no names are passed in, the status of every resource configured on the robot is returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `resourceNames` [(Optional[List[viam.proto.common.ResourceName]])](https://docs.python.org/library/typing.html#typing.Optional): An optional list of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [(List[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): A list containing the status of each resource.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

```python {class="line-numbers linkable-line-numbers"}
# Get the status of the resources on the robot.
statuses = await robot.get_status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `resourceNames` [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): An optional list of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [([]Status)](https://pkg.go.dev/go.viam.com/rdk/robot#Status): Status of each resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
status, err = robot.Status(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `resourceNames` [(commonApi.ResourceName[])](https://ts.viam.dev/classes/commonApi.ResourceName.html): An optional array of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [(robotApi.Status[])](https://ts.viam.dev/classes/robotApi.Status.html): An array containing the status of each resource.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPCD).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
const status = await robot.getStatus();
```

{{% /tab %}}
{{< /tabs >}}

### Close

Close the underlying connections and stop any periodic tasks across all constituent parts of the robot.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.close).

```python {class="line-numbers linkable-line-numbers"}
# Cleanly close the underlying connections and stop any periodic tasks.
await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks,
err := robot.Close(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#disconnect).

```typescript {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks
await robot.disconnect();
```

{{% /tab %}}
{{< /tabs >}}

### StopAll

Cancel all current and outstanding operations for the robot and stop all actuators and movement.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Dict[viam.proto.common.ResourceName, Dict[str, Any]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): Any extra parameters to pass to the resources’ stop methods, keyed on each resource’s [`ResourceName`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName).

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.stop_all).

```python {class="line-numbers linkable-line-numbers"}
# Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stop_all()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[resource.Name]map[string]interface{})](https://pkg.go.dev/go.viam.com/rdk/resource#Name): Any extra parameters to pass to the resources’ stop methods, keyed on each resource’s [`Name`](https://pkg.go.dev/go.viam.com/rdk/resource#Name).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
err := robot.StopAll(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#stopAll).

```typescript {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stopAll();
```

{{% /tab %}}
{{< /tabs >}}

### ResourceNames

Get a list of all known resource names connected to this robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.common.ResourceName])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): List of all known resource names. A property of a [RobotClient](https://python.viam.dev/autoapi/viam/robot/client/index.html)

``` python
resource_names = robot.resource_names
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk@v0.2.47/resource#Name): List of all known resource names.

```go
resource_names := robot.ResourceNames()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(ResourceName.AsObject[])](https://ts.viam.dev/modules/commonApi.ResourceName-1.html): List of all known resource names.

```typescript
// Get a list of all resources on the robot.
const resource_names = await robot.resourceNames();
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}
