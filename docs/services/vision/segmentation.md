---
title: "Segmentation (or 3D object segmentation)"
linkTitle: "Segmentation"
weight: 20
type: "docs"
description: "Select an algorithm that creates point clouds of identified objects in a 3D image."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.2.36 and API v0.1.118](/appendix/release-notes/#25-april-2023)_

_3D Object Segmentation_ is the process of separating and returning a list of the identified "objects" from a 3D scene.
The "objects" are a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinates of the object.

Any camera that can return 3D pointclouds can use 3D object segmentation.

The types of segmenters supported are:

- [**radius_clustering_segmenter**](#configure-a-radius_clustering_segmenter): Radius clustering is a segmenter that identifies well separated objects above a flat plane.
- [**detector_3d_segmenter**](#configure-a-detector_3d_segmenter): This model takes 2D bounding boxes from an object detector and projects the pixels in the bounding box to points in 3D space.

## Configure a `radius_clustering_segmenter`

Radius clustering is a segmenter that identifies well separated objects above a flat plane.
It first identifies the biggest plane in the scene, eliminates all points below that plane, and begins clustering points above that plane based on how near they are to each other.
It is slower than other segmenters and can take up to 30 seconds to segment a scene.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the Vision Service to.
Select the **Config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select **Radius Clustering Segmenter** as the **Model**.
4. Click **Create Service**.

![Create Vision Service for radius_clustering_segmenter](/services/vision/radius_clustering_segmenter.png)

In your Vision Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
    "min_points_in_plane": <integer>,
    "min_points_in_segment": <integer>,
    "clustering_radius_mm": <number>,
    "mean_k_filtering": <integer>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the Vision Service object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
    {
    "name": "<segmenter_name>",
    "type": "vision",
    "model": "radius_clustering_segmenter"
    "attributes": {
        "min_points_in_plane": <integer>,
        "min_points_in_segment": <integer>,
        "clustering_radius_mm": <number>,
        "mean_k_filtering": <integer>
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
  "name": "rc_segmenter",
  "type": "vision",
  "model": "radius_clustering_segmenter"
  "attributes": {
    "min_points_in_plane": 1000,
    "min_points_in_segment": 50,
    "clustering_radius_mm": 3.2,
    "mean_k_filtering": 10
  }
}
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"radius_clustering_segmenter"`.

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `min_points_in_plane` | _Required_ | An integer that specifies how many points there must be in a flat surface for it to count as a plane. This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps. |
| `min_points_in_segment` | _Required_ | An integer that sets a minimum size to the returned objects, and filters out all other found objects below that size.
| `clustering_radius_mm` | _Required_ | A floating point number that specifies how far apart points can be (in units of mm) in order to be considered part of the same object. A small clustering radius will more likely split different parts of a large object into distinct objects. A large clustering radius may aggregate closely spaced objects into one object. 3.0 is a decent starting value. |
| `mean_k_filtering` | _Optional_ | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the number of min_points_in_segment. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |

Click **Save config** and head to the **Components** tab.

## Configure a `detector_3d_segmenter`

This model takes 2D bounding boxes from an [object detector](../detection/), and, using the intrinsic parameters of the chosen camera, projects the pixels in the bounding box to points in 3D space.
If the chosen camera is not equipped to do projections from 2D to 3D, then this vision model will fail.
The label and the pixels associated with the 2D detections become the label and point cloud associated with the 3D segmenter.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the Vision Service to.
Select the **Config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [Vision Service](/services/vision/):

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select **Detector to 3D Segmenter** as the **Model**.
4. Click **Create Service**.

![Create Vision Service for detector_3d_segmenter](/services/vision/detector_3d_segmenter.png)

In your Vision Service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
    "detector_name": "<detector_name>",
    "confidence_threshold_pct": <number>,
    "mean_k": <integer>,
    "sigma": <number>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the Vision Service object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
    {
        "name": "<segmenter_name>",
        "type": "vision",
        "model": "detector_3d_segmenter"
        "attributes": {
            "detector_name": "my_detector",
            "confidence_threshold_pct": 0.5,
            "mean_k": 50,
            "sigma": 2.0
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
        "name": "my_segmenter",
        "type": "vision",
        "model": "detector_3d_segmenter"
        "attributes": {
            "detector_name": "my_detector",
            "confidence_threshold_pct": 0.5,
            "mean_k": 50,
            "sigma": 2.0
        }
    }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"detector_3dsegmenter"`.

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `detector_name`| _Required_  | The name of a registered detector vision service. The segmenter vision service uses the detections from `"detector_name"` to create the 3D segments. |
| `confidence_threshold_pct` | _Optional_ | A number between 0 and 1 which represents a filter on object confidence scores. Detections that score below the threshold will be filtered out in the segmenter. The default is 0.5. |
| `mean_k` | _Required_ | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the minimum segment size. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |
| `sigma` | _Required_ | A floating point parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should usually be set between 1.0 and 2.0. 1.25 is usually a good default. If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower. |

Click **Save config** and head to the **Components** tab.

## Code

The following code gets the robot’s Vision Service and then runs a segmenter vision model on an image from the robot's camera `"camera_1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient, VisModelConfig, VisModelType

robot = await connect()
# Grab Viam's Vision Service for the segmenter
my_segmenter = VisionClient.from_robot(robot, "my_segmenter")

objects = await my_segmenter.get_object_point_clouds("cam1")

await robot.close()
```

To learn more about how to use segmentation, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"go.viam.com/rdk/config"
"go.viam.com/rdk/services/vision"
"go.viam.com/rdk/components/camera"
)

cameraName := "cam1" // make sure to use the same component name that you have in your robot configuration

visService, err := vision.from_robot(robot=robot, name='my_segmenter')
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// Apply the color classifier to the image from your camera (configured as "cam1")
segments, err := visService.GetObjectPointClouds(context.Background(), cameraName, nil)
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
