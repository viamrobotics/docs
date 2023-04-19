---
title: "Classification (or 2D image classification)"
linkTitle: "Classification"
weight: 20
type: "docs"
description: "Select an algorithm that outputs a class label and confidence score associated with a 2D image."
tags: ["vision", "computer vision", "CV", "services", "classification"]
# SMEs: Bijan, Khari
---

{{< readfile "/static/include/services/vision-breaking.md" >}}

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

* `class_name` (string): specifies the label of the found object.
* `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

## Classifier Types

The types of classifiers supported are:

* **tflite_classifier**: a machine learning classifier that returns a class label and confidence score according to the specified `tensorflow-lite` model file available on the robot’s hard drive.

### TFLite classifier

``` json {class="line-numbers linkable-line-numbers"}
{
    "register_models": [
        {
            "name": "<classifier_name>",
            "type": "tflite_classifier",
            "parameters": {
                "model_path" : "/path/to/model.tflite",
                "label_path": "/path/to/labels.txt",
                "num_threads": <integer>
            }
        }
    ]
}
```

The following parameters are available for a `"tflite_classifier"`.
For an example see [Configuration](#configuration).

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `model_path` | _Required_ | The path to the .tflite model file, as a string. |
| `label_path` | _Optional_ | The path to a .txt file that holds class labels for your TFLite model, as a string. The SDK expects this text file to contain an ordered listing of the class labels. Without this file, classes will read "1", "2", and so on. |
| `num_threads` | _Optional_ | An integer that defines how many CPU threads to use to run inference. Default: `1`. |

## Configuration

### Add the service and classifier

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the Vision Service to.
Select the **config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `Vision` as the **Type**.
2. Enter a name as the **Name**.
3. Click **Create Service**.

<img src="../../../tutorials/img/try-viam-color-detection/create-service.png" alt="The Create Service panel lists the type as vision and name as vision, with a Create Service button.">

In your Vision Service's panel, add a classifier into the **Attributes** field.
For example:

```json {class="line-numbers linkable-line-numbers"}
{
 "register_models": [
    {
        "name": "my_classifier",
        "type": "tflite_classifier",
        "parameters": {
            "model_path" : "/path/to/model.tflite",
            "label_path": "/path/to/labels.txt",
            "num_threads": 1
        }
    }
 ]
}
```

Click **Save config** and head to the **Components** tab.

{{%expand "You can also configure the entire Vision Service and classifier in raw JSON" %}}

To add a vision model to your robot, add the `name`, `type`, and `parameters` of the desired classifier to the `register_models` in the attributes field of the Vision Service config.
For example:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
    {
        "name": "vision1",
        "type": "vision",
        "attributes": {
          "register_models": [
            {
              "name": "my_color_detector",
              "type": "color_detector",
              "parameters": {
                "detect_color" : "#A3E2FF",
                "hue_tolerance_pct": 0.06,
                "segment_size_px": 100
              }
            },
            {
              "name": "my_classifier",
              "type": "tflite_classifier",
              "parameters": {
                "model_path" : "/path/to/model.tflite",
                "label_path": "/path/to/labels.txt",
                "num_threads": 1
              }
            },
            {
                "name": "my_segmenter",
                "type": "radius_clustering_segmenter",
                "parameters": {
                    "min_points_in_plane": 2,
                    "min_points_in_segment": 2,
                    "clustering_radius_mm": 3.0,
                    "mean_k_filtering": 0
                }
            }
          ]
        }
    }
]
```

{{% /expand%}}

### Add a camera component and a "transform" model

You cannot interact directly with the [Vision Service](/services/vision/).
To be able to interact with the Vision Service you must:

1. Configure a physical [camera component](../../../components/camera).
2. Configure a [transform camera](../../../components/camera/transform) to view output from the classifier overlaid on images from the physical camera.

After adding the component and its attributes, click **Save config**.

Wait for the robot to reload, and then go to the **control** tab to test the stream of detections.

## Code

The following code gets the robot’s Vision Service and then runs a classifier vision model on an image from the robot's camera `"camera_1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionServiceClient, VisModelConfig, VisModelType

robot = await connect()
# grab camera from the robot
cam1 = Camera.from_robot(robot, "cam1")
# grab Viam's vision service which has the classifier already registered
vision = VisionServiceClient.from_robot(robot)

print("Vision Resources:")
print(await vision.get_classifier_names())

# Apply the classifier configured as "my_classifier" to the image from your camera configured as "camera_1"
classifications = await vision.get_classifications_from_camera("camera_1", "my_classifier")

await robot.close()
```

To learn more about how to use classification, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"go.viam.com/rdk/config"
"go.viam.com/rdk/services/vision"
)

visService, err := vision.FirstFromRobot(robot)
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

clsNames, err := visService.ClassifierNames(context.Background(), nil)
if err != nil {
    logger.Fatalf("Could not list classifiers: %v", err)
}
logger.Info("Vision Resources:")
logger.Info(clsNames)

// Apply the color classifier to the image from your camera (configured as "camera_1")
classifications, err := visService.ClassificationsFromCamera(context.Background(), "camera_1", "my_classifier", nil)
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
