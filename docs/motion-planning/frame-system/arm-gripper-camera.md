---
linkTitle: "Arm with gripper and wrist camera"
title: "Arm with gripper and wrist camera"
weight: 10
layout: "docs"
type: "docs"
description: "Configure frames for a table-mounted arm with an attached gripper and wrist-mounted camera."
aliases:
  - /motion-planning/frame-system-how-to/arm-gripper-camera/
---

A table-mounted arm, a gripper bolted to the end effector, and a camera
clamped near the wrist is the most common manipulation setup. The camera moves
with the arm, so its view is always centered on wherever the arm is reaching.
The motion service and vision pipelines do not know that on their own; you
have to declare three frame relationships: arm-to-world, gripper-to-arm, and
camera-to-arm. This guide walks through all three.

## Frame hierarchy

```text
world
├── my-arm
│   ├── my-gripper (attached to arm)
│   └── my-camera (mounted on arm)
└── table-surface
```

The arm is a direct child of the world frame.
The gripper and camera are both children of the arm, so they move with the arm automatically as it changes position.

## Steps

### 1. Choose your world frame origin

Pick either the arm's base or a corner of the table as your world frame
origin, then mark that point physically. The trade-off: using the arm
base means the arm's translation is `(0, 0, 0)` and every measurement
starts from the arm. Using a table corner gives you a visible landmark
but requires measuring arm-base-to-corner first.

Every frame on the machine is defined relative to this point, so you
will refer to it every time you add or adjust a frame.

### 2. Add a frame to the arm

In the **CONFIGURE** tab, click the arm component's card and then click **Frame**. (For details on the Frame editor, see [Edit a frame in the Viam app](/motion-planning/frame-system/overview/#edit-a-frame-in-the-viam-app).)

If the arm base is your world frame origin:

```json
{
  "parent": "world",
  "translation": { "x": 0, "y": 0, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

If the world frame origin is at a table corner and the arm base is 300 mm to the right and 250 mm forward from that corner:

```json
{
  "parent": "world",
  "translation": { "x": 300, "y": 250, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Click **Save** in the top-right of the page (or press ⌘/Ctrl+S).

### 3. Verify the axes point the way you expect

Before adding more frames, confirm the arm's coordinate axes line up with your
world frame. In the **CONTROL** tab, jog the end effector a small amount in
+z. If the arm moves up, z matches the Viam convention. Repeat for +x and +y.
An axis that points the wrong way will make every subsequent frame offset
wrong in the same direction, so fix it now by rotating the arm's `orientation`
to flip the bad axis.

For example, if the arm's +x points opposite to your intended +x, rotate 180 degrees around the z axis:

```json
{
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 180 }
  }
}
```

### 4. Add a frame to the gripper

In the sidebar, click your gripper component to open its card. On the card, click **Frame**.

#### Pick where the gripper frame origin sits

A point near the center of the gripper jaws is usually the most
convenient frame origin. When you later call the motion service to move
the gripper to a target pose, whatever point you pick here is what gets
moved to that pose.

#### Configure the frame

In the JSON, set `parent` to your arm's component name, `translation` to
the gripper frame origin's offset in mm from the arm's end effector, and
`orientation` to the gripper's rotation relative to the arm.

If the gripper attaches directly to the arm's end effector with no
adapter plate and no rotation, use a zero offset:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 0, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

If the gripper is mounted through an adapter plate or flange that adds
height, set the z translation to the adapter height in millimeters. For
example, with a 50 mm adapter plate:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 0, "z": 50 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Click **Save**.

#### Check whether the gripper has a kinematics file

Some grippers ship with a kinematics file that describes the position of
the jaws as they open and close, along with collision geometry for the
jaw linkages. If the gripper has one, the motion planner already knows
the gripper's volume and you do not need to add collision geometry to
the gripper frame.

Call `GetKinematics` on the gripper (or check the module source). If
the call returns kinematics data, verify the gripper renders as expected
in the **3D SCENE** tab and you are done.

If the gripper has no kinematics file, add a `geometry` field to the
gripper's frame describing its physical volume so the planner can avoid
collisions with the gripper body. See
[Define obstacles](/motion-planning/obstacles/overview/#passive-objects-attached-to-a-component)
for the pattern.

### 5. Add a frame to the wrist camera

In the sidebar, click your camera component to open its card. On the card, click **Frame**.

The camera's parent is the arm, not the world frame.
Measure the offset from the arm's end effector to the camera's optical center.
For a camera mounted 30 mm to the side and 60 mm above the end effector:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 30, "z": 60 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

If the camera is tilted downward (for example, angled 30 degrees toward the gripper), add a rotation around the x axis:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 30, "z": 60 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 1, "y": 0, "z": 0, "th": -30 }
  }
}
```

Click **Save**.

### 6. Visualize the frame system

1. Navigate to the **3D SCENE** tab in the Viam app.
2. The viewer renders all configured frames in 3D space. Each frame appears as a set of colored axes (red = x, green = y, blue = z).
3. Verify that the gripper and camera frames are attached to the arm and move with it.
4. Check that the positions and orientations match your physical setup.

If a frame appears in the wrong position, return to the **CONFIGURE** tab and adjust the translation or orientation values.

### 7. Verify with TransformPose

Use the `TransformPose` API to confirm that the frame system computes correct transforms between frames.
Express the camera's origin `(0, 0, 0)` in the camera frame and transform it to the world frame.
The result should match the physical position of the camera.

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/overview/#transformpose).

## Troubleshooting

{{< expand "Gripper or camera frame does not move with the arm" >}}

Check that the `parent` field is set to your arm's component name (for example, `"my-arm"`), not `"world"`.
If the parent is `"world"`, the frame stays fixed in space when the arm moves.

{{< /expand >}}

{{< expand "Camera image appears rotated or flipped" >}}

The camera's orientation in the frame system must match its physical mounting orientation.
If the camera is mounted upside down, add a 180-degree rotation around the z axis.
If the image is mirrored, check whether you need to rotate around the x or y axis.

{{< /expand >}}

{{< expand "Gripper offset seems wrong after adding an adapter plate" >}}

Measure the adapter plate height from the arm's mounting flange to the gripper's mounting flange.
Use this measurement as the z translation.
If the adapter plate also offsets the gripper laterally, include x and y values as well.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/reference/kinematics/" noimage="true" %}}
{{< /cards >}}
