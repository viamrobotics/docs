---
title: "ORB-SLAM3 Integrated Library"
linkTitle: "ORB-SLAM3"
weight: 70
type: "docs"
draft: true
description: "Configure a SLAM service with the ORB-SLAM3 library."
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

[ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) performs sparse {{< glossary_tooltip term_id="slam" text="SLAM" >}} using monocular or RGB-D images.

{{% alert title="Tip" color="tip" %}}
While ORB-SLAM3 does support the use of monocular cameras, for best results it is recommended that you use an RGB-D camera.
{{% /alert %}}

### Requirements

Install the binary required to utilize `orbslamv3` on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/orb_grpc_server https://storage.googleapis.com/packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{< /tab >}}
{{% tab name="Linux x86_64" %}}

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/orb_grpc_server https://storage.googleapis.com/packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{% /tab %}}
{{< /tabs >}}

### Configuration

How you configure `orbslamv3` depends on whether you want the SLAM service to build your map with data collected live by a [webcam](/components/camera/) or with data provided in a dataset at runtime.

Select from the following modes to obtain the correct instructions to configure the service:

{{% tabs name="Modes"%}}
{{% tab name="Live Data Collection" %}}

{{% alert title="REQUIREMENTS" color="note" %}}

Running `orbslamv3` in Live Data mode requires a [webcam](/components/camera/).
The webcam can be installed on a robot, or just held in your hand.

{{% /alert %}}

First, follow these instructions to connect and calibrate your webcam as a component of your robot:

1. [Connect and configure a webcam](/components/camera/webca/)
2. [Calibrate a camera](/components/camera/calibrate/)

Now, add the `orbslamv3` service:

