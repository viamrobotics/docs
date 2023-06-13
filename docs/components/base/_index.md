---
title: "Base Component"
linkTitle: "Base"
weight: 10
type: "docs"
no_list: true
description: "The moving platform that the other parts of a mobile robot attach to."
tags: ["base", "components"]
icon: "/components/img/components/base.svg"
images: ["/components/img/components/base.svg"]
# SMEs: Steve B
---

A base is the platform that the other parts of a mobile robot attach to.

By configuring a base component, organizing individual components to produce coordinated movement, you gain an interface to control the movement of the whole physical base of the robot without needing to send separate commands to individual motors.

![A robot comprised of a wheeled base (motors, wheels and chassis) as well as some other components. The wheels are highlighted to indicate that they are part of the concept of a 'base', while the non-base components are not highlighted. The width and circumference are required attributes when configuring a base component.](img/base-trk-rover-w-arm.png)

Most mobile robots with a base need at least the following hardware:

- A [board](/components/board/).
- Some sort of actuators to move the base.
  Usually [motors](/components/motor/) attached to wheels or propellers.
- A power supply for the board.
- A power supply for the actuators.
- Some sort of chassis to hold everything together.

## Configuration

Supported base models include:

| Model | Description |
| ----- | ----------- |
| [`wheeled`](wheeled/) | Mobile wheeled robot |
| [`agilex-limo`](agilex-limo/) | [Agilex LIMO Mobile Robot](https://global.agilex.ai/products/limo) |
| [`fake`](fake/) | A model used for testing, with no physical hardware |
| `boat` | Mobile boat robot |

## Control your base with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code Sample** tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a wheeled base called `"my_base"` configured as a component of your robot.
If your base has a different name, change the `name` in the code.

Be sure to import the base package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.base import Base
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/base"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The base component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [MoveStraight](#movestraight)  | Move the base in a straight line across the given distance at the given velocity. |
| [Spin](#spin) | Move the base to the given angle at the given angular velocity. |
| [SetPower](#setpower) | Set the relative power (out of max power) for linear and angular propulsion of the base. |
| [SetVelocity](#setvelocity) | Set the linear velocity and angular velocity of the base. |
| [Stop](#stop) | Stop the base. |
| [DoCommand](#docommand) | Send or receive model-specific commands. |

### MoveStraight

Move the base in a straight line across the given distance (mm) at the given velocity (mm/sec).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `distance` [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- `velocity` [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.move_straight).

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Move the base 10 mm at a velocity of 1 mm/s, forward.
await my_base.move_straight(distance=10, velocity=1)

# Move the base 10 mm at a velocity of -1 mm/s, backward.
await my_base.move_straight(distance=10, velocity=-1)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `distanceMm` [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- `mmPerSec` [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(robot, "my_base")

// Move the base forward 10 mm at a velocity of 1 mm/s.
myBase.MoveStraight(context.Background(), distanceMm: 10, mmPerSec: 1)

// Move the base backward 10 mm at a velocity of -1 mm/s.
myBase.MoveStraight(context.Background(), distanceMm: 10, mmPerSec: -1)
```

{{% /tab %}}
{{< /tabs >}}

### Spin

Turn the base in place, rotating it to the given angle (degrees) at the given angular velocity (degrees/sec).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `angle` [(float)](https://docs.python.org/3/library/functions.html#float): The angle to spin in degrees.
Negative implies backwards.
- `velocity` [(float)](https://docs.python.org/3/library/functions.html#float): The angular velocity at which to spin in degrees per second.
Negative implies backwards.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.spin).

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Spin the base 10 degrees at an angular velocity of 1 deg/sec.
await my_base.spin(angle=10, velocity=1)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(float64)](https://pkg.go.dev/builtin#float64): The angle to spin in degrees.
Negative implies backwards.
- `degsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): The angular velocity at which to spin in degrees per second.
Negative implies backwards.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(robot, "my_base")

// Spin the base 10 degrees at an angular velocity of 1 deg/sec.
myBase.Spin(context.Background(), angleDeg: 10, degsPerSec: 1)
```

{{% /tab %}}
{{< /tabs >}}

### SetPower

Set the linear and angular power of the base, represented as a percentage of max power for each direction in the range of [-1.0 to 1.0].

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `linear` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The percentage of max power of the base's linear propulsion.
  In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
  Viam's coordinate system considers +Y to be the forward axis (+/- X right/left, +/- Z up/down), so use the Y component of this vector to move forward and backward when controlling a wheeled base.
  Negative "Y:" values imply moving backwards.
- `angular` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The percentage of max power of the base's angular propulsion.
  In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
  Use the Z component of this vector to spin left or right when controlling a wheeled base.
  Negative "Z:" values imply spinning to the right.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_power).

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Make your wheeled base move forward. Set linear power to 75%.
print("move forward")
await my_base.set_power(linear=Vector3(x=0,y=-.75,z=0), angular=Vector3(x=0,y=0,z=0))

# Make your wheeled base move backward. Set linear power to -100%.
print("move backward")
await my_base.set_power(linear=Vector3(x=0,y=-1.0,z=0), angular=Vector3(x=0,y=0,z=0))

# Make your wheeled base spin left. Set angular power to 100%.
print("spin left")
await my_base.set_power(linear=Vector3(x=0,y=0,z=0), angular=Vector3(x=0,y=0,z=1))

# Make your wheeled base spin right. Set angular power to -75%.
print("spin right")
await my_base.set_power(linear=Vector3(x=0,y=0,z=0), angular=Vector3(x=0,y=0,z=-.75))
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `linear` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The percentage of max power of the base's linear propulsion. In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
Viam's coordinate system considers +Y to be the forward axis (+/- X left/right, +/- Z up/down), so use the Y component of this vector to move forward and backward when controlling a wheeled base.
Negative "Y:" values imply moving backwards.
- `angular` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The percentage of max power of the base's angular propulsion.
In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
Use the Z component of this vector to spin left or right when controlling a wheeled base. Negative "Z:" values imply spinning to the right.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(robot, "my_base")

// Make your wheeled base move forward. Set linear power to 75%.
logger.Info("move forward")
err = myBase.SetPower(context.Background(), linear: r3.Vector{Y: .75}, angular: r3.Vector{})

// Make your wheeled base move backward. Set linear power to -100%.
logger.Info("move backward")
err = myBase.SetPower(context.Background(), linear: r3.Vector{Y: -1}, angular: r3.Vector{})

// Make your wheeled base spin left. Set angular power to 100%.
logger.Info("spin left")
err = myBase.SetPower(context.Background(), linear: r3.Vector{}, angular: r3.Vector{Z: 1})

// Make your wheeled base spin right. Set angular power to -75%.
logger.Info("spin right")
err = mybase.SetPower(context.Background(), r3.Vector{}, r3.Vector{Z: -.75}, nil)
```

{{% /tab %}}
{{< /tabs >}}

### SetVelocity

Set the linear velocity (mm/sec) and angular velocity (degrees/sec) of the base.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `linear` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The linear velocity in mm per second.
Only the Y component of the vector is used for a wheeled base, since Viam's coordinate system considers +Y to be the forward axis.
- `angular` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base, since Viam's coordinate system considers +Z to point up and the angular velocity to rotate around the Z axis.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_velocity).

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Set the angular velocity to 1 mm/sec and the linear velocity to 1 degree/sec.
await my_base.set_velocity(linear=Vector3(x=0,y=1,z=0), angular=Vector3(x=0,y=0,z=1))
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `linear` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The linear velocity in mm per second. Only the Y component of the vector is used for a wheeled base.
- `angular` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go {class="line-numbers linkable-line-numbers"}
// import "github.com/golang/geo/r3" ...

myBase, err := base.FromRobot(robot, "my_base")

// Set the angular velocity to 1 mm/sec and the linear velocity to 1 deg/sec.
myBase.SetVelocity(context.Background(), linear: r3.Vector{Y: 1}, angular: r3.Vector{Z: 1})
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop the base from moving immediately.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.stop).

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Move the base forward 10 mm at a velocity of 1 mm/s.
await my_base.move_straight(distance=10, velocity=1)

# Stop the base.
await my_base.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(robot, "my_base")

// Move the base forward 10 mm at a velocity of 1 mm/s.
myBase.MoveStraight(context.Background(), 10, 1)

// Stop the base.
myBase.Stop(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own base and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot, "my_base")

command = {"cmd": "test", "data1": 500}
result = my_base.do(command)
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
myBase, err := base.FromRobot(robot, "my_base")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myBase.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/control/yahboom-rover" size="small" %}}
  {{% card link="/tutorials/get-started/try-viam-sdk" size="small" %}}
  {{% card link="/tutorials/services/webcam-line-follower-robot" size="small" %}}
{{< /cards >}}
