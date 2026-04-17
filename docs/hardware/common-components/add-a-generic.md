---
linkTitle: "Generic"
title: "Add a generic component"
weight: 40
layout: "docs"
type: "docs"
description: "Add and configure a generic component for hardware that doesn't fit any other component type."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-generic/
---

Add a generic component to your machine's configuration for hardware that doesn't fit any standard component type.

## Concepts

A generic component is a catch-all for hardware with non-standard interfaces.
The API provides a single method:

- **DoCommand**: send arbitrary key-value commands to the component and
  receive key-value responses.

Because the API is entirely model-defined, generic components almost always
come from **modules in the registry** (or modules you write yourself). The
module author defines what commands are supported and what they do.

Use generic when no other component type fits. If your hardware produces images, use [camera](/hardware/common-components/add-a-camera/). If it produces readings, use [sensor](/hardware/common-components/add-a-sensor/). Standard types give you typed SDK methods like `GetImage` or `GetReadings`, richer test-panel controls tailored to the component, and motion or vision services that know how to work with them. Generic exposes only `DoCommand`, so callers have to know the module-specific command shape.

Browse available generic models in the [Viam registry](https://app.viam.com/registry?type=component&subtype=generic).

The `fake` built-in model echoes commands back for testing.

### Built-in models

- [`fake`](/reference/components/generic/fake/) — A model used for testing, with no physical hardware.

### Registry modules

For hardware the built-in models don't cover, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=generic). Each module's configuration is documented on its registry page.

## Steps

### 1. Add a generic component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your hardware. Search by
   manufacturer name, chip, or device type.
4. Name your component (for example, `my-device`) and click **Create**.

If no model exists for your hardware, you can
[write your own module](/build-modules/write-a-driver-module/) that implements
the generic component API.

### 2. Configure attributes

Attributes are entirely model-defined. For the `fake` model, no attributes
are needed:

```json
{}
```

For a registry module, check the module's documentation for required
attributes.

### 3. Save and test

Click **Save**. Generic components can be tested using `DoCommand` from code
or the Viam app's test panel.

## Try it

Send a command to the generic component and read the response.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the **Connection details** section on the same tab.
With the fake model, you'll see your command echoed back. With a real module, the response depends on what commands the module supports.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `generic_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.generic import Generic


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    device = Generic.from_robot(robot, "my-device")

    # Send a command (the fake model echoes it back)
    result = await device.do_command({"action": "status", "verbose": True})
    print(f"Response: {result}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python generic_test.py
```

With the `fake` model, you'll see your command echoed back:

```text
Response: {'action': 'status', 'verbose': True}
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir generic-test && cd generic-test
go mod init generic-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/generic"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("generic-test")

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

    device, err := generic.FromProvider(robot, "my-device")
    if err != nil {
        logger.Fatal(err)
    }

    // Send a command (the fake model echoes it back)
    result, err := device.DoCommand(ctx, map[string]interface{}{
        "action":  "status",
        "verbose": true,
    })
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Response: %v\n", result)
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "DoCommand returns an error" >}}

- Verify the command format matches what the module expects. Check the module's
  documentation for supported commands and their expected structure.
- With the `fake` model, any valid map is accepted.

{{< /expand >}}

{{< expand "Module not found or not loading" >}}

- Confirm you've added the module to your machine's configuration.
- Check that the module is compatible with your machine's architecture.
- Look at the machine's logs for module startup errors.

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/generic.md" >}}

## Related

- [Generic API reference](/reference/apis/components/generic/): full method documentation.
- [Write a module](/build-modules/write-a-driver-module/): create a
  module for your custom hardware.
- [Add a component](/hardware/common-components/): check if a more specific
  component type fits your hardware before using generic.
