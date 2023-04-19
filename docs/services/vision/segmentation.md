---
title: "Segmentation (or 3D object segmentation)"
linkTitle: "Segmentation"
weight: 20
type: "docs"
description: "Select an algorithm that creates point clouds of identified objects in a 3D image."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
# SMEs: Bijan, Khari
---

{{< readfile "/static/include/services/vision-breaking.md" >}}

_3D Object Segmentation_ is the process of separating and returning a list of the identified "objects" from a 3D scene.
The "objects" are a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinates of the object.

Any camera that can return 3D pointclouds can use 3D object segmentation.

## Segmenter Types

The types of segmenters supported are:

- [**radius_clustering_segmenter**](#radius_clustering_segmenter): Radius clustering is a segmenter that identifies well separated objects above a flat plane.
- [**detector_segmenter**](#detector_segmenter): Object segmenters are automatically created from detectors in the Vision Service.

### `radius_clustering_segmenter`

Radius clustering is a segmenter that identifies well separated objects above a flat plane.
It first identifies the biggest plane in the scene, eliminates all points below that plane, and begins clustering points above that plane based on how near they are to each other.
It is slower than other segmenters and can take up to 30 seconds to segment a scene.

``` json {class="line-numbers linkable-line-numbers"}
{
    "register_models": [
        {
            "name": "<segmenter_name>",
            "type": "radius_clustering_segmenter",
            "parameters": {
                "min_points_in_plane": <integer>,
                "min_points_in_segment": <integer>,
                "clustering_radius_mm": <number>,
                "mean_k_filtering": <integer>
            }
        }
    ]
}
```

The following parameters are available for a `"radius_clustering_segmenter"`.
For an example see [Configuration](#configuration).

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `min_points_in_plane` | _Required_ | An integer that specifies how many points there must be in a flat surface for it to count as a plane. This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps. |
| `min_points_in_segment` | _Required_ | An integer that sets a minimum size to the returned objects, and filters out all other found objects below that size.
| `clustering_radius_mm` | _Required_ | A floating point number that specifies how far apart points can be (in units of mm) in order to be considered part of the same object. A small clustering radius will more likely split different parts of a large object into distinct objects. A large clustering radius may aggregate closely spaced objects into one object. 3.0 is a decent starting value. |
| `mean_k_filtering` | _Optional_ | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the number of min_points_in_segment. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |

### `detector_segmenter`

Object segmenters are automatically created from [detectors](../detection) in the Vision Service.
Any registered detector, for example `detector1`, defined in the `register_models` field or added later to the Vision Service becomes a segmenter with `_segmenter` appended to its name, for example `detector1_segmenter`.
It begins by finding the 2D bounding boxes, and then returns the list of 3D point cloud projection of the pixels within those bounding boxes.

``` json {class="line-numbers linkable-line-numbers"}
{
    "register_models": [
        {
            "name": "<segmenter_name>",
            "type": "detector_segmenter",
            "parameters": {
                "detector_name": "<detector_name>",
                "confidence_threshold_pct": <number>,
                "mean_k": <integer>,
                "sigma": <number>
            }
        }
    ]
}
```

The following parameters are available for a `"detector_segmenter"`.
For an example see [Configuration](#configuration).

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `detector_name`| _Required_  | The name of the detector already registered in the Vision Service that will be turned into a segmenter. |
| `confidence_threshold_pct` | _Optional_ | A number between 0 and 1 which represents a filter on object confidence scores. Detections that score below the threshold will be filtered out in the segmenter. The default is 0.5. |
| `mean_k` | _Required_ | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the minimum segment size. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |
| `sigma` | _Required_ | A floating point parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should usually be set between 1.0 and 2.0. 1.25 is usually a good default. If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower. |

## Configuration

### Add the service and segmenter

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the Vision Service to.
Select the **config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `Vision` as the **Type**.
2. Enter a name as the **Name**.
3. Click **Create Service**.

<img src="../../../tutorials/img/try-viam-color-detection/create-service.png" alt="The Create Service panel lists the type as vision and name as vision, with a Create Service button.">

In your Vision Service's panel, add a segmenter into the **Attributes** field.
For example:

```json {class="line-numbers linkable-line-numbers"}
{
 "register_models": [
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
```

Click **Save config** and head to the **Components** tab.

{{%expand "You can also configure the entire Vision Service and segmenter in raw JSON" %}}

To add a vision model to your robot, add the `name`, `type`, and `parameters` of the desired segmenter to the `register_models` in the attributes field of the Vision Service config.
For example:

```json
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

## Code

The following code gets the robot’s Vision Service and then runs a segmenter vision model on an image from the robot's camera `"camera_1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionServiceClient, VisModelConfig, VisModelType

robot = await connect()
# grab camera from the robot
cam1 = Camera.from_robot(robot, "cam1")
# grab Viam's vision service which has the segmenter already registered
vision = VisionServiceClient.from_robot(robot)

print("Vision Resources:")
print(await vision.get_segmenter_names())

# Apply the segmenter configured as my_segmenter to the image from your camera configured as "camera_1"
segments = await vision.get_object_point_clouds("camera_1", "my_segmenter")

await robot.close()
```

To learn more about how to use segmentation, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

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

segNames, err := visService.SegmenterNames(context.Background(), nil)
if err != nil {
    logger.Fatalf("Could not list detectors: %v", err)
}
logger.Info("Vision Resources:")
logger.Info(segNames)

// Apply the color segmenter to the image from your camera (configured as "camera_1")
segments, err := visService.GetObjectPointClouds(context.Background(), "camera_1", "my_segmenter", nil)
if err != nil {
    logger.Fatalf("Could not get segments: %v", err)
}
if len(segments) > 0 {
    logger.Info(segments[0])
}
```

To learn more about how to use segmentation, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
To see more code examples of how to use Viam's Vision Service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}
