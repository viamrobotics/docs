---
linkTitle: "Orientation Vectors"
title: "Orientation Vector Reference"
weight: 30
layout: "docs"
type: "docs"
description: "Reference for specifying component orientation using orientation vectors and other rotation formats."
aliases:
  - /operate/mobility/orientation-vector/
  - /internals/orientation-vector/
  - /appendix/orientation-vector/
  - /operate/reference/orientation-vector/
---

Orientation vectors describe the rotation of a component's coordinate frame
relative to its parent frame. They are used in frame system configuration,
motion planning destinations, and pose specifications.

## Supported orientation formats

Viam supports five orientation formats, specified via the `type` field in
orientation configuration:

### `ov_degrees` (default)

Orientation vector with angle in degrees. Most commonly used.

```json
{
  "type": "ov_degrees",
  "value": { "x": 0, "y": 0, "z": 1, "th": 90 }
}
```

- `x`, `y`, `z`: components of the rotation axis vector (must be non-zero;
  normalized internally)
- `th`: rotation angle in degrees

Default (identity): `{"x": 0, "y": 0, "z": 1, "th": 0}`. This represents no rotation.

### `ov_radians`

Same as `ov_degrees` but with angle in radians.

```json
{
  "type": "ov_radians",
  "value": { "x": 0, "y": 0, "z": 1, "th": 1.5708 }
}
```

### `euler_angles`

Rotation around the x, y, and z axes. Values are in **radians**.

```json
{
  "type": "euler_angles",
  "value": { "roll": 0, "pitch": 0, "yaw": 1.5708 }
}
```

- `roll`: rotation around x axis (radians)
- `pitch`: rotation around y axis (radians)
- `yaw`: rotation around z axis (radians)

Default: `{"roll": 0, "pitch": 0, "yaw": 0}`.

### `axis_angles`

Rotation axis with angle in **radians**. Similar to `ov_radians` but uses the
R4AA (Rotation 4 Axis Angle) representation.

```json
{
  "type": "axis_angles",
  "value": { "x": 0, "y": 0, "z": 1, "th": 1.5708 }
}
```

- `x`, `y`, `z`: components of the rotation axis (normalized to unit sphere)
- `th`: rotation angle in radians

Default: `{"x": 0, "y": 0, "z": 1, "th": 0}`.

The axis must have a non-zero norm. A zero-norm axis causes a runtime error.

### `quaternion`

Unit quaternion. Values are auto-normalized.

```json
{
  "type": "quaternion",
  "value": { "w": 0.707, "x": 0, "y": 0, "z": 0.707 }
}
```

- `w`: scalar (real) component
- `x`, `y`, `z`: vector (imaginary) components

## Common orientations

| Description | `ov_degrees` value |
|-------------|-------------------|
| No rotation (identity) | `{"x": 0, "y": 0, "z": 1, "th": 0}` |
| 90 degrees around z | `{"x": 0, "y": 0, "z": 1, "th": 90}` |
| 180 degrees around z (flip x and y) | `{"x": 0, "y": 0, "z": 1, "th": 180}` |
| 90 degrees around x | `{"x": 1, "y": 0, "z": 0, "th": 90}` |
| Pointing straight down (-z) | `{"x": 0, "y": 0, "z": -1, "th": 0}` |
| 30 degree tilt around y | `{"x": 0, "y": 1, "z": 0, "th": 30}` |

## Gimbal lock

When using `euler_angles`, certain pitch values (near +/- 90 degrees or pi/2
radians) cause gimbal lock, where roll and yaw become ambiguous. If you need
orientations near these values, use `ov_degrees`, `axis_angles`, or `quaternion`
instead. These formats do not suffer from gimbal lock.

## Validation

For `ov_degrees` and `ov_radians`, the orientation vector `(x, y, z)` must have
a non-zero magnitude. If all three components are zero, the code returns an
error: *"has a normal of 0, probably X, Y, and Z are all 0"*.

For `axis_angles`, a zero-norm axis causes a panic during normalization. Always
provide a non-zero axis vector.

For `quaternion`, values are auto-normalized, so any non-zero quaternion is
valid.
