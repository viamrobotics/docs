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

## API

The base component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
[MoveStraight](#movestraight)  | [MoveStraight][go_base]  |  [move_straight][python_move_straight] | Move the base in a straight line across the given distance at the given velocity. |
[Spin](#spin) |  [Spin][go_base] | [spin][python_spin] | Move the base to the given angle at the given angular velocity. |
[SetPower](#setpower) | [SetPower][go_base] | [set_power][python_set_power] | Set the relative power (out of max power) for linear and angular propulsion of the base. |
[SetVelocity](#setvelocity) | [SetVelocity][go_base] | [set_velocity][python_set_velocity] | Set the linear velocity and angular velocity of the base. |
[Stop](#stop) | [Stop][go_base] | [stop][python_stop] | Stop the base. |

[go_base]: https://pkg.go.dev/go.viam.com/rdk/components/base#Base
[python_move_straight]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.move_straight
[python_spin]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.spin
[python_set_power]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.set_power
[python_set_velocity]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.set_velocity
[python_stop]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.stop

### Control your base with Viam's Client SDK Libraries

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/base/index.html)
- [Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/base)

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app. Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/getting-started/) for app-specific guidance.

The following example assumes you have a base called "my_base" which is configured as a component of your robot.
If your base has a different name, change the `name` in the example.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.base import BaseClient
from viam.proto.common import Vector3

async def main():
    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot. 
    print('Resources:')
    print(robot.resource_names)

    # Connect to your base. 
    myBase = BaseClient.from_robot(robot=robot, name='my_base')

    # Disconnect from your robot. 
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
 "go.viam.com/rdk/components/base"
 "github.com/golang/geo/r3"  
)

func main() { 

  // Create an instance of a logger. 
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot. 
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      })),
  )

  // Log any errors that occur.
  if err != nil {
      logger.Fatal(err)
  }

  // Delay closing your connection to your robot until main() exits. 
  defer robot.Close(context.Background())

  // Log an info message with the names of the different resources that are connected to your robot. 
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Connect to your base.
  myBase, err := base.FromRobot(robot, "my_base")
  if err != nil {
    logger.Fatalf("cannot get base: %v", err)
  }

}
```

{{% /tab %}}
{{< /tabs >}}

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

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Move the base 10 mm at a velocity of 1 mm/s, forward.
await myBase.move_straight(distance=10, velocity=1)

# Move the base 10 mm at a velocity of -1 mm/s, backward.
await myBase.move_straight(distance=10, velocity=-1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `distanceMm` [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- `mmPerSec` [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

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

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Spin the base 10 degrees at an angular velocity of 1 deg/sec.
await myBase.spin(angle=10, velocity=1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(float64)](https://pkg.go.dev/builtin#float64): The angle to spin in degrees.
Negative implies backwards.
- `degsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): The angular velocity at which to spin in degrees per second.
Negative implies backwards.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

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

- `linear` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The percentage of max power of the base's linear propulsion. In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
Viam's coordinate system considers +Y to be the forward axis (+/- X left/right, +/- Z up/down), so use the Y component of this vector to move forward and backward when controlling a wheeled base.
Negative "Y:" values imply moving backwards.
- `angular` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The percentage of max power of the base's angular propulsion.
In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
Use the Z component of this vector to spin left or right when controlling a wheeled base. Negative "Z:" values imply spinning to the right.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_power).

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Make your wheeled base move forward. Set linear power to 75%.
print("move forward")
await myBase.set_power(linear=Vector3(x=0,y=-.75,z=0), angular=Vector3(x=0,y=0,z=0))

# Make your wheeled base move backward. Set linear power to -100%.
print("move backward")
await myBase.set_power(linear=Vector3(x=0,y=-1.0,z=0), angular=Vector3(x=0,y=0,z=0))

# Make your wheeled base spin left. Set angular power to 100%.
print("spin left")
await myBase.set_power(linear=Vector3(x=0,y=0,z=0), angular=Vector3(x=0,y=0,z=1))

# Make your wheeled base spin right. Set angular power to -75%.
print("spin right")
await myBase.set_power(linear=Vector3(x=0,y=0,z=0), angular=Vector3(x=0,y=0,z=-.75))
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `linear` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The percentage of max power of the base's linear propulsion. In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
Viam's coordinate system considers +Y to be the forward axis (+/- X left/right, +/- Z up/down), so use the Y component of this vector to move forward and backward when controlling a wheeled base.
Negative "Y:" values imply moving backwards.
- `angular` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The percentage of max power of the base's angular propulsion.
In the range of -1.0 to 1.0, with 1.0 meaning 100% power.
Use the Z component of this vector to spin left or right when controlling a wheeled base. Negative "Z:" values imply spinning to the right.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Make your wheeled base move forward. Set linear power to 75%.
logger.Info("move forward")
err = myBase.SetPower(context.Background(), linear: r3.Vector{Y: .75}, angular: r3.Vector{})
if err != nil {
    logger.Fatal(err)
}

// Make your wheeled base move backward. Set linear power to -100%.
logger.Info("move backward")
err = myBase.SetPower(context.Background(), linear: r3.Vector{Y: -1}, angular: r3.Vector{})
if err != nil {
    logger.Fatal(err)
}

// Make your wheeled base spin left. Set angular power to 100%.
logger.Info("spin left")
err = myBase.SetPower(context.Background(), linear: r3.Vector{}, angular: r3.Vector{Z: 1})
if err != nil {
  logger.Fatal(err)
}

// Make your wheeled base spin right. Set angular power to -75%.
logger.Info("spin right")
err = mybase.SetPower(context.Background(), r3.Vector{}, r3.Vector{Z: -.75}, nil)
if err != nil {
  logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

### SetVelocity

Set the linear velocity (mm/sec) and angular velocity (degrees/sec) of the base.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `linear` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The linear velocity in mm per second.
Only the Y component of the vector is used for a wheeled base.
- `angular` [(Vector3)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Vector3): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_velocity).

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Set the angular velocity to 1 mm/sec and the linear velocity to 1 degree/sec.
await myBase.set_velocity(linear=Vector3(x=0,y=1,z=0), angular=Vector3(x=0,y=0,z=1))
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `linear` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The linear velocity in mm per second. Only the Y component of the vector is used for a wheeled base.
- `angular` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go
import "github.com/golang/geo/r3"

myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

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

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Move the base forward 10 mm at a velocity of 1 mm/s.
await myBase.move_straight(distance=10, velocity=1)

# Stop the base.
await myBase.stop()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Move the base forward 10 mm at a velocity of 1 mm/s.
myBase.MoveStraight(context.Background(), 10, 1)

// Stop the base.
myBase.Stop(context.Background())
```

{{% /tab %}}
{{< /tabs >}}
