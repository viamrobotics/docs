---
title: "Motion Service"
linkTitle: "Motion"
weight: 20
type: "docs"
description: "Explanation of the motion service, its configuration, its functionality, and its interfaces."
---
Viam’s Motion Service enables your robot to plan and move itself or its components relative to itself, other robots, and the world. The Motion Service brings together information gathered from the robot’s components regarding their current positions with the layout of components in the frame system, and enables planning of the necessary motions to move a component to a given destination.

The Motion Service is capable of using motion planning algorithms locally on your robot to plan coordinated motion across many components, and is also capable of passing through movement requests to individual components which have implemented their own motion planning.


## Configuration

Viam’s Motion Service is enabled in RDK by default, and no extra configuration needs to be done in the [Viam app](https://app.viam.com/).


## How to Move Components


### Move

The “Move” endpoint is the primary way to move multiple components, or to move any object to any other location. Given a destination pose and a component to move to that destination, the motion service will construct a full kinematic chain from goal to destination including all movable components in between, and will solve that chain to place the goal at the destination while meeting specified constraints. It will then execute that movement to move the actual robot, and return whether or not this process succeeded.

{{% alert title="Note" color="note" %}} 
The motions planned by this API endpoint are by default **entirely unconstrained** with the exception of obeying obstacles and interaction spaces as documented below. This may result in motions which appear unintuitive. To apply motion constraints, see the [`extra` parameter](#extra_anchor).
{{% /alert %}}

#### Parameters

**`component_name`**: This is the name of the piece of the robot which should arrive at the destination. Note that this is solved such that the distal end of the component arrives at the destination. For example, if a robotic arm is specified, the piece that will arrive at the destination is the end effector mount point, not the base of the arm where it is mounted.

**`destination`**: A `PoseInFrame` describing where the `component_name` should end up. This can be any pose, from the perspective of any component whose location is known in the robot’s FrameSystem (i.e., it has a `frame` attribute in the Viam config). Note that the Pose specified is relative to the distal end of the frame being specified. This means that if the `_destination`_ and `_component_name`_ are the same frame. For example an arm (or a gripper attached to one), then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector or gripper by 10 mm in the local X direction.

**`world_state`**: This data structure specifies various information about the world around the robot which is used to augment the motion solving process. There are three pieces of world_state: obstacles, interaction spaces, and transforms. Each will be discussed in detail:
* **Obstacles**: These are geometries located at a pose relative to some frame. When solving a motion plan with movable frames that contain inherent geometries, the solved path will be constrained such that at no point will any of those inherent geometries intersect with the specified obstacles. There are three important things to know about obstacles:
    * Obstacles will only be avoided by objects with which they are not in collision at the starting position. If a motion is begun and an obstacle specified such that it is in a location where it intersects with a component in the kinematic chain, collisions between that obstacle and that particular piece of the kinematic chain will not be checked.
    * Obstacles whose parents (or grand… parent) may move as part of a solve request, will be assumed to move along with their parent while solving. This will ensure that obstacles that are temporarily attached to moving components do not cause collisions during the movement.
    * Unlike the `destination` and `component_name` fields, where poses are relative to the most distal piece of a specified frame (i.e., an arm frame will be solved for the pose of its end effector), geometries are interpreted as being “part of” their frame, rather than “at the end of” the frame. Thus, their poses are relative to the _origin_ of the specified frame. A geometry given in the frame of the arm with a pose of {X: 0, Y: 0, Z: -10} will be interpreted as being 10mm underneath the base of the arm, not 10mm underneath the end effector.
* **Interaction spaces**: These are geometries which are effectively the inverse of obstacles- they specify where the inherent geometries of a kinematics chain *may* exist, and disallow them from exiting that geometry. Interaction spaces should fully envelop the geometries of any movable component with geometries. If any movable geometry is outside the given interaction space at the start of the motion, the movement will fail as the constraint will have been violated.
* **Transforms**: These are a list of _PoseInFrame_ messages that specify arbitrary other transformations that will be ephemerally added to the frame system at solve time. The _`destination`_ may be one of these, but at present the _`component_name`_ may not be.

<a id="extra_anchor" />**`extra`**: This data structure is a generic struct, containing maps of strings to any data structure. This is used to pass in additional parameters not supported as first-class parameters in the API. This enables things like the tweaking of individual parameters used by the algorithm, if the user wishes to have something other than the default.


#### Examples

The following code uses the [Viam Python SDK](https://python.viam.dev/) to move an arm to a point in front of a camera and approach that point from a particular direction:


```python
// This is a robot with an arm named "myArm" and a down-pointing camera named "cam".
// The pose of the arm relative to `world` is {x=0,y=0,z=0}
// The pose of the camera relative to `world` is {x=600,y=0,z=700, o_z=-1}
motion = MotionServiceClient.from_robot(robot=robot, name="builtin")
arm_name = "myArm"

// See frame system documentation. Objects have a frame created with name 
// "<name>_offset" to represent the transformation from the object's parent to the location of 
// the object. The distal end of the "_offset" frame is the origin of the named frame.
arm_base = arm_name + "_offset"

// create a geometry representing the table to which the arm is attached
table = Geometry(center=Pose(x=0, y=0, z=-20), box=RectangularPrism(dims_mm=Vector3(x=2000, y=2000, z=40)))
tableFrame = GeometriesInFrame(reference_frame=arm_name, geometries=[table])

// create a geometry 200mm behind the arm to block it from leaning back too much
backboard = Geometry(center=Pose(x=-200, y=0, z=350), box=RectangularPrism(dims_mm=Vector3(x=20, y=10000, z=800)))
backboardFrame = GeometriesInFrame(reference_frame=arm_base, geometries=[backboard])

worldstate = WorldState(obstacles=[tableFrame, backboardFrame] )

// Get the viam resource name for our arm
for resname in robot.resource_names:
    if resname.name == arm_name:
       armRes = resname

// the goal will be a point 300mm directly in front of our camera
// The orientation of the pose will be the direction from which we will grab it.
// As the pose is given in the frame of the camera, whose orientation is o_z = -1,
// giving the pose an orientation of o_z=1 relative to the camera will mean the arm
// will move to that point with an orientation of o_z=-1 relative to `world`, which
// means that it will be pointing downwards at the goal point.
goal_pose = Pose(x=0, y=0, z=300, o_x=0, o_y=0, o_z=1, theta=0)
// note that pieces whose values are 0 will be filled in with 0s automatically
// and can be left blank. They are shown here only for demonstration purposes.

// Move the arm. As the goal pose is relative to the camera, the arm will wind up
// with a final pose relative to `world` of {x=600,y=0,z=400, o_z=-1}
await motion.move(component_name=armRes,destination=PoseInFrame(reference_frame="cam",pose=goal_pose),world_state=worldstate, extra={})

// create an extra param which will cause the arm to move linearly
extra = {"motion_profile": "linear", "line_tolerance": 0.2}

// Create a new goal pose. This will move the arm 150mm in its local +Z direction.
// Since the arm's orientation relative to World is o_z=-1, the arm will wind up
// with a final pose relative to `world` of {x=600,y=0,z=250, o_z=-1}
goal_pose = Pose(x=0, y=0, z=150, o_x=0, o_y=0, o_z=1, theta=0)

// Move the arm with our new command. Notice the changed destination construction
motion.move(component_name=armRes,destination=PoseInFrame(reference_frame="myArm",pose=goal_pose),world_state=worldstate, extra=extra)

```


### MoveSingleComponent

The `MoveSingleComponent` endpoint, while it looks very similar to the “Move” endpoint above, may result in radically different behavior when called.

_`MoveSingleComponent` is meant to allow the user to bypass Viam’s internal motion planning entirely, if desired, for a single component._ If the component in question supports the `MoveToPosition` method taking a Pose as a parameter, this call will use the frame system to translate the given destination into the frame of the specified component, and will then call `MoveToPosition` on that one component to move it to the desired location. As of 10 October 2022, arms are the only component supported by this feature.

As the name of the method suggests, only the single component specified by `component_name` will move.

An example of when this may be useful is if the user has implemented their own version of an arm, and wishes to use their own motion planning for it. That user will implement `MoveToPosition` on that arm using whatever method they desire to plan to the specified pose, and then can use this API endpoint to pass the destination in the frame of any other robot component.

If this method is called with an arm which uses Viam’s motion planning on the backend, then this method is equivalent to using `robot.TransformPose` to transform the destination into the frame of the arm, and then calling `MoveToPosition` on the arm directly.


#### Parameters

**`component_name`**: This is the name of the piece of the robot to which `MoveToPosition` should be called with the transformed destination. This component must support the `MoveToPosition`API call with a Pose. As of 10 October 2022, Arm is the only component so supported.

**`destination`**: A `PoseInFrame` describing where the `component_name` should end up. This can be any pose, from the perspective of any component whose location is known in the robot’s `FrameSystem`. It will be converted into the frame of the component named in `component_name` when passed to `MoveToPosition`.

**`world_state`**: This data structure is structured identically to what is described above in “Move”, and is intended to behave the same. However, a user’s own implementation of `MoveToPosition` may or may not make use of World State.

**`extra`**: This data structure is a generic struct, which the user can use to insert any arbitrary extra data they like to pass to their own motion planning implementation.


## Constraints

Currently (10 October 2022), there is no built in, top level way to specify different constraints. However, several have been pre-programmed and are accessible when using the Go RDK or the Python SDK by passing a string naming the constraint to “motion_profile” via the `extra` parameter, along with individual algorithm variables. This is not available in the Viam app. Available constraints all control the topological movement of the moving component along its path.

For a usage example, see [sample code above](#examples).

The available constraints are:

#### **{"motion_profile": "linear"}**

This forces the path taken by `component_name` to follow an exact linear path from the start to the goal. If the start and goal orientations are different, the orientation along the path will follow the quaternion Slerp (Spherical Linear Interpolation) of the orientation from start to goal. This has the following sub-options:


<table>
  <tr>
   <td><strong>Parameter Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Default</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>line_tolerance
   </td>
   <td>float
   </td>
   <td>0.1
   </td>
   <td>Max linear deviation from straight-line between start and goal, in mm.
   </td>
  </tr>
  <tr>
   <td>orient_tolerance
   </td>
   <td>float
   </td>
   <td>0.05
   </td>
   <td>Allowable deviation from Slerp between start/goal orientations, unit is the norm of the R3AA between start and goal.
   </td>
  </tr>
</table>



#### **{"motion_profile": "pseudolinear"}**

This restricts the path such that it will deviate from the straight-line linear path between start and goal by no more than a certain amount, where that amount is determined as a percentage of the distance from start to goal. Linear and orientation deviation are determined separately, so if a motion has a large linear difference but has identical starting and ending orientations, the motion will hold its orientation constant while allowing some linear deflection. This has the following suboption:


<table>
  <tr>
   <td><strong>Parameter Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Default</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>tolerance
   </td>
   <td>float
   </td>
   <td>0.8
   </td>
   <td>Allowable linear and orientation deviation from direct interpolation path, as a proportion of the linear and orientation distances between start and goal.
   </td>
  </tr>
</table>



#### **{"motion_profile": "orientation"}**

This places a restriction on the orientation change during a motion, such that the orientation during the motion does not deviate from the Slerp between start and goal by more than a set amount. This is similar to the “orient_tolerance” option in the linear profile, but without any path restrictions. If set to zero, a movement with identical starting and ending orientations will hold that orientation throughout the movement.


<table>
  <tr>
   <td><strong>Parameter Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Default</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>tolerance
   </td>
   <td>float
   </td>
   <td>0.05
   </td>
   <td>Allowable deviation from Slerp between start/goal orientations, unit is the norm of the R3AA between start and goal.
   </td>
  </tr>
</table>



#### **{"motion_profile": "free"}**

This places no restrictions on motion whatsoever. This is the default and will be used if nothing is passed. This takes no parameters.


## Planning Algorithms



* CBiRRT

Currently (10 October 2022), the only algorithm available for use is CBiRRT, which stands for Constrained, Bidirectional implementation of <a href="https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree" target="_blank">RRT</a>[^CBiRRT]. It will create paths which are guaranteed to conform to specified constraints, and attempt to smooth them afterwards as needed. By default, it will use a “free” constraint, that is, it will not constrain the path of motion at all. This is to ensure that paths will be found when using defaults, even in highly constrained scenarios.

The algorithm used by Viam is based on the algorithm described in this paper: <a href="https://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf" target="_blank">ht<span></span>tps://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf]</a>

[^CBiRRT]: CBiRRT: <a href="https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Rapidly-exploring_random_tree</a>