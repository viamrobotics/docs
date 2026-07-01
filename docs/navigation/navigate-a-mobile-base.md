---
linkTitle: "Navigate a mobile base"
title: "Navigate a mobile base to a goal"
weight: 40
layout: "docs"
type: "docs"
description: "Drive a configured mobile base to a GPS or SLAM-map waypoint with the motion service, using MoveOnGlobe or MoveOnMap."
---

The motion service can drive a mobile base to a destination and plan a collision-free path along the way.
For a base that knows its own pose, one call moves it to a waypoint: `MoveOnGlobe` for a geographic goal or `MoveOnMap` for a goal on a [SLAM](/navigation/slam-and-mapping/) map.

This page assembles the localization and motion inputs a base needs, issues the move, and maps common failures back to the missing input.

## Prerequisites

Before you start, configure the following on your machine:

- A [mobile base](/reference/components/base/) that you can already drive with velocity or position commands.
- A localization source that reports the base's pose:
  - A [movement sensor](/reference/components/movement-sensor/) that provides GPS position, for a geographic goal.
  - A [SLAM service](/navigation/slam-and-mapping/) that provides a map and pose, for a map goal.
- The [motion service](/reference/apis/services/motion/), which plans the path and issues drive commands to the base.

## Steps

### 1. Confirm the base has a localization source

The motion service moves the base relative to a known pose, so the base needs a source that reports where it is.
Confirm one of the following is configured and reporting:

- **Geographic goals:** a movement sensor returning a valid GPS fix.
- **Map goals:** a SLAM service returning a current pose on its map.

For the localization options and how each one supplies a pose, see [Localization](/navigation/localization/).

### 2. Set up the motion service with the base and its localization source

Add the [motion service](/reference/apis/services/motion/) to your machine.
The motion service reads the machine's [frame system](/motion-planning/frame-system/) to relate the base, its localization source, and any obstacles in a shared coordinate space.

Make sure your frame system places:

- The base as a movable component.
- The movement sensor or SLAM service on the base, so its pose reports describe the base.

With the frame system in place, the motion service has both the pose and the geometry it needs to plan.

### 3. Command the base to a goal

Call the motion service from an SDK.
Use `MoveOnGlobe` for a geographic destination or `MoveOnMap` for a destination on a SLAM map.

**Geographic goal with `MoveOnGlobe`:**

`MoveOnGlobe` takes a base, a destination as a `GeoPoint` (latitude and longitude), the name of the GPS movement sensor, and an optional list of geographic obstacles.

```python
from viam.services.motion import MotionClient
from viam.proto.common import GeoPoint, GeoGeometry

motion = MotionClient.from_robot(machine, "builtin")

await motion.move_on_globe(
    component_name=base_name,
    destination=GeoPoint(latitude=40.7, longitude=-73.98),
    movement_sensor_name=gps_name,
    obstacles=[],            # optional GeoGeometry obstacles
)
```

**Map goal with `MoveOnMap`:**

`MoveOnMap` takes a base, a destination `Pose` on the map, the name of the SLAM service, and an optional list of obstacles.

```python
from viam.services.motion import MotionClient
from viam.proto.common import Pose

motion = MotionClient.from_robot(machine, "builtin")

await motion.move_on_map(
    component_name=base_name,
    destination=Pose(x=1500, y=200, z=0),   # millimeters on the map
    slam_service_name=slam_name,
    obstacles=[],                            # optional obstacles
)
```

For full parameters, obstacle geometry types, and other SDKs, see the [motion service API](/reference/apis/services/motion/).

### 4. Verify the move

`MoveOnGlobe` and `MoveOnMap` run asynchronously: each returns an execution ID immediately and the base keeps driving in the background.
Track progress and completion with `GetPlan` and `ListPlanStatuses`, and stop an in-progress move with `StopPlan`.
To confirm the final pose, read the localization source directly:

- For a geographic goal, read the [movement sensor](/reference/components/movement-sensor/) position.
- For a map goal, read the base pose from the [SLAM service](/navigation/slam-and-mapping/).

## Troubleshooting

If a navigation attempt fails, match the symptom to the input it depends on:

| Symptom                                                                      | Missing input        | Fix                                                                                                                                  |
| ---------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Error that the base has no pose, or the plan starts from the wrong location. | Localization source. | Confirm the movement sensor has a GPS fix or the SLAM service reports a pose (Step 1).                                               |
| `MoveOnMap` reports no map, or the base leaves the mapped area.              | SLAM map.            | Confirm the SLAM service is running and the destination falls within its map (Step 1).                                               |
| Base stops early or refuses to plan a path near an object.                   | Obstacle source.     | Pass known obstacles to the `obstacles` argument, or add a [vision service](/reference/services/vision/) obstacle detector (Step 3). |
| Motion service cannot relate the base and its sensor.                        | Frame system.        | Confirm the frame system places the sensor on the base (Step 2).                                                                     |

## Next steps

- [Localization](/navigation/localization/): compare GPS and SLAM localization sources.
- [Motion service API](/reference/apis/services/motion/): full `MoveOnGlobe` and `MoveOnMap` parameters.
- [Base component](/reference/components/base/): tune the base that carries out the plan.
