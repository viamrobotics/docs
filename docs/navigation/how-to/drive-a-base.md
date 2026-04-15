---
linkTitle: "Drive a base"
title: "Drive a base directly from code"
weight: 35
layout: "docs"
type: "docs"
description: "Move a wheeled base with direct component commands for distance, angle, power, or velocity."
aliases:
  - /operate/mobility/move-base/
  - /how-tos/navigate/
  - /use-cases/navigate/
  - /motion-planning/motion-how-to/drive-a-base/
---

You have a wheeled base and want to drive it without waypoints, a map, or a
navigation service. The base component API exposes direct motion commands for
this case: drive a known distance, spin a known angle, or set linear and
angular power or velocity.

This is the lowest-level path for moving a base. For GPS waypoint navigation,
see [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/). For
SLAM-map-based navigation, see the
[`MoveOnMap`](/motion-planning/reference/api/#moveonmap) motion service
method.

## Before you start

- A configured base component. See the
  [base component documentation](/components/base/) for hardware setup.
- The base's motors work through the Viam app **TEST** panel on each motor's
  configure card.
- An SDK client connected to your machine. See
  [Create a web app](/operate/control/web-app/) or the language-specific
  quickstart.

## Direct motion commands

The base component API provides four motion methods:

| Method         | What it does                                                                    |
| -------------- | ------------------------------------------------------------------------------- |
| `MoveStraight` | Drive forward or backward a given distance at a given speed. Blocks until done. |
| `Spin`         | Rotate in place by a given angle at a given angular speed. Blocks until done.   |
| `SetPower`     | Set linear and angular power as normalized values (-1.0 to 1.0). Non-blocking.  |
| `SetVelocity`  | Set linear and angular velocity directly (mm/s and deg/s). Non-blocking.        |

Use `MoveStraight` and `Spin` when you know the distance or angle you want.
Use `SetPower` or `SetVelocity` for continuous control (for example, an
operator stick, or a sensor-driven control loop).

## Drive a base in a square

This example uses `MoveStraight` and `Spin` to walk a base around a 500 mm
square, stopping at each corner to turn 90 degrees.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio

from viam.components.base import Base
from viam.robot.client import RobotClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def drive_square(base):
    for _ in range(4):
        # Drive forward 500 mm at 500 mm/s.
        await base.move_straight(distance=500, velocity=500)
        # Spin 90 degrees to the left at 100 deg/s.
        await base.spin(angle=90, velocity=100)


async def main():
    async with await connect() as machine:
        my_base = Base.from_robot(machine, "my-base")
        await drive_square(my_base)


if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func driveSquare(ctx context.Context, b base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // Drive forward 500 mm at 500 mm/s.
        if err := b.MoveStraight(ctx, 500, 500.0, nil); err != nil {
            logger.Fatal(err)
        }
        // Spin 90 degrees to the left at 100 deg/s.
        if err := b.Spin(ctx, 90, 100.0, nil); err != nil {
            logger.Fatal(err)
        }
    }
}

func main() {
    logger := logging.NewLogger("client")
    ctx := context.Background()

    machine, err := client.New(
        ctx,
        "YOUR-MACHINE-ADDRESS",
        logger,
        client.WithDialOptions(utils.WithEntityCredentials(
            "YOUR-API-KEY-ID",
            utils.Credentials{
                Type:    utils.CredentialsTypeAPIKey,
                Payload: "YOUR-API-KEY",
            },
        )),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer machine.Close(ctx)

    myBase, err := base.FromProvider(machine, "my-base")
    if err != nil {
        logger.Fatal(err)
    }

    driveSquare(ctx, myBase, logger)
}
```

{{% /tab %}}
{{< /tabs >}}

Replace `my-base` with your base component's name, and replace the
credentials and address placeholders with the values from the **CONNECT**
tab in the Viam app.

## Set continuous power or velocity

For operator-driven control or sensor-driven loops, use `SetPower` or
`SetVelocity` rather than `MoveStraight`/`Spin`. Both methods take a linear
vector and an angular vector.

| Vector field | Meaning for linear (`SetPower`/`SetVelocity`)          | Meaning for angular                                       |
| ------------ | ------------------------------------------------------ | --------------------------------------------------------- |
| `X`          | (unused by built-in drivers)                           | Roll (unused by built-in drivers)                         |
| `Y`          | Forward/backward. Positive Y moves forward.            | Pitch (unused by built-in drivers)                        |
| `Z`          | Up/down (unused by built-in drivers for wheeled bases) | Yaw. Positive Z turns left (counterclockwise from above). |

`SetPower` values range from -1.0 to 1.0 (fraction of maximum). `SetVelocity`
takes linear velocity in millimeters per second and angular velocity in
degrees per second.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.base import Base, Vector3

my_base = Base.from_robot(machine, "my-base")

# Drive forward at 75% power with no rotation.
await my_base.set_power(linear=Vector3(x=0, y=0.75, z=0),
                        angular=Vector3(x=0, y=0, z=0))

# Or drive at a fixed velocity: 50 mm/s forward, 15 deg/s left yaw.
await my_base.set_velocity(linear=Vector3(x=0, y=50, z=0),
                           angular=Vector3(x=0, y=0, z=15))

# Stop.
await my_base.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "github.com/golang/geo/r3"
    "go.viam.com/rdk/components/base"
)

myBase, err := base.FromProvider(machine, "my-base")
if err != nil {
    logger.Fatal(err)
}

// Drive forward at 75% power.
if err := myBase.SetPower(ctx,
    r3.Vector{X: 0, Y: 0.75, Z: 0},
    r3.Vector{X: 0, Y: 0, Z: 0},
    nil); err != nil {
    logger.Fatal(err)
}

// Or drive at fixed velocity: 50 mm/s forward, 15 deg/s left yaw.
if err := myBase.SetVelocity(ctx,
    r3.Vector{X: 0, Y: 50, Z: 0},
    r3.Vector{X: 0, Y: 0, Z: 15},
    nil); err != nil {
    logger.Fatal(err)
}

// Stop.
if err := myBase.Stop(ctx, nil); err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

## When to use direct commands versus motion planning

- **Direct commands (this page)**: short, well-defined movements. No obstacles,
  no mapping, no planning. Fastest to set up. No path checking.
- [**MoveOnGlobe through the navigation service**](/navigation/how-to/navigate-to-waypoint/):
  drive to GPS coordinates with replanning, obstacle avoidance, and mode
  switching.
- **MoveOnMap**: drive to a pose on a SLAM map. Requires a SLAM service; see
  the [motion service API reference](/motion-planning/reference/api/#moveonmap).

## What's next

- [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/):
  autonomous GPS navigation with replanning.
- [Monitor a running plan](/motion-planning/motion-how-to/monitor-a-running-plan/):
  track non-blocking MoveOnGlobe or MoveOnMap executions.
- [Base API reference](/reference/apis/components/base/): full base component
  API surface.
