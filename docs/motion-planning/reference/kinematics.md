---
linkTitle: "Kinematics"
title: "Kinematics"
weight: 25
layout: "docs"
type: "docs"
description: "Reference for the SVA, URDF, and kinematic model file formats, the GetKinematics method, and providing a kinematics file for your arm."
capabilities: ["frame-system", "motion-planning"]
diataxis: reference
aliases:
  - /work-cell-layout/configure-robot-kinematics/
  - /build/work-cell-layout/configure-robot-kinematics/
---

A kinematics file describes your arm's physical structure (link lengths, joint axes, joint limits) so the motion planner can solve the inverse kinematics problem: given a target pose, find joint angles that reach it.

{{< alert title="Most arm modules handle this automatically" color="tip" >}}

Most arm modules in the Viam Registry include a kinematics file. For standard
commercial arms like the UR5e, xArm6, or Viam Arm, the module handles
kinematics automatically; you do not need to provide or configure a
kinematics file. Read this page if you are building a custom arm, using a
module without a built-in kinematics file, or verifying that a kinematics
model matches your physical arm.

{{< /alert >}}

## Concepts

### Forward and inverse kinematics

**Forward kinematics** computes the end effector's pose from the current joint angles. Walk the chain from base to end, applying each joint's rotation and each link's length; the result is deterministic. `GetEndPosition` runs forward kinematics internally.

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
  other. Viam's SVA JSON format supports two joint types directly:
  - **Revolute**: rotates around an axis (like an elbow or shoulder). Limits in
    degrees.
  - **Prismatic**: slides along an axis (like a linear actuator). Limits in
    millimeters.
- URDF files may also declare **continuous** and **fixed** joints. Viam's URDF
  importer converts continuous joints to revolute joints with infinite limits
  and folds fixed joints into static link offsets. SVA JSON rejects either
  type with an unsupported-joint-type error.

### Joint limits

Every joint has limits that define its range of motion:

- **Min/max angle** (revolute joints): the minimum and maximum rotation in
  degrees. For example, a shoulder joint might allow -180 to 180 degrees.
- **Min/max position** (prismatic joints): the minimum and maximum extension in
  millimeters.

Joint limits prevent the motion planner from computing solutions that would
require the arm to bend past its physical limits.

### Tool center point (TCP)

The tool center point is the reference point on the end effector. By default,
it is at the last link's origin. If you attach a gripper or tool, you may need
to define an offset so the TCP reflects the actual point of interaction (for
example, the tip of a gripper or the center of a suction cup). This offset is
configured through the [frame system](/motion-planning/frame-system/), not the
kinematics file.

## Kinematics file formats

Viam supports these kinematics file formats:

| Format                           | Description                                                                                             | When to use                                                                                                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SVA** (Spatial Vector Algebra) | Viam's JSON format for links and joints. Also accepts DH parameters.                                    | When writing a Viam kinematics file directly.                                                                                                                        |
| **URDF**                         | XML format used by ROS and many manufacturers                                                           | When the manufacturer ships a URDF and you want to reuse it.                                                                                                         |
| **Kinematic model**              | The JSON encoding of the kinematic model that `GetKinematics` returns (`viam-server` v1.15.0 and later) | When you need visual geometry, which SVA can't carry, or want the file to match what `GetKinematics` returns. See [Kinematic model format](#kinematic-model-format). |

