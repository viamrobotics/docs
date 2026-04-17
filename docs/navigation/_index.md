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

Outdoor mobile robots need to reach GPS coordinates on their own without
a human joystick operator in the loop. The navigation service does this:
you define waypoints, and the robot drives between them, replanning around
obstacles as it goes.

This is GPS-based outdoor navigation. You need a mobile base, a GPS-capable
movement sensor, and optionally cameras with vision services for obstacle
detection. The navigation service plans paths, replans when the robot
deviates, and avoids obstacles. Your code sets waypoints and monitors
progress.

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
- **Switch between manual and autonomous control.** Set the mode to
  Waypoint to navigate autonomously, or Manual to drive the base directly.
  Switching to Manual stops the active plan but preserves the waypoint
  queue.

## What you need

- A configured [base](/hardware/common-components/add-a-base/) (the robot's
  drive system).
- A configured [movement sensor](/hardware/common-components/add-a-movement-sensor/)
  that provides GPS position and compass heading.
- Optionally, one or more [camera](/hardware/common-components/add-a-camera/)
  and [vision service](/vision/configure/) pairs for obstacle detection.

## How it works

The navigation service operates in one of two modes. In Manual mode the
service is passive and reports the robot's location but does not drive.
In Waypoint mode the service drives the base: it picks the next
unvisited waypoint, calls the motion service's MoveOnGlobe to plan and
execute a path, then moves to the next waypoint on arrival. If a
waypoint fails (obstacle, deviation, error), the service retries
indefinitely.

The service uses the motion service internally for path planning and
execution. You don't call the motion service directly when using
navigation.

{{< cards >}}
{{% card link="/navigation/how-to/" %}}
{{% card link="/navigation/reference/" %}}
{{< /cards >}}
