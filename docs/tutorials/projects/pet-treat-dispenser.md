---
title: "How To Build a Smart Pet Feeder With Machine Learning"
linkTitle: "Build a Smart Pet Treat Dispenser"
weight: 50
type: "docs"
description: "Build a smart pet feeder with machine learning using a Raspberry Pi."
tags: ["raspberry pi", "app", "board", "motor"]
image: "/tutorials/img/pet-treat-dispenser/preview.png"
imageAlt: "Image of a dog interacting with the smart pet feeder."
images: ["/tutorials/img/pet-treat-dispenser/preview.png"]

# Author: Arielle
# Designs: Jessamy
---

Use the Viam app to train and deploy a custom machine learning model on your pets to have your robot give your pet treats whenever they walk by ... programmatically on a schedule!
This tutorial will teach you how to design your own custom pet feeder that utilizes the [Data Manager](/manage/data/), [Machine Learning Service](/services/ml/), the [Vision Service](/services/vision/), and a stepper motor to dispense treats at the sight of your pet!

![Image of a dog interacting with the smart pet feeder.](/tutorials/img/pet-treat-dispenser/preview.png)

## Introduction

Your dog is insatiable.
You wake up every morning to the sound of gentle whining at the door and the pitter patter of begging paws on the floor, and you know your fur-baby is only living for his next meal.
_It’s two hours before my alarm_, you think to yourself, but you remember dogs have no sense of the man-made concept of time.
The sun has barely risen on the horizon as you glance out your east facing window, and you can see a moist nose peering under your door frame.
Your dog commands you: it’s time to eat.

So what if you could build a robot to feed your pet in the morning so you can catch some extra zzz’s before work?
What if you want to give your dog some treats for being a Good Boy™ while you’re spending a day in the office?

In this tutorial you will learn how to design your own custom smart pet feeder or treat dispenser.
You will learn how to train a custom machine learning model on your pet's face, programmatically or autonomously control your feeder using Viam, and how to assemble the necessary hardware and circuitry to make this happen.

## Requirements

### Hardware

You will need the following hardware components:

