<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetPosition`](/reference/apis/components/gantry/#getposition) | Get the current positions of the axis of the gantry (mm). |
| [`MoveToPosition`](/reference/apis/components/gantry/#movetoposition) | Move the axes of the gantry to the desired positions (mm) at the requested speeds (mm/sec). |
| [`GetLengths`](/reference/apis/components/gantry/#getlengths) | Get the lengths of the axes of the gantry (mm). |
| [`Home`](/reference/apis/components/gantry/#home) | Run the homing sequence of the gantry to re-calibrate the axes with respect to the limit switches. |
| [`GetGeometries`](/reference/apis/components/gantry/#getgeometries) | Get all the geometries associated with the gantry in its current configuration, in the frame of the gantry. |
| [`IsMoving`](/reference/apis/components/gantry/#ismoving) | Get if the gantry is currently moving. |
| [`Stop`](/reference/apis/components/gantry/#stop) | Stop all motion of the gantry. |
| [`Reconfigure`](/reference/apis/components/gantry/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/reference/apis/components/gantry/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`GetKinematics`](/reference/apis/components/gantry/#getkinematics) | Get the kinematics information associated with the gantry. |
| [`GetResourceName`](/reference/apis/components/gantry/#getresourcename) | Get the `ResourceName` for this gantry. |
| [`Close`](/reference/apis/components/gantry/#close) | Safely shut down the resource and prevent further use. |
