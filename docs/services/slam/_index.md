---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 70
draft: false
type: "docs"
description: "Explanation of the SLAM Service, its configuration, and its functionality."
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

{{% alert title="Note" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[Simultaneous Localization And Mapping (SLAM)](../../services/slam/) allows your robot to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.
Viam offers users an easy-to-use, intuitive method for interfacing with various cutting-edge SLAM algorithms.

## Viam SLAM Service

The Viam SLAM Service supports the integration of custom SLAM libraries with the Viam RDK through the SLAM Service API.

The following SLAM libraries are integrated:

- [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3)
- [Cartographer](https://github.com/cartographer-project)

## Requirements

Running the SLAM Service with your robot requires the following:

1. A binary running the custom SLAM library stored in your PATH (like `/usr/local/bin`).
2. Changes to the config specifying which SLAM library is used, including library specific parameters.
3. A data folder as it is pointed to by the config parameter `data_dir`.

All three are explained in the following using ORB-SLAM3 as the application example.

## SLAM Library Binary

Download the ORB-SLAM3 binaries into `usr/local/bin`:

{{< tabs >}}
{{< tab name="AArch64 (ARM64)" >}}

```bash
sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
```

Make the file executable by running:

```bash
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{< /tab >}}
{{% tab name="x86_64" %}}

```bash
sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
```

Make the file executable by running:

```bash
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{% /tab %}}
{{< /tabs >}}

## Configuration Overview

To add the SLAM Service to your robot, you need to add the _name_, _type_, _model_, and SLAM library specific _attributes_ to the configuration of your robot.

The following is an example configuration for running ORB-SLAM3 in live `rgbd` mode on your robot, if it has two camera streams available: `"color"` for RGB images, and `"depth"` for depth data.

``` json
"services": [
  {
    "name": "testorb",
    "model": "orbslamv3",
    "type": "slam",
    "attributes": {
      "data_dir": "<path_to_your_data_folder>",
      "sensors": ["color", "depth"],
      "use_live_data": true,
      "map_rate_sec": 60,
      "data_rate_ms": 200,
      "config_params": {
        "mode": "rgbd"
      }
    }
  }
]
```

Assuming that there is already sensor data in `data_dir/data`, you can also run SLAM in offline mode.
Here is an example configuration:

``` json
"services": [
  {
    "name": "testorb",
    "model": "orbslamv3",
    "type": "slam",
    "attributes": {
      "data_dir": "<path_to_your_data_folder>",
      "sensors": [],
      "use_live_data": false,
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

The combination of configuration parameters and existing data in the `data_dir` define the behavior of the running SLAM Service.
This table provides an overview of the different SLAM modes and how to set them.

#### Live vs Offline Mode

| Mode | Description |
| ---- | ----------- |
| Live | Live mode means that SLAM grabs the most recent sensor readings (like images) from the `sensors` and uses those to perform SLAM. SLAM runs in live mode if `use_live_data: true` and one or more `sensors` are present. If no sensors are provided, an error will be thrown. |
| Offline | SLAM runs in offline mode if `use_live_data: false`. This means it will look for and process images that are already saved in the `data_dir/data` directory. |

#### Pure Mapping, Pure Localization, and Update Mode

| Mode | Description |
| ---- | ----------- |
| PURE MAPPING | In PURE MAPPING mode, a new map is generated from scratch. This mode is triggered if no map is found in the `data_dir/map` directory. |
| UPDATING | In UPDATING mode, an existing map is being changed and updated with new data. This mode is triggered when a map is found in the `data_dir/map` directory and `map_rate_sec` is set greater than `0`.|
| LOCALIZING | In LOCALIZING mode, the map is not changed. Data is used to localize on an existing map. This is similar to updating mode, except the loaded map is not changed. This mode is triggered when a map is found in the `data_dir/map` directory and `map_rate_sec` is equal to `0`. |

#### SLAM Library-Specific Sensor Mode

Every integrated SLAM library requires `mode` to be specified under its config parameters, which defines which sensor types or combinations are used.
You can find more information on the `mode` in the description of the integrated libraries:

- [Integrated Library: ORB-SLAM3](#integrated-library-orb-slam3)
- [Integrated Library: CARTOGRAPHER](run-slam-cartographer)

### General Config Parameters

#### Required Attributes

| Name | Data Type | Description |
| ---- | --------- | ----------- |
| `data_dir` | string | This is the data directory used for saving input sensor/map data and output maps/visualizations. It has an architecture consisting of three internal folders, config, data and map. If this directory structure is not present, the SLAM Service creates it. |
| `sensors` | string[] | Names of sensors whose data is input to SLAM. |
| `use_live_data` |  bool | This specifies whether to run in live mode (true) or offline mode (false). If `use_live_data: true` and `sensors: []`, an error will be thrown. If this parameter is set to true and no sensors are provided, SLAM will produce an error. |

#### Optional Attributes

| Name | Data Type | Description |
| ---- | --------- | ----------- |
| `map_rate_sec` | int | (optional) Map generation rate for saving current state (in seconds). The default value is `60`. Note: Setting `map_rate_sec` to `0` causes SLAM to run in LOCALIZATION mode. |
| `data_rate_ms` | int |  (optional) Data generation rate for collecting sensor data to feed to SLAM (in milliseconds). The default value is `200`. |
| `port` | string |  (optional) Port for SLAM gRPC server. If running locally, this should be in the form "localhost:<PORT>". If no value is specified a random available port is assigned. |
| `delete_processed_data` | bool |  (optional) With `delete_processed_data: true` sensor data is deleted after the SLAM algorithm has processed it. This helps reduce the amount of memory required to run SLAM. If `use_live_data: true`, the `delete_processed_data` defaults to `true` and if `use_live_data: false`, it defaults to false. A `delete_processed_data: true` when `use_live_data: false` is invalid and will result in an error. |
| `config_params` |  map[string] string | Parameters specific to the used SLAM library. |

### SLAM Library Specific Config Parameters

The `config_params` is a catch-all attribute for parameters that are unique to the SLAM library being used.
These often deal with the internal algorithms being run and will affect such aspects as submap size, update rate, and details on how to perform feature matching to name a few.

You can find details on which inputs you can include for the available libraries in the following section:

- [Integrated Library: ORB-SLAM3](#integrated-library-orb-slam3)

## Data Directory

A running SLAM Service saves the sensor data it uses and the maps and config files it produces locally on the device in the directory as specified in the config as `data_dir`.

To recap, the directory must be structured as follows:

<pre>
.
└──\(The Directory Defined in Config as `data_dir`)
    ├── data
    ├── map
    └── config
</pre>

- `data` contains all the sensor data collected from the sensors listed in `sensors`, saved at `data_rate_ms`.
- `map` contains the generated maps, saved at `map_rate_sec`.
- `config` contains all SLAM library specific config files.

{{% alert title="Note" color="note" %}}
If this directory structure is not present, the SLAM Service creates it.
{{% /alert %}}

The data present in the map subdirectory dictates SLAM's mode at runtime:

- If the `map` subdirectory is empty, the SLAM algorithm generates a new map using all the provided data (PURE MAPPING MODE).
- If a map is found in the `map` subdirectory, it will be used as a priori information for the SLAM run and only data generated after the map was created will be used (UPDATING MODE or LOCALIZATION MODE).

## Integrated Library: ORB-SLAM3

### Introduction

ORB-SLAM3 can perform sparse SLAM using monocular or RGB-D images.
You must specify this in the configuration under `config_params` (as `mono` or `rgbd`).

In this example, `mono` is selected with one camera stream named `color`:

``` json
"services": [
  {
    "name": "testorb",
    "model": "orbslamv3",
    "type": "slam",
    "attributes": {
      "data_dir": "<path_to_your_data_folder>",
      "sensors": ["color"],
      "use_live_data": true,
      "delete_processed_data": false,
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

This table is an overview of the config parameters for ORB-SLAM3.
All parameters except for `mode` are optional.
You can use all parameters except for `mode` and `debug` to fine-tune ORB-SLAM's algorithm.

| Parameter Mode | Description - The Type of SLAM to Use | Default Value |
| -------------- | ------------------------------------- | ------------------- |
| `mode` | `rgbd` or `mono` | No default |
| `debug` | (optional) `bool` | `false` |
| `orb_n_features` | (optional) ORB parameter. Number of features per image. | 1250 |
| `orb_scale_factor` | (optional) ORB parameter. Scale factor between levels in the scale pyramid. | 1.2 |
| `orb_n_levels` | (optional) ORB parameter. Number of levels in the scale pyramid. |  8 |
| `orb_n_ini_th_fast` | (optional) ORB parameter. Initial FAST threshold. | 20 |
| `orb_n_min_th_fast` | (optional) ORB parameter. Lower threshold if no corners detected. | 7 |
| `stereo_th_depth` | (optional) Number of stereo baselines used to classify a point as close or far. Close and far points are treated differently in several parts of the stereo SLAM algorithm. | 40 |
| `depth_map_factor` | (optional) Factor to transform the depth map to real units. | 1000 |
| `stereo_b` | (optional) Stereo baseline in meters. | 0.0745 |
