---
title: "Configure an Image File Camera"
linkTitle: "image_file"
weight: 31
type: "docs"
description: "Configure a camera that gets color or depth images frames from a file path."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/image-file/"
component_description: "Gets color and depth images frames from a file path."
# SMEs: Bijan, vision team
---

An `image_file` camera gets color and depth image frames or point clouds from a file path on your local system.

{{< tabs name="Configure an Image File Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `image_file` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of an image file camera in the Viam app config builder.](/components/camera/configure-image-file.png)

Edit the attributes as applicable to your camera, according to the table below.
Note that you _must_ specify at least one of `color_image_file_path`, `depth_image_file_path`, and `pointcloud_file_path`.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "image_file",
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
    "distortion_parameters": {
      "rk1": <float>,
      "rk2": <float>,
      "rk3": <float>,
      "tp1": <float>,
      "tp2": <float>
    },
    "debug": <boolean>,
    "color_image_file_path": "<your-file-path>",
    "depth_image_file_path": "<your-file-path>",
    "pointcloud_file_path": "<your-file-path>",
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `image_file` cameras:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |
| `color_image_file_path` | string | Optional | The file path to the color image on your local system. |
| `depth_image_file_path` | string | Optional | The file path to the depth image on your local system. |
| `pointcloud_file_path` | string | Optional | The file path to the point cloud file on your local system. |

You must specify at least one of `color_image_file_path`, `depth_image_file_path`, and `pointcloud_file_path`.

If you provide configuration for the `depth_image_file_path` and `intrinsic_parameters` of the camera, then your machine will also retrieve point cloud data from the `depth_image_file_path`.
If you then also configure a `pointcloud_file_path` on your camera, Viam will try to pull the data from the `pointcloud_file_path` first.

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
