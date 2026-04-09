---
linkTitle: "Set up obstacle avoidance"
title: "Set up obstacle avoidance"
weight: 40
layout: "docs"
type: "docs"
description: "Visualize and adjust obstacle geometry so the motion planner routes around physical objects."
---

The motion planner needs to know where physical objects are in your workspace to plan collision-free paths.
You define obstacles as geometries (boxes, spheres, or capsules) positioned in the frame system.
The 3D scene tab lets you see exactly how these geometries cover your workspace, so you can verify that the planner has an accurate picture before you run a motion plan.

## Prerequisites

- A machine with an arm or gantry configured.
- At least a basic frame system configured (arm frame and world frame).
- Physical objects in the workspace that the arm needs to avoid.

## Visualize existing obstacles

### 1. Open the 3D scene tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D scene** tab.

### 2. Identify obstacles in the scene

Obstacle geometries appear as translucent shapes.
Each geometry is positioned according to its frame configuration: its location is defined by a translation and orientation relative to a parent frame.

Click an obstacle in the scene or the tree view to see its details:

- **Geometry type**: box, sphere, or capsule.
- **Dimensions**: size in mm (for example, x/y/z for a box, radius for a sphere, radius and length for a capsule).
- **Position**: where the geometry's center is located.
- **Parent frame**: which frame the geometry is attached to.

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

After changing obstacle configuration, return to the 3D scene tab to verify the changes.
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

After defining obstacles, run through this checklist in the 3D scene:

1. **Orbit to each workspace boundary.** Can the arm reach past the obstacle geometry into the physical object? If yes, the geometry needs to be larger.
2. **Check the floor and ceiling.** If the arm can reach the floor, add a floor plane geometry. Same for ceiling-mounted setups.
3. **Check between obstacles.** Narrow gaps between geometries that the arm cannot physically fit through should be closed by extending one or both geometries.
4. **Move the arm to known-good targets.** If a target that should be reachable is blocked by obstacle geometry, the geometry is oversized or mispositioned.

## Dynamic obstacles

Static obstacles defined in configuration cover fixed objects in the workspace.
For objects that move (a person, a moving conveyor, another robot), you can pass obstacle geometry at runtime in the `WorldState` parameter of the `Move` request.
Dynamic obstacles use the same geometry types (box, sphere, capsule) and appear in the 3D scene when passed to the motion planner.

Pair a vision service with a camera to detect obstacles at runtime and feed them into the motion planner as dynamic obstacles.
See the [motion service API reference](/motion-planning/reference/) for details on obstacle detectors.
