---
title: "Configure a Velodyne Camera"
linkTitle: "velodyne"
weight: 32
type: "docs"
description: "Configure a camera that uses velodyne lidar."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `velodyne` camera uses velodyne lidar.
The velodyne must be running locally at address `127.0.0.1`.

{{< tabs name="Configure a Velodyne Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `velodyne` model.

![Creation of a velodyne camera in the Viam app config builder.](../img/create-velodyne.png)

Fill in the attributes for your velodyne camera:

![Configuration of a velodyne camera in the Viam app config builder.](../img/configure-velodyne.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "velodyne",
    "attributes": {
        "port": <integer>,
        "ttl_ms": <integer>,
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `velodyne` cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `port` | **Required** | The port the Velodyne camera is running on. |
| `ttl_ms` | **Required** | Frequency in milliseconds to output the [TTL signal](https://en.wikipedia.org/wiki/Transistor%E2%80%93transistor_logic) from the camera. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
