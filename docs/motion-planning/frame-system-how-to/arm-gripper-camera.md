---
linkTitle: "Arm with Gripper and Wrist Camera"
title: "Arm with Gripper and Wrist Camera"
weight: 10
layout: "docs"
type: "docs"
description: "Configure frames for a table-mounted arm with an attached gripper and wrist-mounted camera."
---

This is the most common manipulation setup: a table-mounted arm with a gripper on the end effector and a camera mounted on the arm near the gripper.
The camera moves with the arm, giving you a consistent view of whatever the arm is reaching for.
This guide walks you through configuring the frame system for this hardware arrangement.

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

### 1. Choose your world frame

Pick a fixed point in your workspace that is easy to measure from.
For a table-mounted arm, the arm base or a table corner are good choices.

If you choose the arm base as the world frame origin, the arm's translation offset will be `(0, 0, 0)`.
If you choose a table corner, you will need to measure the distance from that corner to the arm base.

Mark your chosen origin physically so you can take consistent measurements.

### 2. Add a frame to the arm

In the [Viam app](https://app.viam.com), navigate to your machine and click the **CONFIGURE** tab.
Find your arm component and click the **Frame** button.

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

Click **Save** after adding the frame.

### 3. Verify axis directions

Before adding more frames, confirm that the arm's coordinate axes match your expectations.

1. Go to the **CONTROL** tab and find your arm.
2. Use the arm's **TEST** panel to jog the end effector in small increments along each axis.
3. Command a move in the +z direction and observe which way the arm moves physically. If +z moves the arm up, the z axis matches the standard convention.
4. Repeat for +x and +y.

If an axis points the wrong way, adjust the `orientation` field in the arm's frame.
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

Find your gripper component in the **CONFIGURE** tab and click the **Frame** button.

If the gripper attaches directly to the arm's end effector with no adapter plate, use a zero offset:

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

If the gripper is mounted through an adapter plate or flange that adds height, set the z translation to the adapter height in millimeters.
For example, with a 50 mm adapter plate:

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

### 5. Add a frame to the wrist camera

Find your camera component in the **CONFIGURE** tab and click the **Frame** button.

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

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/#transformpose).

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

## What's Next

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/move-arm-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/reference/kinematics/" noimage="true" %}}
{{< /cards >}}
