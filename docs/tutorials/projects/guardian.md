---
title: "A Guardian that Tracks Pets using a Pi, Camera, and Servo"
linkTitle: "Pet Guardian"
type: "docs"
description: "Make a functional guardian with a servo motor, some LEDs, a camera, and the ML Model and vision service to detect people and pets."
videos: ["/tutorials/guardian/preview.webm", "/tutorials/guardian/preview.mp4"]
videoAlt: "A guardian detecting a person or pet."
images: ["/tutorials/guardian/preview.gif"]
tags: ["camera", "vision", "detector", "python"]
no_list: true
authors: ["Naomi Pentrel"]
languages: ["python"]
viamresources: ["camera", "vision", "servo", "mlmodel"]
level: "Intermediate"
date: "2023-05-15"
# updated: ""
cost: 90
---

In the run up to the new Zelda release, I realized you can build a stationary guardian robot with a servo and a camera.
Adding a bit of [machine learning](/ml/), you can then make the guardian detect objects or people or pets and follow them around by rotating its head.
Luckily, I am not the first one to have the idea to build a guardian and there was already a [brilliant guardian 3D model](https://www.thingiverse.com/thing:2391826) on Thingiverse with space for LEDs and a servo.

In this tutorial, I will walk you through the steps to build your own functional guardian with a [servo](/components/servo/), a [camera](/components/camera/), some LEDs and the [ML Model service](/ml/) and [vision service](/ml/vision/).
Here's a video of the finished guardian detecting me:

{{<video webm_src="/tutorials/guardian/guardian-detection.webm" mp4_src="/tutorials/guardian/guardian-detection.mp4" poster="/tutorials/guardian/guardian-detection.jpg" alt="Guardian robot detects person and rotates head to follow them around">}}

## Hardware requirements

To build your own guardian robot, you need the following hardware:

<!-- prettier-ignore -->
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

{{< imgproc src="/tutorials/guardian/printed_parts.jpg" alt="3d printed parts" resize="600x" >}}

To make the guardian's lights shine through its body, use filament that allows the light to shine through and paint the parts that shouldn't allow light to shine through.

Optionally, if you want to decorate your guardian, I recommend the following materials:

- **primer**: Vallego Surface Primer Grey or other brand.
- **acrylic paint**: I ordered armour modelling paint but found that mixing my own colors from a regular acrylic paint set worked best for me.
- **modeling grass, stones, glue**: The Army Painter makes a Battlefields Basing Set which comes with all of this.
- **a base for the guardian**: I used a wooden disk with a hole cut in the middle and a box with a hole in the top underneath.
  {{< imgproc src="/tutorials/guardian/base.jpg" alt="Wooden guardian base" resize="400x" >}}
- **ground texture**: If you want the base to look more natural, you can use Vallejo Ground Texture Acrylic or something similar to create patches that look like stone.
- **wire**: To allow you to position the legs better, you can thread wire through them.

## Software requirements

You will use the following software in this tutorial:

- [Python 3](https://www.python.org/downloads/)
- [`viam-server`](/get-started/installation/#install-viam-server): Follow the [installation instructions](/get-started/installation/#install-viam-server) to install `viam-server` on your Raspberry Pi.

## Assemble the robot

You can view a timelapse of the robot assembly here:

{{<video webm_src="/tutorials/guardian/timelapse.webm" mp4_src="/tutorials/guardian/timelapse.mp4" poster="/tutorials/guardian/timelapse.jpg" alt="Timelapse of guardian assembly">}}

### Assemble for testing

<div class="td-max-width-on-larger-screens" class="alignright" style="max-width: 200px">
  {{<imgproc src="/tutorials/guardian/head.png" resize="300x" declaredimensions=true alt="Head with camera attachment">}}
</div>

To assemble the guardian, start with the head and use four M2 screws to screw the camera with attached ribbon cable to the front half of the head.
Optionally, if the green of the camera is visible from the outside, use a marker to color the camera board.
Then put both parts of the head together.

Your servo probably came with mounting screws and a plastic horn for the gear.
Use the screws to attach the horn to the base of the head.

Next, get your Raspberry Pi and your servo and connect the servo to the Raspberry Pi by connecting the PWM wire to pin 12, the power wire to pin 2, and the ground wire to pin 8.

{{< alert title="Tip" color="tip" >}}
To make it easier for you to see which pin is which, you can print out [this Raspberry Pi Leaf](/get-started/try-viam/viam-raspberry-leaf-8.5x11.pdf) which has labels for the pins and carefully push it onto the pins or fold or cut it so you can hold it up to the Raspberry Pi pins.
If you use A4 paper, use this [this Raspberry Pi Leaf](/get-started/try-viam/viam-raspberry-leaf-A4.pdf) instead.

If you are having trouble punching the pins through, you can pre-punch the pin holes with a pen.
Only attach the paper when the Pi is unplugged.
To make attaching the paper easier, use a credit card or a small screwdriver.
{{< /alert >}}

Then attach the head to the servo.

![A Raspberry Pi connected to a FS90R servo. The yellow PWM wire is attached to pin twelve on the raspberry pi. The red five-volt wire is attached to pin two. The black ground wire is attached to pin eight](/tutorials/single-component-tutorials-servo-mousemover/servo-wiring-diagram.png)

Next, get the three 10mm RGB LEDs ready.
Attach the common cathode of each LED to a [ground pin](https://pinout.xyz/pinout/ground) on your Raspberry Pi.
Attach the wires for the red and the blue LEDs to [GPIO pins](https://pinout.xyz/pinout/wiringpi).

<div class="td-max-width-on-larger-screens" style="margin: auto" style="max-width: 400px;">
  {{<imgproc src="/tutorials/guardian/assembled-testing.jpg" resize="400x" declaredimensions=true alt="Components assembled for testing">}}
</div>

Before continuing with assembly, you should test your components work as expected.
To be able to test the components, you need to install `viam-server` and configure your components.

### Install `viam-server` and connect to your robot

Go to the [Viam app](https://app.viam.com) and create a new machine called `guardian`.

Go to the **Setup** tab of your new machine's page and follow the steps [to install `viam-server` on your computer](/get-started/installation/).

### Configure the components

{{< tabs >}}
{{% tab name="Builder UI" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab.

1. **Add the board.**

   Click **Create component** in the lower-left corner of the page.
   Select `board` for the type, then select `pi` for the model.
   Enter `local` as the name for your [board component](/components/board/), then click **Create**.

2. **Add the camera.**

   Click **Create Component** to add the [camera](/components/camera/).
   Select `camera` for the type, then select `webcam` for the model.
   Enter `cam` as the name for the camera, then click **Create**.
   In the new camera panel, click the **Video Path** field to reveal a dropdown populated with camera paths that have been identified on your machine.
   Select `mmal service 16.1 (platform:bcm2835_v4l2-0)`.

3. **Add the servo.**

   Click **Create component** in the lower-left corner of the page.
   Select `servo` for the type, then select `pi` for the model.
   Enter `servo` as the name for your [servo component](/components/servo/), then click **Create**.
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

On the [`Raw JSON` tab](/build/configure/#the-config-tab), replace the configuration with the following JSON configuration for your board, your camera, and your servo with its PWM wire wired to {{< glossary_tooltip term_id="pin-number" text="pin number" >}} `12`:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "cam",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "servo",
      "model": "pi",
      "type": "servo",
      "namespace": "rdk",
      "attributes": {
        "pin": "12",
        "board": "local"
      },
      "depends_on": ["local"]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

### Test the components

Navigate to your [machine's Control tab](/fleet/machines/#control) to test your components.

{{<imgproc src="/tutorials/guardian/test.png" resize="600x" declaredimensions=true alt="the control tab">}}

Click on the servo panel and increase or decrease the servo angle to test that the servo moves.

{{<imgproc src="/tutorials/guardian/test-servo.png" resize="600x" declaredimensions=true alt="the control tab servo panel">}}

Next, click on the board panel.
The board panel allows you to get and set pin states.
Set the pin states for the pins your LEDs are connected to to high to test that they light up.

{{<imgproc src="/tutorials/guardian/test-board.png" resize="600x" declaredimensions=true alt="the control tab board panel">}}

Next, click on the camera panel and toggle the camera on to test that you get video from your camera.

{{<imgproc src="/tutorials/guardian/test-cam.jpg" resize="600x" declaredimensions=true alt="the control tab camera panel">}}

### Assemble and decorate

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/guardian/finished.jpg" resize="300x" declaredimensions=true alt="Fully assembled guardian" style="max-width: 250px;" class="alignright" >}}
</div>

Now that you have tested your components, you can disconnect them again, paint and decorate your guardian, and then put the rest of the guardian together.
Remove the servo horn, and place one LED in the back of the Guardian head, leaving the wires hanging out behind the ribbon camera.

Then place the servo inside the Guardian body and attach the horn on the head to the servo's gear.
Carefully place the remaining two LEDs in opposite directions inside the body.
Thread all the cables through the hole in the lid for the base of the guardian, and close the lid.

Use a suitable base with a hole, like a box with a hole cut into the top, to place your guardian on top of and reconnect all the wires to the Raspberry Pi.

At this point also connect the speaker to your Raspberry Pi.

Then test the components on the [machine's Control tab](/fleet/machines/#control) again to ensure everything still works.

## Detect persons and pets

For the guardian to be able to detect living beings, you will use a machine learning model from the Viam registry called [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO).
The model can detect a variety of things which you can see in <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> file.

You can also [train your own custom model](/ml/train-model/) based on images from your robot but the provided Machine Learning model is a good one to start with.

{{< tabs >}}
{{% tab name="Builder UI" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **Services** subtab.

1. **Add an ML model service.**

The [ML model service](/ml/) allows you to deploy a machine learning model to your robot.

Click **Create service** in the lower-left corner of the page.
Select type `ML Model`, then select model `TFLite CPU`.
Enter `mlmodel` as the name for your ML model service, then click **Create**.

Select the **Deploy model on robot** for the **Deployment** field.
Then select the `viam-labs:EfficientDet-COCO` model from the **Models** dropdown.

2. **Add a vision service.**

Next, add a [detector](/ml/vision/#detections) as a vision service to be able to make use of the ML model.

Click **Create service** in the lower-left corner of the page.
Select type `Vision`, then select model `ML Model`.
Enter `detector` as the name, then click **Create**.

In the new detector panel, select the `mlmodel` you configured in the previous step.

Click **Save config** in the bottom left corner of the screen.

3. **Add a `transform` camera.**

To be able to test that the vision service is working, add a `transform` camera which will add bounding boxes and labels around the objects the service detects.

Navigate to the **Components** subtab of the **Config** tab.
Click **Create component** in the lower-left corner of the page.

Select `camera` for the type, then select `transform` for the model.
Enter `transform_cam` as the name for your [transform camera](/components/camera/transform/), then click **Create**.

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

On the [**Raw JSON** tab](/build/configure/#the-config-tab), replace the configuration with the following configuration which configures the [ML model service](/ml/), the [vision service](/ml/vision/), and a [transform camera](/components/camera/transform/):

```json {class="line-numbers linkable-line-numbers" data-line="32-80"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "cam",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "servo",
      "model": "pi",
      "type": "servo",
      "namespace": "rdk",
      "attributes": {
        "pin": "12",
        "board": "local"
      },
      "depends_on": ["local"]
    },
    {
      "name": "transform_cam",
      "model": "transform",
      "type": "camera",
      "namespace": "rdk",
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
        "model_path": "${packages.effdet0}/efficientdet0.tflite",
        "label_path": "${packages.effdet0}/effdetlabels.txt",
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
  ],
  "packages": [
    {
      "name": "effdet0",
      "type": "ml_model",
      "version": "latest",
      "package": "bill/effdet0"
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

Navigate to your [machine's Control tab](/fleet/machines/#control) to test the transform camera.
Click on the transform camera panel and toggle the camera on, then point your camera at a person or pet to test if the vision service detects them.
You should see bounding boxes with labels around different objects.

{{<imgproc src="/tutorials/guardian/test-transform.jpg" resize="600x" declaredimensions=true alt="the control tab transform camera panel">}}

## Program the Guardian

With the guardian completely configured and the configuration tested, it's time to make the robot guardian behave like a "real" guardian by programming the person and pet detection, lights, music, and movement.

The full code is available at [the end of the tutorials](#full-code).

### Set up the Python environment

We are going to use Virtualenv to set up a virtual environment for this project, in order to isolate the dependencies of this project from other projects.
Run the following commands in your command-line to install virtualenv, set up an environment `venv` and activate it:

```sh {class="command-line" data-prompt="$"}
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

Now, install the Python Viam SDK with the `mlmodel` extra, and the VLC module:

```sh {class="command-line" data-prompt="$"}
pip3 install 'viam-sdk[mlmodel]' python-vlc
```

The `mlmodel` extra includes additional dependency support for the [ML (machine learning) model service](/ml/).

### Connect

Next, go to the **Code sample** tab on your machine page and select **Python**, then click **Copy**.

{{% snippet "show-secret.md" %}}

This code snippet imports all the necessary packages and sets up a connection with the Viam app in the cloud.

Next, create a file named <file>main.py</file> and paste the boilerplate code from the **Code sample** tab of the Viam app into your file.
Then, save your file.

Run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into your terminal:

```sh {class="command-line" data-prompt="$"}
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
    opts = RobotClient.Options.with_api_key(
      # Replace "<API-KEY>" (including brackets) with your machine's API key
      api_key='<API-KEY>',
      # Replace "<API-KEY-ID>" (including brackets) with your machine's API key
      # ID
      api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)
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

```sh {class="command-line" data-prompt="$"}
python3 main.py
```

Your Guardian lights up blue:

{{<gif webm_src="/tutorials/guardian/light-up.webm" mp4_src="/tutorials/guardian/light-up.mp4" alt="Guardian lights up blue" max-width="300px">}}

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
async def idle_and_check_for_living_creatures(
  camera_name, detector, servo, blue_leds, red_leds, music_player):
    living_creature = None
    while True:
        random_number_checks = random.randint(0, 5)
        if music_player.is_playing():
            random_number_checks = 15
        for i in range(random_number_checks):
            detections = await detector.get_detections_from_camera(camera_name)
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
    camera_name = "cam"
    cam = Camera.from_robot(robot, camera_name)
    img = await cam.get_image(mime_type="image/jpeg")
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
        living_creature = await idle_and_check_for_living_creatures(
            camera_name, detector, servo, blue_leds, red_leds, music_player)
        await focus_on_creature(living_creature, img.width, servo)
    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Now, run the code:

```sh {class="command-line" data-prompt="$"}
python3 main.py
```

If everything works, your guardian should now start to idle and when it detects humans or dogs or cats turn red, start music, and focus on the detected being:

{{<video webm_src="/tutorials/guardian/guardian-finished.webm" mp4_src="/tutorials/guardian/guardian-finished.mp4" poster="/tutorials/guardian/guardian-finished.jpg" alt="FInished guardian">}}

## Run the program automatically

One more thing.
Right now, you have to run the code manually every time you want your Guardian to work.
You can also configure Viam to automatically run your code as a [process](/build/configure/processes/).

To be able to run the Python script from your Raspberry Pi, you need to install the Python SDK on your Raspberry Pi and copy your code onto the Raspberry Pi.

[`ssh` into your Pi](/get-started/installation/prepare/rpi-setup/#connect-with-ssh) and install `pip`:

```sh {class="command-line" data-prompt="$"}
sudo apt install python3-pip
```

Create a folder `guardian` inside your home directory:

```sh {class="command-line" data-prompt="$"}
mkdir guardian
```

Then install the Viam Python SDK and the VLC module **into that folder**:

```sh {class="command-line" data-prompt="$"}
pip3 install --target=guardian viam-sdk python-vlc
```

Exit out of your connection to your Pi and use `scp` to copy your code to your Pi into your new folder.
Your hostname may be different:

```sh {class="command-line" data-prompt="$"}
scp main.py pi@guardian.local:/home/pi/guardian/main.py
```

Also copy your music file over:

```sh {class="command-line" data-prompt="$"}
scp guardian.mp3 pi@guardian.local:/home/pi/guardian/guardian.mp3
```

Now navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Processes** subtab and navigate to the **Create process** menu.

Enter `main` as the process name and click **Create process**.

In the new process panel, enter `python3` as the executable, `main.py` as the argument, and the working directory of your Raspberry Pi as `/home/pi/guardian`.
Click on **Add argument**.

Click **Save config** in the bottom left corner of the screen.

Now your guardian starts behaving like a guardian automatically once booted!

## Use the Viam mobile app

If you want to access your or control your machine on the go, you can use the [Viam mobile app](/fleet/#the-viam-mobile-app).

{{<video webm_src="/tutorials/guardian/app.webm" mp4_src="/tutorials/guardian/app.mp4"
poster="/tutorials/guardian/app.jpg"
alt="Viam mobile app controlling machine" max-width="300px">}}

## Next steps

You now have a functioning guardian robot which you can use to monitor your pets or people.
Or simply use to greet you when you get back to your desk.

Here is a video of how I set up my guardian to follow my dog around my living room:

{{<video webm_src="/tutorials/guardian/ernieandtheguardian.webm" mp4_src="/tutorials/guardian/ernieandtheguardian.mp4" poster="/tutorials/guardian/ernieandtheguardian.jpg" alt="Guardian robot rotates head to follow dog around a room" >}}

Of course, you're free to adapt the code to make it do something else, add more LEDs, or even [train your own custom model](/ml/train-model/) to use.

For more robotics projects, check out our [other tutorials](/tutorials/).

{{< snippet "social.md" >}}

## Full code

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
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)


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


async def idle_and_check_for_living_creatures(camera_name,
                                              detector,
                                              servo,
                                              blue_leds,
                                              red_leds,
                                              music_player):
    living_creature = None
    while True:
        random_number_checks = random.randint(0, 5)
        if music_player.is_playing():
            random_number_checks = 15
        for i in range(random_number_checks):
            detections = await detector.get_detections_from_camera(camera_name)
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
    camera_name = "cam"
    cam = Camera.from_robot(robot, camera_name)
    img = await cam.get_image(mime_type="image/jpeg")
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
        living_creature = await idle_and_check_for_living_creatures(
            camera_name, detector, servo, blue_leds, red_leds, music_player)
        await focus_on_creature(living_creature, img.width, servo)
    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```
