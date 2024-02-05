---
title: "obstacles_pointcloud"
linkTitle: "obstacles_pointcloud"
weight: 20
type: "docs"
description: "A segmenter that identifies well-separated objects above a flat plane."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.2.36 and API v0.1.118](/appendix/changelog/#april-2023)_

`obstacles_pointcloud` is a segmenter that identifies well separated objects above a flat plane.
It first identifies the biggest plane in the scene, eliminates that plane, and clusters the remaining points into objects.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Select the `Vision` type, then select the `Radius Clustering Segmenter` model.
Enter a name for your service and click **Create**.

In your vision service's panel, fill in the **Attributes** field.

```json {class="line-numbers linkable-line-numbers"}
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

```json {class="line-numbers linkable-line-numbers"}
"services": [
    {
    "name": "<segmenter_name>",
    "type": "vision",
    "namespace": "rdk",
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
  "namespace": "rdk",
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

<!-- prettier-ignore -->
| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `min_points_in_plane` | Optional | An integer that specifies how many points to put on the flat surface or ground plane when clustering. This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps. <br> Default: `500` </br> |
| `min_points_in_segment` | Optional | An integer that sets a minimum size to the returned objects, and filters out all other found objects below that size. <br> Default: `10` </br> |
| `clustering_radius` | Optional | An integer that specifies which neighboring points count as being "close enough" to be potentially put in the same cluster. This parameter determines how big the candidate clusters should be, or, how many points should be put on a flat surface. A small clustering radius is likely to split different parts of a large cluster into distinct objects. A large clustering radius is likely to aggregate closely spaced clusters into one object. <br> Default: `1` </br> |
| `clustering_strictness` | Optional | An integer that determines the probability threshold for sorting neighboring points into the same cluster, or how "easy" `viam-server` should determine it is to sort the points the machine's's camera sees into this pointcloud. When the `clustering_radius` determines the size of the candidate clusters, then the clustering_strictness determines whether the candidates will count as a cluster. If `clustering_strictness` is set to a large value, many small clusters are likely to be made, rather than a few big clusters. The lower the number, the bigger your clusters will be. <br> Default: `5` </br> |
| `max_dist_from_plane_mm` | Optional | A float that determines how much area above and below an ideal ground plane should count as the plane for which points are removed. For fields with tall grass, this should be a high number. The default value is 100 mm. <br> Default: `100` </br> |
| `ground_plane_normal_vec` | Optional | A `(x,y,z)` vector that represents the normal vector of the ground plane. Different cameras have different coordinate systems. For example, a lidar's ground plane will point in the `+z` direction `(0, 0, 1)`. On the other hand, the intel realsense `+z` direction points out of the camera lens, and its ground plane is in the negative y direction `(0, -1, 0)`. <br> Default: `(0, 0, 1)` </br> |
| `ground_angle_tolerance_degs` | Optional | An integer that determines how strictly the found ground plane should match the `ground_plane_normal_vec`. For example, even if the ideal ground plane is purely flat, a rover may encounter slopes and hills. The algorithm should find a ground plane even if the found plane is at a slant, up to a certain point. <br> Default: `30` </br> |

Press **Command+S** to save your config and proceed to [test your segmenter](#test-your-segmenter).

## Test your segmenter

The following code uses the [`GetObjectPointClouds`](/ml/vision/#getobjectpointclouds) method to run a segmenter vision model on an image from the machine's camera `"cam1"`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient

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

cameraName := "cam1" // Use the same component name that you have in your machine configuration

// Get the vision service you configured with name "my_segmenter" from the machine
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
