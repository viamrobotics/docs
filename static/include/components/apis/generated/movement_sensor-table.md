<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetLinearVelocity`](/components/movement-sensor/#getlinearvelocity) | Report the current linear velocity in the x, y and z directions (as a 3D vector) in meters per second. |
| [`GetAngularVelocity`](/components/movement-sensor/#getangularvelocity) | Report the current angular velocity about the x, y and z axes (as a 3D vector) in degrees per second. |
| [`GetCompassHeading`](/components/movement-sensor/#getcompassheading) | Report the current [compass heading](https://en.wikipedia.org/wiki/Heading_(navigation)) in degrees. |
| [`GetOrientation`](/components/movement-sensor/#getorientation) | Report the current orientation of the sensor. |
| [`GetPosition`](/components/movement-sensor/#getposition) | Report the current GeoPoint (latitude, longitude) and altitude (in meters). |
| [`GetProperties`](/components/movement-sensor/#getproperties) | Get the supported properties of this sensor. |
| [`GetAccuracy`](/components/movement-sensor/#getaccuracy) | Get the reliability metrics of the movement sensor, including various parameters to assess the sensor's accuracy and precision in different dimensions. |
| [`GetLinearAcceleration`](/components/movement-sensor/#getlinearacceleration) | Report the current linear acceleration in the x, y and z directions (as a 3D vector) in meters per second per second. |
| [`GetGeometries`](/components/movement-sensor/#getgeometries) | Get all the geometries associated with the movement sensor in its current configuration, in the frame of the movement sensor. |
| [`GetReadings`](/components/movement-sensor/#getreadings) | Get all the measurements/data from the sensor. |
| [`Reconfigure`](/components/movement-sensor/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/components/movement-sensor/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`Close`](/components/movement-sensor/#close) | Safely shut down the resource and prevent further use. |
