---
linkTitle: "Gripper"
title: "Add a gripper"
weight: 45
layout: "docs"
type: "docs"
description: "Add and configure a gripper component to open, close, and grasp objects."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-gripper/
---

Add a gripper to your machine's configuration so you can open, close, and grasp objects from the Viam app and from code.

## Concepts

A gripper component controls a grasping device. The API provides:

- **Open**: opens the gripper fully.
- **Grab**: closes the gripper and reports whether it grabbed something.
- **IsHoldingSomething**: checks whether the gripper currently holds an object.
- **Stop**: stops any in-progress motion.

Gripper models almost always come from modules in the [Viam registry](https://app.viam.com/registry?type=component&subtype=gripper) because each
gripper has its own communication protocol and control logic. For example, the
[UFactory module](https://app.viam.com/module/viam/ufactory) includes gripper
models for xArm parallel-jaw and vacuum grippers.

The `fake` built-in model is useful for testing code without physical hardware.

### Built-in models

- [`fake`](/reference/components/gripper/fake/) — A model used for testing, with no physical hardware.

### Registry modules

For hardware the built-in models don't cover, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=gripper). Each module's configuration is documented on its registry page.

## Steps

### 1. Add a gripper component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your gripper hardware. Search by
   manufacturer name or gripper type (for example, "parallel jaw", "vacuum").
4. Name your gripper (for example, `my-gripper`) and click **Create**.

### 2. Configure gripper attributes

Attributes vary by module. For the `fake` model, no attributes are needed:

```json
{}
```

For a physical gripper, you'll typically configure the connection to the
gripper controller. Check your module's documentation for the full list of
attributes.

### 3. Configure a frame (recommended)

If you're using the gripper with an arm and motion planning, add a frame to
define the gripper's position relative to the arm:

```json
{
  "frame": {
    "parent": "my-arm",
    "translation": { "x": 0, "y": 0, "z": 0 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    }
  }
}
```

### 4. Save and test

Click **Save**, then expand the **Test** section.

- Click **Open** to open the gripper.
- Click **Grab** to close the gripper and check if it grabbed something.

{{< alert title="Safety" color="caution" >}}

Keep fingers and loose items clear of the gripper jaws when testing. Start
with no objects in the workspace until you're confident in the configuration.

{{< /alert >}}

## Try it

Open the gripper, grab an object, and check if it's held.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the same tab.
If you're using real hardware, you'll see the gripper open and close when you run the code below.
With the fake model, Grab always returns true.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `gripper_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.gripper import Gripper


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    gripper = Gripper.from_robot(robot, "my-gripper")

    # Open the gripper
    print("Opening gripper...")
    await gripper.open()
    print("Gripper opened")

    # Grab (close and check if something is held)
    print("Grabbing...")
    grabbed = await gripper.grab()
    print(f"Grabbed something: {grabbed}")

    # Check holding status
    status = await gripper.is_holding_something()
    print(f"Currently holding: {status.is_holding_something}")

    # Stop any motion
    await gripper.stop()

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python gripper_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir gripper-test && cd gripper-test
go mod init gripper-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/gripper"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("gripper-test")

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

    g, err := gripper.FromProvider(robot, "my-gripper")
    if err != nil {
        logger.Fatal(err)
    }

    // Open the gripper
    fmt.Println("Opening gripper...")
    if err := g.Open(ctx, nil); err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Gripper opened")

    // Grab (close and check if something is held)
    fmt.Println("Grabbing...")
    grabbed, err := g.Grab(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Grabbed something: %v\n", grabbed)

    // Check holding status
    status, err := g.IsHoldingSomething(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Currently holding: %v\n", status.IsHoldingSomething)

    // Stop any motion
    if err := g.Stop(ctx, nil); err != nil {
        logger.Fatal(err)
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

{{< expand "Gripper doesn't open or close" >}}

- Verify the gripper is powered and connected.
- Check the module's logs for communication errors.
- If the gripper uses a serial connection, verify the device path and baud
  rate in the attributes.

{{< /expand >}}

{{< expand "Grab always returns false" >}}

- Some gripper models detect a grab by measuring force or current. If the
  gripper closes fully without resistance, it reports no grab.
- With the `fake` model, `Grab` always returns `true`.

{{< /expand >}}

{{< expand "Gripper moves too fast or too slow" >}}

- Check your module's documentation for speed or force configuration
  attributes.
- Some grippers support configurable open/close speed and grip force.

{{< /expand >}}

{{< readfile "/static/include/components/troubleshoot/gripper.md" >}}

## What's next

- [Gripper API reference](/reference/apis/components/gripper/): full method documentation.
- [Add an arm](/hardware/common-components/add-an-arm/): configure the arm
  the gripper is mounted on.
- [Fragments](/hardware/fragments/): save and reuse working
  hardware configurations.
- [What is a module?](/build-modules/overview/): write a module that
  coordinates the gripper with a camera for pick-and-place.
