---
title: "Classification (or 2D image classification)"
linkTitle: "Classification"
weight: 20
type: "docs"
description: "Select an algorithm that outputs a class label and confidence score associated with a 2D image."
tags: ["vision", "computer vision", "CV", "services", "classification"]
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.3.0 and API v0.2.0](/appendix/release-notes/#2-may-2023)_

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

* `class_name` (string): specifies the label of the found object.
* `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

The types of classifiers supported are:

* **tflite_cpu**: a machine learning classifier that returns a class label and confidence score according to the specified `tensorflow-lite` model file available on the robot’s hard drive.

## Configure a `tflite_cpu` classifier

### Create the ML Model Service for the classifier

Navigate to the [robot page on the Viam app](https://app.viam.com/robots), then create an ML Model Service for the classifier model:

{{< tabs >}}
{{% tab name="Builder" %}}
Click on the robot you wish to add the classifier to.
Select the **config** tab, and click on **Services**.

Scroll to the **Create Service** section:

1. Select `mlmodel` as the **Type**.
2. Enter a name as the **Name**.
3. Select `tflite_cpu` as the **Model**.
4. Click **Create Service**.

In your ML Model Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
    "model_path": "${packages.<model-name>}/<model-name>.tflite",
    "label_path": "${packages.<model-name>}/labels.txt",
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
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.<model-name>}/<model-name>.tflite",
      "label_path": "${packages.<model-name>}/labels.txt",
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
    "name": "fruit_classifier",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.<model-name>}/<model-name>.tflite",
      "label_path": "${packages.<model-name>}/labels.txt",
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

### Create the Vision Service that uses the classifier

Create another service:

{{< tabs >}}
{{% tab name="Builder" %}}

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select `mlmodel` as the **Model**.
4. Click **Create Service**.

In your Vision Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
  "mlmodel_name": "<classifier_name>"
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

Click **Save config** and head to the **Components** tab.

## Add a camera component and a "transform" model

You cannot interact directly with the [Vision Service](/services/vision/).
To be able to interact with the Vision Service you must:

1. Configure a physical [camera component](../../../components/camera).
2. Configure a [transform camera](../../../components/camera/transform) with the following attributes to view output from the classifier overlaid on images from the physical camera:

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

    After adding the component and its attributes, click **Save config**.
    Wait for the robot to reload, and then go to the **control** tab to test the stream of detections.

    ![Model recognizes a star on camera feed](../../img/model-on-camera.png)

## Code

The following code gets the robot’s Vision Service and then runs a classifier vision model on an image from the robot's camera `"cam1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionServiceClient, VisModelConfig, VisModelType

robot = await connect()
# grab camera from the robot
cam1 = Camera.from_robot(robot, "cam1")
# grab Viam's vision service for the classifier
my_classifier = VisionServiceClient.from_robot(robot, "my_classifier")

img = await cam1.get_image()
classifications = await my_classifier.get_classifications(img)

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

// grab the camera from the robot
cameraName := "cam1" // make sure to use the same component name that you have in your robot configuration
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

visService, err := vision.from_robot(robot=robot, name='my_classifier')
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// gets the stream from a camera
camStream, err := myCam.Stream(context.Background())

// gets an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()

// Apply the color classifier to the image from your camera (configured as "cam1")
classifications, err := visService.GetClassifications(context.Background(), img)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(classifications) > 0 {
    logger.Info(classifications[0])
}
```

To learn more about how to use classification, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
To see more code examples of how to use Viam's Vision Service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}
