---
title: "Configure your frame system"
linkTitle: "Configure your frame system"
weight: 20
type: "docs"
layout: "docs"
description: "Decide on and configure the frames of your arm, its workspace, and other components."
---

This guide will help you decide on a coordinate system for your workspace, and then determine how the frames of your arm and other components relate to that workspace.

Once you have configured frames for all your components, Viam will keep track of the positions and orientations as your robot moves, so you can plan motion in terms of a consistent coordinate system.

For reference information, see [the frame system](/operate/reference/services/frame-system/).

## Determine the world frame

The world reference frame is the fixed coordinate system that serves as the reference point for the other frames in your robotic system.

You choose the world frame, in whatever way is convenient for your application.
It generally makes sense to define the world frame's location as a point in your space that does not move and is easy to measure from.

For example, if you are using a robot arm mounted to a table, it can be convenient to decide that the world frame origin is at the base of the arm, or you can decide that the world frame origin is at one corner of the table that the arm is mounted to.

You do not explicitly configure the world frame.
You define it implicitly by configuring the frame of a component relative to world.

### Add a frame to your arm

1. Mount the arm in a fixed location.
1. On your arm's configuration card, click **+ Add frame**.
1. The card will populate with the following default values:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "x": 0,
         "y": 0,
         "z": 1,
         "th": 0
       }
     },
     "parent": "world",
     "translation": {
       "x": 0,
       "y": 0,
       "z": 0
     }
   }
   ```

   This [orientation vector](/operate/mobility/orientation-vector/) of `x=0, y=0, z=1, th=0` means the frame is aligned with the world frame, and the `0, 0, 0` translation means the arm's {{< glossary_tooltip term_id="origin-frame" text="origin frame" >}} is coincident with the origin of the world frame.
   You can think of it like this: The z-axis of the arm's origin frame is parallel to the z-axis of the world frame, and the origin of the arm's origin frame is in the same place as the origin of the world frame.

   If you want to define the world frame as the corner of the table, leave the default values for now, and continue to the next step so that you know which way `x` and `y` point and can edit the configuration accordingly.

1. Click **Save**.

   By configuring your arm's frame like this, you have now defined the world frame as the same as the arm's origin frame.

### Figure out which way the arm's axes point

The arm's origin frame is now the world frame, but you do not know which way the x, y, and z axes of the arm frame point, unless you happen to be familiar with the arm's [kinematics file](/operate/reference/kinematic-chain-config/).

1. On your arm's configuration card, click the **TEST** section (or use the **CONTROL** tab).

   {{% alert title="Caution" color="caution" %}}
   Moving the arm with the **TEST** or **CONTROL** panel sends commands using the arm API, which does not take obstacles or other components into account.
   Be careful not to hit people or objects with the arm.
   {{% /alert %}}

1. Move the arm in each direction and note which way the arm moves.
   For example, under the **MoveToPosition** section, move the arm in the positive Z direction.
   If it moves upwards, then you know that the z-axis of the arm frame points upwards.
1. If the directions do not match your intended world frame, you can edit the arm's `orientation` field to rotate the arm frame to match your intended world frame.
   For example, if the arm's x-axis points to the right, but you want it to point to the left, you can set the `orientation` field to `"x"=0, "y"=0, "z"=1, "th"=180`.

1. For your reference, we recommend you mark the X, Y, and Z axes of the world frame on your workspace with tape or a marker.

### Add a frame offset

If you want to define the world frame as the corner of the table, you can now edit the arm's frame to be offset from the world frame by the distance from the table corner to the arm's origin:

1. Measure the X and Y distance from your designated table corner to the center of the arm's origin.
1. Edit the arm's frame configuration to set the `translation` field accordingly.
   For example, if the arm's origin is 100mm in the X direction and 200mm in the Y direction from the table corner, set the `translation` field to `"x"=100, "y"=200, "z"=0`.
   If you chose not to align the arm's axes with the world axes, be sure to use the X, Y, and Z directions of the _world_ frame to set the `translation` field.
1. Click **Save**.

   The arm's origin frame is now offset from the world frame by the distance from the table corner to the arm's origin frame.

## The world frame for mobile robots

If none of your components are fixed in place, the world frame is less meaningful.
The motion service will not automatically keep track of the relationship between the robot and its environment in this case.
The relative location of the robot is tracked by the SLAM service or the navigation service, depending on which method you use.

You can set the origin frame of one of your components (such as a {{< glossary_tooltip term_id="base" text="base" >}}) to `0, 0, 0` with respect to world, and parent other component frames to that component so that the motion service can prevent collisions between components.
The SLAM and navigation services keep track of objects parented to the base, but they do not take into account objects parented to world (other than the base itself).

## Visualize components and frames

{{< readfile "/static/include/snippet/visualize.md" >}}
