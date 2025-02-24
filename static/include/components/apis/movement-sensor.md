<!-- prettier-ignore -->
| Method Name | Description | Models That Support This Method | `viam-micro-server` Support |
| ----------- | ----------- | ------------------------------- | ----------------- |
| [`GetPosition`](/dev/reference/apis/components/movement-sensor/#getposition) | Get the current latitude, longitude and altitude. | GPS models, `wheeled-odometry` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetLinearVelocity`](/dev/reference/apis/components/movement-sensor/#getlinearvelocity) | Get the current linear velocity as a 3D vector. | GPS models, `wheeled-odometry` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetAngularVelocity`](/dev/reference/apis/components/movement-sensor/#getangularvelocity) | Get the current angular velocity as a 3D vector. | IMU models, `gyro-mpu6050`, and `wheeled-odometry` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetLinearAcceleration`](/dev/reference/apis/components/movement-sensor/#getlinearacceleration) | Get the current linear acceleration as a 3D vector. | IMU models,  `accel-adxl345`, and `gyro-mpu6050` | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetCompassHeading`](/dev/reference/apis/components/movement-sensor/#getcompassheading) | Get the current compass heading in degrees. | GPS models | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetOrientation`](/dev/reference/apis/components/movement-sensor/#getorientation) | Get the current orientation. | IMU models, `wheeled-odometry` |  |
| [`GetProperties`](/dev/reference/apis/components/movement-sensor/#getproperties) | Get the supported properties of this sensor. | all models | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetAccuracy`](/dev/reference/apis/components/movement-sensor/#getaccuracy) | Get the accuracy of the various sensors. | GPS models |  |
| [`GetReadings`](/dev/reference/apis/components/movement-sensor/#getreadings) | Obtain the measurements/data specific to this sensor. | all models | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`DoCommand`](/dev/reference/apis/components/movement-sensor/#docommand) | Send or receive model-specific commands. | all models | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Close`](/dev/reference/apis/components/movement-sensor/#close) | Safely shut down the resource and prevent further use. | all models |  |
