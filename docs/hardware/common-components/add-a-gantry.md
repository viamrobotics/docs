---
linkTitle: "Gantry"
title: "Add a gantry"
weight: 35
layout: "docs"
type: "docs"
description: "Add and configure a gantry component for precise linear positioning along one or more axes."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-gantry/
---

Add a gantry to your machine's configuration so you can control linear positioning along one or more axes from the Viam app and from code.

## Concepts

A gantry component controls linear motion along one or more axes. The API
provides:

- **Position reading**: get the current position on each axis.
- **Move to position**: command movement to a target position at a specified
  speed.
- **Axis lengths**: query the travel range of each axis.
- **Homing**: run a homing sequence to establish a reference position.

Viam includes two built-in gantry models:

| Model         | What it does                                                      |
| ------------- | ----------------------------------------------------------------- |
| `single-axis` | Controls one linear rail driven by a motor.                       |
| `multi-axis`  | Composes multiple single-axis gantries into a coordinated system. |

The `fake` built-in model is useful for testing without hardware.

## Steps

### 1. Prerequisites

- Your machine is online in the Viam app.
- For the `single-axis` model: a [motor](/hardware/common-components/add-a-motor/)
  is configured and tested.
- You know the travel length of your axis in millimeters and the distance per
  motor revolution.

### 2. Add a gantry component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the gantry model that matches your setup:
   - For a single linear rail driven by a motor, search for
     **single-axis**.
   - For a multi-axis system composed of multiple single-axis gantries,
     search for **multi-axis**.
4. Name your gantry (e.g., `my-gantry`) and click **Create**.

### 3. Configure gantry attributes

**Single-axis gantry:**

```json
{
  "motor": "my-motor",
  "length_mm": 500,
  "mm_per_rev": 8
}
```

| Attribute           | Type   | Required | Description                                                            |
| ------------------- | ------ | -------- | ---------------------------------------------------------------------- |
| `motor`             | string | Yes      | Name of the motor that drives this axis.                               |
| `length_mm`         | int    | Yes      | Total travel length of the axis in mm.                                 |
| `mm_per_rev`        | int    | Yes      | Distance traveled per motor revolution in mm (e.g., lead screw pitch). |
| `board`             | string | No       | Board with limit switches, if using them.                              |
| `limit_pins`        | object | No       | Pin names for limit switches at each end of travel.                    |
| `gantry_mm_per_sec` | int    | No       | Default speed in mm/s. Defaults to 100.                                |

**Multi-axis gantry:**

First configure each axis as a separate `single-axis` gantry, then compose
them:

```json
{
  "subaxes_list": ["x-axis", "y-axis", "z-axis"],
  "move_simultaneously": true
}
```

| Attribute             | Type            | Required | Description                                                     |
| --------------------- | --------------- | -------- | --------------------------------------------------------------- |
| `subaxes_list`        | list of strings | Yes      | Names of the single-axis gantry components.                     |
| `move_simultaneously` | bool            | No       | Whether to move all axes at the same time. Defaults to `false`. |

### 4. Save and test

Click **Save**, then expand the **TEST** section.

- Read the current position.
- Command a short move and verify the axis travels the correct distance.
- If using limit switches, verify homing works correctly.

## Try it

Read the gantry's position and move it along the axis.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
If you're using real hardware, you'll see the gantry move along its axis when you run the code below.
With a fake gantry, position values update without physical motion.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `gantry_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.gantry import Gantry


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    gantry = Gantry.from_robot(robot, "my-gantry")

    # Get axis lengths
    lengths = await gantry.get_lengths()
    print(f"Axis lengths (mm): {lengths}")

    # Get current position
    position = await gantry.get_position()
    print(f"Current position (mm): {position}")

    # Move to 100mm at 50mm/s
    print("Moving to 100mm...")
    await gantry.move_to_position(
        positions=[100.0],
        speeds=[50.0]
    )

    # Verify new position
    position = await gantry.get_position()
    print(f"New position (mm): {position}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python gantry_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir gantry-test && cd gantry-test
go mod init gantry-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/gantry"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("gantry-test")

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

    g, err := gantry.FromProvider(robot, "my-gantry")
    if err != nil {
        logger.Fatal(err)
    }

    // Get axis lengths
    lengths, err := g.Lengths(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Axis lengths (mm): %v\n", lengths)

    // Get current position
    position, err := g.Position(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Current position (mm): %v\n", position)

    // Move to 100mm at 50mm/s
    fmt.Println("Moving to 100mm...")
    if err := g.MoveToPosition(ctx, []float64{100.0}, []float64{50.0}, nil); err != nil {
        logger.Fatal(err)
    }

    // Verify new position
    position, err = g.Position(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("New position (mm): %v\n", position)
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Gantry doesn't move" >}}

- Test the underlying motor from its own test panel. If the motor works alone
  but the gantry doesn't, check that the motor name in the gantry config
  matches exactly.
- Verify `mm_per_rev` is correct for your lead screw or belt drive.

{{< /expand >}}

{{< expand "Position readings are inaccurate" >}}

- Measure the actual distance traveled per revolution and update `mm_per_rev`.
- If using a stepper motor without an encoder, missed steps will cause drift.
  Add an encoder for closed-loop control.

{{< /expand >}}

{{< expand "Homing fails or limit switches don't trigger" >}}

- Verify the limit switch wiring and pin numbers in the `limit_pins` config.
- Check `limit_pin_enabled_high`. Set to `true` if your switches are active
  high, `false` for active low.
- Test the switch by reading the GPIO pin directly from the board's test panel.

{{< /expand >}}

## What's next

- [Gantry API reference](/dev/reference/apis/components/gantry/): full method documentation.
- [Add a motor](/hardware/common-components/add-a-motor/): configure the motor
  that drives the gantry axis.
- [Fragments](/hardware/fragments/): save and reuse working
  hardware configurations.
- [What is a module?](/build-modules/from-hardware-to-logic/): write a module that
  coordinates gantry motion with sensors.
