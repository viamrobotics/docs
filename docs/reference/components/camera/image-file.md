---
title: "image_file"
linkTitle: "image_file"
weight: 31
type: "docs"
description: "Reference for the image_file camera model. Serves color or depth image frames from a file path."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/image-file/"
  - "/reference/components/camera/image-file/"
component_description: "Gets color and depth image frames from a file path."
# SMEs: Bijan, vision team
---

An `image_file` camera gets color and depth image frames or point clouds from a file path on your local system.

## Configuration

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "image_file",
  "api": "rdk:component:camera",
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
    "color_image_file_path": "<your-file-path>",
    "depth_image_file_path": "<your-file-path>",
    "pointcloud_file_path": "<your-file-path>",
    "preloaded_image: "<pizza|dog|crowd>"
  }
}
```

## Attributes

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. Value must be >= 0. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. Value must be >= 0. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `color_image_file_path` | string | Optional | The file path to the color image on your local system. |
| `depth_image_file_path` | string | Optional | The file path to the depth image on your local system. |
| `pointcloud_file_path` | string | Optional | The file path to the point cloud file on your local system. |
| `preloaded_image` | string | Optional | Select a pre-loaded image for the camera to display. Options: `"pizza"`, `"dog"`, `"crowd"`. |

You must specify at least one of `color_image_file_path`, `depth_image_file_path`, and `pointcloud_file_path`.

If you provide configuration for the `depth_image_file_path` and `intrinsic_parameters` of the camera, then your machine will also retrieve point cloud data from the `depth_image_file_path`.
If you then also configure a `pointcloud_file_path` on your camera, Viam will try to pull the data from the `pointcloud_file_path` first.
