---
linkTitle: "Servo"
title: "Add a servo"
weight: 75
layout: "docs"
type: "docs"
description: "Add and configure a hobby servo controlled by a GPIO PWM pin."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-servo/
---

Add a servo to your machine's configuration so you can control its angular position from the Viam app and from code.

## Concepts

A servo moves to a specific angle (typically 0-180 degrees) and holds that position. Continuous-rotation servos also exist; they use the same `Move` API, but the angle value maps to speed and direction rather than absolute position. Check the specific servo model's reference page for how it interprets the value.

The built-in `gpio` servo model uses a single PWM-capable pin on a [board component](/hardware/common-components/add-a-board/). Other servo models in the registry support serial, I2C, or dedicated servo-driver boards.

Search for `servo` in the [Viam registry](https://app.viam.com/registry) to see available models.

### Built-in models

- [`fake`](/reference/components/servo/fake/) — A model used for testing, with no physical hardware.
- [`gpio`](/reference/components/servo/gpio/) — Supports a hobby servo wired to a board that supports PWM, for example Raspberry Pi 5, Orange Pi, Jetson, or PCAXXXX.

Micro-RDK:

- [`gpio`](/reference/components/servo/micro-rdk/gpio/) — _(no description)_.

### Registry modules

Viam-maintained servo modules:

| Module                                                               | Servos supported                                            |
| -------------------------------------------------------------------- | ----------------------------------------------------------- |
| [`viam:raspberry-pi`](https://app.viam.com/module/viam/raspberry-pi) | `rpi-servo` model for hobby servos on Raspberry Pi variants |

For servos not covered above, search for `servo` in the [Viam registry](https://app.viam.com/registry).

## Steps

### 1. Prerequisites

- Your machine is online in the Viam app.
- A [board component](/hardware/common-components/add-a-board/) is configured.
- Your servo's signal wire is connected to a PWM-capable GPIO pin, with
  power and ground wired appropriately.

### 2. Add a servo component

1. Click the **+** button.
2. Select **Configuration block**.
3. For a standard hobby servo controlled by a PWM pin on your board,
   search for **gpio servo**.
4. Name your servo (for example, `pan-servo`) and click **Create**.

### 3. Configure servo attributes

```json
{
  "board": "my-board",
  "pin": "12"
}
```

| Attribute               | Type   | Required | Description                                                  |
| ----------------------- | ------ | -------- | ------------------------------------------------------------ |
| `board`                 | string | Yes      | Name of the board component.                                 |
| `pin`                   | string | Yes      | GPIO pin for the servo signal wire.                          |
| `min_angle_deg`         | float  | No       | Minimum angle. Default: `0`.                                 |
| `max_angle_deg`         | float  | No       | Maximum angle. Default: `180`.                               |
| `starting_position_deg` | float  | No       | Position on startup. Default: `0`.                           |
| `frequency_hz`          | int    | No       | PWM frequency. Default: `300`. Most servos expect 50-330 Hz. |

If your servo doesn't reach its full range or jitters at the extremes, adjust
the pulse width:

| Attribute      | Type | Description                                  |
| -------------- | ---- | -------------------------------------------- |
| `min_width_us` | int  | Minimum pulse width in microseconds (>450).  |
| `max_width_us` | int  | Maximum pulse width in microseconds (<2500). |

### 4. Save and test

Click **Save**, then expand the **Test** section.

- Enter a value in the **Desired angle (º)** field (the built-in `gpio` model accepts 0-180), then click **Execute** to move the servo.
- Use the **Zero** or **Current position** buttons to quickly fill the input.
- The servo should move smoothly and hold its position.

## Try it

Sweep the servo through a range of positions.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the **Connection details** section on the same tab.
If you're using real hardware, you'll see the servo sweep through positions when you run the code below.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `servo_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.servo import Servo


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    servo = Servo.from_robot(robot, "pan-servo")

    # Sweep through positions
    for angle in [0, 45, 90, 135, 180]:
        await servo.move(angle)
        current = await servo.get_position()
        print(f"Moved to {angle}°, position reads {current}°")
        await asyncio.sleep(0.5)

    # Return to center
    await servo.move(90)
    print("Returned to 90°")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python servo_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir servo-test && cd servo-test
go mod init servo-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "time"

    "go.viam.com/rdk/components/servo"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("servo-test")

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

    s, err := servo.FromProvider(robot, "pan-servo")
    if err != nil {
        logger.Fatal(err)
    }

    // Sweep through positions
    for _, angle := range []uint32{0, 45, 90, 135, 180} {
        if err := s.Move(ctx, angle, nil); err != nil {
            logger.Fatal(err)
        }
        position, err := s.Position(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }
        fmt.Printf("Moved to %d°, position reads %d°\n", angle, position)
        time.Sleep(500 * time.Millisecond)
    }

    // Return to center
    if err := s.Move(ctx, 90, nil); err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Returned to 90°")
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Servo jitters or buzzes" >}}

- The servo may not be getting enough power. Servos draw significant current
  when loaded. Use an external power supply rather than powering from the
  SBC's GPIO header.
- Adjust `frequency_hz`. Some servos work better at 50 Hz, others at 300 Hz.

{{< /expand >}}

{{< expand "Servo doesn't reach full range" >}}

- Adjust `min_width_us` and `max_width_us` to match your servo's actual pulse
  width range. Check the servo's datasheet for the correct values.

{{< /expand >}}

{{< expand "Servo doesn't respond" >}}

- Verify the pin supports PWM output. Not all GPIO pins can generate PWM.
- Check power and ground connections.
- Confirm the pin number in your config matches the physical wiring.

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/servo.md" >}}

## Related

- [Servo API reference](/reference/apis/components/servo/): full method documentation.
- [Add a Motor](/hardware/common-components/add-a-motor/): for continuous rotation
  instead of angular positioning.
- [What is a module?](/build-modules/overview/): write code that
  moves the servo based on sensor readings.
