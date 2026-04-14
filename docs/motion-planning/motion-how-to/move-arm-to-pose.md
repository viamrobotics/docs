---
linkTitle: "Move Arm to Pose"
title: "Move an Arm to a Target Pose"
weight: 10
layout: "docs"
type: "docs"
description: "Use the motion service to move a robot arm to a position in 3D space."
aliases:
  - /operate/mobility/move-arm/
  - /operate/mobility/move-arm/arm-motion/
  - /operate/mobility/move-arm/arm-no-code/
  - /how-tos/move-robot-arm/
  - /tutorials/motion/accessing-and-moving-robot-arm/
  - /tutorials/motion/
  - /tutorials/services/plan-motion-with-arm-gripper/
---

You have a robot arm and need to move it to a specific position and orientation
in 3D space. The motion service computes a collision-free path from the arm's
current pose to the target, taking into account the frame system, kinematics,
and any defined obstacles.

## Prerequisites

- A running machine connected to Viam with an arm component configured
- [Frame system](/motion-planning/frame-system/) configured for the arm
- (Optional) [Obstacles](/motion-planning/obstacles/) defined for collision
  avoidance

## Steps

### 1. Connect and get the motion service

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.robot.client import RobotClient
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose

machine = await RobotClient.at_address(
    "<MACHINE-ADDRESS>",
    RobotClient.Options.with_api_key(
        api_key="<API-KEY>",
        api_key_id="<API-KEY-ID>"
    )
)

motion_service = MotionClient.from_robot(machine, "builtin")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "go.viam.com/rdk/services/motion"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/spatialmath"
    "github.com/golang/geo/r3"
)

motionService, err := motion.FromProvider(machine, "builtin")
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Define the target pose

A pose specifies position (x, y, z in mm) and orientation. The `reference_frame`
determines which coordinate system the pose is expressed in.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Move to a position 300mm right, 200mm forward, 400mm up
# Orientation: end effector pointing straight down
destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=300, y=200, z=400, o_x=0, o_y=0, o_z=-1, theta=0)
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Move to a position 300mm right, 200mm forward, 400mm up
// Orientation: end effector pointing straight down
destination := referenceframe.NewPoseInFrame("world",
    spatialmath.NewPose(
        r3.Vector{X: 300, Y: 200, Z: 400},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: -1, Theta: 0},
    ))
```

{{% /tab %}}
{{< /tabs >}}

### 3. Move the arm

{{< tabs >}}
{{% tab name="Python" %}}

```python
await motion_service.move(
    component_name="my-arm",
    destination=destination,
)
print("Arm moved to target pose")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
})
if err != nil {
    logger.Fatal(err)
}
fmt.Println("Arm moved to target pose")
```

{{% /tab %}}
{{< /tabs >}}

### 4. Move with obstacle avoidance

Pass a `WorldState` with obstacles to plan collision-free paths.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Vector3, RectangularPrism, Geometry,
    GeometriesInFrame, WorldState
)

# Define a table obstacle
table = Geometry(
    center=Pose(x=0, y=0, z=-20),
    box=RectangularPrism(dims_mm=Vector3(x=800, y=600, z=40)),
    label="table"
)

obstacles = GeometriesInFrame(
    reference_frame="world",
    geometries=[table]
)
world_state = WorldState(obstacles=[obstacles])

await motion_service.move(
    component_name="my-arm",
    destination=destination,
    world_state=world_state
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
tableOrigin := spatialmath.NewPose(
    r3.Vector{X: 0, Y: 0, Z: -20},
    &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0},
)
table, _ := spatialmath.NewBox(tableOrigin,
    r3.Vector{X: 800, Y: 600, Z: 40}, "table")

obstaclesInFrame := referenceframe.NewGeometriesInFrame(
    referenceframe.World, []spatialmath.Geometry{table})
worldState, _ := referenceframe.NewWorldState(
    []*referenceframe.GeometriesInFrame{obstaclesInFrame}, nil)

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
    WorldState:    worldState,
})
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

### 5. Verify the result

Read the arm's current pose after moving to confirm it reached the target:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm

arm = Arm.from_robot(machine, "my-arm")
current_pose = await arm.get_end_position()
print(f"Current position: x={current_pose.x:.1f}, "
      f"y={current_pose.y:.1f}, z={current_pose.z:.1f}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import "go.viam.com/rdk/components/arm"

myArm, err := arm.FromProvider(machine, "my-arm")
if err != nil {
    logger.Fatal(err)
}
currentPose, err := myArm.EndPosition(ctx, nil)
if err != nil {
    logger.Fatal(err)
}
pt := currentPose.Point()
fmt.Printf("Current position: x=%.1f, y=%.1f, z=%.1f\n",
    pt.X, pt.Y, pt.Z)
```

{{% /tab %}}
{{< /tabs >}}

## Test from the command line

You can move the arm and check poses without writing code:

```sh
# Check the arm's current pose
viam machines part motion get-pose --part "my-machine-main" --component "my-arm"

# Move the arm to a new position (only specified values change)
viam machines part motion set-pose --part "my-machine-main" --component "my-arm" \
  --x 300 --y 200 --z 400
```

## Troubleshooting

{{< expand "Move fails with 'no path found'" >}}

- Check that the target pose is reachable (within the arm's workspace).
- If using obstacles, verify they don't block all possible paths.
- Check joint limits in the kinematics model.
- Try a simpler target pose (closer to current position) to isolate the issue.

{{< /expand >}}

{{< expand "Arm moves to wrong position" >}}

- Verify the `reference_frame` in your destination. A pose in `"world"` frame
  and the same pose in `"my-arm"` frame are different positions.
- Check the frame system configuration. Incorrect translations or orientations
  shift the target.
- Read the arm's position before and after to see what actually changed.

{{< /expand >}}

## What's Next

- [Move with Constraints](/motion-planning/motion-how-to/move-arm-with-constraints/):
  keep the end effector on a straight line or at a fixed orientation.
- [Avoid Obstacles](/motion-planning/motion-how-to/avoid-obstacles/):
  detailed obstacle configuration for complex workspaces.
- [Pick an Object](/motion-planning/motion-how-to/pick-an-object/):
  combine motion planning with vision and gripper control.
