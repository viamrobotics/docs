---
title: "Transform a Camera"
linkTitle: "Transform a Camera"
weight: 60
type: "docs"
description: "Instructions for transforming a camera."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

Use the transform model to apply transformations to input source images.
The transformations are applied in the order they are written in the pipeline.

{{< tabs name="Example transform view" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>transform</code> model.
<br>
<img src="../img/create-transform.png" alt="Creation of an transform view in the Viam app config builder." style="max-width:500px" />
<br>
Fill in the attributes for your transform view:
<br>
<img src="../img/configure-transform.png" alt="Configuration of an transform view in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model": "transform",
    "attributes" : {
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
        "source" : "<camera_name>",
        "pipeline": [
            { "type": "<transformation_type>", "attributes": { ... } },
            ...
        ]
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for transform views:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Optional* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |
| `source` | *Required* | Specify the name of the camera to transform. |
| `pipeline` | *Required* | Specify and array of transformation objects. |

The following are the available transformations:

{{< tabs >}}
{{% tab name="Identity"%}}

The Identity transform does nothing to the image.
You can use this transform to change the underlying camera source's intrinsic parameters or stream type, for example.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "identity"
}
```

**Attributes:**

- None

{{% /tab %}}
{{% tab name="Rotate" %}}

The Rotate transformation rotates the image by 180 degrees.
This feature is useful for when the camera is installed upside down on your robot.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "rotate",
    "attributes": { }
}
```

**Attributes:**

- None

{{% /tab %}}
{{% tab name="Resize" %}}

The Resize transform resizes the image to the specified height and width.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "resize",
    "attributes": {
        "width_px": int,
        "height_px": int
    }
}
```

**Attributes:**

- `width_px`: Specify the expected width for the aligned image.
- `height_px`: Specify the expected width for the aligned image.

{{% /tab %}}
{{% tab name="Depth to Pretty" %}}

The Depth-to-Pretty transform takes a depth image and turns it into a colorful image, with blue indicating distant points and red indicating nearby points.
The actual depth information is lost in the transform.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "depth_to_pretty",
    "attributes": { }
}
```

**Attributes:**

- None.

{{% /tab %}}
{{% tab name="Overlay" %}}

Overlays the depth and the color 2D images.
Useful to debug the alignment of the two images.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "overlay",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": int,
            "height_px": int,
            "ppx": float,
            "ppy": float,
            "fx": float,
            "fy": float,
        }
    }
}
```

**Attributes:**

- `intrinsic_parameters`: The intrinsic parameters of the camera used to do 2D <-> 3D projections.
  - `width_px`: The width of the image in pixels.
  - `height_px`: The height of the image in pixels.
  - `ppx`: The image center x point.
  - `ppy`: The image center y point.
  - `fx`: The image focal x.
  - `fy`: The image focal y.

{{% /tab %}}
{{% tab name="Undistort" %}}

The Undistort transform undistorts the input image according to the intrinsics and distortion parameters specified within the camera parameters.
Currently only supports a Brown-Conrady model of distortion (20 September 2022).
For further information, please refer to the [OpenCV docs](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a).

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "undistort",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": int,
            "height_px": int,
            "ppx": float,
            "ppy": float,
            "fx": float,
            "fy": float
        },
        "distortion_parameters": {
            "rk1": float,
            "rk2": float,
            "rk3": float,
            "tp1": float,
            "tp2": float
        }
    }
}
```

**Attributes:**

- `intrinsic_parameters`: The intrinsic parameters of the camera used to do 2D <-> 3D projections.
  - `width_px`: The expected width of the aligned image in pixels.
  - `height_px`: The expected height of the aligned image in pixels.
  - `ppx`: The image center x point.
  - `ppy`: The image center y point.
  - `fx`: The image focal x.
  - `fy`: The image focal y.
- `distortion_parameters`: Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens.
  - `rk1`: The radial distortion x.
  - `rk2`: The radial distortion y.
  - `rk3`: The radial distortion z.
  - `tp1`: The tangential distortion x.
  - `tp2`: The tangential distortion y.

{{% /tab %}}
{{% tab name="Detections" %}}

The Detections transform takes the input image and overlays the detections from a given detector configured within the [Vision Service](/services/vision/).

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "detections",
    "attributes": {
        "detector_name": string,
        "confidence_threshold": float
    }
}
```

**Attributes:**

- `detector_name`: The name of the detector configured in the [Vision Service](/services/vision).
- `confidence_threshold`: Specify to only display detections above the specified threshold (decimal between 0 and 1).

{{% /tab %}}
{{% tab name="Depth Edges" %}}

The Depth Edges transform creates a canny edge detector to detect edges on an input depth map.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "depth_edges",
    "attributes": {
        "high_threshold_pct": float,
        "low_threshold_pct": float,
        "blur_radius_px": float
    }
}
```

**Attributes:**

- `high_threshold_pct`: The high threshold of ??? : between 0.0 - 1.0.
- `low_threshold_pct`: The low threshold of ??? : between 0.0 - 1.0.
- `blur_radius_px`: The blur radius used to smooth the image before applying the filter.

{{% /tab %}}
{{% tab name="Depth Preprocess" %}}

Depth Preprocessing applies some basic hole-filling and edge smoothing to a depth map.

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "type": "depth_preprocess",
    "attributes": { }
}
```

**Attributes:**

- None.

{{% /tab %}}
{{< /tabs >}}

## Example

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "camera_name",
    "type": "camera",
    "model": "transform",
    "attributes" : {
        "source" : "physical_cam",
        "pipeline": [
            { "type": "rotate", "attributes": { } },
            { "type": "resize", "attributes": {"width_px":200, "height_px" 100} }
        ]
    }
}
```

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col hover-card">
        <a href="../../../services/vision">
        <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Vision Service</h4>
        <p style="text-align: left;">The vision service enables your robot to use its on-board cameras to intelligently see and interpret the world around it.</p>
        <a>
    </div>
    <div class="col hover-card">
        <a href="/tutorials/viam-rover/try-viam-color-detection/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Detect color with a Viam Rover</h4>
            <p style="text-align: left;">Use the vision service in the Viam app to detect a color.</p>
        </a>
    </div>
    <div class="col hover-card">
        <a href="/tutorials/scuttlebot/color-detection-scuttle/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Colored Object Follower</h4>
            <p style="text-align: left;">Instructions for detecting and following a colored object with a SCUTTLE Robot on Viam software.</p>
        </a>
    </div>
  </div>
</div>
