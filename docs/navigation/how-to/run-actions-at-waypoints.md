---
linkTitle: "Run actions at waypoints"
title: "Run actions at waypoints"
weight: 60
layout: "docs"
type: "docs"
description: "Capture data, take readings, or trigger actions when the robot reaches each waypoint."
---

The navigation service drives the robot between waypoints, but it doesn't
perform actions at each stop. To capture an image, take a sensor reading,
or trigger an alert at each waypoint, write code that monitors the robot's
progress and acts when a waypoint is reached.

## Detect waypoint arrivals from the client

The navigation service has no arrival callback. To run actions at each
stop, poll `GetWaypoints` from your client code, watch the list shrink,
and take action each time it does. The loop looks like this:

1. Add waypoints to the navigation service.
2. Set the mode to Waypoint.
3. Poll GetWaypoints to detect when a waypoint is visited (it disappears
   from the list).
4. When a waypoint is visited, run your action.
5. Repeat until all waypoints are visited.

## Example: capture an image at each waypoint

This example navigates to a sequence of GPS coordinates and captures a
camera image at each one.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from datetime import datetime
from viam.robot.client import RobotClient
from viam.services.navigation import NavigationClient
from viam.components.camera import Camera
from viam.proto.common import GeoPoint
from viam.proto.service.navigation import Mode


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    nav = NavigationClient.from_robot(robot, "my-nav")
    cam = Camera.from_robot(robot, "my-cam")

    # Define inspection points
    inspection_route = [
        GeoPoint(latitude=40.6640, longitude=-73.9387),
        GeoPoint(latitude=40.6645, longitude=-73.9382),
        GeoPoint(latitude=40.6642, longitude=-73.9375),
    ]

    # Add all waypoints
    for point in inspection_route:
        await nav.add_waypoint(point)

    # Start navigating
    await nav.set_mode(Mode.MODE_WAYPOINT)

    # Track which waypoints have been visited
    previous_count = len(inspection_route)
    waypoint_index = 0

    while True:
        waypoints = await nav.get_waypoints()
        current_count = len(waypoints)

        # A waypoint was visited when the count decreases
        if current_count < previous_count:
            print(f"Reached waypoint {waypoint_index + 1}")

            # Pause navigation to hold position while capturing
            await nav.set_mode(Mode.MODE_MANUAL)

            # Capture image
            images, metadata = await cam.get_images()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"waypoint_{waypoint_index + 1}_{timestamp}.jpg"

            # Save or process the image
            print(f"Captured image: {filename}")

            # Resume navigation
            await nav.set_mode(Mode.MODE_WAYPOINT)

            waypoint_index += 1
            previous_count = current_count

        if current_count == 0:
            print("Inspection complete")
            break

        await asyncio.sleep(2)

    await nav.set_mode(Mode.MODE_MANUAL)
    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{< /tabs >}}

## How it works

The navigation service marks each waypoint visited on arrival, and
`GetWaypoints` returns only the unvisited ones. That is why a shrinking
count means the robot just reached a waypoint.

When a waypoint is visited:

1. Switch to Manual mode to pause navigation and hold position.
2. Perform your action (capture image, read sensor, send alert).
3. Switch back to Waypoint mode to resume navigation to the next waypoint.

Switching to Manual mode stops the current motion plan but preserves the
remaining waypoints. Switching back to Waypoint mode resumes navigation
from the next unvisited waypoint.

## Other actions you can run at waypoints

The same poll-and-act loop works with any Viam API call. Common
substitutions for the camera step:

- Sensor readings with `sensor.get_readings()` to log environmental
  data at each location.
- Vision detections with `vision.get_detections_from_camera("cam")` to
  run object detection on arrival.
- Alerts through a webhook or logger when the robot reaches a specific
  location.
- Gripper operations to pick or place at designated waypoints.

## What's next

- [Follow a patrol route](/navigation/how-to/follow-a-patrol-route/):
  run waypoint actions on a repeating patrol.
- [Capture and sync data](/data/capture-sync/capture-and-sync-data/):
  configure automatic data capture for your camera or sensors.
