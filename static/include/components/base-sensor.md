If you want to control your base by specifying a desired velocity in terms of distance/time, for example 5 m/s, and you have a movement sensor that measures the actual velocity, you can make use of the sensor to adjust the velocity. Alternatively, if your base has position reporting motors, you can utilize the [wheeled odometry](../../../docs/components/movement-sensor/wheeled-odometry) movement sensor to get an estimate of the necessary velocities.

Setting the `control_parameters` attribute sets up a PID control loop. Setting the `control_parameters` will automatically set up the required PID loop for a sensor controlled base. For more information on PID or to set up a more complex control loop, see the [controls package](../../../docs/internals/controls-package)

If you want these values to be auto-tuned, you can set all values to 0: `[ { "type": "linear_velocity", "p": 0, "i": 0, "d": 0 }, { "type": "angular_velocity", "p": 0, "i": 0, "d": 0 } ]`, and `viam-server` will auto-tune and log the calculated values.
Tuning takes several seconds and spins the motors.
Copy the values from the logs and add them to the configuration once tuned for the values to take effect.

{{< alert title="Note" color="note" >}}
If you need to auto-tune multiple controlled components that depend on the same hardware, such as a sensor controlled base and one of the motors on the base, run the auto-tuning process one component at a time.
{{< /alert >}}
