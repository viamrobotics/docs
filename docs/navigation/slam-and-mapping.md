---
linkTitle: "SLAM and mapping"
title: "SLAM and mapping"
weight: 20
layout: "docs"
type: "docs"
description: "How a mobile robot builds a map of an unknown space while tracking its own position within it, and when to map live versus localize against a prebuilt map."
---

A robot vacuum starts in the middle of a living room it has never seen. It has
no floor plan and no marker on a wall telling it where it stands. Within a few
minutes it has both: a map of the rooms it can reach and a steady sense of where
it sits on that map. It builds the map and finds itself on the map at the same
time. That combined trick is **SLAM**.

## What SLAM produces

SLAM stands for **Simultaneous Localization And Mapping**. The two halves name
the two outputs:

- **A map.** A machine-readable model of the space, commonly an _occupancy grid_
  (a top-down grid where each cell is marked free, occupied, or unknown) or a
  _point cloud_ (a set of 3D points sampled from surfaces the sensors saw).
- **A live pose.** The robot's current position and orientation _within that map_,
  updated continuously as it moves.

The word _simultaneous_ carries the whole idea. Mapping and localization each
depend on the other, which looks like a chicken-and-egg problem: to place a new
wall on the map, the robot needs to know where it was standing when it saw the
wall; to know where it is standing, it needs a map to compare its view against.
SLAM breaks the loop by solving both together. Each new sensor reading nudges the
map and the pose estimate at the same time, and the two converge as the robot
explores. This is what separates SLAM from plain [localization](localization/):
localization answers _where am I_ against a map that already exists, while SLAM
produces the map and the answer together.

## What hardware SLAM requires

SLAM works by matching what the robot senses now against what it sensed a moment
ago and against the map so far. That matching needs sensors that measure the
_shape_ of the surroundings, plus a rough guess of how the robot moved between
readings:

- **A ranging sensor** that reports distances to surrounding surfaces. A spinning
  **LIDAR** sweeps a plane and returns distance at each angle; a **depth camera**
  reports distance per pixel across its field of view. Either gives the geometry
  that becomes the map.
- **Odometry**, a rough estimate of motion from wheel encoders or an inertial
  sensor. This seeds each match with a starting guess ("I probably moved forward
  about 20 cm"), which the ranging data then corrects.

A plain color camera with no depth, or a bare GPS receiver, does not supply the
per-surface geometry SLAM relies on, so a supported ranging sensor is the core
requirement.

## Two modes: map live or localize against a prebuilt map

SLAM on a Viam machine runs as a **SLAM service** (a module paired with a
supported ranging sensor). You configure it in one of two modes, and the right
choice depends on whether the space is already mapped and how stable it is.

**Map live.** The robot builds a fresh map as it drives and localizes against
that growing map in real time. Choose this when the space is unknown, when it
changes often enough that a saved map would go stale, or when you are creating a
map to save and reuse later. The cost is compute and time: the robot is doing the
full simultaneous problem on every reading.

**Localize against a prebuilt map.** You supply a map captured earlier, and the
service only estimates the pose against it, the mapping half is already done.
Choose this when the environment is stable (a warehouse, a fixed building) and you
want lower compute, faster startup, and repeatable behavior across runs. The
trade-off is that the map is a snapshot: if the space is rearranged, the robot's
matches degrade until you remap.

A common pattern combines them: map the space live once, save that map, then run
in localize-only mode for day-to-day operation and remap when the layout changes.

Because these are configuration choices on the SLAM service rather than separate
components, you can switch modes by changing the service configuration. For the
exact configuration shape, supported sensors, and available SLAM modules, see the
[navigation and SLAM reference](/reference/services/navigation/) and
[How a robot knows where it is](localization/).

## How the map feeds navigation

The map and pose are inputs, not the goal. Once SLAM reports where the robot is on
a map, navigation can plan a route across that map to a destination and drive the
base there, steering around the obstacles the map records. That handoff, from
"where am I on the map" to "drive me to that spot", is covered in
[Navigate a mobile base to a goal](navigate-a-mobile-base/).

## Next steps

- [How a robot knows where it is](localization/): how odometry, GPS, and SLAM
  compare as sources of position.
- [Navigate a mobile base to a goal](navigate-a-mobile-base/): turn a map and a
  pose into motion toward a destination.
- [Navigation and SLAM reference](/reference/services/navigation/): configuration
  fields, supported sensors, and the API.
