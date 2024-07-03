<!-- preserve-formatting -->
Data structure specifying information about the world around the machine.
  Used to augment the motion solving process.
  `world_state` includes obstacles and transforms:

  - **Obstacles**: Geometries located at a pose relative to some frame.
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The motion service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with _transforms_.
    - Obstacles are defined by a pose and a [geometry](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the _origin_ of the specified frame.
      Their poses are relative to the _origin_ of the specified frame.
      An obstacle associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} is interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `component_name`, where poses are relative to the distal end of a frame.
  - **Transforms**: A list of `PoseInFrame` messages that specify other transformations to temporarily add to the frame system at solve time.
    Transforms can be used to account for geometries that are attached to the robot but not configured as robot components.
    For example, you could use a transform to represent the volume of a marker held in your machine's gripper.
    Transforms are not added to the config or carried into later processes.
