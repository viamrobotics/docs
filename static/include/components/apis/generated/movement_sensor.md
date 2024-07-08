### GetLinearVelocity

Report the current linear velocity in the x, y and z directions (as a 3D vector) in meters per second.

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.movement_sensor.Vector3](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3)): The linear velocity in m/sec.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear velocity of the movement sensor.
lin_vel = await my_movement_sensor.get_linear_velocity()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_linear_velocity).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear velocity in the x, y and z directions in meters per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current linear velocity of the movement sensor.
linVel, err := myMovementSensor.LinearVelocity(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var linVel = await myMovementSensor.linearVelocity();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/linearVelocity.html).

{{% /tab %}}
{{< /tabs >}}

### GetAngularVelocity

Report the current angular velocity about the x, y and z axes (as a 3D vector) in degrees per second.

Supported by IMU models and by `gyro-mpu6050`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.movement_sensor.Vector3](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3)): The angular velocity in degrees/sec.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current angular velocity of the movement sensor.
ang_vel = await my_movement_sensor.get_angular_velocity()

# Get the y component of angular velocity.
y_ang_vel = ang_vel.y
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_angular_velocity).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spatialmath.AngularVelocity)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#AngularVelocity): A 3D vector containing three floats representing the angular velocity about the x, y and z axes in degrees per second.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current angular velocity of the movement sensor.
angVel, err := myMovementSensor.AngularVelocity(context.Background(), nil)

// Get the y component of angular velocity.
yAngVel := angVel.Y
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var angVel = await myMovementSensor.angularVelocity();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/angularVelocity.html).

{{% /tab %}}
{{< /tabs >}}

### GetCompassHeading

Report the current [compass heading](https://en.wikipedia.org/wiki/Heading_(navigation)) in degrees.

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The compass heading in degrees.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current compass heading of the movement sensor.
heading = await my_movement_sensor.get_compass_heading()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_compass_heading).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The compass heading in degrees (between 0 and 360).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current compass heading of the movement sensor.
heading, err := myMovementSensor.CompassHeading(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var compassHeading = await myMovementSensor.compassHeading();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/compassHeading.html).

{{% /tab %}}
{{< /tabs >}}

### GetOrientation

Report the current orientation of the sensor.

Supported by IMU models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.movement_sensor.Orientation](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Orientation)): The orientation.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current orientation vector of the movement sensor.
orientation = await my_movement_sensor.get_orientation()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_orientation).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spatialmath.Orientation)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Orientation): Abstract base class for protocol messages, containing `o_x`, `o_y`, `o_z`, and `theta`, which together represent a vector pointing in the direction that the sensor is pointing, and the angle (`theta`) in degrees of the sensor's rotation about that axis.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current orientation of the movement sensor.
sensorOrientation, err := myMovementSensor.Orientation(context.Background(), nil)

// Get the orientation vector.
orientation := sensorOrientation.OrientationVectorDegrees()

// Print out the orientation vector.
logger.Info("The x component of the orientation vector: ", orientation.0X)
logger.Info("The y component of the orientation vector: ", orientation.0Y)
logger.Info("The z component of the orientation vector: ", orientation.0Z)
logger.Info("The number of degrees that the movement sensor is rotated about the vector: ", orientation.Theta)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Orientation](https://flutter.viam.dev/viam_sdk/Orientation-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var orientation = await myMovementSensor.orientation();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/orientation.html).

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Report the current GeoPoint (latitude, longitude) and altitude (in meters).

Supported by GPS models.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[viam.components.movement_sensor.GeoPoint, [float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)]): The current lat/long, along with the altitude in m.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot,
    name="my_movement_sensor")

