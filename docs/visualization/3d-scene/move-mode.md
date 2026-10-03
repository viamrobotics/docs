---
linkTitle: "Move mode"
title: "Move mode"
weight: 30
layout: "docs"
type: "docs"
description: "Plan a move to a target pose in the 3D scene, preview the planned motion, and run it on the machine."
capabilities: ["scene-3d", "motion-planning"]
diataxis: explanation
---

Move mode turns the 3D scene into a control for the motion service. You choose a frame, set where it should go, and the motion service plans the motion. You can preview the plan in the scene before anything moves, then run it on the machine.

{{< alert title="Move mode moves real hardware" color="caution" >}}
Running a plan moves the machine. The planner avoids only the geometry it knows about: the geometry in your frame system configuration and any obstacles you pass with the request. It does not avoid objects that are only drawn in the scene, or anything in the workspace that isn't modeled.
{{< /alert >}}

## What you can move

Move mode plans a move for the selected frame through the motion service's `Move` method. The frame has to be carried by a component that moves, such as an arm or a gripper attached to an arm.

Selecting a frame that nothing moves, such as a fixed obstacle or a target marker attached to the world frame, still opens the move controls, but planning fails with `zero IK solutions produced, goal positions appears to be physically unreachable`.

## The move controls

In Move mode, the Details panel for the selected frame becomes a form for a `Move` request:

- **motion service**: the motion service that plans the move. It defaults to `builtin`, and resets to it when you leave the tab.
- **world position** and **world orientation**: the target pose, starting at the frame's current pose. Type values, or drag the frame's transform controls in the viewport.
- **travel**: the straight-line distance and rotation from the current pose to the target.
- **World state** (optional JSON): obstacles and transforms for this request only, in the same shape as the `WorldState` you pass to `Move` in code. See [World state](/visualization/reference/world-state/).
- **Constraints** (optional JSON): constraints on the path, such as `{"linear_constraint": [{"line_tolerance_mm": 1, "orientation_tolerance_degs": 2}]}` to keep the frame on a straight line. See [Move with constraints](/motion-planning/move-an-arm/move-with-constraints/).
- **Collisions**: what the frame is touching now, or would collide with at the target.

## Preview, then run

You can plan and run a move in one step, or preview it first:

- **Preview move** plans the move and shows it in the scene without moving the machine. A translucent copy of the machine appears at its current pose. Once a plan is found, playback controls appear, and playing the preview moves the copy along the plan.
- **Execute plan** runs the plan you previewed, without planning again.
- **Move** plans again and runs the new plan in one step, even if you already previewed one.

A plan is a list of waypoints: joint positions the arm passes through. How many waypoints a plan has depends on the move. An unconstrained move often plans as just a start and an end. A move with a linear constraint can have hundreds of closely spaced waypoints.

The preview can show each frame in one of two ways:

- **Waypoints** shows only the planned waypoints. A two-waypoint plan jumps from start to end.
- **Interpolated** adds frames between widely spaced waypoints, so you can see how the arm sweeps from one to the next. For a plan whose waypoints are already close together, the two views look the same.

The preview is an approximation. Plans carry no timing, so playback runs at a fixed rate, and how the arm moves between waypoints is up to the arm's driver, not the planner.

## Collisions

The **Collisions** readout checks the selected frame's geometry against everything drawn in the scene, and lists each colliding pair of geometries. It shows what the frame is currently touching, and after a preview, what it would collide with at the target.

The readout is a warning, not a gate: you can still run a move it flags. It also checks against geometry the planner never sees, such as custom visuals published by a module. A plan the planner accepts can still show a collision here, and the reverse is true too: obstacles you add in **World state** affect the plan but are not drawn, so the readout doesn't check them. See [Visuals and collisions](/visualization/visuals-and-collisions/).

Some flagged collisions are intended. A gripper that must touch an object to pick it up collides with that object at the grasp pose.

## Obstacles and constraints for one move

Obstacles in **World state** change the plan without appearing in the scene. A move that takes an unexpected route around empty space usually has a **World state** obstacle in the way. To see a request's obstacles after the fact, save plans and replay them in [Monitor mode](/visualization/3d-scene/monitor-mode/): a replayed plan draws the obstacles it was planned against.

A constraint limits the path, not just the target, so it can turn a plan the planner would otherwise find into a failure. For example, a linear constraint whose straight line crosses an obstacle fails, where the same move without the constraint would route around the obstacle.

## When planning fails

The error appears in the move controls. Most errors name the geometries involved, so read the names first:

- `asked for a pose too far`: the target is out of reach. The reported distance is to the arm's end frame, so it includes the offset of anything attached to the arm, such as a gripper.
- `all IK solutions failed constraints`, followed by a list of collisions: the arm can reach the target, but every way of reaching it collides with something. Each entry names the two colliding geometries and the share of candidates that collision ruled out.
- `fatal early collision`: a pose the plan must pass through collides with a **World state** obstacle.
- `zero IK solutions produced`: no arm configuration reaches the target at all. Common causes are a frame that nothing moves, a target too close to the arm's base, or an orientation the arm cannot reach.

Arms with fewer than six joints can reach far fewer orientations than six-joint arms. On these arms, most targets fail with `zero IK solutions produced` unless you choose an orientation the arm can reach. Pointing straight down, with an orientation vector of `0, 0, -1`, is reachable across most of the workspace.

## Save plans for replay

Plans from Move mode are saved only if the motion service selected in the move controls is configured to save them. See [Save plans for replay](/motion-planning/visualize-a-motion-plan/#save-plans-for-replay). Every preview writes a plan file, including previews you never run, and a **Move** after a preview writes a second one.

## What's next

- [Monitor mode](/visualization/3d-scene/monitor-mode/): replay a saved plan and see the obstacles it was planned against.
- [How motion planning works](/motion-planning/how-planning-works/): what the planner does with your request.
- [Debug a motion plan](/motion-planning/debug-motion-plan/): check frames, obstacles, and reach when a plan fails.
