<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetEndPosition`](/appendix/apis/components/arm/#getendposition) | Get the current position of the arm as a pose. |
| [`MoveToPosition`](/appendix/apis/components/arm/#movetoposition) | Move the end of the arm to the desired pose, relative to the base of the arm. |
| [`MoveToJointPositions`](/appendix/apis/components/arm/#movetojointpositions) | Move each joint on the arm to the position specified in `positions`. |
| [`GetJointPositions`](/appendix/apis/components/arm/#getjointpositions) | Get the current position of each joint on the arm. |
| [`GetKinematics`](/appendix/apis/components/arm/#getkinematics) | Get the kinematics information associated with the arm as the format and byte contents of the kinematics file. |
| [`IsMoving`](/appendix/apis/components/arm/#ismoving) | Get if the arm is currently moving. |
| [`Stop`](/appendix/apis/components/arm/#stop) | Stop all motion of the arm. |
| [`GetGeometries`](/appendix/apis/components/arm/#getgeometries) | Get all the geometries associated with the arm in its current configuration, in the frame of the arm. |
| [`Reconfigure`](/appendix/apis/components/arm/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/appendix/apis/components/arm/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`GetResourceName`](/appendix/apis/components/arm/#getresourcename) | Get the `ResourceName` for this arm with the given name. |
| [`Close`](/appendix/apis/components/arm/#close) | Safely shut down the resource and prevent further use. |
