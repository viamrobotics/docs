---
title: "Follow a Colored Object with a Rover (like SCUTTLE)"
linkTitle: "Colored Object Follower"
type: "docs"
description: "Instructions for detecting and following a colored object with a rover, like a SCUTTLE robot."
webmSrc: "/tutorials/videos/scuttle-colordetection-preview.webm"
mp4Src: "/tutorials/videos/scuttle-colordetection-preview.mp4"
videoAlt: "Detecting color with a Scuttle Robot"
images: ["/tutorials/videos/scuttle-colordetection-preview.gif"]
aliases:
  - "/tutorials/color-detection-scuttle"
  - "/tutorials/scuttlebot/color-detection-scuttle/"
tags: ["vision", "detector", "base", "scuttle", "services"]
authors: ["Hazal Mestci"]
languages: ["python"]
viamresources: ["base", "vision", "camera"]
level: "Intermediate"
date: "2022-08-18"
updated: "2023-08-11"
cost: 540
no_list: true
---

In this tutorial, you'll learn how to use the [vision service](/ml/vision/) to make a rover follow a colored object.
We're using a [SCUTTLE rover](https://www.scuttlerobot.org/) for this tutorial but you can use any rover, including the [Viam rover](/get-started/try-viam/rover-resources/).

<div class="aligncenter">
{{<video webm_src="/tutorials/videos/scuttledemos_colordetection.webm" mp4_src="/tutorials/videos/scuttledemos_colordetection.mp4" poster="/tutorials/scuttlebot/scuttledemos_colordetection.jpg" alt="Detecting color with a Scuttle Robot">}}
</div>

