---
linkTitle: "GPS waypoint navigation"
title: "Quickstart: GPS waypoint navigation"
weight: 40
layout: "docs"
type: "docs"
description: "Configure the navigation service end-to-end with fake components, then verify the waypoint API. Swap in real GPS hardware when you are ready."
---

In this quickstart we will configure the navigation service with a
fake wheeled base and a fake GPS movement sensor, then exercise the
waypoint API to add, read, and remove waypoints. You will end up with
a working navigation configuration that is ready to drive real
hardware; all that changes later is the component models.

{{< alert title="About driving the fake base" color="note" >}}

The fake movement sensor returns a fixed position (roughly Prospect
Park, Brooklyn). Because that position never updates, actually
setting `MODE_WAYPOINT` would cause the navigation service to loop
indefinitely trying to reach the target. This tutorial covers
configuration and API verification only. When you have a real
GPS-capable movement sensor on a real base, the same code drives
the robot; see
[Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/).

{{< /alert >}}

Expected total time: about 15 minutes.

## 1. Add the fake base

In the [Viam app](https://app.viam.com), go to your machine's
**CONFIGURE** tab.

1. Click **+** and add a **base** component.
2. Choose the **fake** model.
3. Name it **my-base**.
4. Click **Create** and **Save**.

## 2. Add the fake movement sensor

1. Click **+** and add a **movement_sensor** component.
2. Choose the **fake** model.
3. Name it **my-gps**.
4. Click **Create** and **Save**.

The fake movement sensor reports a static position, compass heading,
and velocity. It implements the GPS interface the navigation service
needs.

## 3. Add the navigation service

1. Click **+** and add a **Service**.
2. Select **navigation**.
3. Choose the **builtin** model.
4. Name it **my-nav**.
5. In the attributes, set:

```json
{
  "base": "my-base",
  "movement_sensor": "my-gps",
  "map_type": "GPS",
  "store": { "type": "memory" }
}
```

Click **Save**.

This is the minimal navigation configuration: which base to drive,
which movement sensor reports position, what kind of map, and where
to store waypoints. The navigation service uses sensible defaults
for every other attribute (speeds, deviation threshold, polling
frequencies). See
[Navigation service configuration](/navigation/reference/navigation-service/)
for the full list.

## 4. Read the current location

Create a file named `gps_nav.py`:

```python
import asyncio

from viam.robot.client import RobotClient
from viam.services.navigation import NavigationClient
from viam.proto.common import GeoPoint


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def main():
    async with await connect() as machine:
        nav = NavigationClient.from_robot(machine, "my-nav")

        # 1. Where does the navigation service think we are?
        location = await nav.get_location()
        print(
            f"location: "
            f"lat={location.location.latitude:.6f} "
            f"lng={location.location.longitude:.6f} "
            f"heading={location.compass_heading:.1f}"
        )


if __name__ == "__main__":
    asyncio.run(main())
```

Replace the placeholder strings and run:

```sh
pip install viam-sdk
python gps_nav.py
```

Expected output:

```text
location: lat=40.700000 lng=-73.980000 heading=25.0
```

Those are the fake movement sensor's constant values. A real GPS
would return the robot's actual position and heading, updated at the
polling frequency.

## 5. Add and read waypoints

Extend the script to add two waypoints and read the queue:

```python
async def main():
    async with await connect() as machine:
        nav = NavigationClient.from_robot(machine, "my-nav")

        # Current location.
        location = await nav.get_location()
        print(
            f"location: "
            f"lat={location.location.latitude:.6f} "
            f"lng={location.location.longitude:.6f}"
        )

        # Add two waypoints.
        await nav.add_waypoint(
            GeoPoint(latitude=40.701000, longitude=-73.981000),
        )
        await nav.add_waypoint(
            GeoPoint(latitude=40.702000, longitude=-73.982000),
        )
        print("added 2 waypoints")

        # Read the queue. Unvisited waypoints only.
        waypoints = await nav.get_waypoints()
        for wp in waypoints:
            print(
                f"  {wp.id}: "
                f"lat={wp.location.latitude:.6f} "
                f"lng={wp.location.longitude:.6f}"
            )

        # Remove the first waypoint.
        if waypoints:
            await nav.remove_waypoint(waypoints[0].id)
            print("removed first waypoint")

        # Read the queue again.
        waypoints = await nav.get_waypoints()
        print(f"{len(waypoints)} waypoint(s) remaining")
```

Run it:

```sh
python gps_nav.py
```

Expected output:

```text
location: lat=40.700000 lng=-73.980000
added 2 waypoints
  <id1>: lat=40.701000 lng=-73.981000
  <id2>: lat=40.702000 lng=-73.982000
removed first waypoint
1 waypoint(s) remaining
```

The waypoint IDs are generated by the navigation service. The memory
store keeps them only for the lifetime of the service; restarting
`viam-server` clears the queue.

## 6. Read the mode

The navigation service has three modes: `MANUAL`, `WAYPOINT`, and
`EXPLORE`. Only Manual and Waypoint are exposed in the Viam app's UI
mode selector; Explore is SDK-only.

```python
from viam.proto.service.navigation import Mode

mode = await nav.get_mode()
print(f"current mode: {mode}")
```

The default starting mode is `MANUAL`. In Manual mode the navigation
service is passive; your code drives the base directly. Setting mode
to `WAYPOINT` hands control to the service.

## 7. What you did NOT do (and why)

You did not set the mode to `WAYPOINT`. If you did, the navigation
service would:

1. Plan a path from the current GPS position to the next waypoint.
2. Call `MoveOnGlobe` on the motion service to execute.
3. Poll the movement sensor at `position_polling_frequency_hz`.
4. Trigger a replan if the reported position drifts beyond
   `plan_deviation_m` from the plan.

The fake movement sensor reports a fixed position that never
changes. Steps 3 and 4 would fire continuously because the reported
position never matches the planned position. The service would loop.

With real GPS hardware, the movement sensor reports the robot's
actual drifting, updating position, and the navigation service
converges on each waypoint as the base moves.

## 8. Swap to real hardware

When you have a real GPS-capable movement sensor and a real wheeled
base, change two component models:

- **Movement sensor**: change `model` from `fake` to the GPS module
  you use (for example, a `gps-nmea` serial GPS, an RTK-capable GPS,
  or a `merged` sensor that fuses GPS with IMU).
- **Base**: change `model` from `fake` to the wheeled base module
  that matches your hardware.

The navigation service configuration and the Python code above do
not change.

## Where to next

- [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/):
  the same flow with a real robot, including setting waypoint mode
  and monitoring progress.
- [Tune navigation](/navigation/how-to/tune-navigation/):
  `plan_deviation_m`, `replan_cost_factor`, and polling rates —
  the parameters you tune for your specific environment.
- [Navigation service configuration](/navigation/reference/navigation-service/):
  the full reference for all attributes.
- [Replanning behavior](/motion-planning/replanning-behavior/):
  when and how the navigation service replans during execution.
