---
title: "Configure an Align Color Depth Homography View"
linkTitle: "align_color_depth_homography"
weight: 38
type: "docs"
description: "Use a homography matrix to align the color and depth images."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/align-color-depth-homography/"
# SMEs: Bijan, vision team
---

When you have a depth image and you need it to overlay on top of a color image exactly, a homography matrix can apply the necessary distortions to the depth image to make it align with the color image.
Use the `align_color_depth_homography` camera model to do this alignment.

{{< tabs name="Configure an Align Color Depth Homography Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `align_color_depth_homography` model.
Enter a name for your camera and click **Create**.

![Configuration of an align color depth homography view in the Viam app config builder.](/components/camera/configure-align-color-depth-homography.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

```json {class="line-numbers linkable-line-numbers"}
{
  "intrinsic_parameters": {
    "width_px": <int>,
    "height_px": <int>,
    "fx": <float>,
    "fy": <float>,
    "ppx": <float>,
    "ppy": <float>
  },
  "homography": {
    "transform": [ <float>, <float>, <float>,
                   <float>, <float>, <float>,
                   <float>, <float>, <float> ],
    "depth_to_color": <boolean>,
    "rotate_depth_degs": <int>
  },
  "color_camera_name": "<your-camera-name>",
  "depth_camera_name": "<your-camera-name>",
  "output_image_type": "<color|depth>",
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
  "model": "align_color_depth_homography",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "intrinsic_parameters": {
      "width_px": <int>,
      "height_px": <int>,
      "fx": <float>,
      "fy": <float>,
      "ppx": <float>,
      "ppy": <float>
    },
    "homography": {
      "transform": [ <float>, <float>, <float>,
                     <float>, <float>, <float>,
                     <float>, <float>, <float> ],
      "depth_to_color": <boolean>,
      "rotate_depth_degs": <int>
    },
    "color_camera_name": "<your-camera-name>",
    "depth_camera_name": "<your-camera-name>",
    "output_image_type": "<color|depth>",
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

The following attributes are available for `align_color_depth_homography` views:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `intrinsic_parameters` | object | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `homography` | object | **Required** | Parameters that morph the depth points to overlay the color points and align the images: <ul> <li> <code>transform</code>: 9 floats representing the 3x3 homography matrix of the depth to color, or color to depth camera. </li> <li> <code>depth_to_color</code>: Whether to transform depth camera points to color camera points. </li> <li> <code>rotate_depth_degs</code>: Degrees by which to rotate the depth camera image. </li> </ul> |
| `color_camera_name` | string | **Required** | `name` of the color camera to pull images from. |
| `depth_camera_name` | string | **Required** | `name` of the depth camera to pull images from. |
| `output_image_type` | string | **Required** | Specify `color` or `depth` for the output stream. |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
