---
linkTitle: "MotionConfiguration"
title: "MotionConfiguration reference"
weight: 23
layout: "docs"
type: "docs"
description: "Per-call motion parameters passed to MoveOnGlobe and MoveOnMap: speed, deviation, polling, and obstacle detectors."
---

`MotionConfiguration` is an optional message you pass to the motion
service's [`MoveOnGlobe`](/motion-planning/reference/api/#moveonglobe)
and [`MoveOnMap`](/motion-planning/reference/api/#moveonmap) calls to
override defaults for a single execution. It is not used with `Move`,
which is synchronous and does not expose per-call motion parameters.

The navigation service uses `MoveOnGlobe` internally and builds a `MotionConfiguration` from its own attributes; see [Navigation service correspondence](#navigation-service-correspondence) below for the mapping.

## Fields

| Field                           | Type                 | Default                                | Description                                                                                                                                           |
| ------------------------------- | -------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `obstacle_detectors`            | `[]ObstacleDetector` | empty                                  | Pairs of `vision_service` and `camera` that the motion service polls for transient obstacles during execution.                                        |
| `position_polling_frequency_hz` | `double` (optional)  | unset (implementation default)         | How often the service polls the movement sensor (or SLAM service) for the current position. Higher values detect deviation sooner but use more CPU.   |
| `obstacle_polling_frequency_hz` | `double` (optional)  | unset (implementation default)         | How often each obstacle detector is queried for transient obstacles. Higher values detect obstacles sooner but use more CPU and camera bandwidth.     |
| `plan_deviation_m`              | `double` (optional)  | 2.6 m (MoveOnGlobe), 1.0 m (MoveOnMap) | Distance in meters the robot may deviate from the current plan before the service triggers a replan. Set larger than your movement sensor's accuracy. |
| `linear_m_per_sec`              | `double` (optional)  | 0.3 m/s                                | Target linear velocity when moving in a straight line.                                                                                                |
| `angular_degs_per_sec`          | `double` (optional)  | 60 deg/s                               | Target angular velocity when turning.                                                                                                                 |

## ObstacleDetector

Each entry pairs a vision service with a camera:

| Field            | Type     | Description                                                 |
| ---------------- | -------- | ----------------------------------------------------------- |
| `vision_service` | `string` | Name of the vision service that reports detected obstacles. |
| `camera`         | `string` | Name of the camera whose images feed that vision service.   |

The motion service queries each detector at
`obstacle_polling_frequency_hz` and feeds the reported geometry to the
planner for the remainder of the current execution.

## Units

`plan_deviation_m` is meters at the API boundary. The motion service stores the value internally as millimeters, and the Go SDK's `MotionConfiguration` struct exposes that millimeter form as `PlanDeviationMM`.

## Usage

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.service.motion import MotionConfiguration, ObstacleDetector
from viam.proto.common import GeoPoint

configuration = MotionConfiguration(
    obstacle_detectors=[
        ObstacleDetector(vision_service="obstacles", camera="front-cam"),
    ],
    position_polling_frequency_hz=2.0,
    obstacle_polling_frequency_hz=2.0,
    plan_deviation_m=5.0,
    linear_m_per_sec=0.5,
    angular_degs_per_sec=30.0,
)

execution_id = await motion_service.move_on_globe(
    component_name="my-base",
    destination=GeoPoint(latitude=40.6640, longitude=-73.9387),
    movement_sensor_name="my-gps",
    configuration=configuration,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    geo "github.com/kellydunn/golang-geo"
    "go.viam.com/rdk/services/motion"
)

positionHz := 2.0
obstacleHz := 2.0
configuration := &motion.MotionConfiguration{
    ObstacleDetectors: []motion.ObstacleDetectorName{
        {VisionServiceName: "obstacles", CameraName: "front-cam"},
    },
    PositionPollingFreqHz: &positionHz,
    ObstaclePollingFreqHz: &obstacleHz,
    PlanDeviationMM:       5000, // 5 meters, stored as mm internally
    LinearMPerSec:         0.5,
    AngularDegsPerSec:     30.0,
}

executionID, err := motionService.MoveOnGlobe(ctx, motion.MoveOnGlobeReq{
    ComponentName:      "my-base",
    Destination:        geo.NewPoint(40.6640, -73.9387),
    MovementSensorName: "my-gps",
    MotionCfg:          configuration,
})
```

{{% /tab %}}
{{< /tabs >}}

## Navigation service correspondence

When you configure the navigation service, it builds a `MotionConfiguration` from its attributes on every internal `MoveOnGlobe` call. The attributes map to `MotionConfiguration` fields as follows:

| Navigation service attribute    | MotionConfiguration field       |
| ------------------------------- | ------------------------------- |
| `meters_per_sec`                | `linear_m_per_sec`              |
| `degs_per_sec`                  | `angular_degs_per_sec`          |
| `plan_deviation_m`              | `plan_deviation_m`              |
| `position_polling_frequency_hz` | `position_polling_frequency_hz` |
| `obstacle_polling_frequency_hz` | `obstacle_polling_frequency_hz` |
| `obstacle_detectors[]`          | `obstacle_detectors[]`          |

The navigation service also has a `replan_cost_factor` attribute with
no `MotionConfiguration` equivalent; it is a navigation-service-only
tuning knob.

## What's next

- [Motion service API](/motion-planning/reference/api/): the methods
  that accept `MotionConfiguration`.
- [Navigation service configuration](/navigation/reference/navigation-service/):
  service-level defaults that become the `MotionConfiguration` for
  navigation-driven moves.
- [Tune navigation](/navigation/how-to/tune-navigation/): guidance for
  choosing specific values for your environment.
