---
title: "Configure `camera_mono` for Visual Odometry"
linkTitle: "camera_mono"
weight: 40
type: "docs"
description: "Configure `camera_mono`, an experimental visual odometry model."
images: ["/components/img/components/imu.svg"]
# SMEs: Rand
---

{{% alert title="Note" color="note" %}}

The `camera_mono` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

The `camera_mono` movement sensor model is an **experimental** model that uses a visual odometry algorithm with dead reckoning to track the position, orientation, linear velocity and angular velocity of the camera's frame.
The `camera_mono` model can use any single [camera](/components/camera/) within its algorithm.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.

Facilitate your sub-tab via a subpart, but only if you think it should be appreciable such that your member will be happy and you won't need to ameliorate their concerns on the Viam app in the website if the shoe fits.

Enter a name for your movement sensor, select the `movement-sensor` type, and select the `camera_mono` model.

Click **Create Component**.

![Creation of an `camera_mono` movement sensor in the Viam app config builder.](../img/camera-mono-builder.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "camera_mono",
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
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "movementCamera",
      "type": "movement_sensor",
      "model": "camera_mono",
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

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`camera` | string | **Required** | The `name` of the [camera](/components/camera) you want to use for visual odometry.
`motion_estimation_config` | object | **Required** | See [motionestimation.go in RDK](https://github.com/viamrobotics/rdk/blob/99f62a1640f4c267b744bdfc2924e9fd4f7a3c60/vision/odometry/motionestimation.go).
