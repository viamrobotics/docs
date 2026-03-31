---
linkTitle: "Avoid obstacles"
title: "Avoid obstacles during navigation"
weight: 40
layout: "docs"
type: "docs"
description: "Configure vision-based obstacle detection and static obstacles for autonomous navigation."
---

The navigation service supports two kinds of obstacles: vision-detected
obstacles from cameras and static obstacles defined in configuration. You
can use both together.

## Prerequisites

- The [navigation service is configured](/navigation/how-to/navigate-to-waypoint/)
  and your robot can navigate to a waypoint.
- For vision-based detection: a [camera](/hardware/common-components/add-a-camera/)
  and a [vision service](/vision/configure/) configured to detect obstacles.

## Add vision-based obstacle detection

Each obstacle detector pairs a vision service with a camera. The vision
service analyzes frames from the camera and reports 3D obstacle geometries.
The navigation service transforms these detections into geographic
coordinates and feeds them to the path planner.

### Configure an obstacle detector

1. Open your navigation service configuration in the Viam app.
2. In the **obstacle_detectors** section, add a detector:
   - **vision_service**: the name of your vision service.
   - **camera**: the name of the camera that feeds it.
3. Click **Save**.

```json
{
  "obstacle_detectors": [
    {
      "vision_service": "obstacle-detector",
      "camera": "front-cam"
    }
  ]
}
```

### Use multiple detectors

You can configure multiple detectors for better coverage. Each detector
operates independently and contributes its obstacles to the planner. The
obstacles from all detectors are combined (not merged or deduplicated).

Common multi-detector setups:

- **Forward and rear cameras** for obstacle detection in both directions.
- **Different vision models** on the same camera (one for large obstacles,
  one for ground-level hazards).
- **Different sensor types** (a camera-based detector for visual obstacles
  and a lidar-based detector for transparent or reflective objects a camera
  would miss).

```json
{
  "obstacle_detectors": [
    {
      "vision_service": "obstacle-detector",
      "camera": "front-cam"
    },
    {
      "vision_service": "ground-hazard-detector",
      "camera": "down-cam"
    }
  ]
}
```

### How detection frequency works

The navigation service polls each detector at
`obstacle_polling_frequency_hz` (default 1 Hz). At each poll:

1. The service queries the vision service for 3D point cloud objects.
2. It transforms each detection from the camera's frame to geographic
   coordinates using the movement sensor's position and heading.
3. The transformed obstacles are added to the planner alongside any
   static obstacles.

Higher polling frequencies detect obstacles sooner but use more CPU and
camera bandwidth. For robots moving at the default 0.3 m/s, 1 Hz means
the robot moves about 30 cm between obstacle checks.

## Add static obstacles

Static obstacles are fixed geographic locations the robot should always
avoid, regardless of what the cameras see. Use these for known hazards
like ponds, buildings, restricted areas, or dropoffs.

### Configure with the visual editor

The easiest way to add static obstacles is through the Viam app:

1. Open your navigation service in the **CONFIGURE** tab.
2. The configuration card shows a map. Click to place obstacles on the
   map.
3. Define the obstacle shape (box, sphere, or capsule) and size.
4. Click **Save**.

### Configure in JSON

Static obstacles are GeoGeometry objects in the `obstacles` array:

```json
{
  "obstacles": [
    {
      "location": {
        "latitude": 40.6645,
        "longitude": -73.9382
      },
      "geometries": [
        {
          "type": "box",
          "x": 5,
          "y": 5,
          "z": 2
        }
      ]
    }
  ]
}
```

## Set up geofences (bounding regions)

Bounding regions define geographic boundaries the robot must stay within.
If configured, the path planner will not generate paths that leave these
regions. Use bounding regions to keep the robot on your property, within a
work zone, or away from roads.

Configure bounding regions in the `bounding_regions` array. The format is
the same as static obstacles (GeoGeometry objects), but the meaning is
inverted: obstacles are areas to avoid, bounding regions are areas to stay
within.

```json
{
  "bounding_regions": [
    {
      "location": {
        "latitude": 40.6643,
        "longitude": -73.938
      },
      "geometries": [
        {
          "type": "box",
          "x": 100,
          "y": 100,
          "z": 10
        }
      ]
    }
  ]
}
```

## What's next

- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust obstacle polling frequency and plan deviation for your
  environment.
- [Navigation service configuration](/navigation/reference/navigation-service/):
  full reference for obstacle and bounding region attributes.
- [Configure a vision service](/vision/configure/): set up the vision
  service that powers your obstacle detectors.
