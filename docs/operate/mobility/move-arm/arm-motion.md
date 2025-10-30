---
title: "Move an arm with motion planning"
linkTitle: "Move an arm with motion planning"
weight: 40
type: "docs"
layout: "docs"
description: "Plan and execute complex movements with an arm using the motion service API."
aliases:
  - /how-tos/move-robot-arm/
  - /tutorials/motion/accessing-and-moving-robot-arm/
  - /tutorials/motion/
  - /operate/mobility/move-arm/arm-no-code/
date: "2025-05-21"
---

{{<gif webm_src="/tutorials/videos/motion_constraints.webm" mp4_src="/tutorials/videos/motion_constraints.mp4" alt="An arm moving a cup from one side of a tissue box to the other, across a table. The cup stays upright." class="alignright" max-width="170px">}}

This is the recommended way to write an application to move an arm.

The [motion service API](/dev/reference/apis/services/motion/) allows you to plan and execute complex movements while avoiding collisions between components and obstacles.

## Prerequisites

{{< expand "A running machine connected to Viam." >}}

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

## Connect your code to your machine

1. From your machine's page, click the **CONNECT** tab.

1. Choose your programming language.
   The examples below are written in Python and Go, so choose one of those to follow along.

1. Toggle **Include API key**.

1. Copy and paste the connection code into a file on your machine, for example `move_arm.py` or `move_arm.go`.

This code connects to your machine with authentication credentials, and creates a `machine` object.
You'll now add to the code to describe the geometry of the arm's environment and move the arm.

## Add imports and access the arm

1. Add the following imports to your code:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   from viam.services.motion import MotionClient, Constraints
   from viam.components.arm import Arm
   from viam.proto.common import (GeometriesInFrame, Geometry, Pose, PoseInFrame,
                                 Vector3, RectangularPrism, Capsule, WorldState,
                                 Transform)
   from viam.gen.service.motion.v1.motion_pb2 import OrientationConstraint
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   "go.viam.com/rdk/components/arm"
   "github.com/golang/geo/r3"
   "go.viam.com/rdk/motionplan"
   "go.viam.com/rdk/referenceframe"
   "go.viam.com/rdk/services/motion"
   "go.viam.com/rdk/spatialmath"
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Within your main function, specify the name (Python) or get the `resource.Name` (Go) of the arm you want to move.
   Replace `"my_arm"` with the name of your arm in your machine's configuration:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   arm_resource_name = "my_arm"
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   armResourceName := "my_arm"
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Get the motion service, which is built into `viam-server`:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   motion_service = MotionClient.from_robot(machine, "builtin")
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   motionService, err := motion.FromProvider(machine, "builtin")
   if err != nil {
     logger.Fatal(err)
   }
   ```

   {{% /tab %}}
   {{< /tabs >}}

## Define the geometry of the environment

You must define the geometries of any objects around your arm that you want to avoid collisions with.

{{< table >}}
{{% tablestep start=1 %}}

In your code, define the geometry of each object, for example a table your arm is mounted to, or a box in the workspace.
The available geometry types are:

<!-- prettier-ignore -->
| Geometry type | Description | Dimensions to define |
| ------------- | ----------- | ------------------ |
| box           | A rectangular prism. | `x`, `y`, `z`: length in each direction in mm. |
| capsule       | A cylinder with hemispherical end caps. | `radius` in mm, overall `length` in mm. |
| sphere        | A sphere. | `radius` in mm. |
| mesh          | A 3D model defined by a mesh. | `triangles`: a list of triangles, each defined by three vertices. |

For example, to define a 120mm x 80mm x 100mm box:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
box_origin = Pose(x=400, y=0, z=50)
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
{{% tablestep %}}

Put the object into a reference frame, creating a `GeometriesInFrame` object.
This example uses the world reference frame, but you can put your object into a different reference frame depending on your application:

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
{{% tablestep %}}

If you have passive objects that are mounted on your arm but are not configured as {{< glossary_tooltip term_id="component" text="components" >}} of the machine, represent them as _transforms_ to prevent collisions.
For example, a marker mounted to the end of the arm can be represented as a transform:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Create a geometry to represent a marker as a 160mm tall, 10mm radius
# capsule. The center of the marker is 90mm from the end of the arm
# (1/2 length of marker plus 10mm radius)
marker_geometry = Geometry(
    center=Pose(x=0, y=0, z=90),
    capsule=Capsule(radius_mm=10, length_mm=160))
transforms = [
    # Create a transform called "markerTransform" and point the marker's long
    # axis along the z axis of the arm
    Transform(
        reference_frame="markerTransform",
        pose_in_observer_frame=PoseInFrame(
            reference_frame=arm_resource_name,
            pose=Pose(x=0, y=0, z=80, o_x=0, o_y=0, o_z=1, theta=0)),
        physical_object=marker_geometry)
]
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Create a geometry to represent a marker as a 160mm tall, 10mm radius
// capsule. The center of the marker is 90mm from the end of the arm
// (1/2 length of marker plus 10mm radius)
marker_geometry, _ := spatialmath.NewCapsule(
   spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 90.0}),
   10.0, 160.0, "marker_1")

// Create a transform called "markerTransform" and point the marker's long
// axis along the z axis of the arm
transform := referenceframe.NewLinkInFrame("my_arm",
   spatialmath.NewPoseFromPoint(r3.Vector{X: 0, Y: 0, Z: 80}),
   "markerTransform", marker_geometry)
transforms := []*referenceframe.LinkInFrame{transform}
```

