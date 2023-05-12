---
title: "Configure a Join Color Depth View"
linkTitle: "join_color_depth"
weight: 39
type: "docs"
description: "Combine and align the streams of a color and a depth camera."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Combine the streams of a color and a depth camera already registered in your config to create a view that outputs the combined and aligned image.

This specific model is good if you don’t need to align the streams.
If you need to adjust the alignment between the depth and color frames, use the [`align_color_depth_extrinsics`](../align-color-depth-extrinsics) model or the[`align_color_depth_homography`](../align-color-depth-homography) model.

{{< tabs name="Configure a Join Color Depth View" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `join_color_depth` model.

![Creation of a join color depth view in the Viam app config builder.](../img/create-join-color-depth.png)

Fill in the attributes for your join color depth view:

![Configuration of a join color depth view in the Viam app config builder.](../img/configure-join-color-depth.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "join_color_depth",
    "attributes": {
        "output_image_type": "<color|depth>",
        "color_camera_name": "<camera_name>",
        "depth_camera_name": "<camera_name>",
        "intrinsic_parameters": {
          "width_px": <integer>, # the expected width of the aligned pic
          "height_px": <integer>, # the expected height of the aligned pic
          "fx": <float64>,
          "fy": <float64>,
          "ppx": <float64>,
          "ppy": <float64>
        },
        "distortion_parameters": {
          "rk1": <float64>,
          "rk2": <float64>,
          "rk3": <float64>,
          "tp1": <float64>,
          "tp2": <float64>
        },
        "debug": <boolean>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `join_color_depth` views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `output_image_type` | **Required** | Specify `color` or `depth` for the output stream. |
| `color_camera_name` | **Required** | Name of the color camera to pull images from. |
| `depth_camera_name` | **Required** | Name of the depth camera to pull images from. |
| `intrinsic_parameters` | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
