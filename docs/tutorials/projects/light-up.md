---
title: "Use Object Detection to Turn Your Lights On"
linkTitle: "Turn on Lights with Object Detection"
type: "docs"
description: "How to turn a light on when your webcam sees a person."
webmSrc: "/tutorials/light-up/light-up.webm"
mp4Src: "/tutorials/light-up/light-up.mp4"
images: ["/tutorials/light-up/light-up.gif"]
videoAlt: "A person sitting at a desk with a computer and light bulb set up in front of her. As she leaves the light turns off, and as she enters the frame, the light turns back on."
tags: ["camera", "vision", "detector", "python"]
authors: ["Hazal Mestci"]
languages: ["python"]
viamresources: ["camera", "mlmodel", "vision"]
level: "Intermediate"
date: "2023-03-30"
# updated: ""
cost: 20
no_list: true
---

This tutorial uses the Viam [vision service](/services/vision/) with your computer's built-in webcam to detect the presence of a person and turn on a lamp when you sit down at your desk.

You can turn it into a night light for reading books, a security robot that alerts you when a person is close by, or a bathroom light that only activates when people enter; the opportunities are endless.

This project is a great place to start if you are new to building robots because the only hardware it requires in addition to your computer is a [smart plug](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-mini) or smart bulb.

{{<gif webm_src="/tutorials/light-up/light-up.webm" mp4_src="/tutorials/light-up/light-up.mp4" alt="The project working: a person sitting at a desk with a computer and light bulb set up in front of her. As she leaves the light turns off, and as she enters the frame, the light turns back on.">}}

## Hardware requirements

You need the following hardware for this tutorial:

- Computer with a webcam
  - This tutorial uses a MacBook Pro but any computer running macOS or 64-bit Linux will work
