---
title: "Configure a detector_3d_segmenter"
linkTitle: "detector_3d_segmenter"
weight: 20
type: "docs"
description: "This model takes 2D bounding boxes from an object detector and projects the pixels in the bounding box to points in 3D space."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
aliases:
  - "/services/vision/segmentation/"
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.2.36 and API v0.1.118](/appendix/changelog/#vision-service)_

The `detector_3d_segmenter` vision service model takes 2D bounding boxes from an [object detector](../#detections), and, using the intrinsic parameters of the chosen camera, projects the pixels in the bounding box to points in 3D space.
If the chosen camera is not equipped to do projections from 2D to 3D, then this vision model will fail.
The label and the pixels associated with the 2D detections become the label and point cloud associated with the 3D segmenter.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Select the `vision` type, then select the `detector to 3D segmenter` model.
Enter a name or use the suggested name for your service and click **Create**.

In your vision service's panel, fill in the attributes field.

```json {class="line-numbers linkable-line-numbers"}
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

```json {class="line-numbers linkable-line-numbers"}
"services": [
    {
        "name": "<segmenter_name>",
        "type": "vision",
        "namespace": "rdk",
        "model": "detector_3d_segmenter",
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
        "namespace": "rdk",
        "model": "detector_3d_segmenter",
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

<!-- prettier-ignore -->
| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `detector_name`| **Required**  | The name of a registered detector vision service. The segmenter vision service uses the detections from `"detector_name"` to create the 3D segments. |
| `confidence_threshold_pct` | Optional | A number between 0 and 1 which represents a filter on object confidence scores. Detections that score below the threshold will be filtered out in the segmenter. The default is 0.5. |
| `mean_k` | **Required** | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the minimum segment size. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |
| `sigma` | **Required** | A floating point parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should usually be set between 1.0 and 2.0. 1.25 is usually a good default. If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower. |

Click the **Save** button in the top right corner of the page and proceed to [test your segmenter](#test-your-segmenter).

## Test your segmenter

The following code uses the [`GetObjectPointClouds`](/services/vision/#getobjectpointclouds) method to run a segmenter vision model on an image from the machine's camera `"cam1"`:

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
