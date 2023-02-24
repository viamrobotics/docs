---
title: "Configure a Single Stream Camera"
linkTitle: "Single Stream"
weight: 35
type: "docs"
description: "Configure a camera that streams image data from an HTTP endpoint."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `single_stream` HTTP server camera is a camera server streaming image data from an HTTP endpoint.
Your `single_stream` camera can output:

- a `depth` stream which outputs a point cloud
- a `color` stream which outputs color values in 2D

{{< tabs name="Configure a single Stream Camera" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>single_stream</code> model.
<br>
<img src="../img/create-single-stream.png" alt="Creation of a single stream camera in the Viam app config builder." style="max-width:500px" />
<br>
Fill in the attributes for your single stream camera:
<br>
<img src="../img/configure-single-stream.png" alt="Configuration of a single stream camera in the Viam App config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
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

The following attributes are available for single stream cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Optional* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `stream` | *Required* | `color` or `depth`. The image to be returned when you call `Next()` or `NextPointCloud()`. |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |
| `url` | *Required* | The color or depth stream url. |

If you have a camera that uses its own SDK to access its images and point clouds (like an Intel RealSense camera), you can attach a camera server as a remote component to your robot.
These remote cameras show up just like regular cameras on your robot.

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
