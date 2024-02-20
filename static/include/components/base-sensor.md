If you want to control your base by specifying the velocity in terms of distance/time, for example 5 m/s and you have a sensor, for example a wheel encoder, that measures the actual value, you can make use of the sensor to adjust the velocity.

One way to adjust velocity based on a sensor's measurements, is using a PID control loop that measures the velocity of movement and determines the difference or error from the desired velocity to compute a correction for the base based on three terms:

- A _proportional_ term that is the current error
- An _integral_ term that is the total cumulative error
- A _derivative_ term that is the rate of change of the error

By tuning the coefficients on each of these terms, you can adjust how your base converges towards the target value, how quickly the system reaches the target value, and how much the system overshoots when approaching the target value.

If you use `[ { "type": "linear_velocity", "p": 0, "i": 0, "d": 0 }, { "type": "angular_velocity", "p": 0, "i": 0, "d": 0 } ]`, `viam-server` auto-tunes the values and logs the tuned values.
Tuning takes several seconds and spins the motors.
To avoid tuning every time the robot starts up, copy the values from the log and add them to the configuration once tuned.
