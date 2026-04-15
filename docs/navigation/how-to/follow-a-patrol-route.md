---
linkTitle: "Follow a patrol route"
title: "Follow a patrol route"
weight: 30
layout: "docs"
type: "docs"
description: "Define a sequence of waypoints and navigate them repeatedly."
---

A patrol route is a sequence of GPS waypoints the robot visits in order.
The navigation service drives between waypoints, replans around obstacles,
and retries on failure, but it does not loop. Your code has to re-add the
waypoints when the robot finishes to keep the patrol going.

## Prerequisites

- The [navigation service is configured](/navigation/how-to/navigate-to-waypoint/)
  and your robot can navigate to a single waypoint.

## Define a patrol route

Add multiple waypoints in the order you want the robot to visit them.
The navigation service visits waypoints in the order they were added.

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

    # Define the patrol route
    route = [
        GeoPoint(latitude=40.6640, longitude=-73.9387),
        GeoPoint(latitude=40.6645, longitude=-73.9382),
        GeoPoint(latitude=40.6642, longitude=-73.9375),
    ]

    # Run the patrol loop
    while True:
        # Add all waypoints
        for point in route:
            await nav.add_waypoint(point)
        print(f"Added {len(route)} waypoints")

        # Start navigating
        await nav.set_mode(Mode.MODE_WAYPOINT)

        # Wait until all waypoints are visited
        while True:
            waypoints = await nav.get_waypoints()
            if len(waypoints) == 0:
                print("Patrol complete, restarting...")
                break
            await asyncio.sleep(5)

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
    geo "github.com/kellydunn/golang-geo"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/services/navigation"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("patrol")

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

    // Define the patrol route
    route := []*geo.Point{
        geo.NewPoint(40.6640, -73.9387),
        geo.NewPoint(40.6645, -73.9382),
        geo.NewPoint(40.6642, -73.9375),
    }

    // Run the patrol loop
    for {
        for _, pt := range route {
            if err := nav.AddWaypoint(ctx, pt, nil); err != nil {
                logger.Fatal(err)
            }
        }
        fmt.Printf("Added %d waypoints\n", len(route))

        if err := nav.SetMode(ctx, navigation.ModeWaypoint, nil); err != nil {
            logger.Fatal(err)
        }

        // Wait until all waypoints are visited
        for {
            wps, err := nav.Waypoints(ctx, nil)
            if err != nil {
                logger.Fatal(err)
            }
            if len(wps) == 0 {
                fmt.Println("Patrol complete, restarting...")
                break
            }
            time.Sleep(5 * time.Second)
        }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

## How waypoint ordering works

The navigation service visits waypoints in the order they were added.
When all waypoints have been visited, GetWaypoints returns an empty list.
The service does not automatically loop. Your code is responsible for
re-adding waypoints to repeat the patrol.

If the robot cannot reach a waypoint, the service retries indefinitely
rather than skipping ahead. To move past a stuck waypoint, remove it
with RemoveWaypoint.

## Persist waypoints across restarts

With the **memory store** (default), waypoints are lost if `viam-server`
restarts. If your robot reboots mid-patrol, your code needs to re-add the
waypoints on startup.

With the **MongoDB store**, waypoints persist across restarts. The robot
resumes from the first unvisited waypoint after a reboot. This is better
for long-running patrol deployments where the robot may restart due to
updates or power cycling.

## What's next

- [Avoid obstacles](/navigation/how-to/avoid-obstacles/): add
  vision-based obstacle detection to your patrol.
- [Run actions at waypoints](/navigation/how-to/run-actions-at-waypoints/):
  capture data or trigger actions at each patrol stop.
- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust speed and deviation for your patrol environment.
