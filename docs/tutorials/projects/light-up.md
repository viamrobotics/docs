---
title: "Use Object Detection to Turn Your Lights On"
linkTitle: "Turn on Lights with Object Detection"
weight: 49
type: "docs"
description: "How to turn a light on when your webcam sees a person."
webmSrc: "/tutorials/img/light-up/light-up.webm"
mp4Src: "/tutorials/img/light-up/light-up.mp4"
videoAlt: "A person sitting at a desk with a computer and light bulb set up in front of her. As she leaves the light turns off, and as she enters the frame, the light turns back on."
tags: ["camera", "vision", "detector", "python"]
# Author: Hazal Mestci
---

This tutorial uses the Viam [Vision Service](/services/vision/) with your computer's built-in webcam to detect the presence of a person and turn on a lamp when you sit down at your desk.

You can turn it into a night light for reading books, a security robot that alerts you when a person is close by, or a bathroom light that only activates when people enter; the opportunities are endless.

This project is a great place to start if you are new to building robots, because the only hardware it requires in addition to your computer is a [smart plug](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-mini) or smart bulb.

{{<gif webm_src="../../img/light-up/light-up.webm" mp4_src="../../img/light-up/light-up.mp4" alt="The project working: a person sitting at a desk with a computer and light bulb set up in front of her. As she leaves the light turns off, and as she enters the frame, the light turns back on.">}}

## Hardware requirements

You need the following hardware for this tutorial:

- Computer with a webcam
  - This tutorial uses a MacBook Pro but any computer running macOS or 64-bit Linux will work
