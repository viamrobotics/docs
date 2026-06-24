---
linkTitle: "End effector frames"
title: "End effector frames"
weight: 5
layout: "docs"
type: "docs"
description: "How Move places a named frame at a target pose, and how the frame attribute and WorldState transforms set which point on the robot a frame represents."
---

When you move an arm with the motion service, you move a _frame_ from its current
pose to a destination pose. That frame is called the **end effector frame**, also called
the tool control point (TCP) or the manipulation control frame. Where the end effector
frame sits depends on the arm, the tool, and the task, and that frame can change partway
through a job. This page explains why the end effector frame exists, how `Move` resolves it,
and how you define and visualize it with Viam.

First, look at where the end effector frame could be defined for two example use cases:

{{<imgproc src="/motion-planning/frame-system/end-effector-types.svg" declaredimensions=true alt="Two arms drawn schematically. On the left, a two-finger gripper with its end effector frame between the fingertips. On the right, a drill whose end effector frame sits at the bit tip, offset from the arm frame in both x and z. Both panels also show small coordinate axes for the world frame at the base and the arm frame at the flange." style="max-width:820px" class="aligncenter">}}

The end effector frame is hardware and task dependent. For a two-finger gripper, the
end effector frame typically sits between the fingertips, a short offset below the arm's frame. For
a drill, it sits at the bit tip, offset from the arm's frame both forward and down,
and the orientation may be flipped, so a positive z would mean to drill deeper.
When you call `Move`, you have the option to specify which frame you are moving, and
using the arm frame is always an option. By creating an end effector frame at the
correct location, a `Move` call becomes easier and better represents the task being
performed.

Now look at how the motion service describes the move. The snippets on this page
assume a connected motion service client, `motion_service` in Python and
`motionService` in Go. For how to set this up in more detail, see
[Access the motion service in your code](/reference/services/motion/#access-the-motion-service-in-your-code).

```python
from viam.proto.common import Pose, PoseInFrame

# A pose in world frame facing Z Down
target_pose = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=400, y=0, z=300, o_x=0, o_y=0, o_z=-1, theta=0),
)

# Move the Gripper Frame to the target_pose
await motion_service.move(
    component_name="my-gripper",
    destination=target_pose,
)
```

You pass two parameters to `Move`: a string `component_name` and a `destination`
pose.

## Which frame Move resolves

The `destination` you pass is a target pose for the resolved frame, and the planner
tries to find a collision-free motion that moves the frame to the destination.

The `component_name` can be a component name or a frame name. The motion service
looks for a frame with that name in the frame system. When you pass a component name
such as `"my-arm"` or `"my-gripper"`, Viam supplies a frame for it behind the scenes:

- **An arm**: its kinematics file (URDF or Viam JSON) defines a single output frame at the
  terminal link of the kinematic chain, commonly called the tool flange. That output frame
  is the arm's built-in end effector frame.
- **Another component**, such as a gripper, defines a static frame through its `frame`
  attribute, which you set on the component's configuration card.

Here is a gripper `frame` attribute from the [Arm with gripper and wrist camera](/motion-planning/frame-system/arm-gripper-camera/) example, whose origin sits 120 mm past the flange:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 0, "z": 120 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

## Why the frame you name matters

A `Move` call that uses the arm frame produces different motion than one that
uses the end-effector frame. The arm's frame sits at the flange, and the end effector
frame sits at the bit tip, so the same `target_pose` produces different motions.
In the example below, the target pose is defined on the face of a box. If you use
the drill-tip frame, the bit moves to the box face. If you use the arm frame, the
drill drives into the box, because the planner tries to move the arm frame to the
target pose.

{{<imgproc src="/motion-planning/frame-system/arm-vs-gripper-frame.svg" declaredimensions=true alt="Two diagrams of the same target pose. On the left, the move targets the arm frame, so the flange lands on the target and the drill bit overshoots past it. On the right, the move targets the drill-tip frame, so the bit lands on the target. Both panels show the world frame, the arm frame, and the labeled target pose." style="max-width:760px" class="aligncenter">}}

## Define an end effector frame in code

The `frame` attribute described above works well when the end effector frame is static.
When the end effector frame moves during a task, or when defining it in code suits
the job better, add a new frame to the frame system with a `WorldState` transform.

A great example is a grasped part. Prior to pickup, the end effector frame is located
with the gripper. After pickup, the end effector frame may need to move to the part for
an assembly step. The grasped part may not have been in the machine configuration,
so you add its frame to the frame system at request time with a `WorldState` transform,
attached to the gripper so it moves with the grasp:

{{<imgproc src="/motion-planning/frame-system/held-object-frame.svg" declaredimensions=true alt="A cobot arm whose gripper holds a bent, L-shaped object. The arm frame sits at the flange and the gripper frame at the jaws. An object-tip frame sits at the far end of the object, offset from the gripper in multiple axes and rotated to point along it. Each frame shows labeled x, y, and z axes." style="max-width:600px" class="aligncenter">}}

To extend that frame system for
one motion, pass a
[`WorldState`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState)
to `Move` with extra frames. The steps differ slightly by language, but the shape is
the same:

1. Define the translation and orientation from the parent frame to the origin of the
   new frame. In Python, this is a `PoseInFrame`; in Go, it is the pose you pass to
   `NewLinkInFrame`. The parent is usually an arm or gripper component name, such as
   `"my-gripper"` for a grasped object.
2. Build a transform from that pose and add it to the `WorldState`.

The `WorldState` applies to a single `Move` call. A later call needs its own
`WorldState` to keep using the transform.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Transform, PoseInFrame, Pose, WorldState
)

