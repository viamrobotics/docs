---
title: "Configure Motion Constraints"
linkTitle: "Constraints"
weight: 10
type: "docs"
description: "Configure constraints to specify certain types of motion."
---

You can control the motion of your robot using the Motion Service's built-in constraint options.

Available constraints all control the topological movement of the moving component along its path.

The available constraints--linear, psuedolinear, orientation, and free--are covered in the following sub-sections.

The following constraints are available:

- [Linear Constraint](#linear-constraint)
- [Orientation Constraint](#orientation-constraint)

## Linear Constraint

The linear constraint (`{"motion_profile": "linear"}`) forces the path taken by `component_name` to follow an exact linear path from the start to the goal.
If the start and goal orientations are different, the orientation along the path will follow the quaternion Slerp (Spherical Linear Interpolation) of the orientation from start to goal.
This has the following sub-options:

| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| line_tolerance | float | 0.1 | Max linear deviation from straight-line between start and goal, in mm. |
| orient_tolerance | float | 0.05 | Allowable deviation from Slerp between start/goal orientations, unit is the norm of the R3AA between start and goal. |

**Example usage**:

```python
extra = {"motion_profile": "linear"}
```

## Orientation Constraint

The orientation constraint (`{"motion_profile": "orientation"}`) places a restriction on the orientation change during a motion, such that the orientation during the motion does not deviate from the Slerp between start and goal by more than a set amount.
This is similar to the "orient_tolerance" option in the linear profile, but without any path restrictions.
If set to zero, a movement with identical starting and ending orientations will hold that orientation throughout the movement.

| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| tolerance | float | 0.05 | Allowable deviation from Slerp between start/goal orientations, unit is the norm of the R3AA between start and goal. |

**Example usage**:

``` python
extra = {"motion_profile": "orientation"}
```

<!--
## Next steps

Insert link to motion tutorial #3 about constraints

-->