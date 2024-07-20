<!-- prettier-ignore -->
| Method Name | Description | micro-RDK Support |
| ----------- | ----------- | ----------------- |
| [`Move`](/components/servo/#move) | Move the servo to the desired angle in degrees. | Yes |
| [`GetPosition`](/components/servo/#getposition) | Get the current set angle of the servo in degrees. | Yes |
| [`GetGeometries`](/components/servo/#getgeometries) | Get all the geometries associated with the servo in its current configuration, in the frame of the servo. | No |
| [`IsMoving`](/components/servo/#ismoving) | Returns whether the servo is actively moving (or attempting to move) under its own power. | No |
| [`Stop`](/components/servo/#stop) | Stop the servo from moving. | Yes |
| [`Reconfigure`](/components/servo/#reconfigure) | Reconfigure this resource. | No |
| [`DoCommand`](/components/servo/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | Yes |
| [`FromRobot`](/components/servo/#fromrobot) | Get the resource from the provided robot with the given name. | No |
| [`GetResourceName`](/components/servo/#getresourcename) | Get the `ResourceName` for this servo with the given name. | No |
| [`Close`](/components/servo/#close) | Safely shut down the resource and prevent further use. | No |
