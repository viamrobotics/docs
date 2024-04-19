---
title: "A Person Detection Security Robot That Sends You Photos"
linkTitle: "Detect a Person and Send a Photo"
type: "docs"
description: "Use the vision service and the Python SDK to send yourself a text message when your webcam detects a person."
imageAlt: "Text message reading 'Alert There is someone at your desk beware' with a photo of a person (Steve) detected by the camera as he approaches the desk."
images: ["/tutorials/send-security-photo/text-message.png"]
tags: ["camera", "vision", "detector", "python"]
authors: ["Hazal Mestci"]
languages: ["python"]
viamresources: ["camera", "mlmodel", "vision"]
level: "Intermediate"
date: "2023-03-30"
updated: "2024-04-19"
cost: "0"
no_list: true
---

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
  - The Viam Python SDK (software development kit) lets you control your Viam-powered machine by writing custom scripts in the Python programming language.
    Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).
- [yagmail](https://github.com/kootenpv/yagmail)
- A Gmail account to send emails.
  You can use an existing account, or create a new one.

## Configure your machine on the Viam app

### Install `viam-server` and connect to your machine

{{% snippet "setup.md" %}}

### Configure the camera component

Configure your [webcam](/components/camera/webcam/) so that your machine can get the video stream from your camera:

1. On the [Viam app](https://app.viam.com), navigate to your machine's page.
   Check that the part status dropdown in the upper left of the page, next to your machine's name, reads "Live"; this indicates that your machine is turned on and that its instance of `viam-server` is in contact with the Viam app.

2. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component**.
   Start typing "webcam" and select **camera / webcam**.
   Give your camera a name.
   This tutorial uses the name `cam` in all example code.
   Click **Create**.

3. Click the **video path** dropdown and select the webcam you'd like to use for this project from the list of suggestions.

4. Click **Save** in the top right corner of the screen to save your changes.

### Test your physical camera

To test your camera, go to the **CONTROL** tab and click to expand your camera's panel.

Toggle **View `cam`** to the "on" position.
The video feed should display.
If it doesn't, double-check that your config is saved correctly, and check the **LOGS** tab for errors.

### Configure your services

Now that you know the camera is properly connected to your machine, it is time to add computer vision by configuring the [vision service](/ml/vision/) on your machine.
This tutorial uses a pre-trained Machine Learning model from the Viam Registry called [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO).
The model can detect a variety of things, including `Persons`.
You can see a full list of what the model can detect in <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> file.

If you want to train your own model instead, follow the instructions in [train a model](/ml/train-model/).

1. **Configure the ML model service**

   Navigate to your machine's **CONFIGURE** tab.

   Click the **+** (Create) button next to your main part in the left-hand menu and select **Service**.
   Start typing `ML model` and select **ML model / TFLite CPU** from the builtin options.

   Enter `people` as the name, then click **Create**.

   In the new ML Model service panel, configure your service.

   ![mlmodel service panel with empty sections for Model Path, and Optional Settings such as Label Path and Number of threads.](/tutorials/send-security-photo/app-service-ml-before.png)

   Select **Deploy model on machine** for the **Deployment** field.
   Then select the `viam-labs:EfficientDet-COCO` model from the **Models** dropdown.

1. **Configure an mlmodel detector** [vision service](/ml/vision/)

   Click the **+** (Create) button next to your main part in the left-hand menu and select **Service**.
   Start typing `ML model` and select **vision / ML model** from the builtin options.

   Enter `myPeopleDetector` as the name, then click **Create**.

   In the new vision service panel, configure your service.

   Select `people` from the **ML Model** dropdown.

   ![vision service panel called myPeopleDetector with filled Attributes section, mlmodel_name is “people”.](/tutorials/send-security-photo/app-service-vision.png)

### Configure the detection camera

To be able to test that the vision service is working, add a [transform camera](/components/camera/transform/) which will add bounding boxes and labels around the objects the service detects.

Click the **+** (Create) button next to your main part in the left-hand menu and select **Component**.
Start typing "transform" and select **camera / transform**.
Give your transform camera the name `detectionCam` and click **Create**.

![detectionCam component panel with type camera and model transform, Attributes section has source and pipeline but they are empty.](/tutorials/send-security-photo/app-detection-before.png)

In the new transform camera panel, click on **{}** to go to advanced mode and replace the attributes JSON object with the following object which specifies the camera source that the `transform` camera will use, and defines a pipeline that adds the defined `myPeopleDetector`:

```json
{
  "source": "cam",
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

It is good practice to also add your camera `cam` as a dependency in the **Depends on** section, to ensure the components are loaded in the correct order.

Click **Save** in the top right corner of the screen.

![detectionCam component panel with type camera and model transform, Attributes section filled with source and pipeline information.](/tutorials/send-security-photo/app-detection-after.png)

### Test the model

{{<imgproc src="/tutorials/send-security-photo/control-view.png" class="alignright" resize="300x" declaredimensions=true alt="the control tab">}}

At this point, you can test that the model is detecting people.
Navigate to your [machine's CONTROL tab](/fleet/machines/#control).

Click on the `detectionCam` panel and toggle **View detectionCam** on.
If the vision service detects a person on the configured camera, you will see a red box around the detection along with the confidence score of the detection.

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

### Create the main script file

On your computer, navigate to the directory where you want to put the code for this project. Create a file there called <file>chocolate_security.py</file>. This will be the main script for the machine.

Copy the following code and paste it into <file>chocolate_security.py</file>:

```python
import asyncio
import os
import yagmail

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import
    VisionClient, VisModelConfig, VisModelType, Detection

# Replace "<API-KEY>" (including brackets) with your machine's api key
api_key='<API-KEY>',
# Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
api_key_id='<API-KEY-ID>'
address = os.getenv('ROBOT_ADDRESS') or ''


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key=_api_key,
      api_key_id=api_key_id
    )
    return await RobotClient.at_address(address, opts)


async def main():
    machine = await connect()
    # make sure that your detector name in the app matches "myPeopleDetector"
    myPeopleDetector = VisionClient.from_robot(machine, "myPeopleDetector")
    # make sure that your camera name in the app matches "my-camera"
    my_camera = Camera.from_robot(robot=machine, name="cam")

    while True:
        img = await my_camera.get_image(mime_type="image/jpeg")
        detections = await myPeopleDetector.get_detections(img)

        found = False
        for d in detections:
            if d.confidence > 0.8 and d.class_name.lower() == "person":
                print("This is a person!")
                found = True
        if found:
            print("sending a message")
            # Change this path to your own
            img.save('/yourpath/foundyou.jpeg')
            # Yagmail section
            # Create a yagmail.SMTP instance
            # to initialize the server connection.
            # Replace username and password with actual credentials.
            yag = yagmail.SMTP('mygmailusername', 'mygmailpassword')
            # Specify the message contents
            contents = ['There is someone at your desk - beware',
                        '/yourpath/foundyou.jpeg']
            # Add phone number and gateway address
            # found in the SMS gateway step
            yag.send('xxx-xxx-xxxx@tmomail.net', 'subject', contents)

            # If the machine detects a person and sends a text, we don't need
            # it to keep sending us more texts so we sleep it for 60
            # seconds before looking for a person again
            await asyncio.sleep(60)
        else:
            print("There's nobody here, don't send a message")
            await asyncio.sleep(10)
    await asyncio.sleep(5)
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

After connecting to your machine, your machine will continuously check images for detections of people.
If a person is detected, your robot will print `sending a message`, take a photo, and save it to your computer as <file>foundyou.png</file> (or whatever name you want).

Then it will create a `yagmail.SMTP` instance to send the email and send the email.

### Connect the code to the robot

You need to tell the code how to access your specific machine (which in this case represents your computer and its webcam).

Navigate to the **CONNECT** tab on the Viam app.
Make sure Python is selected in the Language selector.
Get the machine address and API key from the code sample and set them as environment variables or add them at the top of <FILE>chocolate_security.py</FILE>.

{{% snippet "show-secret.md" %}}

Save your code file.

### Run the code

You are ready to test your machine!

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

## Next steps

In this tutorial, you learned how to build a security robot using the vision service, the ML model service, your computer, and your mobile phone, and we all learned not to trust Steve.

Have you heard about the chocolate box thief?
He's always got a few Twix up his Steve.

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}
