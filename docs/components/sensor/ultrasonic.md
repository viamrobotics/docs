---
title: "Configure an Ultrasonic Sensor"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic model sensor."
tags: ["sensor", "components", "ultrasonic"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/sensor/ultrasonic/"
# SME: #team-bucket
---

{{< alert title="Tip" color="tip" >}}
An ultrasonic distance sensor can also be configured as a [camera](/components/camera/) resource.

When configured as a camera, you can use the camera method [`GetPointCloud()`](/components/camera/#getpointcloud), rather than the sensor method [`GetReadings()`](/components/sensor/#getreadings).
Additionally, you can use the camera component as an input to a [vision service](/ml/vision/) model that returns obstacles.
{{< /alert >}}

Configure an `ultrasonic` sensor to integrate the [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `sensor` type, then select the `ultrasonic` model.
Enter a name for your sensor and click **Create**.

![Creation of a ultrasonic sensor in the Viam app config builder.](/components/sensor/ultrasonic-sensor-ui-config.png)

Fill in the attributes as applicable to your sensor, according to the table below.

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
      "name": "my-ultrasonic-sensor",
      "model": "ultrasonic",
      "type": "sensor",
      "namespace": "rdk",
      "attributes": {
        "trigger_pin": "5",
        "echo_interrupt_pin": "15",
        "board": "local",
        "timeout_ms": "1200"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `ultrasonic` sensors:

{{< readfile "/static/include/components/ultrasonic-attributes.md" >}}

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}