# A frame named "object-tip", 100 mm beyond the gripper, attached to it.
object_tip = Transform(
    reference_frame="object-tip",  # the name of the new frame
    pose_in_observer_frame=PoseInFrame(
        reference_frame="my-gripper",  # the parent: the object moves with the gripper
        # 70 mm across and 130 mm down from the gripper, turned so z points along the bent object.
        pose=Pose(x=70, y=0, z=130, o_x=1, o_y=0, o_z=0, theta=90),
    ),
)

world_state = WorldState(transforms=[object_tip])

# Move can now place "object-tip" at the destination.
await motion_service.move(
    component_name="object-tip",
    destination=target_pose,
    world_state=world_state,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// A frame named "object-tip", 100 mm beyond the gripper, attached to it.
objectTipLink := referenceframe.NewLinkInFrame(
    "my-gripper", // the parent: the object moves with the gripper
    // 70 mm across and 130 mm down from the gripper, turned so z points along the bent object.
    spatialmath.NewPose(
        r3.Vector{X: 70, Y: 0, Z: 130},
        &spatialmath.OrientationVectorDegrees{OX: 1, OY: 0, OZ: 0, Theta: 90},
    ),
    "object-tip", // the name of the new frame
    nil,          // optional collision geometry; nil means a pure coordinate frame
)

worldState, err := referenceframe.NewWorldState(
    nil, []*referenceframe.LinkInFrame{objectTipLink})
if err != nil {
    logger.Fatal(err)
}

// Move can now place "object-tip" at the destination.
_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "object-tip",
    Destination:   targetPose, // your goal *referenceframe.PoseInFrame
    WorldState:    worldState,
})
```

{{% /tab %}}
{{< /tabs >}}

### Attach a geometry to a transform

A transform can also carry a collision geometry, a shape the planner avoids while it
tries to find collision-free motion to the destination. For a grasped object, it can be
helpful to attach geometry so the planner routes the grasped object around obstacles.
Give the transform a box, sphere, capsule, or mesh defined in the frame's own coordinates:

{{<imgproc src="/motion-planning/frame-system/held-object-geometry.svg" declaredimensions=true alt="A cobot arm whose gripper holds an object wrapped in a dashed collision-geometry box. A separate obstacle sits nearby, and the planner routes the held object's geometry around it." style="max-width:700px" class="aligncenter">}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Transform, PoseInFrame, Pose, Geometry, RectangularPrism, Vector3,
)

object_tip = Transform(
    reference_frame="object-tip",
    pose_in_observer_frame=PoseInFrame(
        reference_frame="my-gripper",
        pose=Pose(x=70, y=0, z=130, o_x=1, o_y=0, o_z=0, theta=90),
    ),
    physical_object=Geometry(  # the collision geometry for this frame
        center=Pose(x=0, y=0, z=-50, o_x=0, o_y=0, o_z=1, theta=0),  # centered on the grasped object
        box=RectangularPrism(dims_mm=Vector3(x=30, y=30, z=100)),
        label="object-tip",
    ),
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Make a new 30 x 30 x 100 mm box covering the grasped object.
geometry, err := spatialmath.NewBox(
    spatialmath.NewPoseFromPoint(r3.Vector{X: 0, Y: 0, Z: -50}), // centered on the grasped object
    r3.Vector{X: 30, Y: 30, Z: 100},                             // full dimensions in mm
    "object-tip",
)
if err != nil {
    logger.Fatal(err)
}

objectTipLink := referenceframe.NewLinkInFrame(
    "my-gripper",
    spatialmath.NewPose(
        r3.Vector{X: 70, Y: 0, Z: 130},
        &spatialmath.OrientationVectorDegrees{OX: 1, OY: 0, OZ: 0, Theta: 90},
    ),
    "object-tip",
    geometry, // the planner avoids collisions with this geometry
)
```

{{% /tab %}}
{{< /tabs >}}

## WorldState versus the world state store service

The names are similar, but `WorldState` and the world state store service are
different things, and only one affects a `Move` call.

- `WorldState` is the argument you pass to a single `Move` call. The obstacles
  and transforms in it exist only for that request: the planner uses them to
  plan this motion, and they are gone when the call returns. The transform in
  the previous section is a `WorldState` transform, so it shapes the plan.
- The world state store service is a separate service that holds transforms for
  client-side visualization in the [3D scene](/motion-planning/3d-scene/).

To change where the arm goes, put the transform in the `WorldState` you pass to
`Move`, as shown above. To render a custom visual that leaves planning unchanged,
publish it to the world state store service instead.

## Visualize the end effector frame

Static frames render in the 3D scene automatically. Open the **3D SCENE** tab on
your machine's page, and the arm's built-in end effector frame and any `frame`
attributes you configured appear as coordinate axes at their computed poses, the
same axes drawn in the diagrams on this page.

A frame you add in code with a `WorldState` transform lasts only for that `Move`
call, so it stays out of the 3D scene by default. To draw a code-defined frame in
the [3D scene](/motion-planning/3d-scene/), publish it through a world state store
service. A module that implements this service holds your transforms and streams
them to the scene, which renders a frame with no geometry as a set of coordinate axes
alongside the static frames.

## What's next

- [Frame system overview](/motion-planning/frame-system/overview/):
  configure parent, translation, orientation, and geometry for every component.
- [Arm with gripper and wrist camera](/motion-planning/frame-system/arm-gripper-camera/):
  a worked end effector configuration.
- [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/):
  target a frame with the motion service.
- [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/):
  carry a grasped object's geometry with the end effector.
