---
title: "Classification (or 2D image classification)"
linkTitle: "Classification"
weight: 20
type: "docs"
description: "Select an algorithm that outputs a class label and confidence score associated with a 2D image."
tags: ["vision", "computer vision", "CV", "services", "classification"]
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.2.36 and API v0.1.118](/appendix/changelog/#april-2023)_

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

The types of classifiers supported are:

- **Object classification (`mlmodel`)**: a machine learning classifier that returns a class label and confidence score according to the specified `tensorflow-lite` model file available on the robot’s hard drive.

## Configure an `mlmodel` classifier

To create an `mlmodel` classifier, you need to first:

{{< cards >}}
{{% manualcard %}}

<h4>Train or upload an ML model</h4>

You can [add an existing model](/manage/ml/upload-model/) or [train your own models](/manage/ml/train-model/) for object detection and classification using data from the [data management service](/services/data/).

{{% /manualcard %}}
{{% manualcard %}}

<h4>Deploy your model</h4>

To make use of ML models with your smart machine, use the built-in [ML model service](/services/ml/) to deploy and run the model.

{{% /manualcard %}}

{{< /cards >}}

<br>

Once you have deployed your ML model, configure your `mlmodel` classifier:

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to your robot's **Config** tab on the [Viam app](https://app.viam.com/robots).
Click the **Services** subtab and click **Create service** in the lower-left corner.
Select the `Vision` type, then select the `ML Model` model.
Enter a name for your service and click **Create**.

In your vision service's panel, fill in the **Attributes** field.

```json {class="line-numbers linkable-line-numbers"}
{
  "mlmodel_name": "<classifier_name>"
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
      "mlmodel_name": "<classifier_name>"
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

Click **Save config**.
Proceed to [test your classifier](#test-your-classifier).

## Test your classifier

You can test your classifier with [existing images in the Viam app](#existing-images-in-the-cloud), [live camera footage](#live-camera-footage), or [existing images on a computer](#existing-images-on-your-machine).

### Existing images in the cloud

{{< alert title="Note" color="note" >}}

The feature is only available for classifiers that were uploaded after September 19, 2023.

{{< /alert >}}

{{<gif webm_src="/services/vision/mug-classifier.webm" mp4_src="/services/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

If you have images stored in the [Viam cloud](/manage/data/), you can run your classifier against your images in the [Viam app](https://app.viam.com/).

1. Navigate to the [Data tab](/manage/data/view/) and click on the **Images** subtab.
2. Click on an image to open the side menu, and select the **Actions** tab under the **Data** tab.
3. In the **Run model** section, select your model and specify a confidence threshold.
4. Click **Run model**

If the classifier's results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

### Live camera footage

If you intend to use the classifier with a camera that is part of your robot, you can test your classifier from the [**Control tab**](/manage/fleet/robots/#control) or with code:

1. Configure a [camera component](../../../components/camera/).
2. (Optional) If you would like to see classifications from the **Control tab**, configure a [transform camera](../../../components/camera/transform/) with the following attributes :

   ```json
   {
     "pipeline": [
       {
         "type": "classifications",
         "attributes": {
           "confidence_threshold": 0.5,
           "classifier_name": "my_classifier"
         }
       }
     ],
     "source": "<camera-name>"
   }
   ```

3. After adding the components and their attributes, click **Save config**.
4. Navigate to the **Control** tab, click on your transform camera and toggle it on.
   The transform camera will now show classifications on the image.

   ![Model recognizes a star on camera feed](/services/model-on-camera.png)

5. The following code gets the robot’s vision service and then runs a classifier vision model on an image from the robot's camera `"cam1"`.

   {{% alert title="Tip" color="tip" %}}

Pass the name of the camera you configured in step 1.
Do not pass a transform camera that already has the "detections" or "classifications" transform applied to it.

    {{% /alert %}}

    {{< tabs >}}
    {{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "cam1"
# Grab camera from the robot
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

// Grab the camera from the robot
cameraName := "cam1" // make sure to use the same component name that you have in your robot configuration
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

### Existing images on your machine

If you would like to test your classifier with existing images, load the images and pass them to the classifier:

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

{{% alert title="Tip" color="tip" %}}
To see more code examples of how to use Viam's vision service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}
