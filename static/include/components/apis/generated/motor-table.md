<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`SetPower`](/components/motor/#setpower) | Set the portion of max power to send to the motor (between `-1` and `1`). |
| [`SetRPM`](/components/motor/#setrpm) | Spin the motor indefinitely at the specified speed, in revolutions per minute. If `rpm` is positive, the motor will spin forwards, and if `rpm` is negative, the motor will spin backwards. |
| [`GoFor`](/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified revolutions per minute. |
| [`GoTo`](/components/motor/#goto) | Turn the motor to a specified position (in terms of revolutions from home/zero) at a specified speed in revolutions per minute (RPM). |
| [`ResetZeroPosition`](/components/motor/#resetzeroposition) | Set the current position (modified by `offset`) to be the new zero (home) position. |
| [`GetPosition`](/components/motor/#getposition) | Report the position of the motor based on its encoder. |
| [`GetProperties`](/components/motor/#getproperties) | Report a dictionary mapping optional properties to whether it is supported by this motor. |
| [`IsPowered`](/components/motor/#ispowered) | Return whether or not the motor is currently running, and the portion of max power (between `0` and `1`; if the motor is off the power will be `0`). |
| [`GetGeometries`](/components/motor/#getgeometries) | Get all the geometries associated with the motor in its current configuration, in the frame of the motor. |
| [`IsMoving`](/components/motor/#ismoving) | Return whether the motor is actively moving (or attempting to move) under its own power. |
| [`Stop`](/components/motor/#stop) | Cut the power to the motor immediately, without any gradual step down. |
| [`Reconfigure`](/components/motor/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/components/motor/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`FromRobot`](/components/motor/#fromrobot) | Get the resource from the provided robot with the given name. |
| [`Name`](/components/motor/#name) | Get the `ResourceName` for this motor with the given name. |
| [`Close`](/components/motor/#close) | Safely shut down the resource and prevent further use. |
