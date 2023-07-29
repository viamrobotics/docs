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

In the Python SDK, the [`ResourceBase`](https://python.viam.dev/autoapi/viam/resource/base/index.html) class defines a basic set of API methods that all child resources should provide for users.
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

- `r` [(RobotClient)](https://pkg.go.dev/go.viam.com/rdk/robot#Robot): The robot.
- `name` [(string)](https://pkg.go.dev/builtin#string): The "name" of the resource.

**Returns:**

- [(Resource)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The named resource if it exists on your robot.
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

The [arm component](/components/arm/) supports the following methods:

{{< readfile "/static/include/components/apis/arm.md" >}}

### Base

The [base component](/components/base/) supports the following methods:

{{< readfile "/static/include/components/apis/base.md" >}}

### Board

The [board component](/components/board/) supports the following methods:

{{< readfile "/static/include/components/apis/board.md" >}}

### Camera

The [camera component](/components/camera/) supports the following methods:

{{< readfile "/static/include/components/apis/camera.md" >}}

### Encoder

The [encoder component](/components/encoder/) supports the following methods:

{{< readfile "/static/include/components/apis/encoder.md" >}}

### Gantry

The [gantry component](/components/gantry/) supports the following methods:

{{< readfile "/static/include/components/apis/gantry.md" >}}

### Gripper

The [gripper component](/components/gripper/) supports the following methods:

{{< readfile "/static/include/components/apis/gripper.md" >}}

### Input Controller

The [input controller component](/components/input-controller/) supports the following methods:

{{< readfile "/static/include/components/apis/input-controller.md" >}}

### Motor

The [motor component](/components/motor/) supports the following methods:

{{< readfile "/static/include/components/apis/motor.md" >}}

### Movement Sensor

The [movement sensor component](/components/movement-sensor/) supports the following methods.
Some methods are only supported by certain models:

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

### Sensor

The [sensor component](/components/sensor/) supports the following methods:

{{< readfile "/static/include/components/apis/sensor.md" >}}

### Servo

The [servo component](/components/servo/) supports the following methods:

{{< readfile "/static/include/components/apis/servo.md" >}}

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a robot.
Built-in API methods are defined for each service implementation.
Documentation on using these methods in your SDK code is found on [service pages](/services/) as follows:

### Base Remote Control

The [Base Remote Control Service](/services/base-rc/) supports the following methods:

{{< readfile "/static/include/services/apis/base-rc.md" >}}

### Data Management

The [Data Management Service](/services/data/) supports the following methods:

{{< readfile "/static/include/services/apis/data.md" >}}

### MLModel

The [ML Model Service](/services/ml/) supports the following methods:

{{< readfile "/static/include/services/apis/ml.md" >}}

### Motion

The [Motion Service](/services/motion/) supports the following methods:

{{< readfile "/static/include/services/apis/motion.md" >}}

### Navigation

The [Navigation Service](/services/navigation/) supports the following methods:

{{< readfile "/static/include/services/apis/navigation.md" >}}

### Sensors

Method Name | Description
----------- | -----------
[`Sensors`](/services/sensors/#sensors) | Returns a list of names of the available sensors.
[`Readings`](/services/sensors/#readings) | Returns a list of readings from a given list of sensors.

### SLAM

The [SLAM Service](/services/slam/) supports the following methods:

{{< readfile "/static/include/services/apis/slam.md" >}}

### Vision

Different [Vision Service](/services/vision/) models support different methods:

{{< readfile "/static/include/services/apis/vision.md" >}}

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
- `qs` [([]resource.DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery): A list of [tuples of API and model](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [([]resource.Discovery)](https://pkg.go.dev/go.viam.com/rdk/resource#Discovery): The search query `qs` and the corresponding list of discovered component configurations as an interface called `Results`.
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

- [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): List of all known resource names.

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
