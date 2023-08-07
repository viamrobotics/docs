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

[The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data.

To add Cartographer to your robot, use the [`viam-cartographer`](https://github.com/viamrobotics/viam-cartographer) library, which wraps Cartographer as a [modular resource](/extend/modular-resources/).
`viam-cartographer` provides the `cartographer-module` module, which includes the `viam:slam:cartographer` {{< glossary_tooltip term_id="model-namespace-triplet" text="namespaced">}} custom [model](/extend/modular-resources/key-concepts/#models) of SLAM service.

## Requirements

To use Cartographer with Viam, install the `cartographer-module` module on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/cartographer-module https://storage.googleapis.com/packages.viam.com/apps/slam-servers/cartographer-module-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/cartographer-module
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/cartographer-module https://storage.googleapis.com/packages.viam.com/apps/slam-servers/cartographer-module-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/cartographer-module
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install cartographer-module
```

{{% /tab %}}
{{< /tabs >}}

## Configuration

{{% alert title="REQUIREMENTS" color="tip" %}}

Running `cartographer-module` requires a [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device. The default ['config_params'](#config_params) for the cartographer library, and the example robot config shown below (which uses the default 'config_params'), show nominal parameters one can use for an RPlidar A3. See the notes next to the 'config_params' for recommended settings for an RPlidar A1.

Before adding a SLAM service, you must follow [these instructions](/extend/modular-resources/examples/rplidar/) to add your RPlidar device as a modular component of your robot.

{{% /alert %}}

### Add a SLAM service

{{< tabs name="Add the Cartographer Service">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Services** subtab.

Add a service with type `slam`, model `viam:slam:cartographer`, and a name of your choice:

![adding cartographer slam service](/services/slam/add-cartographer-service-ui.png)

Paste the following into the **Attributes** field of your new service:

{{< tabs name="Add Cartographer Service Configs">}}
{{% tab name="Linux" %}}

```json
{
  "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
  "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
  "config_params": {
    "mode": "2d"
  }
}
```

{{% /tab %}}

{{% tab name="macOS" %}}

```json
{
  "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
  "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
  "config_params": {
    "mode": "2d"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

Click on the **Modules** subtab.
Add the cartographer module with a name of your choice and an executable path that points to the location of your installed `cartographer-module` binary:

{{< tabs name="Add Cartographer Service Module">}}
{{% tab name="Linux/macOS x86_64" %}}

![adding cartographer module linux](/services/slam/add-cartographer-module-ui-linux.png)

{{% /tab %}}

{{% tab name="macOS ARM64 (M1 & M2)" %}}

![adding cartographer module M1 M2](/services/slam/add-cartographer-module-ui-M1-M2.png)

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab.
Select the **Raw JSON** mode, then copy/paste the following `"services"` and `"modules"` JSON to add to your existing RPlidar configuration:

{{< tabs name="Add the Cartographer Service Config JSON OSs">}}
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
      "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
      "config_params": {
        "mode": "2d"
      }
    }
  }
]
```

{{% /tab %}}
{{% tab name="macOS x86_64" %}}

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
      "sensors": ["<YOUR_RPLIDAR_COMPONENT_NAME>"],
      "config_params": {
        "mode": "2d"
      }
    }
  }
]
```

{{% /tab %}}
{{% tab name="macOS ARM64 (M1 & M2)" %}}

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

Change the `data_dir` attribute to point to a directory on your machine where you want to save the internal state your SLAM service produces.

This directory must be structured as follows:

<pre>
.
└──\(<file>CARTOGRAPHER_DIR</file>)
    ├── <file>internal_state</file>
</pre>

The SLAM Mapping Mode is determined by 2 conditions:

1. If the internal state data is present in <file>internal_state</file> at runtime
2. The attribute `map_rate_sec`

### SLAM Mapping Modes

| Mode | Description | Runtime Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | Generate a new internal state in <file>/internal_state</file>. | No internal state is found in <file>/internal_state</file> + [`map_rate_sec > 0`](#attributes). |
| UPDATING | Update an existing internal state with new sensor readings. | An existing internal state is found in <file>/internal_state</file> + [`map_rate_sec > 0`](#attributes).|
| LOCALIZING | Localize the robot on an existing internal state without changing the internal state itself. | An internal state is found in <file>/internal_state</file> + [`map_rate_sec = 0`](#attributes). |

{{% alert title="Info" color="info" %}}

If this directory structure is not present at runtime, the SLAM service creates it.

{{% /alert %}}

### View the Map

After saving your config and connecting to your robot, navigate to the **Control** tab on your robot's page and click on the drop-down menu matching the `name` of the service you created.

Change the **Refresh frequency** to your desired frequency.
Move your RPlidar around slowly.
Watch a map start to appear.

### Attributes

| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | Path to [the directory](#slam-mapping-modes) used for saving output internal state in <file>/internal_state</file>. |
| `sensors` | string[] | **Required** | Names of configured RPlidar devices providing data to the SLAM service. May not be empty. |
| `map_rate_sec` | int | Optional | Rate of <file>/internal_state</file> generation *(seconds)*. <ul> Default: `60`. </ul> |
| `data_rate_msec` | int | Deprecated | Rate of sensor reading collection from `sensors` *(milliseconds)*. <ul>Default: `200`.</ul> |
| `config_params` |  map[string] string | Optional | Parameters available to fine-tune the `cartographer` algorithm: [read more below](#config_params). |

### `config_params`

Adjust these parameters to fine-tune the algorithm `cartographer` utilizes in aspects like submap size, mapping update rate, and feature matching details:

| Parameter Mode | Description | Inclusion | Default Value | Notes |
| -------------- | ----------- | --------- | ------------- | ----- |
| `mode` | `2d` | **Required** | None | |
| `optimize_every_n_nodes` | How many trajectory nodes are inserted before the global optimization is run. | Optional | `3` | To disable global SLAM and use only local SLAM, set this to `0`. |
| `num_range_data` | Number of measurements in each submap. | Optional | `30` | |
| `missing_data_ray_length` | Replaces the length of ranges that are further than `max_range` with this value. | Optional | `25` | Typically the same as `max_range`. |
| `max_range` | Maximum range of valid measurements. | Optional | `25` | For an RPlidar A3, set this value to `25`. For an RPlidar A1, use `12`. |
| `min_range` | Minimum range of valid measurements. | Optional | `0.2` | For an RPlidar A3, set this value to `0.2`. For RPlidar A1, use `0.15`. |
| `max_submaps_to_keep` | Number of submaps to use and track for localization. | Optional | `3` | Only for [LOCALIZING mode](#slam-mapping-modes). |
| `fresh_submaps_count` | Length of submap history considered when running SLAM in updating mode. | Optional | `3` | Only for [UPDATING mode](#slam-mapping-modes). |
| `min_covered_area` | The minimum overlapping area, in square meters, for an old submap to be considered for deletion. | Optional | `1.0` | Only for [UPDATING mode](#slam-mapping-modes). |
| `min_added_submaps_count` | The minimum number of added submaps before deletion of the old submap is considered. | Optional | `1` | Only for [UPDATING mode](#slam-mapping-modes). |
| `occupied_space_weight` | Emphasis to put on scanned data points between measurements. | Optional | `20.0` | Higher values make it harder to overwrite prior scanned points. Relative to `translation weight` and `rotation weight`. |
| `translation_weight` | Emphasis to put on expected translational change from pose extrapolator data between measurements. | Optional | `10.0` | Higher values make it harder for scan matching to translate prior scans. Relative to `occupied space weight` and `rotation weight`. |
| `rotation_weight` | Emphasis to put on expected rotational change from pose extrapolator data between measurements. | Optional | `1.0` | Higher values make it harder for scan matching to rotate prior scans. Relative to `occupied space weight` and `translation weight`. |

For more information, see the Cartographer [algorithm walkthrough](https://google-cartographer-ros.readthedocs.io/en/latest/algo_walkthrough.html), [tuning overview](https://google-cartographer-ros.readthedocs.io/en/latest/tuning.html), and [config parameter list](https://google-cartographer.readthedocs.io/en/latest/configuration.html).

## SLAM Mapping Best Practices

The best way to improve map quality is by taking extra care when creating the initial map.
While in a mapping session, you should:

- turn gently and gradually, completely avoiding sudden quick turns
- make frequent loop closures, arriving back at a previously mapped area so the robot can correct for errors in the map layout
- stay relatively (but not extremely) close to walls
- use a robot that can go smoothly over bumps and transitions between flooring areas
- drive at a moderate speed

## Troubleshooting

### Mount an RPlidar to the rover

If you have a Viam Rover and are mounting an RPlidar to your rover, be sure to position the RPlidar so that it faces forward in the direction of travel, facing in the same direction as the included webcam.
For example, if you are using the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to the Rover so that the pointed end of the RPlidar mount housing points in the direction of the front of the Rover.
This ensures that the generated [SLAM](/services/slam/) map is oriented in the expected direction relative to the Rover, with the top of the generated map corresponding to the direction the RPlidar is facing when you initiate mapping.

If you need a mount plate for your RPlidar A1 or A3 model, you can 3D print an adapter plate using the following:

- [RPlidar A1 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA1_adapter.STL)
- [RPlidar A3 adapter STL](https://github.com/viamrobotics/Rover-VR1/blob/master/CAD/RPIidarA3_adapter.STL)

### Known Issues

#### Maps not appearing in UI

When generating a larger map, it will take longer for Cartographer to return the desired map.
This can result in errors or failed requests for a map, however, this will not affect the `viam-server` or `cartographer-module` process.
Re-requesting the map can and should be successful, although there is currently a fundamental limit for the size of map that can be transmitted to the UI and this issue will become more common as you approach it.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
