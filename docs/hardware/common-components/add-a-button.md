---
linkTitle: "Button"
title: "Add a button"
weight: 20
layout: "docs"
type: "docs"
description: "Add and configure a button component to detect presses from a physical button."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-button/
---

Add a button to your machine's configuration so you can detect and respond to button presses from the Viam app and from code.

## Concepts

A button component represents a momentary push button. The API is intentionally
simple. It exposes a single `Push` method that triggers the button. Physical button
hardware typically comes from a **module in the registry** that reads a GPIO pin
and exposes it as a button component.

The `fake` built-in model is useful for testing code without physical hardware.

## Steps

### 1. Add a button component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your button hardware. Search by
   manufacturer name, chip, or device type.
4. Name your button (e.g., `my-button`) and click **Create**.

### 2. Configure button attributes

Attributes vary by module. For the `fake` model, no attributes are needed:

```json
{}
```

For a GPIO-connected button via a registry module, you'll typically configure
the board and pin:

```json
{
  "board": "my-board",
  "pin": "22"
}
```

Check your module's documentation in the registry for the full list of
attributes.

### 3. Save and test

Click **Save**, then expand the **TEST** section.

- Click **Push** to simulate pressing the button.

## Try it

Push the button programmatically.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
When you run the code below, the button's Push method fires. With a physical button connected via a module, this triggers whatever action the module defines.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `button_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.button import Button


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    button = Button.from_robot(robot, "my-button")

    # Push the button
    print("Pushing button...")
    await button.push()
    print("Button pushed")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python button_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir button-test && cd button-test
go mod init button-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/button"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("button-test")

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

    b, err := button.FromProvider(robot, "my-button")
    if err != nil {
        logger.Fatal(err)
    }

    // Push the button
    fmt.Println("Pushing button...")
    if err := b.Push(ctx, nil); err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Button pushed")
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Button push doesn't trigger anything" >}}

- Verify the button component shows as connected in the Viam app.
- If using a GPIO-connected button, check the wiring and pin number.
- Test the button from the Viam app's test panel first.

{{< /expand >}}

{{< expand "Button module not found" >}}

- Confirm you've added the module to your machine's configuration.
- Check that the module is running. Look for it in the machine's logs.

{{< /expand >}}

## What's next

- [Button API reference](/dev/reference/apis/components/button/): full method documentation.
- [What is a module?](/build-modules/from-hardware-to-logic/): write a module that
  responds to button presses.
- [Component types](/hardware/component-types/): find the right type for
  your hardware.
