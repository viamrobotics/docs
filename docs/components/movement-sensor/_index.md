---
title: "Movement Sensor Component"
linkTitle: "Movement Sensor"
weight: 75
type: "docs"
description: "A sensor that measures location, kinematic data, or both."
tags: ["movement sensor", "gps", "imu", "sensor", "components"]
icon: "img/components/imu.png"
# no_list: true
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
Find the more [generic sensor component here](/components/sensor/).
Find more information about encoders, another component type, [here](/components/encoder/).

## Configuration

Viam supports several different models of GPS, IMU and accelerometer.
Click the model names below for configuration information:

Model | Supported hardware <a name="model-table"></a>
---------- | ------------------
[`gps-nmea`](./gps-nmea/) | [NMEA-based](https://en.wikipedia.org/wiki/NMEA_0183) GPS models
[`gps-rtk`](./gps-rtk/) | [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [RTK](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS models
[`imu-wit`](./imu-wit/) | IMUs manufactured by [WitMotion](https://witmotion-sensor.com/)
[`imu-vectornav`](./imu-wit) | IMUs manufactured by [VectorNav](https://www.vectornav.com/products)
[`mpu6050`](./mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense
[`rtk-station`](./rtk-station/) | An **experimental** model that allows you to configure your own correction source. Can be linked to an RTK-ready GPS module.
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
print(f"my-imu get_linear_acceleration return value: {lin_accel}")
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
myIMU, err := motor.FromRobot(robot, "my-imu")
if err!=nil { 
  fmt.Println(err) 
}

// Get the current linear acceleration
linAccel, err := myIMU.LinearAcceleration(context.Background(), map[string]interface{}{})
if err!=nil { 
  fmt.Println(err) 
}
fmt.Println("my-imu LinearAcceleration return value: %s", linAccel)
```

{{% /tab %}}
{{< /tabs >}}

## API

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

- [(GeoPoint)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint) Abstract base class for protocol messages, containing latitude and longitude as floats.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.get_position).

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

- [(float64)](https://pkg.go.dev/builtin#float64): The unit returned is the number of revolutions which is intended to be fed back into calls of GoFor.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := movementsensor.FromRobot(robot, "motor1")

// Get the current position of the movement sensor.
position, _ := mySensor.Position(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}
