---
title: "Configure an obstacles_distance Segmenter"
linkTitle: "obstacles_distance"
weight: 20
type: "docs"
description: "A segmenter that takes point clouds from a camera input and returns the average single closest point to the camera as a perceived obstacle."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
# SMEs: Bijan, Khari
---

_Changed in [RDK v0.2.36 and API v0.1.118](/appendix/changelog/#april-2023)_

`obstacles_distance` is a segmenter that takes point clouds from a camera input and returns the average single closest point to the camera as a perceived obstacle.
It is best for transient obstacle avoidance.

For example, if you have an ultrasonic distance sensor as an [`ultrasonic` camera](/components/camera/ultrasonic/), this model will query the sensor `"num_queries"` times, and then take the average point from those measurements and return that as an obstacle.

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/robots).
Click the **Services** subtab and click **Create service** in the lower-left corner.
Select the `Vision` type, then select the `Obstacles Distance` model.
Enter a name for your service and click **Create**.

In your vision service's configuration panel, fill in the **Attributes** field with the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "num_queries": 10
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
      "model": "obstacles_distance",
      "attributes": {
        "num_queries": 10
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
        "model": "obstacles_distance",
        "attributes": {
            "num_queries": 10
        }
    }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `obstacles_distance` segmenter:

<!-- prettier-ignore -->
| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `num_queries`| Optional  | How many times the model should call [`GetPointCloud()`](/components/camera/#getpointcloud) before taking the average of the measurements and returning the single closest point. Accepts an integer between `1` and `20`. <br> Default: `10`  |

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
