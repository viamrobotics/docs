---
title: "Navigate with a Rover Base"
linkTitle: "Navigate with a Rover"
type: "docs"
description: "Introduction to using a rover base with the navigation service."
videos:
  [
    "/tutorials/navigate-with-rover-base/preview.webm",
    "/tutorials/navigate-with-rover-base/preview.mp4",
  ]
videoAlt: "The agilex LIMO rover navigating in the grass outside."
images: ["/tutorials/navigate-with-rover-base/preview.gif"]
tags:
  [
    "try viam",
    "navigation",
    "movement sensor",
    "vision",
    "motion",
    "movement sensor",
    "base",
    "rover",
    "motion planning",
    "obstacles",
    "waypoints",
  ]
authors: ["Sierra Guequierre"]
languages: ["python", "go"]
viamresources: ["navigation", "base", "movement_sensor", "encoder"]
platformarea: ["mobility"]
level: "Intermediate"
date: "2023-02-08"
# updated: ""
cost: "0"
no_list: true
weight: 5
# SMEs: Ray Bjorkman, Fahmina
---

The [navigation service](/operate/reference/services/navigation/) allows you to queue up user-defined waypoints for your machine to move to in the order that you specify.
You can also add obstacles or set linear and angular velocity targets in your navigation service config.
Viam's motion planner will plan routes that avoid those obstacles and attempt to keep the robot at your specified velocity.

{{< alert title="Learning Goals" color="info" >}}

After following this tutorial, you will be able to:

- add waypoints to specify locations you want your machine to move to, both in the app and programmatically
- use the navigation service to move your machine along those waypoints

{{< /alert >}}

To try it out yourself, you need a mobile base and a movement sensor that can track the robot's GPS coordinates and angular and linear velocity.
Follow this tutorial to get started using Viam's Navigation service to help your wheeled base navigate across space with our recommended stack.

{{<video webm_src="https://storage.googleapis.com/docs-blog/tutorials/navigate-with-rover-base/agilex-limo-roving.webm" mp4_src="https://storage.googleapis.com/docs-blog/tutorials/navigate-with-rover-base/agilex-limo-roving.mp4" alt="The agilex rover navigating outside" poster="/tutorials/navigate-with-rover-base/agilex-roving.png">}}

## Requirements

