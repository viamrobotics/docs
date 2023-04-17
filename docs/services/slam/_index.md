---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 70
type: "docs"
description: "Simultaneous Localization And Mapping (SLAM) allows your robot to create a map of its surroundings and find its location within that map."
tags: ["slam", "services"]
icon: "/services/img/icons/slam.svg"
# SMEs: Kat, Jeremy
---

{{% alert title="Note" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your robot to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM Service supports the integration of SLAM as a service on your robot.
The following SLAM libraries are integrated:

- [Cartographer](https://github.com/cartographer-project)
- [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3)

### Requirements

Install the binaries required to utilize these libraries on your machine by running the following commands:

`Cartographer`:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install carto-grpc-server
```

{{% /tab %}}
{{< /tabs >}}

`ORB-SLAM3`:
{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{< /tab >}}
{{% tab name="Linux x86_64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{% /tab %}}
{{< /tabs >}}

## Configuration

You can configure your robot to use SLAM on [the Viam app](https://app.viam.com).
Navigate to the **config** tab on your robot's page, and from there, navigate to the **Services** subtab.

Add a service with type `slam`, whatever name you want, and the model of the library you want to use.

Use [this JSON template](#integrated-library-orb-slam3) to configure the service with the ORB-SLAM3 library, and [this JSON template](#integrated-library-cartographer) to configure the service with the Cartographer library.
Then, adjust general attributes and library-specific `config-params`.

### General Attributes

| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | This is [the data directory](#data_dir-data-directory) used for saving input <file>sensor/map</file> data and output <file>map/</file> visualizations. Must be structured as specified [here](#data_dir-data-directory). |
| `sensors` | string[] | **Required** | Names of configured [camera components](../../components/camera/) providing data to the SLAM service. |
| `use_live_data` | bool | **Required** | <p>This specifies whether to run in Live or Offline mode.</p> <ul> `true`: Live mode. The service grabs the most recent sensor readings and uses those to perform SLAM. If no `sensors` are provided, an error will be thrown. </ul><ul>`false`: Offline mode. The service uses image data stored in the [data directory](#data_dir-data-directory) to perform SLAM.</ul> |
| `map_rate_sec` | int | Optional | Map generation rate for saving current state *(seconds)*. <ul> Default: `60`. </ul> |
| `data_rate_msec` | int | Optional | Data generation rate for collecting sensor data to feed to SLAM *(milliseconds)*. <ul>Default: `200`.</ul> |
| `port` | string | Optional | Port for SLAM gRPC server. If running locally, this should be in the form "localhost:<PORT>". If no value is specified a random available port is assigned. |
| `delete_processed_data` | bool | Optional | <p>Setting this to `true` helps to reduce the amount of memory required to run SLAM.</p> <ul> `true`: sensor data is deleted after the SLAM algorithm has processed it. </ul><ul> `false`: sensor data is not deleted after the SLAM algorithm has processed it. </ul> |
| `config_params` |  map[string] string | Optional | Parameters specific to the `model` of SLAM library. |

{{% alert title="Caution" color="caution" %}}

- If `use_live_data: true`, `delete_processed_data: true` by default.
- If `use_live_data: false`, `delete_processed_data: false` by default.

Setting `delete_processed_data: true` and `use_live_data: false` is invalid and will result in an error.
{{% /alert %}}

### `config_params`

The `config_params` attribute is populated with parameters that are unique to the SLAM library being used.

You can use these parameters to fine-tune the algorithms these libraries utilize in aspects like submap size, mapping update rate, and feature matching details.

To see library-specific `config_params` available, navigate to these sections:

- [Integrated Library: ORB-SLAM3](#orb-slam3-config_params)
- [Integrated Library: Cartographer](#cartographer-config_params)

### `data_dir`: Data Directory

A running SLAM Service saves the sensor data it uses and the maps and config files it produces locally on the device in the directory path specified by the [General Attribute](#general-attributes) `data_dir`.

To recap, the directory must be structured as follows:

<pre>
.
└──\(The Directory Defined in Config as `data_dir`)
    ├── data
    ├── map
    └── config
</pre>

- `data` contains all the sensor data collected from the sensors listed in `sensors`, saved at `data_rate_msec`.
- `map` contains the generated maps, saved at `map_rate_sec`.
- `config` contains all SLAM library specific config files.

{{% alert title="Note" color="note" %}}
If this directory structure is not present, the SLAM Service creates it.
{{% /alert %}}

### Mapping Modes

These modes dictate SLAM's mapping behavior at runtime, but are not configured as a part of the SLAM service's JSON configuration.
The mode utilized by the SLAM service is determined by the information found in the [data directory](#data_dir-data-directory) at runtime.

| Mode | Description | Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | In PURE MAPPING mode, a new map is generated from scratch. | This mode is triggered if no map is found in the `data_dir/map` directory at runtime. |
| UPDATING | In UPDATING mode, an existing map is being changed and updated with new data. | This mode is triggered when a map is found in the `data_dir/map` directory at runtime if the attribute `"map_rate_sec"` is `> 0`.|
| LOCALIZING | In LOCALIZING mode, the map is not changed. Data is used to localize on an existing map. This is similar to UPDATING mode, except the loaded map is not changed. | This mode is triggered when a map is found in the `data_dir/map` directory at runtime if the attribute `"map_rate_sec" = 0`. |

## Integrated Library: Cartographer

Cartographer performs dense SLAM using LIDAR data.

Specify whether this LIDAR data is preloaded or collected live by a Rplidar device with the attribute `use_live_data`.

### Example Configuration

#### Live Mode

To run Cartographer in live mode, follow [these instructions](../../program/extend/modular-resources/add-rplidar-module/) to add your Rplidar device as a modular component of your robot, and refer to this example configuration:

{{< tabs >}}
{{% tab name="Linux" %}}

``` json
{
  "modules": [
    {
      "name": "rplidar_module",
      "executable_path": "/usr/local/bin/rplidar-module"
    }
  ],
  "components": [
    {
      "namespace": "rdk",
      "type": "camera",
      "depends_on": [],
      "model": "viam:lidar:rplidar",
      "name": "rplidar"
    }
  ],
  "services": [
    {
      "type": "slam",
      "attributes": {
        "config_params": {
          "min_range": "0.3",
          "max_range": "12",
          "mode": "2d"
        },
        "data_rate_msec": 200,
        "delete_processed_data": false,
        "use_live_data": true,
        "sensors": [
          "rplidar"
        ],
        "port": "localhost:8083",
        "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
        "map_rate_sec": 60
      },
        "model": "cartographer",
        "name": "run-slam"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="MacOS" %}}

``` json
{
  "modules": [
    {
      "executable_path": "/usr/local/bin/rplidar-module",
      "name": "rplidar_module"
    }
  ],
  "components": [
    {
      "namespace": "rdk",
      "type": "camera",
      "depends_on": [],
      "model": "viam:lidar:rplidar",
      "attributes": {
        "device_path": "/dev/tty.SLAB_USBtoUART"
      },
      "name": "rplidar"
    }
  ],
  "services": [
    {
      "attributes": {
        "map_rate_sec": 60,
        "data_rate_msec": 200,
        "use_live_data": true,
        "sensors": [
          "rplidar"
        ],
        "config_params": {
          "mode": "2d",
          "min_range": "0.3",
          "max_range": "12"
        },
        "port": "localhost:8083",
        "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
        "delete_processed_data": false
      },
      "model": "cartographer",
      "name": "run-slam",
      "type": "slam"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

#### Offline Mode

Refer to this example configuration for running Cartographer SLAM in offline mode:

```json
    {
      "services": [
        {
          "attributes": {
            "config_params": {
              "min_range": "0.3",
              "max_range": "12",
              "mode": "2d"
            },
            "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>/data",
            "map_rate_sec": 60,
            "data_rate_msec": 200,
            "delete_processed_data": false,
            "use_live_data": false,
            "sensors": []
          },
          "model": "cartographer",
          "name": "run-slam-offline",
          "type": "slam"
        }
      ]
    }
```

For more information about running [Cartographer in Offline Mode](run-slam-cartographer#run-cartographer-in-offline-mode-with-a-dataset), see [this tutorial](run-slam-cartographer).

### Cartographer `config_params`

| Parameter Mode | Description | Inclusion | Default Value | Notes |
| -------------- | ----------- | --------- | ------------- | ----- |
| `mode` | `2d` | **Required** | None | |
| `optimize_every_n_nodes` | How many trajectory nodes are inserted before the global optimization is run. | Optional | `3` | |
| `num_range_data` | Number of measurements in each submap. | Optional | `100` | |
| `missing_data_ray_length` | Replaces the length of ranges that are further than max_range with this value. | Optional | `25` | Nominally set to max length. |
| `max_range` | Maximum range of valid measurements. | Optional | `25` | |
| `min_range` | Minimum range of valid measurements. | Optional | `0.2` | |
| `max_submaps_to_keep` | Number of submaps to use and track for localization. | Optional | `3` | Only for LOCALIZING mode. |
| `fresh_submaps_count` | Length of submap history considered when running SLAM in updating mode. | Optional | `3` | Only for UPDATING mode. |
| `min_covered_area` | The minimum overlapping area, in square meters, for an old submap to be considered for deletion. | Optional | `1.0` | Only for UPDATING mode. |
| `min_added_submaps_count` | The minimum number of added submaps before deletion of the old submap is considered. | Optional | `1` | Only for UPDATING mode. |
| `occupied_space_weight` | Emphasis to put on scanned data points between measurements. | Optional | `20.0` | Normalized with translational and rotational. |
| `translation_weight` | Emphasis to put on expected translational change from pose extrapolator data between measurements. | Optional | `10.0` | Normalized with occupied and rotational. |
| `rotation_weight` | Emphasis to put on expected rotational change from pose extrapolator data between measurements. | Optional | `1.0` | Normalized with translational and occupied. |

## Integrated Library: ORB-SLAM3

ORB-SLAM3 can perform sparse SLAM using monocular or RGB-D images.

{{% alert title="Note" color="note" %}}
While ORB-SLAM3 does support the use of monocular cameras, for best results it is recommended that you use an RGB-D camera.
{{% /alert %}}

### Example Configuration

#### Live Mode

An example configuration for running ORB-SLAM3 in live mode, with `rgbd` image data, with two camera streams available (`color` for RGB images and `depth` for depth data):

``` json
"services": [
  {
    "name": "testorb",
    "model": "orbslamv3",
    "type": "slam",
    "attributes": {
      "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM_DIR>",
      "sensors": ["color", "depth"],
      "use_live_data": true,
      "map_rate_sec": 60,
      "data_rate_msec": 200,
      "config_params": {
        "mode": "rgbd"
      }
    }
  }
]
```

#### Offline Mode

An example configuration for running ORB-SLAM3 in offline mode:

``` json
"services": [
  {
    "name": "testorb",
    "model": "orbslamv3",
    "type": "slam",
    "attributes": {
      "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM_DIR>",
      "sensors": [],
      "use_live_data": false,
      "map_rate_sec": 120,
      "data_rate_msec": 100,
      "config_params": {
        "mode": "mono"
      }
    }
  }
]
```

### ORB-SLAM3 `config_params`

| Parameter Mode | Description | Inclusion | Default Value |
| -------------- | ----------- | --------- | ------------- |
| `mode` | `rgbd` or `mono` | **Required** | No default |
| `debug` | Boolean specifying if the service should be run in debug mode. Affects log output. | Optional | `false` |
| `orb_n_features` | Number of features per image. | Optional | `1250` |
| `orb_scale_factor` | Scale factor between levels in the scale pyramid. | Optional | `1.2` |
| `orb_n_levels` | Number of levels in the scale pyramid. | Optional | `8` |
| `orb_n_ini_th_fast` | Initial FAST threshold. | Optional | `20` |
| `orb_n_min_th_fast` | Lower threshold if no corners detected. | Optional | `7` |
| `stereo_th_depth` | Number of stereo baselines used to classify a point as close or far. Close and far points are treated differently in several parts of the stereo SLAM algorithm. | Optional | `40` |
| `depth_map_factor` | Factor to transform the depth map to real units. | Optional | `1000` |
| `stereo_b` | Stereo baseline in meters. | Optional | `0.0745` |
