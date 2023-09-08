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
It uses GPS to autonomously navigate a rover [base](/components/base/) to user defined endpoints called `Waypoints`.
Once these waypoints are added and the mode of the service is [set to `MODE_WAYPOINT`](#setmode), the service begins to define the robot's path.

## Configuration

You must configure a [base](/components/base/) with a [movement sensor](/components/movement-sensor/) as part of your robot to configure a Navigation service.

{{% alert title="Important" color="note" %}}

Make sure the [movement sensor](/components/movement-sensor/) you use supports [`GetPosition()`](/components/movement-sensor/#getposition) and at least one of [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading) or [`GetOrientation()`](/components/movement-sensor/#getorientation) in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [Movement Sensor API](/components/movement-sensor/#api).

- It must support `GetPosition()` to report the robot's current GPS location.
- It must also support either `GetCompassHeading()` or `GetOrientation()` to report which way the robot is facing.
- If your movement sensor provides multiple methods, your robot will default to using the values returned by `GetCompassHeading()`.

{{% /alert %}}

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
            "type": "<your-store-type>"
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
            // Remove "config": { ... } below if using "type": "memory"
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
            "z":10
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
| `motion_service` | string | Optional | The `name` of the [motion service](/services/motion/) you have configured for the base you are operating with this service. If you have not added a motion service to your robot, the default motion service will be used. Reference this default service in your code with the name `"builtin"`. |
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

``` python
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

- [(*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The current location of the robot in the navigation service, represented in a `Point` with latitude and longitude values.
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
See the [motion service](/services/motion/) for more information.

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

## Concepts

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

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)
- [imu-wit](/components/movement-sensor/imu/imu-wit/)

An example of a `Compass Heading` reading:

``` go
gps, err := gps.CompassHeading(context.Background, nil)
gps.CompassHeading{25}
```

If you want to read compass headings, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
The movement sensor API's [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading) takes compass heading readings.
Use compass heading readings to determine the *bearing* of your robot, or, the [cardinal direction](https://en.wikipedia.org/wiki/Cardinal_direction) that your robot is facing.

### Orientation

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take orientation measurements:

- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [imu-vectornav](/components/movement-sensor/imu/imu-vectornav/)

An example of an `Orientation` reading:

``` golang
orientation, err := imuwit.Orientation(context.Background, nil)
imu.Orientation{"_type":"quat","i":0,"j":0,"k":0,"r":1}
```

If you want to read orientation, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
The movement sensor API's [`GetOrientation()`](/components/movement-sensor/#getorientation) takes orientation readings.
Additionally, follow [these instructions](/services/frame-system/#configuration) to configure the geometries of each component of your robot within the [frame system](/services/frame-system/).
Use orientation readings to determine the orientation of an object in 3D space as an "orientation vector", or, its position within the [cartesian coordinate system](https://en.wikipedia.org/wiki/Cartesian_coordinate_system) relative to some specific `origin` point that you, the user, need to choose and configure for your robot in Viam's [frame system](/services/frame-system/).

### Angular Velocity

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/components/movement-sensor/) component take angular velocity measurements:

- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [imu-vectornav](/components/movement-sensor/imu/imu-vectornav/)
- [wheeled-odometry](/components/movement-sensor/wheeled-odometry/)
- [gyro-mpu6050](/components/movement-sensor/mpu6050/)

An example of an `AngularVelocity` reading:

``` go
ang_vel, err := imu.AngularVelocity{context.Background, nil}
imu.AngularVelocity{"_type":"angular_velocity","x":0,"y":0,"z":1}
```

If you want to get an angular velocity reading, first [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
The movement sensor API's [`GetAngularVelocity()`](/components/movement-sensor/#getangularvelocity) takes angular velocity readings.
Use angular velocity readings to determine the speed and direction at which your robot is rotating.

### Position

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/components/movement-sensor/) component take position measurements:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

An example of a `Position` reading:

``` go
position, err := imu.Position{context.Background, nil}
gps.Position{"_type":"geopoint","lat":40.7,"lng":-73.98}
```

If you want to get a position, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
The movement sensor API's [`GetPosition()`](/components/movement-sensor/#getposition) takes position readings.
The suggested components allow you to get the *absolute* position of components through their Positions readings for use in the [motion service](/services/motion/) and [navigation service](/services/navigation/).
Use position readings to determine the GPS coordinates of an object in 3D space or its position in the geographic coordinate system [(GCS)](https://en.wikipedia.org/wiki/Geographic_coordinate_system).

### Linear Velocity

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take linear velocity measurements:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)
- [wheeled-odometry](/components/movement-sensor/wheeled-odometry/) (provides a relative estimate only based on where the base component has started)

An example of a `Linear Velocity` reading:

``` go
linear_velocity, err := imu.LinearVelocity{context.Background, nil}
accel.LinearVelocity{"_type":"vector3","x":0,"y":5.4,"z":0}
```

If you want to get linear velocity, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
The movement sensor API's [`GetLinearVelocity()`](/components/movement-sensor/#getlinearvelocity) takes linear velocity readings.
Use linear velocity readings to determine the speed at which your robot is moving through space.
Use [linear acceleration](/services/navigation/#linear-acceleration) readings from another movement sensor to determine the rate of change of this speed.

### Linear Acceleration

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) take linear acceleration measurements:

- [accel-adxl345](/components/movement-sensor/adxl345/)
- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [imu-vectornav](/components/movement-sensor/imu/imu-vectornav/)
- [gyro-mpu6050](/components/movement-sensor/mpu6050/)

An example of a `Linear Acceleration` reading:

``` go
linear_acceleration, err := imu.LinearAcceleration{context.Background, nil}
accel.LinearAcceleration{"_type":"vector3","x":2.2,"y":4.5,"z":2}
```

If you want to get linear acceleration, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
The movement sensor API's [`GetLinearAcceleration()`](/components/movement-sensor/#getlinearacceleration) takes linear acceleration readings.
Use linear acceleration readings to determine the rate of change of the [linear velocity](/services/navigation/#linear-velocity) of your robot, or, the speed at which your robot is moving through space.