1. **A base**

   We used [a LEO rover](https://www.leorover.tech/shop?gclid=CjwKCAjw38SoBhB6EiwA8EQVLiDwUFEYgLxaRd1-TiTyLfifIAHs9iD6YnvdW6M-3rXruHOrzfTL2RoCD1AQAvD_BwE), configured as a [`wheeled` base](/operate/reference/components/base/wheeled/), but you can use whatever model of rover base you have on hand:

   {{<imgproc src="/tutorials/navigate-with-rover-base/leo-in-office.png" resize="500x" declaredimensions=true alt="Leo rover that is navigating using the navigation service in a robotics lab.">}}

2. **A movement sensor with GPS position, compass heading, and angular and linear velocity readings**

   We used three movement sensors to satisfy these requirements:

   1. A [SparkFun GPS-RTK-SMA Breakout](https://www.sparkfun.com/products/16481) [movement sensor](/operate/reference/components/movement-sensor/) configured as a [`gps-nmea-rtk-serial`](https://app.viam.com/module/viam/gps) model, providing GPS position and compass heading measurements.
   2. A [`wheeled-odometry`](/operate/reference/components/movement-sensor/wheeled-odometry/) model gathering angular and linear velocity information from the [encoders](/operate/reference/components/encoder/) wired to our base's [motors](/operate/reference/components/motor/).
   3. A [`merged`](/operate/reference/components/movement-sensor/merged/) model aggregating the readings together for the navigation service to consume.

   You can use any combo of movement sensors you want as long as you are getting all the types of measurements required.
   See [the navigation service](/operate/reference/services/navigation/#requirements) for more info on movement sensor requirements.

{{% alert title="Tip" color="tip" %}}

If you are using different hardware, the navigation setup process will be mostly the same, but you will need to substitute your robot's components.

{{% /alert %}}

Before you start, make sure to create a machine on [Viam](https://app.viam.com) and [install `viam-server`](/operate/get-started/setup/) on your robot.
Also, make sure to physically connect your components together to your machine's computer and power it on.

## Configure the components you need

First, configure the {{< glossary_tooltip term_id="component" text="components" >}} of your robot.
If you are using different hardware, configure them according to the instructions for the component model that supports your hardware.

{{% expand "Click to see how we configured our LEO rover" %}}

{{< tabs >}}
{{% tab name="Config Builder" %}}

### Configure a board with `"digital_interrupts"`

First, configure the [board](/operate/reference/components/board/) local to your rover.
Follow [these instructions](/operate/reference/components/board/#configuration) to configure your board model.
We used a [`jetson` board](https://github.com/viam-modules/nvidia/tree/main/jetson), but you can use any model of board you have on hand, as the [resource's API](/dev/reference/apis/components/board/#api) is hardware agnostic.

1. Configure a board named `local` as shown below:

{{<imgproc src="/tutorials/navigate-with-rover-base/board-config-builder.png" resize="1200x" declaredimensions=true alt="Configuration of a jetson board with digital interrupts." style="width:650px" class="shadow imgzoom" >}}

2. Configure [digital interrupts](https://github.com/viam-modules/nvidia/blob/main/README.md#digital-interrupt-configuration) on your board to signal precise GPIO state changes to the [encoders](/operate/reference/components/encoder/) on your rover base.
   Find your board on the **CONFIGURE** tab in **Builder** mode.
   Click the **{}** (Switch to advanced) button on the right side of your board's card to switch to JSON attributes editing mode.
   Copy and paste the following JSON into your board's attributes field to add [digital interrupts](https://github.com/viam-modules/nvidia/blob/main/README.md#digital-interrupt-configuration) on pins `31`, `29`, `23`, and `21`:

```json {class="line-numbers linkable-line-numbers"}
{
  "digital_interrupts": [
    {
      "name": "ra",
      "pin": "31"
    },
    {
      "pin": "29",
      "name": "rb"
    },
    {
      "pin": "23",
      "name": "lb"
    },
    {
      "name": "la",
      "pin": "21"
    }
  ]
}
```

3. Save your config.

### Configure a rover base with encoded motors

Configure your rover base to act as the moving platform of the navigating robot.
Start by configuring the [encoders](/operate/reference/components/encoder/) and [motors](/operate/reference/components/motor/) of your encoded motor.

1. Follow the [encoder configuration instructions](/operate/reference/components/encoder/#configuration) to configure the left and right encoders of the wheeled base.
   We configured ours as [`incremental` encoders](/operate/reference/components/encoder/incremental/), as shown below:

   {{<imgproc src="/tutorials/navigate-with-rover-base/right-encoder-config-builder.png" resize="1000x" declaredimensions=true alt="Configuration of a right incremental encoder." class="aligncenter" style="min-height:550px; max-height:600px">}}

   {{<imgproc src="/tutorials/navigate-with-rover-base/left-encoder-config-builder.png" resize="950x" declaredimensions=true alt="Configuration of a left incremental encoder." class="aligncenter" style="min-height:550px; max-height:600px">}}

   Assign the pins as the [digital interrupts](https://github.com/viam-modules/nvidia/blob/main/README.md#digital-interrupt-configuration) you configured for the board, and wire the encoders accordingly to pins {{< glossary_tooltip term_id="pin-number" text="numbered" >}} `31`, `29`, `23`, and `21` on your `local` board.
   Refer to the [`incremental` encoder documentation](/operate/reference/components/encoder/incremental/) for attribute information.

2. Next, follow [these instructions](/operate/reference/components/motor/#configuration) to configure the left and right [motors](/operate/reference/components/motor/) of the `wheeled` base.
   We [configured ours as `gpio` motors](/operate/reference/components/motor/gpio/), as shown below:

{{<imgproc src="/tutorials/navigate-with-rover-base/right-motor-config-builder.png" resize="1500x" declaredimensions=true alt="Configuration of a right gpio motor." style="min-height:550px; max-height:600px">}}

{{<imgproc src="/tutorials/navigate-with-rover-base/left-motor-config-builder.png" resize="1500x" declaredimensions=true alt="Configuration of a left gpio motor." style="min-height:550px; max-height:600px">}}

Wire the motors accordingly to the GPIO pins {{< glossary_tooltip term_id="pin-number" text="numbered" >}} `35`, `35`, `15`, `38`, `40`, and `33` on your `local` board.
Refer to the [`gpio` motor](/operate/reference/components/motor/gpio/) documentation for attribute information.

3. Finally, configure whatever rover you have as a [`wheeled`](/operate/reference/components/base/wheeled/) model of base, bringing the motion produced by these motors together on one platform:
   {{<imgproc src="/tutorials/navigate-with-rover-base/wheeled-base-config-builder.png" resize="800x" declaredimensions=true alt="An example configuration for a wheeled base." style="min-height:550px; max-height:600px">}}

   - Make sure to select each of your right and left motors as **right** and **left**, as well as set the **wheel_circumference_mm** and **width_mm** of each of the wheels the motors are attached to.
   - [Configure the frame system](/operate/reference/services/frame-system/) for this wheeled base so that the navigation service knows where it is in relation to the movement sensor.

     - Switch to **Frame** mode on the **CONFIGURE** tab and select your base.
       If your movement sensor is mounted on top of the rover like ours is, set **Orientation**'s third input field, Z, to `1` and its fourth input field, theta, to `90`.
     - Select the `world` as the parent frame.

       {{<imgproc src="/tutorials/navigate-with-rover-base/wheeled-base-frame-sys.png" resize="500x" declaredimensions=true alt="An example configuration for a wheeled base in the Frame System." style="min-height:200px; max-height:250px">}}

   Refer to the [`wheeled` base configuration instructions](/operate/reference/components/base/wheeled/) for attribute information.

{{< alert title="Tip" color="tip" >}}

Be sure to wire the board to the encoders and motors on your base matching this configuration.
If you choose to wire your components differently, adjust your pin assignment configuration from these instructions according to your wiring.

{{< /alert >}}

{{% /tab %}}
{{% tab name="JSON" %}}

In the **JSON** mode in your machine's **CONFIGURE** tab, add the following JSON objects to the `"components"` array:

```json {class="line-numbers linkable-line-numbers"}
    {
      "depends_on": [],
      "model": "jetson",
      "name": "local",
      "api": "rdk:component:board",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "ra",
            "pin": "31"
          },
          {
            "pin": "29",
            "name": "rb"
          },
          {
            "pin": "23",
            "name": "lb"
          },
          {
            "name": "la",
            "pin": "21"
          }
        ]
      }
    },
    {
      "attributes": {
        "width_mm": 350,
        "left": [
          "left-motor"
        ],
        "right": [
          "right-motor"
        ],
        "wheel_circumference_mm": 400
      },
      "depends_on": [
        "left-motor",
        "right-motor"
      ],
      "frame": {
        "translation": {
          "y": 0,
          "z": 0,
          "x": 0
        },
        "orientation": {
          "value": {
            "y": 0,
            "z": 1,
            "th": 90,
            "x": 0
          },
          "type": "ov_degrees"
        },
        "parent": "world"
      },
      "model": "wheeled",
      "name": "base",
      "api": "rdk:component:base"
    },
    {
      "model": "gpio",
      "name": "left-motor",
      "api": "rdk:component:motor",
      "attributes": {
        "ticks_per_rotation": 420,
        "board": "local",
        "max_rpm": 50,
        "pins": {
          "pwm": "33",
          "a": "38",
          "b": "40"
        },
        "encoder": "l-encoder"
      },
      "depends_on": []
    },
    {
      "model": "gpio",
      "name": "right-motor",
      "api": "rdk:component:motor",
      "attributes": {
        "encoder": "r-encoder",
        "ticks_per_rotation": 425,
        "max_rpm": 50,
        "pins": {
          "a": "35",
          "b": "36",
          "pwm": "15"
        },
        "board": "local"
      },
      "depends_on": []
    },
    {
      "attributes": {
        "board": "local",
        "pins": {
          "b": "lb",
          "a": "la"
        }
      },
      "depends_on": [],
      "name": "l-encoder",
      "api": "rdk:component:encoder",
      "model": "incremental"
    },
    {
      "model": "incremental",
      "api": "rdk:component:encoder",
      "attributes": {
        "board": "local",
        "pins": {
          "b": "rb",
          "a": "ra"
        }
      },
      "depends_on": [],
      "name": "r-encoder"
    }
```

{{% /tab %}}
{{< /tabs >}}

{{% /expand %}}

### Configure movement sensors

{{< tabs >}}
{{% tab name="Config Builder" %}}

1.  Configure a GPS movement sensor so the robot knows where it is while navigating.
    We configured ours as a `gps-nmea-rtk-serial` movement sensor:

    {{<imgproc src="/tutorials/navigate-with-rover-base/gps-movement-sensor-config-builder.png" resize="1100x" declaredimensions=true alt="An example configuration for a GPS movement sensor." style="width:550px" class="shadow imgzoom" >}}

    We named ours `gps`.
    Refer to [the `gps-nmea-rtk-serial` movement sensor documentation](https://github.com/viam-modules/gps/blob/main/README.md#configure-your-rtk-serial-movement_sensor) for attribute information.

2.  Configure a wheeled odometry movement sensor to provide angular and linear velocity measurements from the encoded motors on our base.

    {{<imgproc src="/tutorials/navigate-with-rover-base/wheeled-odometry-movement-sensor-config-builder.png" resize="1100x" declaredimensions=true alt="An example configuration for a wheeled-odometry movement sensor." style="width:550px" class="shadow imgzoom" >}}

    We named ours `enc-linear`.
    Refer to [the `wheeled-odometry` movement sensor documentation](/operate/reference/components/movement-sensor/wheeled-odometry/) for attribute information.

3.  Now that you've got movement sensors which can give you GPS position and linear and angular velocity readings, configure a `merged` movement sensor to aggregate the readings from our other movement sensors into a singular sensor:

    {{<imgproc src="/tutorials/navigate-with-rover-base/merged-movement-sensor-config-builder.png" resize="1100x" declaredimensions=true alt="An example configuration for a merged movement sensor." style="width:550px" class="shadow imgzoom" >}}

    We named ours `merged`.
    Refer to [the `merged` movement sensor documentation](/operate/reference/components/movement-sensor/merged/) for attribute information.

    - Make sure your `merged` movement sensor is configured to gather `"position"` readings from the `gps` movement sensor.
    - [Configure the frame system](/operate/reference/services/frame-system/) for this movement sensor so that the navigation service knows where it is in relation to the base.

      - On the **CONFIGURE** tab, add a frame to your movement sensor configuration by clicking **+ Add Frame**.
        If your movement sensor is mounted on top of the rover like ours is, leave the default frame values.
      - Set the `base` as the `parent` frame.

{{% /tab %}}
{{% tab name="JSON" %}}

In the **JSON** mode in your machine's **CONFIGURE** tab, add the following JSON objects to the `"components"` array:

```json {class="line-numbers linkable-line-numbers"}
    {
      "name": "gps",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "ntrip_password": "yourpassword",
        "ntrip_url": "http://your.url:8082",
        "ntrip_username": "yourusername",
        "serial_baud_rate": 115200,
        "serial_path": "/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00",
        "ntrip_connect_attempts": 10,
        "ntrip_mountpoint": "NJI2"
      },
      "depends_on": [],
      "model": "gps-nmea-rtk-serial"
    },
    {
      "name": "merged",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "angular_velocity": [
          "enc-linear"
        ],
        "compass_heading": [
          "gps"
        ],
        "orientation": [
          "enc-linear"
        ],
        "position": [
          "gps"
        ]
      },
      "depends_on": [],
      "frame": {
        "orientation": {
          "value": {
            "z": 1,
            "th": 0,
            "x": 0,
            "y": 0
          },
          "type": "ov_degrees"
        },
        "parent": "base",
        "translation": {
          "y": 0,
          "z": 0,
          "x": 0
        }
      },
      "model": "merged"
    },
    {
      "model": "wheeled-odometry",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "base": "base",
        "left_motors": [
          "left-motor"
        ],
        "right_motors": [
          "right-motor"
        ]
      },
      "depends_on": [],
      "name": "enc-linear"
    }
```

{{% /tab %}}
{{< /tabs >}}

## Configure a navigation service

{{< tabs >}}
{{% tab name="Config Builder" %}}

Add the navigation service so that your wheeled base can navigate between waypoints and avoid obstacles.
To add the navigation service to your robot, do the following:

1. Navigate to the **CONFIGURE** tab of your machine's page.
1. Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
1. Select the `navigation` type.
1. Enter a name or use the suggested name for your service and click **Create**.
1. Select **JSON** mode.
   Copy and paste the following into your new service's attributes field:

   ```json
   {
     "base": "base",
     "movement_sensor": "merged",
     "obstacles": [],
     "store": {
       "type": "memory"
     },
     "position_polling_frequency": 2,
     "meters_per_sec": 1.2,
     "degs_per_sec": 90,
     "plan_deviation_m": 0.25
   }
   ```

   Edit the attributes as applicable.
   Attribute information is available in [the navigation service documentation](/operate/reference/services/navigation/#configuration).

1. Click **Save** in the top right corner of the screen to save your changes.

Your navigation service should now appear in your machine's **CONFIGURE** tab as a card with a map like the following:

{{<imgproc src="/tutorials/navigate-with-rover-base/navigation-config-builder.png" resize="1200x" declaredimensions=true alt="Navigation Card" style="width:650px" class="shadow imgzoom" >}}

For more detailed information see [the navigation service](/operate/reference/services/navigation/#configuration).

{{% /tab %}}
{{% tab name="JSON" %}}

In **JSON** mode in your machine's **CONFIGURE** tab, add the following JSON object to the `"services"` array:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "nav",
      "api": "rdk:service:navigation",
      "model": "rdk:builtin:builtin",
    "attributes": {
      "base": "base",
      "movement_sensor": "merged",
      "obstacles": [],
      "store": {
        "type": "memory"
      },
      "position_polling_frequency": 2,
      "meters_per_sec": 1.2,
      "degs_per_sec": 90,
      "plan_deviation_m": 0.25
    }
  }
]
```

Click **Save** in the top right corner of the screen to save your changes.

{{% /tab %}}
{{< /tabs >}}

## Start navigating with the navigation service

Now that you have configured your navigation service, add waypoints to your navigation service.
You can add waypoints from the [**CONTROL** tab](#control-tab-method) or [programmatically](#programmatic-method).

### Control tab method

Go to the **CONTROL** tab of your machine, and open the navigation service card.

From there, ensure that **Navigation mode** is selected as **Manual**, so your robot will not begin navigation while you add waypoints.

#### Add waypoints

Select **Waypoints** on the upper-left corner menu of the navigation card.
Zoom in on your current location and click on the map to add a waypoint.

{{<imgproc src="/tutorials/navigate-with-rover-base/add-first-waypoint.png" resize="1200x" declaredimensions=true alt="Waypoint 0 being added on a New York City street" style="width:650px" class="shadow imgzoom" >}}

Add as many waypoints as you desire.
Hover over a waypoint in the left-hand menu and click the trash icon to delete a waypoint.

{{<imgproc src="/tutorials/navigate-with-rover-base/add-second-waypoint.png" resize="1200x" declaredimensions=true alt="Waypoint 1 being added, further down the street" style="width:650px" class="shadow imgzoom" >}}

#### (Optional) Add obstacles

If you want your robot to avoid certain obstacles in its path while navigating, you can also add obstacles.
In the **CONFIGURE** tab, select the **Obstacles** subtab on the navigation card.
Zoom in on your current location, then hold **shift** and drag on the map to draw an obstacle.
Add as many obstacles as you desire.
Hover over an obstacle in the left-hand menu and click the trash icon to delete an obstacle.

#### Begin navigation

Toggle **Navigation mode** to **Waypoint**.
Your rover will begin navigating between waypoints.

{{<video webm_src="https://storage.googleapis.com/docs-blog/tutorials/navigate-with-rover-base/agilex-navigation.webm" mp4_src="https://storage.googleapis.com/docs-blog/tutorials/navigate-with-rover-base/agilex-navigation.mp4" alt="The agilex rover navigating outside" poster="/tutorials/navigate-with-rover-base/agilex-outside.png">}}

### Programmatic method

If you want to do add waypoints programmatically, use the service's [API method `AddWaypoint()`](/dev/reference/apis/services/navigation/#addwaypoint):

#### Add waypoints

{{< tabs >}}
{{% tab name="Go" %}}

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Create a new waypoint at the specified latitude and longitude
location = geo.NewPoint(40.76275, -73.96)

// Add your waypoint to the service's data storage
err := myNav.AddWaypoint(context.Background(), location, nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Create a new waypoint at the specified latitude and longitude
location = GeoPoint(latitude=40.76275, longitude=-73.96)

# Add your waypoint to the service's data storage
await my_nav.add_waypoint(point=location)
```

{{% /tab %}}
{{< /tabs >}}

#### Begin navigation

To start navigating, set your service to `MODE_WAYPOINT` with the service's [API method `SetMode()`](/dev/reference/apis/services/navigation/#setmode):

{{< tabs >}}
{{% tab name="Go" %}}

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Set the Mode the service is operating in to MODE_WAYPOINT and begin navigation
mode, err := myNav.SetMode(context.Background(), Mode.MODE_WAYPOINT, nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Set the Mode the service is operating in to MODE_WAYPOINT and begin
# navigation
await my_nav.set_mode(Mode.ValueType.MODE_WAYPOINT)
```

{{% /tab %}}
{{< /tabs >}}

## Next steps: automate obstacle detection

In this tutorial, you have learned how to use Navigation to navigate across waypoints.
Now, you can make navigation even better with automated obstacle detection.

First, configure a depth [camera](/operate/reference/components/camera/) that your robot can sense how far away it is from obstacles.

We configured ours as an Intel RealSense Camera, which is available as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} in the [registry](https://app.viam.com/module/viam/realsense):

{{<imgproc src="/tutorials/navigate-with-rover-base/realsense-camera-config-builder.png" resize="1200x" declaredimensions=true alt="An example configuration for an Intel RealSense camera." style="width:650px" class="shadow imgzoom" >}}

{{< alert title="Tip" color="tip" >}}

You can alternatively use [`viam:ultrasonic:camera`](https://app.viam.com/module/viam/ultrasonic) from the official viam module.

{{< /alert >}}

If you want the robot to be able to automatically detect obstacles in front of it, [configure a Vision service segmenter](/dev/reference/apis/services/vision/#segmentations).
For example, configure the Vision service model [`obstacles_depth`](https://app.viam.com/module/viam/obstacles-pointcloud) to detect obstacles in front of the robot.
Then, use one of [Viam's client SDKs](/dev/reference/sdks/) to automate obstacle avoidance with the navigation service like in the following Python program:

{{%expand "Click to view full example of automated obstacle avoidance with the Python SDK" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import time
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.base import Base
from viam.services.vision import VisionClient
from viam.proto.common import GeoPoint
from viam.services.navigation import NavigationClient

MANUAL_MODE = 1
DRIVE_MODE = 2
SECONDS_TO_RUN = 60 * 15


async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with your machine's
        # API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address("<MACHINE-ADDRESS>", opts)


async def nav_avoid_obstacles(
    base: Base,
    nav_service: NavigationClient,
    obstacle_detection_service: VisionClient
):
    while True:
        obstacle = await obstacle_detection_service.get_object_point_clouds(
          "myRealSense"
        )
        print("obstacle: ", obstacle)
        z = obstacle[0].geometries.geometries[0].center.z
        print(z)
        r = await nav_service.get_mode()
        if z < 1000:
            if r != MANUAL_MODE:
                await nav_service.set_mode(MANUAL_MODE)
        else:
            if r != DRIVE_MODE:
                await nav_service.set_mode(DRIVE_MODE)


async def main():
    robot = await connect()

    # Get base component and services from the robot
    base = Base.from_robot(robot, "base")
    obstacle_detection_service = VisionClient.from_robot(robot, "myObsDepth")
    nav_service = NavigationClient.from_robot(robot, "nav")

    # Get waypoints and add a new waypoint
    waypoints = await nav_service.get_waypoints()
    assert (len(waypoints) == 0)
    await nav_service.add_waypoint(GeoPoint(latitude=0.00006, longitude=0))

    # Get waypoints again, check to see that one has been added
    waypoints = await nav_service.get_waypoints()
    assert (len(waypoints) == 1)

    # Avoid obstacles
    await nav_avoid_obstacles(base, nav_service, obstacle_detection_service)

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /expand%}}

{{< snippet "social.md" >}}
