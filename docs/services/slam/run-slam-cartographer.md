---
title: "Run Cartographer SLAM on your Robot with a Rplidar"
linkTitle: "Run Cartographer SLAM on your Robot with a Rplidar"
weight: 50
type: "docs"
draft: false
description: "Instructions to run Cartographer SLAM with a Rplidar or sample dataset."
tags: ["slam", "camera", "services", "lidar"]
# SMEs: Kat
---

{{% alert title="Note" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[Simultaneous Localization And Mapping (SLAM)](../../slam/) allows your robot to create a map of its surroundings and find its location within that map.

This tutorial shows you how to run [Cartographer](https://github.com/cartographer-project), software that provides real-time SLAM, as a service on your robot.

You have two options:

1. Run Cartographer SLAM in live mode with a [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.
2. Run Cartographer SLAM in offline mode with Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip) or with data you've collected.

## Requirements

* A Linux or MacOS machine with `viam-server` and `Cartographer` installed.
* [optionally] A [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.

For more information on how to install `viam-server` and set up your machine on the [Viam app](https://app.viam.com), see [Install viam-server](/installation/install/).

### Install the Cartographer Binary

Install Cartographer with one of these commands:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

``` bash
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

``` bash
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="MacOS" %}}

``` bash
brew tap viamrobotics/brews && brew install carto-grpc-server
```

{{% /tab %}}
{{< /tabs >}}

## Run Cartographer in Live Mode with an Rplidar

Run Cartographer as a live SLAM Service with a Rplidar.

### Configuration with Viam

Configure your robot to run Cartographer with a Rplidar in two steps:

1. Add your Rplidar as a modular component.
2. Add Cartographer as a SLAM Service in live mode.

#### Step 1: Add your Rdiplar as a Modular Component

First, install the Rplidar Module:

{{< tabs >}}
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
{{% tab name="MacOS" %}}

```bash
brew tap viamrobotics/brews && brew install rplidar-module
```

{{% /tab %}}
{{< /tabs >}}

Now, add the Rplidar as a modular component of your robot in the [Viam app](https://app.viam.com/):

* Physically connect the Rplidar to your machine.
* Go to your robot's page on the [Viam app](https://app.viam.com/).
* In the **CONFIG** tab, select **Raw JSON** mode.
* Copy the following configuration code for your Rplidar device.
  Paste it into the **Raw JSON** block:

  {{< tabs >}}
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
  {{% tab name="MacOS" %}}

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
  {{< /tabs >}}

* Save the config.
* Check the **LOGS** of your robot in the Viam app to make sure your Rplidar has connected and no errors are being raised.

#### Step 2: Add Cartographer as a SLAM Service in Live Mode

Now that you've added your Rplidar device as a modular component of your robot, you can add Cartographer to your robot as a SLAM service.

* Go to your robot's page on the [Viam app](https://app.viam.com/).
* On the **CONFIG** tab, click the **SERVICES** sub tab.
* Create a service with type `slam`, a name (example: `run-slam`) and a model (`cartographer`).
* Paste the following into the **Attributes** field of your new service:

```json
{
  "config_params": {
    "min_range": "0.3",
    "max_range": "12",
    "mode": "2d"
  },
  "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
  "map_rate_sec": 60,
  "data_rate_ms": 200,
  "delete_processed_data": false,
  "use_live_data": true,
  "sensors": ["rplidar"]
}
```

{{%expand "Click here if you prefer to use Raw JSON to build your service" %}}
In the **CONFIG** tab, select the **Raw JSON** mode, then copy/paste the following configuration:

```json
  "services": [
    {
      "attributes": {
        "config_params": {
          "min_range": "0.3",
          "max_range": "12",
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
      "name": "test",
      "type": "slam"
    }
  ]
```

{{% /expand %}}
</br>

* Now, change the `"data_dir":` attribute on line 8.
  
  Edit `YOUR_USERNAME` in `"/home/YOUR_USERNAME/cartographer_dir"` to match your username on your computer.
  * This tells the service to create a directory named `cartographer_dir` within your home directory, and to save all data and maps to that location.
  * To find your machine's home directory path, run `pwd` in your terminal.
    Make sure to do this while your terminal is at the home directory level (denoted by `~`).

{{% alert title="Note" color="note" %}}
If you are using a Raspberry Pi as your machine, you must `ssh` into your Pi to complete this step.

```bash
YOUR_USERNAME@YOUR_RPI_NAME:~ $ pwd
/home/YOUR_USERNAME
```

{{% /alert %}}

<br>

* Save the config.

At this point, your complete configuration should look like:

  {{< tabs >}}
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
        "name": "rplidar_module"
      }
    ],
    "services": [
      {
        "attributes": {
          "config_params": {
            "min_range": "0.3",
            "max_range": "12",
            "mode": "2d"
          },
          "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
          "map_rate_sec": 60,
          "data_rate_ms": 200,
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
  {{% tab name="MacOS" %}}

  ``` json
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
            "mode": "2d"
          },
          "data_dir": "/home/YOUR_USERNAME/cartographer_dir",
          "map_rate_sec": 60,
          "data_rate_ms": 200,
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

* Head over to the **CONTROL** tab and click on the drop-down menu for the service you created (example: `run-slam`).
* Change the **Refresh frequency** to your desired frequency, move the Rplidar device around slowly, and watch a map start to appear.

## Run Cartographer in Offline Mode with a Dataset

Run Cartographer in offline mode using one of your previously saved LIDAR datasets or Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip).

### Configuration

Configure your robot to run Cartographer in offline mode in two steps:

1. Find an existing dataset to run Cartographer with.
2. Add Cartographer as a SLAM Service in offline mode.

#### Step 1: Find a Dataset for Cartographer to Use

In offline mode SLAM uses an existing dataset to create a map.

If you already have a dataset inside of a `data` folder in `/cartographer_dir` from running SLAM in live mode, no change to the `data_dir` attribute of your Cartographer service is needed.

If you wish to use another dataset for SLAM, you can either move it to inside of the `cartographer_dir` directory and rename to `data`, or put the path to that dataset on your machine as your `data_dir` configuration attribute.

Make sure the folder holding the data is named `data`, and that it is structured as follows:

<pre>
.
└──\(The Directory Defined in Config as `data_dir`)
    ├── data
    ├── map
    └── config
</pre>

If you don't already have a dataset in `data_dir/data` from running SLAM in live mode, download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip) and follow these instructions:

1. Copy the zipped file to the machine running `viam-server` and unzip it.

    For example:

    ```bash
    scp ~/Downloads/viam-old-office-small-pcd.zip YOUR_USERNAME@MACHINE.local:~/.
    unzip viam-old-office-small-pcd.zip
    ```

2. Rename the unzipped folder to `data` and place it in the cartographer_dir directory.

    For example:

    ``` bash
    cd /home/YOUR_USERNAME/cartographer_dir
    mv ~/Downloads/viam-old-office-small-pcd data/
    ```

#### Step 2: Add Cartographer as a SLAM Service in Offline Mode

Now that you have chosen a dataset that the service can use to build its map, you can set up Cartographer to run on your robot without a LIDAR scanning device.

To enable offline mode, set the `use_live_data` flag to `false`.
This tells the service to use only data found within the `data_dir` directory specified in your config while running SLAM.

* Go to your robot's page on [the Viam app](https://app.viam.com/robots).
* In the **CONFIG** tab, select the **Raw JSON** mode.
* Copy the following JSON code:

    ```json
    {
      "services": [
        {
          "attributes": {
            "config_params": {
              "min_range": "0.3",
              "max_range": "12",
              "mode": "2d"
            },
            "data_dir": "/home/YOUR_USERNAME/cartographer_dir/data",
            "map_rate_sec": 60,
            "data_rate_ms": 200,
            "delete_processed_data": false,
            "use_live_data": false,
            "sensors": []
          },
          "model": "cartographer",
          "name": "run-slam-offline",
          "type": "slam"
        }
      ]
    }
    ```

    Paste it into the **Raw JSON** box.

* Now, change the `"data_dir":` attribute on line 8.
  * Edit `"/home/YOUR_USERNAME/viam-old-office-small-pcd"` to match the path to your existing dataset on your machine.
  This tells the service to read from the directory located at this path and to save all data and maps to that location.
  * To find your machine's home directory path, run the `pwd` command in your terminal.
    Make sure to do this while your terminal is at the home directory level (denoted by `~`).
<br><br>

* Save the config.
* Head over to the **CONTROL** tab and click on the drop-down menu with the name of the service you created (example: `run-slam-offline`).
* Refresh until the map appears, or change the **Refresh frequency** to your desired frequency.

## Troubleshooting

### Issue: Maps JPEG not Appearing in UI

When generating a larger map, it can take a while for the Cartographer service to return the `JPEG` map.

Reducing the frequency the Cartographer service returns the map by adjusting **Refresh frequency** should help the JPEG visualization to appear consistently.

### Issue: Maps not Appearing as Expected

Only `2D SLAM` is currently implemented for Cartographer.
Because of this, Cartographer assumes your Rplidar will remain at roughly the same height while in use.
If maps are not building the way you expect, make sure your Rplidar is secure and at roughly the same height throughout the run.

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