- Mobile phone (to download the Kasa Smart app)
- Either a smart plug or bulb:
  - [Kasa Smart Wi-Fi Plug Mini](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-wifi-plug-mini)
    - (This is what we used for this tutorial)
  - [Kasa Smart Light Bulb](https://www.kasasmart.com/us/products/smart-lighting/kasa-smart-light-bulb-multicolor-kl125)
- [Table Lamp Base](https://www.amazon.com/gp/product/B08KZNZVY7/ref=ppx_yo_dt_b_asin_title_o02_s00?) or similar

## Software requirements

You will use the following software in this tutorial:

- [Python 3.8 or newer](https://www.python.org/downloads/)
- [`viam-server`](/installation/#install-viam-server)
- [Viam Python SDK](https://python.viam.dev/)
  - The Viam Python SDK (software development kit) lets you control your Viam-powered robot by writing custom scripts in the Python programming language.
    Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).
- [Project repo on GitHub](https://github.com/viam-labs/devrel-demos/tree/main/Light%20up%20bot)

## Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new robot.

Go to the **Setup** tab of your new robot's page and follow the steps to install `viam-server` on your computer.

## Configure the camera component

On your new robot's page, go to the **Config** tab.

Navigate to the **Components** subtab and click **Create component** in the lower-left corner.

Select `camera` for type and `webcam` for model.

Enter `my-camera` as the name for your camera, then click **Create**.

Click the **video path** field to reveal a drop-down populated with camera paths that have been identified on your machine.

Select the path to the camera you want to use.

Click **Save Config** in the bottom left corner of the screen.

Navigate to the **Control** tab where you can see your camera working.

{{< gif webm_src="/tutorials/light-up/control-panel.webm" mp4_src="/tutorials/light-up/control-panel.mp4" alt= "Opening the camera panel on the control tab, toggling the video feed on, and watching as a person wearing headphones waves at the camera." >}}

## Configure your services

This tutorial uses pre-trained ML packages.
If you want to train your own, you can [train a model](/manage/ml/train-model/).

To use the provided Machine Learning model, copy the <file>[effdet0.tflite](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/effdet0.tflite)</file> file and the <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> to your project directory.

Navigate to the **Services** subtab of your robot's **Config** tab.

### Configure the ML model service

Click **Create service** in the lower-left corner of the page.
Select `ML Model` for the type, then select `TFLite CPU` for the model.
Enter `people` as the name for your [mlmodel](/services/ml/), then click **Create**.

In the new ML Model service panel, configure your service.

![mlmodel service panel with empty sections for Model Path, and Optional Settings such as Label Path and Number of threads.](/tutorials/tipsy/app-service-ml-before.png)

Select the **Path to existing model on robot** for the **Deployment** field.
Then specify the absolute **Model path** as where your tflite file lives and any **Optional settings** such as the absolute **Label path** as where your labels.txt file lives and the **Number of threads** as `1`.

### Configure an mlmodel detector

Click **Create service** in the lower-left corner of the page.
For your [vision service](/services/vision/), select type `vision` and model `mlmodel`.
Enter `myPeopleDetector` for the name, then click **Create**.

In the new vision service panel, configure your service.

From the **Select model** drop-down, select the name of the TFLite model (`people`).

### Configure the detection camera

To be able to test that the vision service is working, add a `transform` camera which will add bounding boxes and labels around the objects the service detects.

Click the **Components** subtab and click the **Create component** button in the lower-left corner.
Create a [transform camera](/components/camera/transform/) by selecting type `camera` and model `transform`.
Name it `detectionCam` and click **Create**.

![detectionCam component panel with type camera and model transform, Attributes section has source and pipeline but they are empty.](/tutorials/tipsy/app-detection-before.png)

In the new transform camera panel, replace the attributes JSON object with the following object which specifies the camera source that the `transform` camera will be using and defines a pipeline that adds the defined `myPeopleDetector`:

```json
{
  "source": "my-camera",
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "detector_name": "myPeopleDetector",
        "confidence_threshold": 0.5
      }
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

![detectionCam component panel with type camera and model transform, Attributes section filled with source and pipeline information.](/tutorials/tipsy/app-detection-after.png)

## Set up the Kasa Smart Plug

1. Plug your smart plug into any power outlet and turn it on by pressing the white button on the smart plug.
   To connect the plug to your wifi, download the Kasa Smart app from the [App Store](https://apps.apple.com/us/app/kasa-smart/id1034035493) or [Google Play](https://play.google.com/store/apps/details?id=com.tplink.kasa_android) to your mobile phone.
   When you first open the app, you will be prompted to create an account.
   As you do this, you will receive an email with the subject line "TP-Link ID: Activation Required" to complete your account registration.

2. Follow the steps in Kasa's [setup guide](https://www.tp-link.com/us/support/faq/946/) to add your device and connect it to your wifi.
   Once it is connected, you will no longer need to use the mobile app.

3. Open a terminal on your computer and run the following command to install the [smart plug Python API](https://github.com/python-kasa/python-kasa):

   ```sh {class="command-line" data-prompt="$"}
   pip3 install python-kasa
   ```

4. <a name=kasa ></a> Run the following command to return information about your smart device:

   ```sh {class="command-line" data-prompt="$"}
   kasa discover
   ```

   You should see this command output something like this:

   ![Terminal output with information about the smart plug including the host, device state (on), timestamp, hardware and software versions, MAC address, location (latitude and longitude), whether the LED is currently on, and the timestamp of when it last turned on. There is also a list of modules (schedule, usage, antitheft, time, and cloud).](/tutorials/light-up/kasa-discover-output.png)

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

1. Navigate to the **Code sample** tab on [the Viam app](https://app.viam.com).
   Make sure **Python** is selected in the **Language** selector.

   {{% snippet "show-secret.md" %}}

1. Get the robot address and API key from the code sample and set them as environment variables or add them at the top of <file>lightupbot.py</file>.

   You also need to tell the code how to access your smart plug.

1. Add the host address (for example, `10.1.11.221`) of your smart plug that you found in the [`kasa discover` step](#kasa) to line 55 of <file>lightupbot.py</file>.

### Run the code

Now you are ready to test your robot!

From a command line on your computer, navigate to the project directory and run the code with this command:

```sh {class="command-line" data-prompt="$"}
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

To detect something else with the camera, just change the string "person" on line 46 of <file>lightupbot.py</file> to a different item in the <file>label.txt</file> file.

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
