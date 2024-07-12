<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`MoveStraight`](/components/base/#movestraight) | Move the base in a straight line across the given distance (mm) at the given velocity (mm/sec). |
| [`Spin`](/components/base/#spin) | Turn the base in place, rotating it to the given angle (degrees) at the given angular velocity (degrees/sec). |
| [`SetPower`](/components/base/#setpower) | Set the linear and angular power of the base, represented as a percentage of max power for each direction in the range of [-1.0 to 1.0]. |
| [`SetVelocity`](/components/base/#setvelocity) | Set the linear velocity (mm/sec) and angular velocity (degrees/sec) of the base. |
| [`GetProperties`](/components/base/#getproperties) | Get the width and turning radius of the {{< glossary_tooltip term_id="model" text="model" >}} of base in meters. |
| [`IsMoving`](/components/base/#ismoving) | Returns whether the base is actively moving (or attempting to move) under its own power. |
| [`Stop`](/components/base/#stop) | Stop the base from moving immediately. |
| [`GetGeometries`](/components/base/#getgeometries) | Get all the geometries associated with the base in its current configuration, in the frame of the base. |
| [`Reconfigure`](/components/base/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/components/base/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`FromRobot`](/components/base/#fromrobot) | Get the resource from the provided robot with the given name. |
| [`GetResourceName`](/components/base/#getresourcename) | Get the `ResourceName` for this base with the given name. |
| [`Close`](/components/base/#close) | Safely shut down the resource and prevent further use. |
