---
title: "Configure an Ultrasonic Sensor (Micro-RDK)"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic sensor."
tags: ["sensor", "components", "ultrasonic"]
icon: true
images: ["/icons/components/sensor.svg"]
micrordk_component: true
aliases:
  - /build/micro-rdk/sensor/ultrasonic/
# SME: Andrew Morrow
---

Configure an `ultrasonic` sensor to integrate the [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `sensor` type, then select the `ultrasonic` model.
Enter a name or use the suggested name for your sensor and click **Create**.

![Creation of a ultrasonic sensor in the Viam app config builder.](/build/micro-rdk/ultrasonic/ultrasonic-sensor-ui-config.png)

Edit and fill in the attributes as applicable to your sensor, according to the table below.
Although `"board"` is marked as required in the RDK, it is not required for Micro-RDK usage.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "trigger_pin": "<pin-number>",
  "echo_interrupt_pin": "<pin-number>"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "trigger_pin": "15",
  "echo_interrupt_pin": "18"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-ultrasonic-sensor-name>",
      "model": "ultrasonic",
      "type": "sensor",
      "namespace": "rdk",
      "attributes": {
        "trigger_pin": "<pin-number>",
        "echo_interrupt_pin": "<pin-number>"
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
      "name": "my-ultrasonic-sensor",
      "model": "ultrasonic",
      "type": "sensor",
      "namespace": "rdk",
      "attributes": {
        "trigger_pin": "15",
        "echo_interrupt_pin": "18"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `ultrasonic` sensors:

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `trigger_pin` | string | **Required** | The GPIO number of the [board's](/components/board/) GPIO pin that you have wired to the trigger pin of your ultrasonic sensor. |
| `echo_interrupt_pin` | string | **Required** | The GPIO number of the board's GPIO pin that you have wired to the echo pin of your ultrasonic sensor. Please note that unlike the RDK ultrasonic sensor, you must not use a named pin associated with a digital interrupt configured on your board: it will not (currently) work. |
| `timeout_ms`  | int | Optional | Time to wait in milliseconds before initiating a timeout when requesting readings from your ultrasonic sensor. <br> Default: `50` <br> Max: `100` |

## Test the sensor

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}
