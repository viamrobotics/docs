<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`GetEndPosition`](/components/arm/#getendposition) | Get the current position of the arm as a [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose).
[`MoveToPosition`](/components/arm/#movetoposition) | Move the end of the arm to the desired [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose), relative to the base of the arm.
[`MoveToJointPositions`](/components/arm/#movetojointpositions) | Move each joint on the arm to the position specified in `positions`.
[`GetJointPositions`](/components/arm/#getjointpositions) | Get the current position of each joint on the arm.
[`GetKinematics`](/components/arm/#getkinematics) | Get the kinematics information associated with the arm as the format and byte contents of the [kinematics file](/internals/kinematic-chain-config/).
[`IsMoving`](/components/arm/#ismoving) | Get if the arm is currently moving.
[`Stop`](/components/arm/#stop) | Stop all motion of the arm.
[`GetGeometries`](/components/arm/#getgeometries) | Get all the geometries associated with the arm in its current configuration, in the [frame](/mobility/frame-system/) of the arm.
[`Reconfigure`](/components/arm/#reconfigure) | Reconfigure this resource.
[`DoCommand`](/components/arm/#docommand) | Execute model-specific commands that are not otherwise defined by the component API.
[`Close`](/components/arm/#close) | Safely shut down the resource and prevent further use.
