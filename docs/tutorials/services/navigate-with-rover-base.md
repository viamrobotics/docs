---
title: "Introduction to the Navigation Service"
linkTitle: "Intro to Navigation"
type: "docs"
description: "Configure data capture and cloud sync, filter and view captured data, and export your data."
# image: "/tutorials/data-management/image1.png"
# imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
# images: ["/services/data-management/image1.png"]
tags: ["try viam", "navigation", "movement sensor"]
authors: []
languages: []
viamresources: [ "navigation", "camera" ]
level: "Intermediate"
date: "2023-02-08"
# updated: ""
cost: "0"
no_list: true
weight: 4
# SMEs: Ray Bjorkman, Fahmina
---

TODO: edit this intro because it's basically just copy-pasted from Nav service intro as-is 

One key feature of Viam is [Navigation](/manage/data/), the stateful definition of Viam's [motion service](/services/motion/).
It uses GPS to autonomously navigate a rover [base](/components/base/) to user defined endpoints called `Waypoints`.
Once these waypoints are added and the mode of the service is [set to `MODE_WAYPOINT`](#setmode), the service begins to define the robot's path.

Follow this tutorial to get started using Viam's Navigation service to help your wheeled base navigate across space.

## Requirements

1. **A wheeled base**

    For this tutorial, we are using an AgileX [LIMO](https://global.agilex.ai/products/limo) rover base, a mobile robot platform from AgileX robotics.
    You can use another model of base if you want, but be sure to [configure](#configure-a-rover-base) your rover base accordingly.

    <!-- 
    
    RECOMMENDATIONS
    
    Hardware Combo 1:
    Base: Agilex Base
    Camera: Intel RealSense Camera
    Movement sensor: “merged” model that depends on GPS RTK & vectornav IMU

    Hardware Combo 2:
    Base: Wheeled Base (scuttle)
    Camera: Ultrasonic Sensor
    Movement sensor: Garmin GP

    HARDWARE COMBO I WANT TO USE 
    Base: Agilex Base
    Camera: Ultrasonic Sensor
    Movement sensor: Garmin GPS  -->

2. **A camera**

    For this tutorial, we are configuring an [ultrasonic sensor](/components/sensor/ultrasonic/) as an `ultrasonic` [camera](/components/camera/).

3. **A movement sensor**

    For this tutorial, we are configuring a [Garmin GPS]() [movement sensor](/components/movement-sensor) as a [`gps-nmea`] model.
    <!-- TODO: is this correct? what model of movement sensor is this anyways? -->

TODO: ADD THESE INSTRUCTIONS HERE:

- Wire your board to your base
- SSH into your board
- Wire the board to your ultrasonic sensor
- Wire the GPS movement sensor

{{% alert title="Tip" color="tip" %}}

If you are using your own robot, be sure that you have [`viam-server` installed](/installation/) on your robot.
The navigation setup process will be mostly the same, but you will need to substitute your robot's components.

{{% /alert %}}

## Configure the components you need

First, configure the components of your robot.
If you are using different *models* of hardware, adjust your configuration accordingly.

### Configure a rover base

First, configure your rover base to act as the moving platform of the navigating robot.
Configure an `agilex-limo` base as follows:

{{< tabs name="Configure an Agilex-Limo Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `agilex-limo` model.
Enter a name for your base and click **Create**.

![An example configuration for a agilex-limo base in the Viam app Config Builder.](/components/base/agilex-limo-ui-config.png)

Copy and paste the following attributes:

```json {class="line-numbers linkable-line-numbers"}
"attributes": {
    "drive_mode": "ackermann",
    "serial_path": "<your-serial-path>"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-base-name>",
      "type": "base",
      "model": "agilex-limo",
      "attributes": {
        "drive_mode": "ackermann",
        "serial_path": "<your-serial-path>"
      },
      "depends_on": []
    }
}
```

{{% /tab %}}
{{< /tabs >}}

Adjust the attributes according to your preferred drive mode and serial path for connection.
Refer to [the `agilex-limo` configuration instructions](/components/base/agilex-limo/) for attribute information.

### Configure an ultrasonic camera

Next, configure the ultrasonic sensor as a camera so that your robot can sense how far away it is from obstacles.

<!-- TODO: configure vision service to detect obstacles? is that needed?

MAKE SURE YOU HAVE INSTRUCTED THEM TO WIRE THE SENSOR BEFOREHAND -->
{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `ultrasonic` model.
Enter a name for your sensor and click **Create**.

![Creation of a ultrasonic sensor in the Viam app config builder.](/components/sensor/ultrasonic-sensor-ui-config.png)

Fill in the attributes as applicable:

Copy and paste the following attributes:

```json {class="line-numbers linkable-line-numbers"}
"attributes": {
    "trigger_pin": "5",
    "echo_interrupt_pin": "15",
    "board": "my-jetson-board"
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "your-ultrasonic-sensor",
      "type": "camera",
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": "5",
        "echo_interrupt_pin": "15",
        "board": "my-jetson-board"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

Refer to [the `ultrasonic` sensor configuration instructions](/components/sensor/ultrasonic/) for attribute information.

### Configure a movement sensor

Next, configure a GPS movement sensor so the robot knows where it is while navigating.

Refer to [the `gps-nmea` movement sensor configuration instructions](/components/movement-sensor/gps-nmea) for attribute information.

<!-- TODO: add frame system configuration instructions for each component and vision service information? -->

## Add the Navigation service

First, you need to add and configure the data management service to capture data and store it at a specified location.
To enable the data capture on your robot, do the following:

1. On your robot's **Config** page, navigate to the **Services** tab.
2. At the bottom of the page, create a service.
   Choose `Navigation` as the type.
3. Then click **Create Service**.
4. Click **Save Config** at the bottom of the window.

![Navigation Card](/tutorials/data-management/data-manager.png)

For more detailed information see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).

## Start navigating with the Navigation service

Next, add waypoints to your navigation service.

<!-- TODO: UI For adding waypoints, and then set to Waypoint mode -->


## Next steps

In this tutorial, you have learned how to use Navigation to navigate across waypoints.

{{< snippet "social.md" >}}
