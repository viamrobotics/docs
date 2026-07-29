---
linkTitle: "Navigation"
title: "Navigation and localization"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "How a mobile robot knows where it is and drives itself to a goal: localization, SLAM, sensor fusion, base navigation, and multi-robot coordination."
---

Before a mobile robot can go anywhere on purpose, it has to answer one
question: _where am I?_ Everything else, planning a path, driving to a goal,
coordinating with other robots, builds on that answer. This section covers
how a machine estimates its own position and uses that estimate to move.

- [How a robot knows its position](localization/): odometry, GPS, and SLAM as
  localization sources, and their drift and cost trade-offs.
- [SLAM and mapping](slam-and-mapping/): building a map and locating within it.
- [Combine sensors with sensor fusion](sensor-fusion/): why one sensor is
  rarely enough, and what "fusion" does and doesn't mean today.
- [Navigate a mobile base to a goal](navigate-a-mobile-base/): drive to a map
  or GPS waypoint with the motion service.
- [Coordinate a multi-robot fleet](coordinate-a-fleet/): share tasks and avoid
  deadlock across machines.
