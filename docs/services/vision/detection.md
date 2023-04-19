---
title: "Detection (or 2D object detection)"
linkTitle: "Detection"
weight: 10
type: "docs"
description: "Select an algorithm that identifies objects in a 2D image and adds bounding boxes around identified objects."
tags: ["vision", "computer vision", "CV", "services", "detection"]
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.3.0 and API v0.2.0](/appendix/release-notes/#2-may-2023)_

_2D Object Detection_ is the process of taking a 2D image from a camera and identifying and drawing a box around the distinct "objects" of interest in the scene.
Any camera that can return 2D images can use 2D object detection.

The service provides different types of detectors, both based on heuristics and machine learning, so that you can create, register, and use detectors for any object you may need to identify.

The returned detections consist of the bounding box around the identified object, as well as its label and confidence score:

- `x_min`, `y_min`, `x_max`, `y_max` (int): specify the bounding box around the object.
- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

You can use the following types of detectors:

- [**color_detector**](#configure-a-color_detector): A heuristic detector that draws boxes around objects according to their hue (does not detect black, gray, and white).
- [**tflite_detector**](#configure-a-tflite_detector): A machine learning detector that draws bounding boxes according to the specified .tflite model file available on the robot’s hard drive.

## Configure a `color_detector`

A heuristic detector that draws boxes around objects according to their hue.
Color detectors do not detect black, perfect grays (grays where the red, green, and blue color component values are equal), or white.
It only detects hues found on the color wheel.

{{% alert title="Note" color="note" %}}
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual camera component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

If the color is not reliably detected, increase the `hue_tolerance_pct`.
{{< /alert >}}

### Create the Vision Service that uses the `color_detector`

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the Vision Service to.
Select the **config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select `ml_model` as the **Model**.
4. Click **Create Service**.

In your Vision Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
      "segment_size_px": <integer>,
      "detect_color": "#ABCDEF",
      "hue_tolerance_pct": <number>,
      "saturation_cutoff_pct": <number>,
      "value_cutoff_pct": <number>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the Vision Service object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<service_name>",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": <integer>,
      "detect_color": "#ABCDEF",
      "hue_tolerance_pct": <number>,
      "saturation_cutoff_pct": <number>,
      "value_cutoff_pct": <number>
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "blue_square",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 100,
      "detect_color": "#1C4599",
      "hue_tolerance_pct": 0.07,
      "value_cutoff_pct": 0.15
    }
  },
  {
    "name": "green_triangle",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 200,
      "detect_color": "#62963F",
      "hue_tolerance_pct": 0.05,
      "value_cutoff_pct": 0.20
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"color_detector"`.

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `segment_size_px` | _Required_ | An integer that sets a minimum size (in pixels) of a contiguous color region to be detected, and filters out all other found objects below that size. |
| `detect_color` | _Required_ | The color to detect in the image, as a string of the form `#RRGGBB`. The color is written as a hexadecimal string prefixed by ‘#’. |
| `hue_tolerance_pct` | _Required_ | A number bigger than 0.0 and smaller than or equal to 1.0 that defines how strictly the detector must match to the hue of the color requested. ~0.0 means the color must match exactly, while 1.0 matches to every color, regardless of the input color. 0.05 is a good starting value. |
| `saturation_cutoff_pct` | _Optional_ | A number > 0.0 and <= 1.0 which defines the minimum saturation before a color is ignored. Defaults to 0.2. |
| `value_cutoff_pct` | _Optional_ | A number > 0.0 and <= 1.0 which defines the minimum value before a color is ignored. Defaults to 0.3. |

{{% alert title="Note" color="note" %}}

**hue_tolerance_pct**, **saturation_cutoff_pct**, and **value_cutoff_pct** refer to hue, saturation, and value (brightness) in the HSV Color Model, but do not set color values in Viam.

**hue_tolerance_pct** specifies the exactness of the color match to **detect_color**.

The optional **saturation_cutoff_pct** and **value_cutoff_pct** attributes specify cutoff thresholds levels for saturation and brightness, rather than specifying color saturation and brightness as they do in the standard HSV Color Model.

{{% /alert %}}

Click **Save config** and head to the **Components** tab.
Proceed to [Add a camera component and a "transform" model](#add-a-camera-component-and-a-transform-model).

## Configure a `tflite_detector`

A machine learning detector that draws bounding boxes according to the specified tensorflow-lite model file available on the robot’s hard drive.

### Create the ML Model Service for the classifier

Navigate to the [robot page on the Viam app](https://app.viam.com/robots), then create an ML Model Service for the classifier model:

{{< tabs >}}
{{% tab name="Builder" %}}
Click on the robot you wish to add the classifier to.
Select the **config** tab, and click on **Services**.

Scroll to the **Create Service** section:

1. Select `ml_model` as the **Type**.
2. Enter a name as the **Name**.
3. Select `tflite_cpu` as the **Model**.
4. Click **Create Service**.

In your ML Model Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
      "model_path": "/path/to/file.tflite",
      "label_path": "/path/to/labels.tflite",
      "num_threads": <number>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the classifier ML model object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<classifier_name>",
    "type": "ml_model",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "/path/to/file.tflite",
      "label_path": "/path/to/labels.tflite",
      "num_threads": <number>
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "person_detector",
    "type": "ml_model",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "/path/to/file.tflite",
      "label_path": "/path/to/labels.tflite",
      "num_threads": 1
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"tflite_cpu"` model:

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `model_path` | _Required_ | The path to the `.tflite model` file, as a `string`. |
| `label_path` | _Optional_ | The path to a `.txt` file that holds class labels for your TFLite model, as a `string`. The SDK expects this text file to contain an ordered listing of the class labels. Without this file, classes will read as "1", "2", and so on. |
| `num_threads` | _Optional_ | An integer that defines how many CPU threads to use to run inference. Default: `1`. |

Click **Save config**.

#### `tflite_model` Limitations

We strongly recommend that you package your `.tflite` model with metadata in [the standard form](https://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs).

In the absence of metadata, your `.tflite` model must satisfy the following requirements:

- A single input tensor representing the image of type UInt8 (expecting values from 0 to 255) or Float 32 (values from -1 to 1).
- At least 3 output tensors (the rest won’t be read) containing the bounding boxes, class labels, and confidence scores (in that order).
- Bounding box output tensor must be ordered [x x y y], where x is an x-boundary (xmin or xmax) of the bounding box and the same is true for y.
  Each value should be between 0 and 1, designating the percentage of the image at which the boundary can be found.

These requirements are satisfied by a few publicly available model architectures including EfficientDet, MobileNet, and SSD MobileNet V1.
You can use one of these architectures or build your own.

### Create the Vision Service that uses the `tflite_model` detector

Create another service:

{{< tabs >}}
{{% tab name="Builder" %}}

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select `ml_model` as the **Model**.
4. Click **Create Service**.

In your Vision Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
  "ml_model_name": "<classifier_name>"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the Vision Service object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<service_name>",
    "type": "vision",
    "model": "ml_model",
    "attributes": {
      "ml_model_name": "<classifier_name>"
    }
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "person_detector",
    "type": "vision",
    "model": "ml_model",
    "attributes": {
      "ml_model_name": "person_detector"
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

Click **Save config** and head to the **Components** tab.

## Add a camera component and a "transform" model

You cannot interact directly with the [Vision Service](/services/vision/).
To be able to interact with the Vision Service you must:

1. Configure a physical [camera component](../../../components/camera).
2. Configure a [transform camera](../../../components/camera/transform) to view output from the detector overlaid on images from the physical camera.

After adding the component and its attributes, click **Save config**.

Wait for the robot to reload, and then go to the **control** tab to test the stream of detections.

## Code

The following code gets the robot’s vision service and then runs a color detector vision model on an image from the robot's camera `"camera_1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionServiceClient, VisModelConfig, VisModelType

robot = await connect()
# grab camera from the robot
cam1 = Camera.from_robot(robot, "cam1")
# grab Viam's vision service for the detector
my_detector = VisionServiceClient.from_robot(robot, "my_detector")

img = await cam1.get_image()
detections = await my_detector.get_detections(img)

await robot.close()
```

To learn more about how to use detection, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"go.viam.com/rdk/config"
"go.viam.com/rdk/services/vision"
"go.viam.com/rdk/components/camera"
)

// grab the camera from the robot
cameraName := "cam1" // make sure to use the same component name that you have in your robot configuration
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

visService, err := vision.from_robot(robot=robot, name='my_detector')
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// gets the stream from a camera
camStream, err := myCam.Stream(context.Background())

// gets an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()

// Apply the color classifier to the image from your camera (configured as "cam1")
detections, err := visService.GetDetections(context.Background(), img)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detections) > 0 {
    logger.Info(detections[0])
}
```

To learn more about how to use detection, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
To see more code examples of how to use Viam's Vision Service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/services/try-viam-color-detection/" size="small" %}}
  {{% card link="/tutorials/services/color-detection-scuttle/" size="small" %}}
  {{% card link="/tutorials/services/webcam-line-follower-robot/" size="small" %}}
{{< /cards >}}
