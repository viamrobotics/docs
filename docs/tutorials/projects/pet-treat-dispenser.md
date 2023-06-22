---
title: "Build a Smart Pet Feeder with Machine Learning"
linkTitle: "Smart Pet Treat Dispenser"
weight: 50
type: "docs"
description: "Use a Raspberry Pi, a motor, and machine learning to build a smart pet feeder."
tags: ["raspberry pi", "app", "board", "motor"]
image: "/tutorials/img/pet-treat-dispenser/preview.png"
imageAlt: "Image of a dog interacting with the smart pet feeder."
images: ["/tutorials/img/pet-treat-dispenser/preview.png"]

# Author: Arielle
# Designs: Jessamy
---

<div class="td-max-width-on-larger-screens">
<img src="../../img/pet-treat-dispenser/pet-feeder.png" alt="Image of a dog interacting with the smart pet feeder." width="250px" class="alignright">
</div>

If your dog is as insatiable as mine, you are familiar with having to wake up every morning to the sound of gentle whining at the door and the pitter patter of begging paws on the floor - two hours before the alarm.
The sun has barely risen on the horizon as you glance out your east facing window, and you can see a moist nose peering under your door frame.
Your dog commands you: it’s time to eat.

To allow myself to get some extra zzz’s before work, I've built a robot to feed my dog in the morning.
It has also come in useful to give him some treats for being a Good Boy™ while I'm spending my day at the office.

In this tutorial you can follow along and build your own pet feeder.
You will use the Viam app's [Data Manager](/manage/data/) to train a custom machine learning model that recognizes your pet and use the [Machine Learning Service](/services/ml/) and the [Vision Service](/services/vision/) to use it on your robot.
The final component is a stepper motor and a 3D printed model which holds and dispenses treats when your pet is recognized.

## Requirements

### Hardware

You will need the following hardware components:

