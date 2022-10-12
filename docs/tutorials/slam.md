---
title: "Run SLAM on your robot"
linkTitle: "Run SLAM"
weight: 90
type: "docs"
draft: true
description: "Instructions to run SLAM with either a webcam or provided example data."
---

## Warning: This is an experimental feature.
Stability is not guaranteed. Breaking changes are likely to occur, and occur often.

## Introduction
[SLAM](../../services/slam) allows your robot to create a map of its surroundings, as well as find its location within that map.

This tutorial shows you how to run ORB-SLAM3 on your robot. You have two choices:
* Run SLAM in online mode with a webcam. The webcam can be installed on a robot, or just be held by hand.
* Run SLAM in offline mode either with collected data or our provided example data.

## Requirements

* A Raspberry Pi with Raspian OS 64-bit Lite and the viam-server installed.
Refer to [Installing Raspian on the Raspberry Pi](../../getting-started/installation/#installing-raspian-on-the-raspberry-pi), if necessary.
* [optionally] A webcam or other off-the-shelf RGB camera.

## Setup
If you haven’t already, please set up the Raspberry Pi on the [Viam App](https://app.viam.com) per [these instructions](../../getting-started/installation).

Next, we'll install the ORB-SLAM3 binary.

### Installing the ORB-SLAM3 binary
First, check the architecture of your system by running `lscpu`. Depending on the output download and install one of the following ORB-SLAM3 binaries:

* AArch64 (ARM64) (e.g., on an RPI):
    ```bash
    sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-latest-aarch64.AppImage
    ```
* x86_64:
    ```bash
    sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-latest-x86_64.AppImage
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
First, you will need to add a webcam to your configuration. Configure the webcam by clicking on the "CONFIG" tab. Go to the Builder, and add a component of Type "camera" and Model "webcam", and name it "color".

Go to the "CONTROL" tab, and click on the "color" dropdown menu. Toggle "View Camera" and make sure you can see the live video feed of your camera.

Next, follow the instructions to obtain the `intrinsic_parameters` and `distortion_parameters` as described in the [camera documentation](../../components/camera#camera-models) and this [camera calibration repository](https://github.com/viam-labs/camera-calibration).

You will need to print out the checkerboard and take images of the checkerboard from various angles by clicking the "Export Screenshot" button.

After running the calibration script, you'll get a print out of the `intrinsic_parameters` and `distortion_parameters`. We will use the values we've obtained as an example moving forward:

```json
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
}
```

Copy/paste the parameters into your camera config by going into the "CONFIG" tab and clicking "Raw JSON". For us, the config now looks like this:

```json
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
        "path": "video0",
        "path_pattern": "",
        "width_px": 0,
        "height_px": 0
      },
      "depends_on": []
    }
  ]
}
```

Make sure to update the `width_px` and `height_px`in `attributes` to match the `width_px` and `height_px` as defined within `intrinsic_parameters`, which are in our case:

```json
"height_px": 480,
"width_px": 640,
```


#### Add SLAM to the configuration

Find out your home directory by typing `pwd`. This is an example of what you will see:
```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```

In the config tab, click on "Raw JSON", and copy/paste the following configuration:

```json
  "services": [
    {
      "type": "slam",
      "attributes": {
        "data_dir": "/home/YOUR_USERNAME/data",
        "map_rate_sec": 60,
        "data_rate_ms": 200,
        "input_file_pattern": "1:100:1",
        "sensors": [
          "color"
        ],
        "algorithm": "orbslamv3",
        "config_params": {
          "debug": "false",
          "orb_scale_factor": "1.2",
          "mode": "mono",
          "orb_n_features": "3000",
          "orb_n_ini_th_fast": "20",
          "orb_n_levels": "8",
          "orb_n_min_th_fast": "7"
        }
      },
      "name": "test-slam"
    }
  ]
```

Change `YOUR_USERNAME` under `"data_dir": "/home/YOUR_USERNAME/data"` to your username that you found out by typing `pwd`.

The complete configuration in our case looks now like this:

```json
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
        "path": "video0",
        "path_pattern": "",
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
        "data_dir": "/home/YOUR_USERNAME/data",
        "map_rate_sec": 60,
        "data_rate_ms": 200,
        "input_file_pattern": "1:100:1",
        "sensors": [
          "color"
        ],
        "algorithm": "orbslamv3",
        "config_params": {
          "debug": "false",
          "orb_scale_factor": "1.2",
          "mode": "mono",
          "orb_n_features": "3000",
          "orb_n_ini_th_fast": "20",
          "orb_n_levels": "8",
          "orb_n_min_th_fast": "7"
        }
      },
      "name": "test-slam"
    }
  ]
}
```

Head over to the "CONTROL" tab, move the webcam around slowly, and watch a map come to life!
