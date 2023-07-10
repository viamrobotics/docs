---
title: "A Guardian that Tracks Pets using a Pi, Camera, and Servo"
linkTitle: "Security Guardian"
weight: 50
type: "docs"
description: "Make a functional guardian with a servo motor, some LEDs, a camera, and the ML Model and Vision Service to detect people and pets."
webmSrc: "/tutorials/img/guardian/preview.webm"
mp4Src: "/tutorials/img/guardian/preview.mp4"
videoAlt: "A guardian detecting a person or pet."
images: ["/tutorials/img/guardian/preview.gif"]
tags: ["camera", "vision", "detector", "python"]
no_list: true
authors: [ "Naomi Pentrel" ]
languages: [ "python" ]
viamresources: [ "camera", "vision", "servo", "mlmodel" ]
level: "Beginner"
date: "15 May 2023"
cost: 90
---

In the run up to the new Zelda release, I realized you can build a stationary guardian robot with a servo and a camera.
Adding a bit of [machine learning](/services/ml/), you can then make the guardian detect objects or people or pets and follow them around by rotating its head.
Luckily, I am not the first one to have the idea to build a guardian and there was already a [brilliant guardian 3D model](https://www.thingiverse.com/thing:2391826) on Thingiverse with space for LEDs and a servo.

In this tutorial, I will walk you through the steps to build your own functional guardian with a [servo](/components/servo/), a [camera](/components/camera/), some LEDs and the [ML Model service](/services/ml/) and [Vision Service](/services/vision/).
Here's a video of the finished guardian detecting me:

{{<video webm_src="/tutorials/img/guardian/guardian-detection.webm" mp4_src="/tutorials/img/guardian/guardian-detection.mp4" poster="/tutorials/img/guardian/guardian-detection.jpg" alt="Guardian robot detects person and rotates head to follow them around">}}

## Hardware requirements

To build your own guardian robot, you need the following hardware:

| Hardware | Approximate price |
| -------- | ----------------- |
| **Raspberry Pi + power cable** | $60 |
| **Raspberry Pi Camera v1.3 + 50cm ribbon cable**: The default 15cm ribbon cable is not long enough. | $15 |
| **180 degree SG90 servo**: Because of the camera ribbon, I restricted the servo to only 180 degrees. | $4 |
| 3x **10mm RGB LEDs with common cathode** | $4 |
| **cables** | $5 |
| 4x **M2 screws** to attach the camera | $2 |
| **speaker**: Optional if you want music. I used a 4Ω 2W speaker with connected aux in. You can use any speaker you can connect to your Pi. | Optional |

Print or order the following printed 3D parts:

- [this head](https://www.thingiverse.com/thing:6027280) which fits the camera
- the decorations for the head from [this Guardian Robot model](https://www.thingiverse.com/thing:2387723)
- the body, base cover, claws, and leg segments from the [Guardian Robot, Hackable](https://www.thingiverse.com/thing:2391826)

  <div style="max-width: 600px">
  <img src="../../img/guardian/printed_parts.jpg" alt="3d printed parts">
  </div>

To make the guardian's lights shine through its body, use filament that allows the light to shine through and paint the parts that shouldn't allow light to shine through.

Optionally, if you want to decorate your guardian, I recommend the following materials:

- **primer**: Vallego Surface Primer Grey or other brand.
- **acrylic paint**: I ordered armour modelling paint but found that mixing my own colors from a regular acrylic paint set worked best for me.
- **modeling grass, stones, glue**: The Army Painter makes a Battlefields Basing Set which comes with all of this.
- **a base for the guardian**: I used a wooden disk with a hole cut in the middle and a box with a hole in the top underneath.
    <div style="max-width: 400px">
    <img src="../../img/guardian/base.jpg" alt="Wooden guardian base">
    </div>
- **ground texture**: If you want the base to look more natural, you can use Vallejo Ground Texture Acrylic or something similar to create patches that look like stone.
- **wire**: To allow you to position the legs better, you can thread wire through them.

## Software requirements

You will use the following software in this tutorial:

- [Python 3](https://www.python.org/downloads/)
- [`viam-server`](/installation/#install-viam-server): Follow the [installation instructions](/installation/#install-viam-server) to install `viam-server` on your Raspberry Pi.

## Assemble the robot

You can view a timelapse of the robot assembly here:

{{<video webm_src="/tutorials/img/guardian/timelapse.webm" mp4_src="/tutorials/img/guardian/timelapse.mp4" poster="/tutorials/img/guardian/timelapse.jpg" alt="Timelapse of guardian assembly">}}

### Assemble for testing

<div class="td-max-width-on-larger-screens">
  <img src="/tutorials/img/guardian/head.png" class="alignright" alt="Head with camera attachment" style="max-width: 200px" />
</div>

To assemble the guardian, start with the head and use four M2 screws to screw the camera with attached ribbon cable to the front half of the head.
Optionally, if the green of the camera is visible from the outside, use a marker to color the camera board.
Then put both parts of the head together.

Your servo probably came with mounting screws and a plastic horn for the gear.
Use the screws to attach the horn to the base of the head.

Next, get your Raspberry Pi and your servo and connect the servo to the Raspberry Pi by connecting the PWM wire to pin 12, the power wire to pin 2, and the ground wire to pin 8.

{{< alert title="Tip" color="tip" >}}
To make it easier for you to see which pin is which, you can print out [this piece of paper at 100% scaling level](/try-viam/rover-resources/img/rpi4_rover_leaf_A4.pdf) which has labels for the pins and carefully push it onto the pins or fold or cut it so you can hold it up to the Raspberry Pi pins.
Only attach the paper when the Pi is unplugged.
To make attaching the paper easier, use a credit card or a small screwdriver.
{{< /alert >}}

Then attach the head to the servo.

![A Raspberry Pi connected to a FS90R servo. The yellow PWM wire is attached to pin twelve on the raspberry pi. The red five-volt wire is attached to pin two. The black ground wire is attached to pin eight](/tutorials/img/single-component-tutorials-servo-mousemover/servo-wiring-diagram.png)

Next, get the three 10mm RGB LEDs ready.
Attach the common cathode of each LED to a [ground pin](https://pinout.xyz/pinout/ground) on your Raspberry Pi.
Attach the wires for the red and the blue LEDs to [GPIO pins](https://pinout.xyz/pinout/wiringpi).

<div class="td-max-width-on-larger-screens" style="margin: auto">
  <img src="../../img/guardian/assembled-testing.jpg" alt="Components assembled for testing" style="max-width: 400px;" />
</div>

Before continuing with assembly, you should test your components work as expected.
To be able to test the components, you need to install `viam-server` and configure your components.

### Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new robot called `guardian`.

Go to the **Setup** tab of your new robot's page and follow the steps [to install `viam-server` on your computer](/installation/).

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
    Select `mmal service 16.1 (platform:bcm2835_v4l2-0)`.

3. **Add the servo.**

    Create a [servo component](/components/servo/) with the name `servo`, the type `servo` and the model `pi`.
    Click **Create Component** to add the servo.
    Configure the attributes by adding the name of your board, `local`, and the {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin on `local` that you connected your servo PWM wire to, `12`:

    ```json
    {
        "pin": "12",
        "board": "local"
    }
    ```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following JSON configuration for your board, your camera, and your servo with its PWM wire wired to  {{< glossary_tooltip term_id="pin-number" text="pin number" >}} `12`:

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

<div style="max-width: 600px" >
    <img src="../../img/guardian/test.png" alt="the control tab">
</div>

Click on the servo panel and increase or decrease the servo angle to test that the servo moves.

<div style="max-width: 600px" >
    <img src="../../img/guardian/test-servo.png" alt="the control tab servo panel">
</div>

Next, click on the board panel.
The board panel allows you to get and set pin states.
Set the pin states for the pins your LEDs are connected to to high to test that they light up.

<div style="max-width: 600px" >
    <img src="../../img/guardian/test-board.png" alt="the control tab board panel">
</div>

Next, click on the camera panel and toggle the camera on to test that you get video from your camera.

<div style="max-width: 600px" >
    <img src="../../img/guardian/test-cam.jpg" alt="the control tab camera panel">
</div>

### Assemble and decorate

<div class="td-max-width-on-larger-screens">
  <img src="../../img/guardian/finished.jpg" class="alignright" alt="Fully assembled guardian" style="max-width: 250px" />
</div>

Now that you have tested your components, you can disconnect them again, paint and decorate your guardian, and then put the rest of the guardian together.
Remove the servo horn, and place one LED in the back of the Guardian head, leaving the wires hanging out behind the ribbon camera.

Then place the servo inside the Guardian body and attach the horn on the head to the servo's gear.
Carefully place the remaining two LEDs in opposite directions inside the body.
Thread all the cables through the hole in the lid for the base of the guardian, and close the lid.

Use a suitable base with a hole, like a box with a hole cut into the top, to place your guardian on top of and reconnect all the wires to the Raspberry Pi.

At this point also connect the speaker to your Raspberry Pi.

Then test the components on the [robot's Control tab](/manage/fleet/robots/#control) again to ensure everything still works.

## Detect persons and pets

For the guardian to be able to detect living beings, you can use [this Machine Learning model](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/effdet0.tflite).
The model can detect a variety of things which you can see in the associated <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> file.

You can also [train your own custom model](/manage/ml/train-model/) based on images from your robot but the provided Machine Learning model is a good one to start with.

To use the provided Machine Learning model, copy the <file>[effdet0.tflite](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/effdet0.tflite)</file> file and the <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> to your Raspberry Pi:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
scp effdet0.tflite pi@guardian.local:/home/pi/effdet0.tflite
scp labels.txt pi@guardian.local:/home/pi/labels.txt
```

{{< tabs >}}
{{% tab name="Builder UI" %}}

Next, navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Services** subtab and navigate to the **Create service** menu.

1. **Add a ML model service.**

   The [ML model service](/services/ml/) allows you to deploy the provided machine learning model to your robot.
   Create an ML model with the name `mlmodel`, the type `mlmodel` and the model `tflite_cpu`.
   Then click **Create Service**.

   In the new ML Model panel, select **Path to Existing Model On Robot** for the **Deployment**.

   Then specify the absolute **Model Path** as `/home/pi/effdet0.tflite` and the **Label Path** as `/home/pi/labels.txt`.

2. **Add a vision service.**

   Next, add a [detector](/services/vision/detection/) as a vision service to be able to make use of the ML model.
   Create an vision service with the name `detector`, the type `vision` and the model `mlmodel`.
   Then click **Create Service**.

   In the new detector panel, select the `mlmodel` you configured in the previous step.

   Click **Save config** in the bottom left corner of the screen.

3. **Add a `transform` camera.**

   To be able to test that the vision service is working, add a `transform` camera which will add bounding boxes and labels around the objects the service detects.

   Click on the **Components** subtab and navigate to the **Create component** menu.
   Create a [transform camera](/components/camera/transform/) with the name `transform_cam`, the type `camera` and the model `transform`.

   Replace the attributes JSON object with the following object which specifies the camera source that the `transform` camera will be using and defines a pipeline that adds the defined `detector`:

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

Next, on the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following configuration which configures the [ML model service](/services/ml/), the [vision service](/services/vision/), and a [transform camera](/components/camera/transform/):

```json {class="line-numbers linkable-line-numbers" data-line="31-48,50-69"}
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
You should see bounding boxes with labels around different objects.

<div style="max-width: 600px" >
    <img src="../../img/guardian/test-transform.jpg" alt="the control tab transform camera panel">
</div>

## Program the Guardian

With the guardian completely configured and the configuration tested, it's time to make the robot guardian behave like a "real" guardian by programming the person and pet detection, lights, music, and movement.

The full code is available at [the end of the tutorials](#full-code).

### Set up the Python environment

We are going to use Virtualenv to set up a virtual environment for this project, in order to isolate the dependencies of this project from other projects.
Run the following commands in your command-line to install virtualenv, set up an environment `venv` and activate it:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

Now, install the Python Viam SDK and the VLC module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install viam-sdk python-vlc
```

### Connect

Next, go to the **Code sample** tab on your robot page and select **Python**, then click **Copy**.

{{% snippet "show-secret.md" %}}

This code snippet imports all the necessary packages and sets up a connection with the Viam app in the cloud.

Next, create a file named <file>main.py</file> and paste the boilerplate code from the **Code sample** tab of the Viam app into your file.
Then, save your file.

Run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

The program prints a list of robot resources.

On top of the packages that the code sample snippet imports, add the `random` and the `vlc` package to the imports.
The top of your code should now look like this:

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import random
import vlc

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.camera import Camera
from viam.components.servo import Servo
from viam.services.vision import VisionClient

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='LOCATION SECRET FROM THE VIAM APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)
```

{{% snippet "show-secret.md" %}}

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

Your Guardian lights up blue:

{{<gif webm_src="/tutorials/img/guardian/light-up.webm" mp4_src="/tutorials/img/guardian/light-up.mp4" alt="Guardian lights up blue" max-width="300px">}}

### Detections

Now, you'll add the code for the Guardian to detect persons and pets.
If you are building it for persons or cats or dogs, you'll want to use `Person`, `Dog`, `Cat`, and, if you have a particularly teddy-bear-like dog, `Teddy bear`.
You can also specify different ones based on the available labels in <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file>.

Above the `connect()` method, add the following variable which defines the labels that you want to look for in detections:

```python {class="line-numbers linkable-line-numbers"}
LIVING_OBJECTS = ["Person", "Dog", "Cat", "Teddy bear"]
```

Then, above the `main()` method add the following function which checks detections for living creatures as they are defined in the `LIVING_OBJECTS` variable.

```python {class="line-numbers linkable-line-numbers"}
async def check_for_living_creatures(detections):
    for d in detections:
        if d.confidence > 0.6 and d.class_name in LIVING_OBJECTS:
            print("detected")
            return d
```

### Idling

Underneath the `check_for_living_creatures()` function, add the following function which gets images from the Guardian's camera and checks them for living creatures and if none are detected moves the servo randomly.
If a creature is detected, the red LEDs will light up and music will play.

```python {class="line-numbers linkable-line-numbers"}
async def idle_and_check_for_living_creatures(cam, detector, servo, blue_leds, red_leds, music_player):
    living_creature = None
    while True:
        random_number_checks = random.randint(0, 5)
        if music_player.is_playing():
            random_number_checks = 15
        for i in range(random_number_checks):
            img = await cam.get_image()
            detections = await detector.get_detections(img)
            living_creature = await check_for_living_creatures(detections)
            if living_creature:
                await red_leds.led_state(True)
                await blue_leds.led_state(False)
                if not music_player.is_playing():
                    music_player.play()
                return living_creature
        print("START IDLE")
        await blue_leds.led_state(True)
        await red_leds.led_state(False)
        if music_player.is_playing():
            music_player.stop()
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
- loads a music file `guardian.mp3`
- runs an infinite loop where it calls the `idle_and_check_for_living_creatures()` function and when a creature is found calls the `focus_on_creature()` function

{{< alert title="Important" color="note" >}}
Copy a suitable music file to the directory where your code is running and name it `guardian.mp3`.
{{< /alert >}}

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

    music_player = vlc.MediaPlayer("guardian.mp3")

    # grab Viam's vision service for the detector
    detector = VisionClient.from_robot(robot, "detector")
    while True:
        # move head periodically left and right until movement is spotted.
        living_creature = await idle_and_check_for_living_creatures(cam, detector, servo, blue_leds, red_leds, music_player)
        await focus_on_creature(living_creature, img.width, servo)
    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Now, run the code:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 main.py
```

If everything works, your guardian should now start to idle and when it detects humans or dogs or cats turn red, start music, and focus on the detected being:

{{<video webm_src="/tutorials/img/guardian/guardian-finished.webm" mp4_src="/tutorials/img/guardian/guardian-finished.mp4" poster="/tutorials/img/guardian/guardian-finished.jpg" alt="FInished guardian">}}

## Run the program automatically

One more thing.
Right now, you have to run the code manually every time you want your Guardian to work.
You can also configure Viam to automatically run your code as a [process](/manage/configuration/#processes).

To be able to run the Python script from your Raspberry Pi, you need to install the Python SDK on your Raspberry Pi and copy your code onto the Raspberry Pi.

[`ssh` into your Pi](/installation/prepare/rpi-setup/#connect-with-ssh) and install `pip`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt install python3-pip
```

Create a folder `guardian` inside your home directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mkdir guardian
```

Then install the Viam Python SDK and the VLC module **into that folder**:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install --target=guardian viam-sdk python-vlc
```

Exit out of your connection to your Pi and use `scp` to copy your code to your Pi into your new folder.
Your hostname may be different:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
scp main.py pi@guardian.local:/home/pi/guardian/main.py
```

Also copy your music file over:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
scp guardian.mp3 pi@guardian.local:/home/pi/guardian/guardian.mp3
```

Now navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Processes** subtab and navigate to the **Create process** menu.

Enter `main` as the process name and click **Create process**.

In the new process panel, enter `python3` as the executable, `main.py` as the argument, and the working directory of your Raspberry Pi as `/home/pi/guardian`.
Click on **Add argument**.

Click **Save config** in the bottom left corner of the screen.

Now your guardian starts behaving like a guardian automatically once booted!

## Next steps

You now have a functioning guardian robot which you can use to monitor your pets or people.
Or simply use to greet you when you get back to your desk.

Here is a video of how I set up my guardian to follow my dog around my living room:

{{<video webm_src="/tutorials/img/guardian/ernieandtheguardian.webm" mp4_src="/tutorials/img/guardian/ernieandtheguardian.mp4" poster="/tutorials/img/guardian/ernieandtheguardian.jpg" alt="Guardian robot rotates head to follow dog around a room">}}

Of course, you're free to adapt the code to make it do something else, add more LEDs, or even [train your own custom model](/manage/ml/train-model/) to use.

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}

## Full Code

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import random
import vlc

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.camera import Camera
from viam.components.servo import Servo
from viam.services.vision import VisionClient

LIVING_OBJECTS = ["Person", "Dog", "Cat", "Teddy bear"]


async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='SECRET_FROM_VIAM_APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('guardian-main.vw3iu72d8n.viam.cloud', opts)


async def check_for_living_creatures(detections):
    for d in detections:
        if d.confidence > 0.6 and d.class_name in LIVING_OBJECTS:
            print("detected")
            return d


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


class LedGroup:
    def __init__(self, group):
        print("group")
        self.group = group

    async def led_state(self, on):
        for pin in self.group:
            await pin.set(on)


async def idle_and_check_for_living_creatures(cam, detector, servo, blue_leds, red_leds, music_player):
    living_creature = None
    while True:
        random_number_checks = random.randint(0, 5)
        if music_player.is_playing():
            random_number_checks = 15
        for i in range(random_number_checks):
            img = await cam.get_image()
            detections = await detector.get_detections(img)
            living_creature = await check_for_living_creatures(detections)
            if living_creature:
                await red_leds.led_state(True)
                await blue_leds.led_state(False)
                if not music_player.is_playing():
                    music_player.play()
                return living_creature
        print("START IDLE")
        await blue_leds.led_state(True)
        await red_leds.led_state(False)
        if music_player.is_playing():
            music_player.stop()
        await servo.move(random.randint(0, 180))


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

    music_player = vlc.MediaPlayer("guardian.mp3")

    # grab Viam's vision service for the detector
    detector = VisionClient.from_robot(robot, "detector")
    while True:
        # move head periodically left and right until movement is spotted.
        living_creature = await idle_and_check_for_living_creatures(cam, detector, servo, blue_leds, red_leds, music_player)
        await focus_on_creature(living_creature, img.width, servo)
    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```
