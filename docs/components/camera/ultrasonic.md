---
title: "Configure an Ultrasonic Camera"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic model camera."
tags: ["camera", "components", "ultrasonic"]
icon: true
images: ["/icons/components/camera.svg"]
aliases:
  - "/components/camera/ultrasonic/"
# SME: #team-bucket
---

{{< alert title="Usage" color="tip" >}}
An ultrasonic distance sensor can also be configured as a [sensor](/components/sensor/) resource.
When configured as a sensor, you can use the sensor method [`GetReadings()`](/components/sensor/#getreadings), rather than the camera method [`GetPointCloud()`](/components/camera/#getpointcloud).
{{< /alert >}}

Configure an `ultrasonic` camera to integrate the [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `ultrasonic` model.
Enter a name or use the automatically suggested name for your camera and click **Create**.

![Creation of a ultrasonic camera in the Viam app config builder.](/components/camera/configure-ultrasonic.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "trigger_pin": "<pin-number>",
  "echo_interrupt_pin": "<pin-number>",
  "board": "<your-board-name>",
  "timeout_ms": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "trigger_pin": "5",
  "echo_interrupt_pin": "15",
  "board": "local",
  "timeout_ms": "1200"
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
      "type": "camera",
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
      "type": "camera",
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

The following attributes are available for `ultrasonic` cameras:

{{< readfile "/static/include/components/ultrasonic-attributes.md" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
