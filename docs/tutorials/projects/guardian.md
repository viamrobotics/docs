---
title: "Security Guardian"
linkTitle: "Security Guardian"
weight: 50
type: "docs"
description: "Make a functional guardian with a servo motor, some LEDs, a camera, and the ML and Vision Service to detect people and pets."
webmSrc: "/tutorials/videos/foam-dart.webm"
mp4Src: "/tutorials/videos/foam-dart.mp4"
videoAlt: "A guardian detecting a person or pet."
images: ["/tutorials/img/guardian/preview.gif"]
tags: ["camera", "vision", "detector", "python"]
# Author: Naomi Pentrel
---

In the run up to the new Zelda release, I decided to build my very own personal guardian.
Luckily, I am not the first one to have the idea to build a guardian and there was already a brilliant guardian 3D model.
This model was made hackable by ... and some folks added a servo and LEDs and ultrasonic sensors.
The guardian I built, goes one step further and makes the robot smart enough to be able to detect people and pets and follow them around the room by rotating its head.
All powered by the [ML Service](/services/ml/) and the [Vision Service](/services/vision/).

<!-- ADD GRAPHIC -->

## Hardware requirements

You need the following hardware for this tutorial:

- A Raspberry Pi + power cable
- A Raspberry Pi Camera v1.3 + 50cm ribbon cable
- 3x 10mm RGB LEDs with common cathode
- A  180  servo
- cables
- 4x M2 screws
- The following printed 3D parts:
  - Head
- Decoration materials (Optional)
  - Acrylic paint
  - modeling grass, stones
  - A base for the guardian
  - Wire

## Software requirements

You will use the following software in this tutorial:

