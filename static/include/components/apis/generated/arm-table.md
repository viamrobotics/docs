<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetEndPosition`](/reference/apis/components/arm/#getendposition) | Get the current position of the arm as a pose. |
| [`MoveToPosition`](/reference/apis/components/arm/#movetoposition) | Move the end of the arm in a straight line to the desired pose, relative to the base of the arm. |
| [`MoveToJointPositions`](/reference/apis/components/arm/#movetojointpositions) | Move each joint on the arm to the position specified in `positions`. |
| [`MoveThroughJointPositions`](/reference/apis/components/arm/#movethroughjointpositions) | Move the arm's joints through the given positions in the order they are specified. |
| [`GetJointPositions`](/reference/apis/components/arm/#getjointpositions) | Get the current position of each joint on the arm. |
| [`Get3DModels`](/reference/apis/components/arm/#get3dmodels) | Get the 3D models of the arm. |
| [`GetKinematics`](/reference/apis/components/arm/#getkinematics) | Get the kinematics information associated with the arm as the format and byte contents of the kinematics file. |
| [`IsMoving`](/reference/apis/components/arm/#ismoving) | Get if the arm is currently moving. |
| [`Stop`](/reference/apis/components/arm/#stop) | Stop all motion of the arm. |
| [`GetGeometries`](/reference/apis/components/arm/#getgeometries) | Get all the geometries associated with the arm in its current configuration, in the frame of the arm. |
| [`Reconfigure`](/reference/apis/components/arm/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/reference/apis/components/arm/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`GetResourceName`](/reference/apis/components/arm/#getresourcename) | Get the `ResourceName` for this arm. |
| [`Close`](/reference/apis/components/arm/#close) | Safely shut down the resource and prevent further use. |
