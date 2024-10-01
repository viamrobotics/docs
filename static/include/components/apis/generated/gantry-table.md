<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetPosition`](/appendix/apis/components/gantry/#getposition) | Get the current positions of the axis of the gantry (mm). |
| [`MoveToPosition`](/appendix/apis/components/gantry/#movetoposition) | Move the axes of the gantry to the desired positions (mm) at the requested speeds (mm/sec). |
| [`GetLengths`](/appendix/apis/components/gantry/#getlengths) | Get the lengths of the axes of the gantry (mm). |
| [`Home`](/appendix/apis/components/gantry/#home) | Run the homing sequence of the gantry to re-calibrate the axes with respect to the limit switches. |
| [`GetGeometries`](/appendix/apis/components/gantry/#getgeometries) | Get all the geometries associated with the gantry in its current configuration, in the frame of the gantry. |
| [`IsMoving`](/appendix/apis/components/gantry/#ismoving) | Get if the gantry is currently moving. |
| [`Stop`](/appendix/apis/components/gantry/#stop) | Stop all motion of the gantry. |
| [`Reconfigure`](/appendix/apis/components/gantry/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/appendix/apis/components/gantry/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`FromRobot`](/appendix/apis/components/gantry/#fromrobot) | Get the resource from the provided robot with the given name. |
| [`GetResourceName`](/appendix/apis/components/gantry/#getresourcename) | Get the `ResourceName` for this gantry with the given name. |
| [`Close`](/appendix/apis/components/gantry/#close) | Safely shut down the resource and prevent further use. |
