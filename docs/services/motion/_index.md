---
title: "Motion Service"
linkTitle: "Motion"
weight: 40
type: "docs"
description: "The Motion Service enables your robot to plan and move its components relative to itself, other robots, and the world."
tags: ["motion", "motion planning", "services"]
icon: "/services/img/icons/motion.svg"
no_list: true
# SME: Motion team
---

The Motion Service enables your robot to plan and move itself or its components relative to itself, other robots, and the world.
The Motion Service:

1. Gathers the current positions of the robot’s components as defined with the [Frame System](../frame-system/).
2. Plans the necessary motions to move a component to a given destination.

The Motion Service can:

- use motion planning algorithms locally on your robot to plan coordinated motion across many components.
- pass movement requests through to individual components which have implemented their own motion planning.

## Configuration

The Motion Service is enabled in RDK by default, and no extra configuration needs to be done in the [Viam app](https://app.viam.com/) to enable it.

You do need to configure frames for your components with the [Frame System](../frame-system/).
This defines the spacial context of your robot.

## API

Method Name | Description
----------- | -----------
[`Move`](#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`MoveSingleComponent`](#movesinglecomponent) | Move a single component "manually".
[`GetPose`](#getpose) | Get the current location and orientation of a component.

### Move

`Move` is the primary way to move multiple components, or to move any object to any other location.
Given a destination pose and a component to move to that destination, `Move` will:

1. Construct a full kinematic chain from goal to destination including all movable components in between.
2. Solve that chain to place the goal at the destination while meeting specified constraints.
3. Execute that movement to move the actual robot.
4. Return whether or not this process succeeded.

The volumes associated with all configured robot components (local and remote) will be taken into account for each request to ensure that collisions do not occur.

{{% alert title="Note" color="note" %}}

The motions planned by this API endpoint are by default **entirely unconstrained** with the exception of obeying obstacles as documented below.
This may result in motions which appear unintuitive.
To apply motion constraints (experimental), see the [`extra` parameter](#extra_anchor).

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): Name of the piece of the robot that should arrive at the destination.
  Note that this is solved such that the distal end of the component arrives at the destination.
  For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.

- `destination` ([PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)):
  Describes where the `component_name` should end up.
  Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).

  Note that the destination pose is relative to the distal end of the specified frame.
  This means that if the `destination` is the same as the `component_name` frame, for example an arm's frame, then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector by 10 mm in the local X direction.

- `world_state` ([WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState)) (*optional*): Data structure specifying information about the world around the robot.
  Used to augment the motion solving process.
  `world_state` includes obstacles and transforms:
  - **Obstacles**: Geometries located at a pose relative to some frame
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The Motion Service assumes that obstacles with mobile parents move along with their parents while solving.
      This ensures that obstacles that are temporarily attached to moving components do not cause collisions during movement.
    - Geometries are "part of" their frame, rather than at the distal end of the frame.
      Their poses are relative to the *origin* of the specified frame.
      A geometry associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} will be interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `component_name`, where poses are relative to the distal end of a frame.
  - **Transforms**: These are a list of `PoseInFrame` messages that specify arbitrary other transformations that will be ephemerally added to the frame system at solve time.
  The `destination` may be one of these, but at present the `component_name` may not be.

- `extra` (Mapping[str, Any]): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/index.html#viam.components.gripper.Gripper.open).

**Example usage:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionServiceClient.from_robot(robot=robot, name="builtin")

# Assumes a gripper configured with name "my_gripper" on the robot
my_frame = "my_gripper_offset"

goal_pose = Pose(x=0, y=0, z=300, o_x=0, o_y=0, o_z=1, theta=0)

# Move the gripper
moved = await motion.move(component_name=my_gripper, destination=PoseInFrame(reference_frame="myFrame", pose=goal_pose), world_state=worldState, constraints={}, extra={})
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

**Example usage:**

```go {class="line-numbers linkable-line-numbers"}
// Assumes a gripper configured with name "my_gripper" on the robot
myFrame := "my_gripper_offset"

goalPose := PoseInFrame(0, 0, 300, 0, 0, 1, 0)

// Move the gripper
moved, err := motion.Move(context.TODO(), goalPose, worldState, nil, nil)
```

{{% /tab %}}
{{< /tabs >}}

#### Parameters

**`component_name`**: This is the name of the piece of the robot which should arrive at the destination.
Note that this is solved such that the distal end of the component arrives at the destination.
For example, if a robotic arm is specified, the piece that will arrive at the destination is the end effector mount point, not the base of the arm where it is mounted.

**`destination`**: A `PoseInFrame` describing where the `component_name` should end up.
This can be any pose, from the perspective of any component whose location is configured as the `frame` attribute in the Viam config and is therefore known in the robot’s [Frame System](../frame-system/).
Note that the Pose specified is relative to the distal end of the frame being specified.
This means that if the `destination` and `component_name` are the same frame, for example an arm (or a gripper attached to one), then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector or gripper by 10 mm in the local X direction.

**`world_state`**: This data structure specifies various information about the world around the robot which is used to augment the motion solving process.
There are two pieces of world_state: obstacles and transforms.
Both will be discussed in detail:

- **Obstacles**: These are geometries located at a pose relative to some frame.
When solving a motion plan with movable frames that contain inherent geometries, the solved path will be constrained such that at no point will any of those inherent geometries intersect with the specified obstacles.
There are three important things to know about obstacles:
  - Obstacles will only be avoided by objects with which they are not in collision at the starting position.
    If a motion is begun and an obstacle specified such that it is in a location where it intersects with a component in the kinematic chain, collisions between that obstacle and that particular piece of the kinematic chain will not be checked.
  - Obstacles whose parents (or grand… parent) may move as part of a solve request, will be assumed to move along with their parent while solving.
    This will ensure that obstacles that are temporarily attached to moving components do not cause collisions during the movement.
  - Unlike the `destination` and `component_name` fields, where poses are relative to the most distal piece of a specified frame (for example, an arm frame will be solved for the pose of its end effector), geometries are interpreted as being "part of" their frame, rather than "at the end of" the frame.
    Thus, their poses are relative to the *origin* of the specified frame.
    A geometry associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} will be interpreted as being 10mm underneath the base of the arm, not 10mm underneath the end effector.
