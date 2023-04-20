---
title: "Motion Service"
linkTitle: "Motion"
weight: 40
type: "docs"
description: "The Motion Service enables your robot to plan and move its components relative to itself, other robots, and the world."
tags: ["motion", "motion planning", "services"]
icon: "/services/img/icons/motion.svg"
# SME: Peter Lo Verso
---
The Motion Service enables your robot to plan and move itself or its components relative to itself, other robots, and the world.
The Motion Service brings together information gathered from the robot’s components regarding their current positions with the layout of components in the frame system, and enables planning of the necessary motions to move a component to a given destination.

The Motion Service is capable of using motion planning algorithms locally on your robot to plan coordinated motion across many components, and is also capable of passing through movement requests to individual components which have implemented their own motion planning.

## Configuration

Viam’s Motion Service is enabled in RDK by default, and no extra configuration needs to be done in the [Viam app](https://app.viam.com/) to enable it.

## API Methods

### Move

The "Move" endpoint is the primary way to move multiple components, or to move any object to any other location.
Given a destination pose and a component to move to that destination, the Motion Service will construct a full kinematic chain from goal to destination including all movable components in between, and will solve that chain to place the goal at the destination while meeting specified constraints.
It will then execute that movement to move the actual robot, and return whether or not this process succeeded.
The volumes associated with all configured robot components (local and remote) will be taken into account for each request to ensure that collisions do not occur.

{{% alert title="Note" color="note" %}}
The motions planned by this API endpoint are by default **entirely unconstrained** with the exception of obeying obstacles as documented below.
This may result in motions which appear unintuitive.
To apply motion constraints (experimental), see the [`extra` parameter](#extra_anchor).
{{% /alert %}}

#### Parameters

**`component_name`**: This is the name of the piece of the robot which should arrive at the destination.
Note that this is solved such that the distal end of the component arrives at the destination.
For example, if a robotic arm is specified, the piece that will arrive at the destination is the end effector mount point, not the base of the arm where it is mounted.

**`destination`**: A `PoseInFrame` describing where the `component_name` should end up.
This can be any pose, from the perspective of any component whose location is configured as the `frame` attribute in the Viam config and is therefore known in the robot’s FrameSystem.
Note that the Pose specified is relative to the distal end of the frame being specified.
This means that if the `destination` and `component_name` are the same frame.
For example an arm (or a gripper attached to one), then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector or gripper by 10 mm in the local X direction.

**`world_state`**: This data structure specifies various information about the world around the robot which is used to augment the motion solving process.
There are two pieces of world_state: obstacles and transforms.
Both will be discussed in detail:

* **Obstacles**: These are geometries located at a pose relative to some frame.
When solving a motion plan with movable frames that contain inherent geometries, the solved path will be constrained such that at no point will any of those inherent geometries intersect with the specified obstacles.
There are three important things to know about obstacles:
  * Obstacles will only be avoided by objects with which they are not in collision at the starting position.
    If a motion is begun and an obstacle specified such that it is in a location where it intersects with a component in the kinematic chain, collisions between that obstacle and that particular piece of the kinematic chain will not be checked.
  * Obstacles whose parents (or grand… parent) may move as part of a solve request, will be assumed to move along with their parent while solving.
    This will ensure that obstacles that are temporarily attached to moving components do not cause collisions during the movement.
  * Unlike the `destination` and `component_name` fields, where poses are relative to the most distal piece of a specified frame (for example, an arm frame will be solved for the pose of its end effector), geometries are interpreted as being "part of" their frame, rather than "at the end of" the frame.
    Thus, their poses are relative to the _origin_ of the specified frame.
    A geometry associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} will be interpreted as being 10mm underneath the base of the arm, not 10mm underneath the end effector.
* **Transforms**: These are a list of _PoseInFrame_ messages that specify arbitrary other transformations that will be ephemerally added to the frame system at solve time.
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
Note that `arm.MoveToPosition` does not use `world_state`, so collision checking and obstacle avoidance _will not_ be performed.

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

* `reference_frame`: This field specifies the name of the frame which will be added to the frame system
* `pose_in_observer_frame`: This field provides the relationship between the frame being added and another frame
* `physical_object`: An optional `Geometry` can be added to the frame being added

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

## Motion Profile Constraints

Currently (October 18, 2022), there is no built in, top level way to specify different constraints.
However, several have been pre-programmed and are accessible when using the Go RDK or the Python SDK by passing a string naming the constraint to "motion_profile" inside the `extra` parameter, along with individual algorithm variables.
This is not available in the Viam app.
Available constraints all control the topological movement of the moving component along its path.

For a usage example, see [sample code above](#examples).

The available constraints--linear, psuedolinear, orientation, and free--are covered in the following sub-sections.

{{% alert title="Note" %}}
The motion profile constraints passed using the `extra` parameter are experimental features.
Stability is not guaranteed.
{{% /alert %}}

### Linear Constraint

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

### Pseudolinear Constraint

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

### Orientation Constraint

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

### Free Constraint

The free constraint (`{"motion_profile": "free"}`) places no restrictions on motion whatsoever.
This is the default and will be used if nothing is passed.
This profile takes no parameters.

**Example usage**:

``` python
extra = {"motion_profile": "free"}
```

## Planning Algorithms

Viam implements two planning algorithms, both based in principle on [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree).

### RRT*-Connect

RRT*-Connect is an asypmptotically optimal planner that samples the planning space randomly, connecting viable paths as it finds them.
It will continue sampling after it finds its first valid path, and if it finds future paths that are more efficient, it will update to report those instead.
For Viam, efficiency/path quality is measured in terms of total kinematics state excursion.
For an arm, this refers to joints; the total amount of joint change will be minimized.
For a gantry, this refers to the amount of linear movement.
This algorithm is able to route around obstacles, but is unable to satisfy topological constraints.

### CBiRRT

CBiRRT stands for Constrained, Bidirectional implementation of [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree).
It will create paths which are guaranteed to conform to specified constraints, and attempt to smooth them afterwards as needed.
By default, it will use a "free" constraint, that is, it will not constrain the path of motion at all.
This is to ensure that paths will be found when using defaults.
CBiRRT will return the first valid path that it finds.
The CBiRRT algorithm used by Viam is based on the algorithm described in this paper: <https://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf>

By default, Viam uses a hybrid approach.
First, RRT*-Connect is run for 1.5 seconds.
If a path is not returned, then CBiRRT is called to attempt to find a path, as it takes a more incremental approach which tends to be more likely to find paths in more difficult, constrained scenarios.
If CBiRRT is successful, then this path will be returned.
If unsuccessful, an error is returned.
However, if RRT*-Connect is initially successful, the path will be evaluated for optimality.
If the total amount of joint excursion is more than double the minimum possible to go directly to the best Inverse Kinematics solution, then CBiRRT will be run to attempt to get a better path than what RRT*-Connect was able to create.
The two paths will be smoothed, then compared to one another, and the most optimal path will be returned.

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/services/accessing-and-moving-robot-arm" size="small" %}}
{{< /cards >}}
