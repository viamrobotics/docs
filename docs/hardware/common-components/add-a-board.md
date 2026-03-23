---
linkTitle: "Board"
title: "Add a board"
weight: 15
layout: "docs"
type: "docs"
description: "Add and configure a board component to expose GPIO pins, analog readers, and digital interrupts."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-board/
---

Add a board to your machine's configuration so other components can use your single-board computer's GPIO pins, analog readers, and digital interrupts.

## Concepts

A board component exposes the low-level I/O on your single-board computer:

- **GPIO pins**: digital output (high/low) and PWM.
- **Analog readers**: read analog voltage values from ADC-capable pins.
- **Digital interrupts**: react to signal changes on a pin.

The board doesn't represent external hardware. It represents the I/O
capabilities of the computer itself. Motors, encoders, and servos reference
the board by name to access the pins they're wired to.

## Steps

### 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.

### 2. Add a board component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your single-board computer:
   - For a Raspberry Pi (any model), search for **pi**.
   - For an NVIDIA Jetson, search for **jetson**.
   - For an Orange Pi, search for **orangepi**.
4. Name your board (e.g., `my-board`) and click **Create**.

### 3. Configure board attributes

For most single-board computers, the board works with **no additional
configuration**. The model auto-detects available pins.

If you need analog readers or digital interrupts, add them in the attributes:

**Analog readers:**

```json
{
  "analogs": [
    {
      "name": "my-analog",
      "pin": "32",
      "spi_bus": "main",
      "chip_select": "0",
      "channel": 0
    }
  ]
}
```

**Digital interrupts:**

```json
{
  "digital_interrupts": [
    {
      "name": "my-interrupt",
      "pin": "37"
    }
  ]
}
```

### 4. Save the configuration

Click **Save** in the upper right. `viam-server` initializes the board
immediately. No restart needed.

### 5. Test the board

1. Find your board in the configuration view.
2. Expand the **TEST** section.
3. Try setting a GPIO pin high or low, or read an analog value.

If you have an LED wired to a GPIO pin, setting the pin high should light
it up.

## Try it

Toggle a GPIO pin and read its state programmatically.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
If you have an LED wired to pin 11, you'll see it turn on and off when you run the code below.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `board_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.board import Board


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    board = Board.from_robot(robot, "my-board")
    pin = await board.gpio_pin_by_name("11")

    await pin.set(True)
    state = await pin.get()
    print(f"Pin 11 is {'high' if state else 'low'}")

    await pin.set(False)
    state = await pin.get()
    print(f"Pin 11 is {'high' if state else 'low'}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python board_test.py
```

You should see:

```text
Pin 11 is high
Pin 11 is low
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir board-test && cd board-test
go mod init board-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/board"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("board-test")

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

    myBoard, err := board.FromProvider(robot, "my-board")
    if err != nil {
        logger.Fatal(err)
    }

    pin, err := myBoard.GPIOPinByName("11")
    if err != nil {
        logger.Fatal(err)
    }

    if err := pin.Set(ctx, true, nil); err != nil {
        logger.Fatal(err)
    }
    state, err := pin.Get(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Pin 11 is high: %v\n", state)

    if err := pin.Set(ctx, false, nil); err != nil {
        logger.Fatal(err)
    }
    state, err = pin.Get(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Pin 11 is high: %v\n", state)
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Board model not available" >}}

- Linux boards are detected at runtime. If your SBC isn't recognized, check
  that `viam-server` is running on the SBC itself (not on a different machine).
- Confirm you're using a supported OS.
  See [device setup](/reference/device-setup/) for supported platforms.

{{< /expand >}}

{{< expand "GPIO pin doesn't respond" >}}

- Verify the pin number matches your board's pinout diagram. Viam uses the
  **board pin number** (the physical pin on the header), not the GPIO/BCM
  number.
- Check that nothing else on the system is using the pin (another process,
  a kernel driver).

{{< /expand >}}

{{< expand "Analog reader returns unexpected values" >}}

- Most SBCs don't have built-in ADCs. You may need an external ADC connected
  via SPI or I2C. Check the model's reference page for ADC configuration.

{{< /expand >}}

## What's next

- [Board API reference](/dev/reference/apis/components/board/): full method documentation.
- [Add a Motor](/hardware/common-components/add-a-motor/): wire a motor to your
  board's GPIO pins.
- [Add an Encoder](/hardware/common-components/add-an-encoder/): wire an encoder to
  your board's interrupt pins.
- [Add a Servo](/hardware/common-components/add-a-servo/): control a servo from a
  PWM-capable pin.
