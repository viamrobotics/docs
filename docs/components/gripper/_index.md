---
title: "Gripper Component"
linkTitle: "Gripper"
weight: 60
type: "docs"
description: "A gripper is a robotic grasping device."
tags: ["gripper", "components"]
icon: "/components/img/components/gripper.svg"
no_list: true
# SMEs: Bucket Team
---

A *gripper* is a robotic grasping device, often attached to the end of an [arm](../arm/) or to a [gantry](../gantry/).

## Configuration

For configuration information, click on your gripper's model:

Model | Supported hardware
----- | -----------
[`softrobotics`](./softrobotics/) | The [mGrip soft gripper by Soft Robotics](https://www.softroboticsinc.com/products/mgrip-modular-gripping-solution-for-food-automation/)

If you have another gripper model, you can [define a custom component](../../program/extend/).

## Control your gripper with Viam's client SDK libraries

The following example assumes you have a gripper called `my_gripper` configured as a component of your robot.
If your gripper has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

Place the example code in the `main()` function after `robot = await connect()`.

```python
from viam.components.gripper import Gripper

robot = await connect() # Refer to CODE SAMPLE tab code
my_gripper = Gripper.from_robot(robot, "my_gripper")

# Open the gripper
await my_gripper.open()

# Grab with the gripper and get whether it grabbed anything
grabbed = await my_gripper.grab()
```

{{% /tab %}}
{{% tab name="Go" %}}

Place the example code in the `main()` function after `robot, err := client.New(...)`.

```go
import (
  "context"
  "time"

  "github.com/edaniels/golog"

  "go.viam.com/rdk/components/gripper"
)

robot, err := client.New() // Refer to CODE SAMPLE tab code
// Get the gripper from the robot
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Open the gripper
grip.Open(context.TODO(), nil)

// Grab with the gripper and get whether it grabbed anything
grabbed, err := grip.Grab(context.TODO(), nil)
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

### Grab

### Stop

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

- [(bool)](https://pkg.go.dev/builtin#bool): True if the gripper is currently moving.
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

## Next Steps

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/gripper/index.html)
