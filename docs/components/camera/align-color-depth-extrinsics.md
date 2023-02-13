---
title: "Configure an Align Color Depth Extrinsics View"
linkTitle: "Align Color Depth Extrinsics"
weight: 37
type: "docs"
description: "Use the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Use the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images.

{{< tabs name="Configure an Align Color Depth Extrinsics View" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> tab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>align_color_depth_extrinsics</code> model.
<br>
<img src="../img/create-align-color-depth-extrinsics.png" alt="Creation of an align color depth extrinsics view in the Viam App config builder." />
<br>
Fill in the attributes for your align color depth extrinsics view:
<br>
<img src="../img/configure-align-color-depth-extrinsics.png" alt="Configuration of an align color depth extrinsics view in the Viam App config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "align_color_depth_extrinsics",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <number>,
            "fy": <number>,
            "ppx": <number>,
            "ppy": <number>
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

The following attributes are available for align color depth extrinsics views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Required* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `output_image_type` | *Required* | Specify `color` or `depth` for the output stream. |
| `color_camera_name` | *Required* | Name of the color camera to pull images from. |
| `depth_camera_name` | *Required* | Name of the depth camera to pull images from. |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
