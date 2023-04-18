---
title: "Configure a Velodyne Camera"
linkTitle: "Velodyne"
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

On the **Components** subtab, navigate to the **Create Component** menu.
Enter a name for your camera, select the type `camera`, and select the `velodyne` model.

<img src="../img/create-velodyne.png" alt="Creation of a velodyne camera in the Viam app config builder." style="max-width:500px" />

Fill in the attributes for your velodyne camera:

<img src="../img/configure-velodyne.png" alt="Configuration of a velodyne camera in the Viam app config builder." />

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

The following attributes are available for velodyne cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `port` | *Required* | Specify the port the velodyne camera is running on. |
| `ttl_ms` | *Required* | Specify the  milliseconds ???. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
