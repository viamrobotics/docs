---
title: "Configure a Join Color Depth View"
linkTitle: "join_color_depth"
weight: 39
type: "docs"
description: "Combine and align the streams of a color and a depth camera."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/join-color-depth/"
component_description: "Joins the outputs of a color and depth camera already registered in your config to create a third “camera” that outputs the combined and aligned image."
# SMEs: Bijan, vision team
---

The `join_color_depth` model combines the streams of a color and depth camera already registered in your config to create a view that outputs the combined and aligned image.

This specific model is good if you don’t need to align the streams.

{{< tabs name="Configure a Join Color Depth View" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `join_color_depth` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of a join color depth view in the Viam app config builder.](/components/camera/configure-join-color-depth.png)

Copy and paste the following attribute template into your camera's attributes field.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

```json {class="line-numbers linkable-line-numbers"}
{
  "output_image_type": "<color|depth>",
  "color_camera_name": "<your-camera-name>",
  "depth_camera_name": "<your-camera-name>",
  "intrinsic_parameters": {
    "width_px": <int>, # the expected width of the aligned pic
    "height_px": <int>, # the expected height of the aligned pic
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
  "model": "join_color_depth",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "output_image_type": "<color|depth>",
    "color_camera_name": "<your-camera-name>",
    "depth_camera_name": "<your-camera-name>",
    "intrinsic_parameters": {
      "width_px": <int>, # the expected width of the aligned pic
      "height_px": <int>, # the expected height of the aligned pic
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

The following attributes are available for `join_color_depth` views:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `output_image_type` | string | **Required** | Specify `color` or `depth` for the output stream. |
| `color_camera_name` | string | **Required** | `name` of the color camera to pull images from. If your camera provides both color and depth image streams, you must set this to be the same as `depth_camera_name`. |
| `depth_camera_name` | string | **Required** | `name` of the depth camera to pull images from. If your camera provides both color and depth image streams, you must set this to be the same as `color_camera_name`. |
| `intrinsic_parameters` | object | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