{{% /tab %}}
{{< /tabs >}}

See [Use a transform to represent a drinking cup](/tutorials/services/constrain-motion/#use-a-transform-to-represent-a-drinking-cup) for another example.

{{% /tablestep %}}
{{% tablestep %}}

Construct a `WorldState` object, which includes the static obstacles and moving transforms:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
world_state = WorldState(obstacles=obstacles_in_frame, transforms=transforms)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
worldState, err := referenceframe.NewWorldState(obstacles, transforms)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% /table %}}

You will pass your `WorldState` object to the motion planning API in the next section.

## Move the arm

To move the arm, use the motion service API's [`Move` method](/dev/reference/apis/services/motion/#move).
Follow the steps below to construct the necessary objects and pass them to `Move`.

1. Construct a destination pose for the arm.
   Specify the reference frame of the destination pose, creating a `PoseInFrame` object.
   For example:

   {{< tabs >}}
   {{% tab name="Python" %}}

   ```python {class="line-numbers linkable-line-numbers"}
   destination_pose = Pose(x=-800.0,
                          y=-239.0,
                          z=-100.0,
                          o_x=0.0,
                          o_y=0.0,
                          o_z=1.0,
                          theta=0.0)
   destination_pose_in_frame = PoseInFrame(
      reference_frame="world",
      pose=destination_pose)
   ```

   {{% /tab %}}
   {{% tab name="Go" %}}

   ```go {class="line-numbers linkable-line-numbers"}
   destinationPose := spatialmath.NewPose(
      r3.Vector{X: -800.0, Y: -239.0, Z: -100.0},
      &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
      )
   destinationPoseInFrame := referenceframe.NewPoseInFrame("world", destinationPose)
   ```

   {{% /tab %}}
   {{< /tabs >}}

   {{% alert title="Tip" color="tip" %}}
   To get a better intuition for poses and where you want the arm to move, try driving the arm manually from the **CONTROL** tab or **TEST** panel and notice how the pose indicated in the control interface corresponds to the arm's position in the real world.

   You can also [use the **VISUALIZE** tab](/operate/reference/services/frame-system/#visualize-components-and-frames) to see a representation of your arm's geometry and reference frames.
   {{% /alert %}}

1. If you want to specify any [constraints](/operate/reference/services/motion/constraints/) for the motion, add them to a `Constraints` object:

   {{< tabs >}}
   {{% tab name="Linear constraint" %}}

To move the end of the arm in a straight line, use a linear constraint:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
constraints = Constraints(
    linear_constraint=[LinearConstraint(line_tolerance_mm=0.5)])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myConstraints := &motionplan.Constraints{
   LinearConstraint: []motionplan.LinearConstraint{motionplan.LinearConstraint{
      LineToleranceMm:          0.5,
      OrientationToleranceDegs: 0.9,
   }},
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Orientation constraint" %}}

To keep the orientation the same (within a tolerance) throughout the motion, use an orientation constraint:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
constraints = Constraints(orientation_constraint=[
   OrientationConstraint(orientation_tolerance_degs=3.0)])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myConstraints := &motionplan.Constraints{
  OrientationConstraint: []motionplan.OrientationConstraint{{3.0}},
}
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
  WorldState: worldState,
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
import asyncio

from viam.robot.client import RobotClient
from viam.services.motion import MotionClient, Constraints
from viam.components.arm import Arm
from viam.proto.common import (GeometriesInFrame, Geometry, Pose, PoseInFrame,
                               Vector3, RectangularPrism, Capsule, WorldState,
                               Transform)
from viam.gen.service.motion.v1.motion_pb2 import OrientationConstraint


async def connect():
    opts = RobotClient.Options.with_api_key(
       api_key='xxxx1234abcd1234abcd1234aaaa0000',
       api_key_id='xxxx-1234-abcd-1234-abcd1234abcd1234'
    )
    return await RobotClient.at_address('demo-main.xyzefg123.viam.cloud', opts)


async def main():
    machine = await connect()

    motion_service = MotionClient.from_robot(machine, "builtin")

    box_origin = Pose(x=400, y=0, z=50)
    box_dims = Vector3(x=120.0, y=80.0, z=100.0)
    box_object = Geometry(
        center=box_origin,
        box=RectangularPrism(dims_mm=box_dims))

    obstacles_in_frame = [GeometriesInFrame(
        reference_frame="world",
        geometries=[box_object])]

    marker_geometry = Geometry(
        center=Pose(x=0, y=0, z=90),
        capsule=Capsule(radius_mm=10, length_mm=160))
    transforms = [
        Transform(
            reference_frame="markerTransform",
            pose_in_observer_frame=PoseInFrame(
                reference_frame="my_arm",
                pose=Pose(x=0, y=0, z=80, o_x=0, o_y=0, o_z=1, theta=0)),
            physical_object=marker_geometry)
    ]

    world_state = WorldState(
        obstacles=obstacles_in_frame,
        transforms=transforms)

    destination_pose = Pose(
        x=-800,
        y=-239,
        z=-100,
        o_x=0.0,
        o_y=0.0,
        o_z=1.0,
        theta=0.0)
    destination_pose_in_frame = PoseInFrame(
        reference_frame="world",
        pose=destination_pose)

    constraints = Constraints(
        orientation_constraint=[OrientationConstraint(
            orientation_tolerance_degs=3.0)])

    await motion_service.move(
        component_name="my_arm",
        destination=destination_pose_in_frame,
        world_state=world_state,
        constraints=constraints)

    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
   "context"

   "go.viam.com/rdk/logging"
   "go.viam.com/rdk/robot/client"
   "go.viam.com/utils/rpc"
   "go.viam.com/rdk/components/arm"
   "github.com/golang/geo/r3"
   "go.viam.com/rdk/motionplan"
   "go.viam.com/rdk/referenceframe"
   "go.viam.com/rdk/services/motion"
   "go.viam.com/rdk/spatialmath"
)

func main() {
   logger := logging.NewDebugLogger("client")
   machine, err := client.New(
      context.Background(),
      "demo-main.xyzefg123.viam.cloud",
      logger,
      client.WithDialOptions(rpc.WithEntityCredentials(
         "xxxx-1234-abcd-1234-abcd1234abcd1234",
         rpc.Credentials{
            Type:    rpc.CredentialsTypeAPIKey,
            Payload: "xxxx1234abcd1234abcd1234aaaa0000",
         })),
   )
   if err != nil {
      logger.Fatal(err)
   }

   defer machine.Close(context.Background())

   armResourceName := "my_arm"
   motionService, err := motion.FromProvider(machine, "builtin")
   if err != nil {
      logger.Fatal(err)
   }

   boxPose := spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 0.0})
   boxDims := r3.Vector{X: 0.2, Y: 0.2, Z: 0.2}
   obstacle, _ := spatialmath.NewBox(boxPose, boxDims, "obstacle_1")

   geometryInFrame := referenceframe.NewGeometriesInFrame("world",
      []spatialmath.Geometry{obstacle})
   obstacles := []*referenceframe.GeometriesInFrame{geometryInFrame}

   marker_geometry, _ := spatialmath.NewCapsule(
      spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 90.0}),
      10.0, 160.0, "marker_1")

   transform := referenceframe.NewLinkInFrame("my_arm",
      spatialmath.NewPoseFromPoint(r3.Vector{X: 0, Y: 0, Z: 80}),
      "markerTransform", marker_geometry)
   transforms := []*referenceframe.LinkInFrame{transform}

   worldState, err := referenceframe.NewWorldState(obstacles, transforms)

   destinationPose := spatialmath.NewPose(
      r3.Vector{X: -800.0, Y: -239.0, Z: -100.0},
      &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
   )
   destinationPoseInFrame := referenceframe.NewPoseInFrame("world", destinationPose)

   myConstraints := &motionplan.Constraints{
      OrientationConstraint: []motionplan.OrientationConstraint{{3.0}},
   }

   moved, err := motionService.Move(context.Background(), motion.MoveReq{
      ComponentName: armResourceName,
      Destination:   destinationPoseInFrame,
      WorldState:    worldState,
      Constraints:   myConstraints,
   })
   if err != nil {
      logger.Fatal(err)
   }
   logger.Info("moved", moved)

}
```

{{% /tab %}}
{{% /tabs %}}

## More examples

The following tutorials use the motion planning service:

{{< cards >}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper/" %}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
