<!-- prettier-ignore -->
| Method Name | Description | micro-RDK Support |
| ----------- | ----------- | ----------------- |
| [`SetPower`](/components/motor/#setpower) | Set the portion of max power to send to the motor (between `-1` and `1`). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetRPM`](/components/motor/#setrpm) | Spin the motor indefinitely at the specified speed, in revolutions per minute. If `rpm` is positive, the motor will spin forwards, and if `rpm` is negative, the motor will spin backwards. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GoFor`](/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified revolutions per minute. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GoTo`](/components/motor/#goto) | Turn the motor to a specified position (in terms of revolutions from home/zero) at a specified speed in revolutions per minute (RPM). | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`ResetZeroPosition`](/components/motor/#resetzeroposition) | Set the current position (modified by `offset`) to be the new zero (home) position. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GetPosition`](/components/motor/#getposition) | Report the position of the motor based on its encoder. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetProperties`](/components/motor/#getproperties) | Report a dictionary mapping optional properties to whether it is supported by this motor. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`IsPowered`](/components/motor/#ispowered) | Return whether or not the motor is currently running, and the portion of max power (between `0` and `1`; if the motor is off the power will be `0`). | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GetGeometries`](/components/motor/#getgeometries) | Get all the geometries associated with the motor in its current configuration, in the frame of the motor. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`IsMoving`](/components/motor/#ismoving) | Return whether the motor is actively moving (or attempting to move) under its own power. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Stop`](/components/motor/#stop) | Cut the power to the motor immediately, without any gradual step down. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Reconfigure`](/components/motor/#reconfigure) | Reconfigure this resource. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`DoCommand`](/components/motor/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`FromRobot`](/components/motor/#fromrobot) | Get the resource from the provided robot with the given name. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GetResourceName`](/components/motor/#getresourcename) | Get the `ResourceName` for this motor with the given name. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Close`](/components/motor/#close) | Safely shut down the resource and prevent further use. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
