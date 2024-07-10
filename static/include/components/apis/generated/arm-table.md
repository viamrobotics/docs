<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetEndPosition`](/components/arm/#getendposition) | Get the current position of the arm as a pose. |
| [`MoveToPosition`](/components/arm/#movetoposition) | Move the end of the arm to the desired pose, relative to the base of the arm. |
| [`MoveToJointPositions`](/components/arm/#movetojointpositions) | Move each joint on the arm to the position specified in `positions`. |
| [`GetJointPositions`](/components/arm/#getjointpositions) | Get the current position of each joint on the arm. |
| [`GetKinematics`](/components/arm/#getkinematics) | Get the kinematics information associated with the arm as the format and byte contents of the kinematics file. |
| [`IsMoving`](/components/arm/#ismoving) | Get if the arm is currently moving. |
| [`Stop`](/components/arm/#stop) | Stop all motion of the arm. |
| [`GetGeometries`](/components/arm/#getgeometries) | Get all the geometries associated with the arm in its current configuration, in the frame of the arm. |
| [`Reconfigure`](/components/arm/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/components/arm/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`FromRobot`](/components/arm/#fromrobot) | Get the resource from the provided robot with the given name. |
| [`Name`](/components/arm/#name) | Get the `ResourceName` for this arm with the given name. |
| [`Close`](/components/arm/#close) | Safely shut down the resource and prevent further use. |
