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

On the **COMPONENTS** subtab of your robot's page in [the Viam app](https://app.viam.com), navigate to the **Create Component** menu.

1. Configure your [board](/components/board).
    Enter a name for your board, select the type `board`, and select the appropriate model.
    Paste  `"digital_interrupts"` into the **Attributes** section:

    ``` json
    "digital_interrupts": [
      {
        "name": <your-digital-interrupt-name>,
        "pin": <your-pin-number>
      }
    ]
    ```

    Replace `"name"` with a name of your choosing, and `"pin"` with the number of the pin on your board you have connected your sensor's echo pin to.
    For example:

    ![Creation of a ultrasonic sensor's board with digital interrupts configured in the Viam app config builder.](../img/ultrasonic-sensor-board-ui-config.png)

2. Configure your sensor.
    Enter a name for your sensor, select the type `sensor`, and select the `ultrasonic` model.
    Paste your `"trigger_pin"`, `"echo_interrupt_pin"`, and `"board"` into the **Attibutes** section.
    For example:

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
        "trigger_pin": <number>,
        "echo_interrupt_pin": <your-digital-interrupt-name>,
        "board": <your-board-name>,
        "timeout_ms": <number>
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
        "echo_interrupt_pin": "your-example-echo-interrupt",
        "board": "your-board-name",
        "timeout_ms": "1000"
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
            "name": "your-example-echo-interrupt",
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

You must [configure a digital interrupt](/components/board/#digital-interrupts) as part of your [board's configuration](/components/board/#configuration) to configure this sensor.

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `trigger_pin` | **Required** | The pin number on the board that you have connected [the sensor's trigger pin](https://www.sparkfun.com/products/15569). Example: `"5"`. |
| `echo_interrupt_pin` | **Required** | The `name` of the [digital interrupt](/components/board/#digital-interrupts) you have configured on your board that contains the pin number of the pin [the sensor's echo pin](https://www.sparkfun.com/products/15569) is connected to. Example: `"my-interrupt-1"`. |
| `board`  | **Required** | The `name` of the [board](/components/board) the sensor is connected to. |
| `timeout_ms`  | Optional | Time to wait in milliseconds before timing out of requesting to get readings from the sensor. Default: `1000`. |

{{% alert title="Tip" color="tip" %}}

A `trigger_pin` value of `5` corresponds to [Pin 5 GPIO 3](https://pinout.xyz/pinout/pin5_gpio3) on a Raspberry Pi.

{{% /alert %}}
