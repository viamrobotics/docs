---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 70
draft: false
type: "docs"
description: "Explanation of the SLAM service, its configuration, its functionality, and its interfaces."
---

## Warning: This is an experimental feature.
Stability is not guaranteed. Breaking changes are likely to occur, and occur often.

## Introduction

SLAM, which stands for Simultaneous Localization and Mapping, is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers. At Viam, we want to offer our users an easy-to-use, intuitive method for interfacing with various cutting edge SLAM algorithms that may be useful in their mission.

## The Viam SLAM Service
The Viam SLAM Service supports the integration of custom SLAM libraries with the Viam RDK via the SLAM Service API. 

As of 11 October 2022, the following SLAM library is integrated:

-   <a href="https://github.com/UZ-SLAMLab/ORB_SLAM3" target="_blank">ORB-SLAM3</a>[^orb]


[^orb]: <a href="https://github.com/UZ-SLAMLab/ORB_SLAM3" target="_blank"> ORB-SLAM3: ht<span></span>tps://github.com/UZ-SLAMLab/ORB_SLAM3</a>


{{% alert title="Note" color="note" %}}  
* Viam creates a timestamp following this format: `2022-10-10T09_28_50.2630`. We append the timestamp to each filename prior to saving images, maps, and *.yaml files. We will be updating the timestamp format to the RFC339 Nano time format (here: `2022-10-10T09:28:50Z26:30`) in the near future.
{{% /alert %}}


## Requirements
Running the SLAM Service with your robot requires the following:
1. A binary running the custom SLAM library stored in your PATH (e.g., `/usr/local/bin`).
2. Changes to the config specifiying which SLAM library is used, including library specific parameters.
3. A data folder as it is pointed to by the config parameter `data_dir`.

All three are explained in the following using ORB-SLAM3 as the application example.

## The SLAM library binary
A binary that is running the custom SLAM library is required and is assumed to be stored in `/usr/local/bin`. Its location in the case of ORB-SLAM3 is defined <a href="https://github.com/viamrobotics/rdk/blob/7d15c61d59ee1f4948d116d605f4f23a199d2fb1/services/slam/slamlibraries.go#L48" target="_blank">here</a>.

You can download and install the ORB-SLAM3 binaries as follows:

* AArch64 (ARM64) (e.g., on an RPI):
    ```bash
    sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
    ```
* x86_64:
    ```bash
    sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
    ```

