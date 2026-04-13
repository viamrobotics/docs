---
linkTitle: "Control components"
title: "Control components"
weight: 55
layout: "docs"
type: "docs"
description: "Read from sensors and control motors, arms, and other actuators from your app using the SDK component clients."
date: "2026-04-13"
---

Read sensor data and send commands to motors, arms, grippers, and other actuators from your app. Each component type has its own SDK client with methods specific to that type. This page shows the pattern for getting a component client and calling its methods.

For the full list of component types and their methods, see the SDK reference for your language: [TypeScript](https://ts.viam.dev/), [Python](https://python.viam.dev/), [Flutter](https://flutter.viam.dev/), [Go](https://pkg.go.dev/go.viam.com/rdk), or [C++](https://cpp.viam.dev/).

## Prerequisites

- A project with an active machine connection (see [Connect to a machine](./connect-to-machine/))
- At least one component configured on the machine (sensor, motor, camera, arm, or any other type). If you do not have physical hardware, add a fake component in the Viam app's **CONFIGURE** tab (`fake:sensor`, `fake:motor`, and so on).

## Get a component client

Every component type follows the same pattern: you get a typed client from the connected machine by name, then call methods on that client.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
import * as VIAM from "@viamrobotics/sdk";

const sensor = new VIAM.SensorClient(machine, "my_sensor");
const motor = new VIAM.MotorClient(machine, "my_motor");
```

In TypeScript, you construct a client by passing the `RobotClient` and the component name.

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
import 'package:viam_sdk/viam_sdk.dart';

final sensor = Sensor.fromRobot(robot, 'my_sensor');
final motor = Motor.fromRobot(robot, 'my_motor');
```

In Flutter, each component type has a `fromRobot` factory method.

{{% /tab %}}
{{% tab name="Python" %}}

```python
from viam.components.sensor import Sensor
from viam.components.motor import Motor

sensor = Sensor.from_robot(robot=machine, name="my_sensor")
motor = Motor.from_robot(robot=machine, name="my_motor")
```

In Python, each component type has a `from_robot` class method.

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/components/motor"
)

mySensor, err := sensor.FromProvider(machine, "my_sensor")
if err != nil {
    logger.Fatal(err)
}

myMotor, err := motor.FromProvider(machine, "my_motor")
if err != nil {
    logger.Fatal(err)
}
```

In Go, each component package has a `FromProvider` function that returns the typed interface.

{{% /tab %}}
{{< /tabs >}}

The string `"my_sensor"` or `"my_motor"` is the name you gave the component in your machine configuration. If you named it something different, change the string to match.

## Read from a sensor

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
const readings = await sensor.getReadings();
console.log(readings);
// Example output: { temperature: 22.5, humidity: 45.2 }
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
final readings = await sensor.readings();
print(readings);
// Example output: {temperature: 22.5, humidity: 45.2}
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
readings = await sensor.get_readings()
print(readings)
# Example output: {'temperature': 22.5, 'humidity': 45.2}
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
readings, err := mySensor.Readings(context.Background(), nil)
if err != nil {
    logger.Fatal(err)
}
fmt.Println(readings)
// Example output: map[temperature:22.5 humidity:45.2]
```

{{% /tab %}}
{{< /tabs >}}

The readings map contains whatever key-value pairs the sensor returns. The keys and types depend on the sensor model. For `fake:sensor`, the readings are generated test values.

## Control a motor

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
// Set power (range: -1 to 1)
await motor.setPower(0.5);

// Stop
await motor.stop();

// Check if moving
const moving = await motor.isMoving();
console.log(`Motor is moving: ${moving}`);
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
// Set power (range: -1 to 1)
await motor.setPower(0.5);

// Stop
await motor.stop();

// Check if moving
final moving = await motor.isMoving();
print('Motor is moving: $moving');
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
# Set power (range: -1 to 1)
await motor.set_power(power=0.5)

# Stop
await motor.stop()

# Check if moving
moving = await motor.is_moving()
print(f"Motor is moving: {moving}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Set power (range: -1 to 1)
err = myMotor.SetPower(context.Background(), 0.5, nil)
if err != nil {
    logger.Fatal(err)
}

// Stop
err = myMotor.Stop(context.Background(), nil)
if err != nil {
    logger.Fatal(err)
}

// Check if moving
moving, err := myMotor.IsMoving(context.Background())
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Motor is moving: %v\n", moving)
```

{{% /tab %}}
{{< /tabs >}}

`setPower` takes a value from -1 (full reverse) to 1 (full forward). 0 is stopped. For `fake:motor`, the state changes are tracked internally but nothing physical moves. You can verify the state change by opening the Viam app's **CONTROL** tab for the same machine.

## Other component types

The pattern is the same for every component type. Get a typed client by name, then call that type's methods:

| Component | Get client (Python)                           | Common methods                                                                                   |
| --------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Arm       | `Arm.from_robot(robot=machine, name="x")`     | `get_end_position`, `move_to_position`, `get_joint_positions`, `move_to_joint_positions`, `stop` |
| Base      | `Base.from_robot(robot=machine, name="x")`    | `move_straight`, `spin`, `set_power`, `set_velocity`, `stop`                                     |
| Camera    | `Camera.from_robot(robot=machine, name="x")`  | `get_images`, `get_point_cloud`, `get_properties`                                                |
| Gripper   | `Gripper.from_robot(robot=machine, name="x")` | `open`, `grab`, `stop`, `is_moving`                                                              |
| Servo     | `Servo.from_robot(robot=machine, name="x")`   | `move`, `get_position`, `stop`                                                                   |

The method names follow the same naming convention in each language: Python uses `snake_case`, Go uses `CamelCase`, TypeScript uses `camelCase`, Flutter uses `camelCase`. See your SDK's reference for the exact signatures.

## Next

- [Stream video](./stream-video/) for displaying camera feeds (TypeScript and Flutter WebRTC streaming, or `get_images` polling for Python and Go)
- [Handle disconnection and reconnection](./handle-connection-state/) for reconnection behavior when controlling actuators
- [Connect to a machine](./connect-to-machine/) if you have not set up a connection yet
