---
linkTitle: "Navigate to waypoint"
title: "Navigate to a waypoint"
weight: 20
layout: "docs"
type: "docs"
description: "Configure the navigation service and autonomously navigate to GPS waypoints."
aliases:
  - /navigation/how-to/drive-the-base/
  - /navigation/how-to/move-to-gps-coordinate/
---

This guide walks you through configuring the navigation service and sending
your robot to its first GPS waypoint.

## Prerequisites

- A configured [base](/hardware/common-components/add-a-base/) that drives
  your robot.
- A configured [movement sensor](/navigation/how-to/set-up-gps/) that
  provides GPS position and compass heading. Verify it reports accurate
  data before proceeding.
- Your machine is online in the [Viam app](https://app.viam.com).

## Add the navigation service

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for **navigation** and select the **builtin** model.
4. Name it (for example, `my-nav`) and click **Create**.

## Configure required attributes

Set these attributes in the configuration panel:

- **base**: the name of your base component (for example, `my-base`).
- **movement_sensor**: the name of your GPS movement sensor (for example,
  `my-gps`).
- **map_type**: select **GPS**.

Leave the other attributes at their defaults for now.
See [navigation service configuration](/navigation/reference/navigation-service/)
for all available attributes and what they control.

Click **Save**.

## Send the robot to a waypoint

You can add waypoints through the Viam app's Control tab or from code.

### Using the Control tab

1. Go to your machine's **CONTROL** tab.
2. Find the navigation service card. It shows a map centered on your
   robot's GPS position.
3. Click on the map to add a waypoint. A marker appears at that location.
4. Switch the mode to **Waypoint**.
5. The robot begins navigating to the waypoint. Watch its position update
   on the map.

When the robot reaches the waypoint, it marks the waypoint as visited.
If you've added multiple waypoints, it navigates to the next one in order.

### Using code

Add a waypoint and set the mode to Waypoint programmatically.

To get the credentials for the code below, go to your machine's page in
the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on. Copy the machine address, API key, and
API key ID from the code sample.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.robot.client import RobotClient
from viam.services.navigation import NavigationClient
from viam.proto.common import GeoPoint
from viam.proto.service.navigation import Mode


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    nav = NavigationClient.from_robot(robot, "my-nav")

    # Add a waypoint (replace with your target coordinates)
    target = GeoPoint(latitude=40.6640, longitude=-73.9387)
    await nav.add_waypoint(target)
    print(f"Added waypoint at {target.latitude}, {target.longitude}")

    # Start navigating
    await nav.set_mode(Mode.MODE_WAYPOINT)
    print("Navigation started")

    # Monitor progress
    while True:
        location = await nav.get_location()
        waypoints = await nav.get_waypoints()
        print(f"Position: {location.latitude:.6f}, {location.longitude:.6f}")
        print(f"Remaining waypoints: {len(waypoints)}")

        if len(waypoints) == 0:
            print("All waypoints reached")
            break

        await asyncio.sleep(2)

    # Stop navigation
    await nav.set_mode(Mode.MODE_MANUAL)
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
    "time"

    "github.com/golang/geo/s2"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/services/navigation"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("nav-test")

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

    nav, err := navigation.FromProvider(robot, "my-nav")
    if err != nil {
        logger.Fatal(err)
    }

    // Add a waypoint (replace with your target coordinates)
    target := s2.LatLngFromDegrees(40.6640, -73.9387)
    point := s2.PointFromLatLng(target)
    geoPoint := geo.NewPoint(target.Lat.Degrees(), target.Lng.Degrees())
    err = nav.AddWaypoint(ctx, geoPoint, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Added waypoint at %f, %f\n", target.Lat.Degrees(), target.Lng.Degrees())

    // Start navigating
    err = nav.SetMode(ctx, navigation.ModeWaypoint, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Println("Navigation started")

    // Monitor progress
    for {
        loc, err := nav.Location(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }
        waypoints, err := nav.Waypoints(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }

        fmt.Printf("Position: %f, %f\n", loc.Location().Lat(), loc.Location().Lng())
        fmt.Printf("Remaining waypoints: %d\n", len(waypoints))

        if len(waypoints) == 0 {
            fmt.Println("All waypoints reached")
            break
        }

        time.Sleep(2 * time.Second)
    }

    // Stop navigation
    nav.SetMode(ctx, navigation.ModeManual, nil)
}
```

{{% /tab %}}
{{< /tabs >}}

## What to expect

When navigation starts:

- The robot turns to face the waypoint, then drives toward it.
- If the robot deviates from its path by more than `plan_deviation_m`
  (default 2.6 meters), the service automatically replans.
- If an obstacle is detected (from configured obstacle detectors), the
  service replans around it.
- When the robot reaches the waypoint, it marks it as visited and stops
  (or moves to the next waypoint if more are queued).

## Troubleshooting

{{< expand "Robot doesn't move" >}}

- Confirm the machine shows as **Live** in the Viam app.
- Confirm the navigation mode is set to **Waypoint** (not Manual).
- Check the **LOGS** tab for errors from the navigation or motion service.
- Verify your base responds to direct commands first (use the base's
  TEST section in the configure tab).
- Verify your GPS movement sensor reports a valid position.

{{< /expand >}}

{{< expand "Robot moves erratically or in circles" >}}

- Check compass heading accuracy. If the compass is affected by motor
  interference, the robot won't know which direction to face. See
  [Set up GPS](/navigation/how-to/set-up-gps/) for interference guidance.
- Increase `plan_deviation_m` if the robot replans too frequently due
  to GPS jitter. See [Tune navigation](/navigation/how-to/tune-navigation/).

{{< /expand >}}

{{< expand "Robot stops before reaching waypoint" >}}

- The robot may be detecting an obstacle it can't navigate around. Check
  GetObstacles from the API or the Control tab map for detected obstacles.
- If using obstacle detectors, check that the vision service isn't
  producing false positives.

{{< /expand >}}

## What's next

- [Follow a patrol route](/navigation/how-to/follow-a-patrol-route/):
  navigate a sequence of waypoints in a loop.
- [Avoid obstacles](/navigation/how-to/avoid-obstacles/): add
  vision-based obstacle detection.
- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust speed, deviation, and polling for your environment.
