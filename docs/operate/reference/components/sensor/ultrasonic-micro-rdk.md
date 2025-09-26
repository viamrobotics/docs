---
title: "Configure an Ultrasonic Sensor (Micro-RDK)"
linkTitle: "ultrasonic (Micro-RDK)"
weight: 60
type: "docs"
description: "Configure an ultrasonic sensor with a microcontroller."
tags: ["sensor", "components", "ultrasonic"]
icon: true
images: ["/icons/components/sensor.svg"]
micrordk_component: true
aliases:
  - /build/micro-rdk/sensor/ultrasonic/
  - /components/sensor/ultrasonic-micro-rdk/
toc_hide: true
# SME: Andrew Morrow
---

Configure an `ultrasonic` sensor to integrate the [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor into your machine.
Physically connect your sensor to your microcontroller and power both on.
Then, configure the sensor:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `sensor` type, then select the `ultrasonic` model.
Enter a name or use the suggested name for your sensor and click **Create**.

![Creation of a ultrasonic sensor.](/build/micro-rdk/ultrasonic/ultrasonic-sensor-ui-config.png)

Edit and fill in the attributes as applicable to your sensor, according to the table below.
Although `"board"` is marked as required in `viam-server`, it is not required for `viam-micro-server` usage.

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
      "api": "rdk:component:sensor",
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
      "api": "rdk:component:sensor",
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
| `trigger_pin` | string | **Required** | The GPIO number of the [board's](/operate/reference/components/board/) GPIO pin that you have wired to the trigger pin of your ultrasonic sensor. |
| `echo_interrupt_pin` | string | **Required** | The GPIO number of the board's GPIO pin that you have wired to the echo pin of your ultrasonic sensor. Please note that unlike the RDK ultrasonic sensor, you must not use a named pin associated with a digital interrupt configured on your board: it will not (currently) work. |
| `timeout_ms`  | int | Optional | Time to wait in milliseconds before initiating a timeout when requesting readings from your ultrasonic sensor. <br> Default: `50` <br> Max: `100` |

## Test the sensor

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/sensor.md" >}}

## Next steps

Check out the [sensor API](/dev/reference/apis/components/sensor/) or check out one of these guides:

{{< cards >}}
{{% card link="/dev/reference/apis/components/sensor/" customTitle="Sensor API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{< /cards >}}
