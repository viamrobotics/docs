<!-- prettier-ignore -->
| Method Name | Description | `viam-micro-server` Support |
| ----------- | ----------- | --------------------------- |
| [`SetPower`](/dev/reference/apis/components/motor/#setpower) | Set the portion of max power to send to the motor (between `-1` and `1`). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetRPM`](/dev/reference/apis/components/motor/#setrpm) | Spin the motor indefinitely at the specified speed, in revolutions per minute. If `rpm` is positive, the motor will spin forwards, and if `rpm` is negative, the motor will spin backwards. |  |
| [`GoFor`](/dev/reference/apis/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified revolutions per minute. |  |
| [`GoTo`](/dev/reference/apis/components/motor/#goto) | Turn the motor to a specified position (in terms of revolutions from home/zero) at a specified speed in revolutions per minute (RPM). |  |
| [`ResetZeroPosition`](/dev/reference/apis/components/motor/#resetzeroposition) | Set the current position (modified by `offset`) to be the new zero (home) position. |  |
| [`GetPosition`](/dev/reference/apis/components/motor/#getposition) | Report the position of the motor based on its encoder. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetProperties`](/dev/reference/apis/components/motor/#getproperties) | Report a dictionary mapping optional properties to whether it is supported by this motor. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`IsPowered`](/dev/reference/apis/components/motor/#ispowered) | Return whether or not the motor is currently running, and the portion of max power (between `0` and `1`; if the motor is off the power will be `0`). |  |
| [`IsMoving`](/dev/reference/apis/components/motor/#ismoving) | Return whether the motor is actively moving (or attempting to move) under its own power. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Stop`](/dev/reference/apis/components/motor/#stop) | Cut the power to the motor immediately, without any gradual step down. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Reconfigure`](/dev/reference/apis/components/motor/#reconfigure) | Reconfigure this resource. |  |
| [`DoCommand`](/dev/reference/apis/components/motor/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`GetResourceName`](/dev/reference/apis/components/motor/#getresourcename) | Get the `ResourceName` for this motor. |  |
| [`Close`](/dev/reference/apis/components/motor/#close) | Safely shut down the resource and prevent further use. |  |
