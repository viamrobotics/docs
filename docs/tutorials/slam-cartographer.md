---
title: "Run SLAM on your Robot with a LIDAR"
linkTitle: "Run SLAM on your Robot using a LIDAR"
weight: 50
type: "docs"
draft: false
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

You have two options:

* Run Cartographer SLAM in online mode with a [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.
* Run Cartographer SLAM in offline mode with Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/) or with data you've collected.

## Requirements

* A Linux or macOS machine with `viam-server` and `Cartographer` installed.
* [optionally] A [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.

For more information on how to install `viam-server` and set up your machine on the [Viam app](https://app.viam.com), see [Install viam-server](/installation/install/).

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

Configure your robot to run Cartographer with a Rplidar in two steps:

1. Add your Rplidar as a modular component.
2. Add Cartographer as a SLAM service in online mode.

#### Step 1: Add your Rdiplar as a Modular Component

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

Now add the Rplidar as a modular component of your robot in the [Viam app](https://app.viam.com/):

1. Physically connect the Rplidar to your machine.
2. Go to your robot's page on the [Viam app](https://app.viam.com/).
3. In the **CONFIG** tab, select **Raw JSON** mode.
4. Copy the following configuration code for your Rplidar device. Paste it into the "Raw JSON":

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
5. Click **Save Config** to save the module.

#### Step 2: Add Cartographer as a SLAM Service in Online Mode

Now that you've added your Rplidar device as a modular component of your robot, you can set up Cartographer to use the device's scan data while performing SLAM.

1. Go to your robot's page on the [Viam app](https://app.viam.com/).
2. On the **CONFIG** tab, click the **SERVICES** sub tab.
3. Create a service with type `slam`, a name (example: `run-slam`) and a model (`cartographer`).
4. Paste the following into the **Attributes** field of your new service:

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

{{%expand "Click here if you prefer to use Raw JSON to build your service" %}}
In the **CONFIG** tab, select the **Raw JSON** mode, then copy/paste the following configuration:

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
5. Now, change the `"data_dir":` attribute (line 8):

* Edit `"/home/YOUR_USERNAME/cartographer_dir"` to be your home directory path followed by `/cartographer_dir`.
  * This tells the service to create a directory named `cartographer_dir` within your home directory, and to save all data and maps to that location.
  * To find your machine's home directory path, run the `pwd` command in your terminal. Make sure to do this while your terminal is at the home directory level (denoted by `~`).
  
{{% alert title="Note" color="note" %}}
If you are using a Raspberry Pi as your machine, you must `ssh` into your Pi to complete this step.

```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```
{{% /alert %}}

1. Click **Save Config** to save the service.

At this point, your complete configuration should look like:

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
          "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
          "map_rate_sec": 60,
          "data_rate_msec": 200,
          "delete_processed_data": false,
          "use_live_data": true,
          "sensors": ["rplidar"]
        },
        "model": "cartographer",
        "name": "run-slam",
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
          "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
          "map_rate_sec": 60,
          "data_rate_msec": 200,
          "delete_processed_data": false,
          "use_live_data": true,
          "sensors": ["rplidar"]
        },
        "model": "cartographer",
        "name": "run-slam",
        "type": "slam"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{< /tabs >}}

7. Head over to the **CONTROL** tab and click on the drop-down menu for the service you created (example: `run-slam`).
8. Change the **Refresh frequency** to your desired frequency, move the Rplidar device around slowly, and watch a map start to appear.

## Run Cartographer in Offline Mode with a Dataset

Run Cartographer in offline mode using one of your previously saved LIDAR datasets or Viam's lab dataset.

### Configuration with Viam

Configure your robot to run Cartographer in offline mode in two steps:

1. Find an existing dataset to run Cartographer with.
2. Add Cartographer as a SLAM service in offline mode.

#### Step 1: Find a Dataset for Cartographer to Use

In offline mode SLAM uses an existing dataset to create a map.

* If you already have a dataset in `data_dir/data` from running SLAM in live mode, or wish to use another dataset for SLAM, grab the path to that dataset on your local machine to complete part 4 of Step 2.
* If you don't already have a dataset in `data_dir/data` from running SLAM in live mode, download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip).
Copy it to the machine running `viam-server` and unzip it.
For example:
  
```bash
scp ~/Downloads/viam-old-office-small-pcd.zip YOUR_USERNAME@MACHINE.local:~/.
unzip viam-old-office-small-pcd.zip
```

Now you're ready to configure SLAM to use your dataset and to run in offline mode.

#### Step 2: Add Cartographer as a SLAM Service in Offline Mode

Now that you have chosen a dataset that the service can use to build its map, you can set up Cartographer to run on your robot without a LIDAR scanning device.

To enable offline mode, set the `use_live_data` flag to `false`.
This tells the service to use only data found within the `data_dir` directory specified in your config while running SLAM.

1. Go to your robot's page on [the Viam app](https://app.viam.com/robots).
2. In the **CONFIG** tab, select **Raw JSON** mode.
3. Copy the following configuration code for your Cartographer service. Paste it into the "Raw JSON":

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
        "data_dir": "/home/YOUR_USERNAME/viam-old-office-small-pcd",
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

4. Now, change the `"data_dir":` attribute (line 8).

    Edit `"/home/YOUR_USERNAME/viam-old-office-small-pcd"` to match the path to your existing dataset on your local machine.
   * This tells the service to read from the directory located at this path and to save all data and maps to that location.
   * To find your machine's home directory path, run the `pwd` command in your terminal. Make sure to do this while your terminal is at the home directory level (denoted by `~`).

{{% alert title="Note" color="note" %}}
If you're using a Raspberry Pi as your machine, you must `ssh` into your Pi to complete this step.

```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```
{{% /alert %}}

5. Head over to the **CONTROL** tab and click on the drop-down menu of the service you created.
6. Change the **Refresh frequency** to your desired frequency, move the Rplidar device around slowly, and watch a map start to appear.

## Troubleshooting

### Issue: Maps JPEG not Appearing in UI

When generating a larger map, it can take longer for Cartographer to return the `JPEG` map endpoint. Reducing the frequency the endpoint returns should allow the map to return.

### Issue: Maps not Appearing as Expected

For Cartographer, only `2D SLAM` is implemented currently.
Because of this, Cartographer assumes your Rplidar will remain at roughly the same height while in use.
If maps are not building the way you expect, make sure your Rplidar is secure and at roughly the same height throughout the run.

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](../../appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
