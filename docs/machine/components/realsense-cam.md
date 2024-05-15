---
title: "Intel RealSense Camera"
linkTitle: "RealSense Camera"
weight: 45
type: "docs"
draft: true
description: "Adding an External Intel Realsense Camera to Viam."
tags: ["camera", "realsense camera", "components"]
aliases:
  - "/machine/components/realsense-cam/"
---

There are two ways to add your intel RealSense camera to Viam.
You can either use a {{< glossary_tooltip term_id="grpc" text="gRPC" >}} server or an HTTP server.

You can find the source code for these servers in the [Viam Robotics repo](https://github.com/viamrobotics/camera-servers).

## Using the gRPC server

Use the gRPC server if you want 2D image streams and also want the 3D point clouds from the Intel RealSense camera.
They will show up as 3 separate cameras.

### Download the Intel RealSense gRPC camera server

On your Raspberry Pi, download the following server for your intel camera

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/intelgrpcserver https://storage.googleapis.com/packages.viam.com/apps/camera-servers/intelrealgrpcserver-latest-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/intelgrpcserver
```

### Configure the server to run on machine start-up

On the [Viam app](https://app.viam.com), click **CONFIGURE** and then access the **Processes** tab. Add the following configuration:

```json
[
  {
    "id": "intel",
    "log": true,
    "name": "/usr/local/bin/intelgrpcserver"
  }
]
```

This configures the gRPC server to run on port 8085 of your Pi.

On the **CONFIGURE** tab, click **Remotes**, and then add the following configuration:

```json
[
  {
    "name": "intel",
    "address": "ip-address-of-your-pi:8085",
    "insecure": true
  }
]
```

This adds the two cameras to your machine.
They will have the names `intel:color` and `intel:depth`.

### Create a camera to display point clouds

Click **Components** on the **CONFIGURE** tab.
Now, add the `align_color_depth` camera model.
Click the **{}** (Switch to Advanced) button in the top right of the component panel to edit the component's attributes directly with JSON.

Enter the necessary JSON configuration for your camera:

```json
{
    "homography": {
        "transform": [ // the color and depth image are already aligned
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ],
        "depth_to_color": false,
        "rotate_depth_degs": 0
    },
    "stream": "color",
    "width_px": 1280,
    "height_px": 720,
    // you can get intrinsics by calling GetProperties on the intel gRPC camera server, too
    "intrinsic_parameters": {
        "height_px": 720,
        "width_px": 1280,
        "ppx": 648.1280,
        "ppy": 367.736,
        "fx": 900.538,
        "fy": 900.818
    },
    "color_camera_name": "intel:color",
    "depth_camera_name": "intel:depth"

    "depends_on": [
        "intel:color",
        "intel:depth"
    ]
}
```

In the **CONTROL** tab, you can now see both the individual 2D camera streams, as well as the point cloud camera of the combined color and depth image that you created with `join_color_depth`.

## Using the HTTP server

Use this method if you don’t care about the individual 2D image streams and only need the 3D point clouds from the Intel RealSense camera.

### Download the Intel RealSense HTTP camera server

On your Raspberry Pi, download the following server for your Intel RealSense camera:

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/intelrealserver https://storage.googleapis.com/packages.viam.com/apps/camera-servers/intelrealserver-latest-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/intelrealserver
```

### Configure the server to run on machine start-up

On the [Viam app](https://app.viam.com), click **CONFIGURE** and then click **Processes**.
Enter the following configuration:

```json
[
  {
    "id": "intel",
    "log": true,
    "name": "/usr/local/bin/intelrealserver"
  }
]
```

This configures the HTTP server to run on port 8181 of your Pi. You can access the server at [http://your-raspi-address:8181/](http://your-raspi-address:8181/) to view a slowly refreshing image from the color camera.

The endpoints that it creates are:

- [http://your-raspi-address:8181/pic.jpg](http://your-raspi-address:8181/pic.jpg) - a jpeg image from the color camera
- [http://your-raspi-address:8181/pic.png](http://your-raspi-address:8181/pic.png) - a png image from the color camera
- [http://your-raspi-address:8181/depth.png](http://your-raspi-address:8181/depth.png) - a png image from the depth camera

## Create a camera to display point clouds

Click **CONFIGURE** and then click **Components**.

<!-- dual_stream no longer exists -->

Enter the following camera model: "dual_stream"

```json
{
  "intrinsic_parameters": {
    "fx": 900.538,
    "fy": 900.818,
    "height_px": 720,
    "ppx": 648.934,
    "ppy": 367.736,
    "width_px": 1280
  },
  "color_url": "http://127.0.0.1:8181/pic.png",
  "depth_url": "http://127.0.0.1:8181/depth.png",
  "stream": "color"
}
```

This configures one camera that shows both, the color stream as a 2D image, and the 3D point cloud.
To display the depth image as the 2D image, you can change the stream parameter to "depth."
