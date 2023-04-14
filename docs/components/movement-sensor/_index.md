---
title: "Movement Sensor Component"
linkTitle: "Movement Sensor"
weight: 70
type: "docs"
description: "A sensor that measures location, kinematic data, or both."
tags: ["movement sensor", "gps", "imu", "sensor", "components"]
icon: "img/components/imu.png"
no_list: true
aliases:
    - /components/movement-sensor/
# SME: Rand
---

The movement sensor component is an abstraction of a sensor that gives data on where a robot is and how fast it is moving.

We have chosen to abstract these types of sensors into one common API.
There are many different types of sensors that can provide data for some or all of the following methods: `Position`, `Orientation`, `LinearVelocity`, `AngularVelocity`, `LinearAcceleration` and `CompassHeadings`.
A global positioning system (GPS) can provide position, linear velocity and compass headings.
An inertial measurement unit (IMU) can provide angular velocity and orientation.
We can further apply algorithms, such as a [Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter), to combine data from both a GPS and an IMU to output the full set of information of the movement sensor methods.

We specifically cover GPS, accelerometer and IMU units in this documentation.
Find the more generic [sensor component here](/components/sensor/).
Find more information about encoders, another component type, [here](/components/encoder/).

## Configuration

Viam supports several different models of GPS, IMU and accelerometer.
Click the model names below for configuration information:

