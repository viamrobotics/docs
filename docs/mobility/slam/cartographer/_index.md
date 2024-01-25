---
title: "Cartographer Modular Resource"
linkTitle: "Cartographer"
weight: 70
type: "docs"
description: "Configure a Simultaneous Localization And Mapping (SLAM) service with the Cartographer modular resource."
tags: ["slam", "services"]
icon: "/services/icons/slam.svg"
aliases:
  - "/services/slam/run-slam-cartographer/"
  - "/services/slam/cartographer/"
# SMEs: Kat, Jeremy
---

[The Cartographer Project](https://github.com/cartographer-project) contains a C++ library that performs dense Simultaneous Localization And Mapping (SLAM).

To use Cartographer with the Viam {{< glossary_tooltip term_id="slam" text="SLAM" >}} service, you can use the [`cartographer`](https://app.viam.com/module/viam/cartographer) {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}.
See the [Use Modules](/registry/#use-modules) section for instructions on using a module from the Viam registry on your machine.

The source code for this module is available on the [`viam-cartographer` GitHub repository](https://github.com/viamrobotics/viam-cartographer).

{{% alert title="Info" color="info" %}}

Cartographer supports taking **2D LiDAR** or **3D LiDAR** data and optionally **Inertial Measurement Unit (IMU)** and/or **odometry** data as input.

However, currently, the `cartographer` modular resource only supports taking **2D LiDAR** and optionally **IMU** data as input.
Support for taking **3D LiDAR** and **odometry** data as input may be added in the future.

{{% /alert %}}

Cartographer can operate:

- _online_ [using a live machine](#use-a-live-machine) for creating and updating maps or for localization
- _offline_ [using previously captured data](#use-previously-captured-data) for creating and updating maps

## Use a live machine

The `cartographer` module supports three modes of operation:

- [Create a new map](#create-a-new-map)
- [Update an existing map](#update-an-existing-map)
- [Pure localization](#localize-only)

Creating and updating SLAM maps with Cartographer is especially CPU-intensive, so the `cartographer` modular resource runs in the cloud for these two tasks.
For doing pure localization on an existing map, the `cartographer` modular resource runs locally on your machine.

{{% alert title="Info" color="info" %}}

Running `cartographer` in the cloud incurs cost for Data Management, Cloud Data Upload, and Cloud Data Egress. Currently, you incur no cost for compute.
See Viam's [Pricing](https://www.viam.com/product/pricing) for more information.

{{% /alert %}}

### Requirements

- You must have an RPlidar, such as the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3), physically connected to your machine.

  Be sure to position the RPlidar so that it **faces forward in the direction of travel**. For example, if you are using a [Viam Rover](https://www.viam.com/resources/rover) and the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to the Rover so that the **pointed** end of the RPlidar mount housing is facing in the same direction as the webcam.

  Furthermore, ensure that the center of the RPlidar is mounted at the center of your machine's [base](/components/base/).
  In the case of the Viam Rover the center is in the middle between the wheels.

  If you need a **mount plate** for your RPlidar A1 or A3 model, you can 3D print an adapter plate using the following:

  - [RPlidar A1 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA1_adapter.STL)
  - [RPlidar A3 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA3_adapter.STL)

- In addition, you must [add the `rplidar` module to your machine](https://github.com/viamrobotics/rplidar) to support the RPlidar hardware, if you have not done so already.

  {{< alert title="SUPPORT" color="note" >}}

  Currently, the `rplidar` and `cartographer` modules only support the Linux platform.

  {{< /alert >}}

### Create a new map

To create a new map, follow the instructions below.
Creating a new map uses an instance of the cartographer module running in the cloud.

1. Enable data capture and configure your `cartographer` SLAM service

   Follow the steps below to enable data capture and add the `cartographer` module to your machine:

   {{< tabs name="Create new map">}}
   {{% tab name="Config Builder" %}}

   Add the data management service:

   1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
   2. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
      Choose `Data Management` as the type and specify a name for your data management service, for example `Data-Management-Service`.
   3. Click **Create**.
   4. On the panel that appears, you can manage the capturing and syncing functions. You can also specify the **directory**, the sync **interval**, and any **tags** to apply to captured data. See the [data management service](/data/) for more information.

   Enable data capture for your camera, and for your movement sensor if you would like to use a movement sensor to provide IMU input:

   5. Find the component's card on your machine's **CONFIGURE** tab.
   6. Click `Add Method`, the specify the method type and the capture frequency. For the camera, choose the [`NextPointCloud`](/components/camera/#getpointcloud) method. For a movement sensor, choose the [`AngularVelocity`](/components/movement-sensor/#getangularvelocity) and [`LinearAcceleration`](/components/movement-sensor/#getlinearacceleration) methods.
      We recommend a capture frequency of `5` Hz for RPlidar cameras and `20` Hz for movement sensors.

   {{< alert title="Tip" color="tip" >}}
   Note that [Data Capture](/data/capture/) continuously monitors and captures your machine’s sensor data while the machine is running. To avoid incurring charges while not in use, [turn off data capture for your sensors](/data/capture/) once you have finished your SLAM session.
   {{< /alert >}}

   Set up the `cartographer` module on your machine:

   7. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
   8. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
   9. Select **SLAM**, then select `cartographer`.
      You can also search for "cartographer".
   10. Click **Add module**, give your service a name of your choice, then click **Create**.
   11. In the resulting `SLAM` service configuration pane, choose `Create new map` as the **Mapping mode**, then configure the rest of the **Attributes** for that mapping mode:

   - **Camera**: Select the `name` of the camera component that you created when you [added the `rplidar` module to your machine](https://github.com/viamrobotics/rplidar).
     Example: "my-rplidar"
   - **Movement Sensor (Optional)**: Select the `name` of a movement sensor component that implements the `GetAngularVelocity` and `GetLinearAcceleration` methods of the movement sensor API.
     Example: "my-imu"
   - **Minimum range (meters)**: Set the minimum range of your `rplidar`.
     See [config params](#config_params) for suggested values for RPLidar A1 and A3.
   - **Maximum range (meters)**: Set the maximum range of your `rplidar`.
     See [config params](#config_params) for suggested values for RPLidar A1 and A3.

   If you would like to tune additional Cartographer parameters, you can expand **Show additional parameters**.
   See the [`config_params`](#config_params) section for more information on the other parameters.

   To save your changes, click **Save config** at the bottom of the page.

   Check the **LOGS** tab of your machine in the Viam app to make sure your RPlidar has connected and no errors are being raised.

   {{%/tab %}}
   {{% tab name="JSON Example" %}}

   This example JSON configuration:

   - adds the `viam:rplidar` and the `viam:cartographer` modules
   - configures the `viam:slam:cartographer` service and the [data management service](/data/)
   - adds an `viam:lidar:rplidar` camera with data capture configured

   <br>

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "modules": [
       {
         "type": "registry",
         "name": "viam_rplidar",
         "module_id": "viam:rplidar",
         "version": "0.1.14"
       },
       {
         "type": "registry",
         "name": "viam_cartographer",
         "module_id": "viam:cartographer",
         "version": "0.3.36"
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
           "use_cloud_slam": true
         },
         "name": "slam",
         "type": "slam",
         "namespace": "rdk",
         "model": "viam:slam:cartographer"
       },
       {
         "name": "Data-Management-Service",
         "type": "data_manager",
         "attributes": {
           "tags": [],
           "additional_sync_paths": [],
           "sync_interval_mins": 0.1,
           "capture_dir": ""
         }
       }
     ],
     "components": [
       {
         "namespace": "rdk",
         "attributes": {},
         "depends_on": [],
         "service_configs": [
           {
             "attributes": {
               "capture_methods": [
                 {
                   "disabled": false,
                   "method": "NextPointCloud",
                   "capture_frequency_hz": 5
                 }
               ]
             },
             "type": "data_manager"
           }
         ],
         "name": "rplidar",
         "model": "viam:lidar:rplidar",
         "type": "camera"
       }
     ]
   }
   ```

   {{% /tab %}}
   {{< /tabs >}}

   For more information about the configuration attributes, see [Attributes](#attributes).

2. Start a mapping session

   Navigate to the **Control** tab on your machine's page and click on the dropdown menu matching the `name` of the service you created.
   On the cartographer panel, you can start a mapping session.

   When you start a mapping session, Cartographer uses the data captured from when you click **Start session** until you click **End session** to create the map.

   Enter a name for your new map and click **Start session**.
   Wait for the slam session to finish starting up in the cloud, which **takes about 2 minutes**.

   Make sure to either **manually refresh**, or **change the refresh frequency** to something other than `Manual`.

   ![slam RC card start session](/mobility/slam/slam-RC-card-start-session.png)

   While the slam session is starting, you will see a loading screen.

   ![slam RC card wait for session to finish starting](/mobility/slam/slam-RC-card-wait-for-session-to-finish-starting.png)

   Once the slam session has finished starting, your first pointcloud will appear.

   ![slam RC card first pointcloud](/mobility/slam/slam-RC-card-first-pointcloud.png)

   You can see that your cloud slam session is in progress from your **Location** page's **SLAM library** tab.

   ![offline mapping maps computing table](/mobility/slam/offline-mapping-maps-computing-table.png)

   When you are ready to end the slam session, return to your machine's **Control** tab and click **End session**.
   If you do not click **End session**, the slam session will automatically end after 45 minutes.

   Once the session has ended, the map is saved to your **Location** page's **SLAM library** tab.

   ![offline mapping available maps](/mobility/slam/offline-mapping-available-maps.png)

   You can click `View map` to view the map in a dynamic pointcloud viewer.

   ![slam library view map](/mobility/slam/slam-library-view-map.png)

### Update an existing map

To update an existing map with new pointcloud data from a new SLAM session, follow the instructions below.
Updating an existing map uses an instance of the `cartographer` module running in the cloud, and _does not_ overwrite the existing map.

1. Configure your `cartographer` SLAM service

   {{< tabs name="Update existing map">}}
   {{% tab name="Config Builder" %}}

   Configure **Select map** and **Map version** with the name and version of the map you would like to update.
   For the other attributes, review the information in [Create a new map](#create-a-new-map).
   You can see more details about the available maps from your machine's **Location** page under the **SLAM library** tab.

   {{% /tab %}}
   {{% tab name="JSON Example" %}}

   This example JSON configuration:

   - adds the `viam:rplidar` and the `viam:cartographer` modules
   - configures the `viam:slam:cartographer` service and the [data management service](/data/)
   - adds an `viam:lidar:rplidar` camera with data capture configured
   - specifies the `slam_map` to be updated in the `packages`

   <br>

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "modules": [
       {
         "type": "registry",
         "name": "viam_rplidar",
         "module_id": "viam:rplidar",
         "version": "0.1.14"
       },
       {
         "type": "registry",
         "name": "viam_cartographer",
         "module_id": "viam:cartographer",
         "version": "0.3.36"
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
           "use_cloud_slam": true,
           "existing_map": "${packages.slam_map.test-map-1}/internalState.pbstream"
         },
         "name": "slam",
         "type": "slam",
         "namespace": "rdk",
         "model": "viam:slam:cartographer"
       },
       {
         "name": "Data-Management-Service",
         "type": "data_manager",
         "attributes": {
           "tags": [],
           "additional_sync_paths": [],
           "sync_interval_mins": 0.1,
           "capture_dir": ""
         }
       }
     ],
     "components": [
       {
         "namespace": "rdk",
         "attributes": {},
         "depends_on": [],
         "service_configs": [
           {
             "attributes": {
               "capture_methods": [
                 {
                   "disabled": false,
                   "method": "NextPointCloud",
                   "capture_frequency_hz": 5
                 }
               ]
             },
             "type": "data_manager"
           }
         ],
         "name": "rplidar",
         "model": "viam:lidar:rplidar",
         "type": "camera"
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

2. Start a mapping session

   Navigate to the **Control** tab on your machine's page and click on the dropdown menu matching the `name` of the service you created.
   On the cartographer panel, you can start a mapping session.

   When you start a mapping session, Cartographer uses the data captured from when you click **Start session** until you click **End session** to create the map.

   Once you click **End session**, the map is uploaded to the cloud and visible on your **Location** page under **SLAM library**.

   Click **Start session**.
   Wait for the slam session to finish starting up in the cloud, which **takes about 2 minutes**.

   Once the slam session has started, you can follow the same steps as in [Create a new map](#create-a-new-map) to view your map.

{{% alert title="Info" color="info" %}}

Cartographer may take several minutes to find your machine's position on the existing map.
In the meantime, your machine will show up at the map's origin (with the `(x,y)` coordinates `(0,0)`).

{{% /alert %}}

### Localize only

In this mode, the `cartographer` module on your machine executes the Cartographer algorithm itself locally to find its position on a map.

1.  Configure your `cartographer` SLAM service

    {{< tabs name="Localize only">}}
    {{% tab name="Config Builder" %}}

The configuration is similar to the configuration for [updating an existing map](#update-an-existing-map), except instead of adding a data management service and configuring data capture on the camera and movement sensor, set a `Data polling rate (Hz)` on both.
The `cartographer` module on your machine polls the live LiDAR and IMU directly at these rates, whereas data capture is only used when data is being sent to the cloud.

    {{% /tab %}}
    {{% tab name="JSON Example" %}}

This example JSON configuration:

- adds the `viam:rplidar` and the `viam:cartographer` modules
- configures the `viam:slam:cartographer` service
- adds an `viam:lidar:rplidar` camera with a `Data polling rate (Hz)` of `5`
- specifies the `slam_map` for localization in the `packages`

<br>

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.14"
    },
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.36"
    }
  ],
  "services": [
    {
      "type": "slam",
      "namespace": "rdk",
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
      "type": "camera",
      "namespace": "rdk",
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

1.  Start a mapping session

    Navigate to the **Control** tab on your machine's page and click on the dropdown menu matching the `name` of the service you created.

    Unlike when creating or updating a map, you do not need to start and end a slam session.
    The pointcloud for the existing map will appear **immediately** and Cartographer will try to find your machine's position on it.

    Since the map will not change, nothing new will be added to this machine's location's **SLAM library**.

    ![slam RC card localize only](/mobility/slam/slam-RC-card-localize-only.png)

    {{% alert title="Info" color="info" %}}

Cartographer may take several minutes to find your machine's position on the existing map.
In the meantime, your machine will show up at the map's origin (with the `(x,y)` coordinates `(0,0)`).

If you move your machine, it will appear to be moving in a trajectory from the map's origin.

    {{% /alert %}}

### Attributes

<!-- prettier-ignore -->
| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `use_cloud_slam` | boolean | **Required** | If `true`, the Cartographer algorithm will execute in the cloud rather than locally on your machine. |
| `camera` | obj | **Required** | An object of the form `{ "name": <string>, "data_frequency_hz": <int> }` where `name` is the name of the LiDAR camera component to use as input and `data_frequency_hz` is the rate at which to capture (in "Create new map" or "Update existing map" modes) or poll (in "Localize only" mode) data from that camera component. |
| `movement_sensor` | obj | Optional | An object of the form `{ "name": <string>, "data_frequency_hz": <int> }` where `name` is the name of the IMU movement sensor (that is, a movement sensor that supports the `GetAngularVelocity` and `GetLinearAcceleration` API methods) to use as additional input and `data_frequency_hz` is the rate at which to capture (in "Create new map" or "Update existing map" modes) or poll (in "Localize only" mode) data from that movement sensor component. |
| `enable_mapping` | boolean | Optional | If `true`, Cartographer will build the map in addition to doing localization. <ul> Default: `true` </ul> |
| `existing_map` | string | Optional | The alias of the package containing the existing map to build on (in "Update existing map" mode) or localize on (in "Localize only" mode). |
| `config_params` |  obj | Optional | Parameters available to fine-tune the `cartographer` algorithm: [read more below](#config_params). |

#### `config_params`

{{< readfile "/static/include/services/cartographer/configparams.md" >}}

## Use previously captured data

You can specify a range of **previously captured** LiDAR and optional IMU data to create a map or update an existing map in the cloud.
You can browse your previously captured data from the **Data** page under the **Point clouds** tab (for LiDAR data) and **Sensors** tab (for IMU data).

### Requirements

To create a map, you must have already captured LiDAR data in the location in which you would like to create the map.

The following example shows the previously-captured LiDAR data under the **Point clouds** tab for a machine named `test`.
Selecting a row opens a pane to the right that contains more information, such as the `Machine ID` of the machine the component belongs to:

{{<imgproc src="/mobility/slam/offline-mapping-pointcloud-data.png" resize="1200x" declaredimensions=true alt="UI showing captured point clouds">}}

Example of previously captured IMU data:

{{<imgproc src="/mobility/slam/offline-mapping-imu-data.png" resize="1200x" declaredimensions=true alt="UI showing captured sensor data">}}

### Create or update a map

Navigate to the **SLAM library** tab on your location page, and click **Make new map** on the top right and specify a map name or click **Update map** next to an existing map.

1. Enter the **Machine name**, **Camera name**, and optionally the **Movement Sensor name** of the components whose previously captured data you want to use to create or update a map.
   If your machine has been deleted, you can alternatively specify the **machine ID**.
1. Adjust the configuration parameters as needed.
   See [`config_params`](#config_params) for details.
1. Select the timeframe of the data you'd like to use.
1. At the bottom, you can see the total number of PCD files and movement sensor data points that will be processed.
1. Click **Generate map**.

{{<imgproc src="/mobility/slam/offline-mapping-generate-map.png" resize="1200x" declaredimensions=true alt="UI for creating a new map from captured data">}}

### View the map

Unlike in `Online` mode, you cannot see the map being created while the slam session is in progress, but similar to when creating or updating a map in `Online` mode, you can see that your cloud slam session is in progress from your **Location** page's **SLAM library** tab.
When all the data has been processed (or 45 minutes have passed, whichever occurs first), the map will be saved to your **Location** page's **SLAM library** tab.

### Delete the map

To clear a SLAM map, go to your **Location** page's **SLAM library** tab.
Click on the trash can icon in the upper right-hand corner of a map's card to delete the map.

## SLAM mapping best practices

The best way to improve map quality is by taking extra care when creating the initial map.
While in a slam session, you should:

- turn gently and gradually, completely avoiding sudden quick turns
- make frequent loop closures, arriving back at a previously mapped area so the machine can correct for errors in the map layout
- stay relatively (but not extremely) close to walls
- use a robot that can go smoothly over bumps and transitions between flooring areas
- drive at a moderate speed

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
