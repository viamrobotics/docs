---
title: "Run ORB-SLAM3 on your Robot with a Webcam"
linkTitle: "Run ORB-SLAM3 on your Robot with a Webcam"
weight: 50
type: "docs"
draft: true
description: "Instructions to run ORB-SLAM3 with a webcam or sample dataset."
tags: ["slam", "camera", "services"]
# SMEs: Kat
---

{{% alert title="Note" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[Simultaneous Localization And Mapping (SLAM)](../../slam/) allows your robot to create a map of its surroundings and find its location within that map.

This tutorial shows you how to run [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3), software that provides real-time SLAM, as a service on your robot.

You have two options:

1. Run ORB-SLAM3 in live mode with a webcam.
The webcam can be installed on a robot, or just held in your hand.
1. Run ORB-SLAM3 in offline mode with Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-office-hallway-1-rgbd.zip) or with data you've collected.

## Requirements

* A Linux or macOS machine with `viam-server` and `ORB-SLAM3` installed.
* [optionally] A webcam or other off-the-shelf RGB camera.

For more information on how to install `viam-server` and set up your machine on the [Viam app](https://app.viam.com), see [Install viam-server](/installation#install-viam-server).

### Install the ORB-SLAM3 Binary

Install ORB-SLAM3 with one of these commands:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

  ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
  sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
  sudo chmod a+rx /usr/local/bin/orb_grpc_server
  ```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

  ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
  sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
  sudo chmod a+rx /usr/local/bin/orb_grpc_server
  ```

{{% /tab %}}
{{< /tabs >}}

## Run ORB-SLAM3 in Live Mode with a Webcam

Run ORB-SLAM3 as a live SLAM Service with a webcam.

### Configuration with Viam

Configure your robot to run ORB-SLAM3 with a webcam in two steps:

1. Add your webcam and calibrate it.
2. Add ORB-SLAM3 as a SLAM Service in live mode.

#### Step 1: Add and Calibrate your Webcam

Follow these tutorials to connect and calibrate your webcam as a modular component of your robot:

* [Connect and configure a webcam](/components/camera/webcam)
* [Calibrate a camera](/components/camera/calibrate)

#### Step 2: Add ORB-SLAM3 as a SLAM Service in Live Mode

* Go to your robot's page on the [Viam app](https://app.viam.com/).
* On the **config** tab, click the **Services** sub tab.
* Create a service with type `slam`, a name (example: `run-slam`) and a model (`orbslamv3`).
* Paste the following into the **Attributes** field of the SLAM Service:

```json {class="line-numbers linkable-line-numbers"}
{
  "data_dir": "/home/YOUR_USERNAME/data",
  "use_live_data": true,
  "delete_processed_data": false,
  "map_rate_sec": 60,
  "data_rate_msec": 200,
  "sensors": [
    "color"
  ],
  "config_params": {
    "debug": "false",
    "orb_scale_factor": "1.2",
    "mode": "mono",
    "orb_n_features": "1250",
    "orb_n_ini_th_fast": "20",
    "orb_n_levels": "8",
    "orb_n_min_th_fast": "7"
  }
}
```

{{%expand "Click here if you prefer to use raw JSON mode" %}}

In the **config** tab, click on **Raw JSON**, and copy/paste the following configuration:

```json {class="line-numbers linkable-line-numbers"}
  "services": [
    {
      "type": "slam",
      "model": "orbslamv3",
      "attributes": {
        "data_dir": "/home/YOUR_USERNAME/data",
        "use_live_data": true,
        "map_rate_sec": 60,
        "data_rate_msec": 200,
        "sensors": [
          "color"
        ],
        "config_params": {
          "debug": "false",
          "orb_scale_factor": "1.2",
          "mode": "mono",
          "orb_n_features": "1250",
          "orb_n_ini_th_fast": "20",
          "orb_n_levels": "8",
          "orb_n_min_th_fast": "7"
        }
      },
      "name": "run-slam"
    }
  ]
```

{{% /expand %}}

</br>

* Now, change the `"data_dir":` attribute on line 8. Edit `"/home/YOUR_USERNAME/data"` to match the path to your existing dataset on your machine, followed by `/data`.
  * This tells the service to create a directory named `data` within your home directory, and to save all data and maps to that location.
  * To find your machine's home directory path, run the `pwd` command in your terminal.
    Make sure to do this while your terminal is at the home directory level (denoted by `~`).

{{% alert title="Note" color="note" %}}
If you're using a Raspberry Pi as your machine, you must `ssh` into your Pi to complete this step.

```sh {id="terminal-prompt" class="command-line" data-prompt="YOUR_USERNAME@YOUR_RPI_NAME:~ $" data-output="2"}
pwd
/home/YOUR_USERNAME
```

{{% /alert %}}

* Save the config.

At this point, your complete configuration should look like:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "color",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "intrinsic_parameters": {
          "fy": 940.2928257873841,
          "height_px": 480,
          "ppx": 320.6075282958033,
          "ppy": 239.14408757087756,
          "width_px": 640,
          "fx": 939.2693584627577
        },
        "distortion_parameters": {
          "rk2": 0.8002516496932317,
          "rk3": -5.408034254951954,
          "tp1": -0.000008996658362365533,
          "tp2": -0.002828504714921335,
          "rk1": 0.046535971648456166
        },
        "stream": "",
        "debug": false,
        "format": "",
        "video_path": "video0",
        "width_px": 0,
        "height_px": 0
      },
      "depends_on": []
    }
  ],
  "services": [
    {
      "type": "slam",
      "model": "orbslamv3",
      "attributes": {
        "data_dir": "/home/slam-bot/data",
        "use_live_data": true,
        "delete_processed_data": false,
        "map_rate_sec": 60,
        "data_rate_msec": 200,
        "sensors": [
          "color"
        ],
        "config_params": {
          "debug": "false",
          "orb_scale_factor": "1.2",
          "mode": "mono",
          "orb_n_features": "1250",
          "orb_n_ini_th_fast": "20",
          "orb_n_levels": "8",
          "orb_n_min_th_fast": "7"
        }
      },
      "name": "run-slam"
    }
  ]
}
```

* Head over to the **control** tab and click on the drop-down menu for the service you created (example: `run-slam`).
* Change the **Refresh frequency** to your desired frequency, move the webcam around slowly, and watch a map start to appear.

{{% alert title="Note" color="note" %}}
It might take a couple of minutes before the first map is created and will be shown in the UI.
Keep moving the camera slowly within your space and wait for the map to get created.
{{% /alert %}}

## Run ORB-SLAM3 in Offline Mode with a Dataset

Run ORB-SLAM3 in offline mode using one of your previously saved datasets or Viam's lab dataset.

### Configuration with Viam

Configure your robot to run ORB-SLAM3 in offline mode in two steps:

1. Find an existing dataset to run ORB-SLAM3 with.
2. Add ORB-SLAM3 as a SLAM Service in offline mode.

#### Step 1: Find a Dataset for ORB-SLAM3 to Use

In offline mode, SLAM will use an existing dataset to create a map.

You might have an RGB dataset already saved in your `data_dir/data` directory from running SLAM in live mode.
If not, don't worry! You can download our dataset: <a href="https://storage.googleapis.com/viam-labs-datasets/viam-office-hallway-1-rgbd.zip" target="_blank">Viam Office Hallway 1 - RGBD</a>.

If you downloaded our dataset, and assuming that the zip file is now located in your `~/Downloads` folder, you can copy/paste it into your Pi by running the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
scp ~/Downloads/data.zip YOUR_USERNAME@YOUR_RPI_NAME.local:~/.
```

