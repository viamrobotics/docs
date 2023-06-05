---
title: "A Person Detection Security Robot That Sends You Photos"
linkTitle: "Detect a Person and Send a Photo"
weight: 50
type: "docs"
description: "Use the Vision Service and the Python SDK to send yourself a text message when your webcam detects a person."
image: "/tutorials/img/send-security-photo/text-message.png"
imageAlt: "Text message reading 'Alert There is someone at your desk beware' with a photo of a person (Steve) detected by the camera as he approaches the desk."
images: ["/tutorials/img/send-security-photo/text-message.png"]
tags: ["camera", "vision", "detector", "python"]
# Author: Hazal Mestci
---

{{< alert title="Caution" color="caution" >}}
There are [breaking changes in the Vision Service](/appendix/release-notes/#25-april-2023).
This tutorial has not yet been updated.
{{< /alert >}}

{{% alert title="Note" color="note" %}}

This tutorial is part of our built-in webcam projects series.
For a similar project that integrates a Kasa smart plug, see [Use Object Detection to Turn Your Lights On](/tutorials/projects/light-up/).

{{% /alert %}}

In this tutorial you will create a desk security system with no hardware other than your laptop and built-in webcam.

Maybe you keep a box of chocolates on your desk to snack on when you are hungry.
Maybe someone is eating your chocolates when you are away.
You're not sure who, but you suspect Steve.
This robot will help you catch the culprit.

When someone comes to your desk, the robot will use the [Vision Service](/services/vision/) and an ML model to detect a person, take their photo, and text you an alert with a photo of the person.

![Text message reading "Alert There is someone at your desk beware" with a photo of a person (Steve) detected by the camera as he approaches the desk.](../../img/send-security-photo/text-message.png)

## Hardware requirements

You need the following hardware for this tutorial:

- Computer with a webcam
  - This tutorial uses a MacBook Pro but any computer running macOS or 64-bit Linux will work
- Mobile phone (to receive the text messages)

## Software requirements

You will use the following software in this tutorial:

- [Python 3.8 or newer](https://www.python.org/downloads/)
- [`viam-server`](/installation/#install-viam-server)
- [Viam Python SDK](https://python.viam.dev/)
  - The Viam Python SDK (software development kit) lets you control your Viam-powered robot by writing custom scripts in the Python programming language.
  Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).
- [yagmail](https://github.com/kootenpv/yagmail)
- A gmail account to send emails. You can use an existing account, or create a new one.

## Configure your robot on the Viam app

If you followed the [Use Object Detection to Turn Your Lights On](/tutorials/projects/light-up/) tutorial, you already have a robot set up on the [Viam app](https://app.viam.com), connected and live, with a [webcam configured](/components/camera/webcam/).

{{% expand "If you're starting with this tutorial, click here for instructions." %}}

### Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new robot.

Go to the **Setup** tab of your new robot's page and follow the steps [to install `viam-server` on your computer](/installation/).

### Configure the camera component

On your new robot's page, go to the **Config** tab.

![The CONFIG tab in Builder mode on the Viam app.](../../img/light-up/config-tab.png)

On the **Config** tab, create a new component:

- **Name**: `my-camera`
- **Type**: `camera`
- **Model**: `webcam`

Click **Create Component** to add the camera.

Click the **Video Path** field to reveal a drop-down populated with camera paths that have been identified on your machine.

Select the path to the camera you want to use.

Click **Save Config** in the bottom left corner of the screen.

Navigate to the **Control** tab where you can see your camera working.

{{% /expand %}}

## How to use yagmail

Install yagmail (Yet Another Gmail/SMTP client) by running the following command in a terminal on your computer:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install yagmail
```

{{% alert title="Tip" color="tip" %}}
As you are programming the yagmail section of this project, you will be prompted to use your Gmail username and password within the code.
If you use 2-step verification for your email, some apps or devices may be blocked from accessing your Google account.
You can get an "Application-Specific Password" following [this guide](https://support.google.com/accounts/answer/185833).

App Passwords are 16-digit passcodes that allow the app or device access to your Google account.
This step is optional.
{{% /alert %}}

Then we have to indicate whom to send a message to, the subject, and the contents of the text message (which can be a string, image or audio).
Example code below (though you don’t have to use it yet, this will get used in the next section):

```python
yag.send('phone_number@gatewayaddress.com', 'subject', contents)
```

You will need to access to your phone number through your carrier.
For this tutorial, you are going to send the text to yourself.
You will replace `to@someone.com` with your phone number and [SMS gateway address](https://en.wikipedia.org/wiki/SMS_gateway).
You can find yours here: [Gateway Addresses for Mobile Phone Carrier Text Message](https://support-en.wd.com/app/answers/detailweb/a_id/44431/~/gateway-addresses-for-mobile-phone-carrier-text-message).
Some common ones:

- AT&T: `txt.att.net`
- T-Mobile:`tmomail.net`
- Verizon Wireless: `vtext.com`

As an example, if you have T-Mobile your code will look like this:

```python
yag.send('xxxxxxxxxx@tmomail.net', 'subject', contents)

```

This allows us to route the email to our phone as a text message.

## Use the Viam Python SDK to control your security robot

If you followed the [Use Object Detection to Turn Your Lights On](/tutorials/projects/light-up/) tutorial, you already set up a folder with some Python code that connects to your robot and implements the Vision Service.

If you are starting with this tutorial, follow the [steps here](/tutorials/projects/light-up/#write-python-code-to-control-your-object-detection-robot) to create the main script file, connect the code to the robot, and select the model and label path.
Ignore the step about the Kasa smart plug host address.

Instead of using this person detector to activate a smart plug, you will send yourself a text message.

Make a copy of the [<file>lightupbot.py</file>](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/lightupbot.py) file in your project directory and save it as <file>chocolate_security.py</file>.
You will use the same robot connection code and Vision Service configuration code but edit some other parts of the file.

Delete the `from kasa import Discover, SmartPlug` line and replace it with the following to import the Yagmail Python library:

```python
import yagmail
```

Now you need to rewrite the if/else function.
If a person is detected, your robot will print `sending a message`, take a photo, and save it to your computer as <file>foundyou.png</file> (or whatever name you want).

Then you will create a `yagmail.SMTP` instance to initialize the server connection.

Refer to the code below and the [yagmail instructions](#how-to-use-yagmail) to edit your <file>chocolate_security.py</file> file as necessary.

{{% expand "Click to show the full example code." %}}

```python {class="line-numbers linkable-line-numbers" data-line="6"}
import asyncio
import os

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.types import CameraMimeType
from viam.services.vision import VisionClient, VisModelConfig, VisModelType, Detection
import yagmail


# These must be set. You can get them from your robot's 'CODE SAMPLE' tab
robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload=robot_secret)
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address(robot_address, opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)
    # This string should match your camera component name in your robot config on the Viam app
    camera = Camera.from_robot(robot, "my-camera")
    image = await camera.get_image()

    # Get and set up the Vision Service
    vision = VisionClient.from_robot(robot)
    params = {"model_path": "./effdet0.tflite", "label_path": "./labels.txt", "num_threads": 1}
    personDet = VisModelConfig(name="person_detector", type=VisModelType("tflite_detector"), parameters=params)
    await vision.add_detector(personDet)
    names = await vision.get_detector_names()
    print(names)

    N = 100
    for i in range(N):
        image = await camera.get_image()
        detections = await vision.get_detections(image, "person_detector")
        found = False
        for d in detections:
            if d.confidence > 0.8:
                print(d)
                print()
                if d.class_name.lower() == "person":
                    print("This is a person!")
                    found = True

            if found:
                print("sending a message")
                # Change this path to your own
                image.save('/yourpath/foundyou.png')
                # yagmail section
                # Create a yagmail.SMTP instance to initialize the server connection
                # Replace username and password with your actual credentials
                yag = yagmail.SMTP('mygmailusername', 'mygmailpassword')
                # Specify the message contents
                contents = ['There is someone at your desk - beware','/yourpath/foundyou.png']
                # Add phone number and gateway address found in the SMS gateway step
                yag.send('xxx-xxx-xxxx@tmomail.net', 'subject', contents)

                # If the robot detects a person and sends a text, we don't need it to keep sending us more texts
                # so we sleep it for 60 seconds before looking for a person again
                await asyncio.sleep(60)
            else:
                print("There's nobody here, don't send a message")
                await asyncio.sleep(10)

    await asyncio.sleep(5)
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())

```

{{% /expand %}}

Save your code file.

### Run the code

You are ready to test your robot!

From a command line on your computer, navigate to the project directory and run the code with this command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 chocolate_security.py
```

If you are in front of your computer's webcam, you should get a text!

Your terminal should look like this as your project runs if you are in front of the camera for a bit, and then move away from the screen:

```sh {id="terminal-prompt" class="command-line" data-prompt="$" data-output="2-25"}
python3 chocolate_security.py
This is a person!
sending message
x_min: 7
y_min: 0
x_max: 543
y_max: 480
confidence: 0.94140625
class_name: "Person"


This is a person!
sending message
x_min: 51
y_min: 0
x_max: 588
y_max: 480
confidence: 0.9375
class_name: "Person"

This is a person!
sending message
There's nobody here, don't send message
There's nobody here, don't send message
```

## Summary and next steps

In this tutorial, you learned how to build a security robot using the Vision Service, your computer, and your mobile phone, and we all learned not to trust Steve.

Have you heard about the chocolate box thief?
He's always got a few Twix up his Steve.

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}
