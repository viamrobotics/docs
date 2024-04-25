If you want to control your motor by specifying the distance and velocity in terms of distance and distance/time, for example 2 rotations at 5 m/s, and you have an encoder, you can make use of the position of your encoder to adjust the distance and velocity.

You can do this in two ways:

The first just uses the encoder feedback to increase or decrease the power being set on the motors in increments of 10%.

The second requires setting the `control_parameters` attribute, which sets up a PID control loop to adjust the distance and velocity of the motor.
Setting the `control_parameters` will automatically set up the required PID loop for an encoded motor.
For more information on PID or to set up a more complex control loop, see the [controls package](/internals/controls-package/)

If you want these values to be auto-tuned, you can set all values to 0: `{ "p": 0, "i": 0, "d": 0 }`, and `viam-server` will auto-tune and log the calculated values.
Tuning takes several seconds and spins the motor.
Copy the values from the logs and add them to the configuration once tuned for the values to take effect.
