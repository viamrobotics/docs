---
title: "Arm Component"
linkTitle: "Arm"
weight: 10
type: "docs"
description: "Explanation of arm types, configuration, and usage in Viam."
# SME: Peter L
---

Arms are serial chains of joints and links, with a fixed end and an end effector end. 
The end effector is able to be placed at arbitrary cartesian positions relative to the base of the arm, and can be moved to cartesian coordinates or controlled directly via the joint positions.

As an example, to move an xArm6 whose component name is "my_xArm6" forwards in the X direction by 300mm:
```python
  	from viam.components.arm import Arm
  	from viam.proto.api.common import WorldState
 	 
  	arm = Arm.from_robot(robot=robot, name='my_xArm6')
  	pos = await arm.get_end_position()
  	pos.x += 300
  	await arm.move_to_position(pose=pos, world_state=WorldState())
```
This document will teach you how to configure, connect to, and move the arms with preprogrammed support from Viam, as well as introduce you to the steps required to implement support for any other arm.

An arm consists of movable pieces, joints, immovable pieces, and links. Joints may rotate, translate, or both, while a link will always be the same shape.

An arm can be thought of as something that can set or get joint positions, and can compute the cartesian position of its end effector(s) given its set of joint positions. 
Arms will also support moving to a specified cartesian position, something that requires inverse kinematics and motion planning to determine the ending joint positions.

The way most supported arms are set up is via a driver in Viam's RDK which is compatible with whatever software API is supported by that specific arm's manufacturer. 
This driver handles turning the arm on and off, engaging brakes as needed (if supported), querying the arm for its current joint position, and sending requests for the arm to move to a specified set of joint positions.

Arm drivers are paired with JSON files describing the kinematics parameters of each arm. 
The arm driver will load and parse the kinematics file to be used with the Frame System that is part of RDK. 
The Frame System will allow you to easily calculate where any part of your robot is relative to any other part, other robot, or piece of the environment.

All arms have a "Home" position, which corresponds to setting all joint angles to 0.

While some arms include onboard inverse kinematics, many do not. 
Most Viam RDK arm drivers bypass any onboard inverse kinematics, and use Viam's motion planning instead. 
When an arm is moved via the `move_to_position` call, it is enforced that the movement will follow a straight line, and not deviate from the start or end orientations more than the start and orientations differ from one another. 
If there is no way to move to the desired location in a straight line for the arm in question, or if it would self-collide or collide with an obstacle that was passed in as something to avoid, then the `move_to_position` call will fail.

## Features

- Linear motion planning
- Self-collision prevention
- Obstacle avoidance

## Viam Configuration:
```json-viam
{
  "components": [
	{
  	"attributes": {
    	"host": "10.0.0.97"
  	},
  	"depends_on": [],
  	"frame": {
    	"orientation": {
      	"type": "ov_degrees",
      	"value": {
        	"th": 0,
        	"x": 0,
        	"y": 0,
        	"z": 1
      	}
    	},
    	"parent": "world",
    	"translation": {
      	"x": 0,
      	"y": 0,
      	"z": 0
    	}
  	},
  	"model": "xArm6",
  	"name": "xArm6",
  	"type": "arm"
	}
  ]
}
```
### Optional Attributes:

Individual arm implementations have their own sets of configurable parameters that vary by vendor. 
For example, for an xArm6 or an xArm7, there are three parameters:

- **host**: A string representing the IP address of the arm.
  
- **speed** (Optional. Default: 20.0): A float representing the desired maximum joint movement speed in degrees/second.
  
- **acceleration** (Optional. Default: 50.0):  A float representing the desired maximum joint acceleration in degrees/second/second.


## Examples:

The following code for an xArm6 will do the following:

1. First perform a linear movement 300mm +X from its starting point, then a linear movement back to the starting point, assuming the +300mm position is within the arm's workspace. 
If you have trouble with this, try starting the arm in the home position.
1.  Next, it will define an obstacle along the straight-line path between the start and the same goal from above. 
It will then call the Viam motion service to move the arm (rather than `arm.move_to_position`), which is able to route around the hypothetical obstacle. It will return to the starting point, again routing around the obstacle.
1. Finally, it will call `arm.move_to_position` to the goal as in the first movement, but this time passing the obstacle. 
As there is no straight-line path to the goal that does not intersect the obstacle, this request will fail with a "unable to solve for position" GRPC error.
``` python
	motion_svc = MotionServiceClient.from_robot(robot, "NAME”)
  	arm = Arm.from_robot(robot=robot, name='xArm6')
  	pos = await arm.get_end_position()
 	 
  	print("~~~~TESTING ARM LINEAR MOVE~~~~~")
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x += 300
  	# Note we are passing an empty worldstate
  	await arm.move_to_position(pose=pos, world_state=WorldState())
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x -= 300
  	await asyncio.sleep(1)
  	await arm.move_to_position(pose=pos, world_state=WorldState())
 	 
  	print("~~~~TESTING MOTION SERVICE MOVE~~~~~")
 	 
  	geom = Geometry(center=Pose(x=pos.x + 150, y=pos.y, z=pos.z), box=RectangularPrism(width_mm =2, length_mm =5, depth_mm =5))
  	geomFrame = GeometriesInFrame(reference_frame="xArm6", geometries=[geom])
  	worldstate = WorldState(obstacles=[geomFrame])
 	 
  	pos = await arm.get_end_position()
  	jpos = await arm.get_joint_positions()
  	print(pos)
  	print("joints", jpos)
  	pos.x += 300
 	 
  	for resname in robot.resource_names:
    	if resname.name == "xArm6":
      	armRes = resname
 	 
  	# We pass the WorldState above with the geometry. The arm should successfully route around it.
  	await motionServ.move(component_name=armRes, destination=PoseInFrame(reference_frame="world", pose=pos), world_state=worldstate)
  	pos = await arm.get_end_position()
  	jpos = await arm.get_joint_positions()
  	print(pos)
  	print("joints", jpos)
  	pos.x -= 300
  	await asyncio.sleep(1)
  	await motionServ.move(component_name=armRes, destination=PoseInFrame(reference_frame="world", pose=pos), world_state=worldstate)
 	 
  	print("~~~~TESTING ARM MOVE- SHOULD FAIL~~~~~")
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x += 300
  	# We pass the WorldState above with the geometry. As arm.move_to_position will enforce linear motion, this should fail
  	# since there is no linear path from start to goal that does not intersect the obstacle.
  	await arm.move_to_position(pose=pos, world_state=worldstate)
```


## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/arm/index.html)

## Next Steps:

See also:

<a href="/services/motion">Viam's Motion Service</a>

