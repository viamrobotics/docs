---
title: "Use Object Detection to Turn Your Lights On"
linkTitle: "Turn on Lights with Object Detection"
weight: 49
type: "docs"
tags: ["camera", "vision", "detector", "python"]
description: "How to turn a light on when your webcam sees a person."
# Author: Hazal Mestci
---

In this tutorial, we will show you how to build your very own object detection robot using Viam, your computer with a webcam, a [Kasa Smart Plug](https://www.kasasmart.com/us/products/smart-plugs), and a desk lamp.
This robot will turn the lights on or off when it detects a person in front of it.
You can turn it into a night light for reading books, a security robot that alerts you when a person is close by, or a bathroom light that only activates when people enter; the opportunities are endless.

This project is a great place to start if you are new to building robots, and have a smart plug laying around.

<!-- insert GIF -->

## Hardware requirements

The following hardware is used in this tutorial:

- Computer with a webcam
  - This tutorial uses a MacBook Pro but any computer running macOS or 64-bit Linux will work
- Mobile phone (to download the Kasa Smart app)
- [Kasa Smart Wi-Fi Plug Mini](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-mini)
- [Kasa Smart Light Bulb](https://www.kasasmart.com/us/products/smart-lighting/kasa-smart-light-bulb-multicolor-kl125)
- [Table Lamp Base](https://www.amazon.com/gp/product/B08KZNZVY7/ref=ppx_yo_dt_b_asin_title_o02_s00?) or similar

## Software requirements

The following software is used in this tutorial:

- [Python3](https://www.python.org/downloads/)
- [`viam-server`](/installation/install/)
- [Viam Python SDK](https://python.viam.dev/)
- [Project repo on GitHub](https://github.com/viam-labs/devrel-demos/tree/main/Light%20up%20bot)

## Prerequisites

Make sure you have a recent version of Python installed on your computer by running

```bash
python --version
```

If the output is Python 3.9.0 or later, you should be fine for this tutorial.
If not, [download a newer version here](https://www.python.org/downloads/).

The Viam Python SDK (software development kit) lets you control your robot by writing custom scripts in the Python programming language.
Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).

Now you are ready to make your robot!

## Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and make or log in to your account.

Create a new robot.

Go to the **SETUP** tab of your new robot's page.
Select the correct **Mode** (Linux or Mac) and (if you're on Linux) **Architecture** for your computer.
Most Linux desktops and laptops use **X86_64** architecture.

Follow the steps on this tab to install `viam-server` on your computer.

## Configure object detection

On your new robot's page, go to the **CONFIG** tab.

![The CONFIG tab in Builder mode on the Viam app.](../img/light-up/config-tab.png)

On the **CONFIG** tab, create a new component:

- **Name**: `my-camera`
- **Type**: `camera`
- **Model**: `webcam`

Click **Create Component** to add the camera.

Click the **Video Path** box to reveal a drop-down populated with camera paths that have been identified on your machine.
Select the path to the camera you want to use.
Often on Linux systems, this is `video0` or `video1`.
On Mac, this is often a long string of letters and numbers.

Click **Save Config** in the bottom left corner of the screen.

Navigate to the **CONTROL** tab where you can see your camera working.

<!-- Insert GIF -->

## Set up the Kasa Smart Plug

Plug your smart plug into any power outlet and turn it on by pressing the white button on the smart plug.
To connect the plug to your wifi, download the Kasa Smart app from the [App Store](https://apps.apple.com/us/app/kasa-smart/id1034035493) or [Google Play](https://play.google.com/store/apps/details?id=com.tplink.kasa_android&gl=US) to your mobile phone.
When you first open the app, you will be prompted to create an account.
As you do this, you will receive an email with subject line "TP-Link ID: Activation Required" to complete your account registration.

Next, follow the steps in Kasa's [How to set up my TP-Link Smart Plug Switch via Kasa guide](https://www.tp-link.com/us/support/faq/946/) to add your device and connect it to your wifi.
Once it is connected, you will no longer need to use the mobile app.

Next, open a terminal on your computer and run the following command to download the [smart plug Python API](https://github.com/python-kasa/python-kasa):

```bash
pip3 install python-kasa
```

Next, run the following command to return information about your smart device:

```bash
kasa discover
```

You should see this command output something like this:

![Terminal output with information about the smart plug including the host, device state (on), timestamp, hardware and software versions, MAC address, location (latitude and longitute), whether the LED is currently on, and the timestamp of when it last turned on. There is also a list of modules (schedule, usage, antitheft, time and cloud).](../img/light-up/kasa-discover-output.png)

Copy the host address (for example, 10.1.11.221).
You will need to include it in your Python code in a later step.

## Write Python code to control your object detection robot

Navigate to the **CODE SAMPLE** tab on the Viam app.
Make sure **Python** is selected in the **Language** selector.

Click the **COPY CODE** button.
Paste the code into a new Python file on your computer.
This code connects your script to your robot.

Now you are ready to write the code to turn your smart plug on and off based on camera readings.
You will use a [TFLite](https://www.tensorflow.org/lite) model to detect specific objects, and a corresponding text that holds class labels for your TFLite model.
For more information on the Vision Service, check out our [documentation](/services/vision/).

In your Python code, as you set up the vision service parameters, you will need to change the `model_path` to where your TFLite package lives, and the `label_path` to where your text file lives.
You can download them from [here](https://github.com/viam-labs/devrel-demos/tree/main/Light%20up%20bot).

You will also generate a person detector function within your code, to detect a person and trigger the camera.

{{% alert title="Info" color= "info" %}}

Technically, you can detect any object that is listed in the <file>labels.txt</file> (such as a dog or a toilet) but for this tutorial, we are detecting a person.

To detect something else with the camera, just change the string "person" to a different item in the <file>label.txt</file> file.

```python
               if d.class_name.lower() == "person":
                   print("This is a person!")
                   found = True
```

{{% /alert %}}

The sample code below specifies the file locations of the model and labels, which object you are detecting, and it configures the detector.

```python
    vision = VisionServiceClient.from_robot(robot)
    params = {"model_path": "./effdet0.tflite", "label_path": "./labels.txt", "num_threads": 1}
    personDet = VisModelConfig(name="person_detector", type=VisModelType("tflite_detector"), parameters=params)
    await vision.add_detector(personDet)
    names = await vision.get_detector_names()
    print(names)
```
