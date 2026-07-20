---
linkTitle: "Mobile base with arm"
title: "Mobile base with arm"
weight: 40
layout: "docs"
type: "docs"
description: "Configure frames for a mobile base with a mounted arm, gripper, and sensors."
aliases:
  - /motion-planning/frame-system-how-to/mobile-base-arm/
---

A mobile manipulator is a base with an arm on top. It has two distinct
kinds of motion: the base moves through the environment, and the arm
moves within reach of the base. The frame system represents this by
parenting the arm to the base rather than to the world. Every
arm-attached component (the gripper, a wrist camera) then inherits the
base's motion, while navigation sensors mounted directly on the base
form a parallel subtree. This guide builds that full hierarchy.

## Frame hierarchy

```text
world
└── my-base
    ├── my-arm (mounted on base)
    │   ├── my-gripper
    │   └── wrist-camera
    ├── nav-camera (front-facing)
    └── my-lidar
```

The hierarchy reflects what physically moves with what. The arm's parent is
the base, so arm motion moves the gripper and wrist camera but not the
navigation sensors. This separation keeps lidar readings fixed to the base
while the arm reaches for something.

## Steps

### 1. Choose your world frame

For a mobile base, configure the base with zero translation so the
world frame origin sits at the base center. The frame system holds this
configured relationship; tracking the base's actual position as it
drives is the job of SLAM or a movement sensor, not the frame system.
All component offsets on the machine are
measured from this point.

### 2. Add a frame to the base

In the **CONFIGURE** tab, click the base component's card and then click **Frame**. (For details on the Frame editor, see [Edit a frame in the Viam app](/motion-planning/frame-system/overview/#edit-a-frame-in-the-viam-app).) Edit the JSON for each component below as you go.

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

Click **Save** in the top-right of the page (or press ⌘/Ctrl+S).

### 3. Add a frame to the arm

In the sidebar, click your arm component to open its card. On the card, click **Frame**.
The arm's parent is the base, not the world frame.

Measure the offset from the center of the base to the arm's mounting point.
For an arm mounted 100 mm forward of center and 200 mm above the base center:

```json
{
  "parent": "my-base",
  "translation": { "x": 0, "y": 100, "z": 200 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

If the arm is mounted off-center to one side, include an x offset as well.

Click **Save**.

### 4. Add frames to the gripper and wrist camera

Both the gripper and wrist camera are children of the arm.

**Gripper** (attached directly to the end effector). In the sidebar, click your gripper component to open its card, then click **Frame**:

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

If there is an adapter plate between the arm and gripper, set the z translation to the plate height.

**Wrist camera** (mounted on the arm, offset from the end effector). In the sidebar, click your wrist camera component to open its card, then click **Frame**:

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

Adjust the translation values to match the camera's actual mounting position relative to the arm's end effector.
If the camera is tilted, set `(x, y, z)` to the direction the lens points in the arm's end effector frame. For example, tilted 30 degrees from the tool axis back toward the gripper jaws:

```json
{
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": -0.5, "z": 0.87, "th": 0 }
  }
}
```

In an orientation vector, `(x, y, z)` is the direction the camera's +z axis (the lens) points; Viam normalizes the vector for you.

Click **Save** after adding each frame.

### 5. Add frames to navigation sensors

Navigation sensors are children of the base, not the arm.

**Front-facing navigation camera.** In the sidebar, click your front camera to open its card, then click **Frame**:

```json
{
  "parent": "my-base",
  "translation": { "x": 0, "y": 200, "z": 120 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 1, "z": 0, "th": 0 }
  }
}
```

Point `(x, y, z)` where the lens aims. A base's forward direction is +y,
so `(0, 1, 0)` faces the camera forward; the identity orientation
`(0, 0, 1)` would aim the lens at the ceiling.

**Lidar mounted on top of the base.** In the sidebar, click your lidar component to open its card, then click **Frame**:

```json
{
  "parent": "my-base",
  "translation": { "x": 0, "y": 0, "z": 150 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Adjust translation values to match your sensor mounting positions.

Click **Save** after adding each frame.

### 6. Visualize and verify

1. Open the **3D SCENE** tab.
2. Confirm the tree structure: arm, gripper, and wrist camera under the base; navigation sensors as direct children of the base.
3. **Jog the arm from the CONTROL tab.** This is the clearest test that your hierarchy is correct: only the arm subtree should move; the base and navigation sensors should stay put. (The visualizer shows frames parented to the base at the base's configured pose, even while the base drives.)
4. Measure a known physical offset (base center to lidar, for example) and compare to the translation values in your config.

### 7. Verify with TransformPose

Use `TransformPose` to verify the full chain of transforms.
For example, transform the wrist camera's origin from the camera frame to the world frame.
The result should account for the base-to-arm offset, the arm's current joint positions, and the arm-to-camera offset.

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/overview/#transformpose).

## Troubleshooting

{{< expand "Arm frame does not move with the base" >}}

Check that the arm's `parent` field is set to the base component name (for example, `"my-base"`), not `"world"`.
If the arm's parent is `"world"`, moving the base will leave the arm frame behind.

{{< /expand >}}

{{< expand "Gripper position is wrong after base moves" >}}

The gripper's parent should be the arm, not the base.
The chain should be: world -> base -> arm -> gripper.
If the gripper's parent is the base, its position will not account for the arm's joint positions.

{{< /expand >}}

{{< expand "Navigation camera and wrist camera report conflicting object positions" >}}

The navigation camera's parent is the base and the wrist camera's parent is the arm, so their raw coordinates are in different reference frames.
Always use `TransformPose` to convert positions to a common frame (such as the world frame) before comparing them.
Also verify that each camera's translation and orientation offsets are accurate.

{{< /expand >}}

{{< expand "Arm sits in the wrong place relative to the base in the 3D scene" >}}

The arm's `translation` offset from the base is probably measured from the
wrong point. Measure from the base's rotation center (usually the wheel axis
midpoint) rather than from a corner of the base chassis. This matters on the
physical robot too: when the base turns in place, anything mounted off the
rotation center sweeps through an arc, so an offset measured from the wrong
point puts every downstream frame in the wrong place by that same error.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/reference/kinematics/" noimage="true" %}}
{{< /cards >}}
