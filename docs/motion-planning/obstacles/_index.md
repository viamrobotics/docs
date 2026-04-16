---
linkTitle: "Obstacles"
title: "Define obstacles"
weight: 30
layout: "docs"
type: "docs"
description: "Define collision geometry so the motion planner computes safe, collision-free paths."
aliases:
  - /work-cell-layout/define-obstacles/
  - /build/work-cell-layout/define-obstacles/
  - /operate/mobility/define-obstacles/
  - /operate/mobility/define-dynamic-obstacles/
  - /operate/mobility/define-geometry/
  - /operate/mobility/move-arm/configure-additional/
  - /services/frame-system/nested-frame-config/
  - /mobility/frame-system/nested-frame-config/
  - /reference/services/frame-system/nested-frame-config/
  - /operate/reference/services/frame-system/nested-frame-config/
---

A robot arm that knows nothing about its surroundings plans the shortest path
to its target, even if that path goes through a table, a wall, or another
piece of equipment. The motion planner has no way to know that certain regions
of space are occupied unless you tell it.

By defining obstacles (tables, walls, posts, equipment, and other fixtures in
your workspace) you give the motion planner the information it needs to plan
collision-free paths. The planner routes the arm around obstacles, and if no
collision-free path exists, it returns an error rather than commanding a
dangerous motion.

## Concepts

Five ideas make up Viam's obstacle model: the geometry types you have
available, the sizing rule (Viam does not add clearance for you), the
split between static and dynamic obstacles, the `WorldState` container
that carries dynamic ones, and the passive-object pattern for things
that move with a component but have no API. The same primitives also
serve as keep-out zones; the planner treats them identically.

### Geometry types

Viam supports five geometry types for defining obstacles. The three primitives
are the most commonly used:

| Type        | JSON `type` | Config fields                          | Best for                                                                                                                                         |
| ----------- | ----------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Box**     | `"box"`     | `x`, `y`, `z` (dimensions in mm)       | Tables, shelves, walls, rectangular equipment. Match surface dimensions; include thickness if the arm could approach from below.                 |
| **Sphere**  | `"sphere"`  | `r` (radius in mm)                     | Balls, round obstacles, keep-out zones. Use the bounding radius.                                                                                 |
| **Capsule** | `"capsule"` | `r` (radius in mm), `l` (length in mm) | Posts, columns, pipes. Set the radius to match the column width and length to the height.                                                        |
| **Point**   | `"point"`   | (none, position only)                  | Single points in space.                                                                                                                          |
| **Mesh**    | `"mesh"`    | `mesh_data`, `mesh_content_type`       | Complex shapes from STL/PLY files when no primitive fits. More expensive to collision-check; use a primitive bounding shape if accuracy permits. |

For irregular objects, use a Box that fully encloses the object (over-approximation is safer than under-approximation, even though it shrinks the planner's solution space).

Each geometry has a center point (pose) relative to a reference frame, typically the world frame. Geometry configs also support `translation` and `orientation` offsets to shift the shape relative to the frame origin. Capsule length must be at least twice the radius; a capsule whose length equals exactly twice the radius becomes a sphere.

### Sizing obstacles safely

The motion planner does not add clearance around obstacle geometries by
default. The built-in collision buffer is effectively zero (1e-8 mm,
present only to prevent numerical edge cases). To keep the robot clear
of physical obstacles, size your obstacle geometries to fully enclose
the real object plus any desired safety margin: 20 to 50 mm is a
reasonable starting point for most arms. Approximate shapes that fully
enclose the real object are safer and work better with the planner than
ones that try to model every surface detail.

You can override the buffer on a per-call basis by passing
`collision_buffer_mm` in the `extra` map on a Move request. This adds
the specified clearance in millimeters to every collision check for
that call.

### Static vs dynamic obstacles

**Static obstacles** are permanent fixtures in your workspace: the table the
arm is bolted to, walls, bins, work-cell envelopes, fixed equipment. You
configure them once through the Viam app and the planner includes them on
every plan. See [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/)
for the recommended patterns.

**Dynamic obstacles** are objects your code defines at runtime and passes to
the motion service through `WorldState`. They can change between calls.
Examples include a box that was just placed on the table, a temporary
keep-out zone, or objects detected by a vision system. Both static and
dynamic obstacles use the same geometry primitives. See [Plan collision-free
paths](/motion-planning/obstacles/avoid-obstacles/) for the runtime pattern.

### Passive objects attached to a component

Some objects are always attached to a component but have no API of their own:
a camera mount bolted to an arm, a tool-changer plate, a cable bundle. The
motion planner should treat them as collision volume, but Viam has no
component to talk to.

Viam models this pattern with a passive component (typically a `generic`/`fake`)
whose frame is parented to the moving component. The geometry rides the parent
on every motion plan. The passive component never runs; it exists only to hold
the collision shape. See [Attach geometry to a moving component](/motion-planning/obstacles/configure-workspace-obstacles/#attach-geometry-to-a-moving-component)
for the configuration walkthrough.

### WorldState

WorldState is the container that holds obstacle and transform information passed
to the motion service at call time. It contains:

- **obstacles**: a list of `GeometriesInFrame`, where each entry specifies a
  reference frame and one or more geometries in that frame
- **transforms**: supplemental frame transforms that augment the frame system
  for this call only

You construct a WorldState in your code and pass it to the `Move` call.

Transforms merge into the frame system by addition only. The motion
service builds a fresh frame system for each call, appends the configured
parts, then appends each transform from `WorldState.transforms`. A
transform with a name that already exists in the configured frame system
causes the call to fail with `frame with name "<name>" already in frame
system`. Use transforms to introduce new frames (a detected object, a
picked-up workpiece), not to rewrite the pose of an existing component.

{{< expand "Coming from ROS" >}}

Viam keeps no persistent world representation between motion-planning
calls. There is no Octomap voxel grid, no costmap layer, no Planning
Scene held between calls.

Every `Move` starts with the `WorldState` you pass in. Static obstacles
from component frame configs are always included; dynamic obstacles
from `WorldState.obstacles` are included only for that call. The
planner has no memory between calls, so a dynamic obstacle passed to
one `Move` is forgotten by the next unless you pass it again.

`MoveOnGlobe` and `MoveOnMap` do maintain some state during a single
execution: configured obstacle detectors poll vision services and feed
new detections to the planner for as long as the execution runs. That
state is bounded to the execution; it does not persist once the plan
completes.

Practical consequences:

- **Stale obstacles decay automatically.** An obstacle you include in
  one `Move` and omit from the next simply disappears from the
  planner's world. There is no "clear costmap" step to run.
- **Your application is the source of truth for the world.** Whatever
  your code tracks about the environment (object positions, operator
  no-go zones, expired grasp targets) is what the planner sees. The
  motion service does not build its own picture over time.
- **For dynamic obstacle avoidance with arms,** check the world between
  calls and call `Move` again with an updated `WorldState`. `Move` does
  not re-evaluate obstacles during execution. For the per-method
  behavior, see [Replanning behavior](/motion-planning/replanning-behavior/).

{{< /expand >}}

## How-tos

{{< cards >}}
{{% card link="/motion-planning/obstacles/configure-workspace-obstacles/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/avoid-obstacles/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/attach-detach-geometries/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/allow-frame-collisions/" noimage="true" %}}
{{< /cards >}}

## What's next

- [Move an arm to a target pose](/motion-planning/move-an-arm/move-to-pose/):
  use the motion service to move the arm while avoiding obstacles.
- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  restrict how the arm moves between poses.
- [How motion planning works](/motion-planning/how-planning-works/):
  understand how the planner computes collision-free paths.
