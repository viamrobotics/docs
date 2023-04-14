---
title: "Run Cartographer SLAM on your Robot with Sample LIDAR Data"
linkTitle: "Offline Mode"
weight: 50
type: "docs"
description: "Configure Cartographer SLAM to run in offline mode with a sample LIDAR dataset."
tags: ["slam", "camera", "services", "lidar"]
# SMEs: Kat
---

In offline mode, [Cartographer](https://github.com/cartographer-project) SLAM uses an existing LIDAR dataset to create a map.

## Find your dataset

The path to this dataset is specified by the SLAM service's `data_dir` configuration attribute.
The directory at the `data_dir` path should have a folder inside it called `data`, which is where this data should be stored.

- If your folder `data_dir/data` is already populated from running SLAM in live mode, no change is needed.
- If you wish to use another dataset for SLAM, you can make it the folder `data_dir/data`.

See [SLAM: Data Directory](/services/slam/#data_dir) for requirements on this directory's structure and more information.

If you don't already have a dataset in `data_dir/data` from running SLAM in live mode, follow these instructions:

{{%expand "use Viam's lab dataset" %}}

1. Download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip).
2. Copy the zipped file to the machine running `viam-server` and unzip it.

    For example:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    scp ~/Downloads/viam-old-office-small-pcd.zip YOUR_USERNAME@MACHINE.local:~/.
    unzip viam-old-office-small-pcd.zip
    ```

3. Rename the unzipped folder to `data` and place inside of the [data directory](/services/slam/#data_dir).

    For example:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    cd /home/YOUR_USERNAME/cartographer_dir
    mv ~/Downloads/viam-old-office-small-pcd data/
    ```

{{% /expand%}}

## Configuration

{{< tabs name="Add the Cartographer Service">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **CONFIG** tab on your robot's page, and click on the **SERVICES** subtab.

Add a service with type `slam`, model `cartographer`, and a name of your choice:

![adding cartographer slam service](/services/slam/img/run_slam/add-slam-service-ui.png)

Paste the following into the **Attributes** field of your new service::

```json
{
    "config_params": {
        "mode": "2d"
    },
    "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>/data",
    "delete_processed_data": false,
    "use_live_data": false
}
```

![adding cartographer slam service attributes box](/services/slam/img/run_slam/add-cartographer-service-attributes-offline.png)

Change `data_dir` to match the path to your dataset on your machine.

{{% alert title="Tip" color="tip" %}}

To find the path to your dataset on your machine, use your terminal to navigate to the dataset with `cd` and run the `pwd` command.

{{% /alert %}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **CONFIG** tab.
Select the **Raw JSON** mode, then copy/paste the following `"services"` JSON to add to your existing configuration:

``` json
"services": [
{
    "attributes": {
    "config_params": {
        "mode": "2d"
    },
    "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>/data",
    "delete_processed_data": false,
    "use_live_data": false
    },
    "model": "cartographer",
    "name": <"your-service-name">,
    "type": "slam"
}
]
```

Now, change the `data_dir` attribute to match the path to your dataset on your machine.

See [SLAM: Data Directory](/services/slam/#data_dir) for requirements on this directory's structure and more information.

{{% /tab %}}
{{< /tabs >}}

After saving your config, head over to the **CONTROL** tab and click on the drop-down menu matching the `name` of the service you created to watch a map start to appear.

Now that you've added your basic configuration, try adjusting `cartographer`'s attributes and config parameters to fine-tune the SLAM algorithm.

### Attributes

| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | This is [the data directory](/services/slam/#data_dir) used for saving input <file>sensor/map</file> data and output <file>map/</file> visualizations. Must be structured as specified [here](/services/slam/#data_dir). |
| `sensors` | string[] | **Required** | Names of configured Rplidar sensors providing data to the SLAM service. |
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

#### Offline mode produces an error after restart

If there is a saved map in `data_dir/map` and saved data in `data_dir/data` from a previous run, then offline mode
may error at startup, since the data has already been incorporated into the map. If that occurs, you can
clear `data_dir/map` to rerun the dataset in offline mode.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
