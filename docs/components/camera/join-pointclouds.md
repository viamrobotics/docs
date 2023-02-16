---
title: "Configure a Join Pointclouds View"
linkTitle: "Join Pointclouds"
weight: 40
type: "docs"
description: "Combine the point clouds from multiple camera sources and project them to be from the point of view of target_frame."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Combine the point clouds from multiple camera sources and project them to be from the point of view of target_frame:

{{< tabs name="Configure a Join Pointclouds View" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> tab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>join_pointclouds</code> model.
<br>
<img src="../img/create-join-pointclouds.png" alt="Creation of a Join Pointclouds view in the Viam app config builder." />
<br>
Fill in the attributes for your join pointclouds view:
<br>
<img src="../img/configure-join-pointclouds.png" alt="Configuration of a Join Pointclouds view in the Viam App config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "join_pointclouds",
    "attributes": {
        "target_frame": <string>,
        "source_cameras": ["cam1", "cam2", ... ],
        "proximity_threshold_mm": <integer>,
        "merge_method": "<naive|icp>",
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <number>,
            "fy": <number>,
            "ppx": <number>,
            "ppy": <number>
        },
        "distortion_parameters": {
            "rk1": <number>,
            "rk2": <number>,
            "rk3": <number>,
            "tp1": <number>,
            "tp2": <number>
        },
        "debug": <boolean>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for join pointcloud views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `target_frame` | *Required* | The frame of reference for the points in the merged point cloud. |
| `source_cameras` | *Required* | The camera sources to combine. |
| `proximity_threshold_mm` | *Optional* | Defines the biggest distance 2 points can have in mm to be considered the same point when merged. |
| `merge_method` | *Optional* | `naive` or `icp`. Defaults to `naive`. |
| `intrinsic_parameters` | *Required* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
