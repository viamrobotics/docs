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

- [**Obstacles point cloud (`obstacles_pointcloud`)**](#configure-an-obstacles_pointcloud-segmenter): A segmenter that identifies well-separated objects above a flat plane.
- [**Object detector (`detector_3d_segmenter`)**](#configure-a-detector_3d_segmenter): This model takes 2D bounding boxes from an object detector and projects the pixels in the bounding box to points in 3D space.
- [**Obstacles depth (`obstacles_depth`)**](#configure-an-obstacles_depth-segmenter): A segmenter for depth cameras that returns a projection of a bounding box or boxes with a Pose as a vector from the depth camera lens to the center of the obstacle identified.

## Configure an `obstacles_pointcloud` segmenter

Radius clustering is a segmenter that identifies well separated objects above a flat plane.
It first identifies the biggest plane in the scene, eliminates all points below that plane, and begins clustering points above that plane based on how near they are to each other.
It is slower than other segmenters and can take up to 30 seconds to segment a scene.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the vision service to.
Select the **Config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [vision service](/services/vision/):

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select **Radius Clustering Segmenter** as the **Model**.
4. Click **Create Service**.

![Create vision service for obstacles_pointcloud](/services/vision/obstacles_pointcloud.png)

In your vision service's panel, fill in the **Attributes** field.

``` json {class="line-numbers linkable-line-numbers"}
{
    "min_points_in_plane": <integer>,
    "min_points_in_segment": <integer>,
    "max_dist_from_plane_mm": <number>,
        "ground_plane_normal_vec": {
            "x": <integer>,
            "y": <integer>,
            "z": <integer>
        },
    "ground_angle_tolerance_degs": <integer>,
    "clustering_radius": <integer>,
    "clustering_strictness": <integer>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
    {
    "name": "<segmenter_name>",
    "type": "vision",
    "model": "obstacles_pointcloud"
    "attributes": {
        "min_points_in_plane": <integer>,
        "min_points_in_segment": <integer>,
        "max_dist_from_plane_mm": <number>,
        "ground_plane_normal_vec": {
            "x": <integer>,
            "y": <integer>,
            "z": <integer>
        },
        "ground_angle_tolerance_degs": <integer>,
        "clustering_radius": <integer>,
        "clustering_strictness": <integer>
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
  "model": "obstacles_pointcloud",
  "attributes": {
    "min_points_in_plane": 1500,
    "min_points_in_segment": 250,
    "max_dist_from_plane_mm": 10.0,
    "ground_plane_normal_vec": {x: 0, y:0, z: 1},
    "ground_angle_tolerance_degs": 20.0,
    "clustering_radius": 5,
    "clustering_strictness": 3
  }
}
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"obstacles_pointcloud"`.

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `min_points_in_plane` | Optional | An integer that specifies how many points to put on the flat surface or ground plane when clustering. This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps. <br> Default: `500` </br> |
| `min_points_in_segment` | Optional | An integer that sets a minimum size to the returned objects, and filters out all other found objects below that size. |
| `clustering_radius` | Optional | An integer that specifies which neighboring points count as being "close enough" to be potentially put in the same cluster. This parameter determines how big the candidate clusters should be, or, how many points should be put on a flat surface. A small clustering radius is likely to split different parts of a large cluster into distinct objects. A large clustering radius is likely to aggregate closely spaced clusters into one object. <br> Default: `1` </br> |
| `clustering_strictness` | Optional | An integer that determines the probability threshold for sorting neighboring points into the same cluster, or how "easy" `viam-server` should determine it is to sort the points the robot's camera sees into this pointcloud. When the `clustering_radius` determines the size of the candidate clusters, then the clustering_strictness determines whether the candidates will count as a cluster. If `clustering_strictness` is set to a large value, many small clusters are likely to be made, rather than a few big clusters. The lower the number, the bigger your clusters will be. <br> Default: `5` </br> |
| `max_dist_from_plane_mm` | Optional | A float that determines how much area above and below an ideal ground plane should count as the plane for which points are removed. For fields with tall grass, this should be a high number. The default value is 100 mm. <br> Default: `100` </br> |
| `ground_plane_normal_vec` | Optional | A `(x,y,z)` vector that represents the normal vector of the ground plane. Different cameras have different coordinate systems. For example, a lidar's ground plane will point in the `+z` direction `(0, 0, 1)`. On the other hand, the intel realsense `+z` direction points out of the camera lens, and its ground plane is in the negative y direction `(0, -1, 0)`. <br> Default: `(0, 0, 1)` </br> |
| `ground_angle_tolerance_degs` | Optional | An integer that determines how strictly the found ground plane should match the `ground_plane_normal_vec`. For example, even if the ideal ground plane is purely flat, a rover may encounter slopes and hills. The algorithm should find a ground plane even if the found plane is at a slant, up to a certain point. <br> Default: `30` </br> |

Click **Save config** and proceed to [test your segmenter](#test-your-segmenter).

## Configure a `detector_3d_segmenter`

This model takes 2D bounding boxes from an [object detector](../detection/), and, using the intrinsic parameters of the chosen camera, projects the pixels in the bounding box to points in 3D space.
If the chosen camera is not equipped to do projections from 2D to 3D, then this vision model will fail.
The label and the pixels associated with the 2D detections become the label and point cloud associated with the 3D segmenter.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the vision service to.
Select the **Config** tab, and click on **Services**.

Scroll to the **Create Service** section.
To create a [vision service](/services/vision/):

1. Select `vision` as the **Type**.
2. Enter a name as the **Name**.
3. Select **Detector to 3D Segmenter** as the **Model**.
4. Click **Create Service**.

![Create vision service for detector_3d_segmenter](/services/vision/detector_3d_segmenter.png)

In your vision service's panel, fill in the **Attributes** field.

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

Add the vision service object to the services array in your raw JSON configuration:

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

The following parameters are available for a `detector_3d_segmenter`.

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `detector_name`| _Required_  | The name of a registered detector vision service. The segmenter vision service uses the detections from `"detector_name"` to create the 3D segments. |
| `confidence_threshold_pct` | _Optional_ | A number between 0 and 1 which represents a filter on object confidence scores. Detections that score below the threshold will be filtered out in the segmenter. The default is 0.5. |
| `mean_k` | _Required_ | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the minimum segment size. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |
| `sigma` | _Required_ | A floating point parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should usually be set between 1.0 and 2.0. 1.25 is usually a good default. If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower. |

Click **Save config** and proceed to [test your segmenter](#test-your-segmenter).

## Configure an `obstacles_depth` segmenter

This segmenter model is for depth cameras, and is best for motion planning with transient obstacles.
If you have [configured the frame system](/services/frame-system/#configuration) for the components of your robot, then you can implement this model to identify well separated objects above a flat plane.

To configure an `obstacles_depth` segmenter, first decide if you want to use the segmenter with or without intrinsic parameters.

This is determined by the value of the configuration attribute `with_geometries`:

- `true`: this segmenter will return point clouds within the `GeometryInFrame` object it captures.
- `false`: this segmenter will return a single point within the `GeometryInFrame` object it captures.

If `true`, start configuring your segmenter by following [these instructions](/services/frame-system/#configuration) to configure the relative spatial orientation of the components of your robot within Viam's [frame system service](/services/frame-system/).

After doing this, your camera will populate its own `Properties` with the intrinsic parameters of the geometric configuration.
You can then get those parameters from your camera through the [camera API](/components/camera/#getproperties).

Then, configure an `obstacles_depth` segmenter:

{{< tabs >}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
    {
    "name": "<segmenter_name>",
    "type": "vision",
    "model": "obstacles_pointcloud"
    "attributes": {
        "h_min_m": <number>,
        "h_max_m": <number>,
        "theta_max_deg": <number>,
        "return_pcds": <boolean>,
        "with_geometries": <boolean>,
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
    "model": "obstacles_pointcloud",
    "attributes": {
        "h_min_m": 0.0,
        "h_max_m": 1.0,
        "theta_max_deg": 45,
        "return_pcds": "false",
        "with_geometries": "false"
    }
}
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"obstacles_depth"` segmenter:

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `return_pcds` | Required | If you would like point clouds or a single point returned within their `GeometryInFrame` object. `true` indicates wanting point clouds. <br> Example: `false` </br> |
| `h_min_m` | Optional | The vertical height (in m) such that any obstacle strictly lower than would not be an obstacle. <br> Default: `0.0` </br> |
| `h_max_m` | Optional | The vertical height (in m) such that any obstacle strictly higher than would not be an obstacle. <br> Default: `1.0` </br> |
| `theta_max_deg` | Optional | The largest slope (in degrees) acceptable for non-obstacle surface ramps. <br> Default: `45` </br> |
| `with_geometries` | Optional | If you have configured the geometries, or, spatial orientation of the components of your robot, within the frame system. `true` is necessary to `return_pcds` properly, if `"return_pcds": "true"`  <br> Example: `false` </br> |

Click **Save config** and proceed to [test your segmenter](#test-your-segmenter).

## Test your segmenter

The following code uses the [`GetObjectPointClouds`](/services/vision/#getobjectpointclouds) method to run a segmenter vision model on an image from the robot's camera `"cam1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient, VisModelConfig, VisModelType

robot = await connect()

# Grab Viam's vision service for the segmenter
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

cameraName := "cam1" // Use the same component name that you have in your robot configuration

// Get the vision service you configured with name "my_segmenter" from the robot
mySegmenter, err := vision.from_robot(robot, "my_segmenter")
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get segments
segments, err := mySegmenter.ObjectPointClouds(context.Background(), cameraName, nil)
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
To see more code examples of how to use Viam's vision service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}
