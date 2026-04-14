---
linkTitle: "Arm Kinematics"
title: "Arm Kinematics"
weight: 25
layout: "docs"
type: "docs"
description: "Set up the kinematic model that describes how your arm's joints and links create motion."
aliases:
  - /work-cell-layout/configure-robot-kinematics/
  - /build/work-cell-layout/configure-robot-kinematics/
---

When you command a robot arm to move its end effector to a position in 3D space,
something needs to figure out what angle each joint should be set to in order to
reach that position. This is the inverse kinematics problem, and solving it
requires a mathematical model of the arm's physical structure: how long each
link is, how each joint rotates, and what the limits of each joint are.

{{< alert title="Most arms handle this automatically" color="tip" >}}

Most arm modules in the Viam registry include a kinematics file that describes
this structure. For standard commercial arms like the UR5e, xArm6, or Viam Arm,
the module handles kinematics automatically. You do not need to provide or
configure a kinematics file for these arms.

This page is relevant if you are building a custom arm, using a module without a
built-in kinematics file, or need to verify that a kinematics model matches your
physical arm.

{{< /alert >}}

## Concepts

### Forward and inverse kinematics

**Forward kinematics** answers the question: given the current angle of every
joint, where is the end effector? This is a straightforward calculation. You
start at the base, apply each joint angle and link length in sequence, and
arrive at the end effector's position and orientation in space. Every time you
call `GetEndPosition`, the arm uses forward kinematics.

**Inverse kinematics** answers the reverse question: given a target position and
orientation for the end effector, what joint angles will get the arm there? This
is harder because there may be zero, one, or many solutions. The arm might be
able to reach the same point with the elbow up or elbow down, or it might not
be able to reach the point at all. Viam's motion planner uses inverse kinematics
internally when you call `Move`.

### Links and joints

A robot arm is modeled as a chain of rigid bodies (links) connected by joints:

- **Links** are the rigid structural segments. Each link has a length and
  optionally a geometry (for collision checking). Links do not move on their
  own. They are moved by the joints that connect them.
- **Joints** connect two links and define how they can move relative to each
  other. Viam supports four joint types:
  - **Revolute**: rotates around an axis (like an elbow or shoulder). Limits in
    degrees.
  - **Prismatic**: slides along an axis (like a linear actuator). Limits in
    millimeters.
  - **Continuous**: like revolute, but with no joint limits (full rotation).
  - **Fixed**: no degrees of freedom (used in URDF files for rigid attachments).

### Joint limits

Every joint has limits that define its range of motion:

- **Min/max angle** (revolute joints): the minimum and maximum rotation in
  degrees. For example, a shoulder joint might allow -180 to 180 degrees.
- **Min/max position** (prismatic joints): the minimum and maximum extension in
  millimeters.

Joint limits prevent the motion planner from computing solutions that would
require the arm to bend past its physical limits.

### Kinematics file formats

Viam supports two kinematics file formats at the API level:

| Format                           | Description                                   | When to use                                |
| -------------------------------- | --------------------------------------------- | ------------------------------------------ |
| **SVA** (Spatial Vector Algebra) | Viam's native JSON format                     | Preferred for new arms, most detailed      |
| **URDF**                         | XML format used by ROS and many manufacturers | When the manufacturer provides a URDF file |

The `GetKinematics` API returns one of these two formats. DH
(Denavit-Hartenberg) parameters can be written inside the SVA JSON schema as
a convenience for converting textbook DH tables into Viam's format. DH is not
a separate API-level format.

Most registry arm modules use SVA internally. You rarely need to write a
kinematics file from scratch unless you are building a custom arm.

### Tool center point (TCP)

The tool center point is the reference point on the end effector. By default,
it is at the last link's origin. If you attach a gripper or tool, you may need
to define an offset so the TCP reflects the actual point of interaction (for
example, the tip of a gripper or the center of a suction cup). This offset is
configured through the [frame system](/motion-planning/frame-system/), not the
kinematics file.

## Steps

### 1. Check if your arm has a built-in kinematics file

Most arm modules in the Viam registry ship with a kinematics file built into
the module. The module loads and applies the kinematics automatically when
`viam-server` starts.

Verify this by calling `GetKinematics`:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm

arm = Arm.from_robot(machine, "my-arm")
kinematics = await arm.get_kinematics()
print(f"Kinematics format: {kinematics[0]}")
# kinematics[1] contains the raw kinematics data
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
myArm, err := arm.FromProvider(machine, "my-arm")
if err != nil {
    logger.Fatal(err)
}

