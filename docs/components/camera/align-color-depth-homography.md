---
title: "Configure an Align Color Depth Homography View"
linkTitle: "Align Color Depth Homography"
weight: 38
type: "docs"
description: "Use a homography matrix to align the color and depth images."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Use a homography matrix to align the color and depth images.

{{< tabs name="Configure an Align Color Depth Homography Camera" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>align_color_depth_homography</code> model.
<br>
<img src="../img/create-align-color-depth-homography.png" alt="Creation of an align color depth homography view in the Viam app config builder." />
<br>
Fill in the attributes for your align color depth homography view:
<br>
<img src="../img/configure-align-color-depth-homography.png" alt="Configuration of an align color depth homography view in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "align_color_depth_homography",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <number>,
            "fy": <number>,
            "ppx": <number>,
            "ppy": <number>
        },
        "homography": {
            "transform": [ <number>, <number>, <number>,
                           <number>, <number>, <number>,
                           <number>, <number>, <number> ],
            "depth_to_color": <boolean>,
            "rotate_depth_degs": <integer>
        },
        "color_camera_name": "<camera_name>",
        "depth_camera_name": "<camera_name>",
        "output_image_type": "<color|depth>",
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

The following attributes are available for align color depth homography views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Required* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `homography` | *Required* | Parameters that morph the depth points to overlay the color points and align the images: <ul> <li> <code>transform</code>: 9 floats representing the 3x3 homography matrix of the depth to color, or color to depth camera. </li> <li> <code>depth_to_color</code>: Whether to turn the depth information into colors. </li> <li> <code>rotate_depth_degs</code>: Degrees by which to rotate the depth camera image. </li> </ul> |
| `color_camera_name` | *Required* | Name of the color camera to pull images from. |
| `depth_camera_name` | *Required* | Name of the depth camera to pull images from. |
| `output_image_type` | *Required* | Specify `color` or `depth` for the output stream. |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
