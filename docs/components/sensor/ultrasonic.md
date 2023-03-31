---
title: "Configure an ultrasonic Sensor"
linkTitle: "ultrasonic"
weight: 60
draft: false
type: "docs"
description: "Configure an ultrasonic model sensor."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---

Configure an `ultrasonic` sensor to integrate a [An HC-S204 ultrasonic distance sensor](https://www.sparkfun.com/products/15569) into your robot.

Configure a `ultrasonic` sensor as follows:

{{< tabs >}}
{{% tab name="JSON Template" %}}

On the **COMPONENTS** subtab of your robot's page in [the Viam app](https://app.viam.com), navigate to the **Create Component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `ultrasonic` model.

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-ultrasonic-sensor-name>,
      "type": "sensor",
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": <number>
        "board": <your-board-name>
      },
      "depends_on": []
    },
  {
      "name": <your-board-name>,
      "type": "board",
      "model": <your-board-model>,
      "attributes": {
        "digital_interrupts": [
          {
            "name": <your-digital-interrupt-name>,
            "pin": <your-pin-number>
          }
        ]
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
        "echo_interrupt_pin": "your-digital-interrupt-name",
        "board": "your-board-name"
      },
      "depends_on": []
    },
    {
      "name": "your-board-name",
      "type": "board",
      "model": "pi",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "your-example-interrupt",
            "pin": "15"
          }
        ]
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

You must configure a digital interrupt as part of your [board's configuration](/components/board/#configuration) to configure this sensor.
See [here](/components/board/#digital-interrupts) for instructions on how to modify the Template or Example JSON to do so.

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `trigger_pin` | **Required** | The pin number on the board that you have connected [the sensor's trigger pin](https://components101.com/sensors/ultrasonic-sensor-working-pinout-datasheet). Example: `"5"`. |
| `echo_interrupt_pin` | **Required** | The name of the [digital interrupt](/components/board/#digital-interrupts) you have configured on your board that contains the pin number of the pin [the sensor's echo pin](https://components101.com/sensors/ultrasonic-sensor-working-pinout-datasheet) is connected to. Example: `"my-interrupt-1"`. |
| `board`  | **Required** | The `name` of the [board](/components/board) the sensor is connected to. |
| `timeout_ms`  | **Required** | Time to wait in milliseconds before timing out of getting a reading from the sensor. Default: `1000`. |

{{% alert title="Tip" color="Tip" %}}

An `trigger_pin` value of `5` would correspond to [Pin 5 GPIO 3](https://pinout.xyz/pinout/pin5_gpio3) on a Raspberry Pi.

{{% /alert %}}
