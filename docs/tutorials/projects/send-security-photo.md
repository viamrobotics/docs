---
title: "A Person Detection Security Robot That Sends You Photos"
linkTitle: "Detect a Person and Send a Photo"
type: "docs"
description: "Use the vision service and the Python SDK to send yourself a text message when your webcam detects a person."
image: "/tutorials/send-security-photo/text-message.png"
imageAlt: "Text message reading 'Alert There is someone at your desk beware' with a photo of a person (Steve) detected by the camera as he approaches the desk."
images: ["/tutorials/send-security-photo/text-message.png"]
tags: ["camera", "vision", "detector", "python"]
authors: ["Hazal Mestci"]
languages: ["python"]
viamresources: ["camera", "mlmodel", "vision"]
level: "Intermediate"
date: "2023-03-30"
# updated: ""
cost: "0"
no_list: true
---

{{% alert title="Tip" color="tip" %}}

This tutorial is part of our built-in webcam projects series.
For a similar project that integrates a Kasa smart plug, see [Use Object Detection to Turn Your Lights On](/tutorials/projects/light-up/).

{{% /alert %}}

In this tutorial, you will create a desk security system with no hardware other than your laptop and the built-in webcam.

Maybe you keep a box of chocolates on your desk to snack on when you are hungry.
Maybe someone is eating your chocolates when you are away.
You're not sure who, but you suspect Steve.
This robot will help you catch the culprit.

When someone comes to your desk, the robot will use the [vision service](/ml/vision/) and the [ML model service](/ml/) to detect a person, take their photo, and text you an alert with a photo of the person.

![Text message reading "Alert There is someone at your desk beware" with a photo of a person (Steve) detected by the camera as he approaches the desk.](/tutorials/send-security-photo/text-message.png)

## Hardware requirements

You need the following hardware for this tutorial:

- Computer with a webcam
  - This tutorial uses a MacBook Pro but any computer running macOS or 64-bit Linux will work
- Mobile phone (to receive text messages)

## Software requirements

You will use the following software in this tutorial:

- [Python 3.8 or newer](https://www.python.org/downloads/)
- [`viam-server`](/get-started/installation/#install-viam-server)
- [Viam Python SDK](https://python.viam.dev/)
  - The Viam Python SDK (software development kit) lets you control your Viam-powered robot by writing custom scripts in the Python programming language.
    Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).
- [yagmail](https://github.com/kootenpv/yagmail)
- A Gmail account to send emails.
  You can use an existing account, or create a new one.

## Configure your robot on the Viam app

If you followed the [Use Object Detection to Turn Your Lights On](/tutorials/projects/light-up/) tutorial, you already have a robot set up on the [Viam app](https://app.viam.com), connected and live, with a [webcam configured](/components/camera/webcam/).

{{% expand "If you're starting with this tutorial, click here for instructions." %}}

### Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new robot.

Go to the **Setup** tab of your new robot's page and follow the steps [to install `viam-server` on your computer](/get-started/installation/).

### Configure the camera component

On your new robot's page, go to the **Config** tab and create a [camera component](/components/camera/):

Click **Create component** in the lower-left corner of the screen.

Select type `camera` and model `webcam`.

Enter `my-camera` as the name, then click **Create** to add the camera.

Click the **Video Path** field to reveal a dropdown populated with camera paths that have been identified on your machine.

Select the path to the camera you want to use.

Click **Save config** in the lower-left corner of the screen.

Navigate to the **Control** tab where you can see your camera working.

{{% /expand %}}

### Configure your services

This tutorial uses pre-trained ML packages.
If you want to train your own, you can [train a model](/ml/train-model/).

To use the provided Machine Learning model, copy the <file>[effdet0.tflite](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/effdet0.tflite)</file> file and the <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> to your project directory.

Click the **Services** subtab.

1. **Configure the ML model service**

   Add an [mlmodel](/ml/) service:

   Click **Create service** in the lower-left corner of the **Services** subtab.
   Select type `mlmodel`, then select model `tflite_cpu`.

   Enter `people` as the name, then click **Create**.

   In the new ML Model service panel, configure your service.

   ![mlmodel service panel with empty sections for Model Path, and Optional Settings such as Label Path and Number of threads.](/tutorials/tipsy/app-service-ml-before.png)

   Select the **Path to Existing Model On Robot** for the **Deployment** field.
   Then specify the absolute **Model Path** as where your tflite file lives and any **Optional Settings** such as the absolute **Label Path** as where your labels.txt file lives and the **Number of threads** as 1.

1. **Configure an mlmodel detector**

   Add a [vision service](/ml/vision/) with the name `myPeopleDetector`, type `vision` and model `mlmodel`.
   Click **Create service**.

   In the new vision service panel, configure your service.

   Select `people` from the **ML Model** dropdown.

   ![vision service panel called myPeopleDetector with filled Attributes section, mlmodel_name is “people”.](/tutorials/tipsy/app-service-vision.png)

### Configure the detection camera

To be able to test that the vision service is working, add a `transform` camera which will add bounding boxes and labels around the objects the service detects.

Click on the **Components** subtab and click **Create component** in the lower-left corner.
Create a [transform camera](/components/camera/transform/) with type `camera` and model `transform`.
Name it `detectionCam` and click **Create**.

![detectionCam component panel with type camera and model transform, Attributes section has source and pipeline but they are empty.](/tutorials/tipsy/app-detection-before.png)

In the new transform camera panel, replace the attributes JSON object with the following object which specifies the camera source that the `transform` camera will use, and defines a pipeline that adds the defined `myPeopleDetector`:

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

Click **Save config** in the lower-left corner of the screen.

![detectionCam component panel with type camera and model transform, Attributes section filled with source and pipeline information.](/tutorials/tipsy/app-detection-after.png)

## How to use yagmail

Install yagmail (Yet Another Gmail/SMTP client) by running the following command in a terminal on your computer:

```sh {class="command-line" data-prompt="$"}
pip3 install yagmail
```

{{% alert title="Tip" color="tip" %}}
As you are programming the yagmail section of this project, you will be prompted to use your Gmail username and password within the code.
If you use 2-step verification for your email, some apps or devices may be blocked from accessing your Google account.
You can get an "Application-Specific Password" following [this guide](https://support.google.com/accounts/answer/185833).

App Passwords are 16-digit passcodes that allow the app or device access to your Google account.
This step is optional.
{{% /alert %}}

Then we have to indicate whom to send a message to, the subject, and the contents of the text message (which can be a string, image, or audio).
Example code below (though you don’t have to use it yet, this will get used in the next section):

```python
yag.send('phone_number@gatewayaddress.com', 'subject', contents)
```

You will need access to your phone number through your carrier.
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

This allows you to route the email to your phone as a text message.

## Use the Viam Python SDK to control your security robot

If you followed the [Use Object Detection to Turn Your Lights On](/tutorials/projects/light-up/) tutorial, you already set up a folder with some Python code that connects to your robot and gets detections from your camera.

If you are starting with this tutorial, follow [these steps](/tutorials/projects/light-up/#write-python-code-to-control-your-object-detection-robot) to create the main script file and connect the code to the robot.
Ignore the step about the Kasa smart plug host address.

Instead of using this person detector to activate a smart plug, you will send yourself a text message.

Make a copy of the [<file>lightupbot.py</file>](https://github.com/viam-labs/devrel-demos/blob/main/Light%20up%20bot/lightupbot.py) file in your project directory and save it as <file>chocolate_security.py</file>.
You will use the same robot connection code and detector configuration code but edit some other parts of the file.

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
from viam.services.vision import VisionClient
from viam.components.camera import Camera
from viam.media.video import RawImage
import yagmail

# These must be set. You can get them from your robot's 'Code sample' tab
robot_api_key = os.getenv('ROBOT_API_KEY') or ''
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key=robot_api_key,
      api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)


async def main():
    robot = await connect()
    # make sure that your detector name in the app matches "myPeopleDetector"
    myPeopleDetector = VisionClient.from_robot(robot, "myPeopleDetector")
    # make sure that your camera name in the app matches "my-camera"
    my_camera = Camera.from_robot(robot=robot, name="my_camera")

    N = 100
    for i in range(N):
        img = await my_camera.get_image()
        raw_img = RawImage(data=img.data, mime_type=img.mime_type)
        detections = await myPeopleDetector.get_detections(raw_img)

        found = False
        for d in detections:
            if d.confidence > 0.8 and d.class_name.lower() == "person":
                print("This is a person!")
                found = True
        if found:
            print("sending a message")
            # Change this path to your own
            raw_img.save('/yourpath/foundyou.png')
            # Yagmail section
            # Create a yagmail.SMTP instance
            # to initialize the server connection.
            # Replace username and password with actual credentials.
            yag = yagmail.SMTP('mygmailusername', 'mygmailpassword')
            # Specify the message contents
            contents = ['There is someone at your desk - beware',
                        '/yourpath/foundyou.png']
            # Add phone number and gateway address
            # found in the SMS gateway step
            yag.send('xxx-xxx-xxxx@tmomail.net', 'subject', contents)

            # If the robot detects a person and sends a text, we don't need
            # it to keep sending us more texts so we sleep it for 60
            # seconds before looking for a person again
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

{{% snippet "show-secret.md" %}}

Save your code file.

### Run the code

You are ready to test your robot!

From a command line on your computer, navigate to the project directory and run the code with this command:

```sh {class="command-line" data-prompt="$"}
python3 chocolate_security.py
```

If you are in front of your computer's webcam, you should get a text!

Your terminal should look like this as your project runs if you are in front of the camera for a bit, and then move away from the screen:

```sh {class="command-line" data-prompt="$" data-output="2-25"}
python3 chocolate_security.py
This is a person!
sending a message
x_min: 7
y_min: 0
x_max: 543
y_max: 480
confidence: 0.94140625

This is a person!
sending a message
x_min: 51
y_min: 0
x_max: 588
y_max: 480
confidence: 0.9375

This is a person!
sending a message
There's nobody here, don't send a message
There's nobody here, don't send a message
```

## Summary and next steps

In this tutorial, you learned how to build a security robot using the vision service, the ML model service, your computer, and your mobile phone, and we all learned not to trust Steve.

Have you heard about the chocolate box thief?
He's always got a few Twix up his Steve.

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}
