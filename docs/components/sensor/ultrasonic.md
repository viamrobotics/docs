---
title: "Configure an ultrasonic Sensor"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic model sensor."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---

Configure an `ultrasonic` sensor to integrate an [HC-S204 ultrasonic distance sensor](https://www.sparkfun.com/products/15569) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `ultrasonic` model.

Click **Create component**.
Paste into the **Attributes** box:

``` json
{
  "trigger_pin": "<number>",
  "echo_interrupt_pin": "<number>"
  "board": <your-board-name>,
  "timeout_ms": <number>
}
```

![Creation of a ultrasonic sensor in the Viam app config builder.](../img/ultrasonic-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-ultrasonic-sensor-name>,
      "type": "sensor",
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": <"number">,
        "echo_interrupt_pin": <"number">,
        "board": <your-board-name>,
        "timeout_ms": <number>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "your-ultrasonic-sensor",
      "type": "sensor",
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": "5",
        "echo_interrupt_pin": "15",
        "board": "your-board-name",
        "timeout_ms": "1000"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `ultrasonic` sensors:

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `trigger_pin` | **Required** | The pin number on the board that you have connected [the sensor's trigger pin](https://www.sparkfun.com/products/15569). <br> Example: `"5"`. |
| `echo_interrupt_pin` | **Required** | The pin number of the pin [the sensor's echo pin](https://www.sparkfun.com/products/15569) is connected to. If you have already created a [digital interrupt](/components/board/#digital_interrupts) for this pin in the [board's configuration](/components/board), use that digital interrupt's `name` instead. <br> Example: `"15"`. |
| `board`  | **Required** | The `name` of the [board](/components/board) the sensor is connected to. |
| `timeout_ms`  | Optional | Time to wait in milliseconds before timing out of requesting to get readings from the sensor. <br> Default: `1000`. |

{{% alert title="Tip" color="tip" %}}

A `trigger_pin` value of `"5"` corresponds to [Pin 5 GPIO 3](https://pinout.xyz/pinout/pin5_gpio3) on a Raspberry Pi.

{{% /alert %}}
