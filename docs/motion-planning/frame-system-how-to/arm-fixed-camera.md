---
linkTitle: "Arm with a fixed external camera"
title: "Arm with a fixed external camera"
weight: 20
layout: "docs"
type: "docs"
description: "Configure frames for a table-mounted arm with a camera mounted separately, such as overhead or on a tripod."
---

In this setup, the arm and camera are both positioned independently in the workspace.
The camera is mounted overhead, on a tripod, or at some other fixed location rather than on the arm itself.
This is common for vision-guided pick-and-place tasks where the camera needs to observe the entire workspace from a fixed vantage point.

## Frame hierarchy

```text
world
├── my-arm
│   └── my-gripper (attached to arm)
├── my-camera (overhead or tripod-mounted)
└── table-surface
```

The key difference from a wrist-mounted camera setup is that the camera is a child of the world frame, not the arm.
The camera frame stays fixed in space when the arm moves.

## Steps

### 1. Choose your world frame

Pick a fixed, easy-to-measure point in your workspace.
A table corner works well for this setup because you need to measure distances to both the arm base and the camera position from the same reference point.

Mark the origin physically so you can take consistent measurements to both the arm and the camera.

### 2. Add a frame to the arm

In the [Viam app](https://app.viam.com), navigate to your machine and click the **CONFIGURE** tab.
Find your arm component and click the **Frame** button.

Measure the distance from your world frame origin to the arm base along each axis.
For an arm base 300 mm to the right and 250 mm forward from a table corner:

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

Click **Save**.

### 3. Add a frame to the gripper

Find your gripper component and click the **Frame** button.
Set the parent to the arm:

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

If you have an adapter plate between the arm and gripper, set the z translation to the plate height in millimeters.

Click **Save**.

### 4. Add a frame to the fixed camera

Find your camera component and click the **Frame** button.
The camera's parent is `"world"`, not the arm.

Measure the camera's position relative to your world frame origin.
You need to measure in all three axes: left/right (x), forward/backward (y), and height (z).

**Overhead camera example:**
For a camera mounted 200 mm to the right, 300 mm forward, and 800 mm above the world frame origin:

```json
{
  "parent": "world",
  "translation": { "x": 200, "y": 300, "z": 800 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 1, "y": 0, "z": 0, "th": 180 }
  }
}
```

The orientation `(1, 0, 0), 180` rotates the camera frame 180 degrees around the x axis.
This is appropriate for an overhead camera pointing straight down, because it flips the z axis to point downward.

**Tripod-mounted camera at an angle:**
For a camera on a tripod 500 mm to the left, 600 mm forward, and 700 mm above the origin, tilted 45 degrees downward:

```json
{
  "parent": "world",
  "translation": { "x": -500, "y": 600, "z": 700 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 1, "y": 0, "z": 0, "th": -45 }
  }
}
```

A negative angle around the x axis tilts the camera's view downward from the horizontal.

Click **Save**.

### 5. Verify axis directions

Go to the **CONTROL** tab and jog the arm in small increments along each axis to confirm that +x, +y, and +z match your physical setup.
If any axis is wrong, adjust the arm's orientation in the **CONFIGURE** tab.

### 6. Visualize the frame system

1. Navigate to the **3D SCENE** tab in the Viam app.
2. Verify that the arm and camera frames appear as separate branches from the world frame.
3. Confirm that the camera frame stays fixed when the arm moves.
4. Check that the positions and orientations match your physical workspace.

### 7. Verify with TransformPose

Use `TransformPose` to verify the relationship between the camera and arm frames.
Place an object at a known position visible to the camera, then transform that position from the camera frame to the world frame.
The result should match the object's measured position in the workspace.

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/#transformpose).

## Troubleshooting

{{< expand "Camera frame moves when the arm moves" >}}

The camera's `parent` field is set to the arm instead of `"world"`.
Change the parent to `"world"` so the camera frame remains fixed in space.

{{< /expand >}}

{{< expand "Overhead camera orientation looks wrong in the visualizer" >}}

For a camera pointing straight down, the rotation should be 180 degrees around the x axis: `"value": { "x": 1, "y": 0, "z": 0, "th": 180 }`.
This flips the camera's z axis to point downward.
If the camera is rotated in the horizontal plane as well (not aligned with the x or y axis), you may need to combine rotations or use a different orientation type.

{{< /expand >}}

{{< expand "Transformed coordinates are consistently offset" >}}

Double-check your physical measurements from the world frame origin to the camera.
Small measurement errors accumulate, so measure carefully.
If you are using a table corner as the world frame, make sure you are measuring from the same corner consistently.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/move-arm-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/camera-calibration/" noimage="true" %}}
{{< /cards >}}
