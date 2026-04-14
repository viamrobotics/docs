---
title: "Configure detections-to-segments"
linkTitle: "detections-to-segments"
weight: 30
type: "docs"
description: "Project 2D detections into 3D point cloud segments using a depth camera's intrinsic parameters."
service_description: "A segmenter that projects 2D detection bounding boxes into 3D point cloud objects."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
date: "2026-04-14"
aliases:
  - /operate/reference/services/vision/detector_3d_segmenter/
  - /services/vision/detector_3d_segmenter/
  - /ml/vision/detector_3d_segmenter/
  - /services/vision/segmentation/
  - /data-ai/services/vision/detector_3d_segmenter/
---

The `viam:vision:detections-to-segments` vision service wraps an existing 2D detector and projects its bounding boxes into 3D point cloud objects using a depth camera's intrinsic parameters. The label and pixels associated with each 2D detection become the label and point cloud of the corresponding 3D segment.

The camera you reference must provide both 2D images and point cloud data (for example, an Intel RealSense D400-series camera configured with the [RealSense module](https://github.com/viamrobotics/viam-camera-realsense)). A plain 2D camera will not work.

This model previously shipped with core RDK as `detector_3d_segmenter`. It now ships as a module at [`viam-modules/detections-to-segments`](https://github.com/viam-modules/detections-to-segments).

## Prerequisites

- A configured 2D detector vision service (for example, an [`mlmodel`](/reference/services/vision/mlmodel/) or [`color_detector`](/reference/services/vision/color_detector/)).
- A camera that returns both color images and a point cloud. See the RealSense and OAK-D modules in the [registry](https://app.viam.com/registry?type=Module).

## Install the module

1. In the Viam app, open your machine's **CONFIGURE** tab.
2. Click the **+** icon next to your machine part and select **Component or service**.
3. Select the `vision` type, then search for `detections-to-segments`.
4. Click **Add module** if prompted, then **Add component**.
5. Enter a name for the service and click **Create**.

The module downloads and starts automatically when you save the configuration.

## Configure

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<segmenter_name>",
    "api": "rdk:service:vision",
    "model": "viam:vision:detections-to-segments",
    "attributes": {
      "detector_name": "<detector_name>",
      "camera_name": "<camera-name>",
      "mean_k": 5,
      "sigma": 1.25,
      "confidence_threshold_pct": 0.5
    }
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "my_segmenter",
    "api": "rdk:service:vision",
    "model": "viam:vision:detections-to-segments",
    "attributes": {
      "detector_name": "person_detector",
      "camera_name": "realsense",
      "mean_k": 5,
      "sigma": 1.25,
      "confidence_threshold_pct": 0.5
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `detector_name` | string | **Required** | Name of a configured 2D detector vision service. Detections from this service are the input to the segmenter. |
| `camera_name` | string | **Required** | Name of the depth-capable camera. Must support point clouds (`supports_pcd` in `GetProperties`). |
| `mean_k` | int | **Required** | Point-cloud noise-filtering parameter (from the [PCL statistical outlier removal subroutine](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html)). Set to roughly 5 to 10 percent of the minimum expected segment size. Set to `0` or less to disable filtering. |
| `sigma` | float | **Required** | Point-cloud noise-filtering parameter. Typical values are `1.0` to `2.0`; `1.25` is a good default. Lower values produce less noisy objects at the risk of losing points near edges. |
| `confidence_threshold_pct` | float | Optional | Detections below this confidence are filtered out before 3D projection. Must be between `0.0` and `1.0`. <br> Default: `0.5` |

## Test your segmenter

The segmenter exposes its output through the vision service's [`GetObjectPointClouds`](/reference/apis/services/vision/#getobjectpointclouds) method.

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient

robot = await connect()
my_segmenter = VisionClient.from_robot(robot, "my_segmenter")

objects = await my_segmenter.get_object_point_clouds("realsense")
for o in objects:
    print(f"label: {o.geometries.geometries[0].label}")

await robot.close()
```

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/services/vision"
)

mySegmenter, err := vision.FromProvider(machine, "my_segmenter")
if err != nil {
  logger.Fatalf("cannot get vision service: %v", err)
}

segments, err := mySegmenter.GetObjectPointClouds(context.Background(), "realsense", nil)
if err != nil {
  logger.Fatalf("could not get segments: %v", err)
}
if len(segments) > 0 {
  logger.Info(segments[0])
}
```

## Troubleshoot

{{< expand "Service fails with \"camera does not support point clouds\"" >}}

The camera you specified does not return point cloud data. Confirm with `GetProperties` that `supports_pcd` is `true`. Point-cloud support usually requires a depth-capable camera module (RealSense, OAK-D, Orbbec, Azure Kinect) rather than a plain webcam.

{{< /expand >}}

{{< expand "Segments are very noisy" >}}

Lower `sigma` (try `1.0`) and raise `mean_k` to filter more aggressively. If segments still look wrong, verify the underlying detector is producing reasonable 2D bounding boxes by testing it independently in the Control tab.

{{< /expand >}}

{{< expand "No segments returned despite detections being visible" >}}

- `confidence_threshold_pct` may be filtering everything out. Lower it to `0.2` temporarily and verify segments appear.
- The depth alignment between the color and depth streams may be off. Most modules handle this automatically, but cameras without proper extrinsic calibration produce no points at the detection locations.

{{< /expand >}}

## Next steps

{{< cards >}}
{{% card link="/vision/measure-depth/" %}}
{{% card link="/reference/services/vision/mlmodel/" %}}
{{% card link="/reference/services/vision/color_detector/" %}}
{{< /cards >}}
