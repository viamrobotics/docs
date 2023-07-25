---
title: "The Navigation Service"
linkTitle: "Navigation"
description: "The Navigation Service uses GPS to autonomously navigate a rover to user defined endpoints."
type: docs
weight: 60
no_list: true
icon: "/services/icons/navigation.svg"
images: ["/services/icons/navigation.svg"]
tags: ["navigation", "services", "base", "rover"]
# SMEs: Raymond
---

The Navigation service is the stateful definition of Viam's [Motion Service](/services/motion/).
It uses GPS to autonomously navigate a rover [base](/components/base/) to user defined endpoints called `Waypoints`.
Once these waypoints are added and the mode of the service is [set to `MODE_WAYPOINT`](#setmode), the service begins to define the robot's path.

## Configuration

You must configure a [base](/components/base/) with a [movement sensor](/components/movement-sensor/) as part of your robot to configure a Navigation service.

The movement sensor must support `GetPosition`, `GetCompassHeading`, or `Orientation` in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [Sensor API](/components/sensor/#api).
If your movement sensor provides multiple methods, your robot will default to using the values returned by `GetCompassHeading`.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Services** subtab and navigate to the **Create service** menu.
Select the type `navigation` and enter a name for your service.

Click **Create service**:

![An example configuration for a Navigation service in the Viam app Config Builder.](/services/navigation/navigation-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
{
    "name": "your-navigation-service",
    "type": "navigation",
    "attributes": {
        "store": {
            "type": "memory"
        },
        "movement_sensor": "<your-movement-sensor>",
        "base": "<your-base>"
    }
}
    ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "test_navigation",
    "type": "navigation",
    "attributes": {
        "store": {
            "type": "mongodb",
            "config": {
                "uri": "mongodb://127.0.0.1:12345"
            }
        }
    },
    "movement_sensor": "your-movement-sensor",
    "base": "your-base",
    "obstacles":[{
        "geometries": [{
            "label":"your-label-for-this-obstacle",
            "orientation":{
                "type":"ov_degrees",
                    "value":{
                        "x":1,
                        "y":0,
                        "z":0,
                        "th": 90
                    }
            },
            "x":10,
            "y":10,
            "z":10,
            "translation":{
                "x":1,
                "y":1,
                "z":1
            }
        }],
        "location": {
            "latitude":1,
            "longitude":1
        }
    }]
}

```

{{% /tab %}}
{{< /tabs >}}

Next, add the JSON `"attributes"` you want the service to have.
The following attributes are available for `Navigation` services:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `store` | obj | **Required** | The type and configuration of data storage to use. Either type `"memory"`, where no additional configuration is needed and the waypoints are stored in local memory while the Navigation process is running, or `"mongodb"`, where data persists at the specified [MongoDB URI](https://www.mongodb.com/docs/manual/reference/connection-string) of your MongoDB deployment. |
| `base` | string | **Required** | The `name` you have configured for the [base](/components/base/) you are operating with this service. |
| `movement_sensor` | string | **Required** | The `name` of the [movement sensor](/components/movement-sensor/) you have configured for the base you are operating with this service. |
| `motion_service` | string | Optional | The `name` of the [Motion Service](/services/motion/) you have configured for the base you are operating with this service.
If you have not added a Motion Service to your robot, the default Motion Service will be used.
Reference this default service by using the name `"builtin"`. |
| `degs_per_sec` | float | Optional | The default angular velocity for the [base](/components/base/) in degrees per second. <br> Default: `60` |
| `meters_per_sec` | float | Optional | The default linear velocity for the [base](/components/base/) in meters per second. <br> Default: `0.3` |
| `obstacles` | obj | Optional | Any obstacles you wish to add to the robot's path. See the [Motion Service](/services/motion/) for more information. |

## API

The Navigation Service supports the following methods:

Method Name | Description
----------- | -----------
[`Mode`](#mode) | Get the mode the service is operating in.
[`SetMode`](#setmode) | Set the mode the service is operating in.
[`Location`](#location) | Get the current location of the robot.
[`Waypoints`](#waypoints) | Get the waypoints currently in the service's data storage.
[`AddWaypoint`](#addwaypoint) | Add a waypoint to the service's data storage.
[`RemoveWaypoint`](#removewaypoint) | Remove a waypoint from the service's data storage.
[`GetObstacles`](#getobstacles) | Get the obstacles currently in the service's data storage.

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a `Navigation` service, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code Sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Mode

Get the `Mode` the service is operating in.

There are three options for modes: `MODE_UNSPECIFIED`, `MODE_MANUAL`, or `MODE_WAYPOINT`.

- `MODE_UNSPECIFIED`: Do not perform autonomous navigation.
When you create a new service, its default mode is `MODE_UNSPECIFIED`.
- `MODE_WAYPOINT`: Start to look for added waypoints and begin autonomous navigation.
- `MODE_MANUAL`: Stop autonomous navigation between waypoints and allow the base to be controlled manually.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Mode)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Mode): The `Mode` the service is operating in.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Get the Mode the service is operating in
mode, err := myNav.Mode(context.Background(), nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [navigation.Mode.ValueType](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.Mode): The `Mode` the service is operating in.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.get_mode).

``` python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the Mode the service is operating in
await my_nav.get_mode()
```

{{% /tab %}}
{{< /tabs >}}

### SetMode

Set the `Mode` the service is operating in.

There are three options for modes: `MODE_UNSPECIFIED`, `MODE_MANUAL`, or `MODE_WAYPOINT`.

- `MODE_UNSPECIFIED`: Do not perform autonomous navigation.
When you create a new service, its default is `MODE_UNSPECIFIED`.
- `MODE_WAYPOINT`: Start to look for added waypoints and begin autonomous navigation.
- `MODE_MANUAL`: Stop autonomous navigation between waypoints and allow the base to be controlled manually.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `mode` [(Mode)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Mode): The `Mode` for the service to operate in.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Set the Mode the service is operating in to MODE_WAYPOINT and begin navigation
mode, err := myNav.SetMode(context.Background(), Mode.MODE_WAYPOINT, nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.
- `mode` [navigation.Mode.ValueType](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.Mode): The `Mode` for the service to operate in.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.set_mode).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Set the Mode the service is operating in to MODE_WAYPOINT and begin navigation
await my_nav.set_mode(Mode.ValueType.MODE_WAYPOINT)
```

{{% /tab %}}
{{< /tabs >}}

### Location

Get the current location of the robot in the navigation service.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The current location of the robot in the navigation service, represented in a `Point` with latitude (lat) and longitude (lng) values.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Get the current location of the robot in the navigation service
location, err := myNav.Location(context.Background(), nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(navigation.GeoPoint)](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoPoint): The current location of the robot in the navigation service, represented in a `GeoPoint` with latitude and longitude values.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.get_waypoints).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the current location of the robot in the navigation service
location = await my_nav.get_location()
```

{{% /tab %}}
{{< /tabs >}}

### Waypoints

Get an array of waypoints currently in the service's data storage.
These are locations designated within a path for the robot to navigate to.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]Waypoints)](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Waypoint): An array comprised of each `Waypoint` in the service's data storage. These are locations designated within a path for the robot to navigate to.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Get an array containing each waypoint stored by the navigation service
waypoints, err := myNav.Waypoints(context.Background(), nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[navigation.Waypoint])](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.Waypoint): An array comprised of each `Waypoint` in the service's data storage.
These are locations designated within a path for the robot to navigate to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.get_waypoints).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each waypoint stored by the navigation service
waypoints = await my_nav.get_waypoints()
```

{{% /tab %}}
{{< /tabs >}}

### AddWaypoint

Add a waypoint to the service's data storage.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `point` [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The current location of the robot in the navigation service, represented in a `Point` with latitude (lat) and longitude (lng) values.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Create a new waypoint with latitude and longitude values of 0 degrees
location = geo.NewPoint(0, 0)

// Add your waypoint to the service's data storage
err := myNav.AddWaypoint(context.Background(), location, nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `point`[(navigation.GeoPoint)](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoPoint): The current location of the robot in the navigation service, represented in a `GeoPoint` with latitude and longitude values.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.add_waypoint).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Create a new waypoint with latitude and longitude values of 0 degrees
location = GeoPoint(latitude=0, longitude=0)


# Add your waypoint to the service's data storage
await my_nav.add_waypoint(point=location)
```

{{% /tab %}}
{{< /tabs >}}

### RemoveWaypoint

Remove a waypoint from the service's data storage.
If the robot is currently navigating to this waypoint, the motion will be canceled, and the robot will proceed to the next waypoint.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(primitive.ObjectID)](https://pkg.go.dev/go.mongodb.org/mongo-driver/bson/primitive#ObjectID): The MongoDB ObjectID of the `Waypoint` to remove from the service's data storage.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Create a new ObjectID
waypoint_id = primitive.NewObjectID()

// Remove the waypoint matching that ObjectID from the service's data storage
err := myNav.RemoveWaypoint(context.Background(), waypoint_id, nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `id`[(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The MongoDB ObjectID of the `Waypoint` to remove from the service's data storage.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.remove_waypoint).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Remove the waypoint matching that ObjectID from the service's data storage
await my_nav.remove_waypoint(waypoint_id)
```

{{% /tab %}}
{{< /tabs >}}

### GetObstacles

Get an array of obstacles currently in the service's data storage.
These are locations designated for the robot to avoid when navigating.
See the [Motion Service](/services/motion/) for more information.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]*spatialmath.GeoObstacle)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoObstacle): An array comprised of each `GeoObstacle` in the service's data storage.
These are locations designated for the robot to avoid when navigating.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Get an array containing each obstacle stored by the navigation service
obstacles, err := myNav.GetObstacles(context.Background(), nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[navigation.GeoObstacle])](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoObstacle): An array comprised of each `GeoObstacle` in the service's data storage.
These are locations designated for the robot to avoid when navigating.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.get_obstacles).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each obstacle stored by the navigation service
obstacles = await my_nav.get_obstacles()
```

{{% /tab %}}
{{< /tabs >}}
