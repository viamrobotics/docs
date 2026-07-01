---
linkTitle: "Force and compliance control"
title: "Force and compliance control"
weight: 10
layout: "docs"
type: "docs"
description: "Why contact tasks like insertion need force feedback and compliance, and how a grasped part becomes part of the arm's collision geometry during planning."
---

Picture an arm pressing a round peg into a hole that is only a fraction of a
millimeter wider than the peg. You command the arm to the exact pose where the
peg should end up and move it straight down. The peg touches the rim slightly
off-center, catches, and stops. Position control keeps driving toward the
commanded pose, so the arm pushes harder against a wall it cannot pass through.
The peg jams, and the force at the contact point climbs until something flexes
or the motors stall.

This is the core problem with contact tasks. When an arm moves through open air,
knowing where to go is enough. When it presses two parts together, where to go
is only half the story. The other half is how hard to push and when to stop or
adjust. Insertion tasks such as seating a connector, tending tasks such as
loading a part into a fixture, and any operation where the tool touches the
world all share this property.

## Why position-only control struggles with contact

A position controller has one goal: drive the joints until the tool reaches a
commanded pose. It succeeds by minimizing the gap between where the tool is and
where you told it to be. That works well in free space, where the only thing
between the current pose and the target is air.

Contact changes the situation. Real parts have tiny misalignments, the hole is
never exactly where the model says, and surfaces have friction. A stiff
position controller treats the resulting contact force as an error to overcome,
so it commands more torque to close a gap that physical contact makes impossible
to close. The result is high contact forces, jamming, and marred parts. The
information the controller needs, how much force the contact is producing, never
enters the loop.

## Force and torque feedback

Force and torque feedback adds that missing information. A force/torque (F/T)
sensor, usually mounted at the wrist between the arm and the gripper, measures
the forces and torques the tool experiences: how hard it is pushing along each
axis and how much it is being twisted around each axis. In plain terms, it lets
the arm feel contact rather than only tracking position.

With that signal available, the control goal can shift. Instead of only asking
"is the tool at the commanded pose," the system can also ask "is the contact
force within the range I want." For a peg insertion, a useful strategy is to
press downward with a gentle, bounded force while allowing small sideways motion
so the peg can slide until it aligns with the hole, then seat it. The force
reading tells the system when the peg has bottomed out and the task is complete.

## Compliance: yielding to contact

Compliance is the willingness of the arm to yield when it meets resistance,
rather than holding a commanded pose rigidly. A compliant arm behaves a little
like a spring: push on it, and it gives a controlled amount instead of fighting
back with full torque.

Compliance is what turns force feedback into useful behavior. If the peg
contacts the rim off-center, a compliant response lets the arm move sideways in
the direction the contact pushes it, so the peg settles into the opening instead
of jamming against the edge. You choose how compliant each direction is: an
insertion often stays stiff along the insertion axis, so the arm still drives
the peg home, while staying soft in the sideways directions, so the part can
self-align. This selective softness is what makes reliable insertion and tending
possible.

At a high level, the control idea is a loop that blends two aims: reach the
target region using position, and regulate contact using force. The F/T sensor
reports the current force, the controller compares it to the force you want, and
it adjusts the commanded motion so the actual force stays in range. The details
vary by strategy, but the shape is always feedback on force rather than position
alone.

## Assembling force control on Viam

Force control is an active area rather than a single turnkey primitive. The
building blocks are a force-capable arm or an arm paired with a wrist F/T
sensor, a fast feedback loop, and a control strategy tuned to the task. In
practice, teams implement this pattern as a custom
[module](/operate/get-started/other-hardware/) that reads the F/T sensor,
runs the force loop, and commands the arm. Treat any specific force-control API
as something you provide in your module rather than a built-in signature, and
size the approach to the hardware you actually have: a sensitive insertion needs
a genuinely force-capable arm and a responsive sensor, not just position
commands issued quickly.

## The payload point: a grasped part joins the arm's geometry

Contact tasks usually start by picking something up, and that changes what the
planner has to reason about. Before the grasp, the motion planner models the arm
and gripper and routes them around obstacles. The moment the gripper closes on a
part, that part rigidly extends the gripper. A connector held in the jaws sweeps
through space exactly as the gripper does, so from the planner's point of view it
is now part of the moving hardware.

If you do not tell the planner about the held part, motion planning still avoids
collisions for the arm and gripper while treating the carried part as empty
space. The part can then clip a fixture wall or the edge of the workspace on the
way to the insertion point, even though the plan looks collision-free.

The fix is to describe the grasped part as a geometry and attach it to the
gripper's frame in the planning world. When you call the motion service, its
[`WorldState`](/motion-planning/) carries both obstacles and transforms. Adding
a transform whose parent is the gripper frame, with a geometry sized to the held
part, places that shape in the planner's model of the scene. Because it is
parented to the gripper frame, it moves with the gripper as the arm moves,
exactly like the real part. Motion planning then routes the arm, the gripper,
and the carried part around obstacles together. When the gripper releases the
part, you drop that transform from `WorldState` so the planner stops carrying a
shape that is no longer attached.

This is where the [frame system](/motion-planning/frame-system/) does the work.
Frames define how each part of the machine is positioned relative to its parent,
and a geometry parented to the gripper frame inherits the gripper's motion for
free. Getting the gripper frame right, and sizing the attached geometry to
enclose the real part with a small margin, is what lets the arm carry a part
through a cluttered cell without collisions.

## Next steps

- [Motion planning](/motion-planning/): how the motion service plans
  collision-free paths and what `WorldState` contains.
- [Frame system](/motion-planning/frame-system/): how frames position each part
  of the machine and how attached geometry moves with a frame.
- [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/):
  how to give the planner the static obstacles your contact task moves among.
