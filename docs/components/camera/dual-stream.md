---
title: "Configure a Dual Stream Camera"
linkTitle: "dual_stream"
weight: 37
type: "docs"
description: "Combine the streams of two camera servers to create colorful point clouds."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `dual_stream` HTTP client camera combines the streams of two camera servers to create colorful point clouds.
One camera server streams a color stream and the other camera server streams a depth stream.

{{< tabs name="Configure a Dual Stream Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `dual_stream` model.

Click **Create component**.

![Configuration of a dual stream camera in the Viam app config builder.](/components/camera/configure-dual-stream.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-camera-name>",
    "type": "camera",
    "model" : "dual_stream",
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

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
