---
title: "Configure your frame system"
linkTitle: "Configure your frame system"
weight: 20
type: "docs"
layout: "docs"
description: "Decide on and configure the frames of your arm, its workspace, and other components."
---

Frames can be confusing.
This guide will help you decide on a coordinate system for your workspace, and then determine how the [frames](/operate/reference/services/frame-system/) of your arm and other components relate to that workspace.

Once you have configured frames for all your components, Viam will keep track of the positions and orientations as your robot moves, so you can plan motion in terms of a consistent coordinate system.

## Determine the world frame

The world reference frame is the fixed coordinate system that serves as the reference point for the other frames in your robotic system.

You define the world frame.
You can define it however is convenient for your application.

For example, if you are using a robot arm mounted in a fixed location, it can be convenient to define the arm's base frame as equal to the world frame:

1. Mount the arm in a fixed location.
1. On your arm's configuration card, click **+ Add frame**.
1. The card will populate with the following default values:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": 0,
         "x": 0,
         "y": 0,
         "z": 1
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

   This [orientation vector](/operate/mobility/orientation-vector/) of `x=0, y=0, z=1, th=0` means the frame is aligned with the world frame, and the `0, 0, 0` translation means the origin of the arm frame is coincident with the origin of the world frame.
   You can think of it like this: The z-axis of the arm frame is parallel to the z-axis of the world frame, and the origin of the arm frame is in the same place as the origin of the world frame.

1. Click **Save**.

   By configuring your arm's frame like this, _you have now defined the world frame as the same as the arm's base frame_.

### Figure out which way the world frame's axes point

The arm's base frame is now the world frame, but you do not know which way the x, y, and z axes of the arm (or world)frame point, unless you happen to be familiar with the arm's [kinematics file](/operate/reference/kinematic-chain-config/).

1. On your arm's configuration card, click the **TEST** section (or use the **CONTROL** tab).

1. Move the arm in each direction and note which way the arm moves.
   For example, under the **MoveToPosition** section, move the arm in the positive Z direction.
   If it moves upwards, then you know that the z-axis of the arm frame (and world frame) points upwards.
1. Tip: Mark the X, Y, and Z axes of the arm frame on your workspace with tape or a marker.

## Other setups

If your arm is mounted on a mobile {{< glossary_tooltip term_id="base" text="base" >}}, with a fixed camera overhead, it could make sense to define the world frame as the frame of the camera.

If none of your components are fixed in place, you can define the world frame as the frame of the first component you add to your robot, for example, the mobile base.
