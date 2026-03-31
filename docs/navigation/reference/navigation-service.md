---
linkTitle: "Navigation service"
title: "Navigation service configuration"
weight: 10
layout: "docs"
type: "docs"
description: "Configure the navigation service for autonomous GPS-based waypoint navigation."
---

The navigation service is configured as a service in your machine's JSON
configuration. You can configure it through the Viam app UI or by editing
JSON directly.

## Required attributes

| Attribute         | Type   | Description                                                                                                                                                            |
| ----------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `base`            | string | Name of the [base component](/hardware/common-components/add-a-base/) the navigation service drives.                                                                   |
| `movement_sensor` | string | Name of the [movement sensor](/hardware/common-components/add-a-movement-sensor/) that provides GPS position and compass heading. Required when `map_type` is `"GPS"`. |
| `store`           | object | Where to store waypoints. See [Store configuration](#store-configuration).                                                                                             |

## Optional attributes

| Attribute                       | Type   | Default     | Description                                                                                                                                                                                                                                                        |
| ------------------------------- | ------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `map_type`                      | string | `"GPS"`     | `"GPS"` for GPS-based waypoint navigation. `"none"` for manual-only mode (no autonomous navigation).                                                                                                                                                               |
| `motion_service`                | string | `"builtin"` | Name of the motion service to use for path planning. Most users should leave this as the default.                                                                                                                                                                  |
| `meters_per_sec`                | float  | `0.3`       | Linear speed in meters per second. How fast the robot drives in a straight line. Start low and increase after testing. Faster speeds need more stopping distance for obstacle avoidance.                                                                           |
| `degs_per_sec`                  | float  | `20.0`      | Angular speed in degrees per second. How fast the robot turns. Higher values make sharper turns. Lower values make smoother, wider turns.                                                                                                                          |
| `plan_deviation_m`              | float  | `2.6`       | How far the robot can deviate from its planned path (in meters) before replanning. Set this larger than your GPS error. With standard GPS (~3m accuracy), the default of 2.6m means frequent replanning. Consider 5-10m for standard GPS, or 1-2m if you have RTK. |
| `position_polling_frequency_hz` | float  | `1.0`       | How often to check the robot's GPS position, in Hz. Higher values detect deviation sooner but use more CPU. 1 Hz is sufficient for most outdoor robots.                                                                                                            |
| `obstacle_polling_frequency_hz` | float  | `1.0`       | How often to query obstacle detectors, in Hz. Higher values detect obstacles sooner but use more CPU and camera bandwidth.                                                                                                                                         |
| `obstacle_detectors`            | array  | `[]`        | List of vision service and camera pairs for obstacle detection. See [Obstacle detectors](#obstacle-detectors).                                                                                                                                                     |
| `obstacles`                     | array  | `[]`        | Static obstacles the robot should avoid, defined as geographic geometries. These are fixed locations on the map (buildings, ponds, restricted areas). Configure these through the visual editor in the Viam app's configure tab.                                   |
| `bounding_regions`              | array  | `[]`        | Geographic regions the robot must stay within (geofences). If configured, the robot will not navigate outside these boundaries. Define these as geographic geometries.                                                                                             |
| `log_file_path`                 | string | `""`        | Path to a file for navigation debug logging. When set, all navigation service logging (mode transitions, waypoint attempts, obstacle detections, frame transformations) is written to this file. Useful for debugging navigation behavior in the field.            |

## Store configuration

The `store` object configures where waypoints are persisted.

| Field  | Type   | Description                          |
| ------ | ------ | ------------------------------------ |
| `type` | string | `"memory"` (default) or `"mongodb"`. |

**Memory store** keeps waypoints in RAM. Simple, no dependencies, works
for development and single-session deployments. Waypoints are lost when
`viam-server` restarts.

**MongoDB store** persists waypoints to a MongoDB database. Waypoints
survive restarts. Requires a MongoDB server accessible from the machine.
Add a `config` object with your MongoDB connection details:

```json
{
  "type": "mongodb",
  "config": {
    "uri": "mongodb://127.0.0.1:27017"
  }
}
```

## Obstacle detectors

Each obstacle detector pairs a [vision service](/vision/configure/) with a
[camera](/hardware/common-components/add-a-camera/). The vision service
analyzes frames from the camera and reports detected obstacles. The
navigation service transforms these detections into geographic coordinates
and feeds them to the path planner.

You can configure multiple detectors. Each one contributes obstacles
independently. For example, use a forward-facing camera for path obstacles
and a downward-facing camera for terrain hazards.

```json
{
  "obstacle_detectors": [
    {
      "vision_service": "obstacle-detector",
      "camera": "front-cam"
    },
    {
      "vision_service": "terrain-classifier",
      "camera": "down-cam"
    }
  ]
}
```

## Full example

```json
{
  "name": "my-nav",
  "api": "rdk:service:navigation",
  "model": "builtin",
  "attributes": {
    "base": "my-base",
    "movement_sensor": "my-gps",
    "map_type": "GPS",
    "store": {
      "type": "memory"
    },
    "meters_per_sec": 0.5,
    "degs_per_sec": 30,
    "plan_deviation_m": 5.0,
    "position_polling_frequency_hz": 2,
    "obstacle_polling_frequency_hz": 2,
    "obstacle_detectors": [
      {
        "vision_service": "obstacle-detector",
        "camera": "front-cam"
      }
    ]
  }
}
```

## What's next

- [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/):
  set up the navigation service and send your robot to a GPS coordinate.
- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust speeds, deviation threshold, and polling for your environment.
- [Navigation API](/navigation/reference/api/): full method reference.