Model | Supported hardware <a name="model-table"></a>
---------- | ------------------
[`gps-nmea`](./gps/gps-nmea/) | [NMEA-based](https://en.wikipedia.org/wiki/NMEA_0183) GPS models
[`gps-rtk`](./gps/gps-rtk/) | [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [RTK](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS models
[`imu-wit`](./imu/imu-wit/) | IMUs manufactured by [WitMotion](https://witmotion-sensor.com/)
[`imu-vectornav`](./imu/imu-wit) | IMUs manufactured by [VectorNav](https://www.vectornav.com/products)
[`accel-adxl345`](./adxl345) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer
[`mpu6050`](./mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense
[`rtk-station`](./gps/rtk-station/) | An **experimental** model that allows you to configure your own correction source. Can be linked to an RTK-ready GPS module.
[`fake`](./fake/) | Used to test code without hardware

## Control your movement sensor with Viam's client SDK libraries

The following example assumes you have a movement sensor called `my-imu` configured as a component of your robot.
If your movement sensor has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

Place the example code after the `robot = await connect()` function in `main()`.

```python
from viam.components.movement_sensor import MovementSensor

robot = await connect() # Refer to CODE SAMPLE tab code
my_imu = MovementSensor.from_robot(robot, "my-imu")

# Get the current linear acceleration
lin_accel = await my_imu.get_linear_acceleration()
print(f"my-imu linear acceleration in the x direction: {lin_accel.x}")
```

{{% /tab %}}
{{% tab name="Go" %}}

Example code should be placed after the `robot, err := client.New(...)` function in `main()`.

```go
import (
  "context"
  "time"

  "github.com/edaniels/golog"

  "go.viam.com/rdk/components/movementsensor"
)

robot, err := client.New() // Refer to CODE SAMPLE tab code
// Grab the movement sensor from the robot
myIMU, err := movementsensor.FromRobot(robot, "my-imu")
if err!=nil { 
  fmt.Println(err) 
}

// Get the current linear acceleration
linAccel, err := myIMU.LinearAcceleration(context.Background(), map[string]interface{}{})
if err!=nil { 
  fmt.Println(err) 
}
fmt.Println("my-imu LinearAcceleration in the x direction: ", linAccel.X)
```

{{% /tab %}}
{{< /tabs >}}

## API

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

Method Name | Description
----------- | -----------
[GetPosition](#getposition) | Gets the current latitude, longitude and altitude.
[GetLinearVelocity](#getlinearvelocity) | Gets the current linear velocity as a 3D vector.
[GetAngularVelocity](#getangularvelocity) | Gets the current angular velocity as a 3D vector.
[GetLinearAcceleration](#getlinearacceleration) | Gets the current linear acceleration as a 3D vector.
[GetCompassHeading](#getcompassheading) | Gets the current compass heading in degrees.
[GetOrientation](#getorientation) | Get the current orientation.
[GetProperties](#getproperties) | Get the supported properties of this sensor.
[GetAccuracy](#getaccuracy) | Get the accuracy of the various sensors.
[GetReadings](#getreadings) | Obtain the measurements/data specific to this sensor.
[DoCommand](#docommand) | Sends or receives model-specific commands.

In addition to the information below, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor)
or [Python SDK docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#).

### GetPosition

Report the current GeoPoint (latitude, longitude) and altitude (in millimeters).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(GeoPoint)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint): Abstract base class for protocol messages, containing latitude and longitude as floats.
- [(float)](https://docs.python.org/3/library/functions.html#float): Altitude in millimeters.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_position).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the current position of the movement sensor.
position = await my_sensor.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): Contains the current latitude and longitude as floats.
- [(float64)](https://pkg.go.dev/builtin#float64): The altitude in millimeters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the current position of the movement sensor.
position, _ := mySensor.Position(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetLinearVelocity

Report the current linear velocity in the x, y and z directions (as a 3D vector) in millimeters per second.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the linear velocity in the x, y and z directions in millimeters per second.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_linear_velocity).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the current linear velocity of the movement sensor.
lin_vel = await my_sensor.get_linear_velocity()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear velocity in the x, y and z directions in millimeters per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the current linear velocity of the movement sensor.
linVel, _ := mySensor.LinearVelocity(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetAngularVelocity

Report the current angular velocity about the x, y and z axes (as a 3D vector) in radians per second.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the angular velocity about the x, y and z axes in radians per second.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_angular_velocity).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the current angular velocity of the movement sensor.
ang_vel = await my_sensor.get_angular_velocity()
# Get the y component of angular velocity
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
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the current angular velocity of the movement sensor.
angVel, _ := mySensor.AngularVelocity(context.TODO(), nil)
// Get the y component of angular velocity
yAngVel := angVel.Y
```

{{% /tab %}}
{{< /tabs >}}

### GetLinearAcceleration

Report the current linear acceleration in the x, y and z directions (as a 3D vector) in millimeters per second per second.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Vector3)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3): A 3D vector containing three floats representing the linear acceleration in the x, y and z directions in millimeters per second per second (mm/s<sup>2</sup>).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_linear_acceleration).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the current linear acceleration of the movement sensor.
lin_accel = await my_sensor.get_linear_acceleration()
# Get the x component of linear acceleration
x_lin_accel = lin_accel.x
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear acceleration in the x, y and z directions in millimeters per second per second (mm/s<sup>2</sup>).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the current linear acceleration of the movement sensor.
linAccel, _ := mySensor.LinearAcceleration(context.TODO(), nil)
// Get the x component of linear acceleration
xAngVel := linAccel.X
```

{{% /tab %}}
{{< /tabs >}}

### GetCompassHeading

Report the current [compass heading](https://en.wikipedia.org/wiki/Heading_(navigation)) in degrees.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(float)](https://docs.python.org/3/library/functions.html#float): Compass heading in degrees (between 0 and 360).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_compass_heading).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the current compass heading of the movement sensor.
heading = await my_sensor.get_compass_heading()
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
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the current compass heading of the movement sensor.
heading, _ := mySensor.CompassHeading(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetOrientation

Report the current orientation of the sensor.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Orientation)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Orientation): Abstract base class for protocol messages, containing `o_x`, `o_y`, `o_z`, and `theta`, which together represent a vector pointing in the direction that the sensor is pointing, and the angle (`theta`) of the sensor's rotation about that axis.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_orientation).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the current orientation vector of the movement sensor.
orientation = await my_sensor.get_orientation()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spacialmath.Orientation)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Orientation): Orientation is an interface used to express the different parameterizations of the orientation of the movement sensor in 3D Euclidean space.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

**Example usage:**

```go {class="line-numbers linkable-line-numbers"}
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the current orientation of the movement sensor.
sensorOrientation, _ := mySensor.Orientation(context.TODO(), nil)
// Get the orientation vector (a unit vector pointing in the same direction as the sensor,
// plus an angle representing the sensor's rotation about that axis)
vector := sensorOrientation.OrientationVectorDegrees()
fmt.Println("The x component of the orientation vector: ", vector.OX)
fmt.Println("The y component of the orientation vector: ", vector.OY)
fmt.Println("The z component of the orientation vector: ", vector.OZ)
fmt.Println("The number of degrees that the movement sensor is rotated about the vector: ", vector.OX)
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

- ([Properties](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.Properties))<!--this link isn't very useful -->: The supported properties of the movement sensor.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_properties).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the supported properties of the movement sensor.
properties = await my_sensor.get_properties()
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

**Example usage:**

```go
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the supported properties of the movement sensor.
properties, _ := mySensor.Properties(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetAccuracy

Get the accuracy of the sensor (and/or precision, depending on the sensor model).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- (Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [float](https://docs.python.org/3/library/functions.html#float)]): The accuracy and/or precision of the sensor, if supported.
  Contents depend on sensor model.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_accuracy).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the accuracy of the movement sensor.
accuracy = await my_sensor.get_accuracy()
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

**Example usage:**

```go
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the accuracy of the movement sensor.
accuracy, _ := mySensor.Accuracy(context.TODO(), nil)
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

- ([Mapping](https://docs.python.org/3/glossary.html#term-mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]): An object containing the measurements from the sensor.
  Contents depend on sensor model and can be of any type.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.MovementSensor.get_readings).

**Example usage:**

```python
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

# Get the latest readings from the movement sensor.
readings = await my_sensor.get_readings()
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

**Example usage:**

```go
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

// Get the latest readings from the movement sensor.
readings, _ := mySensor.Readings(context.TODO(), nil)
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
my_sensor = MovementSensor.from_robot(robot=robot, name='my_movement_sensor')

reset_dict = {
  "command": "reset",
  "example_param": 30
}
do_response = await my_sensor.do_command(reset_dict)
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
mySensor, err := movementsensor.FromRobot(robot, "sensor1")

resp, err := mySensor.DoCommand(ctx, map[string]interface{}{"command": "reset", "example_param": 30})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/components/movementsensor/movementsensor.go#L212).

{{% /tab %}}
{{< /tabs >}}

## Next Steps

Try adding a movement sensor to your [mobile robot](../base/) and writing some code with our [SDKs](../../program/sdk-as-client/) to implement closed-loop movement control for your robot!

Or, try configuring [data capture](../../services/data/) on your movement sensor!

{{< snippet "social.md" >}}
