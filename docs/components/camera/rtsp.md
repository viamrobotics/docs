---
title: "Configure an RTSP camera"
linkTitle: "rtsp"
weight: 34
type: "docs"
description: "Configure a streaming camera with an MJPEG track."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

The `rtsp` camera model supports streaming cameras with MJPEG tracks.
The model doesn’t support streaming cameras with H264/MP4 tracks.

{{< tabs name="Configure an rtsp camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `rtsp` model.

![Creation of a rtsp camera in the Viam app config builder.](../img/create-rtsp.png)

Fill in the attributes for your RTSP camera:

![Configuration of a rtsp camera in the Viam app config builder.](../img/configure-rtsp.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "rtsp",
    "rtsp_address": "<string>",
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
        }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `rtsp` cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `rtsp_address` | **Required** | The RTSP address where the camera streams. |
| `intrinsic_parameters` | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
