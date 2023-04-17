---
title: "Gripper Component"
linkTitle: "Gripper"
weight: 60
type: "docs"
description: "A gripper is a robotic grasping device that can open and close."
tags: ["gripper", "components"]
icon: "/components/img/components/gripper.svg"
no_list: true
# SMEs: Bucket Team
---

A *gripper* is a robotic grasping device that can open and close, often attached to the end of an [arm](../arm/) or to a [gantry](../gantry/).

## Configuration

For configuration information, click on your gripper's model:

Model | Supported hardware
----- | -----------
[`softrobotics`](./softrobotics/) | The [*m*Grip soft gripper by Soft Robotics](https://www.softroboticsinc.com/products/mgrip-modular-gripping-solution-for-food-automation/)

If you have another gripper model, you can [define a custom component](../../program/extend/).

## Control your gripper with Viam's client SDK libraries

The following example assumes you have a gripper called `my_gripper` configured as a component of your robot.
If your gripper has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

Place the example code in the `main()` function after `robot = await connect()`.

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper

robot = await connect() # Refer to CODE SAMPLE tab code
# Get the gripper from the robot
my_gripper = Gripper.from_robot(robot, "my_gripper")

# Open the gripper
await my_gripper.open()

# Grab with the gripper and get whether it grabbed anything
grabbed = await my_gripper.grab()
print(f"Grabbed an object: {grabbed}")
```

{{% /tab %}}
{{% tab name="Go" %}}

Place the example code in the `main()` function after `robot, err := client.New(...)`.

```go {class="line-numbers linkable-line-numbers"}
import (
  "context"
  "fmt"

  "go.viam.com/rdk/components/gripper"
)

robot, err := client.New() // Refer to CODE SAMPLE tab code
if err != nil {
    return nil, err
}
// Get the gripper from the robot
myGripper, err := gripper.FromRobot(robot, "my_gripper")
if err != nil {
    return nil, err
}

// Open the gripper
myGripper.Open(context.TODO(), nil)

// Grab with the gripper and get whether it grabbed anything
grabbed, err := myGripper.Grab(context.TODO(), nil)
if err != nil {
    return nil, err
}
fmt.Println("Grabbed something?")
fmt.Println(grabbed)
```

{{% /tab %}}
{{< /tabs >}}

## API

Method Name | Description
----------- | -----------
[`Open`](#open) | Open the gripper.
[`Grab`](#grab) | Close the gripper until it grabs something or closes completely.
[`Stop`](#stop) | Stop the gripper's movement.
[`IsMoving`](#ismoving) | Report whether the gripper is currently moving.
[`DoCommand`](#docommand) | Send or receive model-specific commands.

### Open

Opens the gripper.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/index.html#viam.components.gripper.Gripper.open).

**Example usage:**

```python
my_gripper = Gripper.from_robot(robot=robot, name='my_gripper')

# Open the gripper.
await my_gripper.open()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

**Example usage:**

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Open the gripper.
err := myGripper.Open(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Grab

Closes the gripper until it grabs something or closes completely, and returns whether it grabbed something or not.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether or not the gripper grabbed something.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/index.html#viam.components.gripper.Gripper.grab).

**Example usage:**

```python
my_gripper = Gripper.from_robot(robot=robot, name='my_gripper')

# Grab with the gripper.
grabbed = await my_gripper.grab()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): True if the gripper grabbed something with nonzero thickness.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

**Example usage:**

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Grab with the gripper.
grabbed, err := myGripper.Grab(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stops the gripper.
It is assumed that the gripper stops immediately, so `IsMoving` will return false after calling `Stop`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/index.html#viam.components.gripper.Gripper.stop).

**Example usage:**

```python
my_gripper = Gripper.from_robot(robot=robot, name='my_gripper')

# Stop the gripper.
await my_gripper.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

**Example usage:**

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Stop the gripper.
err := myGripper.Stop(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Returns whether the gripper is actively moving (or attempting to move) under its own power.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(bool)](https://docs.python.org/3/library/functions.html#bool): True if the gripper is currently moving; false if not.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/index.html#viam.components.gripper.Gripper.is_moving).

**Example usage:**

```python
my_gripper = Gripper.from_robot(robot=robot, name='my_gripper')

# Check whether the gripper is currently moving.
moving = await my_gripper.is_moving()
print('Moving:', moving)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): If the gripper is currently moving.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#MovingCheckable).

**Example usage:**

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Check whether the gripper is currently moving.
moving, _ := myGripper.IsMoving(context.TODO())
logger.Info("Is moving?")
logger.Info(moving)
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own gripper and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=robot, name='my_gripper')

raw_dict = {
  "command": "raw",
  "raw_input": "home"
}
await my_gripper.do_command(raw_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/#the-do-method).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` (`cmd map[string]interface{}`): The command to execute.

**Returns:**

- `result` (`cmd map[string]interface{}`): Result of the executed command.
- `error` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myGripper, err := gripper.FromRobot(robot, "my_gripper")

resp, err := myGripper.DoCommand(ctx, map[string]interface{}{"command": "example"})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/api/blob/main/component/gripper/v1/gripper_grpc.pb.go).

{{% /tab %}}
{{< /tabs >}}
