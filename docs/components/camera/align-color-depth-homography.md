---
title: "Configure an Align Color Depth Homography View"
linkTitle: "align_color_depth_homography"
weight: 38
type: "docs"
description: "Use a homography matrix to align the color and depth images."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

When you have a depth image and you need it to overlay on top of a color image exactly, a homography matrix can apply the necessary distortions to the depth image for it to overlap.

{{< tabs name="Configure an Align Color Depth Homography Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `align_color_depth_homography` model.

![Creation of an align color depth homography view in the Viam app config builder.](../img/create-align-color-depth-homography.png)

Fill in the attributes for your align color depth homography view:

![Configuration of an align color depth homography view in the Viam app config builder.](../img/configure-align-color-depth-homography.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "align_color_depth_homography",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <float64>,
            "fy": <float64>,
            "ppx": <float64>,
            "ppy": <float64>
        },
        "homography": {
            "transform": [ <float64>, <float64>, <float64>,
                           <float64>, <float64>, <float64>,
                           <float64>, <float64>, <float64> ],
            "depth_to_color": <boolean>,
            "rotate_depth_degs": <integer>
        },
        "color_camera_name": "<camera_name>",
        "depth_camera_name": "<camera_name>",
        "output_image_type": "<color|depth>",
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

The following attributes are available for `align_color_depth_homography` views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `homography` | **Required** | Parameters that morph the depth points to overlay the color points and align the images: <ul> <li> <code>transform</code>: 9 floats representing the 3x3 homography matrix of the depth to color, or color to depth camera. </li> <li> <code>depth_to_color</code>: Whether to transform depth camera points to color camera points. </li> <li> <code>rotate_depth_degs</code>: Degrees by which to rotate the depth camera image. </li> </ul> |
| `color_camera_name` | **Required** | `name` of the color camera to pull images from. |
| `depth_camera_name` | **Required** | `name` of the depth camera to pull images from. |
| `output_image_type` | **Required** | Specify `color` or `depth` for the output stream. |
| `distortion_parameters` | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