Be sure to replace `YOUR_USERNAME` and `YOUR_RPI_NAME` with your username and Pi name.
The dataset is large, so it might take a while for it to copy over to your Pi.

Next, `ssh` into your Pi, and run:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
unzip data.zip
```

Now you're ready to configure SLAM to use your dataset and to run in offline mode.

#### Step 2: Add ORB-SLAM3 as a SLAM Service in Offline Mode

Now that you have chosen a dataset that the service can use to build its map, you can set up ORB-SLAM3 to run on your robot without a webcam.

To enable offline mode, set the `use_live_data` flag to `false`.
This tells the service to use only data found within the `data_dir` directory specified in your config while running SLAM.

* In your web browser, navigate to the robot you set up on the Viam app ([https://app.viam.com](https://app.viam.com)).
* In the **config** tab, click on **Raw JSON**, and copy/paste the following configuration:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "type": "slam",
      "model": "orbslamv3",
      "attributes": {
        "data_rate_msec": 200,
        "sensors": [],
        "use_live_data": false,
        "delete_processed_data": false,
        "config_params": {
          "debug": "false",
          "orb_scale_factor": "1.2",
          "mode": "mono",
          "orb_n_features": "1250",
          "orb_n_ini_th_fast": "20",
          "orb_n_levels": "8",
          "orb_n_min_th_fast": "7"
        },
        "data_dir": "/home/YOUR_USERNAME/data",
        "map_rate_sec": 60
      },
      "name": "run-offline-slam"
    }
  ]
}
```

* Now, change the `"data_dir":` attribute on line 8. Edit `"/home/YOUR_USERNAME/data"` to match the path to your existing dataset on your machine.
  * This tells the service to read from the directory located at this path and to save all data and maps to that location.
  * To find the home directory path for the logged-in user, run `echo $HOME` in your terminal.

* Save the config.
* Head over to the **control** tab and click on the drop-down menu for the service you created (example: `run-offline-slam`).
* Change the **Refresh frequency** to your desired frequency, move the webcam around slowly, and watch a map start to appear.

{{% alert title="Note" color="note" %}}
It may take a couple of minutes for the first map to show in the UI.
{{% /alert %}}

## Troubleshooting

### Issue: "CURRENTLY NO MAP POINTS EXIST"

This issue has a couple of potential causes.

<img src="../img/run_slam/01_slam_tutorial_no_map_points.png" alt="Error getting slam map" width="700">

First, it might take a few minutes for ORB-SLAM3 to create an initial map after starting up.
In both live and offline mode, this might mean that you have to wait a little while before you can see a map on the UI.

Second, map generation depends on the quality of the dataset.
For consecutive images, the camera's focus should not be moved too far from that of the previous image, and images should contain enough details that can be detected by ORB-SLAM3.
Images from a white wall for example will not successfully generate a map.
Try to point the camera into areas that contain a lot of information, such as objects, window frames, and similar.

In live mode, it helps to move the camera around _slowly_, so that consecutive images containing similar items can be matched to each other.

In offline mode, it can be difficult to determine the quality of the dataset.
If no map can be generated using the offline dataset, a new dataset should be generated.

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
