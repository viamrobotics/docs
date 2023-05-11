---
title: "Configure an Align Color Depth Extrinsics View"
linkTitle: "align_color_depth_extrinsics"
weight: 38
type: "docs"
description: "Use the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Use the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images.

{{< tabs name="Configure an Align Color Depth Extrinsics View" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `align_color_depth_extrinsics` model.

![Creation of an align color depth extrinsics view in the Viam app config builder.](../img/create-align-color-depth-extrinsics.png)

Fill in the attributes for your align color depth extrinsics view:

![Configuration of an align color depth extrinsics view in the Viam app config builder.](../img/configure-align-color-depth-extrinsics.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "align_color_depth_extrinsics",
    "attributes": {
        "camera_system": {
            "color_intrinsic_parameters": {
                "width_px": <integer>,
                "height_px": <integer>,
                "fx": <float64>,
                "fy": <float64>,
                "ppx": <float64>,
                "ppy": <float64>
            },
            "depth_intrinsic_parameters": {
                "width_px": <integer>,
                "height_px": <integer>,
                "fx": <float64>,
                "fy": <float64>,
                "ppx": <float64>,
                "ppy": <float64>
            },
                "depth_to_color_extrinsic_parameters": {
                "translation_mm": [ <float64>, <float64>, <float64>],
                "rotation_rads": [ <float64>, <float64>, <float64>,
                                   <float64>, <float64>, <float64>,
                                   <float64>, <float64>, <float64> ],
            }
        },
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <float64>,
            "fy": <float64>,
            "ppx": <float64>,
            "ppy": <float64>
        },
        "output_image_type": "<color|depth>",
        "color_camera_name": "<camera_name>",
        "depth_camera_name": "<camera_name>",
        "debug": false,
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `align_color_depth_extrinsics` views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `camera_system` | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>color_intrinsic_parameters</code>: The model uses the color camera intrinsics to project the 3D points to a 2D depth map, but "as if" it was taken from the POV of the color camera. </li> <li> <code>depth_intrinsic_parameters</code>: The model uses the depth camera intrinsics to de-project the 2D depth points to 3D points, from the point of view of the depth camera. </li> <li> <code>depth_to_color_extrinsic_parameters</code>: The model uses the extrinsic parameters to shift the 3D depth points to be from the POV of the color camera. </li> </ul> |
| `intrinsic_parameters` | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `output_image_type` | **Required** | Specify `color` or `depth` for the output stream. |
| `color_camera_name` | **Required** | `name` of the color camera to pull images from. |
| `depth_camera_name` | **Required** | `name` of the depth camera to pull images from. |
| `distortion_parameters` | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
