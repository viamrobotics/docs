---
title: "Navigate with a Rover Base"
linkTitle: "Navigate with a Rover"
type: "docs"
description: "Introduction to using a rover base."
image: "/tutorials/navigate-with-rover-base/leo-in-office.png"
imageAlt: "The leo rover navigating in the Viam Lab."
images: ["/tutorials/navigate-with-rover-base/leo-in-office.png"]
tags: ["try viam", "navigation", "movement sensor"]
authors: ["Sierra Guequierre"]
languages: ["python", "go"]
viamresources: ["navigation", "camera"]
level: "Intermediate"
date: "2023-02-08"
# updated: ""
cost: "0"
no_list: true
weight: 4
# SMEs: Ray Bjorkman, Fahmina
---

One key feature of Viam is [Navigation](/manage/data/), the stateful definition of Viam's [motion service](/services/motion/).

Using Navigation, you can queue up user-defined waypoints and expect your robot to move to them in the order that you specify.
You may also add obstacles or set linear and angular velocity targets in your navigation service config.
If you do so, our motion planner will plan routes that avoid those obstacles and attempt to keep the robot at your specified velocity.
Gone are the days of managing complicated integrations because Viam provides an end to end navigation stack that is easy to use.

To try it out yourself, you need a mobile base and a movement sensor that can track the robot's GPS coordinates, angular, and linear velocity.
Follow this tutorial to get started using Viam's Navigation service to help your wheeled base navigate across space.

## Requirements

