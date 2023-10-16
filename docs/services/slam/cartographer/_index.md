---
title: "Cartographer Modular Resource"
linkTitle: "Cartographer"
weight: 70
type: "docs"
description: "Configure a SLAM service with the Cartographer modular resource."
tags: ["slam", "services"]
icon: "/services/icons/slam.svg"
aliases:
  - "/services/slam/run-slam-cartographer"
# SMEs: Kat, Jeremy
---

[The Cartographer Project](https://github.com/cartographer-project) contains a C++ library that performs dense SLAM.

Viam provides the `cartographer` [modular resource](/extend/modular-resources/) which adds support for using Cartographer with the Viam [SLAM service](/services/slam/). 

Since creating maps with Cartographer is CPU-intensive, for **creating** or **updating** a map, the `cartographer` modular resource **runs in the cloud**.

For doing **pure localization** on an existing map, the `cartographer` modular resource **runs on your robot**.

{{% alert title="Info" color="info" %}}

See Viam's [Pricing](https://www.viam.com/product/pricing) page to understand the costs associated with running Cartographer in the cloud.

{{% /alert %}}

The `cartographer` {{< glossary_tooltip term_id="module" text="module" >}} is available [from the Viam registry](https://app.viam.com/module/viam/cartographer).
See [Modular resources](/extend/modular-resources/#the-viam-registry) for instructions on using a module from the Viam registry on your robot.

The source code for this module is available on the [`viam-cartographer` GitHub repository](https://github.com/viamrobotics/viam-cartographer).

{{% alert title="Info" color="info" %}}

Cartographer supports taking **2D LiDAR** or **3D LiDAR** data and optionally **inertial measurement unit (IMU)** and/or **odometry** data as input.

However, currently, the `cartographer` modular resource only supports taking **2D LiDAR** and optionally **IMU** data as input. Support for taking **3D LiDAR** and **odometry** data as input may be added in the future.

{{% /alert %}}

## Online mode

In this mode, you use **live** LiDAR and optional IMU data to **create a map**, **update an existing map**, or **do pure localization** on an existing map.

### Requirements

If you haven't already, [install `viam-server`](/installation/) on your robot.

Your robot must have an RPlidar installed to be able to use the `cartographer` module, such as the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3).

In addition, you must [add the `rplidar` module to your robot](/extend/modular-resources/examples/rplidar/) to support the RPlidar hardware, if you have not done so already.

Currently, the `rplidar` and `cartographer` modules support the Linux platform only.

Physically connect the RPlidar to your robot.

If you have a Viam Rover and are mounting an RPlidar to your rover, be sure to position the RPlidar so that it **faces forward in the direction of travel**, facing in the same direction as the included webcam.
For example, if you are using the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to the Rover so that the **pointed** end of the RPlidar mount housing points in the direction of the front of the Rover.

If you need a **mount plate** for your RPlidar A1 or A3 model, you can 3D print an adapter plate using the following:

- [RPlidar A1 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA1_adapter.STL)
- [RPlidar A3 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA3_adapter.STL)

### Configuration

#### Create new map

Because Cartographer's algorithm is CPU-intensive, especially for creating or updating a map, the **`cartographer-module` on your robot acts as a stub** in this mode and the algorithm executes in the cloud.

Your robot's sensor data will be **captured continuously** using Viam's [Data Capture](/services/data/configure-data-capture/) while the robot is running, and the data from when you click "Start session" until you click "End session" will be used to create the map. See [View the map being created](#view-the-map-being-created) for details about starting and stopping a cloud slam session.

Follow the instructions below to set up the `cartographer` module on your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Services** subtab and click **Create service** in the lower-left corner.
1. Select **SLAM**, then select `cartographer`.
   You can also search for "cartographer".
1. Click **Add module**, give your service a name of your choice, then click **Create**.
1. In the resulting `SLAM` service configuration pane, from the `"Mapping mode"` dropdown, choose `"Create new map"`
1. Configure the rest of the **Attributes** as follows:

   - `"Camera"`: Select the `name` of the camera component that you created when you [added the `rplidar` module to your robot](/extend/modular-resources/examples/rplidar/). Example: "my-rplidar"
       - Then set a `"Data capture rate (Hz)"` for it. Example: "5"
   - `"Movement Sensor (Optional)"`: Select the `name` of a movement sensor component that implements the `GetAngularVelocity` and `GetLinearAcceleration` methods of the movement sensor API. Example: "my-imu"
       - Then set a `"Data capture rate (Hz)"` for it. Example: "20"
   - `"Minimum range (meters)"`: Set the minimum range of your `rplidar`. See [config params](#config_params) for suggested values for RPLidar A1 and A3.
   - `"Maximum range (meters)"`: Set the maximum range of your `rplidar`. See [config params](#config_params) for suggested values for RPLidar A1 and A3.

If you would like to tune additional Cartographer parameters, you can expand `"Show additional parameters"`. See the [config_params](#config_params) section for more information on the other parameters.

To save your changes, click **Save config** at the bottom of the page.

Check the **Logs** tab of your robot in the Viam app to make sure your RPlidar has connected and no errors are being raised.

{{%expand "Click to view an example JSON configuration for creating a new map" %}}

See [Attributes](#attributes) for details.

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

{{% /expand%}}

#### Update existing map

This mode is similar to [Create new map](#create-new-map), except it creates a new version of an existing map in the robot's location. (It does not overwrite the old version of the map.)

The configuration is similar to the configuration for [creating a new map](#create-new-map), except you additionally configure the following **Attribute**:

   - `"Select map"`, `"Map version"`: Provide the name and version of the map you would like to update. You can see more details about the available maps from this robot's **Location** page under the **SLAM library** tab.

{{%expand "Click to view an example JSON configuration for updating an existing map" %}}

See [Attributes](#attributes) for details.

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

{{% /expand%}}

#### Localize only

In this mode, the cartographer-module on your robot executes the Cartographer algorithm itself locally.

The configuration is similar to the configuration for [updating an existing map](#update-existing-map), except instead of setting a `Data capture rate (Hz)` on the camera and movement sensor, you set a `Data polling rate (Hz)` on them, since the `cartographer-module` on your robot will poll the live LiDAR and IMU directly at these rates instead of the data being sent to the cloud.

{{%expand "Click to view an example JSON configuration for localizing only" %}}

See [Attributes](#attributes) for details.

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

{{% /expand%}}

#### Attributes

<!-- prettier-ignore -->
| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `use_cloud_slam` | boolean | **Required** | If `true`, the Cartographer algorithm will execute in the cloud rather than locally on your robot. |
| `camera` | obj | **Required** | An object of the form `{ "name": <string>, "data_frequency_hz": <int> }` where `name` is the name of the LiDAR camera component to use as input and `data_frequency_hz` is the rate at which to capture (in "Create new map" or "Update existing map" modes) or poll (in "Localize only" mode) data from that camera component. |
| `movement_sensor` | obj | Optional | An object of the form `{ "name": <string>, "data_frequency_hz": <int> }` where `name` is the name of the IMU movement sensor (that is, a movement sensor that supports the `GetAngularVelocity` and `GetLinearAcceleration` API methods) to use as additional input and `data_frequency_hz` is the rate at which to capture (in "Create new map" or "Update existing map" modes) or poll (in "Localize only" mode) data from that movement sensor component. |
| `enable_mapping` | boolean | Optional | If `true`, Cartographer will build the map in addition to doing localization. <ul> Default: `true` </ul> |
| `existing_map` | string | Optional | The alias of the package containing the existing map to build on (in "Update existing map" mode) or localize on (in "Localize only" mode). |
| `config_params` |  obj | Optional | Parameters available to fine-tune the `cartographer` algorithm: [read more below](#config_params). |

### View the Map

#### "Create new map" mode

Navigate to the **Control** tab on your robot's page and click on the drop-down menu matching the `name` of the service you created.

Enter a name for your new map and click `"Start session"`, then wait for the slam session to finish starting up in the cloud, which **takes about 2 minutes**.

Make sure to either **manually refresh**, or **change the refresh frequency** to something other than `Manual`.

![slam RC card start session](/services/slam/slam-RC-card-start-session.png)

While the slam session is starting, you will see a loading screen.

![slam RC card wait for session to finish starting](/services/slam/slam-RC-card-wait-for-session-to-finish-starting.png)

Once the slam session has finished starting, your first pointcloud will appear.

![slam RC card first pointcloud](/services/slam/slam-RC-card-first-pointcloud.png)

You will be able to see that your cloud slam session is in progress from your **Location** page's **SLAM library** tab.

![offline mapping maps computing table](/services/slam/offline-mapping-maps-computing-table.png)

When you would like to end the slam session, back on the robot's **Control** tab, click `"End session"`. If you do not click `"End session"`, the slam session will automatically be ended after 45 minutes.

Once the session has ended, the map will be saved to your **Location** page's **SLAM library** tab.

![offline mapping available maps](/services/slam/offline-mapping-available-maps.png)

You can click `View map` to view the map in a dynamic pointcloud viewer.

![slam library view map](/services/slam/slam-library-view-map.png)

#### "Update existing map" mode

This is similar to [viewing the map in "create new map" mode](#create-new-map-mode), except it builds on top of an existing map.

{{% alert title="Info" color="info" %}}

Cartographer may take several minutes to find your robot's position on the existing map. In the meantime, your robot will show up at the map's origin (i.e., (x,y) coordinates (0,0)).

You may not want to move your robot until it has localized correctly.

{{% /alert %}}

#### "Localize only" mode

Navigate to the **Control** tab on your robot's page and click on the drop-down menu matching the `name` of the service you created.

Unlike when creating or updating a map, you do not need to start and end a slam session. The pointcloud for the existing map will appear **immediately** and Cartographer will try to find your robot's position on it.

Since the map will not change, nothing new will be added to this robot's location's **SLAM library**.

![slam RC card localize only](/services/slam/slam-RC-card-localize-only.png)

{{% alert title="Info" color="info" %}}

Cartographer may take several minutes to find your robot's position on the existing map. In the meantime, your robot will show up at the map's origin (i.e., (x,y) coordinates (0,0)).

If you move your robot, it will appear to be moving in a trajectory from the map's origin.

{{% /alert %}}

## Offline mode

In this mode, you specify a range of **previously captured** LiDAR and optional IMU data to create a map or update an existing map in the cloud.

### Requirements

You can browse your previously captured data from the **Data** page.
To create a map, you must have already captured LiDAR data in the location in which you would like to create the map.

Example of previously captured LiDAR data (note, you can click on a row to see the `Robot ID` of the robot the component belonged to):

{{<imgproc src="/services/slam/offline-mapping-pointcloud-data.png" resize="1200x" declaredimensions=true alt="UI showing captured point clouds">}}

Example of previously captured IMU data:

{{<imgproc src="/services/slam/offline-mapping-imu-data.png" resize="1200x" declaredimensions=true alt="UI showing captured sensor data">}}

### Configuration

Navigate to the **SLAM library** tab on your location page, and click `"Make new map"` on the top right and specify a map name or click `"Update map"` next to an existing map.

1. Enter the `"Robot name"`, `"Camera name"`, and optionally the `"Movement Sensor name"` of the components whose previously captured data you want to use to create or update a map. If your robot has been deleted, you can alternatively specify the `"robot ID`".
1. Adjust the config parameters as needed. See [config_params](#config_params) for details.
1. Select the timeframe of the data you'd like to use.
1. At the bottom, you can see the total number of PCD files and movement sensor data points that will be processed.
1. Click `"Generate map"`.

{{<imgproc src="/services/slam/offline-mapping-generate-map.png" resize="1200x" declaredimensions=true alt="UI for creating a new map from captured data">}}

### View the Map

Unlike in `Online` mode, you cannot see the map being created while the slam session is in progress, but similar to when creating or updating a map in `Online` mode, you can see that your cloud slam session is in progress from your **Location** page's **SLAM library** tab, and when all the data has been processed (or 45 minutes have passed, whichever occurs first), the map will be saved to your **Location** page's **SLAM library** tab.

## `config_params`

Adjust these parameters to fine-tune the algorithm `cartographer` utilizes in aspects like submap size, mapping update rate, and feature matching details:

<!-- prettier-ignore -->
| Parameter Mode | Description | Inclusion | Default Value | Notes |
| -------------- | ----------- | --------- | ------------- | ----- |
| `mode` | `2d` | **Required** | None | |
| `optimize_every_n_nodes` | How many trajectory nodes are inserted before the global optimization is run. | Optional | `3` | To disable global SLAM and use only local SLAM, set this to `0`. |
| `num_range_data` | Number of measurements in each submap. | Optional | `30` | |
| `missing_data_ray_length_meters` | Replaces the length of ranges that are further than `max_range` with this value. | Optional | `25` | Typically the same as `max_range`. |
| `max_range_meters` | Maximum range of valid measurements. | Optional | `25` | For an RPlidar A3, set this value to `25`. For an RPlidar A1, use `12`. |
| `min_range_meters` | Minimum range of valid measurements. | Optional | `0.2` | For an RPlidar A3, set this value to `0.2`. For RPlidar A1, use `0.15`. |
| `max_submaps_to_keep` | Number of submaps to use and track for localization. | Optional | `3` | Only for [LOCALIZING mode](#slam-mapping-modes). |
| `fresh_submaps_count` | Length of submap history considered when running SLAM in updating mode. | Optional | `3` | Only for [UPDATING mode](#slam-mapping-modes). |
| `min_covered_area_meters_squared` | The minimum overlapping area, in square meters, for an old submap to be considered for deletion. | Optional | `1.0` | Only for [UPDATING mode](#slam-mapping-modes). |
| `min_added_submaps_count` | The minimum number of added submaps before deletion of the old submap is considered. | Optional | `1` | Only for [UPDATING mode](#slam-mapping-modes). |
| `occupied_space_weight` | Emphasis to put on scanned data points between measurements. | Optional | `20.0` | Higher values make it harder to overwrite prior scanned points. Relative to `translation weight` and `rotation weight`. |
| `translation_weight` | Emphasis to put on expected translational change from pose extrapolator data between measurements. | Optional | `10.0` | Higher values make it harder for scan matching to translate prior scans. Relative to `occupied space weight` and `rotation weight`. |
| `rotation_weight` | Emphasis to put on expected rotational change from pose extrapolator data between measurements. | Optional | `1.0` | Higher values make it harder for scan matching to rotate prior scans. Relative to `occupied space weight` and `translation weight`. |

For more information, see the Cartographer [algorithm walkthrough](https://google-cartographer-ros.readthedocs.io/en/latest/algo_walkthrough.html), [tuning overview](https://google-cartographer-ros.readthedocs.io/en/latest/tuning.html), and [config parameter list](https://google-cartographer.readthedocs.io/en/latest/configuration.html).

## SLAM Mapping Best Practices

The best way to improve map quality is by taking extra care when creating the initial map.
While in a slam session, you should:

- turn gently and gradually, completely avoiding sudden quick turns
- make frequent loop closures, arriving back at a previously mapped area so the robot can correct for errors in the map layout
- stay relatively (but not extremely) close to walls
- use a robot that can go smoothly over bumps and transitions between flooring areas
- drive at a moderate speed

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