Each format is a way to write the same model. Viam parses every format into one kinematic model, and that model is what `GetKinematics` returns. See [The `GetKinematics` method](#the-getkinematics-method).

Most registry arm modules use SVA internally. You rarely need to write a
kinematics file from scratch unless you are building a custom arm.

### SVA format

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
        "type": "box",
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
- **`links[].orientation`**: optional orientation of the link relative to its
  parent, in any of the
  [orientation formats](/motion-planning/reference/orientation-vectors/)
- **`links[].geometry`**: optional collision shape (uses `type`, `x`/`y`/`z` for box, `r` for sphere/capsule/cylinder, `l` for capsule length or cylinder height)
- **`links[].geometries`**: optional additional collision shapes for the
  link, in the same format as `geometry`, for a link that one shape fits
  poorly (`viam-server` v1.14.0 and later). If a link has only one shape and it
  has no `label`, it is labeled with the link's `id`. If a link has more than
  one shape, each unlabeled shape is labeled `<id>_collision_<i>`, where `<i>`
  is the shape's position among all of the link's shapes, counting from 0 with
  `geometry` first. Viam rejects the file if two shapes share a label, or if a
  label is `world` or another link's or joint's `id`. A component's `frame`
  configuration accepts `geometry` only, not `geometries`.
- **`joints[].id`**: unique name for the joint
- **`joints[].type`**: `"revolute"` (rotates) or `"prismatic"` (slides)
- **`joints[].parent`**: the link this joint attaches to
- **`joints[].axis`**: the axis of rotation or translation (unit vector)
- **`joints[].min`** / **`joints[].max`**: joint limits in degrees (revolute)
  or mm (prismatic)
- **`joints[].geometry`**: optional collision shape, prismatic joints only
- **`joints[].mimic`** (optional): make this joint follow another joint at a
  fixed multiplier and offset, for parallel-jaw grippers and other mechanically
  coupled axes. The mimic object takes `joint` (the source joint's `id`),
  `multiplier`, and `offset`; the joint's value is computed as
  `multiplier * source_value + offset`. An omitted `multiplier` defaults to
  1.0. Mimic joints must not declare their own `min`/`max`; the source joint's
  limits apply.

The SVA format also accepts Denavit-Hartenberg (DH) parameters: set `kinematic_param_type` to `"DH"` and supply a `dhParams` array, a convenience when you are converting a textbook DH table.

### Kinematic model format

On `viam-server` v1.15.0 and later, a `.json` kinematics file can use the JSON encoding of the kinematic model that `GetKinematics` returns.
Viam tells the two JSON formats apart by their fields. A file with a top-level `properties`, a link `pose`, `collision`, or `visual`, a joint `limits`, or a `JOINT_TYPE_` joint type is read as a kinematic model. Otherwise, SVA or DH markers such as `kinematic_param_type`, `dhParams`, a link-level `translation`, a joint-level `min`, or a lowercase joint type make it SVA or DH. A file with neither set of markers is read as a kinematic model.
Here is the first link and joint of a UR5e in this format:

```json
{
  "name": "UR5e",
  "links": [
    {
      "id": "base_link",
      "parent": "world",
      "pose": { "translation": { "z": 162.5 } },
      "collision": [
        {
          "center": { "z": 130, "o_z": 1 },
          "capsule": { "radius_mm": 60, "length_mm": 260 },
          "label": "base_link"
        }
      ]
    }
  ],
  "joints": [
    {
      "id": "shoulder_pan_joint",
      "parent": "base_link",
      "type": "JOINT_TYPE_REVOLUTE",
      "axis": { "z": 1 },
      "limits": { "min": -360, "max": 360 }
    }
  ]
}
```

- **`links[].pose`**: offset from the parent, as a `translation` in mm and an optional orientation in degrees
- **`links[].collision`** and **`links[].visual`**: lists of geometries; visual geometries are for display only and are not used for collision checking
- **`joints[].type`**: `JOINT_TYPE_REVOLUTE`, `JOINT_TYPE_PRISMATIC`, or `JOINT_TYPE_CONTINUOUS` (a revolute joint with no position limits)
- **`joints[].limits`**: `min` and `max`, in degrees for revolute joints or mm for prismatic joints

A mesh geometry can point to a mesh file instead of embedding its contents, for example `{"mesh": {"original_file_source_path_diagnostic": "../meshes/base.ply"}}`; the content type comes from the file extension.
Mesh file paths are relative to the kinematics file and use forward slashes. `..` is allowed, but URI schemes such as `package://` are not.
Collision meshes must be STL or PLY files; visual meshes can be any format with a file extension, such as GLB.
Mesh file references work only when the kinematics file is loaded from disk by its path, for example through a fake arm's `model-path` attribute.
A kinematic model read from bytes, such as a file embedded in a module's binary, has no directory to resolve paths against, so it must carry its mesh contents; a file reference there fails with `mesh "<path>" cannot be read without the directory of the model file`.

Viam parses this format strictly.
An unknown field, a `NaN` or `Infinity` value, a parent that is not in the model, a cycle, a duplicate `id`, a missing mesh file, or a mimic joint that sets its own limits fails the load, and the error names the file.

### URDF format

If your arm manufacturer provides a URDF file, you can reference it in your arm
module's configuration. URDF (Unified Robot Description Format) is an XML format
that describes links, joints, visual meshes, and collision geometry.

A typical URDF structure:

```xml
<robot name="my_arm">
  <link name="base_link">
    <visual>
      <geometry><box size="0.1 0.1 0.1"/></geometry>
    </visual>
    <collision>
      <geometry><box size="0.1 0.1 0.1"/></geometry>
    </collision>
  </link>
  <link name="upper_arm"/>
  <joint name="shoulder_pan" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" velocity="1.0"/>
  </joint>
</robot>
```

## The `GetKinematics` method

`GetKinematics` returns a component's kinematics. For the method signature and usage in each SDK, see [`GetKinematics`](/reference/apis/components/arm/#getkinematics) in the arm API reference.

For example, to check whether your arm has kinematics:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm
from viam.proto.common import KinematicsFileFormat

arm = Arm.from_robot(machine, "my-arm")
kinematics = await arm.get_kinematics()

# On viam-server v1.14.0 and later, the fourth element is the kinematic model.
model = kinematics[3]
print(f"Kinematic model: {len(model.links)} links, {len(model.joints)} joints")

# The first two elements are the deprecated format and file fields.
print(f"Deprecated format field: {KinematicsFileFormat.Name(kinematics[0])}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
myArm, err := arm.FromProvider(machine, "my-arm")
if err != nil {
    logger.Fatal(err)
}

model, err := myArm.Kinematics(ctx)
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Arm model: %s with %d DoF\n", model.Name(), len(model.DoF()))
```

{{% /tab %}}
{{< /tabs >}}

If the call succeeds and returns data, your arm module has kinematics built in. If it fails or returns empty data, the module does not include them. See [Provide a kinematics file](#provide-a-kinematics-file).

### Response

On `viam-server` v1.14.0 and later, `GetKinematics` returns the kinematics as a structured kinematic model: the links, the joints and their limits, mimic joints, and collision and visual geometry. By default, the response includes the file contents of every mesh. On v1.15.0 and later, a request can instead ask for the contents of only the collision meshes, only the visual meshes, or both. The response then contains the kinematic model alone, without the deprecated fields described below, and every other mesh carries only its path and content type. Check your SDK's method reference for how to make that request.

By default, the response also includes three deprecated fields for clients that predate the typed model. New code should read the model instead.

- `format`: the file format, `SVA` or `URDF`.
- `kinematics_data`: the contents of the kinematics file, as bytes.
- `meshes_by_urdf_filepath`: for a URDF file, the mesh files it references, keyed by path.

For an SVA, DH, or URDF file, `kinematics_data` holds the original file. For a kinematic model file, the field holds an SVA derived from the original, without visual geometry.

## Provide a kinematics file

Most arm modules in the Viam Registry include a kinematics file built into the module. The module loads and applies it automatically when `viam-server` starts. If you are building a custom arm, or your module has none, provide a file in any of the [formats above](#kinematics-file-formats).

Place the file in a location accessible to `viam-server` and reference it in the module's configuration. The exact configuration depends on the module. Consult the module's documentation for the specific attribute name.

To check the result, open the **3D SCENE** tab for your machine and compare the arm's visualization with the physical arm. Move a joint in the **CONTROL** tab and confirm that the visualization follows, in the right direction and by the right amount. If it doesn't match, the file may have incorrect link lengths, joint axes, or joint limits.

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

## What's next

- [Add an arm](/hardware/common-components/add-an-arm/): read joint positions and control the arm directly.
- [Define obstacles](/motion-planning/obstacles/): add collision geometry to
  your workspace so the motion planner avoids collisions.
- [Move an arm to a target pose](/motion-planning/move-an-arm/move-to-pose/):
  use the motion service to move the arm to a position in 3D space.
- [Camera calibration](/motion-planning/frame-system/camera-calibration/): calibrate your
  camera for accurate 3D position estimation.
