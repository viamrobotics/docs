---
linkTitle: "Arm with a fixed external camera"
title: "Arm with a fixed external camera"
weight: 20
layout: "docs"
type: "docs"
description: "Configure frames for a table-mounted arm with a camera mounted separately, such as overhead or on a tripod."
aliases:
  - /motion-planning/frame-system-how-to/arm-fixed-camera/
---

An overhead or tripod-mounted camera sees the whole workspace at once. A
wrist-mounted camera sees only where the arm points. For pick-and-place
across a full bench (a bin on one side, a target area on the other), the
fixed camera is the better choice: the arm can move freely while the camera
keeps its vantage point. This guide configures frames for that arrangement:
the arm as a child of the world frame, and the camera as a separate child of
the world frame.

## Frame hierarchy

```text
world
├── my-arm
│   └── my-gripper (attached to arm)
├── my-camera (overhead or tripod-mounted)
└── table-surface
```

Unlike a wrist-mounted camera, this camera is a child of the world frame, not the arm.
The camera frame stays fixed in space when the arm moves.
`table-surface` is workspace obstacle geometry, configured separately; see [Define obstacles](/motion-planning/obstacles/).

## Steps

### 1. Choose your world frame

Pick a fixed, easy-to-measure point in your workspace.
A table corner works well for this setup because you need to measure distances to both the arm base and the camera position from the same reference point.

Mark the origin physically so you can take consistent measurements to both the arm and the camera.

### 2. Add a frame to the arm

In the **CONFIGURE** tab, click the arm component's card and then click **Frame**. (For details on the Frame editor, see [Edit a frame in the Viam app](/motion-planning/frame-system/overview/#edit-a-frame-in-the-viam-app).)

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

Click **Save** in the top-right of the page (or press ⌘/Ctrl+S).

### 3. Add a frame to the gripper

In the sidebar, click your gripper component to open its card. On the card, click **Frame**.
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

In the sidebar, click your camera component to open its card. On the card, click **Frame**.
The camera's parent is `"world"`, not the arm.

Measure the camera's position relative to your world frame origin.
Measure along all three axes: x (right), y (forward), z (up).

**Overhead camera example:**
For a camera mounted 200 mm to the right, 300 mm forward, and 800 mm above the world frame origin:

```json
{
  "parent": "world",
  "translation": { "x": 200, "y": 300, "z": 800 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": -1, "th": 0 }
  }
}
```

In an orientation vector, `(x, y, z)` is the direction the camera's +z
axis points in the parent frame, and the camera's +z axis is the lens.
An overhead camera's lens points at the floor, so set the pointing
vector to `(0, 0, -1)`: straight down at the workspace. Use `th` to
spin the camera about the lens axis if the image needs to rotate to
line up with your world axes.

**Tripod-mounted camera at an angle:**
For a camera on a tripod 500 mm to the left, 600 mm forward, and 700 mm above the origin, tilted 45 degrees downward:

```json
{
  "parent": "world",
  "translation": { "x": -500, "y": 600, "z": 700 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0.7, "y": 0, "z": -0.7, "th": 0 }
  }
}
```

Set `(x, y, z)` to the direction the lens points; Viam normalizes the
vector for you. `(0.7, 0, -0.7)` aims the lens 45 degrees below
horizontal, facing the +x direction. To aim at a different part of the
bench, change the horizontal components: for example,
`(0.5, -0.5, -0.7)` faces between +x and -y.

Click **Save**.

### 5. Verify axes on the arm and on the camera

For the arm, jog in **CONTROL** along +x, +y, +z and watch the physical
direction. For the camera, open the camera stream in **CONTROL** and move a
known object (a pen, a ruler) in the physical +x direction; the object should
move along one consistent axis in the camera's image. If it moves along the
wrong image axis or in the wrong direction, adjust `th` (which spins the
image about the lens axis) or the pointing vector until image motion matches
physical motion.

### 6. Visualize the frame system

1. Navigate to the **3D SCENE** tab in the Viam app.
2. Verify that the arm and camera frames appear as separate branches from the world frame.
3. Confirm that the camera frame stays fixed when the arm moves.
4. Check that the positions and orientations match your physical workspace.

### 7. Verify with TransformPose

Use `TransformPose` to verify the relationship between the camera and arm frames.
Place an object at a known position visible to the camera, then transform that position from the camera frame to the world frame.
The result should match the object's measured position in the workspace.

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/overview/#transformpose).

## Troubleshooting

{{< expand "Camera frame moves when the arm moves" >}}

The camera's `parent` field is set to the arm instead of `"world"`.
Change the parent to `"world"` so the camera frame remains fixed in space.

{{< /expand >}}

{{< expand "Overhead camera orientation looks wrong in the visualizer" >}}

For a camera pointing straight down, set the pointing vector to `(0, 0, -1)`: `"value": { "x": 0, "y": 0, "z": -1, "th": 0 }`.
In an orientation vector, `(x, y, z)` is the direction the lens points, so point it wherever the lens actually aims.
If the image appears rotated in the visualizer, adjust `th`, which spins the camera about the lens axis.

{{< /expand >}}

{{< expand "Transformed coordinates are consistently offset" >}}

Double-check your physical measurements from the world frame origin to the camera.
Small measurement errors accumulate, so measure carefully.
If you are using a table corner as the world frame, make sure you are measuring from the same corner consistently.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/frame-system/camera-calibration/" noimage="true" %}}
{{< /cards >}}
