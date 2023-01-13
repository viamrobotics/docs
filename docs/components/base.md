---
title: "Base Component"
linkTitle: "Base"
weight: 10
type: "docs"
description: "Explanation of base configuration and usage in Viam."
tags: ["base", "components"]
# SMEs: Steve B
---

Most robots with wheeled bases will comprise at least the following:

- A [board component](/components/board/) that can run a viam-server instance.
That is to say, a computing device with general purpose input/output (GPIO) pins such as a Raspberry Pi or other single-board computer with GPIO.

- Two or more motors with wheels attached

- A power supply for the board

- A power supply for the motors

- Some sort of chassis to hold everything together

For example:

<img src="../img/base/base-trk-rover-w-arm.png" alt="A robot comprised of a base (motors, wheels and chassis) as well as some other components. The wheels are highlighted to indicate that they are part of the concept of a 'base', while the non-base components are not highlighted. There are width and diameter labels on the diagram because width and circumference (pi times diameter) are required attributes when configuring a base component." />

An example of a wiring diagram for a base that has one motor on each side is shown below.
Note that this will vary greatly depending on choice of motors, motor drivers, power supply, and board.

<img src="../img/base/base-wiring-diagram.png" alt="Wiring diagram showing a Raspberry Pi, motor drivers, motors, power supply, and voltage regulator for the rover."/>

## Configuration

Configuring a base involves configuring the drive motors and ensuring the base attributes section contains the names of all motors that move the base right or left, respectively.
Configure each motor according to its type.
You can find more information on wiring and configuring different types of motors in the [motor topic](../motor/).
The [board](/components/board/) controlling the base must also be configured.

An example configuration file, including the board, motors, and base:

{{< tabs name="Example Servo Config" >}}
{{% tab name="Raw JSON" %}}

```json-viam
{
  "components": [
    {
      "attributes": {},
      "model": "pi",
      "name": "follow-pi",
      "type": "board"
    },
    {
      "attributes": {
        "board": "follow-pi",
        "max_rpm": 300,
        "pins": {
          "dir": "16",
          "pwm": "15"
        }
      },
      "model": "gpio",
      "name": "rightm",
      "type": "motor"
    },
    {
      "attributes": {
        "board": "follow-pi",
        "max_rpm": 300,
        "pins": {
          "dir": "13",
          "pwm": "11"
        }
      },
      "model": "gpio",
      "name": "leftm",
      "type": "motor"
    },
    {
      "attributes": {
        "left": [
          "leftm"
        ],
        "right": [
          "rightm"
        ],
        "wheel_circumference_mm": 183,
        "width_mm": 195
      },
      "model": "wheeled",
      "name": "tread-base",
      "type": "base"
    }
  ]
}
```

{{% /tab %}}
{{< tab name="Annotated JSON" >}}

<img src="../img/base/base-json.png" alt="An image of the JSON configuration file with annotations explaining some of the attributes."/>

{{< /tab >}}
{{< /tabs >}}

### Required Attributes

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>type</code></td>
    <td>string</td>
    <td>Use "base" for any base component</td>
  </tr>
  <tr>
    <td><code>model</code></td>
    <td>string</td>
    <td>Select "wheeled" unless you have a "boat".</td>
  </tr>
  <tr>
    <td><code>name</code></td>
    <td>string</td>
    <td>Name your base.</td>
  </tr>
  <tr>
    <td><code>left</code></td>
    <td>array of strings</td>
    <td>List with the names of all drive motors on the left side of the base. There may be one or more motors.</td>
  </tr>
  <tr>
    <td><code>right</code></td>
    <td>array of strings</td>
    <td>List with the names of all drive motors on the right side of the base. There may be one or more motors.</td>
  </tr>
  <tr>
    <td><code>wheel_circumference_mm</code></td>
    <td>int</td>
    <td>The outermost circumference (not diameter!) of the drive wheels in millimeters. Used for odometry, so try to enter your best approximation of the effective circumference.</td>
  </tr>
  <tr>
    <td><code>width_mm</code></td>
    <td>int</td>
    <td>Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels.</td>
  </tr>

</tbody>
</table>

### Optional Attributes

`spin_slip_factor` (float): Used in steering calculations to correct for slippage between the wheels and the floor.
To be calibrated by the user.

## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/base/index.html)

[Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk)

## API

