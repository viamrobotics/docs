<!-- prettier-ignore -->
| Method Name | Description | micro-RDK Support |
| ----------- | ----------- | ----------------- |
| [`MoveStraight`](/components/base/#movestraight) | Move the base in a straight line across the given distance (mm) at the given velocity (mm/sec). | No |
| [`Spin`](/components/base/#spin) | Turn the base in place, rotating it to the given angle (degrees) at the given angular velocity (degrees/sec). | No |
| [`SetPower`](/components/base/#setpower) | Set the linear and angular power of the base, represented as a percentage of max power for each direction in the range of [-1.0 to 1.0]. | Yes |
| [`SetVelocity`](/components/base/#setvelocity) | Set the linear velocity (mm/sec) and angular velocity (degrees/sec) of the base. | No |
| [`GetProperties`](/components/base/#getproperties) | Get the width and turning radius of the {{< glossary_tooltip term_id="model" text="model" >}} of base in meters. | No |
| [`IsMoving`](/components/base/#ismoving) | Returns whether the base is actively moving (or attempting to move) under its own power. | No |
| [`Stop`](/components/base/#stop) | Stop the base from moving immediately. | Yes |
| [`GetGeometries`](/components/base/#getgeometries) | Get all the geometries associated with the base in its current configuration, in the frame of the base. | No |
| [`Reconfigure`](/components/base/#reconfigure) | Reconfigure this resource. | No |
| [`DoCommand`](/components/base/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | Yes |
| [`FromRobot`](/components/base/#fromrobot) | Get the resource from the provided robot with the given name. | No |
| [`GetResourceName`](/components/base/#getresourcename) | Get the `ResourceName` for this base with the given name. | No |
| [`Close`](/components/base/#close) | Safely shut down the resource and prevent further use. | No |
