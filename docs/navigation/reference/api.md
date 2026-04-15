---
linkTitle: "API"
title: "Navigation service API"
weight: 20
layout: "docs"
type: "docs"
description: "The navigation service API for autonomous GPS-based navigation."
---

The navigation service API provides methods for controlling autonomous
GPS-based navigation. Use these methods to set the navigation mode, manage
waypoints, monitor the robot's location, and query obstacles and paths.

## GetMode

Get the current navigation mode.

**Returns:** `Mode` (MANUAL, WAYPOINT, or EXPLORE)

{{< tabs >}}
{{% tab name="Python" %}}

```python
mode = await nav.get_mode()
print(f"Current mode: {mode}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
mode, err := nav.Mode(ctx, nil)
```

{{% /tab %}}
{{< /tabs >}}

## SetMode

Set the navigation mode.

| Parameter | Type | Description                                                         |
| --------- | ---- | ------------------------------------------------------------------- |
| `mode`    | Mode | The mode to set: `MODE_MANUAL`, `MODE_WAYPOINT`, or `MODE_EXPLORE`. |

In **Manual** mode, the navigation service is passive. You control the
base directly. In **Waypoint** mode, the service takes control of the
base and navigates to unvisited waypoints.

Switching from Waypoint to Manual stops the current motion plan but
preserves all waypoints. Switching back to Waypoint resumes from the next
unvisited waypoint.

**Explore** mode is accepted by SetMode and returned by GetMode but is not
currently exposed in the Viam app's navigation UI mode selector. To use it,
call SetMode from an SDK.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.service.navigation import Mode

await nav.set_mode(Mode.MODE_WAYPOINT)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err := nav.SetMode(ctx, navigation.ModeWaypoint, nil)
```

{{% /tab %}}
{{< /tabs >}}

## GetLocation

Get the robot's current GPS location and compass heading.

**Returns:** `GeoPoint` with latitude and longitude, plus compass heading
in degrees (0 = north, 90 = east, 180 = south, 270 = west).

{{< tabs >}}
{{% tab name="Python" %}}

```python
location = await nav.get_location()
print(f"Lat: {location.latitude}, Lng: {location.longitude}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
geoPose, err := nav.Location(ctx, nil)
loc := geoPose.Location()
heading := geoPose.Heading()
```

{{% /tab %}}
{{< /tabs >}}

## GetWaypoints

Get all unvisited waypoints. Visited waypoints are not included.

**Returns:** list of `Waypoint` objects, each with an `id` and `location`
(GeoPoint).

{{< tabs >}}
{{% tab name="Python" %}}

```python
waypoints = await nav.get_waypoints()
for wp in waypoints:
    print(f"Waypoint {wp.id}: {wp.location.latitude}, {wp.location.longitude}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
waypoints, err := nav.Waypoints(ctx, nil)
for _, wp := range waypoints {
    pt := wp.ToPoint()
    fmt.Printf("Waypoint %s: %f, %f\n", wp.ID.Hex(), pt.Lat(), pt.Lng())
}
```

{{% /tab %}}
{{< /tabs >}}

## AddWaypoint

Add a GPS waypoint to the navigation queue. Waypoints are visited in the
order they are added.

| Parameter  | Type     | Description                                                |
| ---------- | -------- | ---------------------------------------------------------- |
| `location` | GeoPoint | The GPS coordinates (latitude, longitude) of the waypoint. |

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import GeoPoint

point = GeoPoint(latitude=40.6640, longitude=-73.9387)
await nav.add_waypoint(point)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
point := geo.NewPoint(40.6640, -73.9387)
err := nav.AddWaypoint(ctx, point, nil)
```

{{% /tab %}}
{{< /tabs >}}

## RemoveWaypoint

Remove a waypoint by its ID. Use this to skip a waypoint the robot can't
reach, or to clear the queue.

| Parameter | Type   | Description                        |
| --------- | ------ | ---------------------------------- |
| `id`      | string | The waypoint ID from GetWaypoints. |

{{< tabs >}}
{{% tab name="Python" %}}

```python
waypoints = await nav.get_waypoints()
if waypoints:
    await nav.remove_waypoint(waypoints[0].id)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
waypoints, _ := nav.Waypoints(ctx, nil)
if len(waypoints) > 0 {
    err := nav.RemoveWaypoint(ctx, waypoints[0].ID, nil)
}
```

{{% /tab %}}
{{< /tabs >}}

## GetObstacles

Get all known obstacles, including both static obstacles from configuration
and transient obstacles detected by vision services.

**Returns:** list of `GeoGeometry` objects.

{{< tabs >}}
{{% tab name="Python" %}}

```python
obstacles = await nav.get_obstacles()
print(f"Found {len(obstacles)} obstacles")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
obstacles, err := nav.Obstacles(ctx, nil)
```

{{% /tab %}}
{{< /tabs >}}

## GetPaths

Get the planned paths to waypoints, if any exist.

**Returns:** list of `Path` objects, each with a destination waypoint ID
and a list of GeoPoints defining the path.

{{< tabs >}}
{{% tab name="Python" %}}

```python
paths = await nav.get_paths()
for path in paths:
    print(f"Path to {path.destination_waypoint_id}: {len(path.geopoints)} points")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
paths, err := nav.Paths(ctx, nil)
for _, p := range paths {
    fmt.Printf("Path to %s: %d points\n",
        p.DestinationWaypointID().Hex(), len(p.GeoPoints()))
}
```

{{% /tab %}}
{{< /tabs >}}

## GetProperties

Get the navigation service's properties, including the map type.

**Returns:** `MapType` (NONE or GPS).

{{< tabs >}}
{{% tab name="Python" %}}

```python
props = await nav.get_properties()
print(f"Map type: {props.map_type}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
props, err := nav.Properties(ctx)
fmt.Printf("Map type: %v\n", props.MapType)
```

{{% /tab %}}
{{< /tabs >}}

## DoCommand

Send a model-specific command to the navigation service. The builtin
model does not define any DoCommand keys, so this is useful only with
custom navigation modules that document their own command schema.

| Parameter | Type | Description                           |
| --------- | ---- | ------------------------------------- |
| `command` | map  | Key-value pairs defining the command. |

{{< tabs >}}
{{% tab name="Python" %}}

```python
result = await nav.do_command({"custom_command": "value"})
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
result, err := nav.DoCommand(ctx, map[string]interface{}{"custom_command": "value"})
```

{{% /tab %}}
{{< /tabs >}}

## GetStatus

Return a generic status map for liveness checks. The content of the map
is implementation-defined; treat it as opaque unless a specific model
documents its fields.

{{< tabs >}}
{{% tab name="Python" %}}

```python
status = await nav.get_status()
print(status)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
status, err := nav.GetStatus(ctx)
```

{{% /tab %}}
{{< /tabs >}}
