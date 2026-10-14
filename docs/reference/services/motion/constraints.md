---
title: "Motion constraints reference"
linkTitle: "Constraints"
weight: 10
layout: "docs"
type: "docs"
description: "Configure constraints to specify certain types of motion."
capabilities: ["motion-planning"]
diataxis: reference
date: "2026-04-18"
aliases:
  - /operate/reference/services/motion/constraints/
  - /services/motion/constraints/
  - /mobility/motion/constraints/
---

You can constrain the motion of your machine using the motion service's built-in constraint options.
Constraints are passed as arguments to the [`Move`](/reference/apis/services/motion/#move) method.

The following constraints are available:

- [Linear constraint](#linear-constraint)
- [Orientation constraint](#orientation-constraint)
- [Next steps](#next-steps)

## Linear constraint

The linear constraint (`LinearConstraint`) forces the path taken by `component_name` to stay within `line_tolerance_mm` of the straight line from the start to the goal.
If `line_tolerance_mm` is 0, the default, the planner doesn't check the path against the line.
If `orientation_tolerance_degs` is set, the orientation along the path stays within that angle of the start or goal orientation, whichever is closer.
This has the following sub-options:

<!-- prettier-ignore -->
| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| line_tolerance_mm | float | 0 | Max linear deviation from straight-line between start and goal, in mm. Only checked when greater than 0, so 0 turns the check off. |
| orientation_tolerance_degs | float | 0 | Max angular distance, in degrees, between the current orientation and the closer of the start or goal orientation. Only checked when greater than 0, so 0 turns the check off. |

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

The orientation constraint (`OrientationConstraint`) places a restriction on the orientation change during a motion, such that the orientation during the motion does not deviate from the direct rotation between start and goal by more than a set amount.
The direct rotation is the shortest arc between the two orientations, also known as the [Slerp](https://en.wikipedia.org/wiki/Slerp) path.
This is similar to the `orientation_tolerance_degs` option in the linear constraint, but without any path restrictions, and with a tolerance that follows the whole arc instead of only the start and goal.
If set to zero, any deviation from the direct rotation is rejected, so a movement with identical starting and ending orientations will hold that orientation throughout the movement.
This differs from the linear constraint, where 0 turns the orientation check off.

<!-- prettier-ignore -->
| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| orientation_tolerance_degs | float | 0 | Max angular distance, in degrees, between the current orientation and the direct rotation from the start orientation to the goal orientation. 0 rejects any deviation. |
| ignore_theta | bool | false | When true, deviation is measured between orientation vectors alone, disregarding rotation about the component's own pointing axis. Use this for payloads symmetric about that axis (for example, an open container that spills when tipped but not when spun). |

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
