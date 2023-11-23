<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`SetPower`](/platform/build/configure/components/motor/#setpower) | Set the power to send to the motor as a portion of max power.
[`GoFor`](/platform/build/configure/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified RPM.
[`GoTo`](/platform/build/configure/components/motor/#goto) | Send the motor to a specified position (in terms of revolutions from home) at a specified speed.
[`ResetZeroPosition`](/platform/build/configure/components/motor/#resetzeroposition) | Set the current position to be the new zero (home) position.
[`GetPosition`](/platform/build/configure/components/motor/#getposition) | Report the position of the motor based on its encoder. Not supported on all motors.
[`GetProperties`](/platform/build/configure/components/motor/#getproperties) | Return whether or not the motor supports certain optional features.
[`IsPowered`](/platform/build/configure/components/motor/#ispowered) | Return whether or not the motor is currently on, and the amount of power to it.
[`IsMoving`](/platform/build/configure/components/motor/#ismoving) | Return whether the motor is moving or not.
[`Stop`](/platform/build/configure/components/motor/#stop) | Cut power to the motor off immediately, without any gradual step down.
[`GetGeometries`](/platform/build/configure/components/motor/#getgeometries) | Get all the geometries associated with the motor in its current configuration, in the [frame](/platform/build/configure/services/frame-system/) of the motor.
[`DoCommand`](/platform/build/configure/components/motor/#docommand) | Send or receive model-specific commands.
[`Close`](/platform/build/configure/components/motor/#close) | Safely shut down the resource and prevent further use.
