---
title: "Configure an mlmodel Detector or Classifier"
linkTitle: "mlmodel"
weight: 10
type: "docs"
description: "A detector or classifier that uses a tflite model available on the machine to draw bounding boxes around objects or return a class label."
tags: ["vision", "computer vision", "CV", "services", "detection"]
images: ["/ml/vision/dog-detector.png"]
aliases:
  - "/services/vision/detection/"
  - "/services/vision/classification/"
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.2.36 and API v0.1.118](/appendix/changelog/#vision-service)_

The `mlmodel` vision service model is a machine learning detector that draws bounding boxes or returns class labels according to the specified TensorFlow Lite model file available on the machine’s hard drive.
To create a `mlmodel` classifier, you need an [ML model service with a suitable model](/ml/).
Before configuring your `mlmodel` detector or classifier, you need to:

{{< cards >}}
{{% manualcard %}}

<h4>Train or upload an ML model</h4>

You can [add an existing model](/ml/upload-model/) or [train your own models](/ml/train-model/) for object detection and classification using data from the [data management service](/data/).

{{% /manualcard %}}
{{% manualcard %}}

<h4>Deploy your model</h4>

To make use of ML models with your machine, use the built-in [ML model service](/ml/) to deploy and run the model.
s
{{% /manualcard %}}
{{< /cards >}}

<br>

Once you have deployed your ML model, configure your `mlmodel` detector or classifier:

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/robots).
Click the **Services** subtab and click **Create service** in the lower-left corner.
Select the `Vision` type, then select the `ML Model` model.
Enter a name for your service and click **Create**.

In your vision service's panel, fill in the **Attributes** field.

```json {class="line-numbers linkable-line-numbers"}
{
  "mlmodel_name": "<mlmodel-service-name>"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<service_name>",
    "type": "vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "<mlmodel-service-name>"
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

{{< tabs >}}
{{% tab name="Detector" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "person_detector",
    "type": "vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "my_mlmodel_service"
    }
  }
]
```

