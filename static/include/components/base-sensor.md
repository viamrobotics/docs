If you want to control your base by specifying a desired velocity in terms of distance/time, for example 5 m/s, and you have a sensor, for example a wheel encoder, that measures the actual velocity, you can make use of the sensor to adjust the velocity.

By setting the `control_parameters` attribute, you can use a PID control loop that measures the velocity of movement and determines the difference or error from the desired velocity to compute a correction for the base based on three terms:

- A _proportional_ term that is the current error
- An _integral_ term that is the total cumulative error
- A _derivative_ term that is the rate of change of the error

By tuning the coefficients on each of these terms, you can adjust how your base converges towards the target value, how quickly the system reaches the target value, and how much the system overshoots when approaching the target value.

If you want these values to be auto-tuned, you can set all values to 0: `[ { "type": "linear_velocity", "p": 0, "i": 0, "d": 0 }, { "type": "angular_velocity", "p": 0, "i": 0, "d": 0 } ]`, and `viam-server` will auto-tune and log the calculated values.
Tuning takes several seconds and spins the motors.
Copy the values from the logs and add them to the configuration once tuned for the values to take effect.

{{< alert title="Note" color="note" >}}
If you need to auto-tune multiple controlled components that depend on the same hardware, such as a sensor controlled base and one of the motors on the base, run the auto-tuning process one component at a time.
{{< /alert >}}
