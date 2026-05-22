---
linkTitle: "Motor"
title: "Add a motor"
weight: 55
layout: "docs"
type: "docs"
description: "Add and configure a motor component and test it from the Viam app."
date: "2025-03-07"
aliases:
  - /operate/reference/components/motor/
  - /hardware-components/add-a-motor/
---

Add a motor to your machine's configuration so you can control it from the Viam app and from code.

## Concepts

The motor API gives you `SetPower`, `GoFor` (rotate a number of revolutions at a given speed), `GoTo` (move to an absolute position), and `Stop`. Other models exist as modules for network-controlled motors and specific motor controllers. Search for `motor` in the [Viam registry](https://app.viam.com/registry) to see available models.

This page covers the `gpio` model, which controls a motor through a motor driver wired to GPIO pins on a [board](/hardware/common-components/add-a-board/). You need to add a board first.

GPIO motor drivers typically use one of two wiring schemes:

- **A/B mode**: two direction pins (IN1, IN2) plus an optional enable pin.
  Common with L298N and similar H-bridge drivers.
- **PWM/DIR mode**: one PWM pin for speed and one direction pin.
  Common with many motor driver breakout boards.

### Built-in models

- [`dmc4000`](/reference/components/motor/dmc4000/) — Stepper motor driven by a DMC-40x0 series motion controller.
- [`encoded-motor`](/reference/components/motor/encoded-motor/) — Standard brushed or brushless DC motor with an encoder.
- [`fake`](/reference/components/motor/fake/) — A model for testing, with no physical hardware.
- [`gpio`](/reference/components/motor/gpio/) — Supports standard brushed or brushless DC motors.
- [`gpiostepper`](/reference/components/motor/gpiostepper/) — Supports stepper motors driven by basic GPIO-controlled stepper driver chips.

Micro-RDK:

- [`gpio`](/reference/components/motor/micro-rdk/gpio/) — _(no description)_.

### Registry modules

Viam-maintained motor modules:

| Module                                                                   | Motors supported                                         |
| ------------------------------------------------------------------------ | -------------------------------------------------------- |
| [`viam:analog-devices`](https://app.viam.com/module/viam/analog-devices) | Stepper motors through the Analog Devices TMC5072 driver |
| [`viam:odrive`](https://app.viam.com/module/viam/odrive)                 | ODrive brushless motor controllers (serial)              |
| [`viam:uln2003`](https://app.viam.com/module/viam/uln2003)               | 28BYJ-48 stepper motor through the ULN2003 driver        |

For motors not covered above, search for `motor` in the [Viam registry](https://app.viam.com/registry).

## Steps

### 1. Prerequisites

- Your machine is online in the Viam app.
- A [board component](/hardware/common-components/add-a-board/) is configured.
- Your motor is wired to the board through a motor driver.

### 2. Add a motor component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the motor model that matches your hardware:
   - For a brushed DC motor controlled through a motor driver with GPIO
     pins, search for **gpio motor**.
   - For a stepper motor controlled through a stepper driver with GPIO
     pins, search for **gpiostepper**.
   - For other motor types, search by your motor driver or manufacturer
     name.
4. Name your motor (for example, `left-motor`) and click **Create**.

### 3. Configure motor attributes

The `gpio` model requires you to specify the board and pin mappings.

**A/B mode (for example, L298N driver):**

```json
{
  "board": "my-board",
  "max_rpm": 200,
  "pins": {
    "a": "11",
    "b": "13",
    "pwm": "15"
  }
}
```

**PWM/DIR mode:**

```json
{
  "board": "my-board",
  "max_rpm": 200,
  "pins": {
    "dir": "11",
    "pwm": "13"
  }
}
```

| Attribute       | Type   | Required | Description                                                           |
| --------------- | ------ | -------- | --------------------------------------------------------------------- |
| `board`         | string | Yes      | Name of the board component.                                          |
| `max_rpm`       | int    | Yes      | Estimated max RPM under no load. Used to calculate speed for `GoFor`. |
| `pins`          | object | Yes      | GPIO pin mappings (see wiring modes above).                           |
| `dir_flip`      | bool   | No       | Reverse forward/backward direction. Default: `false`.                 |
| `pwm_freq`      | int    | No       | PWM frequency in Hz. Default: `800`.                                  |
| `min_power_pct` | float  | No       | Minimum power to spin the motor (0.0-1.0). Default: `0.0`.            |
| `max_power_pct` | float  | No       | Maximum power cap (0.06-1.0). Default: `1.0`.                         |

If you have an encoder attached, also set:

| Attribute            | Type   | Description                                  |
| -------------------- | ------ | -------------------------------------------- |
| `encoder`            | string | Name of the encoder component.               |
| `ticks_per_rotation` | int    | Encoder ticks per full motor shaft rotation. |

### 4. Save and test

Click **Save**, then expand the **Test** section for the motor.

- Use the power slider to spin the motor at different speeds.
- Toggle direction to verify forward and backward.
- If you set `max_rpm` and have an encoder, try `GoFor` to rotate a
  specific number of revolutions.

## Try it

Spin the motor forward for 2 revolutions, then check if it's still moving.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the **Connection details** section on the same tab.
If you're using real hardware, you'll see the motor spin when you run the code below.
Without an encoder, position readings will be estimates based on time and max RPM.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `motor_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.motor import Motor


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    motor = Motor.from_robot(robot, "left-motor")

    # Spin at 60 RPM for 2 revolutions
    await motor.go_for(rpm=60, revolutions=2)

    moving = await motor.is_moving()
    print(f"Motor is moving: {moving}")

    position = await motor.get_position()
    print(f"Motor position: {position} revolutions")

    await motor.stop()
    print("Motor stopped")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python motor_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir motor-test && cd motor-test
go mod init motor-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/motor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("motor-test")

    robot, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithCredentials(utils.Credentials{
            Type:    utils.CredentialsTypeAPIKey,
            Payload: "YOUR-API-KEY",
        }),
        client.WithAPIKeyID("YOUR-API-KEY-ID"),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)

    m, err := motor.FromProvider(robot, "left-motor")
    if err != nil {
        logger.Fatal(err)
    }

    // Spin at 60 RPM for 2 revolutions
    if err := m.GoFor(ctx, 60, 2, nil); err != nil {
        logger.Fatal(err)
    }

    moving, err := m.IsMoving(ctx)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Motor is moving: %v\n", moving)

    position, err := m.Position(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Motor position: %.2f revolutions\n", position)

    if err := m.Stop(ctx, nil); err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Motor stopped")
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Motor doesn't spin" >}}

- Check that the motor driver is powered (many drivers need a separate power
  supply for the motor, not just the logic voltage).
- Verify pin numbers match your wiring. Use the board test panel to set each
  pin high/low individually and confirm the motor responds.
- Try increasing `min_power_pct`. Some motors need a minimum threshold to
  overcome static friction.

{{< /expand >}}

{{< expand "Motor spins the wrong direction" >}}

- Set `dir_flip` to `true` in the attributes.
- Or swap the `a` and `b` pins if using A/B mode.

{{< /expand >}}

{{< expand "GoFor doesn't stop at the right position" >}}

- `GoFor` without an encoder estimates time from `max_rpm`. Set `max_rpm`
  accurately for your motor.
- For precise position control,
  [add an encoder](/hardware/common-components/add-an-encoder/) and configure
  `encoder` and `ticks_per_rotation` on the motor.

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/motor.md" >}}

## Related

- [Motor API reference](/reference/apis/components/motor/): full method documentation.
- [Add an Encoder](/hardware/common-components/add-an-encoder/): add position
  feedback for precise motor control.
- [Add a Base](/hardware/common-components/add-a-base/): combine two motors into a
  driveable mobile base.