- [Python 3.8 or newer](https://www.python.org/downloads/)
- [`viam-server`](/installation#install-viam-server)
- [Viam Python SDK](https://python.viam.dev/)
  - The Viam Python SDK (software development kit) lets you control your Viam-powered robot by writing custom scripts in the Python programming language.
  Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).

## Assemble the robot

<!-- TIME LAPSE -->

To make the guardian's lights shine through just like the real one, you need to use filament that allows the light to shine through and then paint the parts that shouldn't allow light to shine through.
Of course, painting and decorating the guardian is entirely optional.

### Assemble for testing

To assemble the guardian, start with the head and use four M2 screws to screw the camera with attached ribbon cable to the front half of the head.
Then put both parts of the head together.

Your servo probably came with a plastic horn for the gear and mounting screws, use the screws to attach the horn to the base of the head.
Get your Raspberry Pi and your servo and connect the servo to the Raspberry Pi by connecting the PWM wire to pin 12, the power wire to pin 2, and the ground wire to pin 8.
Then attach the head to the servo.

![A Raspberry Pi connected to a FS90R servo. The yellow PWM wire is attached to pin twelve on the raspberry pi. The red five-volt wire is attached to pin two. The black ground wire is attached to pin eight](/tutorials/img/single-component-tutorials-servo-mousemover/servo-wiring-diagram.png).

Next, get the three 10mm RGB LEDs ready.
Attach the common cathode of each LED to a [ground pin](https://pinout.xyz/pinout/ground) on your Raspberry Pi.
Attach the wires for the red and the blue LEDs to [GPIO pins](https://pinout.xyz/pinout/wiringpi).

To be able to test the components, you need to install `viam-server` and configure your components.

### Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new robot called `guardian`.

Go to the **Setup** tab of your new robot's page and follow the steps [to install `viam-server` on your computer](/installation).

### Configure the components

{{< tabs >}}
{{% tab name="Builder UI" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.

1. **Add the board.**

    Enter `local` for the name for your [board component](/components/board/), select the type `board`, and select the `pi` model.
    Then click **Create component**.

2. **Add the camera.**

    Create a [camera component](/components/camera/) with the name `cam`, the type `camera` and the model `webcam`.
    Click **Create Component** to add the camera.
    In the new camera panel, click the **Video Path** field to reveal a drop-down populated with camera paths that have been identified on your machine.
    Select `video0`.

3. **Add the servo.**

    Create a [servo component](/components/servo/) with the name `servo`, the type `servo` and the model `pi`.
    Click **Create Component** to add the servo.
    Configure the attributes, by adding the name of your board `local` and the pin you connected your servo to `12`:

    ```json
    {
        "pin": "12",
        "board": "local"
    }
    ```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following configuration which configured your board, your camera, and your servo on pin `12`:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "cam",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "servo",
      "type": "servo",
      "model": "pi",
      "attributes": {
        "pin": "12",
        "board": "local"
      },
      "depends_on": [
        "local"
      ]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

### Test the components

Navigate to your [robot's Control tab](/manage/fleet/robots/#control) to test your components.
Click on the servo panel and increase or decrease the servo angle to test that the servo moves.

Next, click on the board panel.
The board panel allows you to get and set pin states.
Set the pin states for the pins your LEDs are connected to to high to test that they light up.

Next, click on the camera panel and toggle the camera on to test that you get video from your camera.

### Assemble and decorate

Now that you have tested your components, you can paint and decorate your guardian and then put the rest of the guardian together.
Remove the servo horn, and place one LED in the back of the Guardian head, leaving the wires hanging out behind the ribbon camera.

Then place the servo inside the Guardian body and attach the horn on the head to the servo's gear.
Carefully place the remaining two LEDs in opposite directions inside the body.
Thread all the cables through the hole in the lid for the base of the guardian, and close the lid.

Use a suitable base with a hole, like a box with a hole cut into the top, to place your guardian on top of and reconnect all the wires to the Raspberry Pi.

Then test the components on the [robot's Control tab](/manage/fleet/robots/#control) again to ensure everything still works.

## Detect persons, dogs, cats, and teddy bears

For the guardian to be able to detect living beings, you need to use [this Machine Learning model](LINK).
The model can detect a variety of things which you can see in the associated <file>labels.txt</file> file.
For the guardian you're building, the ones you're most likely going to be interested in are `Person`, `Dog`, `Cat`, and, if you have a particularly teddy-bear-like dog, `Teddy bear`.

You can choose different labels, or [train your own custom model](/manage/ml/train-model/) based on images from your robot but the provided Machine Learning model should be good to start with.

To use the provided Machine Learning model, copy the [<file>effdet0.tflite</file>](LINK) file and the [<file>labels.txt</file>](LINK) to your Raspberry Pi.

{{< tabs >}}
{{% tab name="Builder UI" %}}

Next, navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Services** subtab and navigate to the **Create service** menu.

1. **Add a ML service.**

   The [ML model service](/services/ml) allows you to deploy the provided machine learning model to your robot.
   Create an ML model with the name `mlmodel`, the type `mlmodel` and the model `tflite_cpu`.
   Then click **Create Service**.

   In the new ML Model panel, select **Path to Existing Model On Robot** for the **Deployment**.

   Then specify the absolute **Model Path** as `/home/pi/effdet0.tflite` and the **Label Path** as `/home/pi/labels.txt`.

2. **Add a vision service.**

   Next, add a [detector](/services/vision/detector) as a vision service to be able to make use of the ML model.
   Create an vision service with the name `detector`, the type `vision` and the model `mlmodel`.
   Then click **Create Service**.

   In the new detector panel, select the `mlmodel` you configured in the previous step.

   Click **Save config** in the bottom left corner of the screen.

3. **Add a `transform` camera.**

   To be able to test that the vision service is working, add a `transform` camera which will add bounding boxes and labels around the objects the service detects.

   Click on the **Components** subtab and navigate to the **Create component** menu.
   Create a [transform camera](/components/camera/transform) with the name `transform_cam`, the type `camera` and the model `transform`.

   Replace the attributes JSON object with the following:

   ```json
   {
   "source": "cam",
   "pipeline": [
       {
       "type": "detections",
       "attributes": {
           "detector_name": "detector",
           "confidence_threshold": 0.6
       }
       }
   ]
   }
   ```

   Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}

{{% tab name="Raw JSON" %}}

Next, on the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following configuration which configures the [ML model service](/services/ml), the [vision service](/services/vision), and a [transform camera](/components/camera/transform):

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "cam",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "servo",
      "type": "servo",
      "model": "pi",
      "attributes": {
        "pin": "12",
        "board": "local"
      },
      "depends_on": [
        "local"
      ]
    },
    {
      "name": "transform_cam",
      "type": "camera",
      "model": "transform",
      "attributes": {
        "source": "cam",
        "pipeline": [
          {
            "attributes": {
              "detector_name": "detector",
              "confidence_threshold": 0.6
            },
            "type": "detections"
          }
        ]
      },
      "depends_on": []
    }
  ],
  "services": [
    {
      "name": "mlmodel",
      "type": "mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "model_path": "/home/pi/effdet0.tflite",
        "label_path": "/home/pi/labels.txt",
        "num_threads": 1
      }
    },
    {
      "name": "detector",
      "type": "vision",
      "model": "mlmodel",
      "attributes": {
        "mlmodel_name": "mlmodel"
      }
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

Navigate to your [robot's Control tab](/manage/fleet/robots/#control) to test the transform camera.
Click on the transform camera panel and toggle the camera on, then point your camera at a person or pet to test if the vision service detects them.
You should see a bounding box with label around the person, pet, or object.

## Program the Guardian

With the guardian completely configured and the configuration tested, it's time to program the guardian to behave like a real guardian.
The following sections walk you through each part of the code.
The full code is available on [GitHub](LINK).

### Set up the Python environment

We are going to use Virtualenv to set up a virtual environment for this project, in order to isolate the dependencies of this project from other projects.
Run the following commands in your command-line to install virtualenv, set up an environment `venv` and activate it:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

Now, install the Python SDK:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install viam-sdk
```

### Connect

Next, go to the **Code Sample** tab on your robot page and select **Python**.

Copy the boilerplate code.
This code snippet imports all the necessary packages and sets up a connection with the Viam app in the cloud.

Next, create a file named <file>main.py</file> and paste the boilerplate code from the **Code Sample** tab of the Viam app into your file.
Then, save your file.

Run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

The program should print a list of robot resources.

On top of the packages that the code sample snippet imports, add the `random` package to the imports.
The top of your code should now look like this:

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import random

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.camera import Camera
from viam.components.servo import Servo
from viam.services.vision import VisionClient

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='SECRET_FROM_VIAM_APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ADDRESS_FROM_VIAM_APP', opts)
```

You will update the `main()` method later.

### Lighting

Next, you'll write the code to manage the LEDs.
Underneath the `connect()` function, add the following class which allows you to create groups of LEDs that you can then turn on and off with one method call:

```python {class="line-numbers linkable-line-numbers"}
class LedGroup:
    def __init__(self, group):
        print("group")
        self.group = group

    async def led_state(self, on):
        for pin in self.group:
            await pin.set(on)
```

If you want to test this code, change your `main()` method to:

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()
    local = Board.from_robot(robot, 'local')
    red_leds = LedGroup([
        await local.gpio_pin_by_name('22'),
        await local.gpio_pin_by_name('24'),
        await local.gpio_pin_by_name('26')
    ])
    blue_leds = LedGroup([
        await local.gpio_pin_by_name('11'),
        await local.gpio_pin_by_name('13'),
        await local.gpio_pin_by_name('15')
    ])

    await blue_leds.led_state(True)
```

You can test the code by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

### Detections

Now, you'll add the code for the guardian to detect persons and pets.
Above the `connect()` method, add the following variable which defines the labels we want to look for in detections:

```python {class="line-numbers linkable-line-numbers"}
LIVING_OBECTS = ["Person", "Dog", "Cat", "Teddy bear"]
```

Then, above the `main()` method add the following function which checks detections for living creatures as they are defined in the `LIVING_OBJECTS` variable.

```python {class="line-numbers linkable-line-numbers"}
async def check_for_living_creatures(detections, blue_leds, red_leds):
    for d in detections:
        if d.confidence > 0.6 and d.class_name in LIVING_OBECTS:
            print("{} detected".format(d.class_name))
            await red_leds.led_state(True)
            await blue_leds.led_state(False)
            return d
        else:
            await blue_leds.led_state(True)
            await red_leds.led_state(False)
```

### Idling

Underneath the `check_for_living_creatures()` function, add the following function which gets images from the guardian's camera and checks them for living creatures and if none are detected moves the servo randomly:

```python {class="line-numbers linkable-line-numbers"}
async def idle_and_check_for_living_creatures(cam, detector, servo, blue_leds, red_leds):
    print("START IDLE")
    living_creature = None
    while True:
        for i in range(random.randint(0, 5)):
            img = await cam.get_image()
            detections = await detector.get_detections(img)
            living_creature = await check_for_living_creatures(detections, blue_leds, red_leds)
            if living_creature:
                return living_creature
        await servo.move(random.randint(0, 180))
```

### Focus

There is one last function that you need to add before you can write the full `main()` function and that is a function to focus on a given creature.
The function calculates the center of the detected object and then checks if that center is close to the middle of the entire image.
If it is not near the middle of the entire image, the function moves the servo to the left or right to attempt to center the object.

Add the following function above your `main()` function:

```python {class="line-numbers linkable-line-numbers"}
async def focus_on_creature(creature, width, servo):
    creature_midpoint = (creature.x_max + creature.x_min)/2
    image_midpoint = width/2
    center_min = image_midpoint - 0.2*image_midpoint
    center_max = image_midpoint + 0.2*image_midpoint

    movement = (image_midpoint - creature_midpoint)/image_midpoint
    angular_scale = 20
    print("MOVE BY: ")
    print(int(angular_scale*movement))

    servo_angle = await servo.get_position()
    if (creature_midpoint < center_min or creature_midpoint > center_max):
        servo_angle = servo_angle + int(angular_scale*movement)
        if servo_angle > 180:
            servo_angle = 180
        if servo_angle < 0:
            servo_angle = 0

        if servo_angle >= 0 and servo_angle <= 180:
            await servo.move(servo_angle)

    servo_return_value = await servo.get_position()
    print(f"servo get_position return value: {servo_return_value}")
```

### Main logic

The main logic for the guardian robot:

- initializes all the variables
- turns all LEDs blue
- runs an infinite loop where it calls the `idle_and_check_for_living_creatures()` function and when a creature is found calls the `focus_on_creature()` function

Replace your `main()` function with the following:

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()
    local = Board.from_robot(robot, 'local')
    cam = Camera.from_robot(robot, "cam")
    img = await cam.get_image()
    servo = Servo.from_robot(robot, "servo")
    red_leds = LedGroup([
        await local.gpio_pin_by_name('22'),
        await local.gpio_pin_by_name('24'),
        await local.gpio_pin_by_name('26')
    ])
    blue_leds = LedGroup([
        await local.gpio_pin_by_name('11'),
        await local.gpio_pin_by_name('13'),
        await local.gpio_pin_by_name('15')
    ])

    await blue_leds.led_state(True)

    # grab Viam's vision service for the detector
    detector = VisionClient.from_robot(robot, "detector")
    while True:
        # move head periodically left and right until movement is spotted.
        living_creature = await idle_and_check_for_living_creatures(cam, detector, servo, blue_leds, red_leds)
        await focus_on_creature(living_creature, img.width, servo)
    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Now, run code:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

<!-- image -->

## Run the program automatically

One more thing.
Right now, you have to run the code manually every time you want your guardian to do get to work.
You can also configure Viam to automatically run your code as a [process](/manage/configuration/#processes).

To be able to run the python script from your Raspberry Pi, you need install the Python SDK on your Raspberry Pi and copy your code onto the Raspberry Pi.

[`ssh` into your Pi](/installation/prepare/rpi-setup/#connect-with-ssh) and install `pip`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt install python3-pip
```

Then install the Viam Python SDK:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install viam-sdk
```

Lastly, create a folder `guardian` inside your home directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mkdir guardian
```

Exit out of your connection to your pi and use `scp` to copy your code to your Pi into your new folder.
Your hostname may be different:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
scp main.py pi@guardian.local:/home/pi/guardian/main.py
```

Now navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Processes** subtab and navigate to the **Create process** menu.

Enter `main` as the process name and click **Create process**.

In the new process panel, enter `python3` as the executable, `main.py` as the argument, and the working directory of your Raspberry Pi as `/home/pi/guardian`.
Click on **Add argument**.

Click **Save config** in the bottom left corner of the screen.

Now your guardian should start behaving like a guardian automatically once booted!

## Next steps

You now have a functioning guardian robot which you can use to monitor your pets or people.
Or simply use to greet you when you get back to your desk.

Of course, you're free to adapt the code to make it do something else, add more LEDs, or even [train your own custom model](/manage/ml/train-model/) to use.

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}
