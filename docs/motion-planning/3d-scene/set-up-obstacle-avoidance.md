---
linkTitle: "Set up obstacle avoidance"
title: "Set up obstacle avoidance"
weight: 40
layout: "docs"
type: "docs"
description: "Visualize and adjust obstacle geometry so the motion planner routes around physical objects."
---

The motion planner avoids obstacles only if it knows about them, and it knows about them only as geometries you define: boxes, spheres, or capsules positioned in the frame system. That definition is invisible in JSON. A box specified as `{x: 800, y: 1200, z: 20}` at some parent-relative translation either covers the table or it doesn't, and you can't tell which from the numbers. The **3D SCENE** tab lets you see what the planner sees, so you can check coverage before running a plan.

## Prerequisites

- A machine with an arm or gantry configured.
- At least a basic frame system configured (arm frame and world frame).
- Physical objects in the workspace that the arm needs to avoid.

## Visualize existing obstacles

### 1. Open the 3D SCENE tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D SCENE** tab.

### 2. Identify obstacles in the scene

Obstacle geometries appear as translucent shapes in the viewport and as child rows under their parent frame in the **World** panel.
Each geometry is positioned according to its frame configuration: its location is defined by a translation and orientation relative to a parent frame.

There is no separate "obstacles" list; toggle an obstacle's visibility with the eye icon on its row in the World panel, or select the row and press `H`.

Click an obstacle in the scene or in the World panel to see its details:

- **geometry**: `None`, `Box`, `Sphere`, or `Capsule`.
- **dimensions**: `x` / `y` / `z` (mm) for Box; `r` (mm) for Sphere; `r` and `l` (mm) for Capsule.
- **local position** (mm): the geometry's center relative to its parent frame.
- **parent frame**: which frame the geometry is attached to.

### 3. Compare geometry to physical objects

Orbit the scene to view obstacles from different angles.
Check that:

- Each geometry fully covers the physical object it represents. A box that is too narrow leaves a gap the arm could pass through.
- Geometries are not larger than necessary. Oversized obstacles restrict the planner's solution space and can make valid targets unreachable.
- The geometry center is at the physical object's center. A table surface geometry should be centered at the table surface height, not at the floor.

## Add or adjust obstacles

Obstacles are defined in the motion service configuration or passed as a `WorldState` parameter to `Move` requests.
For static obstacles (tables, walls, posts), define them in the configuration so they persist across motion plans.

See [Define obstacles](/motion-planning/obstacles/) for the full configuration reference, including JSON examples for each geometry type.

After changing obstacle configuration, return to the **3D SCENE** tab to verify the changes.
The scene reflects the current saved configuration.

## Choose the right geometry type

| Physical object  | Recommended geometry | Notes                                                                                 |
| ---------------- | -------------------- | ------------------------------------------------------------------------------------- |
| Table or shelf   | Box                  | Match the surface dimensions. Include thickness if the arm could approach from below. |
| Post or column   | Capsule              | Set the radius to match the column width, length to match the height.                 |
| Round obstacle   | Sphere               | Use the bounding radius. Simple and fast for collision checking.                      |
| Wall or barrier  | Box                  | Use a thin box with large x and z dimensions.                                         |
| Irregular object | Box (oversized)      | Use the bounding box of the object. Oversizing is safer than undersizing.             |

## Verify coverage

After defining obstacles, run through this checklist in the **3D SCENE** tab:

1. **Orbit to each workspace boundary.** If the arm can reach past the geometry into the physical object, the geometry is too small.
2. **Check the floor and ceiling.** If the arm can reach the floor, add a floor plane. Do the same for ceiling-mounted setups.
3. **Close narrow gaps.** If the gap between two geometries is narrower than the arm, the arm cannot fit there anyway; extend one or both geometries to close the gap.
4. **Move the arm to known-good targets.** If a target that should be reachable is blocked, the geometry is oversized or mispositioned.

## Dynamic obstacles

Static obstacles in configuration cover fixed workspace objects. For objects that move, pass geometry at runtime through the `WorldState` parameter of the `Move` request. Runtime geometry uses the same shape types as static geometry and appears in the **3D SCENE** tab the same way.

Pair a vision service with a camera to detect moving objects and feed the detections into `Move` as runtime obstacles. See the [motion service API reference](/motion-planning/reference/) for obstacle detectors.
