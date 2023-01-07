---
title: "How to Run SLAM on your Robot using a LIDAR"
linkTitle: "Run SLAM on your Robot using a LIDAR"
weight: 50
type: "docs"
draft: true
description: "Instructions to run SLAM with either an LIDAR or provided example data."
tags: ["slam", "camera", "services", "lidar"]
# SMEs: Kat
---

{{% alert title="Note" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[SLAM](../../services/slam/) allows your robot to create a map of its surroundings, as well as find its location within that map.

This tutorial shows you how to run [Cartographer](https://github.com/cartographer-project) on your robot.
You have two choices:

* Run SLAM in online mode with an [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3).
* Run SLAM in offline mode either with collected data or our provided example data.

## Requirements

* A Linux or macOS machine with the **viam-server** installed.
* If using a Raspberry Pi refer to [Installing Raspberry Pi OS on the Raspberry Pi](../../installation/rpi-setup/#installing-raspberry-pi-os), if necessary.
* [optionally] An [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3).

## Setup

If you haven’t already, please set up the machine on the [Viam app](https://app.viam.com) per these instructions:
*[Linux install](/installation/linux-install/)
*[macOS install](/installation/macos-install/)
*[Raspberry Pi setup](/installation/rpi-setup/)

Next, we'll install the Cartographer binary.

### Installing Cartographer

To install Cartographer, use one of the following based off your architecture:

{{< tabs >}}
{{% tab name="macOS" %}}

  ```bash
  brew tap viamrobotics/brews && brew install carto-grpc-server
  ```

{{% /tab %}}
{{% tab name="Linux aarch64" %}}

  ```bash
  sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-aarch64.AppImage
  sudo chmod a+rx /usr/local/bin/carto_grpc_server
  ```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

  ```bash
  sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-x86_64.AppImage
  sudo chmod a+rx /usr/local/bin/carto_grpc_server
  ```

{{% /tab %}}
{{< /tabs >}}

## Running Cartographer with an Rplidar

The following setup allows you to run Cartographer in live mode using an Rplidar.

### Configuration using Viam

The configuration of SLAM happens in two steps:

1. Add an Rplidar as a modular component.
2. Add SLAM to the existing configuration.

#### Add an Rplidar

First, we need to install the Rplidar Module:

{{< tabs >}}
{{% tab name="macOS" %}}

  ```bash
  brew tap viamrobotics/brews && brew install rplidar-module
  ```

{{% /tab %}}
{{% tab name="Linux aarch64" %}}

  ```bash
  sudo curl -o /usr/local/bin/rplidar-module http://packages.viam.com/apps/rplidar/rplidar-module-latest-aarch64.AppImage
  sudo chmod a+rx /usr/local/bin/rplidar-module
  ```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

  ```bash
  sudo curl -o /usr/local/bin/rplidar-module http://packages.viam.com/apps/rplidar/rplidar-module-latest-x86_64.AppImage
  sudo chmod a+rx /usr/local/bin/rplidar-module
  ```

{{% /tab %}}
{{< /tabs >}}

Connect the Rplidar into your machine. Add it as a modular component to your configuration on app.viam.com.
Go to your robot's page on the [Viam app](https://app.viam.com/). In the **CONFIG** tab, click on "Raw JSON" and copy/paste the following configuration:

{{< tabs >}}
{{% tab name="macOS" %}}

  ```json
  {
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "attributes": {
          "device_path": "/dev/tty.SLAB_USBtoUART"
        },
        "name": "rplidar"
      }
    ],
    "modules": [
      {
        "executable_path": "rplidar-module",
        "name": "rplidar_module"
      }
    ]
  }
  ```

{{% /tab %}}
{{% tab name="Linux" %}}

  ```json
  {
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "name": "rplidar"
      }
    ],
    "modules": [
      {
        "executable_path": "rplidar-module",
        "name": "rplidar-module"
      }
    ]
  }
  ```

{{% /tab %}}
{{< /tabs >}}

#### Add SLAM to the configuration

Find out your home directory by checking the output of `pwd`. When using a Raspberry Pi, you will need to `ssh` into your machine to check the directory. This is an example of what you might see on a RPi:

```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```

Go to your robot's page on the [Viam app](https://app.viam.com/).
On the **CONFIG** tab, click the **SERVICES** sub-tab.

Create a service with type `slam`, a name (we called ours `run-slam`) and a model `cartographer`.

Paste the following into the **Attributes** field of the SLAM service:

```json
{
  "config_params": {
    "min_range": "0.3",
    "max_range": "12",
    "debug": "false",
    "mode": "2d"
  },
  "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
  "map_rate_sec": 60,
  "data_rate_ms": 200,
  "delete_processed_data": false,
  "sensors": ["rplidar"]
}
```

{{%expand "To use raw JSON rather than editing the Attributes field: " %}}
Click "Raw JSON" on the **CONFIG** tab, then copy/paste the following configuration:

```json-viam
  "services": [
    {
      "attributes": {
        "config_params": {
          "min_range": "0.3",
          "max_range": "12",
          "debug": "false",
          "mode": "2d"
        },
        "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
        "map_rate_sec": 60,
        "data_rate_ms": 200,
        "delete_processed_data": false,
        "sensors": ["rplidar"]
      },
      "model": "cartographer",
      "name": "test",
      "type": "slam"
    }
  ]
```

{{% /expand %}}
<br>

Change the `"data_dir": "/home/YOUR_USERNAME/cartographer_dir"` directory to your home directory that you found out by typing `pwd`, followed by `/cartographer_dir`.
Doing this tells the slam service to create a directory named `cartographer_dir` and to save all data and maps to that location. Save the config.

In our case, `YOUR_USERNAME` is `slam-bot`, and our complete configuration together with the Rplidar module now looks like this:

{{< tabs >}}
{{% tab name="macOS" %}}

  ```json-viam
  {
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "attributes": {
          "device_path": "/dev/tty.SLAB_USBtoUART"
        },
        "name": "rplidar"
      }
    ],
    "modules": [
      {
        "executable_path": "rplidar-module",
        "name": "rplidar_module"
      }
    ],
    "services": [
      {
        "attributes": {
          "config_params": {
            "min_range": "0.3",
            "max_range": "12",
            "debug": "false",
            "mode": "2d"
          },
          "data_dir": "/home/slam-bot/cartographer_dir",
          "map_rate_sec": 60,
          "data_rate_ms": 200,
          "delete_processed_data": false,
          "use_live_data": true,
          "sensors": ["rplidar"]
        },
        "model": "cartographer",
        "name": "test",
        "type": "slam"
      }
    ]
  }
  ```

{{% /tab %}}
{{% tab name="Linux" %}}

  ```json-viam
  {
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "name": "rplidar"
      }
    ],
    "modules": [
      {
        "executable_path": "rplidar-module",
        "name": "rplidar_module"
      }
    ],
    "services": [
      {
        "attributes": {
          "config_params": {
            "min_range": "0.3",
            "max_range": "12",
            "debug": "false",
            "mode": "2d"
          },
          "data_dir": "/home/slam-bot/cartographer_dir",
          "map_rate_sec": 60,
          "data_rate_ms": 200,
          "delete_processed_data": false,
          "use_live_data": true,
          "sensors": ["rplidar"]
        },
        "model": "cartographer",
        "name": "test",
        "type": "slam"
      }
    ]
  }
  ```

{{% /tab %}}
{{< /tabs >}}

Head over to the **CONTROL** tab and choose the **run-slam** drop-down menu.
Change the **Refresh frequency** to your desired frequency, move the webcam around slowly, and watch a map come to life!

## Running ORB-SLAM3 with a dataset

The following setup allows you to run ORB-SLAM3 in offline mode using either one of your previously saved datasets, or our dataset that you can download and play with.

### The dataset

In offline mode, SLAM will use an existing dataset to create a map.

You might have an lidar dataset already saved in your `data_dir/data` directory from running SLAM in live mode.
If not, don't worry! You can download our dataset: <a href="https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip" target="_blank">Viam Old Office - Cartographer</a>.

If you downloaded our dataset and are using a Raspberry Pi, and assuming that the zip file is now located in your `~/Downloads` folder, you can copy/paste it into your Pi by running the following command:

```bash
scp ~/Downloads/viam-old-office-small-pcd.zip YOUR_USERNAME@YOUR_RPI_NAME.local:~/.
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
      "attributes": {
        "config_params": {
          "min_range": "0.3",
          "max_range": "12",
          "debug": "false",
          "mode": "2d"
        },
        "data_dir": "/home/slam-bot/cartographer_dir",
        "map_rate_sec": 60,
        "data_rate_ms": 200,
        "delete_processed_data": false,
        "use_live_data": false,
        "sensors": ["rplidar"]
      },
      "model": "cartographer",
      "name": "test",
      "type": "slam"
    }
  ]
}
```

Change the `"data_dir": "/home/YOUR_USERNAME/cartographer_dir"` directory to your home directory that you found out by typing `pwd`, followed by `/data`.
Save the config.

Head over to the **CONTROL** tab and choose the "run-slam" drop-down menu.
Change the "Refresh frequency" to your desired frequency and watch a map come to life using the data in your dataset!

## Troubleshooting

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](../../appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
