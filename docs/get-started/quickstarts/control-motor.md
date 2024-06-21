---
title: "Control a motor in 2 minutes"
linkTitle: "Control a motor in 2 minutes"
type: "docs"
weight: 30
cost: 75
images: ["/icons/components/motor.svg"]
description: "Use Viam to control a motor's speed and direction in just a few steps."
---

You can use Viam to control a motor's speed and direction directly from [the Viam app](https://app.viam.com/), [the mobile app](/fleet/#the-viam-mobile-app), or [programatically](https://docs.viam.com/build/program/).

### Requirements

- A board with a supported OS installed (such as Raspberry Pi)
- A motor connected to the board
- A motor driver (optional)

Follow these steps to control your motor:

{{< expand "Step 1: Create a machine" >}}

Go to the Viam app and [add a new machine](/cloud/machines/#add-a-new-machine).

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}

{{< expand "Step 2: Configure a Board" >}}

Then, [add a board component](/components/board/), such as a [Raspberry Pi board](/components/board/pi/).

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

{{< /expand >}}

{{< expand "Step 3: Configure a motor" >}}

[Add a motor component](/components/motor/), such as a [gpio motor](/components/motor/gpio/).
Ensure your motor, motor driver, and board are properly connected.

![The CONFIGURE tab of the Viam app populated with a configured gpio motor.](/components/motor/gpio-config-ui.png)

{{< /expand >}}

{{< expand "Step 4: Choose how you will control the motor" >}}

You can control your motor directly from the Viam app, using the mobile app, or programatically.

1. Control from the app

   Navigate to your machine's **CONTROL** tab in the Viam app and use the **Power %** slider to set the motors speed.
   Use the **Backwards** and **Forwards** buttons to change the direction.

   {{<gif webm_src="/get-started/quickstarts/motor-control.webm" mp4_src="/get-started/quickstarts/motor-control.mp4" alt="Using the slider, Backwards, and Forwards buttons on the Viam app to control the direction and speed of a configured motor" class="aligncenter"  min-height="750px">}}

2. Control from the mobile app

   You can use [the Viam mobile app](/fleet/#the-viam-mobile-app) to control your motor's speed and direction directly from your smart device.

   Open the Viam mobile app and log in to your account.
   Select the location where your machine is assigned.
   Choose your machine from the list and use the mobile interface to adjust the motor settings.

   Select the location that your machine is assigned to from the **Locations** tab.

   {{<gif webm_src="/get-started/quickstarts/mobile-app-motor-control.webm" mp4_src="/get-started/quickstarts/mobile-app-motor-control.mp4" alt="Using an example machine on the Viam mobile app to set the direction and speed of a configured motor using the slider on the user interface" max-height="50px" max-width="200px" class="HELLO aligncenter">}}

3. Control programatically

   You can use the following code to control the motor's speed and direction using your preferred SDK:

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.motor import Motor


async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's api key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's api
        # key id
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address(
        'my-machine-main.1ye34y6p21.viam.cloud', opts)


async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)

    # motor-1
    motor_1 = Motor.from_robot(machine, "motor-1")
    # Turn the motor 7.2 revolutions at 60 RPM.
    await motor_1.go_for(rpm=60, revolutions=7.2)
    print(f"motor-1 is_moving return value: {motor_1_return_value}")

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

  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/utils/rpc"
  "go.viam.com/rdk/components/motor")

func main() {
   logger := logging.NewDebugLogger("client")
  machine, err := client.New(
    context.Background(),
    "my-machine-main.1ye34y6p21.viam.cloud",
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
      /* Replace "<API-KEY-ID>" (including brackets) with your machine's api key id */
      "<API-KEY-ID>",
      rpc.Credentials{
        Type:    rpc.CredentialsTypeAPIKey,
        /* Replace "<API-KEY>" (including brackets) with your machine's api key */
        Payload: "<API-KEY>",
      })),
  )
  if err != nil {
    logger.Fatal(err)
  }

  defer machine.Close(context.Background())
  logger.Info("Resources:")
  logger.Info(machine.ResourceNames())


    // motor-1
    motor1Component, err:= motor.FromRobot(machine, "motor-1")
    if err!=nil {
      logger.Error(err)
      return
    }
    // Turn the motor 7.2 revolutions at 60 RPM.
    motor1Component.GoFor(context.Background(), 60, 7.2, nil)
    if err!=nil {
      logger.Error(err)
      return
    }
    logger.Infof("motor-1 IsMoving return value: %+v", motor1ReturnValue)
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

## Next steps

Now that you have made a motor move, explore other components, or related servies:

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