Make the file executable by running:
```bash
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

## Configuration Overview

To add the SLAM service to your robot, you need to add the _name_, _type_, and SLAM library specific _attributes_ to the configuration of your robot.

The following is an example configuration for running ORB-SLAM3 in live `rgbd` mode on your robot, provided that it has two [camera streams](https://docs.viam.com/components/camera/#camera-models) available: `"color"` for RGB images, and `"depth"` for depth data. 

``` json
"services": [
  {
    "name": "testorb",
    "type": "slam",
    "attributes": {
      "algorithm": "orbslamv3",
      "data_dir": "<path_to_your_data_folder>",
      "sensors": ["color", "depth"],
      "map_rate_sec": 60,
      "data_rate_ms": 200,
      "config_params": {
        "mode": "rgbd"
      }
    }
  }
]
```

Assuming that there is already sensor data in `data_dir/data`, SLAM can also be run in offline mode. Here is an example configuration:

``` json
"services": [
  {
    "name": "testorb",
    "type": "slam",
    "attributes": {
      "algorithm": "orbslamv3",
      "data_dir": "<path_to_your_data_folder>",
      "sensors": [],
      "map_rate_sec": 120,
      "data_rate_ms": 100,
      "config_params": {
        "mode": "mono"
      }
    }
  }
]
```

### SLAM Modes Overview
The combination of configuration parameters and existing data in the `data_dir` define the behavior of the running SLAM Service. The following table provides an overview over the different SLAM modes, and how they can be set.


**Live vs. Offline Mode**

| Mode | Description |
| ---- | ----------- |
| Live | SLAM runs in live mode if one or more `sensors` are provided. Live mode means that SLAM grabs the most recent sensor readings (e.g., images) from the `sensors` and uses those to perform SLAM. |
| Offline | SLAM runs in offline mode if `sensors: []` is empty. This means it will look for and process images that are already saved in the `data_dir/data` directory. |


**Pure Mapping, Pure Localization, and Update Mode**

| Mode | Description |
| ---- | ----------- |
| PURE MAPPING | In the PURE MAPPING MODE, a new map is generated from scratch. This mode is triggered if no map is found in the `data_dir/data` directory. |
| UPDATING | In UPDATING MODE, an existing map is being changed and updated with new data. This mode is triggered when a map is found in the `data_dir/map` directory and `map_rate_sec` is set greater than or equal to `0`. Note: Setting `map_rate_sec` to a value of `0` causes the system to reset it to its default value of `60`.|

**SLAM library specific sensor `mode`**

Every integrated SLAM library requires `mode` to be specified under its config parameters, which defines which sensor types or combinations are used. You can find more information on the `mode` in the description of the integrated library:

* [Integrated Library: ORB-SLAM3](#integrated-library-orb-slam3)


### General Config Parameters
**Required Attributes**

| Name | Data Type | Description |
| ---- | --------- | ----------- |
| `algorithm` | string | Name of the SLAM library to be used. Currently (10 Oct 2022) supported option: `orbslamv3`. |
| `data_dir` | string | This is the data directory used for saving input sensor/map data and output maps/visualizations. It has an architecture consisting of three internal folders, config, data and map. If this directory structure is not present, the SLAM service creates it. |
| `sensors` | string[] | Names of sensors whose data is input to SLAM. If sensors are provided, SLAM runs in live mode. If the array is empty, SLAM runs in offline mode. |

**Optional Attributes**

| Name | Data Type | Description |
| ---- | --------- | ----------- |
| `map_rate_sec` | int | [optional] Map generation rate for saving current state (in seconds). The default value is `60`. Note: Setting `map_rate_sec` to a value of `0` causes the system to reset it to its default value of `60`.|
| `data_rate_ms` | int |  [optional] Data generation rate for collecting sensor data to be fed into SLAM (in milliseconds). The default value is `200`. |
| `port` | string |  [optional] Port for SLAM gRPC server. If running locally, this should be in the form "localhost:<PORT>". If no value is given a random available port will be assigned. |
| `config_params` |  map[string] string | Parameters specific to the used SLAM library. |


### SLAM Library Specific Config Parameters

The `config_params` is a catch-all attribute for parameters that are unique to the SLAM library being used. These often deal with the internal algorithms being run and will affect such aspects as submap size, update rate, and details on how to perform feature matching to name a few.

You can find details on which inputs you can include for the available libraries in the following section:
* [Integrated Library: ORB-SLAM3](#integrated-library-orb-slam3)

## The Data Directory

A running SLAM service saves the sensor data it uses and the maps and config files it produces locally on the device in the directory as specified in the config as `data_dir`.

To recap, the directory is required to be structured as follows:

<pre>
.
└──\(The Directory Defined in Config as `data_dir`)
    ├── data
    ├── map
    └── config
</pre>

* `data` contains all the sensor data collected from the sensors listed in `sensors`, saved at `data_rate_ms`.
* `map` contains the generated maps, saved at `map_rate_sec`.
* `config` contains all SLAM library specific config files. 

{{% alert title="Note" color="note" %}}  
If this directory structure is not present, the SLAM service creates it.
{{% /alert %}}

The data in the data directory dictates what type of SLAM will be run: 
* If the `map` subdirectory is empty, the SLAM algorithm generates a new map using all the provided data (PURE MAPPING MODE).
* If a map is found in the `map` subdirectory, it will be used as a priori information for the SLAM run and only data generated after the map was created will be used (UPDATING MODE).

## Integrated Library: ORB-SLAM3

### Introduction

ORB-SLAM3 can perform sparse SLAM using monocular or RGB-D images. This must be specified in the configuration under `config_params` (i.e., `mono` or `rgbd`).

In this example, `mono` is selected with one camera stream named `color`:

``` json
"services": [
  {
    "name": "testorb",
    "type": "slam",
    "attributes": {
      "algorithm": "orbslamv3",
      "data_dir": "<path_to_your_data_folder>",
      "sensors": ["color"],
      "map_rate_sec": 60,
      "data_rate_ms": 200,
      "config_params": {
        "mode": "mono"
      }
    }
  }
]
```

### Configuration Overview
The following table gives an overview over the config parameters for ORB-SLAM3. All except for `mode` are optional, and all except for `mode` and `debug` can be used to fine-tune ORB-SLAM's algorithm.
        
| Parameter Mode | Description - The Type of SLAM to Use | Default value |
| -------------- | ------------------------------------- | ------------------- |
| `mode` | `rgbd` or `mono` | No default |
| `debug` | [optional] `bool` | `false` |
| `orb_n_features` | [optional] ORB parameter. Number of features per image. | 1250 |
| `orb_scale_factor` | [optional] ORB parameter. Scale factor between levels in the scale pyramid. | 1.2 |
| `orb_n_levels` | [optional] ORB parameter. Number of levels in the scale pyramid. |  8 |
| `orb_n_ini_th_fast` | [optional] ORB parameter. Initial FAST threshold. | 20 |
| `orb_n_min_th_fast` | [optional] ORB parameter. Lower threshold if no corners detected. | 7 |
| `stereo_th_depth` | [optional] The number of the stereo baselines we use to classify a point as close or far. Close and far points are treated differently in several parts of the stereo SLAM algorithm. | 40 |
| `depth_map_factor` | [optional] Factor to transform the depth map to real units. | 1000 |
| `stereo_b` | [optional] Stereo baseline in meters. | 0.0745 |
