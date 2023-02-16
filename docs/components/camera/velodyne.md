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
The velodyne must be running locally at address `0.0.0.0`.

{{< tabs name="Configure a Velodyne Camera" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>velodyne</code> model.
<br>
<img src="../img/create-velodyne.png" alt="Creation of a velodyne camera in the Viam app config builder." />
<br>
Fill in the attributes for your velodyne camera:
<br>
<img src="../img/configure-velodyne.png" alt="Configuration of a velodyne camera in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
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
