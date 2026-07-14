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

In machine JSON configuration (frame definitions and world state files), you choose one of five orientation formats with the `type` field. API `Pose` messages always express orientation as an orientation vector in degrees (`o_x`, `o_y`, `o_z`, `theta`); there is no format field to choose. The format you pick in configuration affects validation and singularity behavior. The sections below cover the five supported formats, their schemas, common orientations, and validation rules.

Viam's default format, the orientation vector (OV), is structured similarly
to the
[axis-angle representation](https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation)
but interpreted differently: `(x, y, z)` is the unit vector along which the
component points (for an arm, the direction the end effector points from the
origin), and `th` is the rotation around that pointing direction. The
pointing direction and the rotation axis coincide.

## Supported orientation formats

Viam supports five orientation formats, specified with the `type` field in
orientation configuration:

### `ov_degrees` (default)

The orientation vector format: a pointing direction plus a spin in degrees. Use this for most configurations; the other formats exist to interoperate with Euler, axis-angle, or quaternion inputs.

```json
{
  "type": "ov_degrees",
  "value": { "x": 0, "y": 0, "z": 1, "th": 90 }
}
```

- `x`, `y`, `z`: the direction the component's +z axis points, as a point
  on the unit sphere (must be non-zero; normalized internally)
- `th`: rotation in degrees around that same pointing direction. Values
  wrap every 360 degrees, so `th: 370` and `th: 10` describe the same
  orientation.

Default (identity): `{"x": 0, "y": 0, "z": 1, "th": 0}`. This points the component along +z with no spin, which is no rotation.

The pointing vector must be non-zero. `(x, y, z) = (0, 0, 0)` is a
singularity: the pointing direction is undefined and validation rejects it.

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

Rotation axis plus angle in radians, using the R4 axis-angle representation. Choose `axis_angles` when your input is a true axis-angle rotation. The value keys match an orientation vector's, but the meaning differs: here `(x, y, z)` is the axis to rotate around, while in `ov_radians` it is the direction the component points.

```json
{
  "type": "axis_angles",
  "value": { "x": 0, "y": 0, "z": 1, "th": 1.5708 }
}
```

- `x`, `y`, `z`: components of the rotation axis (normalized to unit sphere)
- `th`: rotation angle in radians

Default: `{"x": 0, "y": 0, "z": 1, "th": 0}`.

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

| Description                                   | `ov_degrees` value                        |
| --------------------------------------------- | ----------------------------------------- |
| No rotation (identity)                        | `{"x": 0, "y": 0, "z": 1, "th": 0}`       |
| Pointing up, spun 90 degrees                  | `{"x": 0, "y": 0, "z": 1, "th": 90}`      |
| Pointing up, spun 180 degrees (flips x and y) | `{"x": 0, "y": 0, "z": 1, "th": 180}`     |
| Pointing horizontally along +x                | `{"x": 1, "y": 0, "z": 0, "th": 0}`       |
| Pointing straight down (-z)                   | `{"x": 0, "y": 0, "z": -1, "th": 0}`      |
| Tilted 30 degrees from vertical toward +x     | `{"x": 0.5, "y": 0, "z": 0.866, "th": 0}` |

## Gimbal lock

When using `euler_angles`, certain pitch values (near +/- 90 degrees or pi/2
radians) cause gimbal lock, where roll and yaw become ambiguous. `quaternion`
and `axis_angles` represent every orientation without this singularity.

An orientation vector has one discontinuity of its own: when the component
points exactly along +z or -z, `th` behaves like a gimbal-locked Euler angle,
and orientations near straight up or straight down can produce large jumps in
`th`. If you need smooth behavior near those poles, use `quaternion`.

## Validation

For `ov_degrees` and `ov_radians`, the axis `(x, y, z)` must have a non-zero magnitude. Passing an all-zero axis returns the error `has a normal of 0, probably X, Y, and Z are all 0`.

For `axis_angles`, a zero-norm axis causes a panic during normalization. Always
provide a non-zero axis vector.

For `quaternion`, values are auto-normalized, so any non-zero quaternion is
valid.
