---
linkTitle: "CLI commands"
title: "Motion CLI commands reference"
weight: 45
layout: "docs"
type: "docs"
description: "Reference for the Viam CLI commands that inspect the frame system and test motion from the command line."
---

`viam machines part motion` exposes four commands that wrap the frame system and motion service RPCs. Use them to inspect frame configuration and test motion from the command line, without writing code.

All three read commands (`print-status`, `get-pose`, and the pose read inside `set-pose`) go through the deprecated `Motion.GetPose` RPC. The CLI output is unchanged; the RPC will switch to the robot service's `GetPose` in a future release.

All four commands require a `--part` flag that identifies the machine part. `get-pose` and `set-pose` additionally require `--component`.

## Command summary

| Command        | Purpose                                                               |     Blocks?      |
| -------------- | --------------------------------------------------------------------- | :--------------: |
| `print-config` | Print the frame system configuration returned by `FrameSystemConfig`. |        No        |
| `print-status` | Print the world-frame pose of every frame part.                       |        No        |
| `get-pose`     | Print the world-frame pose of a specific component.                   |        No        |
| `set-pose`     | Move a component to a target pose by overriding selected fields.      | Yes (calls Move) |

## print-config

Prints the machine's frame system configuration.

```sh
viam machines part motion print-config --part "my-machine-main"
```

Output shows every configured frame part: its name, parent, translation,
orientation, and geometry (if any). This is the same information
returned by the `FrameSystemConfig` RPC on the robot service.

Use this to:

- Verify your JSON frame config parses and produces the frame tree you
  expect.
- Compare configured values against physical measurements.
- List the exact frame names you might reference in
  [`CollisionSpecification`](/motion-planning/obstacles/allow-frame-collisions/)
  or `supplemental_transforms`.

### Flags

| Flag     | Required | Description                |
| -------- | :------: | -------------------------- |
| `--part` |   Yes    | The machine part to query. |

## print-status

For every frame part configured on the machine, prints the current pose
in the world frame.

```sh
viam machines part motion print-status --part "my-machine-main"
```

Each line shows the frame's name followed by X, Y, Z position (mm) and
OX, OY, OZ, Theta orientation vector components (degrees). The ordering
matches the frame tree. Live component poses (such as arm end-effector
positions) reflect the current joint state.

Use this to:

- Read the live world-frame pose of every part in one output.
- Compare "where the frame system says X is" against the physical
  location of X.
- Sanity-check frame configuration after making changes.

### Flags

| Flag     | Required | Description                |
| -------- | :------: | -------------------------- |
| `--part` |   Yes    | The machine part to query. |

## get-pose

Prints the current world-frame pose of a single specified component.

```sh
viam machines part motion get-pose \
    --part "my-machine-main" \
    --component "my-arm"
```

The output format is the same single-frame pose line as `print-status`.

Use this when you want one component's pose without the full frame
tree listing.

### Flags

| Flag          | Required | Description                        |
| ------------- | :------: | ---------------------------------- |
| `--part`      |   Yes    | The machine part to query.         |
| `--component` |   Yes    | The component whose pose to print. |

## set-pose

`set-pose` reads the component's current pose, overrides the fields you pass as flags, and calls `Motion.Move` to the resulting pose. Unset flags keep the current value.

```sh
viam machines part motion set-pose \
    --part "my-machine-main" \
    --component "my-arm" \
    --x 300 --y 200 --z 400
```

In this example, the arm moves to the pose `(300, 200, 400)` in world
coordinates while keeping its current orientation (OX, OY, OZ, Theta
are unchanged).

You can override any subset of fields. To change only the orientation:

```sh
viam machines part motion set-pose \
    --part "my-machine-main" \
    --component "my-arm" \
    --ox 0 --oy 0 --oz -1 --theta 0
```

This drives the arm to face straight down while keeping its current XYZ
position.

### Flags

| Flag          | Required | Description                              |
| ------------- | :------: | ---------------------------------------- |
| `--part`      |   Yes    | The machine part to move.                |
| `--component` |   Yes    | The component to move.                   |
| `--x`         |    No    | Override X position (mm in world frame). |
| `--y`         |    No    | Override Y position (mm in world frame). |
| `--z`         |    No    | Override Z position (mm in world frame). |
| `--ox`        |    No    | Override orientation vector X component. |
| `--oy`        |    No    | Override orientation vector Y component. |
| `--oz`        |    No    | Override orientation vector Z component. |
| `--theta`     |    No    | Override orientation theta (degrees).    |

## Common flows

- **Verify your frame config parses and mounts where you expect**:
  run `print-config`, compare parent/translation values against your
  JSON config and physical measurements.
- **Confirm the arm is where the frame system thinks it is**: run
  `print-status`, move the arm physically by a known amount, run
  `print-status` again.
- **Quick reachability test**: run `get-pose` to read the current pose, then run `set-pose` with a small offset to confirm the motion service can drive the arm. Start with small offsets; large ones risk collisions.

For a step-by-step debugging workflow using these commands, see
[Debug motion with the CLI](/motion-planning/debug-motion-with-cli/).

## What's next

- [Debug motion with the CLI](/motion-planning/debug-motion-with-cli/):
  step-by-step debugging using these commands.
- [Frame system](/motion-planning/frame-system/): the concept the CLI
  inspects.
- [Motion service API](/motion-planning/reference/api/): the
  programmatic equivalents.
