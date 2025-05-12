---
title: "Move an arm with motion planning"
linkTitle: "Move an arm with motion planning"
weight: 40
type: "docs"
layout: "docs"
description: "Move an arm with the motion service API."
---

{{<gif webm_src="/tutorials/videos/motion_constraints.webm" mp4_src="/tutorials/videos/motion_constraints.mp4" alt="An arm moving a cup from one side of a tissue box to the other, across a table. The cup stays upright." class="alignright" max-width="250px">}}

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

{{< table >}}
{{% tablestep number=1 %}}

In your code, define the geometry of each object, for example a table your arm is mounted to, or a box in the workspace.
The available geometry types are:

<!-- prettier-ignore -->
| Geometry type | Description | Dimensions to define |
| ------------- | ----------- | ------------------ |
| box           | A rectangular prism. | `x`, `y`, `z`: length in each direction in mm. |
| capsule       | A cylinder with hemispherical end caps. | `radius` in mm, `length` in mm between the centers of the hemispherical end caps. |
| sphere        | A sphere. | `radius` in mm. |
| mesh          | A 3D model defined by a mesh. | `triangles`: a list of triangles, each defined by three vertices. |

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
box_origin = Pose(x=400, y=0, z=50+z_offset)
box_dims = Vector3(x=120.0, y=80.0, z=100.0)
box_object = Geometry(center=box_origin,
                      box=RectangularPrism(dims_mm=box_dims))
```

See [Geometry](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry) for more information on the geometry types and their parameters.

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
boxPose := spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 0.0})
boxDims := r3.Vector{X: 0.2, Y: 0.2, Z: 0.2} // 20cm x 20cm x 20cm box
obstacle, _ := spatialmath.NewBox(boxPose, boxDims, "obstacle_1")
```

See [spatialmath](https://pkg.go.dev/go.viam.com/rdk/spatialmath) for more information on the geometry types and their parameters.

{{% /tab %}}
{{< /tabs >}}
{{% /tablestep %}}
{{% tablestep number=2 %}}

Put the object into a reference frame, creating a `GeometriesInFrame` object.
This example puts the object into the world reference frame, but you can put it into a different reference frame if it makes sense for your application:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                       geometries=[box_object])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
geometryInFrame := referenceframe.NewGeometriesInFrame("world", []spatialmath.Geometry{obstacle})
obstacles := []*referenceframe.GeometriesInFrame{geometryInFrame}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep number=3 %}}

Construct a `WorldState` object, which includes the geometries of the objects in the workspace:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
world_state = WorldState(obstacles=obstacles_in_frame)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myWorldState := &servicepb.WorldState{Obstacles: []*servicepb.GeometriesInFrame{obstaclesInFrame}}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
You can also add _transforms_ to the world state to represent objects that are connected to a machine without being components of the machine.
See [Use a transform to represent a drinking cup](/tutorials/services/constrain-motion/#use-a-transform-to-represent-a-drinking-cup) for an example.
{{% /alert %}}

{{% /tablestep %}}
{{% /table %}}

You will pass your `WorldState` object to the motion planning API in the next section.

## Move the arm

To move the arm, use the motion service API's [`Move` method](/dev/reference/apis/services/motion/#move).
Follow the steps below to construct the necessary objects and pass them to `Move`.

1. Get the `ResourceName` (Python) or `resource.Name` (Go) of the arm you want to move:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   arm_resource_name = Arm.get_resource_name("arm-1")
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   armResourceName := arm.GetResourceName("arm-1")
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Construct a destination pose for the arm.
   Specify the reference frame of the destination pose, creating a `PoseInFrame` object.
   For example:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   destination_pose = Pose(x=0.0,
                          y=0.0,
                          z=-100.0,
                          o_x=0.0,
                          o_y=0.0,
                          o_z=1.0,
                          theta=0.0)
   destination_pose_in_frame = PoseInFrame(
      reference_frame=world,
      pose=destination_pose)
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   destinationPose := spatialmath.NewPose(
      r3.Vector{X: 0.0, Y: 0.0, Z: -100.0},
      &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
      )
   destinationPoseInFrame := referenceframe.NewPoseInFrame(world, destinationPose)
   ```

   {{% /tab %}}
   {{< /tabs >}}

   {{% alert title="Tip" color="tip" %}}
   To get a better intuition for poses and where you want the arm to move, try [driving the arm manually with the control interface](/operate/mobility/move-arm/arm-no-code/) and notice how the pose indicated in the control interface corresponds to the arm's position in the real world.
   {{% /alert %}}

1. If you want to specify any [constraints](/operate/reference/services/motion/constraints/) for the motion, add them to a `Constraints` object:

   {{< tabs >}}
   {{% tab name="Linear constraint" %}}

To keep the orientation the same (within a tolerance) throughout the motion, use an orientation constraint:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
constraints = Constraints(orientation_constraint=[OrientationConstraint()])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myConstraints := &servicepb.Constraints{OrientationConstraint: []*servicepb.OrientationConstraint{&servicepb.OrientationConstraint{}}}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Orientation constraint" %}}

To move the end of the arm in a straight line, use a linear constraint:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
constraints = Constraints(
    linear_constraint=[LinearConstraint(line_tolerance_mm=0.2)])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myConstraints := &servicepb.Constraints{LinearConstraint: []*servicepb.LinearConstraint{&servicepb.LinearConstraint{}}}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

1. Call the [`Move` method](/dev/reference/apis/services/motion/#move), passing in the destination pose, any constraints, and the world state:

   {{< tabs >}}
   {{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
await motion_service.move(component_name=arm_resource_name,
                          destination=destination_pose_in_frame,
                          world_state=world_state,
                          constraints=constraints)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
moved, err := motionService.Move(context.Background(), motion.MoveReq{
  ComponentName: armResourceName,
  Destination: destinationPoseInFrame,
  WorldState: myWorldState,
  Constraints: myConstraints,
})
```

{{% /tab %}}
{{< /tabs >}}

## Full code

The following is the full code for the example above:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% /tabs %}}

## More examples

{{< cards >}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper/" %}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
