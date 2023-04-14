---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 70
type: "docs"
description: "Simultaneous Localization And Mapping (SLAM) allows your robot to create a map of its surroundings and find its location within that map."
tags: ["slam", "services"]
icon: "/services/img/icons/slam.svg"
no_list: true
# SMEs: Kat, Jeremy
---

{{% alert title="Note" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your robot to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM Service supports the integration of SLAM as a service on your robot.

## Configuration

Integrated SLAM Libraries include:

| Model | Description |
| ----- | ----------- |
| [`cartographer`](cartographer) | [The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data. |
| [`orbslamv3`](orbslamv3) | [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) performs sparse SLAM using monocular or RGB-D images. |

## Data and Mapping Specifications

### `data_dir`

A running SLAM Service saves the sensor data it uses and the maps and config files it produces locally on the device in the directory path specified by the `attribute` `data_dir`.

To recap, the directory must be structured as follows:

<pre>
.
└──\(The Directory Defined in Config as `data_dir`)
    ├── data
    ├── map
    └── config
</pre>

- `data` contains all the sensor data collected.
- `map` contains the generated maps.
- `config` contains all SLAM library-specific config files.

{{% alert title="Note" color="note" %}}
If this directory structure is not present, the SLAM Service creates it.
{{% /alert %}}

### Mapping Modes

These modes dictate SLAM's mapping behavior at runtime, but are not configured as a part of the SLAM service's JSON configuration.
The mode utilized by the SLAM service is determined by the information found in the [data directory](#data_dir) at runtime.

| Mode | Description | Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | In PURE MAPPING mode, a new map is generated from scratch. | This mode is triggered if no map is found in the `data_dir/map` directory at runtime. |
| UPDATING | In UPDATING mode, an existing map is being changed and updated with new data. | This mode is triggered when a map is found in the `data_dir/map` directory at runtime if the attribute `"map_rate_sec"` is `> 0`.|
| LOCALIZING | In LOCALIZING mode, the map is not changed. Data is used to localize on an existing map. This is similar to UPDATING mode, except the loaded map is not changed. | This mode is triggered when a map is found in the `data_dir/map` directory at runtime if the attribute `"map_rate_sec" = 0`. |
