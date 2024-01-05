---
title: "Movement Sensor Component"
linkTitle: "Movement Sensor"
childTitleEndOverwrite: "Movement Sensor"
weight: 70
type: "docs"
description: "A sensor that measures location, kinematic data, or both."
tags: ["movement sensor", "gps", "imu", "sensor", "components"]
icon: "/icons/components/imu.svg"
images: ["/icons/components/imu.svg"]
no_list: true
modulescript: true
aliases:
  - /components/movement-sensor/
# SME: Rand
---

A movement sensor component is a sensor that gives data on where a machine is and how fast it is moving.
Examples of movement sensors include global positioning systems (GPS), inertial measurement units (IMUs), accelerometers and gyroscopes.

{{% alert title="Tip" color="tip" %}}

Viam also supports generic [sensors](/components/sensor/) and [encoders](/components/encoder/).

{{% /alert %}}

## Related Services

{{< cards >}}
{{< relatedcard link="/mobility/motion/" >}}
{{< relatedcard link="/mobility/navigation/" >}}
{{< /cards >}}

## Supported Models

To use your GPS, IMU, accelerometer, or other movement sensor with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your movement sensor.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

Viam supports several different models of movement sensor.
For configuration information, click on the model name:
Click the model names below for configuration information:

<!-- prettier-ignore -->
Model | Description <a name="model-table"></a>
----- | -----------
[`gps-nmea`](./gps/gps-nmea/) | [NMEA-based](https://en.wikipedia.org/wiki/NMEA_0183) GPS models
[`gps-nmea-rtk-pmtk`](./gps/gps-nmea-rtk-pmtk/) | [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [RTK](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS models using I<sup>2</sup>C (**experimental**)
[`gps-nmea-rtk-serial`](./gps/gps-nmea-rtk-serial/) | [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [RTK](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS models using serial communication (**experimental**)
[`imu-wit`](./imu/imu-wit/) | IMUs manufactured by [WitMotion](https://www.wit-motion.com/)
[`accel-adxl345`](./adxl345/) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer
[`gyro-mpu6050`](./mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense
[`merged`](./merged/) | A model that allows you to aggregate the API methods supported by multiple sensors into a singular sensor client, effectively merging the models of the individual resources
[`wheeled-odometry`](./wheeled-odometry/) | A model that uses [encoders](/components/encoder/) to get an odometry estimate from a wheeled base
[`fake`](./fake/) | Used to test code without hardware

### Modular Resources

{{<modular-resources api="rdk:component:movement_sensor" type="movement_sensor">}}

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Movement Sensor](/build/micro-rdk/movement-sensor/) for supported model information.

## Control your movement sensor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a movement sensor called `"my_movement_sensor"` configured as a component of your machine.
If your movement sensor has a different name, change the `name` in the code.

Be sure to import the movement sensor package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.movement_sensor import MovementSensor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/movementsensor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

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

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot,
    name="my_movement_sensor")

# Get the current position of the movement sensor.
position = await my_movement_sensor.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): Contains the current latitude and longitude as floats.
- [(float64)](https://pkg.go.dev/builtin#float64): The altitude in meters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(
    robot, "my_movement_sensor")

// Get the current position of the movement sensor.
position, err := myMovementSensor.Position(context.Background(), nil)
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

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear velocity of the movement sensor.
lin_vel = await my_movement_sensor.get_linear_velocity()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear velocity in the x, y and z directions in meters per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current linear velocity of the movement sensor.
linVel, err := myMovementSensor.LinearVelocity(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetAngularVelocity

Report the current angular velocity about the x, y and z axes (as a 3D vector) in degrees per second.

Supported by IMU models and by `gyro-mpu6050`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the angular velocity about the x, y and z axes in degrees per second.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_angular_velocity).

```python
my_movement_sensor = MovementSensor.from_robot(
  robot=robot, name="my_movement_sensor")

# Get the current angular velocity of the movement sensor.
ang_vel = await my_movement_sensor.get_angular_velocity()

# Get the y component of angular velocity.
y_ang_vel = ang_vel.y
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the angular velocity about the x, y and z axes in degrees per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current angular velocity of the movement sensor.
angVel, err := myMovementSensor.AngularVelocity(context.Background(), nil)

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

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear acceleration of the movement sensor.
lin_accel = await my_movement_sensor.get_linear_acceleration()

# Get the x component of linear acceleration.
x_lin_accel = lin_accel.x
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear acceleration in the x, y and z directions in meters per second per second (m/s<sup>2</sup>).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current linear acceleration of the movement sensor.
linAccel, err := myMovementSensor.LinearAcceleration(context.Background(), nil)

// Get the x component of linear acceleration
xAngVel := linAccel.X
```

{{% /tab %}}
{{< /tabs >}}

### GetCompassHeading

Report the current [compass heading](<https://en.wikipedia.org/wiki/Heading_(navigation)>) in degrees.

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(float)](https://docs.python.org/3/library/functions.html#float): Compass heading in degrees (between 0 and 360).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_compass_heading).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current compass heading of the movement sensor.
heading = await my_movement_sensor.get_compass_heading()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The compass heading in degrees (between 0 and 360).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current compass heading of the movement sensor.
heading, err := myMovementSensor.CompassHeading(context.Background(), nil)
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

- [(Orientation)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Orientation): Abstract base class for protocol messages, containing `o_x`, `o_y`, `o_z`, and `theta`, which together represent a vector pointing in the direction that the sensor is pointing, and the angle (`theta`) in degrees of the sensor's rotation about that axis.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_orientation).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current orientation vector of the movement sensor.
orientation = await my_movement_sensor.get_orientation()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spatialmath.Orientation)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Orientation): Orientation is an interface used to express the different parameterizations of the orientation of the movement sensor in 3D Euclidean space.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go {class="line-numbers linkable-line-numbers"}
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the current orientation of the movement sensor.
sensorOrientation, err := myMovementSensor.Orientation(context.Background(), nil)

// Get the orientation vector (a unit vector pointing in the same direction as the sensor and theta, an angle representing the sensor's rotation about that axis).
orientation := sensorOrientation.OrientationVectorDegrees()

// Print out the orientation vector.
logger.Info("The x component of the orientation vector: ", orientation.OX)
logger.Info("The y component of the orientation vector: ", orientation.OY)
logger.Info("The z component of the orientation vector: ", orientation.OZ)
logger.Info("The number of degrees that the movement sensor is rotated about the vector: ", orientation.Theta)
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

- [(Properties)](https://python.viam.dev/autoapi/viam/components/movement_sensor/movement_sensor/index.html#viam.components.movement_sensor.movement_sensor.MovementSensor.Properties): The supported properties of the movement sensor.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_properties).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the supported properties of the movement sensor.
properties = await my_movement_sensor.get_properties()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(\*movementsensor.Properties)](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#Properties): The supported properties of the movement sensor.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the supported properties of the movement sensor.
properties, err := myMovementSensor.Properties(context.Background(), nil)
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

- [(Dict[str, float])](https://docs.python.org/3/library/stdtypes.html#str): The accuracy and/or precision of the sensor, if supported.
  Contents depend on sensor model.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_accuracy).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the accuracy of the movement sensor.
accuracy = await my_movement_sensor.get_accuracy()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map\[string\]float32)](https://go.dev/blog/maps): The accuracy and/or precision of the sensor, if supported.
  Contents depend on sensor model.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the accuracy of the movement sensor.
accuracy, err := myMovementSensor.Accuracy(context.Background(), nil)
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

- [(Mapping [str, Any])](https://docs.python.org/3/glossary.html#term-mapping): An object containing the measurements from the sensor.
  Contents depend on sensor model and can be of any type.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_readings).

```python
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the latest readings from the movement sensor.
readings = await my_movement_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): A map containing the measurements from the sensor.
  Contents depend on sensor model and can be of any type.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs for Sensor](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor) (because `Readings` is part of the general sensor API that movement sensor wraps).

```go
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

// Get the latest readings from the movement sensor.
readings, err := myMovementSensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the movement sensor in its current configuration, in the [frame](/mobility/frame-system/) of the movement sensor.
The [motion](/mobility/motion/) and [navigation](/mobility/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the movement sensor, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
  robot=robot,
  name="my_movement_sensor"
  )

geometries = await my_movement_sensor.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

{{% /tab %}}

<!-- Go tab

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the movement sensor, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myBase, err := movementsensor.FromRobot(robot, "my_movement_sensor")

geometries, err := myBase.Geometries(context.Background(), nil)

if len(geometries) > 0 {
    // Get the center of the first geometry
    elem := geometries[0]
    fmt.Println("Pose of the first geometry's center point:", elem.center)
}
```

 -->

{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
If you are implementing your own movement sensor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

reset_dict = {
  "command": "reset",
  "example_param": 30
}

do_response = await my_movement_sensor.do_command(reset_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

resp, err := myMovementSensor.DoCommand(ctx, map[string]interface{}{"command": "reset", "example_param": 30})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(robot, "my_movement_sensor")

await my_movement_sensor.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myMovementSensor, err := movementsensor.FromRobot(robot, "my_movement_sensor")

err := myMovementSensor.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

Try adding a movement sensor to your [mobile robot](/components/base/) and writing some code with our [SDKs](/build/program/apis/) to implement closed-loop movement control for your machine.

Or, try configuring [data capture](/data/) on your movement sensor.

{{< snippet "social.md" >}}
