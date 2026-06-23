---
linkTitle: "Visuals and collisions"
title: "Visuals and collisions"
weight: 10
layout: "docs"
type: "docs"
description: "How a Transform defines a custom visual, and which geometry the motion planner actually collision-checks."
---

A custom visual in the 3D scene is a `Transform`: a piece of geometry placed
somewhere in the frame system, with styling that controls how it draws. The
world state store service streams these transforms to the scene. This page
covers what a transform contains, how the scene tracks it over time, and the point
that trips people up most: the scene draws your visual, while the planner avoids a
separate collision geometry.

## Anatomy of a transform

A `Transform` carries four things that together place and style one visual:

- **Reference frame and pose**: where the visual sits. The pose is given in a
  parent reference frame, so the visual is positioned in the frame system and
  moves with its parent.
- **Geometry**: the shape to draw (a box, sphere, capsule, mesh, or point
  cloud).
- **Metadata**: styling such as color and opacity.
- **UUID**: a stable identifier for this specific visual.

The reference frame and pose decide _where_, the geometry decides _what shape_,
and the metadata decides _how it looks_.

## The UUID gives a visual a stable identity

Each transform has a UUID. That identifier is what lets a module change one
visual without disturbing the rest of the scene: to update a visual, the module
re-sends a transform with the same UUID; to remove it, it references that UUID;
to add a new one, it uses a fresh UUID. Without stable identifiers the client
would have to re-render everything on every change. With them, the scene applies
incremental add, update, and remove operations to individual visuals.

## Geometry types

A transform's geometry is the shape the scene draws. The supported types are:

- **box**: dimensions in millimeters
- **sphere**: a radius
- **capsule**: a radius and length
- **mesh**: an arbitrary triangle mesh
- **point cloud**: a set of points

Choose the type that matches what you are representing: a box or capsule to
approximate a physical object, a mesh for a precise model, a point cloud for
sensor data.

## Metadata styles the visual

The metadata is a set of rendering attributes the scene reads when it draws the
geometry:

- `color`: the fill color
- `opacity`: how transparent the shape is
- per-point colors: for point cloud geometry
- `collision_allowed`: a hint about whether the geometry represents an allowed
  collision

These are **visualization attributes**: the scene reads them when it draws the
geometry. They control how the visual looks, including `collision_allowed`, which is
a rendering hint about the visual. The planner reads its solid geometry from the frame
system and `WorldState` instead, so these attributes shape the picture while the
planner's obstacles come from elsewhere.

## The scene draws, the planner collision-checks

The geometry on a world state store transform renders in the 3D scene: publishing a
box draws a box. The motion planner collision-checks a separate geometry, which it
reads from two places:

- The **frame system**: each component's `frame.geometry`.
- The **`WorldState`** you pass to a `Move` call: obstacles and transforms
  supplied for that single planning request.

A world state store transform and a `WorldState` obstacle travel two paths, each with
its own job: one is drawn in the scene, the other is planned around. The same shape can
take both paths.

## Making a geometry both visible and collision-checked

If you want a geometry to appear in the scene _and_ be avoided by the planner,
you do both, separately:

- **For the scene**: publish it as a transform through the world state store
  service (see [Publish visuals from a module](/visualization/publish-visuals-from-a-module/)).
- **For planning**: add it to the frame system, or include it in the
  `WorldState` you pass to `Move`.

Today these are two separate outputs you produce from the same source data: one
transform for the scene, one geometry for the planner.

## What's next

- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/):
  implement a world state store service that publishes transforms.
- [Define obstacles](/motion-planning/obstacles/): the geometry the planner
  collision-checks.
- [Frame system](/motion-planning/frame-system/): how the planner gets the
  geometry and frames it plans around.
