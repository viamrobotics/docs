---
linkTitle: "Base"
title: "Add a base"
weight: 10
layout: "docs"
type: "docs"
description: "Add and configure a base to drive a mobile robot with movement commands."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-base/
---

Add a base to your machine's configuration to drive a mobile robot with movement commands like "move forward 300mm" or "spin 90 degrees." A base wraps your robot's drive system, whatever the motor layout, into a single interface that handles steering and speed for you.

## Concepts

A base component gives you a movement API (`MoveStraight`, `Spin`, `SetVelocity`, `Stop`) regardless of the underlying drive system. The most common model is `wheeled`, which handles differential steering for robots with left and right motors. Other models exist for different platforms, including `sensor-controlled` (adds IMU feedback to improve accuracy) and module-based models for specific hardware.

Browse all available base models in the [Viam registry](https://app.viam.com/registry?type=component&subtype=base).

This page covers the `wheeled` model. You configure your motors first, then the base references them.

For accurate distance and angle calculations, the `wheeled` model needs two physical measurements:

- **Wheel circumference**: how far the robot travels per wheel revolution.
- **Track width** (`width_mm` in the config): the distance between the left and right wheel centers. Not the outside edges of the wheels, and not the robot's overall body width.

### Built-in models

- [`fake`](/reference/components/base/fake/) — A model used for testing, with no physical hardware.
- [`sensor-controlled`](/reference/components/base/sensor-controlled/) — Wrap other base models and add feedback control using a movement sensor.
- [`wheeled`](/reference/components/base/wheeled/) — Supports mobile wheeled robotic bases with motors on both sides for differential steering.

Micro-RDK:

- [`two_wheeled_base`](/reference/components/base/micro-rdk/two_wheeled_base/) — _(no description)_.

### Registry modules

For hardware the built-in models don't cover, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=base). Each module's configuration is documented on its registry page.

## Steps

### 1. Prerequisites

- Your machine is online in the Viam app.
- Left and right [motor components](/hardware/common-components/add-a-motor/) are
  configured and tested.
- You've measured your wheel circumference and track width in millimeters.

### 2. Add a base component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the base model that matches your hardware. For a
   differential-drive robot with left and right motors, search for
   **wheeled**.
4. Name your base (for example, `my-base`) and click **Create**.

### 3. Configure base attributes

```json
{
  "left": ["left-motor"],
  "right": ["right-motor"],
  "wheel_circumference_mm": 220,
  "width_mm": 300
}
```

| Attribute                | Type            | Required | Description                                                                                                            |
| ------------------------ | --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------- |
| `left`                   | list of strings | Yes      | Names of the motors on the left side.                                                                                  |
| `right`                  | list of strings | Yes      | Names of the motors on the right side.                                                                                 |
| `wheel_circumference_mm` | int             | Yes      | Outer circumference of a drive wheel in mm.                                                                            |
| `width_mm`               | int             | Yes      | Distance between left and right wheel centers in mm.                                                                   |
| `spin_slip_factor`       | float           | No       | Correction factor for turning accuracy. Increase if the robot over-rotates during spins; decrease if it under-rotates. |

For robots with multiple motors per side (for example, six-wheel drive), list all
motor names for that side:

```json
{
  "left": ["front-left-motor", "mid-left-motor", "rear-left-motor"],
  "right": ["front-right-motor", "mid-right-motor", "rear-right-motor"],
  "wheel_circumference_mm": 220,
  "width_mm": 300
}
```

### 4. Save and test

Click **Save**, then expand the **Test** section.

- Use the directional controls to drive the base forward, backward, left,
  and right.
- Test `MoveStraight` with a specific distance to verify distance accuracy.
- Test `Spin` with a specific angle to verify turning accuracy.

{{< alert title="Safety" color="caution" >}}

Ensure the robot has room to move and is either on a test stand or in a clear
area. Start with low speeds.

{{< /alert >}}

## Try it

Drive the base forward, spin it, and stop.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the **Connection details** section on the same tab.
If you're using real hardware, you'll see the robot drive forward and spin when you run the code below.
With a fake base, the commands complete without physical motion.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `base_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.base import Base


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    base = Base.from_robot(robot, "my-base")

    # Drive forward 300mm at 200mm/s
    print("Driving forward 300mm...")
    await base.move_straight(distance=300, velocity=200)

    # Spin 90 degrees at 45 degrees/s
    print("Spinning 90 degrees...")
    await base.spin(angle=90, velocity=45)

    # Stop
    await base.stop()
    print("Done")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python base_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir base-test && cd base-test
go mod init base-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("base-test")

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

    b, err := base.FromProvider(robot, "my-base")
    if err != nil {
        logger.Fatal(err)
    }

    // Drive forward 300mm at 200mm/s
    fmt.Println("Driving forward 300mm...")
    if err := b.MoveStraight(ctx, 300, 200, nil); err != nil {
        logger.Fatal(err)
    }

    // Spin 90 degrees at 45 degrees/s
    fmt.Println("Spinning 90 degrees...")
    if err := b.Spin(ctx, 90, 45, nil); err != nil {
        logger.Fatal(err)
    }

    // Stop
    if err := b.Stop(ctx, nil); err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Done")
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Robot drives in the wrong direction" >}}

- Swap the `left` and `right` motor lists.
- Or set `dir_flip` to `true` on the individual motors that are reversed.

{{< /expand >}}

{{< expand "Robot curves instead of driving straight" >}}

- Verify that both motors spin at similar speeds. Different motors or uneven
  friction can cause drift.
- Adding encoders to both motors improves straight-line accuracy.

{{< /expand >}}

{{< expand "Turns are inaccurate" >}}

- Measure `width_mm` carefully. It's the distance between the wheel contact
  points, not the outside edges of the wheels.
- Adjust `spin_slip_factor` up or down until spins land on the correct angle.
  This compensates for tire grip and surface friction.

{{< /expand >}}

{{< expand "Robot doesn't move at all" >}}

- Test each motor individually from its own test panel. If the motors work
  alone but the base doesn't, check that the motor names in the base config
  match exactly (names are case-sensitive).

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/base.md" >}}

## Related

- [Base API reference](/reference/apis/components/base/): full method documentation.
- [Add a Movement Sensor](/hardware/common-components/add-a-movement-sensor/): add
  GPS or odometry to track where the base is.
- [Add an Encoder](/hardware/common-components/add-an-encoder/): add encoders to
  your motors for better accuracy.
- [What is a module?](/build-modules/overview/): write a module that
  drives the base based on sensor input.
