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

Viam provides the `cartographer` [modular resource](/modular-resources/) which adds support for using Cartographer with the Viam [SLAM service](/services/slam/).

The `cartographer` {{< glossary_tooltip term_id="module" text="module" >}} is available [from the Viam registry](https://app.viam.com/module/viam/cartographer).
See [Modular resources](/modular-resources/#the-viam-registry) for instructions on using a module from the Viam registry on your robot.

The source code for this module is available on the [`viam-cartographer` GitHub repository](https://github.com/viamrobotics/viam-cartographer).

## Requirements

If you haven't already, [install `viam-server`](/installation/) on your robot.

Your robot must have an RPlidar installed to be able to use the `cartographer` module, such as the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3).
The default ['config_params'](#config_params) for the cartographer library as well as the example robot config shown below (which uses the default 'config_params') show nominal parameters one can use for an RPlidar A3.
See the notes next to the 'config_params' for recommended settings for an RPlidar A1.

In addition, you must [add the `rplidar` module to your robot](/modular-resources/examples/rplidar/) to support the RPlidar hardware, if you have not done so already.

Currently, the `rplidar` and `cartographer` modules support the Linux platform only.

Physically connect the RPlidar to your robot.
Be sure to position the RPlidar so that it faces forward in the direction your robot travels.
For example, if you are using the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to your robot so that the pointed end of the RPlidar mount housing points in the direction of the front of the robot.

## Configuration

After installing your physical RPlidar and adding the `rplidar` module per the above instructions, follow the steps below to add the `cartographer` module to your robot:

{{< tabs name="Add the cartographer service">}}
{{% tab name="Config Builder" %}}

Follow the instructions below to set up the `cartographer` module on your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Services** subtab and click **Create service** in the lower-left corner.
1. Select **SLAM**, then select `cartographer`.
   You can also search for "cartographer".
1. Click **Add module**, give your service a name of your choice, then click **Create**.
1. In the resulting `SLAM` service configuration pane, configure the `"data_dir"` and `"sensors"` **Attributes** as follows:

   - `"data-dir"`: Provide the path to [the directory](#slam-mapping-modes) used for saving output internal state in <file>/internal_state</file>.
     Example: `"data-dir": "/home/my-username/cartographer-directory"`
   - `"sensors"`: Provide the `name` of the configured movement sensor that you created when you [added the `rplidar` module to your robot](/modular-resources/examples/rplidar/).
     Example: `"sensors": ["my-rplidar"]`

   See the [Attributes](#attributes) section for more information on the other attributes.

1. Click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

Note: This template includes configuration for both the `rplidar` and `cartographer` modules, since both are required here.

```json
{
  "components": [
    {
      "name": "<your-rplidar-name>",
      "model": "viam:lidar:rplidar",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ],
  "services": [
    {
      "name": "<your-cartographer-name>",
      "type": "slam",
      "namespace": "rdk",
      "model": "viam:slam:cartographer",
      "attributes": {
        "config_params": {
          "mode": "2d"
        },
        "data_dir": "</path/to/cartographer-directory>",
        "data_rate_msec": <int>,
        "map_rate_sec": <int>,
        "sensors": [
          "<your-rplidar-name>"
        ]
      }
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.36"
    },
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.14"
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Example" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

Note: This example includes configuration for both the `rplidar` and `cartographer` modules, since both are required here.

```json
{
  "components": [
    {
      "name": "my-rplidar",
      "model": "viam:lidar:rplidar",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ],
  "services": [
    {
      "name": "my-cartographer",
      "type": "slam",
      "namespace": "rdk",
      "model": "viam:slam:cartographer",
      "attributes": {
        "config_params": {
          "mode": "2d"
        },
        "data_dir": "/Users/my-username/cartographer-directory",
        "data_rate_msec": 200,
        "map_rate_sec": 60,
        "sensors": ["my-rplidar"]
      }
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.36"
    },
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.14"
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{< /tabs >}}

Check the **Logs** tab of your robot in the Viam app to make sure your RPlidar has connected and no errors are being raised.

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

<!-- prettier-ignore -->
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

<!-- prettier-ignore -->
| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | Path to [the directory](#slam-mapping-modes) used for saving output internal state in <file>/internal_state</file>. |
| `sensors` | string[] | **Required** | Array of one or more names of configured RPlidar devices providing data to the SLAM service. May not be empty. |
| `map_rate_sec` | int | Optional | Rate of <file>/internal_state</file> generation *(seconds)*. <ul> Default: `60`. </ul> |
| `data_rate_msec` | int | Deprecated | Rate of sensor reading collection from `sensors` *(milliseconds)*. <ul>Default: `200`.</ul> |
| `config_params` |  map[string] string | Optional | Parameters available to fine-tune the `cartographer` algorithm: [read more below](#config_params). |

### `config_params`

Adjust these parameters to fine-tune the algorithm `cartographer` utilizes in aspects like submap size, mapping update rate, and feature matching details:

<!-- prettier-ignore -->
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
