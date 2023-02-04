---
title: "Motor Component"
linkTitle: "Motor"
weight: 70
type: "docs"
description: "Explanation of motor configuration and usage in Viam."
tags: ["motor", "components"]
icon: "img/components/motor.png"
# no_list: true
aliases:
    - /components/motor/
# SME: Rand, Jessamy
---

Electric motors are the most common form of [actuator](https://en.wikipedia.org/wiki/Actuator) in robotics.
The Viam *motor* component type natively supports the following models of motor:

Model | Supported hardware <a name="model-table"></a>
---------- | ------------------
[`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor)
[`gpiostepper`](./gpio-stepper/) | [Stepper motor](https://en.wikipedia.org/wiki/Stepper_motor) driven by a basic stepper driver
[`TMC5072`](./tmc5072/) | Stepper motor driven by [the TMC5072 chip](https://www.trinamic.com/support/eval-kits/details/tmc5072-bob/)
[`DMC4000`](./dmc4000/) | Stepper motor driven by a [DMC-40x0 series motion controller](https://www.galil.com/motion-controllers/multi-axis/dmc-40x0)
[`fake`](./fake/) | Used to test code without hardware

As is evident in the table above, how you configure your motor with Viam depends more on the [motor driver](https://www.wellpcb.com/what-is-motor-driver.html) than on the motor itself.

This document assumes you have motor, compatible motor driver, and power supply.
You'll also need a [board](/components/board/) to send signals to the motor driver[^dmcboard].

## API

Method Name | Golang | Python | Description
----------- | ------ | ------ | -----------
[SetPower](#setpower)    | SetPower | set_power |
[GoFor](#gofor) | GoFor  | [go_for](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.go_for) | Spin the motor the specified number of revolutions at specified RPM.
[GoTo](#goto) | GoTo   | go_to |
[ResetZeroPosition](#resetzeroposition) | ResetZeroPosition | reset_zero_position |
[GetPosition](#getposition) | GetPosition | get_position |
[GetProperties](#getproperties) | GetProperties | get_properties |
[Stop](#stop) | Stop | stop |
[IsPowered](#ispowered) | IsPowered | is_powered |
[IsMoving](#ismoving) | IsMoving | is_moving |

## Configuration

To configure a motor as a component of your robot, first configure the [board](/components/board/) to which the motor driver is wired[^dmcboard].

Configure your motor with the universal component fields:

Field | Description
----- | -----------
`name` | Choose a name to identify the motor.
`type` | `motor` is the type for all motor components.
`model` | Depends on the motor driver; see the list of models in the [table above](#model-table).

Refer to the document for your specific motor model for attribute configuration information:

- [`gpio`](./gpio/)
- [`gpiostepper`](./gpio-stepper/)
- [`TMC5072`](./tmc5072/)
- [`DMC4000`](./dmc4000/)
- [`fake`](./fake/)

```json
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "<board model>",
      "attributes": {},
      "depends_on": [],
      
    },
    {
      "name": "example-gpio",
      "type": "motor",
      "model": "<model, e.g. 'gpio'>",
      "attributes": {
        "<ATTRIBUTES VARY DEPENDING ON MOTOR MODEL; SEE RESPECTIVE DOCUMENTATION>"
        "board": "local"
      },
      "depends_on": []
    }
  ]
}
```

[^dmcboard]: The `DMC4000` model does not require a board.

### Usage example

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you, go to [app.viam.com](https://app.viam.com/), create a new robot and go to the **SETUP** tab and follow the instructions there.

The following example assumes motors called "motor1" and "motor2" are configured as components of your robot.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

This example sends power commands to motors on the robot.

```python
from viam.components.motor import Motor

robot = await connect() # refer to connect code
motor1 = Motor.from_robot(robot, "motor1")
motor2 = Motor.from_robot(robot, "motor2")

# power motor1 at 100% for 3 seconds
await motor1.set_power(1)
await asyncio.sleep(3)
await motor1.stop()

# run motor2 at 1000 rpm for 200 rotations
await motor2.go_for(1000, 200)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"time"
"go.viam.com/rdk/components/motor"
)

robot, err := client.New() // refer to connect code
// grab the motors from the robot
m1, err := motor.FromRobot(robot, "motor1")
m2, err := motor.FromRobot(robot, "motor2")

// power motor1 at 100% for 3 seconds
m1.SetPower(context.Background(), 1, nil)
time.Sleep(3 * time.Second)
m1.Stop(context.Background(), nil)

// run motor2 at 1000 RPM for 200 rotations
m2.GoFor(context.Background(), 1000, 200, nil)
```

{{% /tab %}}
{{< /tabs >}}

### API Details

#### SetPower

#### GoFor

#### GoTo

#### ResetZeroPosition

#### GetPosition

#### GetProperties

#### Stop

#### IsPowered

#### IsMoving
