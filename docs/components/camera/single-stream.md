---
title: "Configure a Single Stream Camera"
linkTitle: "single_stream"
weight: 36
type: "docs"
description: "Configure a camera that streams image data from an HTTP endpoint."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
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

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `single_stream` model.

![Creation of a single stream camera in the Viam app config builder.](../img/create-single-stream.png)

Fill in the attributes for your single stream camera:

![Configuration of a single stream camera in the Viam App config builder.](../img/configure-single-stream.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "single_stream",
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
        "stream": <color|depth>,
        "debug": <boolean>,
        "url": <string>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `single_stream` cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `url` | **Required** | The color or depth stream url. |
| `intrinsic_parameters` | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `stream` | **Required** | `color` or `depth`. The image to be returned when you call `Next()` or `NextPointCloud()`. |
| `debug` | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

If you have a camera that uses its own SDK to access its images and point clouds (like an Intel RealSense camera), you can attach a camera server as a remote component to your robot.
These remote cameras show up just like regular cameras on your robot.

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
