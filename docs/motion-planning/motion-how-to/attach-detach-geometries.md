---
linkTitle: "Attach and detach geometries"
title: "Attach and detach geometries at runtime"
weight: 45
layout: "docs"
type: "docs"
description: "Make the motion planner aware of an object the robot has grasped by attaching the object's geometry to the gripper frame for subsequent Move calls."
---

When an arm grasps an object, the planner needs to know the object is
now part of the robot: it moves with the gripper, collides with
obstacles like any other link, and should be accounted for in every
motion plan until the robot releases it. The mechanism is
`WorldState.transforms`. You pass the object's geometry attached to
the gripper's frame for the duration of the grasp, then stop passing
it after release.

This is the runtime complement to the
[passive objects pattern](/motion-planning/obstacles/#passive-objects-attached-to-a-component),
which covers objects that are always attached (camera mounts, adapter
plates). Use this page's pattern for objects the robot grasps and
releases dynamically.

## Before you start

- A working motion service call (`motion.Move` for arms, a
  grasp-capable gripper configured on the machine).
- The grasped object's rough dimensions. You can approximate with a
  box, sphere, or capsule.
- The offset between the gripper frame origin and the object's center
  (usually close to the gripper's tool center point when the object is
  held centered).

## The Transform message

`WorldState.transforms` is a list of `Transform` entries. Each entry
defines a new frame and optionally attaches a geometry to it:

| Field                    | Purpose                                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| `reference_frame`        | The name of the new frame you are defining (for example, `grasped-object`).                       |
| `pose_in_observer_frame` | A `PoseInFrame` specifying the parent frame and the pose of the new frame relative to the parent. |
| `physical_object`        | Optional `Geometry` for collision checking.                                                       |
| `uuid`                   | Optional identifier. Used by the service for deduplication and lifecycle; safe to leave empty.    |
| `metadata`               | Optional freeform `Struct`. Not used by the planner; available for caller-side bookkeeping.       |

Set `pose_in_observer_frame.reference_frame` to the **parent** frame
name (for example, `my-gripper`). The pose inside `pose_in_observer_frame`
is the new frame's position and orientation relative to that parent.

## Pattern: attach on grasp, detach on release

1. After a successful grasp, build a `Transform` whose parent is the
   gripper, with a geometry approximating the object.
2. On every subsequent `motion.Move` call while the object is held,
   include the transform in `WorldState.transforms`.
3. After release, stop including the transform. No explicit detach
   call is needed — `WorldState` is per-call, so the next Move without
   the transform leaves the object out of the planner's world.

## Example: attach a grasped box

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Pose, PoseInFrame, Vector3, RectangularPrism,
    Geometry, GeometriesInFrame, Transform, WorldState,
)

# Object: a 80mm x 80mm x 100mm box centered 50mm below the gripper origin.
grasped_object = Transform(
    reference_frame="grasped-object",
    pose_in_observer_frame=PoseInFrame(
        reference_frame="my-gripper",
        pose=Pose(x=0, y=0, z=50, o_x=0, o_y=0, o_z=1, theta=0),
    ),
    physical_object=Geometry(
        center=Pose(x=0, y=0, z=0),
        box=RectangularPrism(dims_mm=Vector3(x=80, y=80, z=100)),
        label="grasped-box",
    ),
)

# Static obstacles already known (for example, the table the arm is mounted on).
table = Geometry(
    center=Pose(x=0, y=0, z=-20),
    box=RectangularPrism(dims_mm=Vector3(x=800, y=600, z=40)),
    label="table",
)
obstacles = GeometriesInFrame(
    reference_frame="world",
    geometries=[table],
)

world_state = WorldState(
    obstacles=[obstacles],
    transforms=[grasped_object],
)

# Use world_state on every Move call while the object is held.
await motion_service.move(
    component_name="my-arm",
    destination=destination,
    world_state=world_state,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "github.com/golang/geo/r3"
    commonpb "go.viam.com/api/common/v1"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/spatialmath"
    "go.viam.com/rdk/services/motion"
)

// Object: a 80mm x 80mm x 100mm box centered 50mm below the gripper origin.
grasped, err := spatialmath.NewBox(
    spatialmath.NewZeroPose(),
    r3.Vector{X: 80, Y: 80, Z: 100},
    "grasped-box",
)
if err != nil {
    logger.Fatal(err)
}

graspedPose := spatialmath.NewPoseFromPoint(r3.Vector{X: 0, Y: 0, Z: 50})

