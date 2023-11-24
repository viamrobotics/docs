---
title: "Configure an Align Color Depth Extrinsics View"
linkTitle: "align_color_depth_extrinsics"
weight: 38
type: "docs"
description: "Use the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/align-color-depth-extrinsics/"
# SMEs: Bijan, vision team
---

Use the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images.

{{< tabs name="Configure an Align Color Depth Extrinsics View" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `align_color_depth_extrinsics` model.
Enter a name for your camera and click **Create**.

![Configuration of an align color depth extrinsics view in the Viam app config builder.](/build/configure/components/camera/configure-align-color-depth-extrinsics.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

```json {class="line-numbers linkable-line-numbers"}
{
 "camera_system": {
    "color_intrinsic_parameters": {
      "width_px": <int>,
      "height_px": <int>,
      "fx": <float>,
      "fy": <float>,
      "ppx": <float>,
      "ppy": <float>
    },
    "depth_intrinsic_parameters": {
      "width_px": <int>,
      "height_px": <int>,
      "fx": <float>,
      "fy": <float>,
      "ppx": <float>,
      "ppy": <float>
    },
    "depth_to_color_extrinsic_parameters": {
    "translation_mm": [ <float>, <float>, <float>],
    "rotation_rads": [ <float>, <float>, <float>,
                       <float>, <float>, <float>,
                       <float>, <float>, <float> ],
    }
  },
  "intrinsic_parameters": {
    "width_px": <int>,
    "height_px": <int>,
    "fx": <float>,
    "fy": <float>,
    "ppx": <float>,
    "ppy": <float>
  },
  "output_image_type": "<color|depth>",
  "color_camera_name": "<your-color-camera-name>",
  "depth_camera_name": "<your-depth-camera-name>",
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
  "model": "align_color_depth_extrinsics",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "camera_system": {
      "color_intrinsic_parameters": {
        "width_px": <int>,
        "height_px": <int>,
        "fx": <float>,
        "fy": <float>,
        "ppx": <float>,
        "ppy": <float>
      },
      "depth_intrinsic_parameters": {
        "width_px": <int>,
        "height_px": <int>,
        "fx": <float>,
        "fy": <float>,
        "ppx": <float>,
        "ppy": <float>
      },
      "depth_to_color_extrinsic_parameters": {
      "translation_mm": [ <float>, <float>, <float>],
      "rotation_rads": [ <float>, <float>, <float>,
                         <float>, <float>, <float>,
                         <float>, <float>, <float> ],
      }
    },
    "intrinsic_parameters": {
      "width_px": <int>,
      "height_px": <int>,
      "fx": <float>,
      "fy": <float>,
      "ppx": <float>,
      "ppy": <float>
    },
    "output_image_type": "<color|depth>",
    "color_camera_name": "<your-color-camera-name>",
    "depth_camera_name": "<your-depth-camera-name>",
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

The following attributes are available for `align_color_depth_extrinsics` views:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `camera_system` | object | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>color_intrinsic_parameters</code>: The model uses the color camera intrinsics to project the 3D points to a 2D depth map, but "as if" it was taken from the POV of the color camera. </li> <li> <code>depth_intrinsic_parameters</code>: The model uses the depth camera intrinsics to de-project the 2D depth points to 3D points, from the point of view of the depth camera. </li> <li> <code>depth_to_color_extrinsic_parameters</code>: The model uses the extrinsic parameters to shift the 3D depth points to be from the POV of the color camera. </li> </ul> |
| `intrinsic_parameters` | object | **Required** | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `output_image_type` | string | **Required** | Specify `color` or `depth` for the output stream. |
| `color_camera_name` | string | **Required** | `name` of the color camera to pull images from. |
| `depth_camera_name` | string | **Required** | `name` of the depth camera to pull images from. |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false`. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