{{< tabs name="Add the ORBSLAM3 Service Live">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Services** subtab.

Add a service with type `slam`, model `orbslamv3`, and a name of your choice.

![adding orbslam3 slam service](/services/slam/add-orbslam-service-ui.png)

Paste the following into the **Attributes** field of your new service:

```json
{
  "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM3_DIR>",
  "use_live_data": true,
  "delete_processed_data": true,
  "sensors": ["<your-webcam-name>"],
  "config_params": {
    "mode": "rgbd"
  }
}
```

![adding orbslam3 slam service attributes box](/services/slam/add-orbslam-service-attributes-live.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab .
Select the **Raw JSON** mode, then copy/paste the following `"services"` JSON to add to your existing camera configuration:

```json
// "components": [ ...], YOUR CAMERA COMPONENT
"services": [
  {
    "type": "slam",
    "name": "<your-service-name>",
    "model": "orbslamv3",
    "attributes": {
      "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM_DIR>",
      "use_live_data": true,
      "delete_processed_data": true,
      "sensors": [ <your-webcam-name> ],
      "config_params": {
        "mode": "rgbd"
      }
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

Adjust `"sensors"` to match the name of the webcam you configured.

Now, edit the path specified by `data_dir` to point to a directory on your machine where you want to save the maps and any config files your SLAM service produces.

This directory must be structured as follows:

<pre>
.
└──\(<file>ORBSLAM3_DIR</file>)
    ├── <file>data</file>
    ├── <file>map</file>
    └── <file>config</file>
</pre>

Click through the following tabs to see the usage of each folder in this directory:

{{% tabs name="Folders"%}}
{{% tab name="/data" %}}

The <file>data</file> folder stores the visual data gathered by your webcam and used for SLAM.

{{% /tab %}}
{{% tab name="/map" %}}

Whether mapping data is present in <file>data_dir/map</file> at runtime and the attribute `map_rate_sec` determines the SLAM mapping mode:

### Mapping Modes

<!-- prettier-ignore -->
| Mode | Description | Runtime Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | Generate a new map in file>/map</file>. | No map is found in <file>/map</file>. |
| UPDATING | Update an existing map with new data. | A map is found in <file>/map</file> + [`map_rate_sec > 0`](#attributes-and-config_params).|
| LOCALIZING | Localize the robot on an existing map without changing the map itself. | A map is found in <file>/map</file> + [`map_rate_sec = 0`](#attributes-and-config_params). |

{{% /tab %}}
{{% tab name="/config" %}}

The <file>config</file> folder stores any ORB-SLAM3 specific config files created.
These are generated at runtime, so there is no need to add anything to this folder.

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Info" color="info" %}}

If this directory structure is not present at runtime, the SLAM service creates it.

{{% /alert %}}

{{% /tab %}}
{{% tab name="Dataset" %}}

{{< tabs name="Add the ORBSLAM3 Service with Dataset">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Services** subtab.

Add a service with type `slam`, model `orbslamv3`, and a name of your choice:

![adding orbslam3 slam service](/services/slam/add-orbslam-service-ui.png)

Paste the following into the **Attributes** field of your new service:

```json
{
  "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM3_DIR>",
  "use_live_data": false,
  "delete_processed_data": false,
  "config_params": {
    "mode": "rgbd"
  }
}
```

![adding orbslam3 slam service attributes box](/services/slam/add-orbslam-service-attributes-offline.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab .
Select the **Raw JSON** mode, then copy/paste the following `"services"` JSON to add to your existing camera configuration:

```json
// "components": [ ...], YOUR CAMERA COMPONENT
"services": [
  {
    "type": "slam",
    "name": "<your-service-name>",
    "model": "orbslamv3",
    "attributes": {
      "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM3_DIR>",
      "use_live_data": false,
      "delete_processed_data": false,
      "config_params": {
        "mode": "rgbd"
      }
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

Now, edit the path specified by `data_dir` to point to a directory on your machine where you want to save the maps and any config files your SLAM service produces.

This directory must be structured as follows:

<pre>
.
└──\(<file>ORBSLAM3_DIR</file>)
    ├── <file>data</file>
    ├── <file>map</file>
    └── <file>config</file>
</pre>

Click through the following tabs to see the usage of each folder in this directory:

{{% tabs name="Folders 2"%}}
{{% tab name="/data" %}}

As you are configuring SLAM to run without live data collection, you need to make sure the <file>data</file> folder contains visual data at runtime for the service to generate a <map>map</file> from.

If you do not already have a dataset from running SLAM live or another dataset you want to use as <file>/data</file>, follow these instructions to use a sample dataset from Viam's lab:

1. Download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-office-hallway-1-rgbd.zip).

2. Copy the zipped file to the machine running `viam-server` and unzip it.
   For example:

   ```sh {class="command-line" data-prompt="$"}
   scp ~/Downloads/viam-office-hallway-1-rgbd.zip <YOUR_USERNAME>@<YOUR_MACHINE>.local:~/.
   unzip viam-office-hallway-1-rgbd.zip
   ```

3. Rename the unzipped folder to <file>data</file> and place inside of the folder at <file>data_dir</file>. For example:

   ```sh {class="command-line" data-prompt="$"}
   cd /home/<YOUR_USERNAME>/<ORBSLAM3_DIR>
   mv ~/Downloads/viam-office-hallway-1-rgbd data/
   ```

{{% /tab %}}
{{% tab name="/map" %}}

Whether mapping data is present in <file>data_dir/map</file> at runtime and the attribute `map_rate_sec` determines the SLAM mapping mode:

### Mapping Modes

<!-- prettier-ignore -->
| Mode | Description | Runtime Dictation |
| ---- | ----------- | ------- |
| PURE MAPPING | Generate a new map. | No map is found in <file>/map</file>. |
| UPDATING | Update an existing map with new data. | A map is found in <file>/map</file> + [`map_rate_sec > 0`](#attributes-and-config_params).|
| LOCALIZING | Localize the robot on an existing map without changing the map itself. | A map is found in <file>/map</file> + [`map_rate_sec = 0`](#attributes-and-config_params). |

{{% /tab %}}
{{% tab name="/config" %}}

The <file>config</file> folder stores ORB-SLAM3 specific config files.
These are generated at runtime, so there is no need to adjust this folder.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

### Attributes and `config_params`

{{% tabs name="Attributes"%}}
{{% tab name="Attributes" %}}

<!-- prettier-ignore -->
| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | Path to the directory used for saving input <file>/data</file> and output <file>/map</file> visualizations. |
| `sensors` | string[] | **Required** | Names of any configured [webcams](/components/camera/) providing data to the SLAM service. |
| `use_live_data` | bool | **Required** | <p>Whether to run in Live Data Collection mode.</p> <ul> `true`: Use data collected live by `sensors`to generate <file>/map</file>. </ul><ul>`false`: Use a dataset provided in <file>data_dir/data</file> to generate <file>/map</file>. </ul> |
| `map_rate_sec` | int | Optional | Map generation rate for saving current state *(seconds)*. <ul> Default: `60`. </ul> |
| `data_rate_msec` | int | Optional | Data generation rate for collecting sensor data to feed to SLAM *(milliseconds)*. <ul>Default: `200`.</ul> |
| `port` | string | Optional | Port for SLAM gRPC server. If running locally, this should be in the form "localhost:<PORT>". If no value is specified a random available port is assigned. |
| `delete_processed_data` | bool | Optional | <p>Setting this to `true` helps to reduce the amount of memory required to run SLAM.</p> <ul> `true`: sensor data is deleted after the SLAM algorithm has processed it. </ul><ul> `false`: sensor data is not deleted after the SLAM algorithm has processed it. </ul> |
| `config_params` |  map[string] string | Optional | Parameters to fine-tune the algorithm `orbslamv3` utilizes. |

{{% alert title="Caution" color="caution" %}}

- If `use_live_data: true`, `delete_processed_data: true` by default.
- If `use_live_data: false`, `delete_processed_data: false` by default.

Setting `delete_processed_data: true` and `use_live_data: false` is invalid and will result in an error.
{{% /alert %}}

{{% /tab %}}
{{% tab name="config_params" %}}

Adjust these parameters to fine-tune the algorithm `orbslamv3` utilizes:

<!-- prettier-ignore -->
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

{{% /tab %}}
{{< /tabs >}}

## View the Map

After saving your config, head over to the **Control** tab and click on the dropdown menu matching the `name` of the service you created.

Change the **Refresh frequency** to your desired frequency.
If in Live Data mode, move your webcam around slowly.
Watch a map start to appear.

{{% alert title="Tip" color="tip" %}}
It might take a couple of minutes before a map is displayed.
Keep moving the camera slowly within your space and wait for the map to visualize.
{{% /alert %}}

## Troubleshooting

### Known Issues

#### "CURRENTLY NO MAP POINTS EXIST"

This issue has a couple of potential causes.

![error getting SLAM map](/services/slam/01_slam_tutorial_no_map_points.png)

First, it might take a few minutes for ORB-SLAM3 to create an initial map after starting up.
In both live and offline mode, this might mean that you have to wait a little while before you can see a map on the UI.

Second, map generation depends on the quality of the dataset.
For consecutive images, the camera's focus should not be moved too far from that of the previous image, and images should contain enough details that can be detected by ORB-SLAM3.
Images from a white wall for example will not successfully generate a map.
Try to point the camera into areas that contain a lot of information, such as objects, window frames, and similar.

In live mode, it helps to move the camera around slowly, so that consecutive images containing similar items can be matched to each other.

In offline mode, it can be difficult to determine the quality of the dataset.
If no map can be generated using the offline dataset, a new dataset should be generated.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
