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

A mobile manipulator, a base with an arm on top, has two distinct kinds of
motion: the base moves through the environment, and the arm moves within
reach of the base. The frame system represents this correctly by parenting
the arm to the base rather than to the world. Every arm-attached component
(the gripper, a wrist camera) then inherits the base's motion, while
navigation sensors mounted directly on the base form a parallel subtree.
This guide builds the full hierarchy: world to base to (arm to (gripper,
wrist camera), navigation sensors).

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

The hierarchy reflects what physically moves with what. The base's parent is
the world, so when the base drives, every frame below it shifts with it. The
arm's parent is the base, so arm motion moves the gripper and wrist camera
but not the navigation sensors. This separation keeps the lidar's reading
about the floor consistent while the arm reaches for something.

## Steps

### 1. Choose your world frame

For a mobile base, the world frame origin is typically the center of the base.
All component positions are defined relative to this center point.

### 2. Add a frame to the base

In the [Viam app](https://app.viam.com), navigate to your machine and click the **CONFIGURE** tab.
In the sidebar, click your base component to open its card. On the card, click **Frame**.

The Frame section opens a JSON editor (no form, parent dropdown, or geometry-type picker). Edit the JSON directly for each component below.

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
If the camera is tilted, add a rotation. For example, tilted 30 degrees downward:

```json
{
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 1, "y": 0, "z": 0, "th": -30 }
  }
}
```

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
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

**LIDAR mounted on top of the base.** In the sidebar, click your LIDAR component to open its card, then click **Frame**:

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
3. Jog the arm from the **CONTROL** tab. The arm subtree should move; the base and navigation sensors should not. This is the single clearest test that the hierarchy is correct.
4. Drive the base a short distance. Every frame should shift together.
5. Measure a known physical offset (base center to lidar, for example) and compare to the translation values in your config.

### 7. Verify with TransformPose

Use `TransformPose` to verify the full chain of transforms.
For example, transform the wrist camera's origin from the camera frame to the world frame.
The result should account for the base-to-arm offset, the arm's current joint positions, and the arm-to-camera offset.

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/#transformpose).

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

These cameras have different parents (base and arm respectively), so their raw coordinates are in different reference frames.
Always use `TransformPose` to convert positions to a common frame (such as the world frame) before comparing them.
Also verify that each camera's translation and orientation offsets are accurate.

{{< /expand >}}

{{< expand "Arm subtree shifts unexpectedly when base rotates" >}}

This is expected. When the base rotates in place, anything mounted off-center
sweeps through an arc; the further off-center, the longer the arc. An arm
mounted forward of the base's rotation center will end up 100 mm to the side
after a 90-degree base turn if it is 100 mm forward of center. If the shift
does not match that geometry, the arm's `translation` offset from the base is
probably wrong; measure from the base's rotation center (usually the wheel
axis midpoint) rather than from a corner of the base chassis.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/reference/kinematics/" noimage="true" %}}
{{< /cards >}}
