---
title: "Configure Motion Constraints"
linkTitle: "Constraints"
weight: 10
type: "docs"
description: "Configure constraints to specify certain types of motion."
---

You can constrain the motion of your robot using the Motion Service's built-in constraint options.
Constraints are passed as arguments to the [`Move`](../#move) method.

The following constraints are available:

- [Linear Constraint](#linear-constraint)
- [Orientation Constraint](#orientation-constraint)

## Linear Constraint

The linear constraint (`{"motion_profile": "linear"}`) forces the path taken by `component_name` to follow an exact linear path from the start to the goal.
If the start and goal orientations are different, the orientation along the path will follow the quaternion [Slerp (Spherical Linear Interpolation)](https://en.wikipedia.org/wiki/Slerp) of the orientation from start to goal.
This has the following sub-options:

| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| line_tolerance | float | 0.1 | Max linear deviation from straight-line between start and goal, in mm. |
| orient_tolerance | float | 0.05 | Allowable deviation from Slerp between start/goal orientations, unit is the norm of the R3AA between start and goal. |

**Example usage**:

```python {class="line-numbers linkable-line-numbers"}
# Move a gripper with a linear constraint
moved = await motion.move(
    component_name=my_gripper,
    destination=PoseInFrame(
        reference_frame="myFrame",
        pose=goal_pose), 
    world_state=worldState, 
    constraints={
        "motion_profile": "linear", 
        "line_tolerance": 0.2
     },
     extra={})
```

## Orientation Constraint

The orientation constraint (`{"motion_profile": "orientation"}`) places a restriction on the orientation change during a motion, such that the orientation during the motion does not deviate from the [Slerp](https://en.wikipedia.org/wiki/Slerp) between start and goal by more than a set amount.
This is similar to the "orient_tolerance" option in the linear profile, but without any path restrictions.
If set to zero, a movement with identical starting and ending orientations will hold that orientation throughout the movement.

| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| tolerance | float | 0.05 | Allowable deviation from Slerp between start/goal orientations, unit is the norm of the R3AA between start and goal. |

**Example usage**:

``` python
## Move a gripper with an orientation constraint
moved = await motion.move(
    component_name=my_gripper, 
    destination=PoseInFrame(
        reference_frame="myFrame",
        pose=goal_pose),
    world_state=worldState,
    constraints={"motion_profile": "orientation"},
    extra={})
```

<!--
## Next steps

Insert link to motion tutorial #3 about constraints

-->