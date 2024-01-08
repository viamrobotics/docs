---
title: "Interact with Resources with Viam's Client SDKs"
linkTitle: "APIs"
weight: 20
type: "docs"
description: "Access and control your machine or fleet with the SDKs' client libraries for the resource and robot APIs."
icon: "/services/icons/sdk.svg"
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api"]
aliases:
  - /program/sdks/
  - /program/apis/
no_list: true
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [Application Programming Interface (API)](https://en.wikipedia.org/wiki/API) described through [protocol buffers](https://developers.google.com/protocol-buffers).
You can think of this as a description of how you can interact with that resource.
Different models of resources implement the same API, which [Viam SDKs expose](/internals/machine-to-machine-comms/), allowing you to control different models of resource types with a consistent interface.

The API methods provided by the SDKs for each of these resource APIs wrap gRPC client requests to the machine when you execute your program, providing you a convenient interface for accessing information about and controlling the {{< glossary_tooltip term_id="resource" text="resources" >}} you have [configured](/build/configure/) on your machine.

## Robot Management APIs

### Robot API

All machines support the following methods through the [robot API](/build/program/apis/robot/):

{{< readfile "/static/include/services/apis/robot.md" >}}

### Cloud API

The [cloud API](/build/program/apis/cloud/) supports the following methods:

{{< readfile "/static/include/services/apis/cloud.md" >}}

### Data Client API

The data client API supports the following methods to upload and retrieve data directly to the [Viam app](https://app.viam.com) (among [others](https://python.viam.dev/autoapi/viam/app/data_client/index.html)):

{{< readfile "/static/include/services/apis/data-client.md" >}}

### ML Training API

The ML training API allows you to get information about and cancel ML training jobs taking place on the [Viam app](https://app.viam.com):

{{< readfile "/static/include/services/apis/ml-training-client.md" >}}

## Component APIs

These APIs provide interfaces for controlling and getting information from various components of a machine.
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

### Generic

The [generic component](/components/generic/) supports the following methods:

{{< readfile "/static/include/components/apis/generic.md" >}}

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

### Power Sensor

The [power sensor component](/components/power-sensor/) supports the following methods:

{{< readfile "/static/include/components/apis/power-sensor.md" >}}

### Sensor

The [sensor component](/components/sensor/) supports the following methods:

{{< readfile "/static/include/components/apis/sensor.md" >}}

### Servo

The [servo component](/components/servo/) supports the following methods:

{{< readfile "/static/include/components/apis/servo.md" >}}

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a machine.
Built-in API methods are defined for each service implementation.
Documentation on using these methods in your SDK code is found on [service pages](/services/) as follows:

### Base Remote Control

The [base remote control service](/mobility/base-rc/) supports the following methods:

{{< readfile "/static/include/services/apis/base-rc.md" >}}

### Data Management

The [data management service](/data/) supports the following methods:

{{< readfile "/static/include/services/apis/data.md" >}}

### ML Model

The [ML model service](/ml/) supports the following methods:

{{< readfile "/static/include/services/apis/ml.md" >}}

### Motion

The [motion service](/mobility/motion/) supports the following methods:

{{< readfile "/static/include/services/apis/motion.md" >}}

### Navigation

The [navigation service](/mobility/navigation/) supports the following methods:

{{< readfile "/static/include/services/apis/navigation.md" >}}

### SLAM

The  [{{< glossary_tooltip term_id="slam" text="Simultaneous Localization And Mapping (SLAM) service " >}}](/mobility/slam) supports the following methods:

{{< readfile "/static/include/services/apis/slam.md" >}}

### Vision

Different [vision service](/ml/vision/) models support different methods:

{{< readfile "/static/include/services/apis/vision.md" >}}

## Signaling APIs

### GPIO Pins

In addition to the [board API](#board), the [board component](/components/board/) supports the following methods for interfacing with GPIO pins on a board:

{{< readfile "/static/include/components/apis/gpiopin.md" >}}

### Analog-to-Digital Converters (ADCs)

In addition to the [board API](#board), the [board component](/components/board/) supports the following methods for interfacing with [ADCs](/components/board/#analogs) on a board:

{{< readfile "/static/include/components/apis/analogreader.md" >}}

### Digital Interrupts

In addition to the [board API](#board), the [board component](/components/board/) supports the following methods for interfacing with [digital interrupts](/components/board/#digital_interrupts) on a board:

{{< readfile "/static/include/components/apis/digitalinterrupt.md" >}}

## ResourceBase Methods

In the Python SDK, the [`ResourceBase`](https://python.viam.dev/autoapi/viam/resource/base/index.html) class defines a basic set of API methods that all child resources should provide for users.
In the other SDKs, resource APIs implement but do not inherit these base requirements.

`ResourceBase` methods include:

### FromRobot

Get a resource configured on a machine by `"name"`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot` [(RobotClient)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient): The machine.
- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The `name` of the resource.

**Returns:**

- [(Resource)](https://python.viam.dev/autoapi/viam/resource/base/index.html): The named resource if it exists on your machine.
  For example, an [arm](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```python
my_arm = Arm.from_robot(robot, "my_arm")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/resource/base/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `r` [(RobotClient)](https://pkg.go.dev/go.viam.com/rdk/robot#Robot): The machine.
- `name` [(string)](https://pkg.go.dev/builtin#string): The "name" of the resource.

**Returns:**

- [(Resource)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The named resource if it exists on your machine.
  For example, an [arm](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
my_arm = arm.FromRobot(robot, "my_arm")
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#FromRobot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

In the TypeScript SDK, the equivalent of the `FromRobot` is defined in each resource API's client constructor.

For example, a component with [type `arm`](https://ts.viam.dev/classes/ArmClient.html) and name `my_arm` belonging to a machine `robot` is instantiated as follows:

**Parameters:**

- `client` [(RobotClient)](https://ts.viam.dev/classes/RobotClient.html): The machine.
- `name` [(string)](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html): The `name` of the resource.

**Returns:**

- [(Resource)](https://ts.viam.dev/interfaces/Resource.html): The named resource if it exists on your machine.
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

```python
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

```go
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
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): The result of the executed command.
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
