---
title: "Configure an ultrasonic Camera"
linkTitle: "ultrasonic"
weight: 60
type: "docs"
description: "Configure an ultrasonic model camera."
tags: ["camera", "components", "ultrasonic"]
icon: "/icons/components/camera.svg"
images: ["/icons/components/camera.svg"]
# SME: #team-bucket
---

{{< alert title="Usage" color="tip" >}}
An ultrasonic distance sensor can also be configured as a [sensor](/components/sensor/) resource.
[Configure it as such](/components/sensor/ultrasonic/) to utilize the [sensor API](/components/sensor/#api) with your ultrasonic sensor hardware.

Configure your ultrasonic sensor as a camera if you want to use it as an input to a [vision service](/services/vision/) model that returns obstacles.
As a camera model, the ultrasonic model implements the camera method [`GetPointCloud()`](/components/camera/#getpointcloud), rather than the sensor method [`GetReadings()`](/components/sensor/#getreadings).
{{< /alert >}}

Configure an `ultrasonic` camera to integrate an ultrasonic distance sensor like the [HC-S204](https://www.sparkfun.com/products/15569) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `ultrasonic` model.
Enter a name for your camera and click **Create**.

![Creation of a ultrasonic camera in the Viam app config builder.](/components/camera/configure-ultrasonic.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-ultrasonic-sensor-name>",
      "type": "camera",
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
      "type": "camera",
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

The following attributes are available for `ultrasonic` cameras:

{{< readfile "/static/include/components/ultrasonic-attributes.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
