---
title: "Control a motor in 2 minutes"
linkTitle: "Control a motor in 2 minutes"
type: "docs"
weight: 30
cost: 75
images: ["/icons/components/motor.svg"]
description: "Use Viam to control a motor's speed and direction in just a few steps."
---

You can use Viam to control a motor's speed and direction directly from [the Viam app](https://app.viam.com/), [the mobile app](/fleet/#the-viam-mobile-app), or [programmatically](/build/program/).

## Requirements

- A single-board computer with a supported OS installed (such as Raspberry Pi)
- A motor and compatible motor driver connected to the board
- A power supply for the board
- A separate power supply for the motor

Follow these steps to control your motor:

{{< expand "Step 1: Create a machine" >}}

Go to the Viam app.
Select a location and [add a new machine](/cloud/machines/#add-a-new-machine).
Click the name of your machine to go to that machine's page.

{{< /expand >}}
{{%expand "Step 2: Install viam-server" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer and connect it to the Viam app.

{{% /expand%}}
{{< expand "Step 3: Configure a board" >}}

Then, [add a board component](/components/board/).

Look through the [**Supported Models**](/components/motor/#supported-models) to determine the model of component to configure.
For example, configure a [`pi` board](/components/board/pi/) for a Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero 2 W:

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/get-started/quickstarts/configure-pi.png)

Follow the instructions in the board model's documentation to configure any required attributes.

{{< /expand >}}
{{< expand "Step 4: Configure a motor" >}}

[Add a motor component](/components/motor/) that represents the type of motor and motor driver you're using.
Look through the [**Supported Models**](/components/motor/#supported-models) to determine the model of component to configure.
For example, configure a [`gpio` motor](/components/motor/gpio/) to represent a standard DC motor (both brushed and brushless):

![The CONFIGURE tab of the Viam app populated with a configured gpio motor.](/get-started/quickstarts/configure-motor.png)

Follow the instructions in the model's documentation to configure the attributes and ensure your motor, motor driver, and board are properly wired together so that the computer can connect with the motor.

{{< /expand >}}
{{< expand "Step 5: Choose how you will control the motor" >}}

You can control your motor directly from the Viam app, using the mobile app, or programmatically.

### Option 1: Control from the app

Navigate to your machine's **CONTROL** tab in the Viam app and use the **Power %** slider to set the motor's speed.
Use the **Backwards** and **Forwards** buttons to change the direction.

{{<gif webm_src="/get-started/quickstarts/motor-control.webm" mp4_src="/get-started/quickstarts/motor-control.mp4" alt="Using the slider, Backwards, and Forwards buttons on the Viam app to control the direction and speed of a configured motor" class="aligncenter"  min-height="750px">}}

### Option 2: Control from the mobile app

You can use [the Viam mobile app](/fleet/#the-viam-mobile-app) to control your motor's speed and direction directly from your smart device.

Open the Viam mobile app and log in to your account.
Select the location where your machine is assigned.
Choose your machine from the list and use the mobile interface to adjust the motor settings.

Select the location that your machine is assigned to from the **Locations** tab.

{{<gif webm_src="/get-started/quickstarts/mobile-app-motor-control.webm" mp4_src="/get-started/quickstarts/mobile-app-motor-control.mp4" alt="Using an example machine on the Viam mobile app to set the direction and speed of a configured motor using the slider on the user interface" max-height="50px" max-width="200px" class="HELLO aligncenter">}}

### Option 3: Control programmatically

You can use the following code to control the motor's speed and direction using your preferred SDK.
Find your machine's API key and address on your machine's **CONNECT** tab.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
import time

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.motor import Motor


async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's API
        # key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address(
        '<YOUR MACHINE ADDRESS>', opts)


async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)

    # Instantiate the motor client
    motor_1 = Motor.from_robot(machine, "motor-1")
    # Turn the motor at 35% power forwards
    await motor_1.set_power(power=0.35)
    # Let the motor spin for 4 seconds
    time.sleep(4)
    # Stop the motor
    await motor_1.stop()

    # Don't forget to close the machine when you're done!
    await machine.close()


if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
  "context"
  "time"

  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/utils/rpc"
  "go.viam.com/rdk/components/motor")

func main() {
  logger := logging.NewDebugLogger("client")
  machine, err := client.New(
    context.Background(),
    // Replace "<YOUR MACHINE ADDRESS>" (including brackets) with your machine's address
    "<YOUR MACHINE ADDRESS>",
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
      // Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
      "<API-KEY-ID>",
      rpc.Credentials{
        Type:    rpc.CredentialsTypeAPIKey,
        // Replace "<API-KEY>" (including brackets) with your machine's API key
        Payload: "<API-KEY>",
      })),
  )
  if err != nil {
    logger.Fatal(err)
  }

  defer machine.Close(context.Background())
  logger.Info("Resources:")
  logger.Info(machine.ResourceNames())


  // Instantiate the motor client
  motor1Component, err:= motor.FromRobot(machine, "motor-1")
  if err != nil {
    logger.Error(err)
    return
  }
  // Turn the motor at 35% power forwards
  err = motor1Component.SetPower(context.Background(), 0.35, nil)
  if err != nil {
    logger.Error(err)
    return
  }
  // Let the motor spin for 4 seconds
  time.Sleep(4 * time.Second)
  // Stop the motor
  err = motor1Component.Stop(context.Background(), nil)
  if err != nil {
    logger.Error(err)
    return
  }
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

## Next steps

Now that you have made a motor move, explore other components or related services:

{{< cards >}}
{{% card link="/components/" %}}
{{% card link="/services/navigation/" %}}
{{% card link="/services/SLAM/" %}}
{{< /cards >}}

To see motors in real-world projects, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/confetti-bot/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/configure/configure-rover/" %}}
{{< /cards >}}
