---
title: "Cartographer Modular Resource"
linkTitle: "Cartographer"
weight: 70
type: "docs"
description: "Configure a Simultaneous Localization And Mapping (SLAM) service with the Cartographer modular resource."
tags: ["slam", "services"]
icon: true
images: ["/services/icons/slam.svg"]
aliases:
  - "/services/slam/run-slam-cartographer/"
  - "/services/slam/cartographer/"
  - "/mobility/slam/cartographer/"
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
# SMEs: John N.
---

[The Cartographer Project](https://github.com/cartographer-project) contains a C++ library that performs dense Simultaneous Localization And Mapping (SLAM).

To use Cartographer with the Viam {{< glossary_tooltip term_id="slam" text="SLAM" >}} service, you can use the [`cartographer`](https://app.viam.com/module/viam/cartographer) {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}.

The source code for this module is available on the [`viam-cartographer` GitHub repository](https://github.com/viamrobotics/viam-cartographer).

{{% alert title="Info" color="info" %}}

Currently, the `cartographer` modular resource supports taking 2D LiDAR and optionally IMU and/or odometry data as input.

Support for taking 3D LiDAR data as input may be added in the future.

{{% /alert %}}

## Using Cartographer

The `cartographer` module supports three modes of operation:

- [Create a new map](#create-a-new-map)
- [Update an existing map](#update-an-existing-map)
- [Pure localization](#localize-only)

### Hardware requirements

{{% alert title="Running cartographer in the cloud" color="info" %}}

Creating and updating SLAM maps with Cartographer is especially CPU-intensive.
If you do not have enough resources locally, you can use the [cloudslam wrapper module](../cloudslam/) to move computation to the cloud.

Running `cartographer` in the cloud incurs cost for Data Management, Cloud Data Upload, and Cloud Data Egress. Currently, you incur no cost for compute.
See Viam's [Pricing](https://www.viam.com/product/pricing) for more information.

{{% /alert %}}

#### RPLidar

- You must have an RPlidar, such as the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3), physically connected to your machine.

  Be sure to position the RPlidar so that it **faces forward in the direction of travel**. For example, if you are using a [Viam Rover](https://www.viam.com/resources/rover) and the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to the Rover so that the **pointed** end of the RPlidar mount housing is facing in the same direction as the webcam.

  Furthermore, ensure that the center of the RPlidar is mounted at the center of your machine's [base](/operate/reference/components/base/).
  In the case of the Viam Rover the center is in the middle between the wheels.

  If you need a **mount plate** for your RPlidar A1 or A3 model, you can 3D print an adapter plate using the following:

  - [RPlidar A1 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA1_adapter.STL)
  - [RPlidar A3 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA3_adapter.STL)

- In addition, you must [add the `rplidar` module to your machine](https://github.com/viamrobotics/rplidar) to support the RPlidar hardware, if you have not done so already.

  {{< alert title="SUPPORT" color="note" >}}

  Currently, the `rplidar` and `cartographer` modules only support the Linux platform.

  {{< /alert >}}

#### Movement sensors (optional)

You can use data from one or more movement sensors on your machine to supplement the required LiDAR data.
If you choose to use movement sensor data for SLAM, you can:

- Add only inertial measurement unit (IMU) data
  - Requires a movement sensor that supports [`AngularVelocity`](/operate/reference/services/navigation/#angular-velocity) and [`LinearAcceleration`](/operate/reference/services/navigation/#linear-acceleration) readings
- Add only odometry data
  - Requires a movement sensor that collects [`Position`](/operate/reference/services/navigation/#position) and [`Orientation`](/operate/reference/services/navigation/#orientation) data (for example, [`wheeled-odometry`](/operate/reference/components/movement-sensor/wheeled-odometry/))
- Add both IMU _and_ odometry data
  - Requires all four of the above kinds of data, merged together using the [`merged` movement sensor model](/operate/reference/components/movement-sensor/merged/)
  - If you choose this option, be sure to configure data capture on the `merged` sensor and not on the individual movement sensors when following the steps below.

### Create a new map

To create a new map, follow the instructions below.

{{< tabs name="Create new map">}}
{{% tab name="Config Builder" %}}

1. Ensure any sensors you wish to use are configured on the machine. See the [Hardware Requirements](#hardware-requirements) above.

2. Set up the `cartographer` module on your machine:

   Navigate to the **CONFIGURE** tab of your machine's page.

   Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
   Select **SLAM**, then select `cartographer`.
   You can also search for "cartographer".

   Click **Add module**, give your service a name of your choice, then click **Create**.

   In the resulting `SLAM` service configuration pane, choose `Create new map` as the **Mapping mode**, then configure the rest of the **Attributes** for that mapping mode:

   - **Camera**: Select the `name` of the camera component that you created when you [added the `rplidar` module to your machine](https://github.com/viamrobotics/rplidar).
     Example: "my-rplidar". Then set the `Data polling rate (Hz)` for retrieving pointclouds from the camera. For RPLidar A1 and A3 we recommend a frequency of 5 Hz.
   - **Movement Sensor (Optional)**: Select the `name` of the movement sensor component that you want to use for SLAM.
     If you are using both an IMU _and_ an odometer, select the `name` of the `merged` movement sensor, _not_ the `name` of either of the individual movement sensors.
     Examples: "my-imu", "MyOdometer," or "merged-ms". Then set the `Data polling rate (Hz)` for retrieving readings from the movement sensor. We recommend a frequency of 20 Hz.
   - **Minimum range (meters)**: Set the minimum range of your `rplidar`.
     See [config params](#config_params) for suggested values for RPLidar A1 and A3.
   - **Maximum range (meters)**: Set the maximum range of your `rplidar`.
     See [config params](#config_params) for suggested values for RPLidar A1 and A3.

   If you would like to tune additional Cartographer parameters, you can the click **{}** button to switch to the advanced view, then edit the `config_params` from there.
   See the [`config_params`](#config_params) section for more information on the other parameters.

   To save your changes, click the **Save** button in the top right corner of the page.

   Check the **LOGS** tab of your machine to make sure your RPlidar has connected and no errors are being raised.

3. (Optional) Configure cartographer to use cloudSLAM:

   On the `SLAM` service configuration pane, click the **{}** button to switch to advanced views and set the `use_cloud_slam` field to **true**. This setting disables local mapping to limit cpu usage in favor of using cloudSLAM.

   In addition, your configured LiDAR camera and movement sensor must have data capture enabled. See the [cloudSLAM](../cloudslam/) documentation for more information on how to configure the feature on your machine and how to use cloudSLAM.

{{% /tab %}}
{{% tab name="JSON Example" %}}

This example JSON configuration:

- adds the `viam:rplidar` and the `viam:cartographer` modules
- configures the `viam:slam:cartographer` service

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.16"
    },
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.45"
    }
  ],
  "services": [
    {
      "attributes": {
        "config_params": {
          "max_range_meters": "25",
          "mode": "2d",
          "min_range_meters": "0.2"
        },
        "camera": {
          "name": "rplidar",
          "data_frequency_hz": "5"
        },
        "enable_mapping": true,
        "use_cloud_slam": false
      },
      "name": "slam",
      "api": "rdk:service:slam",
      "model": "viam:slam:cartographer"
    }
  ],
  "components": [
    {
      "attributes": {},
      "depends_on": [],
      "name": "rplidar",
      "model": "viam:lidar:rplidar",
      "api": "rdk:component:camera"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

For more information about the configuration attributes, see [Attributes](#attributes).

After configuring cartographer the machine should begin mapping automatically. Navigate to the **CONTROL** tab on your machine's page and click on the dropdown menu matching the `name` of the service you created. See our [tips](../#slam-mapping-best-practices) for making good maps. If you want to save your locally built map, you can use the **GetInternalState API** or use the local map uploading feature of the [cloudslam wrapper module](../cloudslam/).

### Update an existing map

To update an existing map with new pointcloud data from a new SLAM session, follow the instructions below.

1. Configure your `cartographer` SLAM service using a map from your location:

   {{< tabs name="Update existing map">}}
   {{% tab name="Config Builder" %}}

   1. Select the Mapping mode dropdown and choose the **Update existing map** option.
   2. Configure **Select map** and **Map version** with the name and version of the map you would like to update.
      For the other attributes, review the information in [Create a new map](#create-a-new-map).
      You can see more details about the available maps from your machine's **Location** page by clicking **View SLAM library**.

   {{% /tab %}}
   {{% tab name="JSON Example" %}}

   This example JSON configuration:

   - adds the `viam:rplidar` and the `viam:cartographer` modules
   - configures the `viam:slam:cartographer` service
   - adds an `viam:lidar:rplidar` camera
   - specifies the `slam_map` to be updated in the `packages`

   <br>

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "modules": [
       {
         "type": "registry",
         "name": "viam_rplidar",
         "module_id": "viam:rplidar",
         "version": "0.1.16"
       },
       {
         "type": "registry",
         "name": "viam_cartographer",
         "module_id": "viam:cartographer",
         "version": "0.3.45"
       }
     ],
     "services": [
       {
         "attributes": {
           "config_params": {
             "max_range_meters": "25",
             "mode": "2d",
             "min_range_meters": "0.2"
           },
           "camera": {
             "name": "rplidar",
             "data_frequency_hz": "5"
           },
           "enable_mapping": true,
           "use_cloud_slam": false,
           "existing_map": "${packages.slam_map.test-map-1}/internalState.pbstream"
         },
         "name": "slam",
         "api": "rdk:service:slam",
         "model": "viam:slam:cartographer"
       }
     ],
     "components": [
       {
         "attributes": {},
         "depends_on": [],
         "name": "rplidar",
         "model": "viam:lidar:rplidar",
         "api": "rdk:component:camera"
       }
     ],
     "packages": [
       {
         "name": "test-map-1",
         "version": "1697208847",
         "package": "d1c224e8-483e-4cc7-980f-76b89d8fb507/test-map-1",
         "type": "slam_map"
       }
     ]
   }
   ```

   {{% /tab %}}
   {{< /tabs >}}

   For more information about the configuration attributes, see [Attributes](#attributes).

   If you want to configure cartographer to use a locally saved map instead, see [Using locally built maps](#using-locally-built-maps).

2. After configuring cartographer the machine should begin mapping automatically. Navigate to the **CONTROL** tab on your machine's page and click on the dropdown menu matching the `name` of the service you created.

See our [tips](../#slam-mapping-best-practices) for making a good map! If you want to save your locally built map, you can use the **GetInternalState API** or use the local map uploading feature of the [cloudslam wrapper module](../cloudslam/)

{{% alert title="Info" color="info" %}}

Cartographer may take several minutes to find your machine's position on the existing map.
In the meantime, your machine will show up at the map's origin (with the `(x,y)` coordinates `(0,0)`).

{{% /alert %}}

### Localize only

In this mode, the `cartographer` module on your machine executes the Cartographer algorithm to find its position on a map. This mode is better when using [motion planning's MoveOnMap](/dev/reference/apis/services/motion/#moveonmap) because the map will not be modified.

1.  Configure your `cartographer` SLAM service:

    {{< tabs name="Localize only">}}
    {{% tab name="Config Builder" %}}

1.  Select the Mapping mode dropdown and choose the **Update existing map** option.
1.  Configure **Select map** and **Map version** with the name and version of the map you would like to localize on.
    For the other attributes, review the information in [Create a new map](#create-a-new-map).
    You can see more details about the available maps from your machine's **Location** page by clicking **View SLAM library**.

    {{% /tab %}}
    {{% tab name="JSON Example" %}}

This example JSON configuration:

- adds the `viam:rplidar` and the `viam:cartographer` modules
- configures the `viam:slam:cartographer` service
- adds an `viam:lidar:rplidar`
- specifies the `slam_map` for localization in the `packages`

<br>

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.16"
    },
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.45"
    }
  ],
  "services": [
    {
      "api": "rdk:service:slam",
      "model": "viam:slam:cartographer",
      "attributes": {
        "config_params": {
          "min_range_meters": "0.2",
          "max_range_meters": "25",
          "mode": "2d"
        },
        "camera": {
          "name": "rplidar",
          "data_frequency_hz": "5"
        },
        "enable_mapping": false,
        "use_cloud_slam": false,
        "existing_map": "${packages.slam_map.test-map-1}/internalState.pbstream"
      },
      "name": "slam"
    }
  ],
  "components": [
    {
      "model": "viam:lidar:rplidar",
      "api": "rdk:component:camera",
      "attributes": {},
      "depends_on": [],
      "name": "rplidar"
    }
  ],
  "packages": [
    {
      "type": "slam_map",
      "name": "test-map-1",
      "version": "1697208847",
      "package": "d1c224e8-483e-4cc7-980f-76b89d8fb507/test-map-1"
    }
  ]
}
```

    {{% /tab %}}
    {{< /tabs >}}

    For more information about the configuration attributes, see [Attributes](#attributes).

    If you want to configure cartographer to use a locally saved map instead, see [Using locally built maps](#using-locally-built-maps).

2. After configuring cartographer on the machine, the map should appear automatically. Navigate to the **CONTROL** tab on your machine's page and click on the dropdown menu matching the `name` of the service you created.

   {{% alert title="Info" color="info" %}}

Cartographer may take several minutes to find your machine's position on the existing map.
In the meantime, your machine will show up at the map's origin (with the `(x,y)` coordinates `(0,0)`).

If you move your machine, it will appear to be moving in a trajectory from the map's origin.

    {{% /alert %}}

### Attributes

<!-- prettier-ignore -->
| Name | Data Type | Required? | Description |
| ---- | --------- | --------- | ----------- |
| `use_cloud_slam` | boolean | **Required** | If `true`, the Cartographer algorithm will disable mapping on the machine. This feature should only be used when trying to use [cloudslam](../cloudslam/). |
| `camera` | obj | **Required** | An object of the form `{ "name": <string>, "data_frequency_hz": <int> }` where `name` is the name of the LiDAR camera component to use as input and `data_frequency_hz` is the rate at which to capture (in "Create new map" or "Update existing map" modes) or poll (in "Localize only" mode) data from that camera component. |
| `movement_sensor` | obj | Optional | An object of the form `{ "name": <string>, "data_frequency_hz": <int> }` where `name` is the name of the IMU movement sensor (that is, a movement sensor that supports the `GetAngularVelocity` and `GetLinearAcceleration` API methods) to use as additional input and `data_frequency_hz` is the rate at which to capture (in "Create new map" or "Update existing map" modes) or poll (in "Localize only" mode) data from that movement sensor component. |
| `enable_mapping` | boolean | Optional | If `true`, Cartographer will build the map in addition to doing localization. <ul> Default: `true` </ul> |
| `existing_map` | string | Optional | The alias of the package containing the existing map to build on (in "Update existing map" mode) or localize on (in "Localize only" mode). Can also point to a locally saved `.pbstream` file. |
| `config_params` |  obj | Optional | Parameters available to fine-tune the `cartographer` algorithm: [read more below](#config_params). |

#### `config_params`

{{< readfile "/static/include/services/cartographer/configparams.md" >}}

### Using locally built maps

You can see details about the available maps from your machine's **Location** page by clicking **View SLAM library**.
If you do not have any maps, and you do not wish to use [cloudslam](../cloudslam/), but you still want to use localizing and updating modes with cartographer, you can take the following steps.

1. Save a `.pbstream` file by using the [GetInternalState or InternalStateFull APIs](../#api) by using one of the SDKs. Note, `InternalStateFull` is currently only implemented in Go.
2. Ensure the `.pbstream` file is located somewhere on the machine, and note the directory path to that file.
3. In your cartographer's config, update the `existing_map` field with the path to the file that was noted in #2.

your config should look something like the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.16"
    },
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.45"
    }
  ],
  "services": [
    {
      "attributes": {
        "config_params": {
          "max_range_meters": "25",
          "mode": "2d",
          "min_range_meters": "0.2"
        },
        "camera": {
          "name": "rplidar",
          "data_frequency_hz": "5"
        },
        "enable_mapping": true,
        "use_cloud_slam": false,
        "existing_map": "/PATH/TO/FILE/<INTERNAL-STATE-NAME>.pbstream"
      },
      "name": "slam",
      "api": "rdk:service:slam",
      "model": "viam:slam:cartographer"
    }
  ],
  "components": [
    {
      "attributes": {},
      "depends_on": [],
      "name": "rplidar",
      "model": "viam:lidar:rplidar",
      "api": "rdk:component:camera"
    }
  ],
  "packages": []
}
```

Now your `cartographer` service should be running using your locally saved map.
