---
linkTitle: "Encoder"
title: "Add an encoder"
weight: 30
layout: "docs"
type: "docs"
description: "Add and configure an encoder to track motor position and direction."
date: "2025-03-07"
aliases:
  - /hardware-components/add-an-encoder/
---

Add an encoder to your machine's configuration so you can track motor position and direction from the Viam app and from code.

## Concepts

Encoders come in two main varieties:

- **Incremental (quadrature)**: two signal channels (A and B) let Viam
  determine both position and direction. This is the most common type.
- **Single-channel**: one signal channel tracks position but can't determine
  direction on its own.

Both connect to a board's GPIO pins as digital interrupts. The encoder counts
signal transitions ("ticks") that correspond to motor shaft rotation.

Once you configure an encoder and reference it from a motor component, the
motor gains accurate position control. `GoFor` and `GoTo` use actual encoder
feedback instead of time-based estimates. Browse all available encoder models in the [Viam registry](https://app.viam.com/registry?type=component&subtype=encoder).

### Built-in models

- [`fake`](/reference/components/encoder/fake/) — An encoder model for testing.
- [`incremental`](/reference/components/encoder/incremental/) — Supports a two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point.
- [`single`](/reference/components/encoder/single/) — A single pin 'pulse output' encoder which returns its relative position but no direction.

Micro-RDK:

- [`incremental`](/reference/components/encoder/micro-rdk/incremental/) — _(no description)_.
- [`single`](/reference/components/encoder/micro-rdk/single/) — _(no description)_.

### Registry modules

For hardware the built-in models don't cover, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=encoder). Each module's configuration is documented on its registry page.

## Steps

### 1. Prerequisites

- Your machine is online in the Viam app.
- A [board component](/hardware/common-components/add-a-board/) is configured.
- Your encoder is wired to the board's GPIO pins.

### 2. Add an encoder component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the encoder model that matches your hardware:
   - For a two-channel quadrature encoder, search for **incremental**.
   - For a single-channel encoder, search for **single encoder**.
4. Name your encoder (for example, `left-encoder`) and click **Create**.

### 3. Configure encoder attributes

**Incremental (quadrature) encoder:**

```json
{
  "board": "my-board",
  "pins": {
    "a": "37",
    "b": "35"
  }
}
```

| Attribute | Type   | Required | Description                  |
| --------- | ------ | -------- | ---------------------------- |
| `board`   | string | Yes      | Name of the board component. |
| `pins.a`  | string | Yes      | GPIO pin for channel A.      |
| `pins.b`  | string | Yes      | GPIO pin for channel B.      |

**Single-channel encoder:**

```json
{
  "board": "my-board",
  "pins": {
    "i": "37"
  }
}
```

| Attribute | Type   | Required | Description                      |
| --------- | ------ | -------- | -------------------------------- |
| `board`   | string | Yes      | Name of the board component.     |
| `pins.i`  | string | Yes      | GPIO pin for the signal channel. |

### 4. Link the encoder to a motor

After creating the encoder, update your motor's configuration to reference it:

```json
{
  "board": "my-board",
  "max_rpm": 200,
  "pins": { "a": "11", "b": "13", "pwm": "15" },
  "encoder": "left-encoder",
  "ticks_per_rotation": 600
}
```

`ticks_per_rotation` is the number of encoder ticks in one full rotation of
the motor shaft. Check your encoder's datasheet. Common values are 12, 48,
200, or 600 depending on the encoder type and any gearing.

### 5. Save and test

Click **Save**, then expand the **Test** section for the encoder.

- Manually rotate the motor shaft. The tick count should change.
- Rotating in one direction should increase the count; the other direction
  should decrease it (with an incremental encoder).

Then test the motor. `GoFor` should now stop accurately at the target
position.

## Try it

Read the encoder position and reset it.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the same tab.
When you run the code below, you'll see the encoder's current position, then reset it to zero. Manually rotate the motor shaft to verify the count changes.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `encoder_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.encoder import Encoder


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    encoder = Encoder.from_robot(robot, "left-encoder")

    position, pos_type = await encoder.get_position()
    print(f"Position: {position} ({pos_type})")

    properties = await encoder.get_properties()
    print(f"Ticks count supported: {properties.ticks_count_supported}")
    print(f"Angle degrees supported: {properties.angle_degrees_supported}")

    await encoder.reset_position()
    print("Position reset to zero")

    position, pos_type = await encoder.get_position()
    print(f"Position after reset: {position}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python encoder_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir encoder-test && cd encoder-test
go mod init encoder-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/encoder"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("encoder-test")

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

    enc, err := encoder.FromProvider(robot, "left-encoder")
    if err != nil {
        logger.Fatal(err)
    }

    position, posType, err := enc.Position(ctx, encoder.PositionTypeUnspecified, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Position: %.2f (%v)\n", position, posType)

    properties, err := enc.Properties(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Ticks count supported: %v\n", properties.TicksCountSupported)
    fmt.Printf("Angle degrees supported: %v\n", properties.AngleDegreesSupported)

    if err := enc.ResetPosition(ctx, nil); err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Position reset to zero")
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Encoder count doesn't change" >}}

- Verify the wiring: check that the encoder's power, ground, and signal pins
  are connected correctly.
- Confirm the GPIO pin numbers match your wiring. Use the board test panel to
  check that the pins register changes when you rotate the shaft.

{{< /expand >}}

{{< expand "Count always increases (never decreases)" >}}

- This happens with single-channel encoders, which can't detect direction.
  If you need direction sensing, use an incremental (quadrature) encoder.

{{< /expand >}}

{{< expand "Position is inaccurate or drifts" >}}

- Check `ticks_per_rotation`. If it's wrong, the motor will overshoot or
  undershoot targets. Count actual ticks for one full shaft rotation to verify.
- Try swapping the `a` and `b` pins. If they're reversed, the encoder may
  count in the wrong direction.

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/encoder.md" >}}

## What's next

- [Encoder API reference](/reference/apis/components/encoder/): full method documentation.
- [Add a Motor](/hardware/common-components/add-a-motor/): configure the motor that
  this encoder monitors.
- [Add a Base](/hardware/common-components/add-a-base/): use motors with encoders
  for accurate odometry on a wheeled base.
