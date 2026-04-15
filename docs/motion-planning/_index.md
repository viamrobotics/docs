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
---

Your robot arm needs to move from one position to another without colliding with
the table, the walls, or itself. Computing a collision-free path through 3D
space means reasoning about the arm's kinematic model, the workspace geometry,
and any constraints on how the arm should move.

Viam's motion service handles this for you. You describe the spatial layout of
your workspace (the frame system) and any obstacles, then tell the arm where to
go. The planner finds a safe path and executes it.

This section covers motion planning for arms, gantries, and other kinematic
chains. For GPS-based autonomous navigation with mobile bases, see
[Navigation](/navigation/).

## Start here

New to Viam's motion service? Work through a short quickstart that uses
fake components so you can run it on any machine:

{{< cards >}}
{{% card link="/motion-planning/quickstarts/first-arm/" noimage="true" %}}
{{% card link="/motion-planning/quickstarts/frame-system/" noimage="true" %}}
{{< /cards >}}

## How it works

Motion planning in Viam connects several pieces:

1. **Frame system**: a coordinate tree that tracks where every component is in
   space. The frame system lets you specify target positions in any frame and
   translates between them automatically.

2. **Kinematic model**: a description of the arm's joints and links that tells
   the planner what configurations are physically possible.

3. **Obstacles**: geometry (boxes, spheres, capsules) that define regions the
   arm must avoid.

4. **Constraints**: rules about how the arm should move between poses, such as
   keeping the end effector on a straight line or maintaining its orientation.

5. **Motion service**: takes the frame system, kinematic model, obstacles, and
   constraints and computes a collision-free path from the current pose to the
   target.

## Topic subsections

{{< cards >}}
{{% card link="/motion-planning/frame-system/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/pick-and-place/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/" noimage="true" %}}
{{< /cards >}}

## Other how-tos

{{< cards >}}
{{% card link="/motion-planning/move-gantry/" noimage="true" %}}
{{% card link="/motion-planning/monitor-a-running-plan/" noimage="true" %}}
{{% card link="/motion-planning/debug-motion-with-cli/" noimage="true" %}}
{{< /cards >}}

## Concept pages

{{< cards >}}
{{% card link="/motion-planning/how-planning-works/" noimage="true" %}}
{{% card link="/motion-planning/replanning-behavior/" noimage="true" %}}
{{< /cards >}}

## Reference

{{< cards >}}
{{% card link="/motion-planning/reference/" noimage="true" %}}
{{< /cards >}}
