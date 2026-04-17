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

Once your GPS movement sensor reports accurate position and heading, the
navigation service can drive the base to a coordinate you choose. This
guide adds the navigation service to an existing base-and-GPS machine
and sends the robot to its first waypoint, first from the Control tab
and then from code.

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
   robot's GPS position. If the card shows **Resource is
   configuring...**, wait for the navigation service's status badge to
   read **Ready**.
3. Click on the map to add a waypoint. A marker appears at that location.
4. Above the map, find the **Mode** toggle (options: **Manual** /
   **Waypoint**) and select **Waypoint**.
5. The robot begins navigating to the waypoint. Watch its position update
   on the map.

When the robot reaches the waypoint, it marks the waypoint as visited.
If you've added multiple waypoints, it navigates to the next one in order.

### Using code

Add a waypoint and set the mode to Waypoint programmatically.

To get the credentials for the code below, go to your machine's page in
the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the same tab.

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

    geo "github.com/kellydunn/golang-geo"
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
    latitude, longitude := 40.6640, -73.9387
    target := geo.NewPoint(latitude, longitude)
    err = nav.AddWaypoint(ctx, target, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Printf("Added waypoint at %f, %f\n", latitude, longitude)

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

When navigation starts, the robot turns to face the waypoint, drives
toward it, and marks the waypoint visited on arrival. If more waypoints
are queued, the service drives to the next one automatically.

Two conditions trigger a replan during this sequence:

- The robot drifts more than `plan_deviation_m` (default 2.6 meters)
  from the planned path.
- A configured obstacle detector reports a new obstacle on the path.

## Troubleshooting

If the robot does not move, moves erratically, or stops short, see
[Monitor and troubleshoot navigation](/navigation/how-to/monitor-and-troubleshoot/).
That page covers the common failure modes in one place.

## What's next

- [Follow a patrol route](/navigation/how-to/follow-a-patrol-route/):
  navigate a sequence of waypoints in a loop.
- [Avoid obstacles](/navigation/how-to/avoid-obstacles/): add
  vision-based obstacle detection.
- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust speed, deviation, and polling for your environment.