# Get the current position of the movement sensor.
position = await my_movement_sensor.get_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): Contains the current latitude and longitude as floats.
- [(float64)](https://pkg.go.dev/builtin#float64): The altitude in meters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current position of the movement sensor above sea level in meters.
position, altitude, err := myMovementSensor.Position(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Position](https://flutter.viam.dev/viam_sdk/Position-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var position = await myMovementSensor.position();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/position.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the supported properties of this sensor.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.movement_sensor.movement_sensor.MovementSensor.Properties](https://python.viam.dev/autoapi/viam/components/movement_sensor/movement_sensor/index.html#viam.components.movement_sensor.movement_sensor.MovementSensor.Properties)): The properties.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the supported properties of the movement sensor.
properties = await my_movement_sensor.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*Properties)](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#Properties): The supported properties of the movement sensor.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the supported properties of the movement sensor.
properties, err := myMovementSensor.Properties(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Properties](https://flutter.viam.dev/viam_sdk/Properties.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var props = await myMovementSensor.properties();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/properties.html).

{{% /tab %}}
{{< /tabs >}}

### GetAccuracy

Get the reliability metrics of the movement sensor, including various parameters to assess the sensor's accuracy and precision in different dimensions.

Supported by GPS models and `imu-wit`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([MovementSensor.Accuracy](https://python.viam.dev/autoapi/viam/components/movement_sensor/movement_sensor/index.html#viam.components.movement_sensor.movement_sensor.MovementSensor.Accuracy)): The accuracies of the movement sensor.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the accuracy of the movement sensor.
accuracy = await my_movement_sensor.get_accuracy()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_accuracy).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*Accuracy)](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#Accuracy): The precision and reliability metrics of the movement sensor, which vary depending on model.
  This type contains the following fields:

  - `AccuracyMap` [(map[string]float32)](https://pkg.go.dev/builtin#string): A mapping of specific measurement parameters to their accuracy values.
    The keys are string identifiers for each measurement (for example, "Hdop", "Vdop"), and the values are their corresponding accuracy levels as float32.
  - `Hdop` [(float32)](https://pkg.go.dev/builtin#float32): Horizontal Dilution of Precision (HDOP) value.
    It indicates the level of accuracy of horizontal measurements.
    Lower values indicate improved reliability of positional measurements.
  - `Vdop` [(float32)](https://pkg.go.dev/builtin#float32): Vertical Dilution of Precision (VDOP) value.
    Similar to HDOP, it denotes the accuracy level of vertical measurements.
    Lower values indicate improved reliability of positional measurements.
  - `NmeaFix` [(int32)](https://pkg.go.dev/builtin#int32): An integer value representing the quality of the NMEA fix.
    See [Novatel documentation](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm#GPSQualityIndicators) for the meaning of each fix value.
  - `CompassDegreeError` [(float32)](https://pkg.go.dev/builtin#float32): The estimated error in compass readings, measured in degrees.
    This signifies the deviation or uncertainty in the sensor's compass measurements.
    A lower value implies a more accurate compass direction.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the accuracy of the movement sensor.
accuracy, err := myMovementSensor.Accuracy(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Accuracy](https://flutter.viam.dev/viam_sdk/Accuracy.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var accuracy = await myMovementSensor.accuracy();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/accuracy.html).

{{% /tab %}}
{{< /tabs >}}

### GetLinearAcceleration

Report the current linear acceleration in the x, y and z directions (as a 3D vector) in meters per second per second.

Supported by IMU models, `accel-adxl345`, and `gyro-mpu6050`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.movement_sensor.Vector3](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.Vector3)): The linear acceleration in m/sec^2.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the current linear acceleration of the movement sensor.
lin_accel = await my_movement_sensor.get_linear_acceleration()

# Get the x component of linear acceleration.
x_lin_accel = lin_accel.x
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_linear_acceleration).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): A 3D vector containing three floats representing the linear acceleration in the x, y and z directions in meters per second per second (m/s<sup>2</sup>).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current linear acceleration of the movement sensor.
linVel, err := myMovementSensor.LinearVelocity(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/movementsensor#MovementSensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var linAccel = await myMovementSensor.linearAcceleration();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/linearAcceleration.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the movement sensor in its current configuration, in the [frame](/services/frame-system/) of the movement sensor.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_geometries).

{{% /tab %}}
{{< /tabs >}}

### GetReadings

Get all the measurements/data from the sensor.
Results depend on the sensor model and can be of any type.
If a sensor is not configured to take a certain measurement or fails to read a piece of data, that data will not appear in the readings dictionary.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.SensorReading]): The readings for the MovementSensor. Can be of any type.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_movement_sensor = MovementSensor.from_robot(
    robot=robot, name="my_movement_sensor")

# Get the latest readings from the movement sensor.
readings = await my_movement_sensor.get_readings()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.get_readings).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): A map containing the measurements from the sensor. Contents depend on sensor model and can be of any type.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the readings provided by the sensor.
readings, err := mySensor.Readings(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Sensor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var readings = await myMovementSensor.readings();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/readings.html).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
If you are implementing your own movement sensor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### FromRobot

Get the resource from the provided robot with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `robot` [RobotClient](https://flutter.viam.dev/viam_sdk/RobotClient-class.html) (required)
- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [MovementSensor](https://flutter.viam.dev/viam_sdk/MovementSensor-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/fromRobot.html).

{{% /tab %}}
{{< /tabs >}}

### Name

Get the `ResourceName` for this movement sensor with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/MovementSensor/getResourceName.html).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/movement_sensor/client/index.html#viam.components.movement_sensor.client.MovementSensorClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