- Mobile phone (to download the Kasa Smart app)
- Either a smart plug or bulb:
  - [Kasa Smart Wi-Fi Plug Mini](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-mini)
    - (This is what we used for this tutorial.)
  - [Kasa Smart Light Bulb](https://www.kasasmart.com/us/products/smart-lighting/kasa-smart-light-bulb-multicolor-kl125)
- [Table Lamp Base](https://www.amazon.com/gp/product/B08KZNZVY7/ref=ppx_yo_dt_b_asin_title_o02_s00?) or similar

## Software requirements

You will use the following software in this tutorial:

- [Python 3.8 or newer](https://www.python.org/downloads/)
- [`viam-server`](/installation#install-viam-server)
- [Viam Python SDK](https://python.viam.dev/)
  - The Viam Python SDK (software development kit) lets you control your Viam-powered robot by writing custom scripts in the Python programming language.
  Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).
- [Project repo on GitHub](https://github.com/viam-labs/devrel-demos/tree/main/Light%20up%20bot)

## Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new robot.

Go to the **setup** tab of your new robot's page and follow the steps to install `viam-server` on your computer.

## Configure the camera component

On your new robot's page, go to the **config** tab.

![The CONFIG tab in Builder mode on the Viam app.](../../img/light-up/config-tab.png)

On the **config** tab, create a new component:

- **Name**: `my-camera`
- **Type**: `camera`
- **Model**: `webcam`

Click **Create Component** to add the camera.

Click the **Video Path** field to reveal a drop-down populated with camera paths that have been identified on your machine.

Select the path to the camera you want to use.
Often on Linux systems, this is `video0` or `video1`.
On Mac, this is often a long string of letters and numbers.

Click **Save Config** in the bottom left corner of the screen.

Navigate to the **control** tab where you can see your camera working.

{{< gif webm_src="../../img/light-up/control-panel.webm" mp4_src="../../img/light-up/control-panel.mp4" alt= "Opening the camera panel on the control tab, toggling the video feed on, and watching as a person wearing headphones waves at the camera." >}}

## Set up the Kasa Smart Plug

1. Plug your smart plug into any power outlet and turn it on by pressing the white button on the smart plug.
To connect the plug to your wifi, download the Kasa Smart app from the [App Store](https://apps.apple.com/us/app/kasa-smart/id1034035493) or [Google Play](https://play.google.com/store/apps/details?id=com.tplink.kasa_android) to your mobile phone.
When you first open the app, you will be prompted to create an account.
As you do this, you will receive an email with subject line "TP-Link ID: Activation Required" to complete your account registration.

2. Follow the steps in Kasa's [setup guide](https://www.tp-link.com/us/support/faq/946/) to add your device and connect it to your wifi.
Once it is connected, you will no longer need to use the mobile app.

3. Open a terminal on your computer and run the following command to install the [smart plug Python API](https://github.com/python-kasa/python-kasa):

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    pip3 install python-kasa
    ```

4. <a name=kasa ></a> Run the following command to return information about your smart device:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    kasa discover
    ```

    You should see this command output something like this:

    ![Terminal output with information about the smart plug including the host, device state (on), timestamp, hardware and software versions, MAC address, location (latitude and longitude), whether the LED is currently on, and the timestamp of when it last turned on. There is also a list of modules (schedule, usage, antitheft, time and cloud).](../../img/light-up/kasa-discover-output.png)

    Write down or save the host address (for example, `10.1.11.221`).
You will need to include it in your Python code in a later step.

## Write Python code to control your object detection robot

Now that you have your robot configured and your Kasa plug set up, you are ready to set up the code for the logic of the robot.
The files used in this section can all be found in [the GitHub repo for this project](https://github.com/viam-labs/devrel-demos/tree/main/Light%20up%20bot).

### Create the main script file

On your computer, navigate to the directory where you want to put the code for this project.
Create a file there called <file>lightupbot.py</file>.
This will be the main script for the robot.
Copy the entirety of [this file](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/lightupbot.py) and paste it into your <file>lightupbot.py</file> file.
Save <file>lightupbot.py</file>.

### Connect the code to the robot

You need to tell the code how to access your specific robot (which in this case represents your computer and its webcam).

1. Navigate to the **code sample** tab on the Viam app.
Make sure **Python** is selected in the **Language** selector.
2. In the code sample, find the `payload`, a long string of numbers and letters.
Copy it and paste it into line 13 of <file>lightupbot.py</file> in place of `ROBOT_SECRET`.
3. Find the robot address, of the form `robot-name-main.abc1ab123a1.viam.cloud`, and paste it into line 14 of <file>lightupbot.py</file> in place of `ROBOT_ADDRESS`.

You also need to tell the code how to access your smart plug.

1. Add the host address (for example, `10.1.11.221`) of your smart plug that you found in the [`kasa discover` step](#kasa) to line 55 of <file>lightupbot.py</file>.

### Set the model path and label path

You will use the [Vision Service](/services/vision/) to interpret what your camera sees.
You will configure the Vision Service to use a [TFLite](https://www.tensorflow.org/lite) model to detect specific objects, and a corresponding text file that holds class labels for your TFLite model.

1. Take a look at lines 42-48 in <file>lightupbot.py</file>.
These lines configure a Vision Service object detector to use the TFLite model and the list of labels:

```python
    vision = VisionServiceClient.from_robot(robot)
    params = {"model_path": "./effdet0.tflite", "label_path": "./labels.txt", "num_threads": 1}
    personDet = VisModelConfig(name="person_detector", type=VisModelType("tflite_detector"), parameters=params)
    await vision.add_detector(personDet)
    names = await vision.get_detector_names()
    print(names)
```

2. Download [<file>effdet0.tflite</file>](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/effdet0.tflite) and [<file>labels.txt</file>](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/labels.txt) to your project directory.
3. Line 44 of your <file>lightupbot.py</file> is where you specify the paths to these files.
If you put them in the same directory as <file>lightupbot.py</file>, you don't need to edit this line.
4. Save the file.

### Run the code

Now you are ready to test your robot!

From a command line on your computer, navigate to the project directory and run the code with this command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 lightupbot.py
```

If the camera detects a person, it will print to the terminal “This is a person!” and turn on the smart plug.
If it does not find a person, it will write “There’s nobody here” and will turn off the plug.

Try moving in and out of your webcam's field of view.
You will see your light turn on and off as the robot detects you!

Your terminal output should look like this as your project runs:

```sh {id="terminal-output" class="command-line" data-prompt="$" data-output="2-5"}
python3 lightupbot.py
This is a person!
turning on
There's nobody here
turning off
```

{{% alert title="Info" color= "info" %}}

You can actually detect any object that is listed in the <file>labels.txt</file> (such as a dog or a chair) but for this tutorial, we are detecting a person.

To detect something else with the camera, just change the string "person" on line 69 of <file>lightupbot.py</file> to a different item in the <file>label.txt</file> file.

```python
if d.class_name.lower() == "person":
    print("This is a person!")
    found = True
```

{{% /alert %}}

## Next Steps

In this tutorial, you learned how to build an object detection robot that turns your lights on using Viam.
You could use this same concept to build a smart fan that only turns on if you are sitting at your desk working, turn on the lights in your bathroom mirror only when you are in front of the sink, or activate a pet feeder every time your cat looks at the camera.

To turn this robot into a security alert system, try the other tutorial in this series: [Build a Person Detection Security Robot That Sends You a Photo of the Person Stealing Your Chocolates](/tutorials/projects/send-security-photo/).

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}