The base component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
[MoveStraight](#movestraight)  | [MoveStraight][go_base]  |  [move_straight][python_move_straight] | Move the base in a straight line across the given distance at the given velocity. |
[Spin](#spin) |  [Spin][go_base] | [spin][python_spin] | Move the base to the given angle at the given angular velocity. |
[SetPower](#setpower) | [SetPower][go_base] | [set_power][python_set_power] | Set the linear velocity power and angular velocity power of the base. |
[SetVelocity](#setvelocity) | [SetVelocity][go_base] | [set_velocity][python_set_velocity] | Set the linear velocity and angular velocity of the base. |
[Stop](#stop) | [Stop][go_base] | [stop][python_stop] | Stop the base. |

[go_base]: https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/base#Base
[python_move_straight]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.move_straight
[python_spin]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.spin
[python_set_power]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.set_power
[python_set_velocity]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.set_velocity
[python_stop]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.stop

### Access and control your base with Viam's Client SDK Libraries

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app. Check out our [Client SDK Libraries Quick Start](https://docs.viam.com/product-overviews/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and our [Getting Started with the Viam App guide](https://docs.viam.com/getting-started/) for app-specific guidance.

**Assumption:** A base called "my_base" is configured as a component of your robot on the Viam app.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.base import BaseClient

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    # Get the base client from the robot
    myBase = BaseClient.from_robot(robot=robot, name='my_base')

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
 "go.viam.com/rdk/components/base"
)

func main() {
  // robot, err := client.New(...)

  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Get the base client from the robot.
  myBase, err := base.FromRobot(robot, "my_base")
  if err != nil {
    logger.Fatalf("cannot get base: %v", err)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

### MoveStraight

Move the base in a straight line across the given distance (*mm*) at the given velocity (*mm/sec*).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- *distance* [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards.

**Returns:**

- None

[Python SDK Docs: **move_straight**](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.move_straight)

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Move the base 10 mm at a velocity of 1 mm/s, forward
await myBase.move_straight(distance=10, velocity=1)

# Move the base 10 mm at a velocity of -1 mm/s, backward
await myBase.move_straight(distance=10, velocity=-1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- *distanceMm* [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- *mmPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards.
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **MoveStraight**](https://pkg.go.dev/go.viam.com/rdk/components/base#Base)

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Move the base 10 mm at a velocity of 1 mm/s, forward
myBase.MoveStraight(context.Background(), distanceMm: 10, mmPerSec: 1)

// Move the base 10 mm at a velocity of -1 mm/s, backward
myBase.MoveStraight(context.Background(), distanceMm: 10, mmPerSec: -1)
```

{{% /tab %}}
{{< /tabs >}}

### Spin

Move the base in a spinning motion, rotating it to the given angle (*degrees*) at the given angular velocity (*degrees/sec*).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- *angle* [(float)](https://docs.python.org/3/library/functions.html#float): The angle to spin in degrees.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The angular velocity at which to spin in degrees per second.
Negative implies backwards.

**Returns:**

- None

[Python SDK Docs: **spin**](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.spin)

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Spin the base 10 degrees at an angular velocity of 1 deg/sec
await myBase.spin(angle=10, velocity=1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- *angleDeg* [(float64)](https://pkg.go.dev/builtin#float64): The angle to spin in degrees.
Negative implies backwards.
- *degsPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The angular velocity at which to spin in degrees per second.
Negative implies backwards.
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **Spin**](https://pkg.go.dev/go.viam.com/rdk/components/base#Base)

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Spin the base 10 degrees at an angular velocity of 1 deg/sec
myBase.Spin(context.Background(), angleDeg: 10, degsPerSec: 1)
```

{{% /tab %}}
{{< /tabs >}}

### SetPower

Set the linear velocity power (*%, 1- to 1*) and angular velocity power (*%, 1- to 1*) of the base.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- *linear* [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The linear velocity power percentage (-1 to 1).
Only the Y component of the vector is used for a wheeled base.
Negative implies backwards.
- *angular* [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The angular velocity power percentage (-1 to 1).
Only the Z component of the vector is used for a wheeled base.
Here, a positive value implies turning left and a negative value implies turning right.

**Returns:**

- None

[Python SDK Docs: **set_power**](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_power)

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Set the angular and linear velocity power to 100% backwards and 100% right
await myBase.set_power(linear=Vector3(x=0,y=-1,z=0), angular=Vector3(x=0,y=0,z=-1))
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- *linear* [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The linear velocity power percentage (-1 to 1).
Only the Y component of the vector is used for a wheeled base.
Negative implies backwards.
- *angular* [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The angular velocity power percentage (-1 to 1).
Only the Z component of the vector is used for a wheeled base.
Here, a positive value implies turning left and a negative value implies turning right.
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **SetPower**](https://pkg.go.dev/go.viam.com/rdk/components/base#Base)

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Set the angular and linear velocity power to 100% backwards and 100% right
myBase.SetPower(context.Background(), linear: r3.Vector{Y: -1}, angular: r3.Vector{Z: -1})
```

{{% /tab %}}
{{< /tabs >}}

### SetVelocity

Set the linear velocity (*mm/sec*) and angular velocity (*degrees/sec*) of the base.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- *linear* [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The linear velocity in mm per second.
Only the Y component of the vector is used for a wheeled base.
- *angular* [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base.

**Returns:**

- None

[Python SDK Docs: **set_velocity**](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_velocity)

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Set the angular velocity to 1 mm/sec and the linear velocity to 1 degree/sec
await myBase.set_velocity(linear=Vector3(x=0,y=1,z=0), angular=Vector3(x=0,y=0,z=1))
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- *linear* [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The linear velocity in mm per second. Only the Y component of the vector is used for a wheeled base.
- *angular* [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base.
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **SetVelocity**](https://pkg.go.dev/go.viam.com/rdk/components/base#Base)

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Set the angular velocity to 1 mm/sec and the linear velocity to 1 deg/sec
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

[Python SDK Docs: **stop**](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.stop)

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Move the base forward 10 mm at a velocity of 1 mm/s
await myBase.move_straight(distance=10, velocity=1)

# Stop the base
await myBase.stop()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **Stop**](https://pkg.go.dev/go.viam.com/rdk/components/base#Base)

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Move the base forward 10 mm at a velocity of 1 mm/s
myBase.MoveStraight(context.Background(), 10, 1)

// Stop the base 
myBase.Stop(context.Background())
```

{{% /tab %}}
{{< /tabs >}}
