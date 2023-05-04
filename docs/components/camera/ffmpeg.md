---
title: "Configure a FFmpeg Camera"
linkTitle: "ffmpeg"
weight: 30
type: "docs"
description: "Uses a camera, a video file, or a stream as a camera."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `ffmpeg` camera uses a camera, a video file, or a stream as a camera.

{{< tabs name="Configure a ffmpeg camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `ffmpeg` model.

Click **Create component**.

![Configuration of a ffmpeg camera in the Viam app config builder.](../img/configure-ffmpeg.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-camera-name>",
    "type": "camera",
    "model" : "ffmpeg",
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
        "video_path": "<your-video-path>",
        "input_kw_args": { ... },
        "filters": [
            {
            "name": <string>,
            "args": [ "<first>", "<second>", ... ],
            "kw_args": { ... }
            }
        ],
        "output_kw_args": { ... },
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `ffmpeg` cameras:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `video_path` | string | **Required** | The file path to the color image. |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |
| `input_kw_args` | object | Optional | The input keyword arguments. |
| `filters` | array | Optional | The file path to the depth image. Array of filter objects that specify: <ul> <li> <code>name</code>: The name of the filter. </li> <li> <code>args</code>: The arguments for the filter. </li> <li> <code>kw_args</code>: Any keyword arguments for the filter. </li> </ul> |
| `output_kw_args` | object | Optional | The output keyword arguments. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
