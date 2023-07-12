---
title: "Gripper Component"
linkTitle: "Gripper"
childTitleEndOverwrite: "Gripper Component"
weight: 60
type: "docs"
description: "A gripper is a robotic grasping device that can open and close."
tags: ["gripper", "components"]
icon: "/icons/components/gripper.svg"
images: ["/icons/components/gripper.svg"]
no_list: true
# SMEs: Bucket Team
---

A *gripper* is a robotic grasping device that can open and close, often attached to the end of an [arm](../arm/) or to a [gantry](../gantry/).

## Configuration

For configuration information, click on your gripper's model:

Model | Description
----- | -----------
[`softrobotics`](./softrobotics/) | The [*m*Grip soft gripper by Soft Robotics](https://www.softroboticsinc.com/products/mgrip-modular-gripping-solution-for-food-automation/) |
[`fake`](fake/) | A model used for testing, with no physical hardware. |

If you have another gripper model, you can [define a custom component](../../extend/).

## Control your gripper with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a gripper called `"my_gripper"` configured as a component of your robot.
If your gripper has a different name, change the `name` in the code.

Be sure to import the gripper package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gripper import Gripper
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/gripper"
)
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

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Open the gripper.
await my_gripper.open()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Open the gripper.
err := myGripper.Open(context.Background(), nil)
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

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Grab with the gripper.
grabbed = await my_gripper.grab()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): True if the gripper grabbed something with nonzero thickness.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Grab with the gripper.
grabbed, err := myGripper.Grab(context.Background(), nil)
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

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

# Stop the gripper.
await my_gripper.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Stop the gripper.
err := myGripper.Stop(context.Background(), nil)
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

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): True if the gripper is currently moving; false if not.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/index.html#viam.components.gripper.Gripper.is_moving).

```python
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

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

```go
myGripper, err := gripper.FromRobot(robot, "my_gripper")

// Check whether the gripper is currently moving.
moving, err := myGripper.IsMoving(context.Background())
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

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=robot, name="my_gripper")

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

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myGripper, err := gripper.FromRobot(robot, "my_gripper")

resp, err := myGripper.DoCommand(ctx, map[string]interface{}{"command": "example"})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/api/blob/main/component/gripper/v1/gripper_grpc.pb.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{< /cards >}}
