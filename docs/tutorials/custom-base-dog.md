---
title: "Control a Robot Dog with a Custom Viam Base Component"
linkTitle: "Custom Quadruped Base"
weight: 55
type: "docs"
description: "How to integrate a custom base component with the Viam Python SDK."
# SMEs: James Otting, Eric Daniels
# Author: Jessamy Taylor
---

The [base component type](/docs/components/base/) is useful for controlling mobile robots because it gives users intuitive steering controls to use in code as well as from the [Viam app](https://docs.viam.com/) remote control interface.

Viam natively supports a wheeled base model, but what if you have a quadruped or other form of rover that isn't compatible with the wheeled model?
Not to worry!
You have two great options:

1. Use Viam's Go SDK to [create a custom component as a modular resource](/program/extend/modular-resources/).
2. Use another Viam SDK (for example, the Python SDK) to [create a custom resource server](/program/extend/sdk-as-server/).

This tutorial is an example of option two, using [this robot dog kit and its open source code](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi) as an example.

<img src="../img/custom-base-dog/base-control-dog.gif" style="float:left;margin-right:12px" alt="A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the robot's Control tab on the Viam app open in a browser window." width="400" />

By the end of the tutorial, you will be able to drive this dog around using the Viam base methods: `MoveStraight`, `Spin`, `SetPower`, `SetVelocity`, and `Stop`.
You will also be able to use the **CONTROL** tab in the Viam app to remotely drive the dog around using WASD keys on your keyboard while viewing the camera feed.
You’ll learn to implement a custom component type in Viam, and you’ll be equipped to implement other sorts of custom components in the future for whatever robots you dream up.

## Hardware requirements

- [Freenove Robot Dog Kit for Raspberry Pi](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi)
  - Currently (24 January 2023) [available on Amazon](https://www.amazon.com/gp/product/B08C254F73/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
  - Significant assembly is required.
  Follow Freenove hardware assembly instructions before starting this tutorial.
- Raspberry Pi 4B

## Raspberry Pi setup

Freenove provides a lot of information about how to set up and use a Raspberry Pi in chapters 0 and 1 of their tutorial, some of which overlaps with Viam setup guides, so to avoid confusion, here’s all you need to do for the purposes of this tutorial:

Follow the steps in our [Raspberry Pi Setup Guide](/installation/rpi-setup/) to install Raspberry Pi OS Lite (64 bit).

{{% alert title=Note color="note" %}}
If you choose to install the full Raspberry Pi OS (64 bit) including the desktop environment and recommended software (as Freenove instructs in Chapter 0 of their tutorial), that will also work; set up viam-server in the same way on the **SETUP** tab once you have the Pi OS installed.
{{% /alert %}}

Then [install viam-server and connect your robot to the Viam app](../installation/install/).

SSH into the Pi to complete the following steps.

Install pip and then git:

```bash
sudo apt install pip
sudo apt install git
```

Install the Freenove robot dog code by running the following command from the home directory of the Pi:

```bash
git clone https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi
```

Check which version of Python you have installed on the Pi:

```bash
python --version
```

If it isn’t Python 3.8 or later, be sure to install an updated version of Python.

Install the [Viam Python SDK](https://python.viam.dev/):

```bash
pip install viam-sdk
```

Enable I<sup>2</sup>C per [the instructions in the Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/#enabling-specific-communication-protocols-on-the-raspberry-pi).

Alter the I<sup>2</sup>C baud rate according to [Chapter 1, Step 2 in the Freenove instructions](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf) (page 40 as of 24 January 2023).

Install smbus so that the servo code works:

```bash
sudo apt-get install python3-smbus
```

Follow Chapter 1, Step 3 (page 42 as of 24 January 2023) of the Freenove tutorial to complete the software installation:

```bash
cd ~/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code
sudo python setup.py
```

Restart the Raspberry Pi:

```bash
sudo reboot
```

## Hardware setup

The Freenove hardware instructions are comprehensive. Follow their assembly instructions, including servo setup (i.e. all of Chapters 2 and 3, and the section of Chapter 4 about calibration) before proceeding.

## Create a connection test file

In a convenient directory on your development machine (desktop or laptop), create a Python file and open it in your favorite IDE.
We named ours "dog_test.py" and opened it in Visual Studio Code.

Paste the following code snippet into the file you created:

```python
# dog_test.py is for testing the connection

import socket, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("PASTE IP ADDRESS HERE", 5001))

cmd = "CMD_MOVE_FORWARD#8"
s.send(cmd.encode("utf-8"))
time.sleep(8)
cmd = "CMD_MOVE_STOP"
s.send(cmd.encode("utf-8"))
cmd = "CMD_RELAX"
s.send(cmd.encode("utf-8"))
```

Save the file.

### Find IP address

Go to the robot page (on the Viam app) for your robot dog that you set up when installing viam-server on the Pi.

In the banner towards the top of the page, the IP address of the robot dog Pi is displayed under **ips**.
Copy this number (usually a string of four numbers separated by periods) into the `dog_test.py` file in place of `PASTE IP ADDRESS HERE`.
Save the file.
