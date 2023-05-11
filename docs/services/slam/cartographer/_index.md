---
title: "Cartographer Integrated Library"
linkTitle: "Cartographer"
weight: 70
type: "docs"
description: "Configure a SLAM service with the Cartographer library."
tags: ["slam", "services"]
aliases:
  - "/services/slam/run-slam-cartographer"
# SMEs: Kat, Jeremy
---

[The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data.

## Requirements

Install the binary required to utilize the `cartographer` library on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/cartographer-module https://storage.googleapis.com/packages.viam.com/apps/slam-servers/cartographer-module-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/cartographer-module
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/cartographer-module https://storage.googleapis.com/packages.viam.com/apps/slam-servers/cartographer-module-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/cartographer-module
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install cartographer-module
```

{{% /tab %}}
{{< /tabs >}}

## Configuration

How you configure `cartographer-module` depends on whether you want the SLAM service to build your map with data collected live by a [RPlidar](https://www.slamtec.com/en/Lidar/A3) or with LIDAR data provided in a dataset at runtime.

Select from the following modes to obtain the correct instructions to configure the service:

{{% tabs name="Modes"%}}
{{% tab name="Live Data Collection" %}}

{{% alert title="REQUIREMENTS" color="tip" %}}

Running `cartographer-module` in Live Data Collection mode requires a [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device. The default ['config_params'](#config_params) for the cartographer library, and the example robot config shown below (which uses the default 'config_params'), show nominal parameters one can use for an RPlidar A3. See the notes next to the 'config_params' for recommended settings for an RPlidar A1.

Before adding a SLAM service, you must follow [these instructions](/extend/modular-resources/examples/add-rplidar-module) to add your RPlidar device as a modular component of your robot.

{{% /alert %}}

<br>

### Add a SLAM Service

{{< tabs name="Add the Cartographer Service Live">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Services** subtab.

Add a service with type `slam`, model `viam:slam:cartographer`, and a name of your choice:

![adding cartographer slam service](../img/run_slam/add-cartographer-service-ui.png)

Paste the following into the **Attributes** field of your new service:

{{< tabs name="Add Cartographer Service Live Configs">}}
{{% tab name="Linux" %}}

```json
{
  "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
  "delete_processed_data": true,
  "use_live_data": true,
  "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
  "config_params": {
    "mode": "2d"
  }
}
```

{{% /tab %}}

{{% tab name="MacOS" %}}

```json
{
  "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
  "delete_processed_data": true,
  "use_live_data": true,
  "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
  "config_params": {
    "mode": "2d"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

Click on the **Modules** subtab. Add the cartographer module with a name of your choice and an executable path that points to the location of your installed `cartographer-module` binary:

{{< tabs name="Add Cartographer Service Live Module">}}
{{% tab name="Linux/MacOS x86_64" %}}

![adding cartographer module linux](../img/run_slam/add-cartographer-module-ui-linux.png)

{{% /tab %}}

{{% tab name="MacOS ARM64 (M1 & M2)" %}}

![adding cartographer module M1 M2](../img/run_slam/add-cartographer-module-ui-M1-M2.png)

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab.
Select the **Raw JSON** mode, then copy/paste the following `"services"` and `"modules"` JSON to add to your existing RPlidar configuration:

{{< tabs name="Add the Cartographer Service Live Config JSON OSs">}}
{{% tab name="Linux" %}}

```json
"modules": [
  // { ...}, YOUR RPLIDAR MODULE,
  {
    "executable_path": "/usr/local/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
// "components": [ ...], YOUR RPLIDAR MODULAR COMPONENT,
"services": [
  {
    "model": "viam:slam:cartographer",
    "name": "<your-service-name>",
    "type": "slam",
    "attributes": {
      "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
      "delete_processed_data": true,
      "use_live_data": true,
      "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
      "config_params": {
        "mode": "2d"
      }
    }
  }
]
```

{{% /tab %}}
{{% tab name="MacOS x86_64" %}}

```json
"modules": [
  // { ...}, YOUR RPLIDAR MODULE,
  {
    "executable_path": "/usr/local/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
// "components": [ ...], YOUR RPLIDAR MODULAR COMPONENT,
"services": [
  {
    "model": "viam:slam:cartographer",
    "name": "<your-service-name>",
    "type": "slam",
    "attributes": {
      "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
      "delete_processed_data": true,
      "use_live_data": true,
      "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
      "config_params": {
        "mode": "2d"
      }
    }
  }
]
```

{{% /tab %}}
{{% tab name="MacOS ARM64 (M1 & M2)" %}}

```json
"modules": [
  // { ...}, YOUR RPLIDAR MODULE,
  {
    "executable_path": "/opt/homebrew/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
// "components": [ ...], YOUR RPLIDAR MODULAR COMPONENT,
"services": [
  {
    "model": "viam:slam:cartographer",
    "name": "<your-service-name>",
    "type": "slam",
    "attributes": {
      "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
      "delete_processed_data": true,
      "use_live_data": true,
      "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
      "config_params": {
        "mode": "2d"
      }
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{< /tabs >}}

### Adjust `data_dir`

Change the `data_dir` attribute to point to a directory on your machine where you want to save the sensor data your SLAM service uses and the maps and config files it produces.

This directory must be structured as follows:

<pre>
.
└──\(<file>CARTOGRAPHER_DIR</file>)
    ├── <file>map</file>
    ├── <file>data</file>
    └── <file>config</file>
</pre>

Click through the following tabs to see the usage of each folder in this directory:

{{% tabs name="Folders"%}}
{{% tab name="/map" %}}

Whether mapping data is present in <file>map</file> at runtime and the attribute `map_rate_sec` determines the SLAM mapping mode:

### Mapping Modes

| Mode | Description | Runtime Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | Generate a new map in <file>/map</file>. | No map is found in <file>/map</file>. |
| UPDATING | Update an existing map with new <file>/data</data>. | A map is found in <file>/map</file> + [`map_rate_sec > 0`](#attributes).|
| LOCALIZING | Localize the robot on an existing map without changing the map itself. | A map is found in <file>/map</file> + [`map_rate_sec = 0`](#attributes). |

{{% /tab %}}
{{% tab name="/data" %}}

The <file>data</file> folder stores the LIDAR data gathered by your RPlidar and used for SLAM.

{{% /tab %}}
{{% tab name="/config" %}}

The <file>config</file> folder stores any Cartographer specific config files created.
These are generated at runtime, so there is no need to add anything to this folder.

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}

If this directory structure is not present at runtime, the SLAM Service creates it.

{{% /alert %}}

{{% /tab %}}
{{% tab name="Dataset" %}}

<br>

### Add a SLAM Service

{{< tabs name="Add the Cartographer Service with Dataset">}}

{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Services** subtab.

Add a service with type `slam`, model `viam:slam:cartographer`, and a name of your choice:

![adding cartographer slam service](../img/run_slam/add-cartographer-service-ui.png)

Paste the following into the **Attributes** field of your new service:

{{< tabs name="Add the Cartographer Service with Dataset Configs">}}
{{% tab name="Linux" %}}

```json
{
    "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
    "delete_processed_data": false,
    "use_live_data": false
    "config_params": {
        "mode": "2d"
    },
}
```

{{% /tab %}}

{{% tab name="MacOS" %}}

```json
{
    "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
    "delete_processed_data": false,
    "use_live_data": false
    "config_params": {
        "mode": "2d"
    },
}
```

{{% /tab %}}
{{< /tabs >}}

Select the **Raw JSON** mode and copy/paste the following `"modules"` JSON to your existing SLAM configuration:

{{< tabs name="Add Cartographer Service with Dataset Module">}}
{{% tab name="Linux/MacOS x86_64" %}}

```json
"modules": [
  // { ...}, YOUR RPLIDAR MODULE,
  {
    "executable_path": "/usr/local/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
// "components": [ ...], YOUR RPLIDAR MODULAR COMPONENT,
// "services": [ ...], YOUR SLAM SERVICE
```

{{% /tab %}}

{{% tab name="MacOS ARM64 (M1 & M2)" %}}

```json
"modules": [
  // { ...}, YOUR RPLIDAR MODULE,
  {
    "executable_path": "/opt/homebrew/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
// "components": [ ...], YOUR RPLIDAR MODULAR COMPONENT,
// "services": [ ...], YOUR SLAM SERVICE
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab.
Select the **Raw JSON** mode, then copy/paste the following `"services"` JSON to add to your existing configuration:

{{< tabs name="Add the Cartographer Service with Dataset JSON OSs">}}
{{% tab name="Linux" %}}

``` json
"modules": [
  {
    "executable_path": "/usr/local/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
"services": [
{
    "type": "slam",
    "name": "<your-service-name>",
    "model": "cartographer",
    "attributes": {
    "config_params": {
        "mode": "2d"
    },
    "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
    "delete_processed_data": false,
    "use_live_data": false,
    }
}
]
```

{{% /tab %}}
{{% tab name="MacOS x86_64" %}}

``` json
"modules": [
  {
    "executable_path": "/usr/local/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
"services": [
{
    "type": "slam",
    "name": "<your-service-name>",
    "model": "cartographer",
    "attributes": {
    "config_params": {
        "mode": "2d"
    },
    "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
    "delete_processed_data": false,
    "use_live_data": false,
    }
}
]
```

{{% /tab %}}
{{% tab name="MacOS ARM64 (M1 & M2)" %}}

``` json
"modules": [
  {
    "executable_path": "/opt/homebrew/bin/cartographer-module",
    "name": "cartographer-module"
  }
],
"services": [
{
    "type": "slam",
    "name": "<your-service-name>",
    "model": "cartographer",
    "attributes": {
    "config_params": {
        "mode": "2d"
    },
    "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
    "delete_processed_data": false,
    "use_live_data": false,
    }
}
]
```

{{% /tab %}}
{{% /tab %}}
{{< /tabs >}}
{{< /tabs >}}

### Adjust `data_dir`

Change the `data_dir` attribute to point to a directory on your machine where you want to save the sensor data your SLAM service uses and the maps and config files it produces.

This directory must be structured as follows:

<pre>
.
└──\(<file>CARTOGRAPHER_DIR</file>)
    ├── <file>map</file>
    ├── <file>data</file>
    └── <file>config</file>
</pre>

Click through the following tabs to see the usage of each folder in this directory:

{{% tabs name="Folders 2"%}}
{{% tab name="/map" %}}

Whether mapping data is present in <file>map</file> at runtime and the attribute `map_rate_sec` determines the SLAM mapping mode:

### Mapping Modes

| Mode | Description | Runtime Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | Generate a new map. | No map is found in <file>/map</file>. |
| UPDATING | Update an existing map with new <file>/data</file>. | A map is found in <file>/map</file> + [`map_rate_sec > 0`](#attributes).|
| LOCALIZING | Localize the robot on an existing map without changing the map itself. | A map is found in <file>/map</file> + [`map_rate_sec = 0`](#attributes). |

{{% /tab %}}
{{% tab name="/data" %}}

The <file>data</file> folder stores the LIDAR data used for SLAM.

{{% /tab %}}
{{% tab name="/config" %}}

The <file>config</file> folder stores any Cartographer specific config files created.
These are generated at runtime, so there is no need to add anything to this folder.

{{% /tab %}}
{{< /tabs >}}

### Obtain your Dataset

As you are configuring SLAM to run without live data collection, you need to make sure the <file>/data</file> folder in `data_dir` contains LIDAR data for the service to generate <map>/map</file> output from when you run SLAM.

If you do not already have a dataset from running SLAM live or another dataset you want to use as <file>/data</file>, follow these instructions to use a sample dataset from Viam's lab:

1. Download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip).

2. Copy the zipped file to the machine running `viam-server` and unzip it. For example:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    scp ~/Downloads/viam-old-office-small-pcd.zip <YOUR_USERNAME>@<YOUR_MACHINE>.local:~/.
    unzip viam-old-office-small-pcd.zip
    ```

3. Rename the unzipped folder to <file>data</file> and place inside of the folder at <file>data_dir</file>. For example:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    cd /home/YOUR_USERNAME/<CARTOGRAPHER_DIR>
    mv ~/Downloads/viam-old-office-small-pcd data/
    ```

{{% /tab %}}
{{< /tabs >}}

### View the Map

After saving your config and connecting to your robot, navigate to the **Control** tab on your robot's page and click on the drop-down menu matching the `name` of the service you created.

Change the **Refresh frequency** to your desired frequency.
If in live data collection mode, move your RPlidar around slowly.
Watch a map start to appear.

### Attributes

| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | Path to [the directory](#mapping-modes) used for saving input LIDAR data in <file>/data</file> and output mapping data in <file>/map</file>. |
| `sensors` | string[] | **Required** | Names of configured RPlidar devices providing data to the SLAM service. |
| `use_live_data` | bool | **Required** | <p>Whether to run in Live Data Collection mode.</p> <ul> `true`: Use data collected live by `sensors`to generate <file>/map</file>. </ul><ul>`false`: Use a dataset provided in <file>/data</file> to generate <file>/map</file>. </ul> |
| `map_rate_sec` | int | Optional | Rate of <file>/map</file> generation *(seconds)*. <ul> Default: `60`. </ul> |
| `data_rate_msec` | int | Optional | Rate of <file>/data</file> collection from `sensors` *(milliseconds)*. <ul>Default: `200`.</ul> |
| `port` | string | Optional | Port for SLAM gRPC server. If running locally, this should be in the form "localhost:<PORT>". If no value is specified a random available port is assigned. |
| `delete_processed_data` | bool | Optional | <p>Setting this to `true` helps to reduce the amount of memory required to run SLAM.</p> <ul> `true`: sensor data is deleted after the SLAM algorithm has processed it. </ul><ul> `false`: sensor data is not deleted after the SLAM algorithm has processed it. </ul> |
| `config_params` |  map[string] string | Optional | Parameters available to fine-tune the `cartographer` algorithm: [read more below](#config_params). |

{{% alert title="Caution" color="caution" %}}

- If `use_live_data: true`, `delete_processed_data: true` by default.
- If `use_live_data: false`, `delete_processed_data: false` by default.

Setting `delete_processed_data: true` and `use_live_data: false` is invalid and will result in an error.
{{% /alert %}}

### `config_params`

Adjust these parameters to fine-tune the algorithm `cartographer` utilizes in aspects like submap size, mapping update rate, and feature matching details:

| Parameter Mode | Description | Inclusion | Default Value | Notes |
| -------------- | ----------- | --------- | ------------- | ----- |
| `mode` | `2d` | **Required** | None | |
| `optimize_every_n_nodes` | How many trajectory nodes are inserted before the global optimization is run. | Optional | `3` | |
| `num_range_data` | Number of measurements in each submap. | Optional | `100` | |
| `missing_data_ray_length` | Replaces the length of ranges that are further than `max_range` with this value. | Optional | `25` | Nominally set to max length. |
| `max_range` | Maximum range of valid measurements. | Optional | `25` | For an RPlidar A3, set this value to `25`. For an RPlidar A1, use `12`. |
| `min_range` | Minimum range of valid measurements. | Optional | `0.2` | For an RPlidar A3, set this value to `0.2`. For RPlidar A1, use `0.15`. |
| `max_submaps_to_keep` | Number of submaps to use and track for localization. | Optional | `3` | Only for [LOCALIZING mode](#mapping-modes). |
| `fresh_submaps_count` | Length of submap history considered when running SLAM in updating mode. | Optional | `3` | Only for [UPDATING mode](#mapping-modes). |
| `min_covered_area` | The minimum overlapping area, in square meters, for an old submap to be considered for deletion. | Optional | `1.0` | Only for [UPDATING mode](#mapping-modes). |
| `min_added_submaps_count` | The minimum number of added submaps before deletion of the old submap is considered. | Optional | `1` | Only for [UPDATING mode](#mapping-modes). |
| `occupied_space_weight` | Emphasis to put on scanned data points between measurements. | Optional | `20.0` | |
| `translation_weight` | Emphasis to put on expected translational change from pose extrapolator data between measurements. | Optional | `10.0` | |
| `rotation_weight` | Emphasis to put on expected rotational change from pose extrapolator data between measurements. | Optional | `1.0` | |

## Troubleshooting

### Tip: Lidar Mounting for the Viam Rover

If you have a Viam Rover and need a mount for your RPLidar, you can 3D print an adapter plate.
The STL file for an adapter plate is available on [GitHub](https://github.com/viamrobotics/VR1-22-A001/blob/master/CAD/RPIidar_adapter.STL).

### Known Issues

#### Maps not appearing in UI

When generating a larger map, it will take longer for Cartographer to return the desired map.
This can result in errors or failed requests for a map, however, this will not affect the `viam-server` or `cartographer-module` process.
Re-requesting the map can and should be successful, although there is currently a fundamental limit for the size of map that can be transmitted to the UI and this issue will become more common as you approach it.

#### Dataset mode produces an error

If there is a saved map in <file>data_dir/map</file> and saved data in <file>data_dir/data</file> from a previous run, then running SLAM with an existing dataset may raise an error at startup since the data has already been incorporated into the map.

If that occurs, you can clear <file>data_dir/map</file> and restart the service.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
