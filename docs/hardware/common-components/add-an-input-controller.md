---
linkTitle: "Input controller"
title: "Add an input controller"
weight: 50
layout: "docs"
type: "docs"
description: "Add and configure a gamepad, joystick, or other input device for manual machine control."
date: "2025-03-07"
aliases:
  - /hardware-components/add-an-input-controller/
---

Add an input controller to your machine's configuration so you can use a gamepad, joystick, or other input device to control your machine.

## Concepts

An input controller component reads events from human input devices: button
presses, joystick axis movements, and trigger pulls. Your code registers
callbacks for these events and translates them into machine actions.

### Built-in models

| Model        | Use case                                                                                                                     |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `gamepad`    | USB gamepad or joystick. Works with most HID-compatible controllers.                                                         |
| `webgamepad` | Browser-based gamepad input in the Viam app's CONTROL tab. No physical controller needed.                                    |
| `gpio`       | Buttons and switches wired to GPIO pins on a board.                                                                          |
| `mux`        | Multiplexes multiple input controllers, allowing one to override another (for example, safety controller overrides gamepad). |

Browse all available input controller models in the [Viam registry](https://app.viam.com/registry?type=component&subtype=input_controller).

## Steps

### Option A: USB gamepad

#### 1. Add an input controller component

1. Plug your gamepad into the machine's USB port.
2. Click the **+** button.
3. Select **Configuration block**.
4. Search for **gamepad**. This is the built-in model for USB game
   controllers.
5. Name it (for example, `my-gamepad`) and click **Create**.

#### 2. Configure attributes

The `gamepad` model typically needs no attributes. It auto-detects the
connected controller.

If you have multiple controllers, specify which one:

```json
{
  "dev_file": "/dev/input/event0"
}
```

### Option B: Web gamepad

#### 1. Add a webgamepad component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for **webgamepad**. This model provides browser-based
   controls in the Viam app.
4. Name it (for example, `web-controller`) and click **Create**.

No attributes needed. The web gamepad appears in the Viam app's CONTROL tab
and works with browser-compatible game controllers or on-screen controls.

### Option C: GPIO buttons

#### 1. Prerequisites

- A [board component](/hardware/common-components/add-a-board/) is configured.
- Buttons or switches are wired to GPIO pins.

#### 2. Add and configure

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for **gpio input controller**. This model maps GPIO pins to
   controller buttons.
4. Name it and click **Create**.
5. Configure the pins:

```json
{
  "board": "my-board",
  "buttons": {
    "ButtonNorth": "11",
    "ButtonSouth": "13"
  }
}
```

### Save and test

Click **Save**, then expand the **TEST** section.

- The test panel shows all available controls (buttons, axes).
- Press buttons or move joystick axes. Events should appear in real time.

## Try it

List available controls and print events as they happen.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
When you run the code below, press buttons on your gamepad and watch the events print in real time.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `input_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.input import Controller, Control, EventType


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    controller = Controller.from_robot(robot, "my-gamepad")

    # List available controls
    controls = await controller.get_controls()
    print(f"Available controls: {controls}")

    # Get current state of all events
    events = await controller.get_events()
    for control, event in events.items():
        print(f"  {control}: {event.value}")

    # Register a callback for button presses
    def handle_press(event):
        print(f"Button {event.control} {event.event}: value={event.value}")

    controller.register_control_callback(
        Control.BUTTON_START,
        [EventType.BUTTON_PRESS, EventType.BUTTON_RELEASE],
        handle_press,
    )

    print("\nPress buttons on the gamepad (Ctrl+C to stop)...")
    # Keep running to receive callbacks
    await asyncio.sleep(30)

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python input_test.py
```

Press buttons on your gamepad and watch the events print.

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir input-test && cd input-test
go mod init input-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "time"

    "go.viam.com/rdk/components/input"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("input-test")

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

    controller, err := input.FromProvider(robot, "my-gamepad")
    if err != nil {
        logger.Fatal(err)
    }

    // List available controls
    controls, err := controller.Controls(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Available controls: %v\n", controls)

    // Get current state
    events, err := controller.Events(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    for control, event := range events {
        fmt.Printf("  %s: %.2f\n", control, event.Value)
    }

    // Register a callback for the Start button
    err = controller.RegisterControlCallback(
        ctx,
        input.ButtonStart,
        []input.EventType{input.ButtonPress, input.ButtonRelease},
        func(ctx context.Context, event input.Event) {
            fmt.Printf("Button %s %s: value=%.2f\n",
                event.Control, event.Event, event.Value)
        },
        nil,
    )
    if err != nil {
        logger.Fatal(err)
    }

    fmt.Println("\nPress buttons on the gamepad (waiting 30s)...")
    time.Sleep(30 * time.Second)
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Gamepad not detected" >}}

- Check the USB connection. Try a different USB port.
- On Linux, verify the device exists: `ls /dev/input/event*` or
  `ls /dev/input/js*`.
- Some controllers need drivers. Check if the controller works with other
  Linux applications first.

{{< /expand >}}

{{< expand "Buttons or axes map to wrong controls" >}}

- Different gamepad manufacturers use different button/axis mappings.
  Use the test panel to identify which physical button maps to which
  control name, then update your callback registrations accordingly.

{{< /expand >}}

## What's next

- [Input controller API reference](/dev/reference/apis/components/input-controller/): full method documentation.
- [Add a Base](/hardware/common-components/add-a-base/): drive a mobile robot
  with your gamepad.
- [What is a module?](/build-modules/overview/): write a module that
  translates gamepad input into machine actions.
