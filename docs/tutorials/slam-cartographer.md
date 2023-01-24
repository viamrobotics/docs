---
title: "Run SLAM on your Robot with a LIDAR"
linkTitle: "Run SLAM on your Robot using a LIDAR"
weight: 50
type: "docs"
draft: true
description: "Instructions to run a Cartographer SLAM service with either a LIDAR (Rplidar A1 or A3) or an existing dataset."
tags: ["slam", "camera", "services", "lidar"]
# SMEs: Kat
---

{{% alert title="Note" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[Simultaneous Localization And Mapping (SLAM)](../../services/slam/) allows your robot to create a map of its surroundings and find its location within that map.

This tutorial shows you how to run [Cartographer](https://github.com/cartographer-project), a system that provides real-time SLAM, as a service on your robot.

You have two choices:

* Run SLAM in online mode with a [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) laser range scanning device.
* Run SLAM in offline mode with Viam's lab dataset or data you've collected.

## Requirements

* A Linux or macOS machine with `viam-server` installed. For more information on how to install `viam-server`, see [Install viam-server](/installation/install/).
* If you are using a Raspberry Pi, you must have Raspberry Pi OS installed on it. Refer to [Installing Raspberry Pi OS on the Raspberry Pi](../../installation/rpi-setup/#installing-raspberry-pi-os).
* [optionally] A [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3).

## Setup

If you haven’t already, install the viam-server and set up your machine on the [Viam app](https://app.viam.com) per these instructions:

* [Linux install](/installation/linux-install/)
* [macOS install](/installation/macos-install/)
* [Raspberry Pi setup](/installation/rpi-setup/)

Next, install the Cartographer binary.

### Install Cartographer

Install Cartographer with one of these commands:

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

## Run Cartographer in Online Mode with a Rplidar

Run Cartographer as a live SLAM service in online mode with a Rplidar.

### Configuration with Viam

Configure your robot to run Cartographer in live mode with a Rplidar in two steps:

1. Add your Rplidar as a modular component.
2. Add Cartographer as a SLAM service.

#### Add a Rdiplar as a Modular Component

First, install the Rplidar Module:

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

Connect the Rplidar to your machine by adding it as a modular component to your configuration in the [Viam app](https://app.viam.com/).

Plug the Rplidar into your machine, and go to your robot's page on the [Viam app](https://app.viam.com/).

In the **CONFIG** tab, click on "Raw JSON" and copy/paste the following configuration:

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

#### Add Cartographer in Online Mode as a SLAM Service

Go to your robot's page on the [Viam app](https://app.viam.com/).
On the **CONFIG** tab, click the **SERVICES** sub tab.

Create a service with type `slam`, a name (example: `run-slam`) and a model (`cartographer`).

Paste the following into the **Attributes** field of this SLAM service:

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
  "data_rate_msec": 200,
  "delete_processed_data": false,
  "sensors": ["rplidar"]
}
```

{{%expand "Click here if you prefer to use raw JSON rather than editing the **Attributes** field" %}}
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
        "data_rate_msec": 200,
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

Now, you must change the `"data_dir":` attribute (line 8 above) to be your home directory path followed by `/cartographer_dir`. 

This tells the SLAM service to create a directory named `cartographer_dir` within your home directory and to save all data and maps to that location.

Find the path to your home directory on your machine by running the `pwd` command in your machine's terminal.

{{% alert title="Note" color="note" %}}
If you are using a Raspberry Pi as your machine, you have to `ssh` into your Pi to complete this step.
{{% /alert %}}

After SSH'ing into your pi and running `pwd`, your terminal displays the home directory:

```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```
{{% /alert %}}

Save the config.

If `YOUR_USERNAME` is `slam-bot`, your complete configuration (with the Rplidar module) is:

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
          "data_rate_msec": 200,
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
          "data_rate_msec": 200,
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

Head over to the **CONTROL** tab and choose the `run-slam` drop-down menu.
Change the **Refresh frequency** to your desired frequency, move the Rplidar around slowly, and watch a map come to life!

## Run Cartographer in Offline Mode with a Dataset

Run Cartographer in offline mode using one of your previously saved lidar datasets or Viam's lab dataset.

### Configuration with Viam

Configure your robot to run Cartographer in offline mode in two steps:

1. Find an existing dataset to run Cartographer with.
2. Add Cartographer in offline mode as a SLAM service.

#### Add a Dataset to run Cartographer

In offline mode SLAM uses an existing dataset to create a map.

If you don't already have a dataset in `data_dir/data` from running SLAM in live mode, download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip).
Copy it to the machine running `viam-server` and unzip it.
For example: 

```bash
scp ~/Downloads/viam-old-office-small-pcd.zip YOUR_USERNAME@MACHINE.local:~/.
unzip viam-old-office-small-pcd.zip


Now you're ready to configure SLAM to use your dataset and to run in offline mode.

#### Add Cartographer in Offline Mode as a SLAM Service

Next, add Cartographer as a SLAM service to your configuration on the Viam app.
To enable offline mode, set the `use_live_data` flag to `false`.
This tells the SLAM service to use only data found within the `data_dir` directory you specified in your config while running SLAM.

In your web browser, navigate to your robot on [the Viam app](https://app.viam.com/robots)).
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
        "data_dir": "/home/slam-bot/viam-old-office-small-pcd",
        "map_rate_sec": 60,
        "data_rate_msec": 200,
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

Change the `"data_dir": "/home/YOUR_USERNAME/viam-old-office-small-pcd"` directory path to your machine's home directory path (found by running `pwd`) followed by `/viam-old-office-small-pcd`.

Head over to the **CONTROL** tab and click on the drop-down menu of the Cartographer SLAM service you configured.
Change the "Refresh frequency" to your desired frequency and watch a map come to life using the data in your dataset!

## Troubleshooting

### Issue: Maps JPEG not Appearing in UI

When generating a larger map, it can take longer for cartographer to return the `JPEG` map endpoint. Reducing the frequency the endpoint returns should allow the map to return.

### Issue: Maps not Appearing as Expected

For Cartographer, only `2D SLAM` is implemented currently. Because of this, Cartographer assumes your LiDAR will remain at roughly the same height while in use. If maps are not building the way you expect, ensure your lidar is secure and at roughly the same height throughout the run.

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](../../appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
