---
title: "Configure an RTSP camera"
linkTitle: "rtsp"
weight: 34
type: "docs"
description: "Configure a streaming camera with an MJPEG track."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

The `rtsp` camera model supports streaming cameras with MJPEG tracks.

{{< alert title="Info" color="info" >}}
If your streaming camera uses H264 or MP4 tracks, use the [`ffmpeg` camera](/components/camera/ffmpeg/) instead.
{{< /alert >}}

{{< tabs name="Configure an rtsp camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `rtsp` model.
Enter a name for your camera and click **Create**.

![Configuration of a rtsp camera in the Viam app config builder.](/components/camera/configure-rtsp.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "rtsp_address": "<your-video-path>",
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
  }
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "rtsp_address": "rtsp://admin:456789@111.123.1.180:540/media/video1"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "rtsp",
  "type": "camera",
  "namespace": "rdk",
  "rtsp_address": "<your-rtsp-address>",
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
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `rtsp` cameras:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `rtsp_address` | string | **Required** | The RTSP address where the camera streams. |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
