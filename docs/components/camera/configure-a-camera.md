---
title: "How to Configure a Camera"
linkTitle: "Configure a Camera"
weight: 12
type: "docs"
draft: false
description: "Instructions for configuring a webcam."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

## Introduction

[Cameras](/components/camera/) are a key component of many applications, such as computer vision and SLAM.
This tutorial shows you how to configure a webcam (sometimes called a USB camera) as a component of your robot.

## Connect and configure a webcam

First, you will need to add a webcam to your configuration. In your web browser, navigate to the robot you set up on the Viam app ([https://app.viam.com](https://app.viam.com)).

Configure the webcam by clicking on the **CONFIG** tab. Go to the Builder, and create a component with **Name** "color" of **Type** "camera" and **Model** "webcam".

<img src="../img/configure-a-camera/01_camera_tutorial_builder.png" alt="Create component builder" width="700"><br>

Once you click **Create Component**, you'll see a view on the component that looks like this:

<img src="../img/configure-a-camera/02_camera_tutorial_config.png" alt="Component attributes JSON" width="700"><br>

Manually add the camera path to the camera's attributes and save the config. A good bet is often `video0`:

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "video_path": "video0"
}
```

If `video0` does not work for you, you can find another potential `video_path` by typing the following in your terminal:

```bash
v4l2-ctl --list-devices
```

The output for a webcam may look like this example, in which case `video1` might be the correct path to input for `video_path`:

```bash
C270 HD WEBCAM (usb-0000:01:00.0-1.2):
 /dev/video0
 /dev/video1
 /dev/media4
```

Once your camera is connected, go to the **CONTROL** tab, and click on the "color" dropdown menu. Toggle "View Camera" and make sure you can see the live video feed from your camera.

<img src="../img/configure-a-camera/03_camera_tutorial_image.png" alt="Camera view inside Viam app" width="700px"><br>

## General camera troubleshooting

### Issue: I can't see the live video feed

If you're working on a Pi, `ssh` into it, then in the terminal, restart the `viam-server` by running:

```bash
sudo systemctl restart viam-server
```

If this doesn't work, you can reboot your Pi by running:

```bash
sudo reboot
```

or by powering it off and on again.

### Issue: The "Export Screenshot" button doesn't work

1. In the **CONTROL** tab, pick "Manual Refresh" under the "Refresh frequency".
2. Click the refresh button when you're ready to take an image of the checkerboard.
3. Right click on the image, and choose "Save Image As..." to save the image.

<br>
<img src="../img/configure-a-camera/05_camera_tutorial_manual_img_save.png" alt="Save image as menu" width="700"><br>

## Additional troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
