---
title: "Configure a Dual Stream Camera"
linkTitle: "Dual Stream"
weight: 36
type: "docs"
description: "Combine the streams of two camera servers to create colorful point clouds."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `dual_stream` HTTP server camera combines the streams of two camera servers to create colorful point clouds.
One camera server streams a color stream and the other camera server streams a depth stream.

{{< tabs name="Configure a Dual Stream Camera" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> tab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>dual_stream</code> model.
<br>
<img src="../img/create-dual-stream.png" alt="Creation of a dual stream camera in the Viam App config builder." />
<br>
Fill in the attributes for dual stream camera:
<br>
<img src="../img/configure-dual-stream.png" alt="Configuration of a dual stream camera in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "dual_stream",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <number>,
            "fy": <number>,
            "ppx": <number>,
            "ppy": <number>
        },
        "distortion_parameters": {
            "rk1": <number>,
            "rk2": <number>,
            "rk3": <number>,
            "tp1": <number>,
            "tp2": <number>
        },
        "stream": "<color|depth>",
        "debug": <boolean>,
        "color_url": <string>,
        "depth_url": <string>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for dual stream cameras views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Optional* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `stream` | *Required* | `color` or `depth`. The image to be returned when you call `Next()` or `NextPointCloud()`. |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |
| `color_url` | *Required* | The color stream url. |
| `depth_url` | *Required* | The depth stream url. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
