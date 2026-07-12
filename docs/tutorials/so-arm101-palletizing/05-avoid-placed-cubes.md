---
title: "Phase 5: Avoid placed cubes"
linkTitle: "5. Avoid placed cubes"
type: "docs"
slug: "avoid-placed-cubes"
weight: 50
description: "Model placed cubes and the held cube in WorldState so the planner stacks the full two layers collision-free."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 5
phase_total: 6
prev: "/tutorials/so-arm101-palletizing/pack-from-python/"
next: "/tutorials/so-arm101-palletizing/inline-module/"
languages: ["python"]
draft: true
---

In this phase you teach the motion service about the cubes already on the pallet and the cube in the gripper, so it plans around them instead of through them. Finishing this phase is milestone two: a full, collision-free two-layer pack.

## Why the planner collides

<!-- TODO: explain that the motion service only avoids obstacles you pass it on each move; the bottom-layer pack in Phase 4 had nothing to avoid, but stacking the second layer on top of the first means the arm and the held cube now pass near cubes that are already placed. Without modeling them, the planner routes straight through. -->

## Model placed cubes as obstacles

<!-- TODO: build a WorldState of RectangularPrism geometries (one per placed cube) in the "world" frame and pass it to motion.move via the world_state argument. Imports needed: WorldState, GeometriesInFrame, Geometry, RectangularPrism, Vector3. -->

<!-- TODO (content fidelity): obstacle z = half the geometry height, since the pose is the CENTER of the prism, not its base. Dynamic obstacles like this belong in the per-move WorldState, not in the static machine config. -->

## Model the held cube

<!-- TODO: attach the held cube's geometry to the gripper frame so it moves with the arm and the planner accounts for it while carrying a cube between cells. -->

## Run the full two-layer pack

<!-- TODO: run the pack step end to end across all eight cubes, collision-free, and watch the obstacles render in the 3D scene tab as they accumulate. This is milestone two. -->

{{< workshop-nav >}}
