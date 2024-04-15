---
title: "Configure a Dual Stream Camera"
linkTitle: "dual_stream"
weight: 37
type: "docs"
description: "Combine the streams of two camera servers to create colorful point clouds."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/dual-stream/"
# SMEs: Bijan, vision team
---

A `dual_stream` HTTP client camera combines the streams of two camera servers to create colorful point clouds.
One camera server streams a color stream and the other camera server streams a depth stream.

{{< tabs name="Configure a Dual Stream Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `dual_stream` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of a dual stream camera in the Viam app config builder.](/components/camera/configure-dual-stream.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "stream": "<color|depth>",
  "color_url": <string>,
  "depth_url": <string>,
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
  "color_url": "http://urltogetstreamingcolordatafrom",
  "depth_url": "http://urltogetstreamingdepthdatafrom"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "dual_stream",
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
    "stream": "<color|depth>",
    "debug": <boolean>,
    "color_url": <string>,
    "depth_url": <string>
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `dual_stream` cameras views:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `stream` | string | **Required** | `color` or `depth`. The image stream to return when you call `Next()` or `NextPointCloud()`. |
| `color_url` | string | **Required** | The color stream url. |
| `depth_url` | string | **Required** | The depth stream url. |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
