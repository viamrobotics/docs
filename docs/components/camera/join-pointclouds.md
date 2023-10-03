---
title: "Configure a Join Point Clouds View"
linkTitle: "join_pointclouds"
weight: 40
type: "docs"
description: "Combine the point clouds from multiple camera sources and project them to be from the point of view of target_frame."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Combine the point clouds from multiple camera sources and project them to be from the point of view of target_frame:

{{< tabs name="Configure a Join Point Clouds View" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `join_pointclouds` model.
Enter a name for your camera and click **Create**.

![Configuration of a Join Point Clouds view in the Viam App config builder.](/components/camera/configure-join-pointclouds.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

```json {class="line-numbers linkable-line-numbers"}
{
  "target_frame": "<target-frame-name>",
  "source_cameras": ["<cam-name-1>", "<cam-name-2>", ... ],
  "proximity_threshold_mm": <int>,
  "merge_method": "<naive|icp>",
  "intrinsic_parameters": {
    "width_px": <int>,
    "height_px": <int>,
    "fx": <float>,
    "fy": <float>,
    "ppx": <float>,
    "ppy": <float>
  },
  "distortion_parameters": {
    "rk1": <float>,
    "rk2": <float>,
    "rk3": <float>,
    "tp1": <float>,
    "tp2": <float>
  },
  "debug": <boolean>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "join_pointclouds",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "target_frame": "<target-frame-name>",
    "source_cameras": ["<cam-name-1>", "<cam-name-2>", ... ],
    "proximity_threshold_mm": <int>,
    "merge_method": "<naive|icp>",
    "intrinsic_parameters": {
      "width_px": <int>,
      "height_px": <int>,
      "fx": <float>,
      "fy": <float>,
      "ppx": <float>,
      "ppy": <float>
    },
    "distortion_parameters": {
      "rk1": <float>,
      "rk2": <float>,
      "rk3": <float>,
      "tp1": <float>,
      "tp2": <float>
    },
    "debug": <boolean>
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `join_pointclouds` views:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `target_frame` | string | **Required** | The frame of reference for the points in the merged point cloud. |
| `source_cameras` | array | **Required** | The `name` of each of the camera sources to combine. |
| `intrinsic_parameters` | object | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `proximity_threshold_mm` | int | Optional | Defines the largest distance 2 points can have in millimeters to be considered the same point when merged. |
| `merge_method` | string | Optional | `naive` or `icp`. <br> Default: `naive` |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
