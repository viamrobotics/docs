---
title: "Control a motor in 60 seconds"
linkTitle: "Control a motor in 60 seconds"
type: "docs"
weight: 30
images: ["/icons/components/motor.svg"]
description: "Control a motor using Viam in just a few steps."
---

This guide will demonstrate how to control a motor using Viam in just a few steps. You can use Viam to control a motor's speed and direction directly from [the platform](https://app.viam.com/), [programatically](https://docs.viam.com/build/program/), or by using [the mobile app](/fleet/#the-viam-mobile-app).

To control your motor using Viam, refer to the following instructions:

{{< expand-and-search "Step 1: Configure a Board" >}}

First, [create a machine](/cloud/machines/#add-a-new-machine) if you haven't yet.

Then, [add a board component](/components/board/), such as a [Raspberry Pi board](/components/board/pi/).

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

{{< /expand-and-search >}}

{{< expand-and-search "Step 2: Configure a motor" >}}

[Add a motor component](/components/motor/), such as a [gpio motor](/components/motor/gpio/).
Ensure your motor, motor driver, and board are properly connected.

![The CONFIGURE tab of the Viam app populated with a configured gpio motor.](/components/motor/gpio-config-ui.png)

{{< /expand-and-search >}}

{{< expand-and-search "Step 3: Choose how you will control the motor" >}}

You can control your motor directly from Viam's user interface, programatically using an SDK, or using the mobile app.

1. Control from the app

2. Control programatically

You can use the following example code to control the motor's speed and direction using your preferred SDK:

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Set the motor power to 40% forward.
await my_motor.set_power(power=0.4)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Set the motor power to 40% forward.
myMotor.SetPower(context.Background(), 0.4, nil)

```

{{% /tab %}}
{{< /tabs >}}

3. Control from the mobile app

You can use [the Viam mobile app](/fleet/#the-viam-mobile-app) to control your motor's speed and direction directly from your smart device.

{{<gif webm_src="/fleet/mobile-app-control.webm" mp4_src="/fleet/mobile-app-control.mp4" alt="Using the control interface under the locations tab on the Viam mobile app" max-width="300px">}}

{{< /expand-and-search >}}
