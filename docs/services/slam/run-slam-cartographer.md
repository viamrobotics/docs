---
title: "Run Cartographer SLAM on your Robot with a Rplidar"
linkTitle: "Run Cartographer SLAM on your Robot with a Rplidar"
weight: 50
type: "docs"
description: "Instructions to run Cartographer SLAM with a Rplidar or sample dataset."
tags: ["slam", "camera", "services", "lidar"]
# SMEs: Kat
---

{{% alert title="Note" color="note" %}}
The {{< glossary_tooltip term_id="slam" >}} Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Introduction

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your robot to create a map of its surroundings and find its location within that map.

These instructions show you how to run [Cartographer](https://github.com/cartographer-project), software that provides real-time SLAM, as a service on your robot.

You have two options:

1. Run Cartographer SLAM in live mode with a [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.
2. Run Cartographer SLAM in offline mode with Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip) or with data you've collected.

You'll need at least the following hardware:

- A Linux or MacOS machine with `viam-server` and `Cartographer` installed.
- (Optional, required for Live Mode) A [Rplidar A1](https://www.slamtec.com/en/Lidar/A1) or [Rplidar A3](https://www.slamtec.com/en/Lidar/A3) LIDAR scanning device.

For more information on how to install `viam-server` and set up your machine on the [Viam app](https://app.viam.com), see [Install viam-server](/installation#install-viam-server).

### Install the Cartographer Binary

Install Cartographer by running the appropriate command for your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install carto-grpc-server
```

{{% /tab %}}
{{< /tabs >}}

## Run Cartographer in Live Mode with a Rplidar

### Add your Rdiplar as a Modular Component

Follow [these instructions](../../../program/extend/modular-resources/add-rplidar-module/) to add your Rplidar device as a modular component of your robot.

### Add the Cartographer Service

Now that you've added your Rplidar device as a modular component of your robot, you can edit your robot's configuration along with the Rplidar module to add Cartographer as a `SLAM` service with the attribute `use_live_data: true` [specifying live mode](../#general-attributes).

1. Go to your robot's page on the [Viam app](https://app.viam.com/).
2. On the **CONFIG** tab, click the **SERVICES** sub tab.
3. Create a service with type `slam`, model `cartographer`, and a name of your choice.
4. Paste the following into the **Attributes** field of your new service:

    ```json
    {
      "config_params": {
        "min_range": "0.3",
        "max_range": "12",
        "mode": "2d"
      },
      "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
      "map_rate_sec": 60,
      "data_rate_msec": 200,
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
        "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
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

5. Now, change the `data_dir` attribute on line 8 to point to to a directory on your machine that you want to store your SLAM data in.
See [SLAM: Data Directory](../#data_dir-data-directory) for more information and notes on structure.

    You can edit `"/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>"` directly, changing `<YOUR_USERNAME>` to match your username on your computer and `<CARTOGRAPHER_DIR>` to `cartographer_dir`.

    This tells the service to create a directory named `cartographer_dir` within your home directory, and to save all data and maps to that location.

    {{% alert title="Note" color="note" %}}

If you are using a Raspberry Pi as your machine, you must `ssh` into your Pi to complete this step.

```sh {id="terminal-prompt" class="command-line" data-prompt="YOUR_USERNAME@YOUR_RPI_NAME:~ $" data-output="2"}
pwd
/home/YOUR_USERNAME
```

    {{% /alert %}}

6. Save the config.

At this point, your complete configuration should look like:

  {{< tabs >}}
  {{% tab name="Linux" %}}

  ```json
  {
    "modules": [
      {
        "name": "rplidar_module",
        "executable_path": "/usr/local/bin/rplidar-module"
      }
    ],
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "name": "rplidar"
      }
    ],
    "services": [
      {
        "type": "slam",
        "attributes": {
          "config_params": {
            "min_range": "0.3",
            "max_range": "12",
            "mode": "2d"
          },
          "data_rate_msec": 200,
          "delete_processed_data": false,
          "use_live_data": true,
          "sensors": [
            "rplidar"
          ],
          "port": "localhost:8083",
          "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
          "map_rate_sec": 60
        },
        "model": "cartographer",
        "name": "run-slam"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{% tab name="MacOS" %}}

  ``` json
  {
    "modules": [
      {
        "executable_path": "/usr/local/bin/rplidar-module",
        "name": "rplidar_module"
      }
    ],
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
    "services": [
      {
        "attributes": {
          "map_rate_sec": 60,
          "data_rate_msec": 200,
          "use_live_data": true,
          "sensors": [
            "rplidar"
          ],
          "config_params": {
            "mode": "2d",
            "min_range": "0.3",
            "max_range": "12"
          },
          "port": "localhost:8083",
          "data_dir": "/Users/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>",
          "delete_processed_data": false
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

1. Head over to the **CONTROL** tab and click on the drop-down menu matching the `name` of the service you created.
2. Change the **Refresh frequency** to your desired frequency, move the Rplidar device around slowly, and watch a map start to appear.

## Run Cartographer in Offline Mode with a Dataset

### Find a Dataset for Cartographer to Use

In offline mode SLAM uses an existing dataset to create a map.
The path to this dataset is specified by the SLAM service's `data_dir` configuration attribute.
The directory at the `data_dir` path should have a folder inside it called `data`, which is where this data should be stored.

See [SLAM: Data Directory](../#data_dir-data-directory) for more information and notes on structure.

- If your folder `data_dir/data` is already populated from running SLAM in live mode, no change is needed.
- If you wish to use another dataset for SLAM, you can make it the folder `data_dir/data`.

If you don't already have a dataset in `data_dir/data` from running SLAM in live mode, download Viam's [lab dataset](https://storage.googleapis.com/viam-labs-datasets/viam-old-office-small-pcd.zip) and follow these instructions:

1. Copy the zipped file to the machine running `viam-server` and unzip it.

    For example:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    scp ~/Downloads/viam-old-office-small-pcd.zip YOUR_USERNAME@MACHINE.local:~/.
    unzip viam-old-office-small-pcd.zip
    ```

2. Rename the unzipped folder to `data` and place inside of the [data directory](../#data_dir-data-directory).

    For example:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    cd /home/YOUR_USERNAME/cartographer_dir
    mv ~/Downloads/viam-old-office-small-pcd data/
    ```

### Add the Cartographer Service

Now that you have chosen a dataset that the service can use to build its map, you can edit your robot's configuration to add Cartographer as a `SLAM` service with the attribute `use_live_data: false` [specifying offline mode](../#general-attributes).

1. Go to your robot's page on [the Viam app](https://app.viam.com/robots).
2. In the **CONFIG** tab, select the **Raw JSON** mode.
3. Copy the following JSON code:

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
            "data_dir": "/home/<YOUR_USERNAME>/<CARTOGRAPHER_DIR>/data",
            "map_rate_sec": 60,
            "data_rate_msec": 200,
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

4. Change `data_dir` to match the path to your dataset on your machine.
See [SLAM: Data Directory](../#data_dir-data-directory) for more information and notes on structure.
1. Save the config.
2. Navigate to the **CONTROL** tab and click on the drop-down menu with the name of the service you created.
3. Refresh until the map appears, or change the **Refresh frequency** to your desired frequency.

{{% alert title="Tip" color="tip" %}}
To find your machine's home directory path, run the `pwd` command in your terminal.
Make sure to do this while your terminal is at the home directory level (denoted by `~`).
{{% /alert %}}

## Troubleshooting

### Tip: Lidar Mounting for the Viam Rover

If you have a Viam Rover and need a mount for your RPLidar, you can 3D print an adapter plate.
The STL file for an adapter plate is available on [GitHub](https://github.com/viamrobotics/VR1-22-A001/blob/master/CAD/RPIidar_adapter.STL).

### Issue: Maps JPEG not Appearing in UI

When generating a larger map, it can take a while for the Cartographer service to return the `JPEG` map.

Reducing the frequency the Cartographer service returns the map by adjusting **Refresh frequency** should help the JPEG visualization to appear consistently.

### Issue: Maps not Appearing as Expected

Only `2D SLAM` is currently implemented for Cartographer.
Because of this, Cartographer assumes your Rplidar will remain at roughly the same height while in use.
If maps are not building the way you expect, make sure your Rplidar is secure and at roughly the same height throughout the run.

### Issue: Offline mode produces an error after restart

If there is a saved map in `data_dir/map` and saved data in `data_dir/data` from a previous run, then offline mode may error at startup, since the data has already been incorporated into the map.
If that occurs, you can clear `data_dir/map` to rerun the dataset in offline mode.

## Next Steps

Try adjusting Cartographer's [config parameters](../#cartographer-config_params) to fine-tune the SLAM algorithm.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
