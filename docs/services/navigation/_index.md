---
title: "The Navigation Service"
linkTitle: "Navigation"
description: "The navigation service uses GPS to autonomously navigate a rover to user defined endpoints."
type: docs
weight: 60
no_list: true
icon: "/services/icons/navigation.svg"
images: ["/services/icons/navigation.svg"]
tags: ["navigation", "services", "base", "rover"]
# SMEs: Raymond
---

The Navigation service is the stateful definition of Viam's [motion service](/services/motion/).
It uses GPS to autonomously navigate a rover [base](/components/base/) to user defined endpoints called waypoints.
Configure your base with a navigation service, add waypoints, and set the mode of the service to [**Waypoint**](#setmode) to move your rover along a defined path at your desired motion configuration.

## Requirements

You must configure a [base](/components/base/) with [movement sensors](/components/movement-sensor/) as part of your robot to configure a Navigation service.

To use the navigation service, configure a stack of movement sensors that implement the following methods in their {{< glossary_tooltip term_id="model" text="models'" >}} implementations of the [movement sensor API](/components/movement-sensor/#api):

- [`GetPosition()`](/components/movement-sensor/#getposition)
- [`GetAngularVelocity()`](/components/movement-sensor/#getangularvelocity)
- [`GetLinearVelocity()`](/components/movement-sensor/#getlinearvelocity)
- [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading)

See [navigation concepts](#navigation-concepts) for more info on how to implement and use movement sensors taking these measurements.

## Configuration

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click the **Services** subtab, then click **Create service** in the lower-left corner.
Select the type `Navigation`.
Enter a name for your service, then click **Create**.

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
            "type": "<your-store-type>"
        },
        "movement_sensor": "<your-movement-sensor>",
        "base": "<your-base>",
        "obstacle_detectors": [
          {
          "vision_service": "<your-vision-service>",
          "camera": "<your-camera>"
          }
        ]
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
      // Remove "config": { ... } below if using "type": "memory"
      "config": {
        "uri": "mongodb://127.0.0.1:12345"
      }
    }
  },
  "movement_sensor": "your-movement-sensor",
  "obstacle_detectors": [
    {
      "vision_service": "your-vision-service",
      "camera": "your-camera"
    },
    {
      "vision_service": "your-vision-service-2",
      "camera": "your-camera-2"
    }
  ]
  "base": "your-base",
  "obstacles": [
    {
      "geometries": [
        {
          "label": "your-label-for-this-obstacle",
          "orientation": {
            "type": "ov_degrees",
            "value": {
              "x": 1,
              "y": 0,
              "z": 0,
              "th": 90
            }
          },
          "x": 10,
          "y": 10,
          "z": 10
        }
      ],
      "location": {
        "latitude": 1,
        "longitude": 1
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable.
The following attributes are available for `Navigation` services:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `store` | obj | **Required** | The type and configuration of data storage to use. Either type `"memory"`, where no additional configuration is needed and the waypoints are stored in local memory while the Navigation process is running, or `"mongodb"`, where data persists at the specified [MongoDB URI](https://www.mongodb.com/docs/manual/reference/connection-string) of your MongoDB deployment. <br> Default: `"memory"` |
| `base` | string | **Required** | The `name` you have configured for the [base](/components/base/) you are operating with this service. |
| `movement_sensor` | string | **Required** | The `name` of the [movement sensor](/components/movement-sensor/) you have configured for the base you are operating with this service. |
| `motion_service` | string | Optional | The `name` of the [motion service](/services/motion/) you have configured for the base you are operating with this service. If you have not added a motion service to your robot, the default motion service will be used. Reference this default service in your code with the name `"builtin"`. |
| `obstacle_detectors` | array | Optional | An array containing objects with the `name` of each [`"camera"`](/components/camera/) you have configured for the base you are navigating, along with the `name` of the [`"vision_service"`](/services/motion/) you are using to detect obstacles. Note that any vision services on remote parts will only be able to access cameras on the same remote part. |
| `position_polling_frequency_hz` | float | Optional | The frequency to poll for the position of the robot. <br> Default: `2` |
| `obstacle_polling_frequency_hz` | float | Optional | The frequency in hz to poll each vision service for new obstacles. <br> Default: `2` |
| `plan_deviation_m` | float | Optional | The distance in meters that a robot is allowed to deviate from the motion plan. <br> Default: `3`|
| `degs_per_sec` | float | Optional | The default angular velocity for the [base](/components/base/) in degrees per second. <br> Default: `60` |
| `meters_per_sec` | float | Optional | The default linear velocity for the [base](/components/base/) in meters per second. <br> Default: `0.3` |
| `obstacles` | obj | Optional | Any obstacles you wish to add to the robot's path. See the [motion service](/services/motion/) for more information. |

### Configure and calibrate the frame system service for GPS navigation

{{% alert title="Info" color="info" %}}

The [frame system service](/services/frame-system/) is an internally managed and mostly static system for storing the reference frame of each component of a robot within a coordinate system configured by the user.

It stores the required contextual information for Viam's services like [Motion](/services/motion/) and [Vision](/services/vision/) to use the position and orientation readings returned by components like [movement sensors](/components/movement-sensor/).

{{% /alert %}}

To make sure your rover base's autonomous GPS navigation with the navigation service is accurate, configure and calibrate the frame system service for the components of your robot.
To start, add the frame system service to your rover [base](/components/base/) and [movement sensor](/components/movement-sensor/).

- Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
  Scroll to the card with the name of your base:

  {{< imgproc src="/services/navigation/click-add-frame-ui.png" alt="The button to add a frame selected with the cursor on the Viam app config builder." resize="500x" >}}

- Click **Add Frame**.

  - Keep the `parent` frame as `world`.
    Select the **Geometry** drop-down menu.
  - Configure a **Geometry** for the base that reflects its physical dimensions.
    Reference [these instructions](/services/frame-system/#bounding-geometries) to configure your geometry and measure the physical dimensions of your base.

    ![The frame card for the base in the Viam app config builder.](/services/navigation/full-frame-base-ui.png)

- Scroll to the card with the name of your movement sensor.
  Click **Add Frame** and select the **Parent** box.

  - Type in the `name` of your base to specify this component as the `parent` of the sensor in the reference frame coordinate system, and click **Save Config** to save your configuration.
    See [how to configure nested reference frames](/services/frame-system/nested-frame-config/) for an explanation of this configuration process.
    ![The frame card for the base in the Viam app config builder.](/services/navigation/full-frame-movement-sensor-ui.png)

  - Give the movement sensor a **Translation** that reflects where it is mounted on your base, measuring the coordinates with respect to the origin of the base.

    In other words, designate the origin of the base as `(0,0,0)`, and measure the distance between the origin of the base and the origin of the sensor to obtain the coordinates of the **Translation**.

    See [the frame system service](/services/frame-system/#configuration) for more information, and [the Viam Internals](/internals/orientation-vector/) for a detailed guide on conducting this measurement.

Then, to calibrate your frame system for the most accurate autonomous GPS navigation with the navigation service:

- After configuring your robot, navigate to the **Control** page and select the card matching the name of your movement sensor.
- Monitor the readings displayed on the card, and verify that the compass or orientation readings from the movement sensor report `0` when the base is facing north.
- If you cannot verify this:
  - Navigate back to your robot's **Config** page.
    Scroll to the card with the name of your movement sensor.
    Adjust the **Orientation** of the frame to compensate for the mismatch.
  - Navigate back to the Navigation card on your **Control** page, and confirm that the compass or orientation readings from the movement sensor now report `0` when the base is facing north, confirming that you've successfully calibrated your robot to be oriented accurately within the frame system.
  - If you cannot verify this, repeat as necessary.

## API

The navigation service supports the following methods:

{{< readfile "/static/include/services/apis/navigation.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a `Navigation` service, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code Sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Mode

Get the `Mode` the service is operating in.

There are two options for modes: `MODE_MANUAL` or `MODE_WAYPOINT`.

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

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the Mode the service is operating in
await my_nav.get_mode()
```

{{% /tab %}}
{{< /tabs >}}

### SetMode

Set the `Mode` the service is operating in.

There are two options for modes: `MODE_MANUAL` or `MODE_WAYPOINT`.

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

# Set the Mode the service is operating in to MODE_WAYPOINT and begin
# navigation
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

- [(\*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The current location of the robot in the navigation service, represented in a `Point` with latitude and longitude values.
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_location).

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
- `point` [(\*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The current location of the robot in the navigation service, represented in a `Point` with latitude (lat) and longitude (lng) values.
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

### Obstacles

Get an array of obstacles currently in the service's data storage.
These are locations designated for the robot to avoid when navigating.
See the [motion service](/services/motion/) for more information.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]\*spatialmath.GeoObstacle)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoObstacle): An array comprised of each `GeoObstacle` in the service's data storage.
  These are locations designated for the robot to avoid when navigating.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/navigation#Service).

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Get an array containing each obstacle stored by the navigation service
obstacles, err := myNav.Obstacles(context.Background(), nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[navigation.GeoObstacle])](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.GeoObstacle): A list comprised of each `GeoObstacle` in the service's data storage.
  These are locations designated for the robot to avoid when navigating.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/index.html#viam.services.navigation.NavigationClient.get_obstacles).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each obstacle stored by the navigation service
obstacles = await my_nav.get_obstacles()
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own navigation service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myNav, err := navigation.FromRobot(robot, "my_nav_service")

resp, err := myNav.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await my_nav.do_command(my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.do_command).

{{% /tab %}}
{{< /tabs >}}

## Control Tab Usage

After configuring the navigation service for your robot, navigate to the **Control** tab of the robot's page in the [Viam app](https://app.viam.com) and expand the card matching the name of your service to use an interface for rover navigation.

Here, you can toggle the mode of the service between **Manual** and **Waypoint** to start and stop navigation, add waypoints and obstacles, and view the position of your rover base on a map:

![An example control interface for a Navigation service in the Viam app Control Tab.](/services/navigation/navigation-control-card.png)

## Navigation Concepts

The following concepts are important to understand when utilizing the navigation service.
Each concept is a type of relative or absolute measurement, taken by a [movement sensor](/components/movement-sensor/), which can then be utilized by your robot to navigate across space.

Here's how to make use of the following types of measurements:

- [Compass Heading](/services/navigation/#compass-heading)
- [Orientation](/services/navigation/#orientation)
- [Angular Velocity](/services/navigation/#angular-velocity)
- [Position](/services/navigation/#position)
- [Linear Acceleration](/services/navigation/#linear-acceleration)
- [Linear Velocity](/services/navigation/#linear-velocity)

### Compass Heading

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take compass heading measurements:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/) - some GPS hardware only report heading while moving.
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/) - some GPS hardware only report heading while moving.
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/) - some GPS hardware only report heading while moving.
- [imu-wit](/components/movement-sensor/imu/imu-wit/)

An example of a `Compass Heading` reading:

```go
// heading is a float64 between 0-360
heading, err := gps.CompassHeading(context.Background, nil)
```

Use compass heading readings to determine the _bearing_ of your robot, or, the [cardinal direction](https://en.wikipedia.org/wiki/Cardinal_direction) that your robot is facing.

To read compass headings, [configure a capable movement sensor](/components/movement-sensor/#supported-models) on your robot.
Then use the movement sensor API's [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading) method to get readings from the sensor.

### Orientation

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take orientation measurements:

- [imu-wit](/components/movement-sensor/imu/imu-wit/)

An example of an `Orientation` reading:

```go
// orientation is a OrientationVector struct with OX, OY, OZ denoting the coordinates of the vector and rotation about z-axis, Theta
orientation, err := imuwit.Orientation(context.Background, nil)
```

Use orientation readings to determine the orientation of an object in 3D space as an [_orientation vector_](/internals/orientation-vector/).
An orientation vector indicates how it is rotated relative to an origin coordinate system around the x, y, and z axes.
You can choose the origin reference frame by configuring it using Viam's [frame system](/services/frame-system/).
The `GetOrientation` readings will report orientations relative to that initial frame.

To read orientation, first [configure a capable movement sensor](/components/movement-sensor/#supported-models) on your robot.
Additionally, follow [these instructions](/services/frame-system/#configuration) to configure the geometries of each component of your robot within the [frame system](/services/frame-system/).
Then use the movement sensor API's [`GetOrientation()`](/components/movement-sensor/#getorientation) method to get orientation readings.

### Angular Velocity

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/components/movement-sensor/) component take angular velocity measurements:

- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [wheeled-odometry](/components/movement-sensor/wheeled-odometry/)
- [gyro-mpu6050](/components/movement-sensor/mpu6050/)

An example of an `AngularVelocity` reading:

```go
// angularVelocity is an AngularVelocity r3 Vector with X, Y, and Z magnitudes
angularVelocity, err := imu.AngularVelocity(context.Background, nil)
```

Use angular velocity readings to determine the speed and direction at which your robot is rotating.

To get an angular velocity reading, first [configure a capable movement sensor](/components/movement-sensor/#supported-models) on your robot.
Then use the movement sensor API's [`GetAngularVelocity()`](/components/movement-sensor/#getangularvelocity) method to get angular velocity readings from the sensor.

### Position

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/components/movement-sensor/) component take position measurements:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

An example of a `Position` reading:

```go
// position is a geo.Point consisting  of Lat and Long: -73.98 and an altitude in float64
position, altitude, err:= imu.Position(context.Background, nil)
```

Use position readings to determine the GPS coordinates of an object in 3D space or its position in the geographic coordinate system [(GCS)](https://en.wikipedia.org/wiki/Geographic_coordinate_system).
These position readings reflect the _absolute_ position of components.

To get a position, [configure a capable movement sensor](/components/movement-sensor/#supported-models) on your robot.
Then use the movement sensor API's [`GetPosition()`](/components/movement-sensor/#getposition) method to get position readings from the sensor.

### Linear Velocity

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take linear velocity measurements:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)
- [wheeled-odometry](/components/movement-sensor/wheeled-odometry/) (provides a relative estimate only based on where the base component has started)

An example of a `Linear Velocity` reading:

```go
// linearVelocity is an r3.Vector with X, Y, and Z magnitudes
linearVelocity, err := imu.LinearVelocity(context.Background, nil)
```

Use linear velocity readings to determine the speed at which your robot is moving through space.

To get linear velocity, [configure a capable movement sensor](/components/movement-sensor/#supported-models) on your robot.
Then use the movement sensor API's [`GetLinearVelocity()`](/components/movement-sensor/#getlinearvelocity) method to get linear velocity readings from the sensor.

### Linear Acceleration

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take linear acceleration measurements:

- [accel-adxl345](/components/movement-sensor/adxl345/)
- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [gyro-mpu6050](/components/movement-sensor/mpu6050/)

An example of a `Linear Acceleration` reading:

```go
// linearAcceleration is an r3.Vector with X, Y, and Z magnitudes
linearAcceleration, err := imu.LinearAcceleration(context.Background, nil)
```

You can use linear acceleration readings to determine the rate of change of the [linear velocity](/services/navigation/#linear-velocity) of your robot, or, the acceleration at which your robot is moving through space.

To get linear acceleration, [configure a capable movement sensor](/components/movement-sensor/#supported-models) on your robot.
Then use the movement sensor API's [`GetLinearAcceleration()`](/components/movement-sensor/#getlinearacceleration) method to get linear acceleration readings from the sensor.

## Next steps

If you would like to see the navigation service in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
