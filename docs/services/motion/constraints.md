---
title: "Configure Motion Constraints"
linkTitle: "Constraints"
weight: 10
type: "docs"
description: "Configure constraints to avoid obstacles or specify certain types of motion."
---

Currently (October 18, 2022), there is no built in, top level way to specify different constraints.
However, several have been pre-programmed and are accessible when using the Go RDK or the Python SDK by passing a string naming the constraint to "motion_profile" inside the `extra` parameter, along with individual algorithm variables.
This is not available in the Viam app.
Available constraints all control the topological movement of the moving component along its path.

For a usage example, see [sample code above](../#examples).

The available constraints--linear, psuedolinear, orientation, and free--are covered in the following sub-sections.

{{% alert title="Note" %}}
The motion profile constraints passed using the `extra` parameter are experimental features.
Stability is not guaranteed.
{{% /alert %}}

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

## Pseudolinear Constraint

The pseudolinear constraint (`{"motion_profile": "pseudolinear"}`) restricts the path such that it will deviate from the straight-line linear path between start and goal by no more than a certain amount, where that amount is determined as a percentage of the distance from start to goal.
Linear and orientation deviation are determined separately, so if a motion has a large linear difference but has identical starting and ending orientations, the motion will hold its orientation constant while allowing some linear deflection.
This has the following suboption:

| Parameter Name | Type | Default | Description |
| -------------- | ---- | ------- | ----------- |
| tolerance | float | 0.8 | Allowable linear and orientation deviation from direct interpolation path, as a proportion of the linear and orientation distances between start and goal. |

**Example usage**:

``` python
extra = {"motion_profile": "pseudolinear", "tolerance": 0.7}
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

## Free Constraint

The free constraint (`{"motion_profile": "free"}`) places no restrictions on motion whatsoever.
This is the default and will be used if nothing is passed.
This profile takes no parameters.

**Example usage**:

``` python
extra = {"motion_profile": "free"}
```
