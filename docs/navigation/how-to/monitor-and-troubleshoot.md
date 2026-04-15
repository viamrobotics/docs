---
linkTitle: "Monitor and troubleshoot"
title: "Monitor and troubleshoot navigation"
weight: 70
layout: "docs"
type: "docs"
description: "Use the Control tab map, read logs, and debug common navigation problems."
---

## Monitor navigation in the Viam app

The Control tab shows a live map with your robot's position, waypoints,
and obstacles. Use it to monitor navigation in real time.

1. Go to your machine's **CONTROL** tab.
2. Find the navigation service card. If the card shows **Resource is
   configuring...**, wait for the navigation service's status badge to
   read **Ready**.
3. The navigation card shows:
   - **Robot position** on the map with a directional marker showing heading.
   - **Waypoints** as markers on the map. Click the map to add a waypoint;
     use the **Waypoints** tab in the map's side panel to inspect or
     remove waypoints.
   - **Obstacles** (both static and vision-detected) on the map, with a
     list in the **Obstacles** tab of the side panel.
   - A **Mode** toggle above the map to switch between **Manual** and
     **Waypoint**.
   - Map controls above the map to switch between **2D** and **3D**
     views, center the map, and toggle satellite imagery.

## Enable debug logging

Set `log_file_path` in your navigation service configuration to write
detailed logs to a file:

```json
{
  "log_file_path": "/tmp/navigation.log"
}
```

The log includes mode transitions, waypoint navigation attempts and
completions, obstacle detections, frame transformations, and motion
service calls. This is the most useful tool for understanding why the
robot behaves unexpectedly.

You can also check the **LOGS** tab in the Viam app for errors from the
navigation and motion services.

## Common problems

{{< expand "Robot doesn't move after setting Waypoint mode" >}}

1. Check that waypoints exist: call GetWaypoints or check the Control tab
   map. The service needs at least one unvisited waypoint to navigate.
2. Check the LOGS tab for motion service errors. Common causes:
   - The base isn't responding (hardware or wiring issue).
   - The movement sensor isn't returning position data (GPS not locked).
   - The motion service can't plan a path (obstacles blocking all routes).
3. Verify the base works independently by testing it from its TEST section
   in the configure tab.

{{< /expand >}}

{{< expand "Logs show repeated 'MoveOnGlobe not supported' errors" >}}

The navigation service drives the base by calling `MoveOnGlobe` on its
configured motion service. The built-in motion service does not
implement `MoveOnGlobe`; it returns "not supported" and the navigation
loop retries indefinitely.

Configure your navigation service's `motion_service` attribute to name
a motion-service module that implements `MoveOnGlobe`. See
[Navigation service configuration](/navigation/reference/navigation-service/#optional-attributes).

{{< /expand >}}

{{< expand "Robot replans constantly and makes slow progress" >}}

Your `plan_deviation_m` is likely lower than your GPS error. The robot
replans because normal GPS jitter (2-5 meters with standard GPS) exceeds
the deviation threshold (default 2.6 meters).

Fix: increase `plan_deviation_m` to 5-10 meters for standard GPS. See
[Tune navigation behavior](/navigation/how-to/tune-navigation/) for
guidance on setting this relative to your GPS accuracy.

{{< /expand >}}

{{< expand "Robot moves in circles or turns the wrong way" >}}

This usually indicates a compass heading problem:

- **Compass interference from motors:** Mount the GPS/IMU module farther
  from motors and power wiring.
- **Compass not calibrated:** Run magnetometer calibration per your
  module's documentation.
- **Heading offset:** The compass reports a consistent offset (for
  example, 90 degrees off). Check the module's orientation configuration.

Verify by watching the **GetCompassHeading** value in the movement
sensor's **TEST** section while rotating the robot by hand. The heading
should change smoothly and correspond to the actual direction.

{{< /expand >}}

{{< expand "Robot gets stuck at a waypoint and retries indefinitely" >}}

When the navigation service can't reach a waypoint (obstacle it can't
navigate around, GPS position it can't get close enough to), it retries
the same waypoint indefinitely. It does not skip to the next waypoint.

To unblock:

- Remove the stuck waypoint programmatically with RemoveWaypoint, or
  open the navigation service card on **CONTROL**, click the
  **Waypoints** tab in the map's side panel, and remove the waypoint
  there.
- Check whether a static obstacle or bounding region prevents the robot
  from reaching that location.
- Check whether vision-based obstacle detection is producing false
  positives that block the path.

{{< /expand >}}

{{< expand "Robot navigates but stops short of the waypoint" >}}

The motion service considers a waypoint reached when the robot is within
the planning tolerance of the target. With standard GPS accuracy, the
robot may stop 2-5 meters from the intended coordinates because the GPS
position satisfies the arrival condition even though the robot isn't
exactly at the target.

For tighter arrival accuracy, use RTK GPS.

{{< /expand >}}

{{< expand "Obstacles aren't detected" >}}

1. Verify the vision service detects obstacles independently. Open
   the vision service's **TEST** section, select your camera from the
   **Camera** dropdown, then toggle **Show object point clouds** on.
   Confirm 3D object point clouds appear.
2. Check `obstacle_polling_frequency_hz`. At 0 Hz, no obstacle polling
   occurs.
3. Check that the camera and vision service names in `obstacle_detectors`
   match the exact names in your configuration.
4. Check the LOGS tab for frame transformation errors. The navigation
   service needs to transform obstacle positions from the camera frame
   to geographic coordinates through the movement sensor.

{{< /expand >}}

{{< expand "GPS position jumps or is inaccurate" >}}

- Verify you have clear sky visibility. Trees, buildings, and overhead
  structures degrade GPS accuracy.
- Check the number of satellites your GPS module is tracking (if your
  module exposes this data).
- Consider upgrading to an RTK GPS module for sub-meter accuracy.
- If the position jumps between two locations, you may have multipath
  interference from nearby reflective surfaces.

{{< /expand >}}

## What's next

- [Tune navigation behavior](/navigation/how-to/tune-navigation/):
  adjust parameters based on what you observe.
- [Navigation service configuration](/navigation/reference/navigation-service/):
  full reference for all configuration parameters.
