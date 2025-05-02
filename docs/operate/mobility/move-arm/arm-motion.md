---
title: "Move an arm with motion planning"
linkTitle: "Move an arm with motion planning"
weight: 40
type: "docs"
layout: "docs"
description: "Move an arm with the motion service API."
---

The recommended way to move an arm is with the [motion service API](/dev/reference/apis/services/motion/).

The motion service API allows you to plan and execute complex movements while avoiding collisions between components and obstacles.

## Prerequisites

{{< expand "A running machine connected to the Viam app." >}}

{{% snippet "setup.md" %}}

{{< /expand >}}

{{< expand "Set up your arm hardware." >}}

1. Mount your arm to a stable structure.

1. Ensure there is enough space for the arm to move without hitting obstacles, people, or pets.

1. Ensure the arm is connected to power, and to the computer running `viam-server`.

{{< /expand >}}

{{< expand "Define your arm's reference frame" >}}

See [Configure an arm](/operate/mobility/move-arm/configure-arm/) for instructions.
{{< /expand >}}

## Define the geometry of the environment

You must define the geometries of any objects around your arm that you want to avoid collisions with.

1. In your code, define the geometry of each object, for example a table your arm is mounted to, or a box in the workspace.

   Here is a Python example from the [Add constraints and transforms to a motion plan guide](/tutorials/services/constrain-motion/#modify-your-robots-working-environment):

   ```python {class="line-numbers linkable-line-numbers"}
   box_origin = Pose(x=400, y=0, z=50+z_offset)
   box_dims = Vector3(x=120.0, y=80.0, z=100.0)
   box_object = Geometry(center=box_origin,
                         box=RectangularPrism(dims_mm=box_dims))

   obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                         geometries=[table_object, box_object])
   ```

1. Construct a `WorldState` object, which includes the geometries of the objects in the workspace:

   {{< tabs >}}
   {{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

You will pass your `WorldState` object to the motion planning API in the next section.

## Move the arm

To move the arm, use the motion service API's [`Move` method](/dev/reference/apis/services/motion/#move).
Follow the steps below to construct the necessary objects and pass them to `Move`.

1. Construct a destination pose for the arm.
   For example:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}

   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}

   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Decide on any [constraints](/operate/reference/services/motion/constraints/) for the motion.

   To keep the orientation the same (within a tolerance) throughout the motion, use an orientation constraint:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   constraints=Constraints(orientation_constraint=[OrientationConstraint()])
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   myConstraints := &servicepb.Constraints{OrientationConstraint: []*servicepb.OrientationConstraint{&servicepb.OrientationConstraint{}}}
   ```

   {{% /tab %}}
   {{< /tabs >}}

   To move the end of the arm in a straight line, use a linear constraint:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   constraints=Constraints(
       linear_constraint=[LinearConstraint(line_tolerance_mm=0.2)])
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   myConstraints := &servicepb.Constraints{LinearConstraint: []*servicepb.LinearConstraint{&servicepb.LinearConstraint{}}}
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Call the [`Move` method](/dev/reference/apis/services/motion/#move), passing in the destination pose, any constraints, and the world state:

   {{< tabs >}}
   {{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}
