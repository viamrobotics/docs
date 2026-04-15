---
linkTitle: "Orientation vectors"
title: "Orientation vector reference"
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

When you specify a pose in Viam (in frame system configuration, a motion planning destination, or any other `Pose` payload), the orientation is expressed as one of five rotation formats. This page lists those formats, their schemas, common orientations, and validation rules.

## Supported orientation formats

Viam supports five orientation formats, specified with the `type` field in
orientation configuration:

### `ov_degrees` (default)

The orientation vector format (axis plus angle in degrees). Use this for most configurations; the other formats exist to interoperate with Euler, axis-angle, or quaternion inputs.

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

Rotation axis plus angle in radians, using the R4AA (Rotation 4 Axis Angle) representation. Choose `axis_angles` when your input already comes from an R4AA source; otherwise `ov_radians` is equivalent and more common in Viam configs.

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

| Description                         | `ov_degrees` value                    |
| ----------------------------------- | ------------------------------------- |
| No rotation (identity)              | `{"x": 0, "y": 0, "z": 1, "th": 0}`   |
| 90 degrees around z                 | `{"x": 0, "y": 0, "z": 1, "th": 90}`  |
| 180 degrees around z (flip x and y) | `{"x": 0, "y": 0, "z": 1, "th": 180}` |
| 90 degrees around x                 | `{"x": 1, "y": 0, "z": 0, "th": 90}`  |
| Pointing straight down (-z)         | `{"x": 0, "y": 0, "z": -1, "th": 0}`  |
| 30 degree tilt around y             | `{"x": 0, "y": 1, "z": 0, "th": 30}`  |

## Gimbal lock

When using `euler_angles`, certain pitch values (near +/- 90 degrees or pi/2
radians) cause gimbal lock, where roll and yaw become ambiguous. If you need
orientations near these values, use `ov_degrees`, `axis_angles`, or `quaternion`
instead. These formats do not suffer from gimbal lock.

## Validation

For `ov_degrees` and `ov_radians`, the axis `(x, y, z)` must have a non-zero magnitude. Passing an all-zero axis returns the error `has a normal of 0, probably X, Y, and Z are all 0`.

For `axis_angles`, a zero-norm axis causes a panic during normalization. Always
provide a non-zero axis vector.

For `quaternion`, values are auto-normalized, so any non-zero quaternion is
valid.
