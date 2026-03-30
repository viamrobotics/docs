---
linkTitle: "Switch"
title: "Add a switch"
weight: 80
layout: "docs"
type: "docs"
description: "Add and configure a switch component to read and set the position of a multi-position switch."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-switch/
---

Add a switch to your machine's configuration so you can read and set switch positions from the Viam app and from code.

## Concepts

A switch component represents a multi-position switch. The API provides:

- **GetPosition**: read the current switch position (as a number).
- **SetPosition**: set the switch to a specific position.
- **GetNumberOfPositions**: query how many positions the switch has, along
  with optional labels for each position.

Physical switch hardware typically comes from a **module in the registry** that
reads GPIO pins or communicates with a switch controller.

The `fake` built-in model simulates a switch with configurable positions and
is useful for testing.

## Steps

### 1. Add a switch component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your switch hardware. Search by
   manufacturer name, chip, or device type.
4. Name your switch (for example, `my-switch`) and click **Create**.

### 2. Configure switch attributes

**For the `fake` model:**

```json
{
  "position_count": 3,
  "labels": ["off", "low", "high"]
}
```

| Attribute        | Type            | Required | Description                                                                       |
| ---------------- | --------------- | -------- | --------------------------------------------------------------------------------- |
| `position_count` | int             | No       | Number of positions. Defaults to 2.                                               |
| `labels`         | list of strings | No       | Human-readable labels for each position. Must match `position_count` if provided. |

For a physical switch with a registry module, check the module's documentation
for required attributes.

### 3. Save and test

Click **Save**, then expand the **TEST** section.

- Read the current position.
- Set the switch to different positions and verify it responds correctly.

## Try it

Read the switch position, cycle through positions, and read labels.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
When you run the code below, you'll see the switch cycle through all positions. With the fake model, positions update in memory. With real hardware, verify the switch physically changes state.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `switch_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.switch import Switch


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    switch = Switch.from_robot(robot, "my-switch")

    # Get number of positions and labels
    num_positions, labels = await switch.get_number_of_positions()
    print(f"Positions: {num_positions}, Labels: {labels}")

    # Get current position
    position = await switch.get_position()
    print(f"Current position: {position}")

    # Cycle through all positions
    for pos in range(num_positions):
        await switch.set_position(pos)
        current = await switch.get_position()
        label = labels[pos] if labels else str(pos)
        print(f"Set to position {pos} ({label}), read back: {current}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python switch_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir switch-test && cd switch-test
go mod init switch-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    toggleswitch "go.viam.com/rdk/components/switch"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("switch-test")

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

    sw, err := toggleswitch.FromProvider(robot, "my-switch")
    if err != nil {
        logger.Fatal(err)
    }

    // Get number of positions and labels
    numPositions, labels, err := sw.GetNumberOfPositions(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Positions: %d, Labels: %v\n", numPositions, labels)

    // Get current position
    position, err := sw.GetPosition(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Current position: %d\n", position)

    // Cycle through all positions
    for pos := uint32(0); pos < numPositions; pos++ {
        if err := sw.SetPosition(ctx, pos, nil); err != nil {
            logger.Fatal(err)
        }
        current, err := sw.GetPosition(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }
        label := fmt.Sprintf("%d", pos)
        if int(pos) < len(labels) {
            label = labels[pos]
        }
        fmt.Printf("Set to position %d (%s), read back: %d\n", pos, label, current)
    }
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "SetPosition returns an error" >}}

- Verify the position value is within the valid range (0 to
  `GetNumberOfPositions - 1`).
- Check the module's documentation for any constraints on position changes.

{{< /expand >}}

{{< expand "GetPosition returns unexpected values" >}}

- Some physical switches may bounce between positions. Check if your module
  supports debouncing configuration.
- Verify the wiring matches the expected position mapping.

{{< /expand >}}

## What's next

- [Switch API reference](/dev/reference/apis/components/switch/): full method documentation.
- [What is a module?](/build-modules/from-hardware-to-logic/): write a module that
  responds to switch position changes.
- [Component types](/hardware/component-types/): find the right type for
  your hardware.
