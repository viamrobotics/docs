---
title: "Configure an ultrasonic Sensor"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic model sensor."
tags: ["sensor", "components"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
# SME: #team-bucket
---

Configure an `ultrasonic` sensor to integrate an [HC-S204 ultrasonic distance sensor](https://www.sparkfun.com/products/15569) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `ultrasonic` model.

Click **Create component**.

{{< imgproc src="/components/sensor/ultrasonic-sensor-ui-config.png" alt="Creation of a ultrasonic sensor in the Viam app config builder." resize="1000x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-ultrasonic-sensor-name>",
      "type": "sensor",
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": "<pin-number>",
        "echo_interrupt_pin": "<pin-number>",
        "board": "<your-board-name>",
        "timeout_ms": <int>
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

| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `board`  | string | **Required** | The `name` of the [board](/components/board/) the sensor is wired to. |
| `trigger_pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} on the [board](/components/board/) that you have wired [the sensor's trigger pin](https://www.sparkfun.com/products/15569). |
| `echo_interrupt_pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin [the sensor's echo pin](https://www.sparkfun.com/products/15569) is wired to on the board. If you have already created a [digital interrupt](/components/board/#digital_interrupts) for this pin in the [board's configuration](/components/board/), use that digital interrupt's `name` instead. |
| `timeout_ms`  | int | Optional | Time to wait in milliseconds before timing out of requesting to get readings from the sensor. <br> Default: `1000`. |
