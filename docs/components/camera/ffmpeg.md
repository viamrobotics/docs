---
title: "Configure a FFmpeg Camera"
linkTitle: "FFmpeg"
weight: 30
type: "docs"
description: "Uses a camera, a video file, or a stream as a camera."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `ffmpeg` camera uses a camera, a video file, or a stream as a camera.

{{< tabs name="Configure a ffmpeg camera" >}}
{{% tab name="Config Builder" %}}

On the **Components** subtab, navigate to the **Create Component** menu.
Enter a name for your camera, select the type `camera`, and select the `ffmpeg` model.

<img src="../img/create-ffmpeg.png" alt="Creation of a ffmpeg camera in the Viam app config builder." style="max-width:600px" />

Fill in the attributes for your ffmpeg camera:

<img src="../img/configure-ffmpeg.png" alt="Configuration of a ffmpeg camera in the Viam app config builder." />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "ffmpeg",
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
        "video_path": <string>,
        "input_kw_args": { ... },
        "filters": [
            {
            "name": <string>,
            "args": [ <string>, <string>, ... ],
            "kw_args": { ... }
            }
        ],
        "output_kw_args": { ... },
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for ffmpeg cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Optional* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |
| `video_path` | *Required* | The file path to the color image. |
| `input_kw_args` | *Optional* | The input keyword arguments. |
| `filters` | *Optional* | The file path to the depth image. Array of filter objects that specify: <ul> <li> <code>name</code>: The name of the filter. </li> <li> <code>args</code>: The arguments for the filter. </li> <li> <code>kw_args</code>: The kw arugments for the filter ???. </li> </ul> |
| `output_kw_args` | *Optional* | The output keyword arguments. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