{{% /tab %}}
{{% tab name="Classifier" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "fruit_classifier",
    "type": "vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "fruit_classifier"
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

Click **Save config**.

The following attributes are available for an `mlmodel` detector or classifier:

<!-- prettier-ignore -->
| Parameter | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `mlmodel_name` | string | **Required** | The name of the [ML model service](/ml/deploy) you want to use the model from. |
| `remap_output_names` | object | Optional | The names of your output tensors, mapped to the service requirements. See [Tensor names](#tensor-names) for more information. |
| `remap_input_names` | object | Optional | The name of your input tensor, mapped to the service requirements. See [Tensor names](#tensor-names) for more information. |
| `input_image_bgr` | bool | Optional | Set this to `true` if the ML model service expect the input image to have BGR pixels, rather than RGB pixels. |
| `input_image_mean_value` | array | Optional | The standard deviation of the RGB (or BGR) values. Only required if the ML model service expects the input image to be normalized. |
| `input_image_std_dev` | array | Optional | The standard deviation of the RGB (or BGR) values. Only required if the ML model service expects the input image to be normalized. |

## Tensor names

Both the `mlmodel` detector and classifier require that the input and output tensors defined by your ML model are named according to the following:

- For an `mlmodel` detector:
  - The _input tensor_ must be named `image`
  - The _output tensors_ must be named `location`, `category`, and `score`,
- For an `mlmodel` classifier:
  - The _input tensor_ must be named `image`
  - The _output tensor_ must be named `probability`

If you [trained your ML model using the Viam app](/ml/train-model/), your `mlmodel` tensors are already named in this fashion, and you can proceed to [test your detector or classifier](#test-your-detector-or-classifier).
However, if you [uploaded your own ML model](/ml/upload-model/), or are using one from the [Viam registry](https://app.viam.com/registry), you may need to remap your tensor names to meet this requirement, and should follow the instructions to [remap tensor names](#remap-tensor-names).

{{%expand "Click for details on how to remap tensor names." %}}

### Remap tensor names

If you need to remap the tensor names defined by your ML model to meet the tensor name requirements of the `mlmodel` detector or classifier, you can use the `remap_input_names` and `remap_output_names` attributes:

{{< tabs >}}
{{% tab name="Detector" %}}

To remap your model's tensor names to work with an `mlmodel` detector, add the following to your `mlmodel` vision service configuration, replacing the `my_model` input and output tensor names with the names from your model:

```json {class="line-numbers linkable-line-numbers"}
{
  "type": "vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my_model",
    "remap_output_names": {
      "my_model_output_tensor1": "category",
      "my_model_output_tensor2": "location",
      "my_model_output_tensor3": "score"
    },
    "remap_input_names": {
      "my_model_input_tensor1": "image"
    }
  },
  "name": "my-vision-service"
}
```

{{% /tab %}}
{{% tab name="Classifier" %}}

To remap your model's tensor names to work with an `mlmodel` classifier, add the following to your `mlmodel` vision service configuration, replacing the `my_model` input and output tensor names with the names from your model:

```json {class="line-numbers linkable-line-numbers"}
{
  "type": "vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my_model",
    "remap_output_names": {
      "my_model_output_tensor1": "probability"
    },
    "remap_input_names": {
      "my_model_input_tensor1": "image"
    }
  },
  "name": "my-vision-service"
}
```

{{% /tab %}}
{{< /tabs >}}

When done, click **Save config**, then proceed to [test your detector or classifier](#test-your-detector-or-classifier).

{{% /expand%}}

## Test your detector or classifier

You can test your detector or classifier with [existing images in the Viam app](#existing-images-in-the-cloud) or [live camera footage](#live-camera-footage).
You can also test classifiers with [existing images on a computer](#existing-images-on-your-machine).

### Existing images in the cloud

{{< alert title="Note" color="note" >}}

The feature is only available for classifiers that are uploaded after September 19, 2023.

{{< /alert >}}

{{<gif webm_src="/ml/vision/mug-classifier.webm" mp4_src="/ml/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

If you have images stored in the [Viam cloud](/data/), you can run your classifier against your images in the [Viam app](https://app.viam.com/).

1. Navigate to the [Data tab](/data/view/) and click on the **Images** subtab.
2. Click on an image to open the side menu, and select the **Actions** tab under the **Data** tab.
3. In the **Run model** section, select your model and specify a confidence threshold.
4. Click **Run model**

If the classifier's results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

### Live camera footage

If you intend to use the detector or classifier with a camera that is part of your machine, you can test your detector or classifier from the [**Control tab**](/fleet/machines/#control) or with code:

1. Configure a [camera component](/components/camera/).

   {{< alert title="Tip" color="tip" >}}
   This is the camera whose name you need to pass to vision service methods.
   {{< /alert >}}

2. (Optional) If you would like to see detections or classifications from the **Control tab**, configure a [transform camera](/components/camera/transform/) with the following attributes:

{{< tabs >}}
{{% tab name="Detections" %}}

```json
{
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "confidence_threshold": 0.5,
        "detector_name": "<vision-service-name>",
        "valid_labels": ["<label>"]
      }
    }
  ],
  "source": "<camera-name>"
}
```

{{% /tab %}}
{{% tab name="Classifications" %}}

```json
{
  "pipeline": [
    {
      "type": "classifications",
      "attributes": {
        "confidence_threshold": 0.5,
        "classifier_name": "<vision-service-name>",
        "max_classifications": <int>,
        "valid_labels": [ "<label>" ]
      }
    }
  ],
  "source": "<camera-name>"
}
```

{{% /tab %}}
{{< /tabs >}}

3. After adding the components and their attributes, click **Save config**.
4. Navigate to the **Control** tab, click on your transform camera and toggle it on.
   If you've configured a detector, the transform camera will now show detections with bounding boxes around the object.

   ![Viam app control tab interface showing bounding boxes around two office chairs, both labeled "chair" with confidence score "0.50."](/ml/vision/chair-detector.png)

   If you've configured a classifier, the transform camera will now show classifications on the image.

   ![Model recognizes a star on camera feed](/services/model-on-camera.png)

5. The following code gets the machine’s vision service and then runs a detector or classifier vision model on an image from the machine's camera `"cam1"`.

   {{% alert title="Tip" color="tip" %}}

Pass the name of the camera you configured in step 1.
Do not pass a transform camera that already has the "detections" or "classifications" transform applied to it.

    {{% /alert %}}

{{< tabs >}}
{{% tab name="Detections" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "cam1"

# Grab camera from the machine
cam1 = Camera.from_robot(robot, camera_name)
# Grab Viam's vision service for the detector
my_detector = VisionClient.from_robot(robot, "my_detector")

detections = await my_detector.get_detections_from_camera(camera_name)

# If you need to store the image, get the image first
# and then run detections on it. This process is slower:
img = await cam1.get_image()
detections_from_image = await my_detector.get_detections(img)

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

// Grab the camera from the machine
cameraName := "cam1" // make sure to use the same component name that you have in your machine configuration
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

myDetector, err := vision.from_robot(robot, "my_detector")
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get detections from the camera output
detections, err := myDetector.DetectionsFromCamera(context.Background(), myCam, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(directDetections) > 0 {
    logger.Info(detections[0])
}

// If you need to store the image, get the image first
// and then run detections on it. This process is slower:

// Get the stream from a camera
camStream, err := myCam.Stream(context.Background())

// Get an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()

// Apply the color classifier to the image from your camera (configured as "cam1")
detectionsFromImage, err := myDetector.Detections(context.Background(), img, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detectionsFromImage) > 0 {
    logger.Info(detectionsFromImage[0])
}

```

To learn more about how to use detection, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Classifications" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "cam1"
# Grab camera from the machine
cam1 = Camera.from_robot(robot, camera_name)
# Grab Viam's vision service for the classifier
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get the top 2 classifications with the highest confidence scores from the
# camera output
classifications = await my_classifier.get_classifications_from_camera(
    camera_name, 2)

# If you need to store the image, get the image first
# and then run classifications on it. This process is slower:
img = await cam1.get_image()
classifications_from_image = await my_classifier.get_classifications(img, 2)

await robot.close()
```

To learn more about how to use classification, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

    {{% /tab %}}
    {{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/config"
  "go.viam.com/rdk/services/vision"
  "go.viam.com/rdk/components/camera"
)

// Grab the camera from the machine
cameraName := "cam1" // make sure to use the same component name that you have in your machine configuration
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

myClassifier, err := vision.from_robot(robot, "my_classifier")
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get the top 2 classifications with the highest confidence scores from the camera output
classifications, err := visService.ClassificationsFromCamera(context.Background(), myCam, 2, nil)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(directClassifications) > 0 {
    logger.Info(classifications[0])
}

// If you need to store the image, get the image first
// and then run classifications on it. This process is slower:

// Get the stream from a camera
camStream, err := myCam.Stream(context.Background())

// Get an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()

// Apply the color classifier to the image from your camera (configured as "cam1")
// Get the top 2 classifications with the highest confidence scores
classificationsFromImage, err := visService.GetClassifications(context.Background(), img, 2, nil)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(classificationsFromImage) > 0 {
    logger.Info(classificationsFromImage[0])
}
```

To learn more about how to use classification, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

### Existing images on your machine

If you would like to test your detector or classifier with existing images, load the images and pass them to the detector or classifier:

{{< tabs >}}
{{% tab name="Detector" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient
from PIL import Image

robot = await connect()
# Grab Viam's vision service for the detector
my_detector = VisionClient.from_robot(robot, "my_detector")

# Load an image
img = Image.open('test-image.png')

# Apply the detector to the image
detections_from_image = await my_detector.get_detections(img)

await robot.close()
```

To learn more about how to use detection, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/config"
  "go.viam.com/rdk/services/vision"
  "image/jpeg"
  "os"
)

myDetector, err := vision.from_robot(robot, "my_detector")
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// Read image from existing file
file, err := os.Open("test-image.jpeg")
if err != nil {
    logger.Fatalf("Could not get image: %v", err)
}
defer file.Close()
img, err := jpeg.Decode(file)
if err != nil {
    logger.Fatalf("Could not decode image: %v", err)
}
defer img.Close()

// Apply the detector to the image
detectionsFromImage, err := myDetector.Detections(context.Background(), img, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detectionsFromImage) > 0 {
    logger.Info(detectionsFromImage[0])
}

```

To learn more about how to use detection, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Classifier" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient
from PIL import Image

robot = await connect()
# Grab Viam's vision service for the classifier
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Load an image
img = Image.open('test-image.png')

# Apply the classifier to the image
classifications_from_image = await my_classifier.get_classifications(img)

await robot.close()
```

To learn more about how to use classification, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/config"
  "go.viam.com/rdk/services/vision"
  "image"
  "image/png"
  "os"
)

myClassifier, err := vision.from_robot(robot, "my_classifier")
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// Read image from existing file
file, err := os.Open("test-image.jpeg")
if err != nil {
    logger.Fatalf("Could not get image: %v", err)
}
defer file.Close()
img, err := jpeg.Decode(file)
if err != nil {
    logger.Fatalf("Could not decode image: %v", err)
}
defer img.Close()

// Apply the classifier to the image
classificationsFromImage, err := myClassifier.Classifications(context.Background(), img, nil)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(classificationsFromImage) > 0 {
    logger.Info(classificationsFromImage[0])
}

```

To learn more about how to use classification, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
To see more code examples of how to use Viam's vision service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/services/try-viam-color-detection/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/services/webcam-line-follower-robot/" %}}
{{< /cards >}}
