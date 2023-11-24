<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`SetPower`](/build/configure/components/motor/#setpower) | Set the power to send to the motor as a portion of max power.
[`GoFor`](/build/configure/components/motor/#gofor) | Spin the motor the specified number of revolutions at specified RPM.
[`GoTo`](/build/configure/components/motor/#goto) | Send the motor to a specified position (in terms of revolutions from home) at a specified speed.
[`ResetZeroPosition`](/build/configure/components/motor/#resetzeroposition) | Set the current position to be the new zero (home) position.
[`GetPosition`](/build/configure/components/motor/#getposition) | Report the position of the motor based on its encoder. Not supported on all motors.
[`GetProperties`](/build/configure/components/motor/#getproperties) | Return whether or not the motor supports certain optional features.
[`IsPowered`](/build/configure/components/motor/#ispowered) | Return whether or not the motor is currently on, and the amount of power to it.
[`IsMoving`](/build/configure/components/motor/#ismoving) | Return whether the motor is moving or not.
[`Stop`](/build/configure/components/motor/#stop) | Cut power to the motor off immediately, without any gradual step down.
[`GetGeometries`](/build/configure/components/motor/#getgeometries) | Get all the geometries associated with the motor in its current configuration, in the [frame](/build/configure/services/frame-system/) of the motor.
[`DoCommand`](/build/configure/components/motor/#docommand) | Send or receive model-specific commands.
[`Close`](/build/configure/components/motor/#close) | Safely shut down the resource and prevent further use.
