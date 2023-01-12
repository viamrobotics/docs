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
<!-- [go.viam.com/rdk/components/base] -->

## API

The base component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
[MoveStraight] (#movestraight)  | [MoveStraight] [go_base]  |  [move_straight] [python_move_straight] | Move the base in a straight line the given distance (int)(mm) at the given velocity (double/float)(mm/s). |

[Spin] (#spin) |  [Spin] [go_base] | [spin] [python_spin] | Spin the base in place the given angle (float)(degrees), at the given angular velocity (float)(degrees/s) |

[SetPower](#setpower) | [SetPower] [go_base] | [set_power] [python_set_power] | Set the linear velocity (Vector3) and angular velocity (Vector3) of the base |

[SetVelocity](#setvelocity) | [SetVelocity][go_base] | [set_velocity] [python_set_velocity] | Set the linear velocity (Vector3) (mm/sec) and angular velocity (Vector3) (deg/sec) of the base |

[Stop](#stop) | [Stop][go_base] | [stop][python_stop] | Stop the base |

[IsMoving](#ismoving) | [][] | [is_moving][python_is_moving] | Get if the base is currently moving |

[go_base]: https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/base#Base
[python_move_straight]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.move_straight
[python_spin]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.spin
[python_set_power]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.set_power
[python_set_velocity]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.set_velocity
[python_stop]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.stop
[python_is_moving]: https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.is_moving

### Access and control your base with Viam's Client SDK Libraries
<!-- wip, want a better way to phrase this than it was phrased formerly -->

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app. Check out our [Client SDK Libraries Quick Start](/product-overviews/sdk-as-client/#quick-start-examples) documentation for an overview of how to get started connecting to your robot using these libraries, and our [Getting Started with the Viam App guide](/getting-started/app-usage/) for app-specific guidance.

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

The MoveStraight method requests the base of the robot to move in a straight line the given distance (int)(mm) at the given velocity (double/float)(mm/s).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- distance (int): The distance to move the base in millimeters. Negative implies backwards.
- velocity (float): The velocity (in millimeters per second) at which to move the base. Again, negative implies backwards.

**Returns:**

- None

[Python SDK move_straight Documentation](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.move_straight)

```python
myBase = BaseClient.from_robot(robot=robot, name='my_base')

# Move the base forward 10mm at a velocity of 1 mm/s
await myBase.move_straight(distance=10, velocity=1)

# Move the base backward 10mm at a velocity of -1 mm/s
await myBase.move_straight(distance=10, velocity=-1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- distanceMm (int): The distance to move the base in millimeters. Negative implies backwards.
- mmPerSec (float64): The velocity (in millimeters per second) at which to move the base. Again, negative implies backwards.
- extra (map[string]interface{}): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error if one occurred.

[Go SDK MoveStraight Documentation](https://pkg.go.dev/go.viam.com/rdk/components/base#Base)

```go
myBase, err := base.FromRobot(robot, "my_base")
if err != nil {
  logger.Fatalf("cannot get base: %v", err)
}

// Move the base forward 10mm at a velocity of 1 mm/s
myServo.Move(context.Background(), 10, 1)
```

{{% /tab %}}
{{< /tabs >}}

### Spin

The spin method requests the base of the robot to spin by a given angle in degrees at a given speed in degrees per second.

### SetPower

### SetVelocity

### Stop

### IsMoving