graspedTransform := referenceframe.NewLinkInFrame(
    "my-gripper",
    graspedPose,
    "grasped-object",
    grasped,
)

// Static obstacles already known.
tableOrigin := spatialmath.NewPose(
    r3.Vector{X: 0, Y: 0, Z: -20},
    &spatialmath.OrientationVectorDegrees{OZ: 1},
)
table, _ := spatialmath.NewBox(tableOrigin, r3.Vector{X: 800, Y: 600, Z: 40}, "table")

obstaclesInFrame := referenceframe.NewGeometriesInFrame(
    referenceframe.World,
    []spatialmath.Geometry{table},
)

worldState, err := referenceframe.NewWorldState(
    []*referenceframe.GeometriesInFrame{obstaclesInFrame},
    []*referenceframe.LinkInFrame{graspedTransform},
)
if err != nil {
    logger.Fatal(err)
}

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
    WorldState:    worldState,
})
```

Go uses `referenceframe.NewWorldState` and `referenceframe.LinkInFrame`
for transforms. The SDK wrapper constructs the proto `Transform`
automatically. Ignore `uuid` and `metadata` unless you have a specific
reason to use them.

{{% /tab %}}
{{< /tabs >}}

## Detach: stop including the transform

There is no separate "detach" call. After release, construct the next
`WorldState` without the grasped-object transform:

```python
world_state = WorldState(obstacles=[obstacles])  # no transforms

await motion_service.move(
    component_name="my-arm",
    destination=after_release_pose,
    world_state=world_state,
)
```

The planner's view of the world for this and subsequent calls does
not include the grasped object.

## Allow contact while grasping

During the grasp motion itself, the gripper must come into contact
with the object. The planner rejects paths with any collision by
default, so allow the gripper-to-object pair:

```python
from viam.proto.service.motion import Constraints, CollisionSpecification

constraints = Constraints(
    collision_specification=[
        CollisionSpecification(
            allows=[
                CollisionSpecification.AllowedFrameCollisions(
                    frame1="my-gripper",
                    frame2="target-object",
                ),
            ],
        ),
    ],
)
```

For the full pattern, see
[Allow specific frames to collide](/motion-planning/motion-how-to/allow-frame-collisions/).

## Compared to passive attachment

| Need                                                                           | Use                                                                                                                                                |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Object is always attached to the arm (camera mount, fixed tool, cable bundle). | [Passive objects pattern](/motion-planning/obstacles/#passive-objects-attached-to-a-component) — configure a fake generic component with geometry. |
| Object is attached only during a grasp, and may change between grasps.         | This page — build a `Transform`, pass it through `WorldState.transforms` for the duration.                                                         |
| Object is a static obstacle in the workspace (table, wall).                    | Standard [obstacles](/motion-planning/obstacles/) — no transform needed.                                                                           |

## Troubleshooting

{{< expand "The planner reports a collision between the arm and the grasped object" >}}

The grasped-object geometry likely sits where the arm reaches during
normal motion. Check:

- The `pose_in_observer_frame` offset. Is the object geometry where
  you physically hold it?
- The geometry size. Is it bigger than the real object?
- The arm's own geometry. If the gripper wraps around the object,
  parts of the gripper may overlap with the grasped-object geometry;
  use `CollisionSpecification` to allow the gripper-to-object pair.

{{< /expand >}}

{{< expand "The planner does not seem to account for the grasped object" >}}

`WorldState` is per-call. If you built it once and passed it only to
the first Move, subsequent Move calls use an empty world. Confirm
you are passing the same `WorldState` (or an updated one that still
includes the transform) on every call while the object is held.

{{< /expand >}}

{{< expand "Error: unknown parent frame for transform" >}}

The `pose_in_observer_frame.reference_frame` must name a frame that
exists in the machine's frame system. A typo, a component that is
missing, or a component whose frame is not configured will all produce
this error. Run
[`viam machines part motion print-config`](/motion-planning/reference/cli-commands/#print-config)
to see the valid frame names.

{{< /expand >}}

## What's next

- [Define obstacles](/motion-planning/obstacles/): the static obstacles
  you pass alongside grasped-object transforms.
- [Allow specific frames to collide](/motion-planning/motion-how-to/allow-frame-collisions/):
  permit the contact between gripper and object that the grasp
  requires.
- [Pick an object](/motion-planning/motion-how-to/pick-an-object/):
  end-to-end grasp flow that uses this pattern.
- [Frame system API](/motion-planning/reference/frame-system-api/):
  the `TransformPose` method, which uses the same supplemental
  transforms mechanism for one-off pose conversions.
