If you want to control your motor by specifying the distance and velocity in terms of distance and distance/time, for example 2 rotations at 5 m/s and you have an encoder, you can make use of the position of your encoder to adjust the distance and velocity.

You can do this in two ways.

The first just uses the movement sensor feedback to increase or decrease the power being set on the motors in increments of 10%.

The second requires setting the `control_parameters` attribute and uses a PID control loop that measures the current position and change in position and determines the difference or error from the desired distance and velocity to compute a correction for the motor based on three terms:

- A _proportional_ term that is the current error
- An _integral_ term that is the total cumulative error
- A _derivative_ term that is the rate of change of the error

By tuning the coefficients on each of these terms, you can adjust how your motor converges towards the target values, how quickly the system reaches the target values, and how much the system overshoots when approaching the target values.

If you want these values to be auto-tuned, you can set all values to 0: `{ "p": 0, "i": 0, "d": 0 }`, and `viam-server` will auto-tune and log the calculated values.
Tuning takes several seconds and spins the motor.
To avoid tuning every time the robot starts up, copy the values from the logs and add them to the configuration once tuned.
