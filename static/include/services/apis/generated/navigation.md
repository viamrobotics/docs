### GetMode

Get the `Mode` the service is operating in.

There are two options for modes: `MODE_MANUAL` or `MODE_WAYPOINT`.

- `MODE_WAYPOINT`: Start to look for added waypoints and begin autonomous navigation.
- `MODE_MANUAL`: Stop autonomous navigation between waypoints and allow the base to be controlled manually.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.services.navigation.Mode.ValueType): The Mode the service is operating in.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the Mode the service is operating in
await my_nav.get_mode()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_mode).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Mode)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Mode): The `Mode` the service is operating in.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the Mode the service is operating in.
mode, err := myNav.Mode(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### SetMode

Set the `Mode` the service is operating in.

There are two options for modes: `MODE_MANUAL` or `MODE_WAYPOINT`.

- `MODE_WAYPOINT`: Start to look for added waypoints and begin autonomous navigation.
- `MODE_MANUAL`: Stop autonomous navigation between waypoints and allow the base to be controlled manually.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `mode` (viam.services.navigation.Mode.ValueType) (required): The Mode for the service to operate in.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Set the Mode the service is operating in to MODE_WAYPOINT and begin navigation
await my_nav.set_mode(Mode.ValueType.MODE_WAYPOINT)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.set_mode).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `mode` [(Mode)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Mode): The `Mode` for the service to operate in.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Set the Mode the service is operating in to ModeWaypoint and begin navigation.
err := myNav.SetMode(context.Background(), navigation.ModeWaypoint, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### GetLocation

Get the current location of the robot in the navigation service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.services.navigation.GeoPoint](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoPoint)): The current location of the robot in the navigation service, represented in a GeoPoint with latitude and longitude values.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the current location of the robot in the navigation service
location = await my_nav.get_location()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_location).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*spatialmath.GeoPose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoPose): The current location of the robot in the navigation service, represented in a `Point` with latitude and longitude values.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current location of the robot in the navigation service.
location, err := myNav.Location(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### GetWaypoints

Get an array of waypoints currently in the service's data storage.
These are locations designated within a path for the robot to navigate to.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.services.navigation.Waypoint]](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.Waypoint)): An array comprised of each Waypoint in the service’s data storage. These are locations designated within a path for the robot to navigate to.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each waypoint stored by the navigation service
waypoints = await my_nav.get_waypoints()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_waypoints).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]Waypoint)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Waypoint): An array comprised of each `Waypoint` in the service's data storage. These are locations designated within a path for the robot to navigate to.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
waypoints, err := myNav.Waypoints(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### AddWaypoint

Add a waypoint to the service's data storage.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `point` ([viam.services.navigation.GeoPoint](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoPoint)) (required): The current location of the robot in the navigation service, represented in a GeoPoint with latitude and longitude values.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

 # Create a new waypoint with latitude and longitude values of 0 degrees
 location = GeoPoint(latitude=0, longitude=0)


 # Add your waypoint to the service's data storage
 await my_nav.add_waypoint(point=location)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.add_waypoint).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `point` [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The current location of the robot in the navigation service, represented in a `Point` with latitude (lat) and longitude (lng) values.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Create a new waypoint with latitude and longitude values of 0 degrees.
// Assumes you have imported "github.com/kellydunn/golang-geo" as `geo`.
location := geo.NewPoint(0, 0)

// Add your waypoint to the service's data storage.
err := myNav.AddWaypoint(context.Background(), location, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### RemoveWaypoint

Remove a waypoint from the service's data storage.
If the robot is currently navigating to this waypoint, the motion will be canceled, and the robot will proceed to the next waypoint.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The MongoDB ObjectID of the Waypoint to remove from the service’s data storage.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Remove the waypoint matching that ObjectID from the service's data storage
await my_nav.remove_waypoint(waypoint_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.remove_waypoint).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(primitive.ObjectID)](https://pkg.go.dev/go.mongodb.org/mongo-driver/bson/primitive#ObjectID): The MongoDB ObjectID of the `Waypoint` to remove from the service's data storage.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Assumes you have already called AddWaypoint once and the waypoint has not yet been reached.
waypoints, err := myNav.Waypoints(context.Background(), nil)
if (err != nil || len(waypoints) == 0) {
    return
}

// Remove the first waypoint from the service's data storage.
err = myNav.RemoveWaypoint(context.Background(), waypoints[0].ID, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### GetObstacles

Get an array or list of the obstacles currently in the service's data storage.
These are objects designated for the robot to avoid when navigating.
These include all transient obstacles which are discovered by the vision services configured for the navigation service, in addition to the obstacles that are configured as a part of the service.
See the [motion service](/services/motion/) for more information.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.services.navigation.GeoGeometry]](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoGeometry)): A list comprised of each GeoGeometry in the service’s data storage. These are objects designated for the robot to avoid when navigating.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each obstacle stored by the navigation service
obstacles = await my_nav.get_obstacles()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_obstacles).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]*spatialmath.GeoGeometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoGeometry): An array comprised of each `GeoObstacle` in the service's data storage. These are objects designated for the robot to avoid when navigating.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get an array containing each obstacle stored by the navigation service.
obstacles, err := myNav.Obstacles(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### GetPaths

Get each path, the series of geo points the robot plans to travel through to get to a destination waypoint, in the machine's motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.navigation.Path]](https://python.viam.dev/autoapi/viam/proto/service/navigation/index.html#viam.proto.service.navigation.Path)): An array comprised of Paths, where each path is either a user-provided destination or a Waypoint, along with the corresponding set of geopoints. This outlines the route the machine is expected to take to reach the specified destination or Waypoint.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each path stored by the navigation service
paths = await my_nav.get_paths()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_paths).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]*Path)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Path): An array of paths, each path being a user-provided destination, or [`Waypoint`](#addwaypoint), and the set of [geo `Point`s](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point) the robot plans to travel through to get there.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get an array containing each path stored by the navigation service.
paths, err := myNav.Paths(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get information about the navigation service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.services.navigation.MapType.ValueType): Information about the type of map the service is using.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the properties of the current navigation service.
nav_properties = await my_nav.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Properties): Information about the type of map the service is using.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the properties of the current navigation service.
navProperties, err := myNav.Properties(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own navigation service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
service = SERVICE.from_robot(robot, "builtin")  # replace SERVICE with the appropriate class

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await service.do_command(command=my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
