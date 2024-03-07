---
title: "Configure an Ultrasonic Sensor (Micro-RDK)"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic sensor."
tags: ["sensor", "components", "ultrasonic"]
icon: true
images: ["/icons/components/sensor.svg"]
# SME: Andrew Morrow
---

Configure an `ultrasonic` sensor to integrate the [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `sensor` type, then select the `ultrasonic` model.
Enter a name for your sensor and click **Create**.

![Creation of a ultrasonic sensor in the Viam app config builder.](/build/micro-rdk/ultrasonic/ultrasonic-sensor-ui-config.png)

Copy and paste the following attribute template into your sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "trigger_pin": "<pin-number>",
  "echo_interrupt_pin": "<pin-number>",
  "timeout_ms": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "trigger_pin": "15",
  "echo_interrupt_pin": "18",
  "timeout_ms": "200"
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
        "echo_interrupt_pin": "<pin-number>",
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
      "name": "my-ultrasonic-sensor",
      "model": "ultrasonic",
      "type": "sensor",
      "namespace": "rdk",
      "attributes": {
        "trigger_pin": "15",
        "echo_interrupt_pin": "18",
        "timeout_ms": "200"
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
| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `trigger_pin` | string | **Required** | The GPIO number of the [board's](/build/micro-rdk/board/) GPIO pin that you have wired to the trigger pin of your ultrasonic sensor. |
| `echo_interrupt_pin` | string | **Required** | The GPIO number of the board's GPIO pin that you have wired to the echo pin of your ultrasonic sensor. Please note that unlike the RDK ultrasonic sensor, you must not use a named pin associated with a digital interrupt configured on your board: it will not (currently) work. |
| `timeout_ms`  | int | Optional | Time to wait in milliseconds before initiating a timeout when requesting readings from your ultrasonic sensor. <br> Default: `1000`. |

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}
