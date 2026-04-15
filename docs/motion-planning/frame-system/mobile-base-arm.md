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

This setup combines a mobile base with a mounted arm, gripper, and sensors.
The arm is a child of the base, so the entire arm subtree (including the gripper and any wrist-mounted camera) moves with the base as it navigates.
Navigation sensors like a front camera and LIDAR are also mounted on the base.

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

The base is a child of the world frame.
The arm is a child of the base, and the gripper and wrist camera are children of the arm.
Navigation sensors are children of the base.
When the base moves, every frame in the tree moves with it.
When the arm moves, only the arm, gripper, and wrist camera frames update.

## Steps

### 1. Choose your world frame

For a mobile base, the world frame origin is typically the center of the base.
All component positions are defined relative to this center point.

### 2. Add a frame to the base

In the [Viam app](https://app.viam.com), navigate to your machine and click the **CONFIGURE** tab.
Find your base component and click the **Frame** button.

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

Click **Save**.

### 3. Add a frame to the arm

Find your arm component and click the **Frame** button.
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

**Gripper** (attached directly to the end effector):

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

**Wrist camera** (mounted on the arm, offset from the end effector):

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

**Front-facing navigation camera:**

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

**LIDAR mounted on top of the base:**

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

1. Navigate to the **3D SCENE** tab in the Viam app.
2. Verify that the arm, gripper, and wrist camera form a subtree under the base.
3. Verify that navigation sensors are direct children of the base.
4. Jog the arm using the **CONTROL** tab and confirm that only the arm subtree (arm, gripper, wrist camera) updates, while the base and navigation sensors stay in place.
5. Check that all positions and orientations match your physical setup.

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

This is expected behavior. When the base rotates, the arm's position in the world frame changes because the arm is mounted on the base.
If the shift seems incorrect, check the arm's translation offset from the base.
An arm mounted off-center will trace a larger arc when the base rotates.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/reference/kinematics/" noimage="true" %}}
{{< /cards >}}