kinematicsType, kinematicsData, err := myArm.Kinematics(ctx, nil)
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Kinematics format: %v\n", kinematicsType)
fmt.Printf("Kinematics data length: %d bytes\n", len(kinematicsData))
```

{{% /tab %}}
{{< /tabs >}}

If this call succeeds and returns data, your arm module has kinematics built in.
Proceed to step 4 to read joint and end effector data.

If the call fails or returns empty data, the module does not include kinematics.
You will need to provide a kinematics file (steps 2-3).

### 2. Understand the SVA kinematics format

The SVA format describes the arm as a sequence of links and joints in JSON. Here
is a simplified example for a two-joint arm:

```json
{
  "name": "MyArm",
  "kinematic_param_type": "SVA",
  "links": [
    {
      "id": "base_link",
      "parent": "world",
      "translation": { "x": 0, "y": 0, "z": 162.5 },
      "geometry": {
        "x": 120,
        "y": 120,
        "z": 260,
        "translation": { "x": 0, "y": 0, "z": 130 }
      }
    },
    {
      "id": "upper_arm_link",
      "parent": "shoulder_pan_joint",
      "translation": { "x": 0, "y": 0, "z": 245.0 }
    }
  ],
  "joints": [
    {
      "id": "shoulder_pan_joint",
      "type": "revolute",
      "parent": "base_link",
      "axis": { "x": 0, "y": 0, "z": 1 },
      "min": -360,
      "max": 360
    },
    {
      "id": "shoulder_lift_joint",
      "type": "revolute",
      "parent": "upper_arm_link",
      "axis": { "x": 0, "y": 1, "z": 0 },
      "min": -360,
      "max": 360
    }
  ]
}
```

Each field:

- **`links[].id`**: unique name for the link
- **`links[].parent`**: the joint or frame this link attaches to
- **`links[].translation`**: offset in mm from the parent's origin
- **`links[].geometry`**: optional collision shape (uses `type`, `x`/`y`/`z` for box, `r` for sphere/capsule, `l` for capsule length)
- **`joints[].id`**: unique name for the joint
- **`joints[].type`**: `"revolute"` (rotates) or `"prismatic"` (slides)
- **`joints[].parent`**: the link this joint attaches to
- **`joints[].axis`**: the axis of rotation or translation (unit vector)
- **`joints[].min`** / **`joints[].max`**: joint limits in degrees (revolute)
  or mm (prismatic)

### 3. Import a URDF file

If your arm manufacturer provides a URDF file, you can reference it in your arm
module's configuration. URDF (Unified Robot Description Format) is an XML format
that describes links, joints, visual meshes, and collision geometry.

A typical URDF structure:

```xml
<robot name="my_arm">
  <link name="base_link">
    <visual>
      <geometry><cylinder length="0.1" radius="0.05"/></geometry>
    </visual>
    <collision>
      <geometry><cylinder length="0.1" radius="0.05"/></geometry>
    </collision>
  </link>
  <joint name="shoulder_pan" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" velocity="1.0"/>
  </joint>
</robot>
```

To use a URDF file with your arm module, place the file in a location accessible
to `viam-server` and reference it in the module's configuration. The exact
configuration depends on the module. Consult the module's documentation for the
specific attribute name.

### 4. Verify kinematics in the 3D SCENE tab

The Viam app can render a 3D visualization of your arm based on its kinematic
model:

1. Navigate to your machine in the Viam app.
2. Click the **3D SCENE** tab.
3. The arm should appear as a 3D model with joints and links.

Verify the visualization by comparing it to the physical arm:

1. Move a joint using the **CONTROL** tab.
2. Switch to the **3D SCENE** tab and confirm the visualization updated.
3. Check that the joint rotated in the correct direction and by the correct
   amount.
4. Repeat for each joint.

If the visualization does not match the physical arm, the kinematics file may
have incorrect link lengths, joint axes, or joint limits.

## Try It

1. Run the kinematics check from step 1 to confirm your arm module has a
   built-in kinematics file.
2. Open the 3D SCENE tab and compare the rendered arm to the physical arm. Move
   individual joints using the CONTROL tab and verify the visualization matches.
3. For reading joint positions and controlling the arm, see
   [Add an Arm](/hardware/common-components/add-an-arm/) and the
   [Arm API reference](/reference/apis/components/arm/).

## Troubleshooting

{{< expand "GetKinematics returns an error or empty data" >}}

- The arm module may not include a built-in kinematics file. Check the module's
  documentation or registry page for information about kinematics support.
- Verify the arm component is configured correctly and `viam-server` has no
  errors for this component.
- Ensure you are using the correct component name in your code.

{{< /expand >}}

{{< expand "Joint limits are too restrictive" >}}

- The motion planner may fail to find paths because joint limits prevent it from
  exploring valid configurations. Check the kinematics file and widen limits if
  the physical arm allows greater range of motion.
- If the arm is a commercial model, use the manufacturer's documented joint
  limits. Do not exceed these values.

{{< /expand >}}

{{< expand "3D SCENE tab does not match the physical arm" >}}

- The kinematics file may have incorrect link lengths. Measure the physical arm
  segments and compare to the values in the kinematics file.
- Joint axes may be swapped or inverted. Move one joint at a time in the CONTROL
  tab and verify the correct joint moves in the visualizer.
- If the arm model appears offset from the frame axes, check the arm's frame
  configuration in the CONFIGURE tab.

{{< /expand >}}

## What's Next

- [Define Obstacles](/motion-planning/obstacles/): add collision geometry to
  your workspace so the motion planner avoids collisions.
- [Move an Arm to a Target Pose](/motion-planning/motion-how-to/move-arm-to-pose/):
  use the motion service to move the arm to a position in 3D space.
- [Camera Calibration](/motion-planning/camera-calibration/): calibrate your
  camera for accurate 3D position estimation.