1. **A wheeled base with encoded motors**

    We used [a LEO rover](https://www.leorover.tech/shop?gclid=CjwKCAjw38SoBhB6EiwA8EQVLiDwUFEYgLxaRd1-TiTyLfifIAHs9iD6YnvdW6M-3rXruHOrzfTL2RoCD1AQAvD_BwE), configured as a [`wheeled` base](/components/base/wheeled/), but you can use whatever model of rover base you have on hand.

2. **A camera**

    We used an [Intel RealSense Camera](https://www.intelrealsense.com/depth-camera-d435/) configured as an `viam:camera:realsense` modular [camera](/components/camera/).

3. **A movement sensor**

    We used a [SparkFun GPS-RTK-SMA Breakout](https://www.sparkfun.com/products/16481) [movement sensor](/components/movement-sensor/) configured as a [`gps-nmea-rtk-serial`](/components/movement-sensor/gps/gps-nmea-rtk-serial/) model to provide GPS position measurements, along with a [`wheeled-odometry`](/components/movement-sensor/wheeled-odometry/) model gathering angular and linear velocity information from the encoders, and a [`merged`](/components/movement-sensor/merged/) model aggregating the readings together for the navigation service to consume.d

{{% alert title="Tip" color="tip" %}}

If you are using different hardware than us, the navigation setup process will be mostly the same, but you will need to substitute your robot's components.

{{% /alert %}}

Before you start, make sure to create a robot in [the Viam app](https://app.viam.com) and [install `viam-server`](/installation/) on your robot.

## Configure the components you need

First, configure the components of your robot.
If you are using different *models* of hardware, adjust your configuration accordingly.

### Configure a board with `"digital_interrupts"`

First, configure the [board](/components/board/) local to your rover.
Follow [these instructions](/components/board/#configuration) to configure your board model.
We used a [`jetson` board](/components/board/jetson/), but you can use whatever model of board you have on hand, as the [board API](/components/board/#api) is hardware agnostic.

Configure a board named `local` as shown below:

![Configuration of a jetson board with digital interrupts in the Viam app config builder.](/tutorials/navigate-with-rover-base/board-config-builder.png)

Copy and paste the following into your board's **Attributes** to add [digital interrupts](/components/board/#digital_interrupts) on pins `31`, `29`, `23`, and `21`:

``` json {class="line-numbers linkable-line-numbers"}
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

Save your config.

### Configure a rover base with encoded motors

Now, configure your rover base to act as the moving platform of the navigating robot.
Start by configuring the [encoders](/components/encoder/) and [motors](/components/motor/) of your encoded motor.

Follow [these instructions](/components/) to configure the left and right encoders of the wheeled base.
We configured ours as `incremental` encoders, as shown below:

{{<imgproc src="/tutorials/navigate-with-rover-base/right-encoder-config-builder.png" resize="400x" declaredimensions=true alt="Configuration of a right incremental encoder in the Viam app config builder." class="aligncenter" style="min-height:300px; max-height:350px">}}

{{<imgproc src="/tutorials/navigate-with-rover-base/left-encoder-config-builder.png" resize="400x" declaredimensions=true alt="Configuration of a left incremental encoder in the Viam app config builder." class="aligncenter" style="min-height:300px; max-height:350px">}}

Follow [these instructions](/components/motor/#configuration) to configure the left and right [motors](/components/motor/) of the `wheeled` base.
We [configured ours as `gpio` motors](/components/motor/gpio/), as shown below:

![Configuration of a right gpio motor in the Viam app config builder.](/tutorials/navigate-with-rover-base/right-motor-config-builder.png)

![Configuration of a left gpio motor in the Viam app config builder.](/tutorials/navigate-with-rover-base/left-motor-config-builder.png)

Wire the board to the camera, encoders, and motors on your base matching this configuration.

Now, configure whatever rover you have as a `wheeled` model of base, bringing the motion produced by these motors together on one platform:

![An example configuration for a wheeled base in the Viam app Config Builder.](/tutorials/navigate-with-rover-base/wheeled-base-config-builder.png)

Make sure to select each of your right and left motors as **Right Motors** and **Left Motors** and enter in the wheel circumference and width of each of the wheels the motors are attached to.
Refer to [the `wheeled` base configuration instructions](/components/base/base/) for more attribute information.

### Configure a depth camera

Next, configure a [camera](/components/camera) that your robot can sense how far away it is from obstacles.

We configured ours as an Intel RealSense camera, which is available as a [modular resource](/extend/modular-resources/) [in the Viam registry](https://app.viam.com/module/viam/realsense):

![An example configuration for an Intel RealSense camera in the Viam app Config Builder.](/tutorials/navigate-with-rover-base/realsense-camera-config-builder.png)

### Configure movement sensors

Next, configure a GPS movement sensor so the robot knows where it is while navigating.

We configured ours as a `gps-nmea-rtk-serial` movement sensor:

![An example configuration for a GPS movement sensor in the Viam app Config Builder.](/tutorials/navigate-with-rover-base/gps-movement-sensor-config-builder.png)

Refer to [the `gps-nmea-rtk-serial` movement sensor configuration instructions](/components/movement-sensor/gps/gps-nmea-rtk-serial/) for attribute information.

We also configured a `wheeled-odometry` motor, which uses the encoders from our position reporting motors to get an odometry estimate of a wheeled base as it moves:

![An example configuration for a wheeled-odometry movement sensor in the Viam app Config Builder.](/tutorials/navigate-with-rover-base/wheeled-odometry-movement-sensor-config-builder.png)

Refer to [the `wheeled-odometry` movement sensor configuration instructions](/components/movement-sensor/wheeled-odometry/) for attribute information.

Lastly, we configured a `merged` movement sensor to aggregate the readings from our two movement sensors into a singular sensor:

![An example configuration for a merged movement sensor in the Viam app Config Builder.](/tutorials/navigate-with-rover-base/merged-movement-sensor-config-builder.png)

Refer to [the `merged` movement sensor configuration instructions](/components/movement-sensor/merged/) for attribute information.

<!-- TODO: add frame system configuration instructions for each component and vision service information? -->

### Full JSON Configuration

Now, at this point, if you switch to **Raw JSON** mode in your robot's **Config** tab, the full `"components"` and `"modules"` array should look similar to the following:

{{%expand "Click to view full example JSON" %}}

``` json {class="line-numbers linkable-line-numbers"}
"components": [
    {
      "depends_on": [],
      "model": "jetson",
      "name": "local",
      "type": "board",
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
      "type": "base"
    },
    {
      "name": "gps",
      "type": "movement_sensor",
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
      "model": "gpio",
      "name": "left-motor",
      "type": "motor",
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
      "type": "motor",
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
      "depends_on": [],
      "model": "viam:camera:realsense",
      "name": "myRealSense",
      "namespace": "rdk",
      "type": "camera",
      "attributes": {
        "width_px": 640,
        "height_px": 480,
        "little_endian_depth": false,
        "sensors": [
          "depth",
          "color"
        ]
      }
    },
    {
      "name": "merged",
      "type": "movement_sensor",
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
          "enc-linear"
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
      "attributes": {
        "board": "local",
        "pins": {
          "b": "lb",
          "a": "la"
        }
      },
      "depends_on": [],
      "name": "l-encoder",
      "type": "encoder",
      "model": "incremental"
    },
    {
      "type": "encoder",
      "model": "incremental",
      "attributes": {
        "board": "local",
        "pins": {
          "b": "rb",
          "a": "ra"
        }
      },
      "depends_on": [],
      "name": "r-encoder"
    },
    {
      "model": "wheeled-odometry",
      "type": "movement_sensor",
      "namespace": "rdk",
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
],
"modules": [
    {
      "version": "0.0.3",
      "module_id": "viam:realsense",
      "name": "intel",
      "type": "registry"
    }
  ]
```

{{% /expand%}}

## Configure the services you need

### Configure the Motion service

First, add the motion service to your robot for motion planning.
To add the motion service to your robot, do the following:

1. On your robot's **Config** page, navigate to the **Services** tab.
2. At the bottom of the page, create a service.
   Choose `Motion` as the type.
3. Then click **Create Service**.
4. Optionally, in **Attributes**, add a path to a file where logs will be saved on your robot's computer like the following:

    ``` json
    {
    "log_file_path": "/home/viam/your_log_file_name.log"
    }
    ```

1. Click **Save Config** at the bottom of the window.

For more detailed information see [the navigation service configuration instructions](/services/navigation/#configuration/).

### Configure the Navigation service

Now, add the navigation service so that your wheeled base can navigate between waypoints and avoid obstacles.
To add the navigation service to your robot, do the following:

1. On your robot's **Config** page, navigate to the **Services** tab.
2. At the bottom of the page, create a service.
   Choose `Navigation` as the type.
3. Then click **Create Service**.
4. Select **Raw JSON** mode. Copy and paste the following into your new service's `"attributes"`:

    ``` json
    {
        "base": "base",
        "movement_sensor": "merged",
        "log_file_path": "/home/viam/your_log_filename.log",
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
5. Click **Save Config** at the bottom of the window.

Your navigation service should now appear with a map like the following:

![Navigation Card](/tutorials/navigate-with-rover-base/navigation-config-builder.png)

For more detailed information see [the navigation service configuration instructions](/services/navigation/#configuration/).

### Full JSON Configuration

Now, at this point, if you switch to **Raw JSON** mode in your robot's **Config** tab, the full `"services"` array should look similar to the following:

{{%expand "Click to view full example JSON" %}}

``` json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "builtin",
    "attributes": {
    "log_file_path": "/home/viam/your_log_filename.log"
    },
    "type": "motion"
  },
  {
    "type": "vision",
    "attributes": {
    "h_max_m": 1,
    "h_min_m": 0,
    "return_pcds": false,
    "with_geometries": false
    },
    "model": "obstacles_depth",
    "name": "myObsDepth"
  },
  {
    "name": "nav",
    "type": "navigation",
    "attributes": {
    "base": "base",
    "movement_sensor": "merged",
    "log_file_path": "/home/viam/your_log_filename.log",
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

{{% /expand%}}

## Start navigating with the Navigation service

Next, add waypoints to your navigation service.
If you want to do this programmatically, use the service's [API method `AddWaypoint()`](/services/navigation/#addwaypoint) like the following:

<!-- TODO: find latitude and longitude from ui, ui way of doing it -->

{{< tabs >}}
{{% tab name="Go" %}}

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Create a new waypoint with latitude and longitude values of 0 degrees
location = geo.NewPoint(0, 0)

// Add your waypoint to the service's data storage
err := myNav.AddWaypoint(context.Background(), location, nil)
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Create a new waypoint with latitude and longitude values of 0 degrees
location = GeoPoint(latitude=0, longitude=0)

# Add your waypoint to the service's data storage
await my_nav.add_waypoint(point=location)
```

{{% /tab %}}
{{< /tabs >}}

Then, to start navigating, set your service to `MODE_WAYPOINT` with the service's [API method `SetMode()`](/services/navigation/#setmode):

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

<!-- TODO: UI For adding waypoints 

Insert fahmina's video of rover going from place to place into here

-->

## Next steps

In this tutorial, you have learned how to use Navigation to navigate across waypoints.

{{< snippet "social.md" >}}
