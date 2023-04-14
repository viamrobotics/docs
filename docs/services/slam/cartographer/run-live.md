---
title: "Run Cartographer SLAM on your Robot with a Rplidar"
linkTitle: "Live Data Mode"
weight: 50
type: "docs"
description: "Configure Cartographer SLAM to run in live mode with a Rplidar LIDAR scanning device."
tags: ["slam", "camera", "services", "lidar"]
# SMEs: Kat
---

{{% alert title="REQUIREMENTS" color="note" %}}

Running `cartographer` in Live Data mode requires a [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.

{{% /alert %}}

## Configuration

First, follow [these instructions](/program/extend/modular-resources/add-rplidar-module/) to add your Rplidar device as a modular component of your robot.

Now, add the `cartographer` service:

{{< tabs name="Add the Cartographer Service">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **CONFIG** tab on your robot's page, and click on the **SERVICES** subtab.

Add a service with type `slam`, model `cartographer`, and a name of your choice:

![adding cartographer slam service](/services/slam/img/run_slam/add-slam-service-ui.png)

Paste the following into the **Attributes** field of your new service:

```json
{
  "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
  "delete_processed_data": true,
  "use_live_data": true,
  "sensors": ["rplidar"],
  "config_params": {
    "mode": "2d"
  }
}
```

![adding cartographer slam service attributes box](/services/slam/img/run_slam/add-cartographer-service-attributes-live.png)

Now, change the `data_dir` attribute on line 8 to point to a directory on your machine that you want to store your SLAM data in.
This can be an existing directory or a new directory that you want the SLAM service to automatically create.
See [SLAM: Data Directory](/services/slam/#data_dir) for requirements on this directory's structure and more information.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **CONFIG** tab.
Select the **Raw JSON** mode, then copy/paste the following `"services"` JSON to add to your existing Rplidar configuration:

```json
// "modules": [ ...], YOUR RPLIDAR MODULE, 
// "components": [ ...], YOUR RPLIDAR MODULAR COMPONENT,
"services": [
  {
    "model": "cartographer",
    "name": <"your-service-name">,
    "type": "slam",
    "attributes": {
      "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
      "delete_processed_data": true,
      "use_live_data": true,
      "sensors": ["rplidar"],
      "config_params": {
        "mode": "2d"
      }
    }
  }
]
```

Now, change the `data_dir` attribute to point to a directory on your machine that you want to store your SLAM data in.
This can be an existing directory or a new directory that you want the SLAM service to automatically create.
See [SLAM: Data Directory](/services/slam/#data_dir) for requirements on this directory's structure and more information.

{{% /tab %}}
{{< /tabs >}}

After saving your config, head over to the **CONTROL** tab and click on the drop-down menu matching the `name` of the service you created.
Change the **Refresh frequency** to your desired frequency, move the Rplidar device around slowly, and watch a map start to appear.

{{% alert title="Note" color="note" %}}
It might take a couple of minutes before the first map is created and will be shown in the UI.
Keep moving the camera slowly within your space and wait for the map to get created.
{{% /alert %}}

Now that you've added your basic configuration, try adjusting `cartographer`'s attributes and config parameters to fine-tune the SLAM algorithm.

### Attributes

| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | This is [the data directory](/services/slam/#data_dir) used for saving input <file>sensor/map</file> data and output <file>map/</file> visualizations. Must be structured as specified [here](/services/slam/#data_dir). |
| `sensors` | string[] | **Required** | Names of configured Rplidars providing data to the SLAM service. |
| `use_live_data` | bool | **Required** | <p>This specifies whether to run in Live Data or Offline mode.</p> <ul> `true`: Live Data mode. The service grabs the most recent sensor readings and uses those to perform SLAM. If no `sensors` are provided, an error will be thrown. </ul><ul>`false`: Offline mode. The service uses image data stored in the [data directory](/services/slam/#data_dir) to perform SLAM.</ul> |
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

You can use these parameters to fine-tune the algorithms `cartographer` utilizes in aspects like submap size, mapping update rate, and feature matching details.

| Parameter Mode | Description | Inclusion | Default Value | Notes |
| -------------- | ----------- | --------- | ------------- | ----- |
| `mode` | `2d` | **Required** | None | |
| `optimize_every_n_nodes` | How many trajectory nodes are inserted before the global optimization is run. | Optional | `3` | |
| `num_range_data` | Number of measurements in each submap. | Optional | `100` | |
| `missing_data_ray_length` | Replaces the length of ranges that are further than max_range with this value. | Optional | `25` | Nominally set to max length. |
| `max_range` | Maximum range of valid measurements. | Optional | `25` | |
| `min_range` | Minimum range of valid measurements. | Optional | `0.2` | |
| `max_submaps_to_keep` | Number of submaps to use and track for localization. | Optional | `3` | Only for [LOCALIZING mode](/services/slam/#mapping-modes). |
| `fresh_submaps_count` | Length of submap history considered when running SLAM in updating mode. | Optional | `3` | Only for [UPDATING mode](/services/slam/#mapping-modes). |
| `min_covered_area` | The minimum overlapping area, in square meters, for an old submap to be considered for deletion. | Optional | `1.0` | Only for [UPDATING mode](/services/slam/#mapping-modes). |
| `min_added_submaps_count` | The minimum number of added submaps before deletion of the old submap is considered. | Optional | `1` | Only for [UPDATING mode](/services/slam/#mapping-modes). |
| `occupied_space_weight` | Emphasis to put on scanned data points between measurements. | Optional | `20.0` | Normalized with translational and rotational. |
| `translation_weight` | Emphasis to put on expected translational change from pose extrapolator data between measurements. | Optional | `10.0` | Normalized with occupied and rotational. |
| `rotation_weight` | Emphasis to put on expected rotational change from pose extrapolator data between measurements. | Optional | `1.0` | Normalized with translational and occupied. |

## Troubleshooting

### Known Issues

#### Maps JPEG not appearing in UI

When generating a larger map, it can take a while for the Cartographer service to return the `JPEG` map.

Reducing the frequency the Cartographer service returns the map by adjusting **Refresh frequency** should help the JPEG visualization to appear consistently.

#### Maps not appearing as expected

Only `2D SLAM` is currently implemented for Cartographer.
Because of this, Cartographer assumes your Rplidar will remain at roughly the same height while in use.
If maps are not building the way you expect, make sure your Rplidar is secure and at roughly the same height throughout the run.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
