<!-- prettier-ignore -->
Method Name | Description | Models That Support This Method
----------- | ----------- | -------------------------------
[`GetPosition`](/build/configure/components/movement-sensor/#getposition) | Get the current latitude, longitude and altitude. | GPS models
[`GetLinearVelocity`](/build/configure/components/movement-sensor/#getlinearvelocity) | Get the current linear velocity as a 3D vector. | GPS models
[`GetAngularVelocity`](/build/configure/components/movement-sensor/#getangularvelocity) | Get the current angular velocity as a 3D vector. | IMU models and `gyro-mpu6050`
[`GetLinearAcceleration`](/build/configure/components/movement-sensor/#getlinearacceleration) | Get the current linear acceleration as a 3D vector. | IMU models,  `accel-adxl345`, and `gyro-mpu6050`
[`GetCompassHeading`](/build/configure/components/movement-sensor/#getcompassheading) | Get the current compass heading in degrees. | GPS models
[`GetOrientation`](/build/configure/components/movement-sensor/#getorientation) | Get the current orientation. | IMU models
[`GetProperties`](/build/configure/components/movement-sensor/#getproperties) | Get the supported properties of this sensor. | all models
[`GetAccuracy`](/build/configure/components/movement-sensor/#getaccuracy) | Get the accuracy of the various sensors. | GPS models
[`GetReadings`](/build/configure/components/movement-sensor/#getreadings) | Obtain the measurements/data specific to this sensor. | all models
[`GetGeometries`](/build/configure/components/movement-sensor/#getgeometries) | Get all the geometries associated with the movement sensor in its current configuration, in the [frame](/build/configure/services/frame-system/) of the movement sensor. | all models
[`DoCommand`](/build/configure/components/movement-sensor/#docommand) | Send or receive model-specific commands. | all models
[`Close`](/build/configure/components/movement-sensor/#close) | Safely shut down the resource and prevent further use. | all models
