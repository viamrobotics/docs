---
title: "How to Run SLAM on your Robot"
linkTitle: "Run SLAM on your Robot"
weight: 50
type: "docs"
draft: false
description: "Instructions to run SLAM with either a webcam or provided example data."
# SMEs: Kat
---

{{% alert title="Note" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[SLAM](../../services/slam/) allows your robot to create a map of its surroundings, as well as find its location within that map.

This tutorial shows you how to run ORB-SLAM3 on your robot.
You have two choices:
* Run SLAM in online mode with a webcam.
The webcam can be installed on a robot, or just be held by hand.
* Run SLAM in offline mode either with collected data or our provided example data.

## Requirements

* A Raspberry Pi with Raspian OS 64-bit Lite and the viam-server installed.
Refer to [Installing Raspian on the Raspberry Pi](../../installation/rpi-setup/#installing-raspian-on-the-raspberry-pi), if necessary.
* [optionally] A webcam or other off-the-shelf RGB camera.

## Setup

If you haven’t already, please set up the Raspberry Pi on the [Viam app](https://app.viam.com) per [these instructions](../../installation/rpi-setup/).

Next, we'll install the ORB-SLAM3 binary.

### Installing the ORB-SLAM3 binary

First, `ssh` into your Pi and then check the architecture of your system by running `lscpu`.
Depending on the output download and install one of the following ORB-SLAM3 binaries:

* AArch64 (ARM64) (e.g., on an RPI):
    ```bash
    sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
    ```
* x86_64:
    ```bash
    sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
    ```

Make the file executable by running:
```bash
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

## Running ORB-SLAM3 with a webcam

The following setup allows you to run ORB-SLAM3 in live mode using a webcam.

### Configuration using Viam

The configuration of SLAM happens in two steps:
1. Add a webcam and calibrate it.
2. Add SLAM to the existing configuration.

#### Add a webcam and calibrate it

Follow these tutorials to connect and calibrate your webcam:
* [Connect and configure a webcam](../configure-a-camera/#connect-and-configure-a-webcam)
* [Calibrate a camera](../configure-a-camera/#calibrate-a-camera)

#### Add SLAM to the configuration

Find out your home directory by `ssh`-ing into your Pi, and typing `pwd`.
This is an example of what you might see:
```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```

Go to your robot's page on the [Viam app](https://app.viam.com/).
On the **CONFIG** tab, click the **SERVICES** sub-tab.

Create a service with type `slam` and a name (we called ours `run-slam`).

Paste the following into the **Attributes** field of the SLAM service:

```json
{
  "data_dir": "/home/YOUR_USERNAME/data",
  "map_rate_sec": 60,
  "data_rate_ms": 200,
  "sensors": [
    "color"
  ],
  "algorithm": "orbslamv3",
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
In the **CONFIG** tab, click on "Raw JSON", and copy/paste the following configuration:

```json-viam
  "services": [
    {
      "type": "slam",
      "attributes": {
        "data_dir": "/home/YOUR_USERNAME/data",
        "map_rate_sec": 60,
        "data_rate_ms": 200,
        "sensors": [
          "color"
        ],
        "algorithm": "orbslamv3",
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
<br>

Change the `"data_dir": "/home/YOUR_USERNAME/data"` directory to your home directory that you found out by typing `pwd`, followed by `/data`.
Save the config.

In our case, `YOUR_USERNAME` is `slam-bot`, and our complete configuration together with the [previously obtained camera configuration](#add-a-webcam-and-calibrate-it) now looks like this:

```json-viam
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
      "attributes": {
        "data_dir": "/home/slam-bot/data",
        "map_rate_sec": 60,
        "data_rate_ms": 200,
        "sensors": [
          "color"
        ],
        "algorithm": "orbslamv3",
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

Head over to the **CONTROL** tab and choose the **run-slam** drop-down menu.
Change the **Refresh frequency** to your desired frequency, move the webcam around slowly, and watch a map come to life!

{{% alert title="Note" color="note" %}}  
It might take a couple of minutes before the first map is created and will be shown in the UI.
Keep moving the camera slowly within your space and wait for the map to get created.
{{% /alert %}}

## Running ORB-SLAM3 with a dataset

The following setup allows you to run ORB-SLAM3 in offline mode using either one of your previously saved datasets, or our dataset that you can download and play with.

### The dataset

In offline mode, SLAM will use an existing dataset to create a map.

You might have an RGB dataset already saved in your `data_dir/data` directory from running SLAM in live mode.
If not, don't worry! You can download our dataset: <a href="https://storage.googleapis.com/viam-labs-datasets/viam-office-hallway-1-rgbd.zip" target="_blank">Viam Office Hallway 1 - RGBD</a>.

If you downloaded our dataset, and assuming that the zip file is now located in your `~/Downloads` folder, you can copy/paste it into your Pi by running the following command:

```bash
scp ~/Downloads/data.zip YOUR_USERNAME@YOUR_RPI_NAME.local:~/.
```
Be sure to replace `YOUR_USERNAME` and `YOUR_RPI_NAME` with your username and Pi name.
The dataset is large, so it might take a while for it to copy over to your Pi.

Next, `ssh` into your Pi, and run:

```bash
unzip data.zip
```

Now you're ready to configure SLAM to use your dataset and to run in offline mode.

### Configuration using Viam

Next, we will add SLAM to the configuration.

First, `ssh` into your Pi and find out your home directory by typing `pwd`
This is an example of what you might see:
```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```

In your web browser, navigate to the robot you set up on the Viam app ([https://app.viam.com](https://app.viam.com)).
In the **CONFIG** tab, click on "Raw JSON", and copy/paste the following configuration:

```json-viam
{
  "services": [
    {
      "type": "slam",
      "attributes": {
        "data_rate_ms": 200,
        "sensors": [],
        "algorithm": "orbslamv3",
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

Change the `"data_dir": "/home/YOUR_USERNAME/data"` directory to your home directory that you found out by typing `pwd`, followed by `/data`.
Save the config.

Head over to the **CONTROL** tab and choose the "run-slam" drop-down menu.
Change the "Refresh frequency" to your desired frequency and watch a map come to life using the data in your dataset!

{{% alert title="Note" color="note" %}}  
It might take a couple of minutes before the first map is created and will be shown in the UI.
{{% /alert %}}

## Troubleshooting

### Issue: "CURRENTLY NO MAP POINTS EXIST"

This issue has a couple of potential causes.

<img src="../img/run_slam/01_slam_tutorial_no_map_points.png" width="700"><br>
<br>

First, it might take a few minutes for ORB-SLAM3 to create an initial map after starting up.
Both in online and offline mode this might mean that you have to wait a little while before you can see a map on the UI.

Second, map generation depends on the quality of the dataset.
For consecutive images, the camera's focus should not be moved too far from that of the previous image, and images should contain enough details that can be detected by ORB-SLAM3.
Images from a white wall for example will not successfully generate a map.
Try to point the camera into areas that contain a lot of information, such as objects, window frames, and similar.

Furthermore, in online mode, it helps to move the camera around _slowly_, such that consecutive images contain similar items that can be matched to each other.

In offline mode, it can be difficult to determine the quality of the dataset.
If no map can be generated using the offline dataset, a new dataset should be generated.


## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](../../appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
