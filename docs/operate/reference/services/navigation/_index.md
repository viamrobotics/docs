---
title: "Navigation Service"
linkTitle: "Navigation"
description: "The navigation service uses GPS to autonomously navigate a rover to user-defined waypoints."
type: docs
weight: 50
no_list: true
icon: true
images: ["/services/icons/navigation.svg"]
tags: ["navigation", "services", "base", "rover"]
aliases:
  - "/services/navigation/"
  - "/mobility/navigation/"
no_service: true
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
# SMEs: Raymond
---

The navigation service is the stateful definition of Viam's [motion service](/operate/reference/services/motion/).
It uses GPS to autonomously navigate a rover [base](/operate/reference/components/base/) to user-defined waypoints.

Configure your base with a navigation service, add waypoints, and set the mode of the service to [**Waypoint**](/dev/reference/apis/services/navigation/#setmode) to move your rover along a defined path at your desired motion configuration.

## Requirements

You must configure a [base](/operate/reference/components/base/) with [movement sensors](/operate/reference/components/movement-sensor/) as part of your machine to configure a navigation service.

To use the navigation service, configure a stack of movement sensors that implement the following methods in their {{< glossary_tooltip term_id="model" text="models'" >}} implementations of the [movement sensor API](/dev/reference/apis/components/movement-sensor/#api):

- [`GetPosition()`](/dev/reference/apis/components/movement-sensor/#getposition)
- [`GetCompassHeading()`](/dev/reference/apis/components/movement-sensor/#getcompassheading)
- [`GetProperties()`](/dev/reference/apis/components/movement-sensor/#getproperties)

The base should implement the following:

- [`SetVelocity()`](/dev/reference/apis/components/base/#setvelocity)
- [`GetGeometries()`](/dev/reference/apis/components/base/#getgeometries)
- [`GetProperties()`](/dev/reference/apis/components/base/#getproperties)

See [navigation concepts](#navigation-concepts) for more info on how to implement and use movement sensors taking these measurements.

## Configuration

First, make sure your base is physically assembled and powered on.
Then, configure the service:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `navigation` type.
Enter a name or use the suggested name for your service and click **Create**.

{{<imgproc src="/services/navigation/navigation-ui-config.png" resize="1200x" style="width: 900px" alt="An example configuration for a navigation service.">}}

Edit the attributes as applicable to your machine, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
{
  "name": "your-navigation-service",
  "api": "rdk:service:navigation",
  "model": "rdk:builtin:builtin",
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
  "api": "rdk:service:navigation",
  "model": "rdk:builtin:builtin",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `store` | obj | **Required** | The type and configuration of data storage to use. Either type `"memory"`, where no additional configuration is needed and the waypoints are stored in local memory while the navigation process is running, or `"mongodb"`, where data persists at the specified [MongoDB URI](https://www.mongodb.com/docs/manual/reference/connection-string) of your MongoDB deployment. <br> Default: `"memory"` |
| `base` | string | **Required** | The `name` you have configured for the [base](/operate/reference/components/base/) you are operating with this service. |
| `movement_sensor` | string | **Required** | The `name` of the [movement sensor](/operate/reference/components/movement-sensor/) you have configured for the base you are operating with this service. |
| `motion_service` | string | Optional | The `name` of the [motion service](/operate/reference/services/motion/) you have configured for the base you are operating with this service. If you have not added a motion service to your machine, the default motion service will be used. Reference this default service in your code with the name `"builtin"`. |
| `obstacle_detectors` | array | Optional | An array containing objects with the `name` of each [`"camera"`](/operate/reference/components/camera/) you have configured for the base you are navigating, along with the `name` of the [`"vision_service"`](/operate/reference/services/motion/) you are using to detect obstacles. Note that any vision services on remote parts will only be able to access cameras on the same remote part. |
| `position_polling_frequency_hz` | float | Optional | The frequency in Hz to poll for the position of the machine. <br> Default: `1` |
| `obstacle_polling_frequency_hz` | float | Optional | The frequency in Hz to poll each vision service for new obstacles. <br> Default: `1` |
| `plan_deviation_m` | float | Optional | The distance in meters that a machine is allowed to deviate from the motion plan. <br> Default: `2.6`|
| `degs_per_sec` | float | Optional | The default angular velocity for the [base](/operate/reference/components/base/) in degrees per second. <br> Default: `20` |
| `meters_per_sec` | float | Optional | The default linear velocity for the [base](/operate/reference/components/base/) in meters per second. <br> Default: `0.3` |
| `obstacles` | obj | Optional | Any obstacles you wish to add to the machine's path. See the [motion service](/operate/reference/services/motion/) for more information. |
| `bounding_regions` | obj | Optional | Set of bounds which the robot must remain within while navigating. See the [motion service](/operate/reference/services/motion/) for more information. |

### Configure and calibrate the frame system service for GPS navigation

{{% alert title="Info" color="info" %}}

The [frame system service](/operate/reference/services/frame-system/) is an internally managed and mostly static system for storing the reference frame of each component of a machine within a coordinate system configured by the user.

It stores the required contextual information for Viam's services like [Motion](/operate/reference/services/motion/) and [Vision](/operate/reference/services/vision/) to use the position and orientation readings returned by components like [movement sensors](/operate/reference/components/movement-sensor/).

{{% /alert %}}

To make sure your rover base's autonomous GPS navigation with the navigation service is accurate, configure and calibrate the frame system service for the components of your machine.

#### Configure

Add [reference frames](/operate/reference/services/frame-system/#configuration) to your rover [base](/operate/reference/components/base/) and [movement sensor](/operate/reference/components/movement-sensor/) configurations:

- Navigate to the **CONFIGURE** tab of your machine's page.
- Find your base configuration card and click **+ Add frame**.
- Since you haven't adjusted any parameters yet, the default reference frame will be shown for your base:

  {{<imgproc src="/services/navigation/select-base-frame.png" resize="700x" style="width: 300px" alt="Frame card for a base with the default reference frame settings">}}

- Keep the `parent` frame as `world`.
- Configure a `geometry` for the base that reflects its physical dimensions.
  Measure the physical dimensions of your base and use them to configure the size of your geometry.
  Units are in _mm_.

  For example, you would configure a box-shaped base with dimensions of 100mm x 100mm x 100mm (l x h x w) as follows:

  {{<imgproc src="/services/navigation/configure-base-geometry.png" resize="700x" style="width: 300px" alt="The frame card for the base.">}}

- Add a frame to your movement sensor configuration by clicking **+ Add frame**.
- Set the `parent` within the frame card to the name of your base.
- Give the movement sensor a `translation` that reflects where it is mounted on your base, measuring the coordinates with respect to the origin of the base.
  In other words, designate the base origin as `(0,0,0)` and measure the distance between that and the origin of the sensor to obtain the coordinates.

  For example, you would configure a movement sensor mounted 200mm on top of your base as follows:

  {{<imgproc src="/services/navigation/full-frame-movement-sensor-ui.png" resize="700x" style="width: 300px" alt="The frame card for the movement sensor.">}}

You can also adjust the `orientation` and `geometry` of your movement sensor or base, if necessary.
See [the frame system service](/operate/reference/services/frame-system/) for instructions.

#### Calibrate

Then, to calibrate your frame system for the most accurate autonomous GPS navigation with the navigation service:

- After configuring your machine, navigate to the **CONTROL** tab and select the card matching the name of your movement sensor.
- Monitor the readings displayed on the card, and verify that the compass or orientation readings from the movement sensor report `0` when the base is facing north.
- If you cannot verify this:
  - Navigate back to your machine's **CONFIGURE** tab.
    Scroll to the card with the name of your movement sensor.
    Adjust the `orientation` of the frame to compensate for the mismatch.
  - Navigate back to the movement sensor card on your **CONTROL** page, and confirm that the compass or orientation readings from the movement sensor now report `0` when the base is facing north, confirming that you've successfully calibrated your machine to be oriented accurately within the frame system.
  - If you cannot verify this, repeat as necessary.

## API

The [navigation service API](/dev/reference/apis/services/navigation/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/navigation-table.md" >}}

## Control tab usage

After configuring the navigation service for your machine, navigate to the **CONTROL** tab of the machine's page and expand the card matching the name of your service to use an interface for rover navigation.

Here, you can add waypoints and obstacles and view the position of your rover base on a map:

{{<imgproc src="/services/navigation/navigation-control-card.png" resize="900x" style="width: 700px" alt="An example control interface for a navigation service in the  Control Tab.">}}

## Navigation concepts

The following concepts are important to understand when utilizing the navigation service.
Each concept is a type of relative or absolute measurement, taken by a [movement sensor](/operate/reference/components/movement-sensor/), which can then be used by your machine to navigate across space.

Here's how to use the following types of measurements:

- [Compass Heading](/operate/reference/services/navigation/#compass-heading)
- [Orientation](/operate/reference/services/navigation/#orientation)
- [Angular Velocity](/operate/reference/services/navigation/#angular-velocity)
- [Position](/operate/reference/services/navigation/#position)
- [Linear Acceleration](/operate/reference/services/navigation/#linear-acceleration)
- [Linear Velocity](/operate/reference/services/navigation/#linear-velocity)

### Compass heading

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/operate/reference/components/movement-sensor/) take compass heading measurements:

- [gps-nmea](https://github.com/viam-modules/gps/) - some GPS hardware only report heading while moving.
- [gps-nmea-rtk-pmtk](https://github.com/viam-modules/gps/) - some GPS hardware only report heading while moving.
- [gps-nmea-rtk-serial](https://github.com/viam-modules/gps/) - some GPS hardware only report heading while moving.
- [imu-wit](https://github.com/viam-modules/wit-motion/)
- [imu-wit-hwt905](https://github.com/viam-modules/wit-motion/)

An example of a `CompassHeading` reading:

```go
// heading is a float64 between 0-360
heading, err := gps.CompassHeading(context.Background(), nil)
```

Use compass heading readings to determine the _bearing_ of your machine, or, the [cardinal direction](https://en.wikipedia.org/wiki/Cardinal_direction) that your machine is facing.

To read compass headings, [configure a capable movement sensor](/operate/reference/components/movement-sensor/#configuration) on your machine.
Then use the movement sensor API's [`GetCompassHeading()`](/dev/reference/apis/components/movement-sensor/#getcompassheading) method to get readings from the sensor.

### Orientation

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/operate/reference/components/movement-sensor/) take orientation measurements:

- [imu-wit](https://github.com/viam-modules/wit-motion/)
- [imu-wit-hwt905](https://github.com/viam-modules/wit-motion/)
- [wheeled-odometry](/operate/reference/components/movement-sensor/wheeled-odometry/)

An example of an `Orientation` reading:

```go
// orientation is a OrientationVector struct with OX, OY, OZ denoting the coordinates of the vector and rotation about z-axis, Theta
orientation, err := imuwit.Orientation(context.Background(), nil)
```

Use orientation readings to determine the orientation of an object in 3D space as an [_orientation vector_](/operate/mobility/orientation-vector/).
An orientation vector indicates how it is rotated relative to an origin coordinate system around the x, y, and z axes.
You can choose the origin reference frame by configuring it using Viam's [frame system](/operate/reference/services/frame-system/).
The `GetOrientation` readings will report orientations relative to that initial frame.

To read orientation, first [configure a capable movement sensor](/operate/reference/components/movement-sensor/#configuration) on your machine.
Additionally, follow [these instructions](/operate/reference/services/frame-system/#configuration) to configure the geometries of each component of your machine within the frame system.
Then use the movement sensor API's [`GetOrientation()`](/dev/reference/apis/components/movement-sensor/#getorientation) method to get orientation readings.

### Angular velocity

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/operate/reference/components/movement-sensor/) component take angular velocity measurements:

- [imu-wit](https://github.com/viam-modules/wit-motion/)
- [imu-wit-hwt905](https://github.com/viam-modules/wit-motion/)
- [wheeled-odometry](/operate/reference/components/movement-sensor/wheeled-odometry/)
- [gyro-mpu6050](https://github.com/viam-modules/tdk-invensense/)

An example of an `AngularVelocity` reading:

```go
// angularVelocity is an AngularVelocity r3 Vector with X, Y, and Z magnitudes
angularVelocity, err := imu.AngularVelocity(context.Background(), nil)
```

Use angular velocity readings to determine the speed and direction at which your machine is rotating.

To get an angular velocity reading, first [configure a capable movement sensor](/operate/reference/components/movement-sensor/#configuration) on your machine.
Then use the movement sensor API's [`GetAngularVelocity()`](/dev/reference/apis/components/movement-sensor/#getangularvelocity) method to get angular velocity readings from the sensor.

### Position

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/operate/reference/components/movement-sensor/) component take position measurements:

- [gps-nmea](https://github.com/viam-modules/gps/)
- [gps-nmea-rtk-pmtk](https://github.com/viam-modules/gps/)
- [gps-nmea-rtk-serial](https://github.com/viam-modules/gps/)
- [wheeled-odometry](/operate/reference/components/movement-sensor/wheeled-odometry/)

An example of a `Position` reading:

```go
// position is a geo.Point consisting  of Lat and Long: -73.98 and an altitude in float64
position, altitude, err := imu.Position(context.Background(), nil)
```

Use position readings to determine the GPS coordinates of an object in 3D space or its position in the geographic coordinate system [(GCS)](https://en.wikipedia.org/wiki/Geographic_coordinate_system).
These position readings reflect the _absolute_ position of components.

To get a position, [configure a capable movement sensor](/operate/reference/components/movement-sensor/#configuration) on your machine.
Then use the movement sensor API's [`GetPosition()`](/dev/reference/apis/components/movement-sensor/#getposition) method to get position readings from the sensor.

### Linear velocity

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/operate/reference/components/movement-sensor/) take linear velocity measurements:

- [gps-nmea](https://github.com/viam-modules/gps/)
- [gps-nmea-rtk-pmtk](https://github.com/viam-modules/gps/)
- [gps-nmea-rtk-serial](https://github.com/viam-modules/gps/)
- [wheeled-odometry](/operate/reference/components/movement-sensor/wheeled-odometry/) (provides a relative estimate only based on where the base component has started)

An example of a `LinearVelocity` reading:

```go
// linearVelocity is an r3.Vector with X, Y, and Z magnitudes
linearVelocity, err := imu.LinearVelocity(context.Background(), nil)
```

Use linear velocity readings to determine the speed at which your machine is moving through space.

To get linear velocity, [configure a capable movement sensor](/operate/reference/components/movement-sensor/#configuration) on your machine.
Then use the movement sensor API's [`GetLinearVelocity()`](/dev/reference/apis/components/movement-sensor/#getlinearvelocity) method to get linear velocity readings from the sensor.

### Linear acceleration

The following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/operate/reference/components/movement-sensor/) take linear acceleration measurements:

- [accel-adxl345](https://github.com/viam-modules/analog-devices/)
- [imu-wit](https://github.com/viam-modules/wit-motion/)
- [imu-wit-hwt905](https://github.com/viam-modules/wit-motion/)
- [gyro-mpu6050](https://github.com/viam-modules/tdk-invensense/)

An example of a `LinearAcceleration` reading:

```go
// linearAcceleration is an r3.Vector with X, Y, and Z magnitudes
linearAcceleration, err := imu.LinearAcceleration(context.Background(), nil)
```

You can use linear acceleration readings to determine the rate of change of the [linear velocity](/operate/reference/services/navigation/#linear-velocity) of your machine, or, the acceleration at which your machine is moving through space.

To get linear acceleration, [configure a capable movement sensor](/operate/reference/components/movement-sensor/#configuration) on your machine.
Then use the movement sensor API's [`GetLinearAcceleration()`](/dev/reference/apis/components/movement-sensor/#getlinearacceleration) method to get linear acceleration readings from the sensor.

## Next steps

If you would like to see the navigation service in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