1. A computer running macOS or Linux
1. [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) with [microSD card](https://www.amazon.com/Amazon-Basics-microSDXC-Memory-Adapter/dp/B08TJTB8XS/ref=sr_1_4) (and [microSD card reader](https://www.amazon.com/Card-Reader-Beikell-Memory-Adapter/dp/B09Z6JCKL7/ref=sr_1_3)), with `viam-server` installed following the [Installation Guide](/installation/).
1. [Raspberry Pi power supply](https://www.amazon.com/Raspberry-Model-Official-SC0218-Accessory/dp/B07W8XHMJZ/ref=asc_df_B07W8XHMJZ/)
1. [Stepper motor and motor driver](https://makersportal.com/shop/nema-17-stepper-motor-kit-17hs4023-drv8825-bridge)
1. [12V power supply adaptor for motor driver](https://www.amazon.com/ABLEGRID-12-Volt-Power-Supply/dp/B009ZZKUPG/ref=asc_df_B009ZZKUPG/)
1. [Simple USB powered webcam](https://www.amazon.com/wansview-Microphone-Streaming-Conference-Teaching/dp/B08XQ3TWFX/ref=sr_1_18_sspa)
1. Assorted jumper wires
1. [Four 16mm or 20mm M3 screws](https://www.amazon.com/Cicidorai-M3-0-5-Button-Machine-Quantity/dp/B09TKP6C6B/ref=sr_1_9)

### Tools and Other Materials

You will also need the following tools and materials:

1. Wide mouth Mason Jar or [blender cup](https://www.amazon.com/Ninja-Single-16-Ounce-Professional-Blender/dp/B07Q23X5WP/ref=sr_1_17) (if you want to avoid using glass!)
1. Small pet treats or dry kibble
1. Tools for assembly such as screwdrivers and allen keys
1. 3D printer (or somewhere you can order 3D printed parts from)
1. [3D printed STL models](https://github.com/viam-labs/smart-pet-feeder), wiring, and configuration recommendations.

### Software

You will need the following software:

* [Python 3](https://www.python.org/download/releases/3.0/)
* [pip](https://pip.pypa.io/en/stable/#)
* [`viam-server`](/installation/#install-viam-server) installed to your {{< glossary_tooltip term_id="board" text="board" >}}.
If you haven't done this, we'll walk you through it in the next section.

## Assemble your robot

The STL files for the smart feeder robot are available on [GitHub](https://github.com/viam-labs/smart-pet-feeder).

1. Prepare your 3D prints.
The front of the main body of your print is the side with the dog bone.

{{<gif webm_src="../../img/pet-treat-dispenser/3d-print-design.webm" mp4_src="../../img/pet-treat-dispenser/3d-print-design.gif" alt="Rotating 3d rendered model of the pet feeder design." class="alignright" max-width="300px" class="aligncenter">}}

2. Mount your Raspberry Pi to the side of the main body of your pet feeder using the provided mounting screw holes.
1. Connect your power source to the Pi through the side hole.
1. Mount your webcam to the front of your pet feeder.
Connect the USB cable to your Pi.
1. Insert the 3D printed stepper motor wheel into your pet feeder.
This is what will funnel treats out of your pet feeder programmatically.
1. Place your stepper motor into the motor holder part and gently slide the wires through the hole that leads through the body of your feeder and feeds the cables out on the Raspberry Pi side.
1. Slide the motor driver holder into the body of your feeder, it should sit flush and fit nicely.
1. Connect your stepper motor to the motor driver according to this wiring diagram:

   ![Wiring diagram for the pet feeder showing the components used and the wiring plan to connect them.](../../img/pet-treat-dispenser/wiring-diagram.png)

## Configure and test your robot

Now that you've set up your robot, you can start configuring and testing it.

1. If you haven’t already, set up the Raspberry Pi by following our [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/).
1. Go to [the Viam app](https://app.viam.com) and create a new robot instance in your preferred organization.
1. Then follow the instructions on the **Setup** tab.

{{< tabs >}}
{{% tab name="Builder UI" %}}

### Configure your {{< glossary_tooltip term_id="board" text="board" >}}

Head to the **Config** tab on your robot's page.
Click on the **Components** subtab and navigate to the **Create component** menu.

Select `board` as the type and `pi` as the model.
Name the component `pi`.

![The Viam app showing the configuration page for a board component with name pi.](../../img/pet-treat-dispenser/app-board-pi.png)

### Configure your [webcam](/components/camera/webcam/)

Add another component with the type `camera` component and the model `webcam`.
Name the component `petcam`.

Click on the **video path**.
If the robot is connected, a drop down with available cameras will appear.
Select your camera.

![The Viam app showing the configuration page for a camera component with model webcam.](../../img/pet-treat-dispenser/app-camera-webcam.png)

{{< alert title="Tip" color="tip" >}}
If you are unsure which camera to select, selecte one, save the configuration and go to the [**Control** tab](/components/camera/webcam/#view-the-camera-stream) to confirm you can see the expected video stream.
{{< /alert >}}

### Configure your [stepper motor](/components/motor/gpiostepper/)

Finally, add another component with the type `motor` component and the model `gpiostepper`.

1. If you used the same pins as in the wiring diagram, set the `direction` to pin 15 GPIO 22, and the `step` logic to pin 16 GPIO 23.
1. Enable the pin setting as low and configure it to pin 18 GPIO 24.
1. Set the `ticks per rotation` to `400` and select your board model,`pi`.

![The Viam app showing the configuration page for a stepper motor component with model gpiostepper.](../../img/pet-treat-dispenser/app-stepper-gpiostepper.png)

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following JSON configuration for your {{< glossary_tooltip term_id="board" text="board" >}}, your [webcam](/components/camera/webcam/), and your [stepper motor](/components/motor/gpiostepper/):

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "attributes": {},
      "depends_on": [],
      "name": "pi",
      "type": "board",
      "model": "pi"
    },
    {
      "attributes": {
        "video_path": "usb-GENERAL_GENERAL_WEBCAM-video-index0"
      },
      "depends_on": [],
      "name": "petcam",
      "type": "camera",
      "model": "webcam"
    },
    {
      "depends_on": [],
      "name": "stepper",
      "type": "motor",
      "model": "gpiostepper",
      "attributes": {
        "pins": {
          "en_low": "18",
          "step": "16",
          "dir": "15"
        },
        "board": "pi",
        "ticks_per_rotation": 400
      }
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

To test everything is wired and configured correctly, head to the [Control tab](/manage/fleet/robots/#control).
Start by testing the motor.
Click on the motor panel and set the **RPM** to 20 and **# of Revolutions** to 100 to see your treat dispensing mechanism in action.
Feel free to tweak these values to achieve the desired speed of your dispenser.

![The Viam app showing the control page for a stepper motor with RPM set to 20 and revolutions set to 100.](../../img/pet-treat-dispenser/app-control-stepper.png)

Next, test your camera.
Click on the camera panel and toggle the camera on.
Now check if you can see your pet!
Your pet may be a little skeptical of your robot at first, but once you get some treats in there, your furry friend will love it in no time!

![The Viam app showing the control page for a camera with live video feed of a dog.](../../img/pet-treat-dispenser/app-control-camera.png)

## Use machine learning to recognize your pet

Let’s make our pet feeder smart with some data capture and machine learning models!
To do that, you'll first have to configure [Data Management](/manage/data/) to capture images.
Then you can use these images to train a machine learning model on your pet.

### Configure data management

To enable the [data capture](/services/data/configure-data-capture/) on your robot, do the following:

1. Under the **Config** tab, select **Services**, and navigate to **Create service**.
Here, you will add a service so your robot can sync data to the Viam app in the cloud.
1. For **type**, select **Data Management** from the drop-down, and give your service a name.
We used `pet-data` for this tutorial.
1. Ensure that **Data Capture** is enabled and **Cloud Sync** is enabled.
Enabling data capture here will allow you to view the saved images in the Viam app and allow you to easily tag them and train your own machine learning model.
You can leave the default directory as is.
This is where your captured data is stored on-robot.
By default, it saves it to the <file>~/.viam/capture</file> directory on your robot.

![The data management service configured with the name pet-data.](../../img/pet-treat-dispenser/app-service-data-management.png)

Next, enable the Data Management service on the camera component on your robot:

1. Go to the **Components** tab and scroll down to the camera component you previously configured.
1. Click **+ Add method** in the **Data Capture Configuration** section.
1. Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
This will capture an image from the camera roughly once every 3 seconds.
Feel free to adjust the frequency if you want the camera to capture more or less image data.
You want to capture data quickly so that you have as many pictures of your pet as possible so your classifier model can be very accurate.
You should also select the Mime Type that you want to capture.
For this tutorial, we are capturing `image/jpeg` data.

![The configuration page for a camera component.](../../img/pet-treat-dispenser/app-camera-configuration.png)

### Capture images of your pet

Now it’s time to start collecting images of your beloved pet.
Set your feeder up near an area your pet likes to hang out like your couch or their bed or mount it temporarily over their food bowl, or even just hold it in front of them for a couple of minutes.
You can check that data is being captured by heading over to the [**DATA** page](https://app.viam.com/data/view) and filtering your image data to show just images from the {{< glossary_tooltip term_id="location" text="location" >}} your pet feeder is in.
Capture as many images as you want.
If possible, capture your pet from different angles and with different backgrounds.
Disable Data Capture after you’re done capturing images of your pet.

### Tag images

Head over to the [**DATA** page](https://app.viam.com/data/view) and select an image captured from your robot.
After selecting the image, you can type a custom tag for some of the objects you see in the image.
The first thing you want to consider is what tags you are trying to create and how you want your custom model to function.

![The images tab of the data page with a number of images of the dog.](../../img/pet-treat-dispenser/app-data-images.png)

For the treat dispenser, you can tag images with the name of the pet.
Notice that in our image collection, we captured images at different angles and with different background compositions.
This is to ensure that our model can continue to recognize the object no matter how your robot is viewing it through its camera.

Begin by selecting the image you would like to tag, and you will see all of the data that is associated with that image.
Type in your desired tag in the Tags section.

![The images detail pane of the data page shown selecting tags for an image.](../../img/pet-treat-dispenser/app-data-tags.png)

Be mindful of your naming as you can only use alphanumeric characters and underscores: this is because the model will be exported as a `.tflite` file with a corresponding `.txt` file for labeling.

Add tags for each image that shows your pet.

![The recently-used tags search window.](../../img/pet-treat-dispenser/app-data-recently-used.png)

Note we are just tagging the whole image as we are training an image classification model.

Continue parsing through your collected data (in this case images) and tag away to your heart's desire.
Once you create tags, it is as simple as selecting your image and then selecting the tag in the **Recently used** drop down menu.
Tag as many images with as many tags until you are happy with your dataset.
This is important for the next step.

### Filter based on tags

Upon completion of tagging your data set, you can now [filter images](/manage/data/view/) according to those tags.
Head over to the **Filtering** menu and select a tag from the drop down list.
In the following screenshot, we have filtered the images in our data set according to one tag, in this case `toast`, (which is the name of our doggy test subject) and now we can easily view all images of Toast:

![The filtering tab with toast entered as a filtered tag.](../../img/pet-treat-dispenser/app-data-filter-tags.png)

### Train a model

After tagging and filtering your images so only the pictures of your pet are visible, begin training your model.
Click the **Train Model** button, name your model and select **Single label** as the model type.
Then select the label that you sued to label your pet images.
We called it `puppymodel` and selected the tag `toast` to train on images of the pup.

![The data page with single model selected using name puppymodel.](../../img/pet-treat-dispenser/app-training.png)

If you want your model to be able to recognize multiple pets you can instead create a **Multi Label** model based on multiple tags.
Go ahead and select all the tags you would like to include in your model and click **Train Model**.

### Deploy your model to your robot

Once the model has finished training, deploy it by adding a [ML model service](/services/ml/#tabset-servicesml-1-1):

1. To deploy a new model onto your robot, navigate to the robot page on the Viam app, and in the **Config** tab, select **Services**.
1. Create a new service, select **ML Model** as the **Type**, and name it `puppymodel`.
Select `tflite_cpu` as the **Model**.

![The ML model service panel with the name puppymodel.](../../img/pet-treat-dispenser/app-service-mlmodel.png)

3. To configure your service and deploy a model onto your robot, select **Deploy Model On Robot** for the **Deployment** field.
1. Select your trained model (`puppymodel`) as your desired **Model**.

### Use the Vision Service to detect your pet

To detect your pet with your machine learning model, you need to add a [vision service](/services/vision/) that uses the model and a [transform camera](/components/camera/transform/) that applies the vision service to an existing camera stream and specifies a confidence threshold:

1. Create a new **Service** and select **Vision**, and `mlmodel` as the Type.
1. Select the model you previously created in the drop down menu.

   ![The vision service panel with the puppymodel selected.](../../img/pet-treat-dispenser/app-service-vision.png)

1. Navigate to the **Components** tab and scroll to the **Create Component** menu.
1. Create a [transform camera](/components/camera/transform/) with the name `classifier_cam`, the type `camera` and the model `transform`.
1. Replace the JSON attributes with the following object which specifies the camera source for the transform cam and also defines a pipeline that adds the `classifier` you created.

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

1. Head to your robots **Control** tab, click on your transform cam, toggle it on and you should be able to view your transform cam and if pointed at your pet, it should show it detecting your pet!

<img src="../../img/pet-treat-dispenser/dog-model-matched.png" alt="Image of a dog sitting being recognized as a match by the training model." width="400px" class="aligncenter">

## Control your robot programmatically

With your robot configured, you can now add a program to your robot that controls the pet feeder when executed, using the [Viam SDK](/program/apis/) in the language of your choice.
This tutorial uses Python.

### Set up your python environment

Open your terminal and `ssh` into your Pi.
Run the following command to install the Python package manager onto your Pi:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt install python3-pip
```

Create a folder named <file>petfeeder</file> for your code and create a file called <file>main.py</file> inside.

The [Viam Python SDK](https://python.viam.dev/) allows you to write programs in the Python programming language to operate robots using Viam.
To install the Python SDK on your Raspberry Pi, run the following command in your existing `ssh` session to your Pi:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install --target=petfeeder viam-sdk python-vlc
```

{{< alert title="Note" color="note" >}}
If you want your robot to automatically run your code upon startup, it is important to install the package into the <file>petfeeder</file> folder because of how the Viam platform runs the process.
{{< /alert >}}

### Add the connection code

Go to your robot’s page on [the Viam app](https://app.viam.com) and navigate to the **Code sample** tab.
Select **Python**, then copy the generated sample code and paste it into the <file>main.py</file> file.

{{% snippet "show-secret.md" %}}

Save the file and run this command to execute the code:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

When executed, this sample code connects to your robot as a client and prints the available resources.

### Add the logic

If your program ran successfully and you saw a list of resources printed from the program, you can continue to add the robot logic.

You'll be using the `puppyclassifier`.
The following code initializes a camera and the puppyclassifier and shows you how to get the classifications from the classifier when passing in the camera stream as an argument:

```python
petcam = Camera.from_robot(robot, "petcam")
puppyclassifier = VisionClient.from_robot(robot, "puppyclassifier")
classifications = await puppyclassifier.get_classifications_from_camera(camera_name)
```

Remove the existing code in the `main` function and replace it with the following logic where the the code gets classifications from the puppyclassifier based on the camera stream, and if a pet is found, activates the stepper motor using the [`go_for()` method](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.go_for) to move a certain amount to dispense a treat.

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()

    # robot components + services below, update these based on how you named them in configuration
    pi = Board.from_robot(robot, "pi")
    petcam = Camera.from_robot(robot, "petcam")
    stepper = Motor.from_robot(robot, "stepper")
    puppyclassifier = VisionClient.from_robot(robot, "puppyclassifier")

    while True:
        # look if the camera is seeing the dog
        found = False
        classifications = await puppyclassifier.get_classifications_from_camera(camera_name)
        for d in classifications:
            # check if the model is confident in the classification
            if d.confidence > 0.7:
                print(d)
                if d.class_name.lower() == "toastml":
                    print("This is Toast")
                    found = True

        if (found):
            # turn on the stepper motor
            print("giving snack")
            state = "on"
            await stepper.go_for(rpm=80,revolutions=2)
            # stops the treat from constantly being dispensed
            time.sleep(300)

        else:
            # turn off the stepper motor
            print("it's not the dog, no snacks")
            state = "off"
            await stepper.stop()

        await asyncio.sleep(5)

        # don't forget to close the robot when you're done!
        await robot.close()


if __name__ == '__main__':
    asyncio.run(main())
```

Save your file and run the code, put your pet in front of the robot to check it works:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

## Run the program automatically

One more thing.
Right now, you need to run the code manually every time you want your robot to work.
However, you can configure Viam to automatically run your code as a [process](/manage/configuration/#processes).

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Processes** subtab and navigate to the **Create process** menu.

Enter `main` as the process name and click **Create process**.

In the new process panel, enter `python3` as the executable, `main.py` as the argument, and the working directory of your Raspberry Pi as `/home/pi/petfeeder`.
Click on **Add argument**.

Click **Save config** in the bottom left corner of the screen.

Now your robot starts looking for your pet automatically once booted!

## Full Code

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import os
import time

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.camera import Camera
from viam.components.motor import Motor
from viam.services.vision import VisionClient

# these must be set, you can get them from your robot's 'Code sample' tab
robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

# change this if you named your camera differently in your robot configuration
camera_name = os.getenv('ROBOT_CAMERA') or 'petcam'

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

    # robot components + services below, update these based on how you named them in configuration
    pi = Board.from_robot(robot, "pi")
    petcam = Camera.from_robot(robot, "petcam")
    stepper = Motor.from_robot(robot, "stepper")
    puppyclassifier = VisionClient.from_robot(robot, "puppyclassifier")

    while True:
        # look if the camera is seeing the dog
        found = False
        classifications = await puppyclassifier.get_classifications_from_camera(camera_name)
        for d in classifications:
            # check if the model is confident in the classification
            if d.confidence > 0.7:
                print(d)
                if d.class_name.lower() == "toastml":
                    print("This is Toast")
                    found = True

        if (found):
            # turn on the stepper motor
            print("giving snack")
            state = "on"
            await stepper.go_for(rpm=80,revolutions=2)
            # stops the treat from constantly being dispensed
            time.sleep(300)

        else:
            # turn off the stepper motor
            print("it's not the dog, no snacks")
            state = "off"
            await stepper.stop()

        await asyncio.sleep(5)

        # don't forget to close the robot when you're done!
        await robot.close()


if __name__ == '__main__':
    asyncio.run(main())
```

## Next Steps

Take your smart pet feeder to the next level!
You could try one of the following:

* Add speakers and record your voice so that the pet feeder can play a message to your pet each time it dispenses a treat.
* Train a [ML model](/services/ml/) to recognize when your pet performs a trick, and withhold the treat until a specific trick is detected.
* Add a button that your pet must press to access the treat. If you add several treat types, you might include a different color button for each treat type, allowing your pet to choose.
* If you have multiple pets, you could configure different treats for each pet by training the ML model on each pet, and dispensing different treats depending on the pet recognized.

For more robotics projects, check out our [other tutorials](/tutorials/).
