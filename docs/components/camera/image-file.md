---
title: "Configure an Image File Camera"
linkTitle: "image_file"
weight: 31
type: "docs"
description: "Configure a camera that gets color or depth images frames from a file path."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

An `image_file` camera gets color and depth images frames from a file path.
If you provide a depth image, as well as the intrinsic parameters of the camera that took that depth image, then the camera will also provide a point cloud.

{{< tabs name="Configure an Image File Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `image_file` model.

![Creation of an image file camera in the Viam app config builder.](../img/create-image-file.png)

Fill in the attributes for your image file camera:

![Configuration of an image file camera in the Viam app config builder.](../img/configure-image-file.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "image_file",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
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
        "debug": <boolean>,
        "color_image_file_path": <string>,
        "depth_image_file_path": <string>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `image_file` cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |
| `color_image_file_path` | Optional | The file path to the color image. |
| `depth_image_file_path` | Optional | The file path to the depth image. |

You must specify `color_image_file_path` or `depth_image_file_path`.

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
