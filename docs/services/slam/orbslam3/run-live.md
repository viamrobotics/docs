---
title: "Run ORB-SLAM3 on your Robot with a Webcam"
linkTitle: "Live Data Mode"
weight: 50
type: "docs"
description: "Run ORB-SLAM3 in live data mode with a webcam."
tags: ["slam", "camera", "services"]
# SMEs: Kat
---

{{% alert title="REQUIREMENTS" color="note" %}}

Running `orbslamv3` in Live Data mode requires a [webcam](/components/camera).
The webcam can be installed on a robot, or just held in your hand.

{{% /alert %}}

## Configuration

First, follow these instructions to connect and calibrate your webcam as a component of your robot:

1. [Connect and configure a webcam](/components/camera/webcam)
2. [Calibrate a camera](/components/camera/calibrate)

Now, add the `orbslamv3` service:

{{< tabs name="Add the ORBSLAM Service">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **CONFIG** tab on your robot's page, and click on the **SERVICES** subtab.

Add a service with type `slam`, model `orbslamv3`, and a name of your choice:

![adding orbslam3 slam service](../../img/run_slam/add-orbslam-service-ui.png)

Paste the following into the **Attributes** field of your new service:

```json
{
  "data_dir": "/home/<YOUR_USERNAME>/<ORBSLAM3_DIR>",
  "use_live_data": true,
  "delete_processed_data": false,
  "sensors": [ <"your-webcam-name"> ],
  "config_params": {
    "mode": "rgbd"
  }
}
```

![adding orbslam3 slam service attributes box](../../img/run_slam/add-orbslam-service-attributes-live.png)

Now, adjust `"sensors"` to match the name of the webcam you configured, and change the `data_dir` attribute on line 8 to point to a directory on your machine that you want to store your SLAM data in.
This can be an existing directory or a new directory that you want the SLAM service to automatically create.
See [SLAM: Data Directory](/services/slam/#data_dir) for requirements on this directory's structure and more information.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **CONFIG** tab .
Select the **Raw JSON** mode, then copy/paste the following `"services"` JSON to add to your existing camera configuration:

```json
// "components": [ ...], YOUR CAMERA COMPONENT
"services": [
  {
    "type": "slam",
    "name": <"your-service-name">,
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

Now, adjust `"sensors"` to match the name of the webcam you configured, and change the `data_dir` attribute on line 8 to point to a directory on your machine that you want to store your SLAM data in.
This can be an existing directory or a new directory that you want the SLAM service to automatically create.
See [SLAM: Data Directory](/services/slam/#data_dir) for requirements on this directory's structure and more information.

{{% /tab %}}
{{< /tabs >}}

After saving your config, head over to the **CONTROL** tab and click on the drop-down menu with the `name` of the service you created.
Change the **Refresh frequency** to your desired frequency, move the webcam around slowly, and watch a map start to appear.

{{% alert title="Note" color="note" %}}
It might take a couple of minutes before the first map is created and will be shown in the UI.
Keep moving the camera slowly within your space and wait for the map to get created.
{{% /alert %}}

### Attributes

| Name | Data Type | Inclusion | Description |
| ---- | --------- | --------- | ----------- |
| `data_dir` | string | **Required** | This is [the data directory](/services/slam/#data_dir) used for saving input <file>sensor/map</file> data and output <file>map/</file> visualizations. Must be structured as specified [here](/services/slam/#data_dir). |
| `sensors` | string[] | **Required** | Names of configured [webcams](/components/camera/) providing data to the SLAM service. |
| `use_live_data` | bool | **Required** | <p>This specifies whether to run in Live or Offline mode.</p> <ul> `true`: Live mode. The service grabs the most recent sensor readings and uses those to perform SLAM. If no `sensors` are provided, an error will be thrown. </ul><ul>`false`: Offline mode. The service uses image data stored in the [data directory](/services/slam/#data_dir) to perform SLAM.</ul> |
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

## Troubleshooting

### Known Issues

#### "CURRENTLY NO MAP POINTS EXIST"

This issue has a couple of potential causes.

![error getting SLAM map](../../img/run_slam/01_slam_tutorial_no_map_points.png)

First, it might take a few minutes for ORB-SLAM3 to create an initial map after starting up.
In both live and offline mode, this might mean that you have to wait a little while before you can see a map on the UI.

Second, map generation depends on the quality of the dataset.
For consecutive images, the camera's focus should not be moved too far from that of the previous image, and images should contain enough details that can be detected by ORB-SLAM3.
Images from a white wall for example will not successfully generate a map.
Try to point the camera into areas that contain a lot of information, such as objects, window frames, and similar.

In live mode, it helps to move the camera around slowly, so that consecutive images containing similar items can be matched to each other.

In offline mode, it can be difficult to determine the quality of the dataset.
If no map can be generated using the offline dataset, a new dataset should be generated.
