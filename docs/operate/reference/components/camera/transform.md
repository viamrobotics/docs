---
title: "Transform a Camera"
linkTitle: "transform"
weight: 60
type: "docs"
description: "Use the transform camera model to apply transformation to a camera stream. For example, crop, resize, or add overlays with info about the camera stream."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/transform/"
component_description: "Use pipelines for applying transformations to an input image source."
toc_hide: true
# SMEs: Rand, AV team
---

Use the `transform` model to apply transformations to input source images.
The transformations are applied in the order they are written in the `pipeline`.

{{< tabs name="Example transform view" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `transform` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of an transform view in the Viam app config builder.](/components/camera/configure-transform.png)

Click the **{}** (Switch to Advanced) button in the top right of the component panel to edit the component's attributes directly with JSON.
Copy and paste the following attribute template into the attributes field.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "source" : "<your-camera-name>",
  "pipeline": [
    { "type": "<transformation-type>", "attributes": { ... } },
  ],
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
  "source": "my-webcam",
  "pipeline": [
    { "type": "rotate", "attributes": {} },
    { "type": "resize", "attributes": { "width_px": 200, "height_px": 100 } }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "transform",
  "api": "rdk:component:camera",
  "attributes" : {
    "source" : "<your-source-camera-name>",
    "pipeline": [
      { "type": "<transformation-type>", "attributes": { ... } },
    ],
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

The following attributes are available for `transform` views:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `source` | string | **Required** | `name` of the camera to transform. |
| `pipeline` | array | **Required** | Specify an array of transformation objects. |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. Value must be >= 0.</li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. Value must be >= 0.</li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |

The following are the transformation objects available for the `pipeline`:

### Classifications

Classifications overlay text from the `GetClassifications` method of the [vision service](/operate/reference/services/vision/) onto the image.

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "classifications",
      "attributes": {
        "classifier_name": "<name>",
        "confidence_threshold": <float>,
        "max_classifications": <int>,
        "valid_labels": [ "<label>" ]
      }
    }
  ]
}
```

**Attributes:**

- `classifier_name`: The name of the classifier in the [vision service](/operate/reference/services/vision/).
- `confidence_threshold`: The threshold above which to display classifications.
- `max_classifications`: _Optional_. The maximum number of classifications to display on the camera stream at any given time. Default: `1`.
- `valid_labels`: _Optional_. An array of labels that you to see detections for on the camera stream. If not specified, all labels from the classifier are used.

### Crop

The Crop transform crops takes an image and crops it to a rectangular area specified by two points: the top left point (`(x_min, y_min)`) and the bottom right point (`(x_max, y_max)`).

{{< tabs >}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "crop",
      "attributes": {
        "x_min_px": <int>,
        "y_min_px": <int>,
        "x_max_px": <int>,
        "y_max_px": <int>,
        "overlay_crop_box": <bool>
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Coordinate Example" %}}

If you have a 100 x 200 image, and you want to crop to a box between the points (30, 40) and (60,80), the following would suffice:

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "crop",
      "attributes": {
        "x_min_px": 30,
        "y_min_px": 40,
        "x_max_px": 60,
        "y_max_px": 80,
        "overlay_crop_box": false
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Proportion Example" %}}

If you have a 100 x 200 image, and you want to crop to a box between the points (30, 40) and (60,80), the following would suffice:

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "crop",
      "attributes": {
        "x_min_px": 0.3,
        "y_min_px": 0.2,
        "x_max_px": 0.6,
        "y_max_px": 0.4,
        "overlay_crop_box": false
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

**Attributes:**

- `x_min_px`: The x coordinate or the relative proportion of the top left point of the rectangular area to crop the image to.
- `y_min_px`: The y coordinate or the relative proportion of the top left point of the rectangular area to crop the image to.
- `x_max_px`: The x coordinate or the relative proportion of the bottom right point of the rectangular area to crop the image to.
- `y_max_px`: The y coordinate or the relative proportion of the bottom right point of the rectangular area to crop the image to.
- `overlay_crop_box`: Set to `true` to not actually carry out the crop, but instead overlay the cropping box on the original image and visualize where the crop would be applied.

### Detections

The Detections transform takes the input image and overlays the detections from a given detector configured within the [vision service](/operate/reference/services/vision/).

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "detector_name": string,
        "confidence_threshold": <float>,
        "valid_labels": ["<label>"]
      }
    }
  ]
}
```

**Attributes:**

- `detector_name`: The name of the detector configured in the [vision service](/operate/reference/services/vision/).
- `confidence_threshold`: Specify to only display detections above the specified threshold (decimal between 0 and 1).
- `valid_labels`: _Optional_. An array of labels that you to see detections for on the camera stream. If not specified, all labels from the classifier are used.

### Resize

The Resize transform resizes the image to the specified height and width.

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "resize",
      "attributes": {
        "width_px": <int>,
        "height_px": <int>
      }
    }
  ]
}
```

**Attributes:**

- `width_px`: Specify the expected width for the aligned image. Value must be >= 0.
- `height_px`: Specify the expected width for the aligned image. Value must be >= 0.

### Rotate

The Rotate transformation rotates the image by the angle specified in `angle_deg`. Default: 180 degrees.
This feature is useful for when the camera is installed upside down or sideways on your machine.

```json {class="line-numbers linkable-line-numbers"}
{
  "source": "<your-source-camera-name>",
  "pipeline": [
    {
      "type": "rotate",
      "attributes": {
        "angle_degs": <float>
      }
    }
  ]
}
```

**Attributes:**

- `angle_deg`: Rotate the image by a specific angle in degrees.

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/camera.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}
