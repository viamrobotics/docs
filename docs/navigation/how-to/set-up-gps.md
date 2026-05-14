---
linkTitle: "Set up GPS"
title: "Set up GPS for navigation"
weight: 5
layout: "docs"
type: "docs"
description: "Configure a GPS movement sensor and verify it reports accurate position and heading before enabling navigation."
---

The navigation service needs a movement sensor that reports both GPS
position and compass heading. This guide helps you pick a GPS module,
configure it, and verify that the position and heading are accurate
enough to drive the robot.

## Choose a GPS module

In the [Viam registry](https://app.viam.com/registry), search for `gps` to see GPS-capable
movement sensor models. You can also search by manufacturer or chip name.

### GPS accuracy and what it means for navigation

Standard GPS is accurate to approximately 3 meters under open sky. In
environments with trees, buildings, or uneven terrain, accuracy degrades
due to signal interference.

The navigation service's `plan_deviation_m` parameter controls how far the
robot can drift from its planned path before replanning. The default is
2.6 meters, so if your GPS error is around 3 meters, normal GPS jitter
will exceed the threshold and the robot will replan constantly.

| GPS type          | Typical accuracy | Good `plan_deviation_m` range |
| ----------------- | ---------------- | ----------------------------- |
| Standard GPS      | 2-5 meters       | 5-10 meters                   |
| SBAS-enhanced GPS | 1-3 meters       | 3-5 meters                    |
| RTK GPS           | 1-10 centimeters | 0.5-2 meters                  |

Applications that need sub-meter accuracy, such as driving a narrow
corridor or approaching a charging dock, require RTK GPS. Search for
RTK modules in the registry.

## Configure the movement sensor

1. Open your machine in the [Viam app](https://app.viam.com).
2. Click the **+** button and select **Configuration block**.
3. Search for the model that matches your GPS hardware.
4. Name it (for example, `my-gps`) and click **Create**.
5. Configure the attributes as required by your module (serial port,
   baud rate, I2C address, or network settings).
6. Click **Save**.

## Verify GPS position

Before configuring navigation, confirm the movement sensor reports
accurate GPS data.

1. Find your movement sensor in the configuration view.
2. Expand the **TEST** section. If it shows **Resource is
   configuring...**, wait for the movement sensor's status badge to
   read **Ready**.
3. Check that **GetPosition** shows a latitude and longitude within a
   few meters of your actual location. A map on the right-hand side of
   the section plots the current position; confirm it matches your
   physical location.
4. Rotate the robot by hand and watch **GetCompassHeading** update
   smoothly. Zero degrees is north, 90 is east, 180 is south, 270 is
   west.

Movement-sensor sections only render when the module reports the
corresponding property. If **GetCompassHeading** or **GetPosition** is
missing, your module does not report that property; check
`GetProperties` against the module's documentation.

If the position is significantly wrong or the compass heading doesn't
change when you rotate the robot, check your wiring and module
configuration before proceeding.

### Compass interference

The compass (magnetometer) in many GPS/IMU modules is sensitive to
magnetic interference from motors, metal structures, and power wiring.
Common symptoms:

- Heading doesn't change when the robot rotates.
- Heading jumps erratically.
- Heading is consistently offset by a fixed amount.

To reduce interference:

- Mount the GPS module as far from motors and power wiring as practical.
- Run magnetometer calibration if your module supports it (check the
  module's documentation in the registry).
- Consider the
  [merged movement sensor](/hardware/common-components/add-a-movement-sensor/)
  model, which combines data from multiple sensors. For example, use GPS
  for position and a separately mounted IMU for heading.

## Verify with code

Read position and heading programmatically to confirm the data is
available to your application code.

{{< tabs >}}
{{% tab name="Python" %}}

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

    gps = MovementSensor.from_robot(robot, "my-gps")

    position, altitude = await gps.get_position()
    heading = await gps.get_compass_heading()
    properties = await gps.get_properties()

    print(f"Latitude:  {position.latitude}")
    print(f"Longitude: {position.longitude}")
    print(f"Altitude:  {altitude}m")
    print(f"Heading:   {heading} degrees")
    print(f"Supports position: {properties.position_supported}")
    print(f"Supports heading:  {properties.compass_heading_supported}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

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
    logger := logging.NewLogger("gps-test")

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

    gps, err := movementsensor.FromProvider(robot, "my-gps")
    if err != nil {
        logger.Fatal(err)
    }

    pos, alt, err := gps.Position(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }

    heading, err := gps.CompassHeading(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }

    props, err := gps.Properties(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }

    fmt.Printf("Latitude:  %f\n", pos.Lat())
    fmt.Printf("Longitude: %f\n", pos.Lng())
    fmt.Printf("Altitude:  %fm\n", alt)
    fmt.Printf("Heading:   %f degrees\n", heading)
    fmt.Printf("Supports position: %v\n", props.PositionSupported)
    fmt.Printf("Supports heading:  %v\n", props.CompassHeadingSupported)
}
```

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/):
  configure the navigation service and send your robot to a GPS coordinate.
- [Movement sensor API reference](/reference/apis/components/movement-sensor/):
  full method documentation.
