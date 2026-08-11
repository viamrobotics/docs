---
linkTitle: "Motion planning"
title: "Motion planning"
weight: 160
layout: "docs"
type: "docs"
no_list: true
noedit: true
open_on_desktop: true
overview: true
description: "Plan and execute collision-free movements for robot arms and gantries."
notoc: true
aliases:
  - /operate/mobility/
  - /operate/mobility/motion-concepts/
  - /motion-planning/motion-how-to/
  - /navigation/
  - /navigation/how-to/
  - /navigation/how-to/avoid-obstacles/
  - /navigation/how-to/drive-a-base/
  - /navigation/how-to/follow-a-patrol-route/
  - /navigation/how-to/monitor-and-troubleshoot/
  - /navigation/how-to/navigate-to-waypoint/
  - /navigation/how-to/run-actions-at-waypoints/
  - /navigation/how-to/set-up-gps/
  - /navigation/how-to/tune-navigation/
  - /navigation/reference/
  - /navigation/reference/api/
  - /navigation/reference/navigation-service/
  - /navigation/how-to/detect-while-moving/
  - /navigation/how-to/drive-the-base/
  - /navigation/how-to/move-to-gps-coordinate/
  - /operate/mobility/move-base/
  - /how-tos/navigate/
  - /use-cases/navigate/
  - /motion-planning/motion-how-to/drive-a-base/
  - /tutorials/services/navigate-with-rover-base/
  - /motion-planning/replanning-behavior/
  - /motion-planning/reference/motion-configuration/
  - /motion-planning/reference/plan-monitoring/
  - /motion-planning/monitor-a-running-plan/
  - /motion-planning/motion-how-to/monitor-plan-execution/
  - /motion-planning/motion-how-to/monitor-a-running-plan/
  - /operate/mobility/monitor-plan-execution/
---

Your robot arm needs to move from one pose to another without colliding with
the table, the walls, or itself. To move safely, the planner must reason about
the arm's kinematic model, the workspace geometry, and the motion constraints
you impose.

Viam's motion service plans a collision-free path and executes it, using a
frame system you describe and obstacles you declare. You tell it where to go;
it handles the search.

This section covers motion planning for arms and gantries.

## Start here

New to Viam's motion service? Work through a short quickstart that uses
fake components so you can run it on any machine:

{{< cards >}}
{{% card link="/motion-planning/quickstarts/first-arm/" noimage="true" %}}
{{% card link="/motion-planning/quickstarts/frame-system/" noimage="true" %}}
{{< /cards >}}

## How it works

Each `Move` request to the motion service runs the same pipeline: it reads
the [frame system](/motion-planning/frame-system/) to know where every
component sits, reads the arm's [kinematic model](/motion-planning/reference/kinematics/)
to know what joint configurations are reachable, applies any
[obstacles](/motion-planning/obstacles/) and
[constraints](/motion-planning/move-an-arm/constraints/) you declare, and
returns a collision-free path from the current pose to your target.

## Core topics

{{< cards >}}
{{% card link="/motion-planning/frame-system/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/" noimage="true" %}}
{{< /cards >}}

## Other how-tos

{{< cards >}}
{{% card link="/motion-planning/move-gantry/" noimage="true" %}}
{{% card link="/motion-planning/verify-a-plan/" noimage="true" %}}
{{% card link="/motion-planning/debug-motion-with-cli/" noimage="true" %}}
{{< /cards >}}

## Concept pages

{{< cards >}}
{{% card link="/motion-planning/how-planning-works/" noimage="true" %}}
{{< /cards >}}

## Reference

{{< cards >}}
{{% card link="/motion-planning/reference/" noimage="true" %}}
{{< /cards >}}
