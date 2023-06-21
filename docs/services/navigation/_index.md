---
title: "The Navigation Service"
linkTitle: "Navigation"
description: "The Navigation Service uses GPS to autonomously navigate a rover to user defined endpoints."
type: docs
weight: 60
no_list: true
icon: "/services/img/icons/navigation.svg"
images: ["/services/img/icons/navigation.svg"]
tags: ["navigation", "services", "base", "rover"]
# SMEs: Raymond
---

The Navigation service is the stateful definition of Viam's [Motion Service](/services/motion/).
It uses GPS to autonomously navigate a rover [base](/components/base/) to user defined endpoints called `Waypoints`.
Once these waypoints are added and the mode of the service is [set to `waypoints`](#setmode), the service begins to define the robot's path.

## Configuration

You must configure a [base](/components/base/) with a [movement sensor](/components/movement-sensor/) as part of your robot to configure a Navigation service.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Services** subtab and navigate to the **Create service** menu.
Select the type `navigation` and enter a name for your service.

Click **Create service**:

![An example configuration for a Navigation service in the Viam app Config Builder.](img/navigation-ui-config.png)

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
        "movement_sensor": "test_movement",
        "base": "test_base"
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
                "uri": "mongodb://127.0.0.1:27017"
            } 
        }
        },
        "movement_sensor": "test_movement",
        "base": "test_base",
        "obstacles":[{
            "geometries": [{
                "label":"aLabel",
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
            "location":{
                "latitude":1,
                "longitude":1
            }
        }]
    }
}
```

{{% /tab %}}
{{< /tabs >}}

Next, add the JSON `"attributes"` you want the service to have.
The following attributes are available for `Navigation` services:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `store` | obj | **Required** | The type and configuration of data storage to use. Either type `"memory"`, where no additional configuration is needed and the waypoints are stored in local memory while the Navigation process is running, or `"mongodb"`, where data persists at the specified [MongoDB URI](https://www.mongodb.com/docs/manual/reference/connection-string) of your MongoDB deployment. |
| `base` | string | **Required** | The `name` of the [base](/components/base/) you have configured for the base you are operating with this service. |
| `movement_sensor` | string | **Required** | The `name` of the [movement sensor](/components/movement-sensor/) you have configured for the base you are operating with this service. |
| `motion_service` | string | Optional | The `name` of the [Motion Service](/services/motion/) you have configured for the base you are operating with this service. If you have not added a Motion Service to your robot, a new instance is added.|
| `degs_per_sec` | float | Optional | The default angular velocity for the [base](/components/base/) in degrees per second. <br> Default: `45` |
| `meters_per_sec` | float | Optional | The default linear velocity for the [base](/components/base/) in meters per second. <br> Default: `0.5` |
| `obstacles` | obj | Optional | Any obstacles you wish to add to the robot's path. See the [Motion Service](/services/motion/) for more information. |

## API

The Navigation Service supports the following methods:

Method Name | Description
----------- | -----------
[`Mode`](#mode) | Get the mode the service is operating in.
[`SetMode`](#setmode) | Set the mode the service is operating in.
[`Location`](#location) | Get the current location of the robot.
[`Waypoints`](#waypoints) | Get an array of waypoints currently in the service's data storage.
[`AddWaypoint`](#addwaypoint) | Add a waypoint to the service's data storage.
[`RemoveWaypoint`](#removewaypoint) | Remove a waypoint from the service's data storage.

{{% alert title="Note" color="note" %}}

The following code examples assume that you have a robot configured with a `Navigation` service, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code Sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Mode

{{% alert title="Note" color="note" %}}

The `manual` mode is experimental and will have no effect.

{{% /alert %}}

Get the `Mode` the service is operating in.
There are two options for modes: `manual` and `waypoint`.
If you set the mode to `waypoint`, the service starts looking for added waypoints, effectively beginning navigation.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Mode)](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Mode): The `Mode` the service is operating in.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav")

// Get the Mode the service is operating in
mode, err := myNav.Mode(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### SetMode

{{% alert title="Note" color="note" %}}

The `manual` mode is experimental and will have no effect.

{{% /alert %}}

Set the `Mode` the service is operating in.
There are two options for modes: `manual` and `waypoint`.
If you set the mode to `waypoint`, the service starts looking for added waypoints, effectively beginning navigation.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `mode` [(Mode)](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Mode): The `Mode` for the service to operate in.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav")

// Set the Mode the service is operating in
mode, err := myNav.SetMode(context.Background(), "waypoint", nil)
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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav")

// Get the current location of the robot in the navigation service
location, err := myNav.Location(context.Background(), nil)
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

- [([]Waypoints)](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Waypoint): An array comprised of each `Waypoint` in the service's data storage. These are locations designated within a path for the robot to navigate to.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav")

// Get an array containing each waypoint stored by the navigation service
waypoints, err := myNav.Waypoints(context.Background(), nil)
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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav")

// Create a new waypoint with latitude and longitude values of 0 degrees
location = geo.NewPoint(0, 0)

// Add your waypoint to the service's data storage
err := myNav.AddWaypoint(context.Background(), location, nil)
```

{{% /tab %}}
{{< /tabs >}}

### RemoveWaypoint

Remove a waypoint from the service's data storage.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(primitive.ObjectID)](https://pkg.go.dev/go.mongodb.org/mongo-driver/bson/primitive#ObjectID): The MongoDB ObjectID of the `Waypoint` to remove from the service's data storage.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.49/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav")

// Create a new ObjectID
waypoint_id = primitive.NewObjectID()

// Remove the waypoint matching that ObjectID from the service's data storage
err := myNav.RemoveWaypoint(context.Background(), waypoint_id, nil)
```

{{% /tab %}}
{{< /tabs >}}
