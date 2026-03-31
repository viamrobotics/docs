---
linkTitle: "Navigation"
title: "Navigation"
weight: 170
layout: "docs"
type: "docs"
no_list: true
noedit: true
open_on_desktop: true
overview: true
description: "Autonomous GPS-based navigation for mobile robot bases."
notoc: true
---

The navigation service gives a mobile robot the ability to navigate
autonomously to GPS coordinates while avoiding obstacles. You define
waypoints on a map, and the robot drives itself between them.

This is GPS-based outdoor navigation. You need a mobile base, a GPS-capable
movement sensor, and optionally cameras with vision services for obstacle
detection. The navigation service handles path planning, replanning when
the robot deviates, and obstacle avoidance. Your code sets waypoints and
monitors progress.

## What you can do

- **Navigate to GPS coordinates.** Send the robot to a specific latitude
  and longitude. The navigation service plans a path and drives the base
  there, replanning if the robot deviates or encounters obstacles.
- **Follow patrol routes.** Define a sequence of waypoints and the robot
  navigates to each one in order.
- **Avoid obstacles.** Configure vision services and cameras as obstacle
  detectors. The navigation service feeds detected obstacles into the
  path planner automatically. You can also define static obstacles and
  geofences (bounding regions) in the configuration.
- **Switch between manual and autonomous control.** Set the navigation
  mode to Manual to drive the base directly, or Waypoint to start
  autonomous navigation. Switching to Manual stops the current plan but
  preserves your waypoints.

## What you need

- A configured [base](/hardware/common-components/add-a-base/) (the robot's
  drive system).
- A configured [movement sensor](/hardware/common-components/add-a-movement-sensor/)
  that provides GPS position and compass heading.
- Optionally, one or more [camera](/hardware/common-components/add-a-camera/)
  and [vision service](/vision/configure/) pairs for obstacle detection.

## How it works

The navigation service operates in one of two modes:

- **Manual mode.** The service is passive. You control the base directly
  through base API calls or the Control tab. The service still reports
  the robot's location through GetLocation.
- **Waypoint mode.** The service takes control of the base. It picks the
  next unvisited waypoint, calls the motion service's MoveOnGlobe to plan
  and execute a path, monitors progress, and moves to the next waypoint
  when it arrives. If navigation fails (obstacle, deviation, error), the
  service retries the same waypoint automatically.

The service uses the motion service internally for path planning and
execution. You don't call the motion service directly when using
navigation.

{{< cards >}}
{{% card link="/navigation/how-to/" %}}
{{% card link="/navigation/reference/" %}}
{{< /cards >}}
