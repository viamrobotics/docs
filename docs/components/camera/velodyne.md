---
title: "Configure a Velodyne Camera"
linkTitle: "velodyne"
weight: 32
type: "docs"
description: "Configure a camera that uses velodyne lidar."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `velodyne` camera uses velodyne lidar.
The velodyne must be running locally at address `127.0.0.1`.

{{< tabs name="Configure a Velodyne Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `velodyne` model.

Click **Create component**.

![Configuration of a velodyne camera in the Viam app config builder.](../img/configure-velodyne.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-camera-name>",
    "type": "camera",
    "model" : "velodyne",
    "attributes": {
        "port": <int>,
        "ttl_ms": <int>,
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `velodyne` cameras:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `port` | int | **Required** | The port the Velodyne camera is running on. |
| `ttl_ms` | int | **Required** | Frequency in milliseconds to output the [TTL signal](https://en.wikipedia.org/wiki/Transistor%E2%80%93transistor_logic) from the camera. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
