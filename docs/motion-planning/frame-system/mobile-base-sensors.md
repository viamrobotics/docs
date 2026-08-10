---
linkTitle: "Mobile base with sensors"
title: "Mobile base with sensors"
weight: 30
layout: "docs"
type: "docs"
description: "Configure frames for a mobile base with mounted cameras and lidar sensors."
aliases:
  - /motion-planning/frame-system-how-to/mobile-base-sensors/
---

A lidar point at `(2.0 m, 0, 0)` is two meters in front of the _lidar_,
not two meters in front of the base. Every sensor reports positions in
its own reference frame. The frame system converts each sensor's
readings to the base frame and on to the world frame, so object
detections, mapping data, and camera images line up with each other.
This guide configures frames for a base with a lidar and two cameras.

## Frame hierarchy

```text
world
└── my-base
    ├── my-lidar (mounted on top)
    ├── front-camera (front-facing)
    └── rear-camera (rear-facing)
```

The base is a child of the world frame.
All sensors are children of the base, so the entire sensor subtree moves with the base.

## Steps

### 1. Choose your world frame origin

For a mobile base, configure the base with zero translation so the
world frame origin sits at the base center. Sensor positions are
measured relative to the base center, so you do not need to mark
anything physically. The frame system holds these configured
relationships; tracking the base's position as it drives is the job of
SLAM or a movement sensor, not the frame system.

### 2. Add a frame to the base

In the **CONFIGURE** tab, click the base component's card and then click **Frame**. (For details on the Frame editor, see [Edit a frame in the Viam app](/motion-planning/frame-system/overview/#edit-a-frame-in-the-viam-app).) Edit the JSON for each component below as you go.

Since the world frame origin is at the base center, the translation is zero:

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

### 3. Add a frame to the lidar

In the sidebar, click your lidar component to open its card. On the card, click **Frame**.
Measure the offset from the center of the base to the lidar's sensor origin.

For a lidar mounted on top of the base, centered horizontally and 150 mm above the base center:

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

If the lidar is offset forward or to one side, include x and y values.
For example, a lidar mounted 50 mm forward of center and 150 mm above:

```json
{
  "parent": "my-base",
  "translation": { "x": 0, "y": 50, "z": 150 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Click **Save**.

### 4. Add frames to the cameras

For each camera, click the component in the sidebar to open its card, then click **Frame**.
Measure the offset from the base center to each camera's mounting position.

**Front-facing camera:**
For a camera mounted at the front of the base, 200 mm forward and 120 mm above the base center:

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

In an orientation vector, `(x, y, z)` is the direction the camera's +z
axis (the lens) points. A base's forward direction is +y, so `(0, 1, 0)`
faces the camera forward; the identity orientation `(0, 0, 1)` would aim
the lens at the ceiling. If the image appears rotated, adjust `th`,
which spins the camera about the lens axis.

**Rear-facing camera:**

The rear camera's configuration mirrors the front camera's, with two changes:
a negative y translation (it is behind the base center) and a pointing
vector aimed backward.

For a camera mounted at the back of the base, 200 mm backward and 120 mm above the base center, facing backward:

```json
{
  "parent": "my-base",
  "translation": { "x": 0, "y": -200, "z": 120 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": -1, "z": 0, "th": 0 }
  }
}
```

`(0, -1, 0)` points the lens backward, along -y.

Click **Save** after adding each camera frame.

### 5. Visualize and verify

1. Navigate to the **3D SCENE** tab in the Viam app.
2. Verify that all sensor frames appear as children of the base.
3. Check that sensor positions match their physical mounting locations relative to the base center.
4. Confirm that camera orientations point in the correct directions (forward for the front camera, backward for the rear camera).

If any frame appears in the wrong position or orientation, return to the **CONFIGURE** tab and adjust the values.

### 6. Verify with TransformPose

Use `TransformPose` to confirm the relationships between sensor frames and the base frame.
For example, transform the front camera's origin `(0, 0, 0)` from the camera frame to the base frame.
The result should match the camera's measured offset from the base center.

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/overview/#transformpose).

## Troubleshooting

{{< expand "Lidar data does not align with camera data" >}}

Check that both the lidar and camera frames have the correct translation offsets from the base.
Even small errors in the offsets can cause the two data sources to disagree about object positions.
Verify by placing an object at a known distance and checking that both sensors report consistent positions after frame transformation.

{{< /expand >}}

{{< expand "Front and rear camera frames overlap in the visualizer" >}}

Make sure the y translations have opposite signs. A base's forward direction is +y, so the front camera has a positive y offset and the rear camera a negative y offset.
Also verify that the rear camera's pointing vector is `(0, -1, 0)` so it faces backward.

{{< /expand >}}

{{< expand "A sensor frame sits at the world origin instead of on the base" >}}

Confirm that the sensor's `parent` field is set to the base component name (for example, `"my-base"`), not `"world"`.
A frame parented to `"world"` ignores the base entirely, and its readings no longer transform through the base frame.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/frame-system/mobile-base-arm/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{< /cards >}}
