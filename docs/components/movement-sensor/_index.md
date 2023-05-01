---
title: "Movement Sensor Component"
linkTitle: "Movement Sensor"
weight: 70
type: "docs"
description: "A sensor that measures location, kinematic data, or both."
tags: ["movement sensor", "gps", "imu", "sensor", "components"]
icon: "/components/img/components/imu.svg"
images: ["/components/img/components/imu.svg"]
no_list: true
aliases:
    - /components/movement-sensor/
# SME: Rand
---

A movement sensor component is a sensor that gives data on where a robot is and how fast it is moving.
Examples of movement sensors include global positioning systems (GPS), inertial measurement units (IMUs), accelerometers and gyroscopes.

{{% alert title="Note" color="note" %}}

Viam also supports generic [sensors](/components/sensor/) and [encoders](/components/encoder/).

{{% /alert %}}

## Configuration

Viam supports several different models of GPS, IMU and accelerometer.
Click the model names below for configuration information:

Model | Description <a name="model-table"></a>
----- | -----------
[`gps-nmea`](./gps/gps-nmea/) | [NMEA-based](https://en.wikipedia.org/wiki/NMEA_0183) GPS models
[`gps-rtk`](./gps/gps-rtk/) | [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [RTK](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS models (**experimental**)
[`imu-wit`](./imu/imu-wit/) | IMUs manufactured by [WitMotion](https://witmotion-sensor.com/)
[`imu-vectornav`](./imu/imu-wit) | IMUs manufactured by [VectorNav](https://www.vectornav.com/products)
[`accel-adxl345`](./adxl345) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer
[`camera_mono`](./cameramono/) | A model that derives movement data from a [camera](/components/camera/) stream (**experimental**)
[`gyro-mpu6050`](./mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense
[`rtk-station`](./gps/rtk-station/) | A model that allows you to configure your own correction source. Can be linked to an RTK-ready GPS module (**experimental**).
[`fake`](./fake/) | Used to test code without hardware

## Control your movement sensor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code Sample** tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a movement sensor called `"my_movement_sensor"` configured as a component of your robot.
If your movement sensor has a different name, change the `name` in the code.

## API

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

Method Name | Description | Models That Support This Method
----------- | ----------- | -------------------------------
[GetPosition](#getposition) | Get the current latitude, longitude and altitude. | GPS models
[GetLinearVelocity](#getlinearvelocity) | Get the current linear velocity as a 3D vector. | GPS models
[GetAngularVelocity](#getangularvelocity) | Get the current angular velocity as a 3D vector. | IMU models and `gyro-mpu6050`
[GetLinearAcceleration](#getlinearacceleration) | Get the current linear acceleration as a 3D vector. | IMU models,  `accel-adxl345`, and `gyro-mpu6050`
[GetCompassHeading](#getcompassheading) | Get the current compass heading in degrees. | GPS models and `imu-vectornav`
[GetOrientation](#getorientation) | Get the current orientation. | IMU models
[GetProperties](#getproperties) | Get the supported properties of this sensor. | all models
[GetAccuracy](#getaccuracy) | Get the accuracy of the various sensors. | GPS models
[GetReadings](#getreadings) | Obtain the measurements/data specific to this sensor. | all models
[DoCommand](#docommand) | Send or receive model-specific commands. | all models

In addition to the information below, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor) or [Python SDK docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#).

### GetPosition

Report the current GeoPoint (latitude, longitude) and altitude (in meters).

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(GeoPoint)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint): Abstract base class for protocol messages, containing latitude and longitude as floats.
- [(float)](https://docs.python.org/3/library/functions.html#float): Altitude in meters.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_position).

**Example usage:**

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the current position of the movement sensor.
position = await my_movement_sensor.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): Contains the current latitude and longitude as floats.
- [(float64)](https://pkg.go.dev/builtin#float64): The altitude in meters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current position of the movement sensor.
position, _ := myMovementSensor.Position(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetLinearVelocity

Report the current linear velocity in the x, y and z directions (as a 3D vector) in meters per second.

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the linear velocity in the x, y and z directions in meters per second.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_linear_velocity).

**Example usage:**

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the current linear velocity of the movement sensor.
lin_vel = await my_movement_sensor.get_linear_velocity()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear velocity in the x, y and z directions in meters per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current linear velocity of the movement sensor.
linVel, _ := myMovementSensor.LinearVelocity(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetAngularVelocity

Report the current angular velocity about the x, y and z axes (as a 3D vector) in radians per second.

Supported by IMU models and by `gyro-mpu6050`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the angular velocity about the x, y and z axes in radians per second.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_angular_velocity).

**Example usage:**

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the current angular velocity of the movement sensor.
ang_vel = await my_movement_sensor.get_angular_velocity()

# Get the y component of angular velocity.
y_ang_vel = ang_vel.y
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the angular velocity about the x, y and z axes in radians per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current angular velocity of the movement sensor.
angVel, _ := myMovementSensor.AngularVelocity(context.Background(), nil)

// Get the y component of angular velocity.
yAngVel := angVel.Y
```

{{% /tab %}}
{{< /tabs >}}

### GetLinearAcceleration

Report the current linear acceleration in the x, y and z directions (as a 3D vector) in meters per second per second.

Supported by IMU models, `accel-adxl345`, and `gyro-mpu6050`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the linear acceleration in the x, y and z directions in meters per second per second (m/s<sup>2</sup>).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_linear_acceleration).

**Example usage:**

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the current linear acceleration of the movement sensor.
lin_accel = await my_movement_sensor.get_linear_acceleration()

# Get the x component of linear acceleration.
x_lin_accel = lin_accel.x
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear acceleration in the x, y and z directions in meters per second per second (m/s<sup>2</sup>).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current linear acceleration of the movement sensor.
linAccel, _ := myMovementSensor.LinearAcceleration(context.Background(), nil)

// Get the x component of linear acceleration
xAngVel := linAccel.X
```

{{% /tab %}}
{{< /tabs >}}

### GetCompassHeading

Report the current [compass heading](https://en.wikipedia.org/wiki/Heading_(navigation)) in degrees.

Supported by GPS models and `imu-vectornav`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(float)](https://docs.python.org/3/library/functions.html#float): Compass heading in degrees (between 0 and 360).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_compass_heading).

**Example usage:**

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the current compass heading of the movement sensor.
heading = await my_movement_sensor.get_compass_heading()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The compass heading in degrees (between 0 and 360).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current compass heading of the movement sensor.
heading, _ := myMovementSensor.CompassHeading(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetOrientation

Report the current orientation of the sensor.

Supported by IMU models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Orientation)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Orientation): Abstract base class for protocol messages, containing `o_x`, `o_y`, `o_z`, and `theta`, which together represent a vector pointing in the direction that the sensor is pointing, and the angle (`theta`) of the sensor's rotation about that axis.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_orientation).

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the current orientation vector of the movement sensor.
orientation = await my_movement_sensor.get_orientation()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spatialmath.Orientation)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Orientation): Orientation is an interface used to express the different parameterizations of the orientation of the movement sensor in 3D Euclidean space.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go {class="line-numbers linkable-line-numbers"}
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current orientation of the movement sensor.
sensorOrientation, _ := myMovementSensor.Orientation(context.Background(), nil)

// Get the orientation vector (a unit vector pointing in the same direction as the sensor and theta, an angle representing the sensor's rotation about that axis).
orientation := sensorOrientation.OrientationVectorDegrees()

// Print out the orientation vector.
logger.Info("The x component of the orientation vector: ", orientation.OX)
logger.Info("The y component of the orientation vector: ", orientation.OY)
logger.Info("The z component of the orientation vector: ", orientation.OZ)
logger.Info("The number of degrees that the movement sensor is rotated about the vector: ", orientation.OX)
```

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the supported properties of this sensor.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- ([Properties](https://python.viam.dev/autoapi/viam/components/movement_sensor/movement_sensor/index.html#viam.components.movement_sensor.movement_sensor.MovementSensor.Properties)): The supported properties of the movement sensor.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_properties).

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the supported properties of the movement sensor.
properties = await my_movement_sensor.get_properties()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*movementsensor.Properties)](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#Properties): The supported properties of the movement sensor.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the supported properties of the movement sensor.
properties, _ := myMovementSensor.Properties(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetAccuracy

Get the accuracy of the sensor (and/or precision, depending on the sensor model).

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- (Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [float](https://docs.python.org/3/library/functions.html#float)]): The accuracy and/or precision of the sensor, if supported.
  Contents depend on sensor model.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_accuracy).

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the accuracy of the movement sensor.
accuracy = await my_movement_sensor.get_accuracy()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- (map[[string]](https://pkg.go.dev/builtin#string)[float32](https://pkg.go.dev/builtin#float32)): The accuracy and/or precision of the sensor, if supported.
  Contents depend on sensor model.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the accuracy of the movement sensor.
accuracy, _ := myMovementSensor.Accuracy(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetReadings

Get all the measurements/data from the sensor.
Results depend on the sensor model and can be of any type.
If a sensor is not configured to take a certain measurement or fails to read a piece of data, that data will not appear in the readings dictionary.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- ([Mapping [str, Any]](https://docs.python.org/3/glossary.html#term-mapping)): An object containing the measurements from the sensor.
Contents depend on sensor model and can be of any type.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_readings).

```python
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

# Get the latest readings from the movement sensor.
readings = await my_movement_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- (map[[string]](https://pkg.go.dev/builtin#string)interface{}): A map containing the measurements from the sensor.
    Contents depend on sensor model and can be of any type.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs for Sensor](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor) (because `Readings` is part of the general sensor API that movement sensor wraps).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the latest readings from the movement sensor.
readings, _ := myMovementSensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
If you are implementing your own movement sensor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(robot=robot, name="my_movement_sensor")

reset_dict = {
  "command": "reset",
  "example_param": 30
}

do_response = await my_movement_sensor.do_command(reset_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/#the-do-method).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` (`cmd map[string]interface{}`): The command to execute.

**Returns:**

- `result` (`cmd map[string]interface{}`): Result of the executed command.
- `error` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

resp, err := myMovementSensor.DoCommand(ctx, map[string]interface{}{"command": "reset", "example_param": 30})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## Next Steps

Try adding a movement sensor to your [mobile robot](../base/) and writing some code with our [SDKs](../../program/sdks/) to implement closed-loop movement control for your robot.

Or, try configuring [data capture](../../services/data/) on your movement sensor.

{{< snippet "social.md" >}}