You can see the [full code](#full-code) at the bottom of the page.

## Requirements

You will need the following hardware to complete this tutorial:

- A wheeled rover, configured with a [base component](/components/base/) on the [Viam app](https://app.viam.com/).
  This tutorial uses a [SCUTTLE rover](https://www.scuttlerobot.org/shop/) as an example but you can complete this tutorial using a different rover.
  - Regardless of the type of base you are using, [Setting up a SCUTTLE with Viam](/tutorials/configure/scuttlebot/) is a good place to start if you haven't already configured your base.
- An attached and configured [webcam camera](/components/camera/webcam/).

## Set up the hardware

Connect the camera to the rover's board.
Turn on the power to the rover.

## Configure color detection

This tutorial uses the color `#a13b4c` or `rgb(161,59,76)` (a reddish color).

To create a [color detector vision service](/ml/vision/#detections):

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to your machine's **Config** tab on the [Viam app](https://app.viam.com/robots).
Click the **Services** subtab and click **Create service** in the lower-left corner.
Select the `Vision` type, then select the `Color Detector` model.
Enter `my_color_detector` as the name for your service and click **Create**.

In your vision service's panel, set the following **Attributes**:

- Set the color to `#a13b4c` or `rgb(161,59,76)`
- Set hue tolerance to `0.06`
- Set the segment size to `100`px

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "my_color_detector",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 100,
      "detect_color": "#a13b4c",
      "hue_tolerance_pct": 0.06
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{< /tabs >}}

Click **Save config** and head to the **Components** tab.

You have configured a heuristic-based detector that draws boxes around objects according to their color.

{{< alert title="Tip" color="tip" >}}
If you want to detect other colors, change the color parameter `detect_color`.
Object colors can vary dramatically based on the light source.
We recommend that you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual cam component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).
{{< /alert >}}

### Test your color detector

You can test your detector from the [**Control tab**](/fleet/machines/#control):

1. Configure a [transform camera](/components/camera/transform/) with the following attributes:

   ```json
   {
     "pipeline": [
       {
         "type": "detections",
         "attributes": {
           "confidence_threshold": 0.5,
           "detector_name": "my_color_detector"
         }
       }
     ],
     "source": "<camera-name>"
   }
   ```

   For `<camera-name>`, insert the name of your configured physical camera.

2. Click **Save config**.
3. Navigate to the **Control** tab, click on your transform camera and toggle it on.
   The transform camera will now show detections with bounding boxes around the detected colors.

{{< alert title="Tip" color="tip" >}}
If the color is not reliably detected, try increasing the `hue_tolerance_pct` or adjusting the lighting of the area to make the color being detected more visible.

Note that the detector does not detect black, perfect greys (greys where the red, green, and blue color component values are equal), or white.
{{< /alert >}}

## Program your rover

### Set up your code environment

We are going to use Virtualenv to set up a virtual environment for this project, in order to isolate the dependencies of this project from other projects.
Run the following commands in your command-line to install `virtualenv`, set up an environment `venv` and activate it:

```sh {class="command-line" data-prompt="$"}
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

Then, install the Viam Python SDK:

```sh {class="command-line" data-prompt="$"}
pip3 install viam-sdk
```

### Connect

Next, go to the **Code sample** tab on your [machine page](https://app.viam.com/robots) and select **Python**, then click **Copy**.

{{% snippet "show-secret.md" %}}

This code snippet imports all the necessary packages and sets up a connection with the Viam app.

Next, create a file named <file>main.py</file> and paste the boilerplate code from the **Code sample** tab of the Viam app into your file.
Then, save your file.

Run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.
If you haven't yet installed `viam-server`, follow the [installation guide](/get-started/installation/#install-viam-server) to install `viam-server` on your robot before proceeding with this tutorial.

You can run your code by typing the following into your terminal from the same directory as your `main.py` file:

```sh {class="command-line" data-prompt="$"}
python3 main.py
```

The program prints a list of robot resources.

On top of the packages that the code sample snippet imports, add the `random` and the `vlc` package to the imports.
The top of your code should now look like this:

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient
from viam.components.camera import Camera
from viam.components.base import Base


async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address("ADDRESS FROM THE VIAM APP", opts)


async def main():
    # Other code
    print("Starting main")

if __name__ == "__main__":
    print("Starting up... ")
    asyncio.run(main())
    print("Done.")
```

You will update the `main()` function later.

### Detect the location of a colored object

With the configured color detector, you can programmatically retrieve a list of detections.
Each detection comes with information about where in the camera's picture it is detected.

The following `leftOrRight` function checks where in the picture the largest detection is and returns a responding integer: `0` for left, `1` for center, and `2` for right.

Add the `leftOrRight` function below your `connect` function:

```python {class="line-numbers linkable-line-numbers"}
# Get largest detection box and see if it's center is in the left, center, or
# right third
def leftOrRight(detections, midpoint):
    largest_area = 0
    largest = {"x_max": 0, "x_min": 0, "y_max": 0, "y_min": 0}
    if not detections:
        print("nothing detected :(")
        return -1
    for d in detections:
        a = (d.x_max - d.x_min) * (d.y_max-d.y_min)
        if a > largest_area:
            a = largest_area
            largest = d
    centerX = largest.x_min + largest.x_max/2
    if centerX < midpoint-midpoint/6:
        return 0  # on the left
    if centerX > midpoint+midpoint/6:
        return 2  # on the right
    else:
        return 1  # basically centered
```

### Add the main function

The `main` function:

- defines variables for how the robot should move,
- connects to the robot,
- initializes the base, the camera, and the detector, and
- repeatedly calls the `leftOrRight` function and turns the rover's base in the respective direction.

Replace the `main` function with the following code:

```python {class="line-numbers linkable-line-numbers"}
async def main():
    spinNum = 10         # when turning, spin the motor this much
    straightNum = 300    # when going straight, spin motor this much
    numCycles = 200      # run the loop X times
    vel = 500            # go this fast when moving motor

    # Connect to robot client and set up components
    robot = await connect()
    base = Base.from_robot(robot, "my_base")
    camera_name = "<camera-name>"
    camera = Camera.from_robot(robot, camera_name)
    frame = await camera.get_image(mime_type="image/jpeg")

    # Grab the vision service for the detector
    my_detector = VisionClient.from_robot(robot, "my_color_detector")

    # Main loop. Detect the ball, determine if it's on the left or right, and
    # head that way. Repeat this for numCycles
    for i in range(numCycles):
        detections = await my_detector.get_detections_from_camera(camera_name)

        answer = leftOrRight(detections, frame.size[0]/2)
        if answer == 0:
            print("left")
            await base.spin(spinNum, vel)     # CCW is positive
            await base.move_straight(straightNum, vel)
        if answer == 1:
            print("center")
            await base.move_straight(straightNum, vel)
        if answer == 2:
            print("right")
            await base.spin(-spinNum, vel)
        # If nothing is detected, nothing moves

    await robot.close()
```

For `<camera-name>`, insert the name of your configured physical camera.

## Run the code

Now, run the code again, from the same directory as your `main.py` file:

```sh {class="command-line" data-prompt="$"}
python3 main.py
```

Your rover should detect and navigate towards any red objects that come into view of its camera.
Use something like a red sports ball or book cover as a target to follow to test your rover:

<div class="aligncenter">
{{<video webm_src="/tutorials/videos/scuttledemos_colordetection.webm" mp4_src="/tutorials/videos/scuttledemos_colordetection.mp4" poster="/tutorials/scuttlebot/scuttledemos_colordetection.jpg" alt="Detecting color with a Scuttle Robot">}}
</div>

## Next steps

Congratulations! If you're ready for more, try making your rover detect other colors.
You could also write some code with a Viam SDK to [make your rover move in a square](/tutorials/get-started/try-viam-sdk/).

{{< snippet "social.md" >}}

## Full Code

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient
from viam.components.camera import Camera
from viam.components.base import Base


async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address("ADDRESS FROM THE VIAM APP", opts)


# Get largest detection box and see if it's center is in the left, center, or
# right third
def leftOrRight(detections, midpoint):
    largest_area = 0
    largest = {"x_max": 0, "x_min": 0, "y_max": 0, "y_min": 0}
    if not detections:
        print("nothing detected :(")
        return -1
    for d in detections:
        a = (d.x_max - d.x_min) * (d.y_max-d.y_min)
        if a > largest_area:
            a = largest_area
            largest = d
    centerX = largest.x_min + largest.x_max/2
    if centerX < midpoint-midpoint/6:
        return 0  # on the left
    if centerX > midpoint+midpoint/6:
        return 2  # on the right
    else:
        return 1  # basically centered


async def main():
    spinNum = 10         # when turning, spin the motor this much
    straightNum = 300    # when going straight, spin motor this much
    numCycles = 200      # run the loop X times
    vel = 500            # go this fast when moving motor

    # Connect to robot client and set up components
    robot = await connect()
    base = Base.from_robot(robot, "my_base")
    camera_name = "<camera-name>"
    camera = Camera.from_robot(robot, camera_name)
    frame = await camera.get_image(mime_type="image/jpeg")

    # Grab the vision service for the detector
    my_detector = VisionClient.from_robot(robot, "my_color_detector")

    # Main loop. Detect the ball, determine if it's on the left or right, and
    # head that way. Repeat this for numCycles
    for i in range(numCycles):
        detections = await my_detector.get_detections_from_camera(camera_name)

        answer = leftOrRight(detections, frame.size[0]/2)
        if answer == 0:
            print("left")
            await base.spin(spinNum, vel)     # CCW is positive
            await base.move_straight(straightNum, vel)
        if answer == 1:
            print("center")
            await base.move_straight(straightNum, vel)
        if answer == 2:
            print("right")
            await base.spin(-spinNum, vel)
        # If nothing is detected, nothing moves

    await robot.close()

if __name__ == "__main__":
    print("Starting up... ")
    asyncio.run(main())
    print("Done.")
```
