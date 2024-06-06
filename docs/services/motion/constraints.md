---
title: "Configure Motion Constraints"
linkTitle: "Constraints"
weight: 10
type: "docs"
description: "Configure constraints to specify certain types of motion."
aliases:
  - "/services/motion/constraints/"
  - "/mobility/motion/constraints/"
---

You can constrain the motion of your machine using the motion service's built-in constraint options.
Constraints are passed as arguments to the [`Move`](../#move) method.

The following constraints are available:

- [Linear constraint](#linear-constraint)
- [Orientation constraint](#orientation-constraint)
- [Next steps](#next-steps)

## Linear constraint

The linear constraint (`{"motion_profile": "linear"}`) forces the path taken by `component_name` to follow an exact linear path from the start to the goal.
If the start and goal orientations are different, the orientation along the path will follow the quaternion [Slerp (Spherical Linear Interpolation)](https://en.wikipedia.org/wiki/Slerp) of the orientation from start to goal.
This has the following sub-options:

<!-- prettier-ignore -->
| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| line_tolerance_mm | float | 0.1 | Max linear deviation from straight-line between start and goal, in mm. |
| orientation_tolerance_degs | float | 2.0 | Allowable deviation from Slerp between start/goal orientations, in degrees. |

**Example usage**:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Move a gripper with a linear constraint
moved = await motion.move(
    component_name=my_gripper,
    destination=PoseInFrame(
        reference_frame="my_frame",
        pose=goal_pose),
    world_state=worldState,
    constraints={
        Constraints(
            linear_constraint=[LinearConstraint(line_tolerance_mm=0.2)])
    },
    extra={})
```

You can find more information in the [Python SDK Docs](https://python.viam.dev/autoapi/viam/gen/service/motion/v1/motion_pb2/index.html#viam.gen.service.motion.v1.motion_pb2.Constraints).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Move a gripper with a linear constraint
myConstraints := &servicepb.Constraints{LinearConstraint: []*servicepb.LinearConstraint{&servicepb.LinearConstraint{}}}

moved := motionService.Move(
    context.Background(),
    myGripperResourceName,
    NewPoseInFrame("myFrame", myGoalPose),
    worldState,
    myConstraints,
    nil
    )
```

You can find more information in the [Go SDK Docs](https://pkg.go.dev/go.viam.com/api/service/motion/v1#Constraints).

{{% /tab %}}
{{< /tabs >}}

## Orientation constraint

The orientation constraint (`{"motion_profile": "orientation"}`) places a restriction on the orientation change during a motion, such that the orientation during the motion does not deviate from the [Slerp](https://en.wikipedia.org/wiki/Slerp) between start and goal by more than a set amount.
This is similar to the "orient_tolerance" option in the linear profile, but without any path restrictions.
If set to zero, a movement with identical starting and ending orientations will hold that orientation throughout the movement.

<!-- prettier-ignore -->
| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| orientation_tolerance_degs | float | 2.0 | Allowable deviation from Slerp between start/goal orientations, in degrees. |

**Example usage**:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Move a gripper with an orientation constraint
moved = await motion.move(
    component_name=my_gripper,
    destination=PoseInFrame(
        reference_frame="my_frame",
        pose=goal_pose),
    world_state=worldState,
    constraints=Constraints(orientation_constraint=[OrientationConstraint()]),
    extra={})
```

You can find more information in the [Python SDK Docs](https://python.viam.dev/autoapi/viam/gen/service/motion/v1/motion_pb2/index.html#viam.gen.service.motion.v1.motion_pb2.Constraints).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Move a gripper with an orientation constraint
myConstraints := &servicepb.Constraints{OrientationConstraint: []*servicepb.OrientationConstraint{&servicepb.OrientationConstraint{}}}

moved := motionService.Move(
    context.Background(),
    myGripperResourceName,
    NewPoseInFrame("myFrame", myGoalPose),
    worldState,
    myConstraints,
    nil
    )
```

You can find more information in the [Go SDK Docs](https://pkg.go.dev/go.viam.com/api/service/motion/v1#Constraints).

{{% /tab %}}
{{< /tabs >}}

## Next steps

Constraints are used in the following tutorials:

{{< cards >}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{< /cards >}}
