---
linkTitle: "Avoid obstacles"
title: "Avoid obstacles during navigation"
weight: 40
layout: "docs"
type: "docs"
description: "Configure vision-based obstacle detection and static obstacles for autonomous navigation."
aliases:
  - /navigation/how-to/detect-while-moving/
---

The navigation service keeps the robot away from two kinds of obstacles:
fixed hazards you declare in configuration (ponds, buildings, no-go
zones) and dynamic hazards that cameras detect while the robot drives.
You can use both together, and the planner merges them into a single
avoidance set.

## Prerequisites

- The [navigation service is configured](/navigation/how-to/navigate-to-waypoint/)
  and your robot can navigate to a waypoint.
- For vision-based detection: a [camera](/hardware/common-components/add-a-camera/)
  and a [vision service](/vision/configure/) configured to detect obstacles.

## Add vision-based obstacle detection

Each obstacle detector pairs a vision service with a camera. The vision
service reports 3D geometries for anything it detects in the camera
frame, and the navigation service transforms those detections into
geographic coordinates for the path planner.

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
- **Different sensor types.** A camera-based detector catches visual
  obstacles; a lidar-based detector catches transparent or reflective
  objects that a camera misses.

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
`obstacle_polling_frequency_hz`, which defaults to 1 Hz. On each poll,
the service queries the vision service for 3D point cloud objects,
converts each detection from the camera frame to latitude and longitude
using the movement sensor's pose, and passes the result to the planner
alongside the static obstacles.

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

Static obstacles are GeoGeometry objects in the `obstacles` array. Geometry
dimensions are in millimeters.

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
          "x": 5000,
          "y": 5000,
          "z": 2000
        }
      ]
    }
  ]
}
```

This defines a 5 m x 5 m x 2 m box obstacle (roughly a small shed) anchored
at the given latitude and longitude.

## Set up geofences (bounding regions)

Bounding regions define geographic boundaries the robot must stay within.
If configured, the path planner will not generate paths that leave these
regions. Use bounding regions to keep the robot on your property, within a
work zone, or away from roads.

Bounding regions use the same `GeoGeometry` format as static obstacles
but have the opposite meaning. Obstacles are volumes the robot avoids;
bounding regions are volumes the robot must stay inside. Configure them
in the `bounding_regions` array.

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
          "x": 100000,
          "y": 100000,
          "z": 10000
        }
      ]
    }
  ]
}
```

This defines a 100 m x 100 m x 10 m volumetric bounding region (roughly one
hectare) centered at the given latitude and longitude.

## What's next

- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust obstacle polling frequency and plan deviation for your
  environment.
- [Navigation service configuration](/navigation/reference/navigation-service/):
  full reference for obstacle and bounding region attributes.
- [Configure a vision service](/vision/configure/): set up the vision
  service that powers your obstacle detectors.