1. A computer running macOS or Linux
1. [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) with [microSD card](https://www.amazon.com/Amazon-Basics-microSDXC-Memory-Adapter/dp/B08TJTB8XS/ref=sr_1_4?crid=18AP61IEBXODY&keywords=microsd%2Bcard&qid=1680799199&s=electronics&sprefix=microsd%2Bcard%2Celectronics%2C82&sr=1-4&th=1), with `viam-server` installed following our [Installation Guide](https://docs.viam.com/installation/).
1. [Raspberry Pi power supply](https://www.amazon.com/Raspberry-Model-Official-SC0218-Accessory/dp/B07W8XHMJZ/ref=asc_df_B07W8XHMJZ/?tag=hyprod-20&linkCode=df0&hvadid=416672671431&hvpos=&hvnetw=g&hvrand=10350240906167803476&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-815817210384&psc=1&tag=&ref=&adgrpid=95587150204&hvpone=&hvptwo=&hvadid=416672671431&hvpos=&hvnetw=g&hvrand=10350240906167803476&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-815817210384)
1. [microSD card reader](https://www.amazon.com/Card-Reader-Beikell-Memory-Adapter/dp/B09Z6JCKL7/ref=sr_1_3?crid=26L0FKD1TG7PU&keywords=micro%2Bsd%2Bcard%2Breader&qid=1680799165&s=electronics&sprefix=micro%2Bsd%2Bcard%2Breade%2Celectronics%2C90&sr=1-3&th=1)
1. [Stepper motor and motor driver](https://makersportal.com/shop/nema-17-stepper-motor-kit-17hs4023-drv8825-bridge)
1. [12V power supply adaptor for motor driver](https://www.amazon.com/ABLEGRID-12-Volt-Power-Supply/dp/B009ZZKUPG/ref=asc_df_B009ZZKUPG/?tag=hyprod-20&linkCode=df0&hvadid=167126093426&hvpos=&hvnetw=g&hvrand=1586101707378665255&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9004405&hvtargid=pla-306189306424&psc=1)
1. [Simple USB powered webcam](https://www.amazon.com/wansview-Microphone-Streaming-Conference-Teaching/dp/B08XQ3TWFX/ref=sr_1_18_sspa?crid=31LU3CR5DFPDZ&keywords=simple+usb+webcam&qid=1680799615&sprefix=%2Caps%2C104&sr=8-18-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExQUJONDZRMUtCWkJBJmVuY3J5cHRlZElkPUEwOTAzNDQ1MlQ0TUpDU1pGQlNIWCZlbmNyeXB0ZWRBZElkPUEwNzg3NTk5Wk5KT05EQ0JUSlMzJndpZGdldE5hbWU9c3BfYnRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==)
1. [Assorted jumper wires](https://www.amazon.com/jumper-wires/s?k=jumper+wires)
1. [Four 16mm or 20mm M3 screws](https://www.amazon.com/Cicidorai-M3-0-5-Button-Machine-Quantity/dp/B09TKP6C6B/ref=sr_1_9?crid=1A33C0LT6BKRH&keywords=m3%2Bx%2B16%2Bmachine%2Bscrews%2Bbutton%2Bhead&qid=1681335923&sprefix=m3%2Bx%2B16%2Bmachine%2Bscrews%2Bbutton%2Bhead%2Caps%2C144&sr=8-9&th=1)

### Tools and Other Materials

You will also need the following tools and materials:

1. Wide mouth Mason Jar or [blender cup](https://www.amazon.com/Ninja-Single-16-Ounce-Professional-Blender/dp/B07Q23X5WP/ref=sr_1_17?crid=3TIPZDR7YTO2Q&keywords=ninja+bullet+cups&qid=1685029658&sprefix=ninja+bullet+cups%2Caps%2C84&sr=8-17) (if you want to avoid using glass!)
1. Small pet treats or dry kibble
1. Tools for assembly such as screwdrivers and allen keys
1. 3D printer, optional if you chose to use the provided STL models for this project
1. 3D printed STL models provided [here](https://github.com/viam-labs/smart-pet-feeder), or you may design your own around our component, wiring, and configuration recommendations.

### Software

You will need the following software:

* [Python 3](https://www.python.org/download/releases/3.0/)
* [Pip](https://pip.pypa.io/en/stable/#)
* [`viam-server`](https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b) installed to your {{< glossary_tooltip term_id="board" text="board" >}}. If you haven't done this, we'll walk you through it in the next section.

## Assembling your robot

You can choose to use the open source 3D printed model available to create an encasement for your robot parts, or feel free to design your own.
The STL files for the smart feeder robot are available on [GitHub](https://github.com/viam-labs/smart-pet-feeder).

For the assembly, you will need a Raspberry Pi, a stepper motor and motor driver, a power source for your Pi, a power supply for your motor driver, and a simple webcam.
When you have everything, follow these steps:

1. Prepare your 3D prints.
The front of the main body of your print is the side with the dog bone!

   {{<gif webm_src="/tutorials/img/pet-treat-dispenser/3d-print-design.webm" gif_src="/tutorials/img/pet-treat-dispenser/3d-print-design.gif" alt="Rotating 3d rendered model of the pet feeder design." class="alignright" max-width="250px">}}

1. Mount your raspberry pi to the side of the main body of your pet feeder with the provided mounting screw holes.
1. Connect your power source to the pi through the side hole.
1. Mount your webcam to the front of your pet feeder.
Insert your USB into your Pi.
1. Insert the 3D printed stepper motor wheel into your pet feeder.
This is what will funnel treats out of your pet feeder programmatically.
1. Place your stepper motor into the motor holder print and gently slide the wires through the hole that leads through the body of your feeder and lets out on the Raspberry Pi side.
1. Slide the motor driver holder into the body of your feeder, it should sit flush and fit nicely.
1. Connect your stepper motor to the motor driver.
The diagram provided details the wiring schematics for assembling your pet feeder.

   ![Wiring diagram for the pet feeder showing the components used and the wiring plan to connect them.](/tutorials/img/pet-treat-dispenser/wiring-diagram.png)

Congratulations! Now your robot should be wired correctly and you can begin to test it in the Viam app.

## Testing and configuring your robot

Now that your robot is assembled and your components have been wired, you can now proceed to configure your {{< glossary_tooltip term_id="board" text="board" >}} and test your robot:

1. Go to [the Viam app](https://app.viam.com) and create a new robot instance in your preferred organization.
1. If you haven’t already, set up the Raspberry Pi by following our [Raspberry Pi Setup Guide](https://docs.viam.com/installation/prepare/rpi-setup/).
1. Then follow the instructions on the **Setup** tab in [the Viam app](https://app.viam.com) to download the Viam app config to your Pi and install `viam-server` on your Pi.
1. Once that is complete, head to the **Config** tab and configure your `board` component, and select the model `pi`.

   ![Screenshot of the Viam app showing the configuration page for a board component with name pi.](/tutorials/img/pet-treat-dispenser/app-board-pi.png)

Next, configure your webcam:

1. Select the `camera` component and choose the model `webcam`.
1. The discovery service should automatically detect a path for your camera.

   ![Screenshot of the Viam app showing the configuration page for a camera component with model webcam.](/tutorials/img/pet-treat-dispenser/app-camera-webcam.png)

Finally, configure your stepper motor:

1. Choose the component `motor` and the model `gpiostepper`.
1. Following the provided wiring diagram, you will want to set the `direction` to pin 15, GPIO 22, and the `step` logic to pin 16, GPIO 23.
1. Enable the pin setting as low and configure it to pin 18, GPIO 24.
1. Set the `ticks per rotation` to 400 and connect it to your board model,`pi`.

   ![Screenshot of the Viam app showing the configuration page for a stepper motor component with model gpiostepper.](/tutorials/img/pet-treat-dispenser/app-stepper-gpiostepper.png)

Save all your changes, and head to the Control tab.
If your wiring is correct, you should be able to test all of your components there.
You can set the **RPM** in the control tab to 20 and 100 revolutions to see the speed of your treat dispensing mechanism.
Feel free to tweak these values to achieve the desired speed of your dispenser.

   ![Screenshot of the Viam app showing the control page for a stepper motor with RPM set to 20 and revolutions set to 100.](/tutorials/img/pet-treat-dispenser/app-control-stepper.png)

You can even test your camera and check if you can see your pet!
Your pet may be a little skeptical of your robot at first, but once you get some treats in there, your furry friend will love it in no time!

   ![Screenshot of the Viam app showing the control page for a camera with live video feed of a dog.](/tutorials/img/pet-treat-dispenser/app-control-camera.png)

## Configuring data management

Let’s make our pet feeder smart with some data capture and machine learning models!
First, you'll want to configure Viam’s [Data Management](/manage/data/) service so you can specify the location on the robot to store data.
In this case, the data we are capturing and saving is images so we can train a machine learning model on pictures of your beloved pet.
To enable the data capture on your robot, do the following:

1. Under the **Config** tab, select **Services**, and navigate to **Create service**.
Here, you will add a service so your robot can sync data to the Viam app in the cloud.
1. For **type**, select **Data Management** from the drop-down, and give your service a name.
We used `pet-data` for this tutorial.
1. Be sure that Data Capture is enabled and Cloud Sync is enabled.
Enabling data capture here will allow you to view the saved images for tagging and training your model.
You can leave the default directory in which your captured data is stored on-robot. By default, it saves it to the <file>~/.viam/capture</file> directory on your robot.

   ![Screenshot of the Viam app showing the data management service configured with name pet-data.](/tutorials/img/pet-treat-dispenser/app-service-data-management.png)

Next, enable the Data Management service on the camera component on your robot:

1. Go to the **Components** tab for your robot and scroll down to the camera component you previously configured.
1. Click **+ Add method** on the **Data Capture Configuration** section.
1. Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
This will capture an image from the camera roughly once every 3 seconds.
Feel free to adjust the frequency if you want the camera to capture more or less image data.
You want to capture data quickly so that you have as many pictures of your pet as possible so your classifier model can be very accurate.
You should also select the Mime Type that you want to capture.
For this tutorial, we are capturing `image/jpeg` data because they are images!

   ![Screenshot of the Viam app showing the configuration page for a camera component with configuration options.](/tutorials/img/pet-treat-dispenser/app-camera-configuration.png)

## Capturing images of your pet

Now it’s time to start collecting images of your beloved pet.
We recommend setting your feeder with the camera up near an area your pet likes to hang out: your couch, their bed, mount it temporarily over their food bowl, or even just hold it in front of them for a couple of minutes.
You can check that data is being captured by heading over to the **DATA** tab of the Viam app and filtering to your pet feeder robot location.
Capture as many images as you want and then you can begin to train your custom model.
Disable Data Capture after you’re done capturing images of your pet.

## Turning your pet feeder smart with machine learning

Now that you know how to configure the Data Management Service on your robot, how to collect image based data, and how to export that data; you can go a step further and tag and train image classification models that you can then deploy to your robot.

Head over to the **Data** page of the Viam App and select an image captured from your robot.
After selecting the image, you can type a custom tag for some of the objects you see in the image.
The first thing you want to consider is what tags you are trying to create and how you want your custom model to function.

![Screenshot of the Viam app showing the images tab of the data page with a number of images of the dog.](/tutorials/img/pet-treat-dispenser/app-data-images.png)

## Tagging images

In this example case here, we are tagging images with the name of the pet.
Notice that in our image collection, we captured images at different angles and with different background compositions.
This is to ensure that our model can continue to recognize the object no matter how your robot is viewing it through its camera.

Begin by selecting the image you would like to tag, and you will see all of the data that is associated with that image.
Simply type in your desired tag in the Tags section.

![Screenshot of the Viam app showing the images detail pane of the data page shown selecting tags for an image.](/tutorials/img/pet-treat-dispenser/app-data-tags.png)

Be mindful of your naming as you can only use alphanumeric characters and underscores: this is because the model will be exported as a `.tflite` file as well as a corresponding `.txt` file for labeling.

Congratulations! You have successfully tagged your images with the labels you would like to train your model with.
Note we are just tagging the whole image as we are training an image classification model.

![Screenshot of the Viam app showing the recently-used tags search window.](/tutorials/img/pet-treat-dispenser/app-data-recently-used.png)

Continue parsing through your collected data (in this case images) and tag away to your heart's desire.
Once you create tags, it is as simple as selecting your image and then selecting the tag in the **Recently used** drop down menu.
Tag as many images with as many tags until you are happy with your dataset.
This is important for the next step.

## Filtering through tags

Say you want to only view images in your data set that belong to a certain tag.
Upon completion of tagging your data set, you can now filter images according to those tags.
It is as simple as heading over to the Filtering tab and selecting your desired tag from the available drop down list.
Here we have filtered images in our data set according to one tag, in this case `toast`, (which is the name of our doggy test subject!) and now we can easily view those.

![Screenshot of the Viam app showing the filtering tab with toast entered as a filtered tag.](/tutorials/img/pet-treat-dispenser/app-data-filter-tags.png)

## Training a model

After filtering through your desired tags, you can then select as many as you like to begin to train a model.
In this case, we are selecting all the tags we generated for the images collected from this robot.

And now the moment we’ve all been waiting for ... after selecting all desired tags you can train a model.
Simply click the **Train Model** button and you can then name your model and choose your classification type.
Here we called it `puppymodel` as a **Single label** model type and selected the tag `toast` to train on images of the pup!  

![Screenshot of the Viam app showing the data page with single model selected using name puppymodel.](/tutorials/img/pet-treat-dispenser/app-training.png)

Selecting **Single Label** means your results will include a single predicted label for an image.
Selecting **Multi Label** means your results will include all predicted labels for an image.
Go ahead and select all the tags you would like to include in your model and click **Train Model**.
This is important because your model will only be trained based on the tags you selected here.

## Deploying Your Model to Your Robot

1. Add a ML model service:

   1. To deploy a new model onto your robot, navigate to the robot page on the Viam app, and in the **Config** tab, select **Services**.
   1. Create a new service, select **ML Model** as the **Type**, and name it whatever you like.
   Here we use `puppymodel` for the **name**, and selecting `tflite_cpu` under **Model**.
   For more information, see [ML Model Service](https://docs.viam.com/services/ml/#tabset-servicesml-1-1).

   ![Screenshot of the Viam app showing the ML model service page with name puppymodel.](/tutorials/img/pet-treat-dispenser/app-service-mlmodel.png)

   1. To configure your service and deploy a model onto your robot, select **Deploy Model On Robot** for the **Deployment** field.
   1. Select your trained model (**puppymodel)** as your desired Model.

1. Add a vision service:

   1. Create a new **Service** and select **Vision**, and `mlmodel` as the Type.
   1. Select the model you previously created in the drop down menu.

   ![Screenshot of the Viam app showing the vision service page with name puppyclassifier.](/tutorials/img/pet-treat-dispenser/app-service-vision.png)

1. Add a transform camera:

   1. To test that your vision service is working, add a `transform` camera to see your classifier in action in the Control tab.
   1. Navigate to the **Components** tab and click **Create Component**.
   1. Create a transform camera with the name `classifier_cam`, the type `camera` and the model `transform`.
   1. Replace the JSON attributes with the following object which specifies the camera source the transform cam we will be using, and also defines a pipeline that adds a `classifier` you created.

   ```js
      {
      "source": "petcam",
      "pipeline": [
        {
          "attributes": {
            "classifier_name": "puppyclassifier",
            "confidence_threshold": 0.9
          },
          "type": "classifications"
        }
      ]
      }

   ```

   1. Head to your robots **Control** tab and you should be able to view your transform cam that is now detecting your pets face!

   ![Image of a dog sitting being recognized as a match by the training model.](/tutorials/img/pet-treat-dispenser/dog-model-matched.png)

## Controlling your robot programmatically

Now you can add a program to your robot that controls the pet feeder when executed, using a [Viam SDK](/program/sdks/) in the language of your choice.

Go to your robot’s page on [the Viam app](https://app.viam.com), navigate to the **Code Sample** tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

## Setting up your python environment

Open your terminal and `ssh` into your Pi.
Run the following command to install the Python package manager onto your Pi:

```sh
sudo apt install python3-pip
```

The [Viam Python SDK](https://python.viam.dev/) allows you to write programs in the Python programming language to operate robots using Viam.
To install the Python SDK on your Raspberry Pi, run the following command in your existing `ssh` session to your Pi:

```sh
pip3 install viam-sdk
```

Next, create a file on the Raspberry Pi and edit the file with `nano`.

Run the following command to create a folder in your home directory to put your files in. We named ours `petfeeder`:

```sh
mkdir ~/petfeeder
```

Next, navigate to the new project directory:

```sh
cd ~/petfeeder
```

Create a file using `nano` by choosing a file name and ending it with `.py` . We’ll call ours `main.py`:

```sh
nano main.py
```

## Connect

Head to the **Code Sample** tab and copy the boilerplate code sample into **main.py** and save it.
Here is a sample of what your code will look like without some of the sample return value methods provided just to keep the code looking clean.
Add a [`go_for()` method](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.go_for) to confirm that your code is connected to your robot.
Your stepper motor should turn ten times!

```python
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.camera import Camera
from viam.components.motor import Motor
from viam.services.vision import VisionClient

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='<YOUR ROBOT SECRET HERE>')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('<YOUR HOST ADDRESS HERE>', opts)

async def main():
    robot = await connect()
    # Robot components + services 
    pi = Board.from_robot(robot, "pi")
    petcam = Camera.from_robot(robot, "petcam")
    stepper = Motor.from_robot(robot, "stepper")
    classifier_cam = Camera.from_robot(robot, "classifier_cam")
    puppyclassifier = VisionClient.from_robot(robot, "puppyclassifier")

    # Go for method to turn your stepper motor 
    await stepper.go_for(rpm=10,revolutions=1)

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Press CTRL-X to save and exit. Enter `y` to confirm, and then hit return to accept the same filename.

Now, run the code to see your stepper motor turn to check the connection, and to see if there are any errors.

```sh
python3  main.py
```

## Adding the classifier

This section forthcoming.

## Summary

Congratulations! You've earned the love and respect of your pet! Celebrate by treating yourself to one of your pet's treats -- you've earned it!
