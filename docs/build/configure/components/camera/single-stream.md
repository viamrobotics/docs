---
title: "Configure a Single Stream Camera"
linkTitle: "single_stream"
weight: 36
type: "docs"
description: "Configure a camera that streams image data from an HTTP endpoint."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/single-stream/"
# SMEs: Bijan, vision team
---

A `single_stream` camera reads from a HTTP server streaming image data.

The server that the model reads from should output an image:

- If it's a color image server, then it should output JPEG, PNG, or Viam's custom color format, [`image/vnd.viam.rgba`](https://github.com/viamrobotics/rdk/blob/main/rimage/image_file.go#L51).
- If it's a depth image server, it should output either a Z16 PNG, or Viam's custom depth format, [`image/vnd.viam.dep`](https://github.com/viamrobotics/rdk/blob/main/rimage/image_file.go#L87).

Your `single_stream` camera can output:

- A `depth` stream which outputs a 2D depth map or, if you provide `intrinsic_parameters`, a point cloud.
- A `color` stream which outputs color values in 2D.

{{< tabs name="Configure a single Stream Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `single_stream` model.
Enter a name for your camera and click **Create**.

![Configuration of a single stream camera in the Viam App config builder.](/build/configure/components/camera/configure-single-stream.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "stream": "<color|depth>",
  "url": "<URL>",
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
  "debug": <boolean>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "stream": "color",
  "url": "http://urltogetstreamingimagedatafrom"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "single_stream",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "stream": "<color|depth>",
    "url": "<string>",
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
    "debug": <boolean>
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `single_stream` cameras:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `stream` | string | **Required** | `color` or `depth`. The image to be returned when you call `Next()` or `NextPointCloud()`. |
| `url` | string | **Required** | The color or depth stream URL. |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

If you have a camera that uses its own SDK to access its images and point clouds (like an Intel RealSense camera), you can add a camera server as a {{< glossary_tooltip term_id="remote" text="remote" >}} component of your robot.
These remote cameras are treated like any other camera on your robot.

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
