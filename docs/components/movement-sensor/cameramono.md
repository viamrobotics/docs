---
title: "Configure a camera_mono Model for Visual Odometry"
linkTitle: "camera_mono"
weight: 40
type: "docs"
description: "Configure camera_mono, an experimental visual odometry model."
images: ["/icons/components/imu.svg"]
draft: true
aliases:
  - "/components/movement-sensor/cameramono/"
# SMEs: Rand
---

{{% alert title="Stability Notice" color="note" %}}

The `camera_mono` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

The `camera_mono` movement sensor model is an **experimental** model that uses a visual odometry algorithm with dead reckoning to track the position, orientation, linear velocity and angular velocity of the camera's frame.
The `camera_mono` model can use any single [camera](/components/camera/) within its algorithm.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `camera_mono` model.
Enter a name for your movement sensor and click **Create**.

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "model": "camera_mono",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "camera": "<your-camera-name>",
        "motion_estimation_config": {
            <see Vision Service documentation>
        }
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
      "name": "myCamera",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "movementCamera",
      "model": "camera_mono",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "camera": "myCamera",
        "motion_estimation_config": {
            <see Vision Service documentation>
        }
      },
      "depends_on": [
        "myCamera"
      ]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Name                       | Type   | Inclusion    | Description |
| -------------------------- | ------ | ------------ | ----------- |
| `camera`                   | string | **Required** | The `name` of the [camera](/components/camera/) you want to use for visual odometry. |
| `motion_estimation_config` | object | **Required** | See [motionestimation.go in RDK](https://github.com/viamrobotics/rdk/blob/99f62a1640f4c267b744bdfc2924e9fd4f7a3c60/vision/odometry/motionestimation.go). |

## Test the movement sensor

After you configure your movement sensor, navigate to the [**CONTROL** tab](/fleet/machines/#control) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.