- **Transforms**: These are a list of *PoseInFrame* messages that specify arbitrary other transformations that will be ephemerally added to the frame system at solve time.
The `destination` may be one of these, but at present the `component_name` may not be.

<a id="extra_anchor" />**`extra`**: This data structure is a generic struct, containing maps of strings to any data structure.
This is used to pass in additional parameters not supported as first-class parameters in the API.
This enables things like the tweaking of individual parameters used by the algorithm, if the user wishes to have something other than the default.

#### Examples

The following code uses the [Viam Python SDK](https://python.viam.dev/) to move an arm to a point in front of a camera and approach that point from a particular direction:

```python {class="line-numbers linkable-line-numbers"}
# This is a robot with an arm named "myArm" and a down-pointing camera named "cam".
# The pose of the arm relative to `world` is {x=0,y=0,z=0}
# The pose of the camera relative to `world` is {x=600,y=0,z=700, o_z=-1}
motion = MotionServiceClient.from_robot(robot=robot, name="builtin")
arm_name = "myArm"

# See frame system documentation. Objects have a frame created with name
# "<name>_offset" to represent the transformation from the object's parent to the location of
# the object. The distal end of the "_offset" frame is the origin of the named frame.
arm_base = arm_name + "_offset"

# Create a geometry representing the table to which the arm is attached.
table = Geometry(center=Pose(x=0, y=0, z=-20), box=RectangularPrism(dims_mm=Vector3(x=2000, y=2000, z=40)))
tableFrame = GeometriesInFrame(reference_frame=arm_name, geometries=[table])

# Create a geometry 200mm behind the arm to block it from leaning back too much.
backboard = Geometry(center=Pose(x=-200, y=0, z=350), box=RectangularPrism(dims_mm=Vector3(x=20, y=10000, z=800)))
backboardFrame = GeometriesInFrame(reference_frame=arm_base, geometries=[backboard])

worldstate = WorldState(obstacles=[tableFrame, backboardFrame] )

# Get the Viam resource name for our arm
for resname in robot.resource_names:
    if resname.name == arm_name:
       armRes = resname

# The goal will be a point 300mm directly in front of our camera.
# The orientation of the pose will be the direction from which we will grab it.
# As the pose is given in the frame of the camera, whose orientation is o_z = -1,
# giving the pose an orientation of o_z=1 relative to the camera will mean the arm
# will move to that point with an orientation of o_z=-1 relative to `world`, which
# means that it will be pointing downwards at the goal point.
goal_pose = Pose(x=0, y=0, z=300, o_x=0, o_y=0, o_z=1, theta=0)
# Note that pieces whose values are 0 will be filled in with 0s automatically
# and can be left blank. They are shown here only for demonstration purposes.

# Move the arm. As the goal pose is relative to the camera, the arm will wind up
# with a final pose relative to `world` of {x=600,y=0,z=400, o_z=-1}
await motion.move(component_name=armRes,destination=PoseInFrame(reference_frame="cam",pose=goal_pose),world_state=worldstate, extra={})

# Create an extra param which will cause the arm to move linearly
extra = {"motion_profile": "linear", "line_tolerance": 0.2}

# Create a new goal pose. This will move the arm 150mm in its local +Z direction.
# Since the arm's orientation relative to World is o_z=-1, the arm will wind up
# with a final pose relative to `world` of {x=600,y=0,z=250, o_z=-1}
goal_pose = Pose(x=0, y=0, z=150, o_x=0, o_y=0, o_z=1, theta=0)

# Move the arm with our new command. Notice the changed destination construction.
motion.move(component_name=armRes,destination=PoseInFrame(reference_frame="myArm",pose=goal_pose),world_state=worldstate, extra=extra)

```

### MoveSingleComponent

The `MoveSingleComponent` endpoint, while it looks similar to the "Move" endpoint above, may result in radically different behavior when called.

_`MoveSingleComponent` is meant to allow the user to bypass Viam’s internal motion planning entirely, if desired, for a single component._ If the component in question supports the `MoveToPosition` method taking a Pose as a parameter, this call will use the frame system to translate the given destination into the frame of the specified component, and will then call `MoveToPosition` on that one component to move it to the desired location.
As of April 5, 2023, arms are the only component supported by this feature.

As the name of the method suggests, only the single component specified by `component_name` will move.

An example of when this may be useful is if the user has implemented their own version of an arm, and wishes to use their own motion planning for it.
That user will implement `MoveToPosition` on that arm using whatever method they desire to plan to the specified pose, and then can use this API endpoint to pass the destination in the frame of any other robot component.

{{% alert title="Note" color="note" %}} <a id="move-vs-movetoposition">

If this method is called with an arm which uses Viam’s motion planning on the backend, then this method is equivalent to using `robot.TransformPose` to transform the destination into the frame of the arm, and then calling `MoveToPosition` on the arm directly.
Note that `arm.MoveToPosition` does not use `world_state`, so collision checking and obstacle avoidance *will not* be performed.

If you need collision checking and obstacle avoidance, use [`Move`](#move).

{{% /alert %}}

#### Parameters

**`component_name`**: This is the name of the piece of the robot to which `MoveToPosition` should be called with the transformed destination.
This component must support the `MoveToPosition` API call with a Pose.
As of April 5, 2023, arm is the only component so supported.

**`destination`**: A `PoseInFrame` describing where the `component_name` should end up.
This can be any pose, from the perspective of any component whose location is known in the robot’s `FrameSystem`.
It will be converted into the frame of the component named in `component_name` when passed to `MoveToPosition`.

**`world_state`**: This data structure is structured identically to what is described above in "Move".
However, a user’s own implementation of `MoveToPosition` may or may not make use of WorldState; see <a href="#move-vs-movetoposition">note above</a>.

**`extra`**: This data structure is a generic struct, which the user can use to insert any arbitrary extra data they like to pass to their own motion planning implementation.

### GetPose

The `GetPose` method is an endpoint through which a user can query the location of a robot's component within its frame system.
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
The `supplemental_transforms` argument can be used to augment the robot's existing frame system with supplemental frames.

#### Parameters

**`component_name`**: This is the name of the piece of the robot whose pose will be returned.
The specified component must have an associated frame within the robot's frame system, or this frame must be added through the `supplemental_transforms` argument.

**`destination_frame`**: The name of the frame with respect to which the component's pose will be reported.
This frame must either exist in the robot's frame system, or this frame must be added through the `supplemental_transforms` argument.

**`supplemental_transforms`**: This argument accepts an array of `Transform` structures.
A `Transform` represents an additional frame which is added to the robot's frame system.
It consists of the following fields:

- `reference_frame`: This field specifies the name of the frame which will be added to the frame system
- `pose_in_observer_frame`: This field provides the relationship between the frame being added and another frame
- `physical_object`: An optional `Geometry` can be added to the frame being added

When `supplemental_transforms` are provided, a frame system will be created within the context of the `GetPose` function.
This new frame system will build off the robot's frame system and will incorporate the `Transforms` provided.
If the result of adding the `Transforms` will result in a disconnected frame system an error will be thrown.

**`extra`**: This data structure is a generic struct, which the user can use to insert any arbitrary extra data they wish to pass to their own motion planning implementation.
This parameter is not used for anything in the built-in Motion Service.

#### Example

The following code is a minimal example using the [Viam Python SDK](https://python.viam.dev/) to get the pose of the tip of a [gripper](../../components/gripper/) named `myGripper` which is attached to the end of an arm, in the "world" referenceframe

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionServiceClient

# Assume that the connect function is written and will return a valid robot. 
robot = await connect()

motion = MotionServiceClient.from_robot(robot=robot, name="builtin")
gripperName = Gripper.get_resource_name("myGripper")
gripperPoseInWorld = await robot.get_pose(component_name=gripperName, destination_frame="world")
```

For a more complicated example, let's take the same scenario and get the pose of the same gripper with respect to an object which is situated at a location (100, 200, 0) relative to the "world" frame:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionServiceClient
from viam.proto.common import Transform, PoseInFrame, Pose

# Assume that the connect function is written and will return a valid robot. 
robot = await connect()

motion = MotionServiceClient.from_robot(robot=robot, name="builtin")
objectPose = Pose(x=100, y=200, z=0, o_x=0, o_y=0, o_z=1, theta=0)
objectPoseInFrame = PoseInFrame(reference_frame="world", pose=objectPose)
objectTransform = Transform(reference_frame="object", pose_in_observer_frame=objectPoseInFrame)
gripperName = Gripper.get_resource_name("myGripper")
gripperPoseInObjectFrame = await motion.get_pose(
  component_name=gripperName,
  destination_frame="world",
  supplemental_transforms=objectTransform
)
```

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/services/accessing-and-moving-robot-arm" size="small" %}}
{{< /cards >}}
