---
linkTitle: "Movement sensor"
title: "Add a movement sensor"
weight: 60
layout: "docs"
type: "docs"
description: "Add and configure a movement sensor like a GPS, IMU, or odometry source."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-movement-sensor/
---

You need your machine to know where it is, how fast it's moving, or which
direction it's facing. A movement sensor component provides position,
velocity, orientation, and compass heading data.

## Concepts

Unlike a generic sensor (which returns arbitrary readings), a movement sensor
has a structured API with specific methods for spatial data:

- `GetPosition`: latitude, longitude, altitude.
- `GetLinearVelocity`: speed in X, Y, Z.
- `GetAngularVelocity`: rotation rate around each axis.
- `GetCompassHeading`: heading in degrees.
- `GetOrientation`: orientation as Euler angles or quaternion.

Not every movement sensor supports every method. A GPS provides position and
compass heading but not angular velocity. An IMU provides orientation and
angular velocity but not GPS position. Use `GetProperties` to check which
methods a particular sensor supports.

### Built-in models

| Model              | Use case                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| `wheeled-odometry` | Estimates position and velocity from motor encoders on a wheeled base. No additional hardware needed. |
| `merged`           | Combines data from multiple movement sensors into one. For example, GPS position + IMU orientation.   |

Hardware-specific models (GPS modules, IMUs, RTK receivers) are available as
**modules in the registry**.

## Steps

### Option A: Wheeled odometry (no extra hardware)

If you have a wheeled base with encoders on the motors, you can get position
and velocity estimates without any additional sensors.

#### 1. Prerequisites

- A [wheeled base](/hardware/common-components/add-a-base/) with motors that have
  [encoders](/hardware/common-components/add-an-encoder/) configured.

#### 2. Add the movement sensor

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for **wheeled-odometry**. This is the built-in model that
   computes position from wheel encoder data.
4. Name it (e.g., `odometry`) and click **Create**.

#### 3. Configure attributes

```json
{
  "base": "my-base",
  "left_motors": ["left-motor"],
  "right_motors": ["right-motor"]
}
```

| Attribute            | Type            | Required | Description                               |
| -------------------- | --------------- | -------- | ----------------------------------------- |
| `base`               | string          | Yes      | Name of the wheeled base component.       |
| `left_motors`        | list of strings | Yes      | Left motor names (must have encoders).    |
| `right_motors`       | list of strings | Yes      | Right motor names (must have encoders).   |
| `time_interval_msec` | float           | No       | How often to recalculate. Default: `500`. |

### Option B: Hardware sensor (GPS, IMU)

#### 1. Add the component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your sensor hardware. Search by
   sensor name or chip (e.g., **NMEA GPS**, **BNO055**, **MPU6050**).
4. Name it and click **Create**.
5. Configure attributes per the model's documentation (typically I2C
   address or serial port).

### Option C: Merged sensor

Combine data from multiple movement sensors into one.

```json
{
  "position": "gps-sensor",
  "orientation": "imu-sensor",
  "compass_heading": "gps-sensor",
  "angular_velocity": "imu-sensor",
  "linear_velocity": "odometry"
}
```

Each field names the movement sensor to use for that type of data. This lets
you build a complete spatial picture from multiple hardware sources.

### Save and test

Click **Save**, then expand the **TEST** section.

- The test panel shows all available data: position, velocity, orientation,
  and heading.
- Methods the sensor doesn't support will show as unavailable.

## Try it

Read position and velocity data from the movement sensor.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `movement_sensor_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.movement_sensor import MovementSensor


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    sensor = MovementSensor.from_robot(robot, "odometry")

    # Check which methods this sensor supports
    properties = await sensor.get_properties()
    print(f"Supports position: {properties.position_supported}")
    print(f"Supports linear velocity: {properties.linear_velocity_supported}")
    print(f"Supports angular velocity: {properties.angular_velocity_supported}")
    print(f"Supports compass heading: {properties.compass_heading_supported}")

    if properties.position_supported:
        position = await sensor.get_position()
        print(f"Position: {position}")

    if properties.linear_velocity_supported:
        velocity = await sensor.get_linear_velocity()
        print(f"Linear velocity: {velocity}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python movement_sensor_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir movement-sensor-test && cd movement-sensor-test
go mod init movement-sensor-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/movementsensor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("movement-sensor-test")

    robot, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithCredentials(utils.Credentials{
            Type:    utils.CredentialsTypeAPIKey,
            Payload: "YOUR-API-KEY",
        }),
        client.WithAPIKeyID("YOUR-API-KEY-ID"),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)

    sensor, err := movementsensor.FromProvider(robot, "odometry")
    if err != nil {
        logger.Fatal(err)
    }

    // Check which methods this sensor supports
    properties, err := sensor.Properties(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Supports position: %v\n", properties.PositionSupported)
    fmt.Printf("Supports linear velocity: %v\n", properties.LinearVelocitySupported)
    fmt.Printf("Supports angular velocity: %v\n", properties.AngularVelocitySupported)
    fmt.Printf("Supports compass heading: %v\n", properties.CompassHeadingSupported)

    if properties.PositionSupported {
        pos, alt, err := sensor.Position(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }
        fmt.Printf("Position: %v, altitude: %.2f\n", pos, alt)
    }

    if properties.LinearVelocitySupported {
        vel, err := sensor.LinearVelocity(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }
        fmt.Printf("Linear velocity: %v\n", vel)
    }
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Odometry position drifts over time" >}}

- This is inherent to wheel odometry. Small errors accumulate. For better
  accuracy, add a GPS or IMU and use the `merged` model.
- Check that `ticks_per_rotation` is accurate on your encoders.
- Verify `wheel_circumference_mm` and `width_mm` on your base.

{{< /expand >}}

{{< expand "GPS shows no fix" >}}

- GPS modules need a clear view of the sky. They don't work indoors.
- Initial fix can take 30-60 seconds (cold start) or longer in urban areas.

{{< /expand >}}

{{< expand "Some methods return errors" >}}

- Not all movement sensors support all methods. This is expected. Call
  `GetProperties` to see which methods your sensor supports.

{{< /expand >}}

## What's next

- [Movement sensor API reference](/dev/reference/apis/components/movement-sensor/): full method documentation.
- [Add a Base](/hardware/common-components/add-a-base/): the movement sensor
  typically pairs with a mobile base.
- [Capture and Sync Data](/data/capture-and-sync-data/): capture position and
  motion data over time.
