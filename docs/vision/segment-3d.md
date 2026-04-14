---
linkTitle: "Segment 3D objects"
title: "Segment 3D objects from point clouds"
weight: 45
layout: "docs"
type: "docs"
description: "Use the vision service's GetObjectPointClouds method to find and label objects in 3D space, combining a 2D detector with a depth camera's point cloud."
date: "2026-04-14"
---

When a robot needs to know where objects are in 3D space (not just where they appear in a 2D image), use 3D object segmentation. The vision service returns a list of point cloud objects, one per detected object, each with a label, a 3D bounding box, and a center coordinate. Typical uses are guiding an arm to pick up an object, feeding obstacle positions into a navigation stack, or measuring the size of a physical item.

3D segmentation requires more than a camera and an ML model. You need a depth-capable camera and a segmenter that knows how to project 2D detections into 3D.

## How 3D segmentation works in Viam

The pipeline has three resources:

```text
  Depth camera ──► 2D detector ──► 3D segmenter ──► GetObjectPointClouds
   (images +         (vision           (vision          (your code)
    point cloud)      service)          service)
```

1. A **depth camera** returns both a color image and a point cloud from the same frame.
2. A **2D detector** (an `mlmodel` or `color_detector` vision service) finds bounding boxes in the color image.
3. A **3D segmenter** (the `viam:vision:detections-to-segments` module) takes the 2D bounding boxes and, using the camera's intrinsic parameters, projects the pixels inside each box into 3D space. Each 2D detection produces a corresponding 3D object that keeps the original label and carries the projected pixels as its point cloud.

The segmenter returns results through the vision service's [`GetObjectPointClouds`](/reference/apis/services/vision/#getobjectpointclouds) method.

## 1. Configure a depth camera

You need a camera that returns both images and point clouds. Common choices:

- Intel RealSense D400 series (through the [RealSense module](https://github.com/viamrobotics/viam-camera-realsense))
- Luxonis OAK-D series (through the [OAK camera module](https://github.com/viamrobotics/viam-camera-oak))
- Orbbec cameras (through the [Orbbec module](https://github.com/viam-modules/orbbec))
- The `fake` camera for testing (returns synthetic but structurally correct point clouds)

Verify the camera reports `supports_pcd: true` by calling [`GetProperties`](/reference/apis/components/camera/#getproperties) on it. If `supports_pcd` is `false`, the segmenter will fail at runtime.

## 2. Configure a 2D detector

The segmenter reuses an existing 2D detection vision service. Configure one if you do not have it already:

- For ML-based detection, follow [Deploy an ML model from the registry](/vision/deploy-from-registry/) or [Deploy a custom ML model](/vision/deploy-custom-model/).
- For color-based detection, see [Detect by color](/vision/detect-by-color/).

Name the detector something memorable, for example `person_detector` or `red_block_detector`. You will reference this name from the segmenter config.

## 3. Add the detections-to-segments module

1. Open the **CONFIGURE** tab in the Viam app.
2. Click the **+** icon and select **Configuration block**.
3. In the search field, type `detections-to-segments` and select the matching result.
4. Give the service a name (for example, `my_segmenter`) and click **Add component**. The module is installed automatically.

The module downloads and starts when you save the configuration.

## 4. Configure the segmenter

Set the segmenter's attributes:

```json
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
```

- `detector_name`: the 2D detector vision service name from step 2.
- `camera_name`: the depth camera name from step 1.
- `mean_k` and `sigma`: point-cloud noise filter parameters. Start with `5` and `1.25`. Lower `sigma` gives cleaner objects at the cost of losing edge points. See the [attributes reference](/reference/services/vision/detections-to-segments/).
- `confidence_threshold_pct`: detections below this are discarded before 3D projection.

Save the configuration.

## 5. Call GetObjectPointClouds from code

The segmenter's results come back through the standard vision service API.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def main():
    machine = await connect()
    segmenter = VisionClient.from_robot(machine, "my_segmenter")

    objects = await segmenter.get_object_point_clouds("realsense")

    for o in objects:
        geom = o.geometries.geometries[0]
        center = geom.center
        box = geom.box
        label = geom.label
        print(
            f"{label}: center at ({center.x:.1f}, {center.y:.1f}, {center.z:.1f}) mm, "
            f"box {box.dims_mm.x:.0f}x{box.dims_mm.y:.0f}x{box.dims_mm.z:.0f} mm"
        )

    await machine.close()


if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
  "context"

  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/services/vision"
  "go.viam.com/utils/rpc"
)

func main() {
  ctx := context.Background()
  logger := logging.NewLogger("segmenter")

  machine, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
      "YOUR-API-KEY-ID",
      rpc.Credentials{
        Type:    rpc.CredentialsTypeAPIKey,
        Payload: "YOUR-API-KEY",
      })),
  )
  if err != nil {
    logger.Fatal(err)
  }
  defer machine.Close(ctx)

  segmenter, err := vision.FromProvider(machine, "my_segmenter")
  if err != nil {
    logger.Fatal(err)
  }

  objects, err := segmenter.GetObjectPointClouds(ctx, "realsense", nil)
  if err != nil {
    logger.Fatal(err)
  }

  for _, o := range objects {
    logger.Infof("object: %d points, center %v", o.Size(), o.Geometry.Pose().Point())
  }
}
```

{{% /tab %}}
{{< /tabs >}}

Each returned object contains the raw point cloud bytes plus a `GeometriesInFrame` structure with the label, 3D bounding box dimensions, center coordinate, and the frame the coordinates are in (typically the camera frame).

## 6. Use object coordinates with a robot

The coordinates in each `GetObjectPointClouds` result are in the camera's frame. To use them with an arm, gripper, or navigation stack, transform them into a shared frame through Viam's [frame system](/motion-planning/frame-system/).

A typical pattern:

1. Compute the object center in the camera frame (from the returned `center` field).
2. Use the motion service's [`TransformPose`](/reference/apis/services/motion/) method to transform that pose from the camera frame to the arm's base frame.
3. Plan a motion to the transformed pose using the motion service.

See the [motion planning section](/motion-planning/) for the end-to-end walkthrough. This vision guide focuses on producing the 3D detections; what happens next is usually motion-service territory.

## Troubleshoot

{{< expand "GetObjectPointClouds returns an error about unsupported operation" >}}

The vision service you configured does not implement the 3D segmenter role. Confirm with [`GetProperties`](/reference/apis/services/vision/#getproperties) that `object_point_clouds_supported` is `true`. If not, check that your service's model is `viam:vision:detections-to-segments` (not `mlmodel` or `color_detector`).

{{< /expand >}}

{{< expand "Segmenter starts but returns no objects" >}}

- Verify the underlying detector is producing 2D detections by testing it independently in the Control tab.
- Lower `confidence_threshold_pct` to confirm low-confidence detections can pass through.
- Confirm the camera is returning point cloud data. If `GetPointCloud` on the camera returns empty or fails, the segmenter cannot work.

{{< /expand >}}

{{< expand "Object shapes look very noisy or hollow" >}}

Increase `mean_k` (try `10` to `20`) and lower `sigma` (try `1.0`) to filter outliers more aggressively. If objects still look wrong, the detector's 2D bounding boxes may be poorly aligned with the depth data. Check that the color and depth streams are spatially calibrated.

{{< /expand >}}

## Next steps

- [detections-to-segments reference](/reference/services/vision/detections-to-segments/): every attribute of the segmenter
- [Measure depth](/vision/measure-depth/): simpler depth queries when you do not need 3D segmentation
- [Motion planning](/motion-planning/): move a robot to a detected 3D object
