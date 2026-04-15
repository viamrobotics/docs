---
linkTitle: "Mobile base with sensors"
title: "Mobile base with sensors"
weight: 30
layout: "docs"
type: "docs"
description: "Configure frames for a mobile base with mounted cameras and LIDAR sensors."
aliases:
  - /motion-planning/frame-system-how-to/mobile-base-sensors/
---

A mobile base only knows where it is to the extent its sensors report. Lidar
sweeps tell the base what is around it; front and rear cameras feed detection
and SLAM. Every one of those sensor readings is in the sensor's own reference
frame: a lidar point at `(2.0 m, 0, 0)` is two meters in front of the lidar,
not in front of the base. The frame system is what converts sensor frames to
the base frame and on to the world frame, so the navigation stack sees
consistent positions. Configuring it correctly is a one-time setup; this
guide walks through it.

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

For a mobile base, the world frame origin is the center of the base itself at
machine start. Because the base moves through the environment, the world
frame origin is not a fixed physical location; it is wherever the base was
when it came online. Sensor positions are all measured relative to the base
center, not relative to a point in the room, so you do not need to mark
anything physically. The frame system tracks the base's motion from that
initial origin.

### 2. Add a frame to the base

In the [Viam app](https://app.viam.com), navigate to your machine and click the **CONFIGURE** tab.
In the sidebar, click your base component to open its card. On the card, click **Frame**.

The Frame section opens a JSON editor (no form, parent dropdown, or geometry-type picker). Edit the JSON directly for each component below.

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

### 3. Add a frame to the LIDAR

In the sidebar, click your LIDAR component to open its card. On the card, click **Frame**.
Measure the offset from the center of the base to the LIDAR's sensor origin.

For a LIDAR mounted on top of the base, centered horizontally and 150 mm above the base center:

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

If the LIDAR is offset forward or to one side, include x and y values.
For example, a LIDAR mounted 50 mm forward of center and 150 mm above:

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
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

The default orientation has the camera looking along the +y axis (forward).
If your camera's optical axis does not align with the base's forward direction, adjust the orientation accordingly.

**Rear-facing camera:**

The rear camera's configuration mirrors the front camera's, with two changes:
a negative y translation (it is behind the base center) and a 180-degree
rotation around z (so it faces backward).

For a camera mounted at the back of the base, 200 mm backward and 120 mm above the base center, facing backward:

```json
{
  "parent": "my-base",
  "translation": { "x": 0, "y": -200, "z": 120 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 180 }
  }
}
```

The 180-degree rotation around the z axis points the camera backward (along -y).

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

For details on the TransformPose API, see [Frame system: TransformPose](/motion-planning/frame-system/#transformpose).

## Troubleshooting

{{< expand "LIDAR data does not align with camera data" >}}

Check that both the LIDAR and camera frames have the correct translation offsets from the base.
Even small errors in the offsets can cause the two data sources to disagree about object positions.
Verify by placing an object at a known distance and checking that both sensors report consistent positions after frame transformation.

{{< /expand >}}

{{< expand "Front and rear camera frames overlap in the visualizer" >}}

Make sure the y translations have opposite signs. The front camera should have a positive y offset and the rear camera a negative y offset (or vice versa, depending on your axis convention).
Also verify that the rear camera has a 180-degree rotation to face backward.

{{< /expand >}}

{{< expand "Sensor frames are not updating as the base moves" >}}

Confirm that each sensor's `parent` field is set to the base component name (for example, `"my-base"`), not `"world"`.
Frames parented to the world stay fixed in space.

{{< /expand >}}

## What's next

{{< cards >}}
{{% card link="/motion-planning/frame-system/mobile-base-arm/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{< /cards >}}
