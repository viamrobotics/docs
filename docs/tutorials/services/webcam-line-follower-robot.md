---
title: "Build a Line Follower with a Rover and a Webcam"
linkTitle: "RGB Line Follower"
type: "docs"
description: "Build a line-following robot that relies on a webcam and color detection."
tags: ["base", "vision", "detector", "camera", "services", "python"]
videos:
  [
    "/tutorials/webcam-line-follower/lf-tape-follow3.webm",
    "/tutorials/webcam-line-follower/lf-tape-follow3.mp4",
  ]
videoAlt: "The green line the camera sees as the rover moves along it."
aliases:
  - "/tutorials/webcam-line-follower-robot/"
authors: ["Jessamy Taylor"]
languages: ["python"]
viamresources: ["vision", "camera", "base"]
platformarea: ["ml"]
level: "Intermediate"
date: "2022-08-26"
updated: "2024-05-01"
cost: 570
no_list: true
toc_hide: true
---

<div class="td-max-width-on-larger-screens">
 <div class="alignright" style="width:150px;">
  {{<gif webm_src="/tutorials/webcam-line-follower/lf-following1.webm" mp4_src="/tutorials/webcam-line-follower/lf-following1.mp4" alt="Robot following a line">}}
  </div>
</div>

Many line-following robots rely on a dedicated array of infrared sensors to follow a dark line on a light background or a light line on a dark background.
This tutorial uses a standard webcam in place of these sensors, and allows a robot to follow a line of any color that is at least somewhat different from the background.

**Goal**: To make a wheeled robot follow a colored line along the floor using a webcam and the Viam <a href="/dev/reference/apis/services/vision/#detections">vision service color detector</a>.

**What you will learn**:

- How to use the [vision service](/operate/reference/services/vision/)'s [color detectors](/operate/reference/services/vision/color_detector/)
- How to use the [Python SDK](https://python.viam.dev/), including:
  - How to establish communication between the code you write and your robot
  - How to send commands to components of your robot

If you'd like to directly see the code, check out the [**Line Follower Code on GitHub**](https://github.com/viam-labs/line-follower/).

{{<imgproc src="/tutorials/webcam-line-follower/lf-scuttle2.png" resize="600x" declaredimensions=true alt="A Scuttle robot base with a camera mounted on the front, pointing mostly down and slightly forwards.">}}

## Requirements

To build your own line follower robot, you need the following hardware:

<!-- prettier-ignore -->
| Hardware | Avg. price |
| -------- | ----------------- |
| **A single-board computer**: This tutorial uses a Raspberry Pi 4. If you use a different single-board computer, choose the [model that supports your board](/operate/reference/components/board/#configuration) when you [configure your board component](#configure-your-components). | $60 |
| **A wheeled [base component](/operate/reference/components/base/)**: This tutorial uses a [SCUTTLE robot](https://www.scuttlerobot.org/shop/), but any other wheeled base works as long as it can carry the board and camera, and is capable of turning in place. Make sure to assemble this rover. | $99+ |
| **RGB camera**: A common off-the-shelf webcam (such as the [EMEET C690](https://www.amazon.com/Webcam-Streaming-Recording-Built-Correction/dp/B07M6Y7355/ref=sr_1_5?keywords=webcam&qid=1658796392&sr=8-5&th=1)) connected to the Pi’s USB port, or something like an [ArduCam](https://www.amazon.com/Arducam-Megapixels-Sensor-OV5647-Raspberry/dp/B012V1HEP4/) with a ribbon connector to the Pi’s camera module port. **You must mount the camera on the front of the rover, pointing down towards the floor.** | $30 |
| **Colored tape**: Any color is suitable as long as the color is suitably different from the floor color. For our tutorial, we used green electrical tape to stand out against our grey carpet. | $4 |
| **Floor space**: Non-shiny floors tend to work best. | - |

### Install `viam-server` and connect to your machine

{{% snippet "setup.md" %}}

## Configure your components

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.

1. **Add the board.**

   Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Component or service**.
   Select the type `board`, and select the `pi` model.
   Enter `local` as the name of your [board component](/operate/reference/components/board/), then click **Create**.

2. **Add the motors.**

   Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Component or service**.
   Select the type `motor`, and select the `gpio` model.
   Enter `leftm` as the name of your [motor component](/operate/reference/components/motor/), then click **Create** and fill in the appropriate properties for your motor.
   Repeat the same for the right motor and call it `rightm`.

3. **Add the base.**

   Click the **+** (Create) (Create) icon next to your machine part in the left-hand menu and select **Component or service**.
   Select the type `base`, and select the `wheeled` model.
   Enter `scuttlebase` as the name for your [base component](/operate/reference/components/base/), then click **Create** and select the motors.

4. **Add the camera.**

   Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Component or service**.
   Select the type `camera`, and select the `webcam` model.
   Enter the name `my_camera`, then click create.
   Leave the **video_path** blank and the camera will use the default video path for your machine.
   If this doesn't work when you test your camera later, you can try a different video path by following the prompt on the camera's configuration panel.

5. Click **Save** in the top right corner of the screen.

{{% /tab %}}
{{% tab name="JSON" %}}

With **JSON** mode selected on the **CONFIGURE** tab, replace the configuration with the following JSON configuration for your board, your motors, your base, and your camera:

{{< alert title="Note" color="note" >}}
Your `"video_path"` value may be different.
To find yours, follow [these instructions](/operate/reference/components/camera/webcam/#using-video_path).
{{< /alert >}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "leftm",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "a": "15",
          "b": "16"
        },
        "board": "local",
        "max_rpm": 200
      },
      "depends_on": ["local"]
    },
    {
      "name": "rightm",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "b": "11",
          "dir": "",
          "pwm": "",
          "a": "12"
        },
        "board": "local",
        "max_rpm": 200
      },
      "depends_on": ["local"]
    },
    {
      "name": "scuttlebase",
      "model": "wheeled",
      "api": "rdk:component:base",
      "attributes": {
        "width_mm": 400,
        "wheel_circumference_mm": 258,
        "left": ["leftm"],
        "right": ["rightm"]
      },
      "depends_on": ["leftm", "rightm"]
    },
    {
      "name": "my_camera",
      "model": "webcam",
      "api": "rdk:component:camera",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    }
  ]
}
```

Click **Save** in the top right corner of the screen.

{{% /tab %}}
{{< /tabs >}}

## Test your components

Navigate to your [machine's **CONTROL** tab](/manage/troubleshoot/teleoperate/default-interface/#web-ui) to test your components.
Verify that it’s connected by refreshing the page and ensuring that the part status dropdown (in the top banner) says, "Live."

1. Go to the **CONTROL** tab, click on the base panel, and toggle the camera to on.
   Ensure the camera works as expected.

1. Enable the keyboard controls and move the base using your keyboard.
   Ensure that the base moves as expected.

   {{< alert title="Tip" color="tip" >}}
   If one or both drive motors are going backwards, you can power down the Pi by running `sudo poweroff`, unplug the battery, and switch the wires to the motor before powering it back on.
   {{< /alert >}}

   {{<gif webm_src="/tutorials/webcam-line-follower/lf-viamapp-base-view5.webm" mp4_src="/tutorials/webcam-line-follower/lf-viamapp-base-view5.mp4" alt="Driving the base from the control tab." class="aligncenter" max-width="600px">}}

## Configuring a color detector for the color of your tape line

You'll use the [vision service color detector](/operate/reference/services/vision/color_detector/) to programmatically identify the line to follow.
Before you can start on that, you need to get creative though and use your colored tape to make a path for your robot to follow.
Perhaps a circle or other shape, or perhaps a path from one point of interest to another.
Sharp corners will be more challenging for the robot to follow so consider creating more gentle curves.

Once you have created your path, set your robot on the line such that the line appears in the front of the camera’s view.
Verify that the camera sees the line by viewing the camera feed on the **CONTROL** tab of the machine page.

<p>
{{<imgproc src="/tutorials/webcam-line-follower/lf-cam-view6.png" resize="600x" class="aligncenter" declaredimensions=true alt="The camera view in the control tab on the machine page">}}
</p>

Now, let's configure the color detector so your rover can detect the line:

{{< tabs >}}
{{% tab name="Builder UI" %}}

Next, navigate to the **CONFIGURE** tab of your machine's page.

1. **Add a vision service.**

Next, add a vision service [detector](/dev/reference/apis/services/vision/#detections):

Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Component or service**.
Select type `vision` and model `color detector`.
Enter `green_detector` for the name, then click **Create**.

In your vision service’s panel, select the color your vision service will be detecting, as well as a hue tolerance and a segment size (in pixels).
Use a color picker like [colorpicker.me](https://colorpicker.me/) to approximate the color of your line and get the corresponding rgb or hex value.
We used `rgb(25,255,217)` or `#19FFD9` to match the color of our green electrical tape, and specified a segment size of 100 pixels with a tolerance of 0.06, but you can tweak these later to fine tune your line follower.

2. Click **Save** in the top right corner of the screen.

3. (optional) **Add a `transform` camera as a visualizer**

If you'd like to see the bounding boxes that the color detector identifies in a live stream, you'll need to configure a [transform camera](/operate/reference/components/camera/transform/).
This isn't another piece of hardware, but rather a virtual "camera" that takes in the stream from the webcam we just configured and outputs a stream overlaid with bounding boxes representing the color detections.

Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Component or service**.
Add a [transform camera](/operate/reference/components/camera/transform/) with type `camera` and model `transform`.
Name it `transform_cam` and click **Create**.

Click **{}** (Switch to advanced) in the top right of the camera's configuration panel to switch to advanced mode.
Replace the attributes JSON object (`{}`) with the following object which specifies the camera source that the `transform` camera will be using and defines a pipeline that adds the defined `detector`:

```json
{
  "source": "my_camera",
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "detector_name": "green_detector",
        "confidence_threshold": 0.6
      }
    }
  ]
}
```

4. Click **Save** in the top right corner of the screen.

{{% /tab %}}
{{% tab name="JSON" %}}

With **JSON** mode selected, replace the configuration with the following JSON configuration which adds the configuration for the vision service and the transform camera:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "leftm",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "a": "15",
          "b": "16"
        },
        "board": "local",
        "max_rpm": 200
      },
      "depends_on": ["local"]
    },
    {
      "name": "rightm",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "b": "11",
          "dir": "",
          "pwm": "",
          "a": "12"
        },
        "board": "local",
        "max_rpm": 200
      },
      "depends_on": ["local"]
    },
    {
      "name": "scuttlebase",
      "model": "wheeled",
      "api": "rdk:component:base",
      "attributes": {
        "width_mm": 400,
        "wheel_circumference_mm": 258,
        "left": ["leftm"],
        "right": ["rightm"]
      },
      "depends_on": ["leftm", "rightm"]
    },
    {
      "name": "my_camera",
      "model": "webcam",
      "api": "rdk:component:camera",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "show_detections",
      "model": "transform",
      "api": "rdk:component:camera",
      "attributes": {
        "source": "my_camera",
        "pipeline": [
          {
            "type": "detections",
            "attributes": {
              "detector_name": "green_detector"
            }
          }
        ]
      },
      "depends_on": []
    }
  ],
  "services": [
    {
      "name": "green_detector",
      "api": "rdk:service:vision",
      "model": "color_detector",
      "attributes": {
        "segment_size_px": 100,
        "detect_color": "#19FFD9",
        "hue_tolerance_pct": 0.06
      }
    }
  ]
}
```

Click **Save** in the top right corner of the screen.

{{% /tab %}}
{{< /tabs >}}

## Test your color detector

Navigate to your [machine's **CONTROL** tab](/manage/troubleshoot/teleoperate/default-interface/#web-ui) to test the transform camera.
Click on the transform camera panel and toggle the camera on.
You should now be able to view the camera feed with color detector overlays superimposed on the image.

![A screenshot of the CONTROL tab showing the base card with the show_detections transform camera stream displayed. A green line crosses the left portion of the camera image, and a red box around it is labeled "cyan: 1.00".](/tutorials/webcam-line-follower/bounding.png)

If the camera feed does not render color detector overlays on top of the colored tape, adjust the color hex code and the hue tolerance in the Vision service configuration until it is able to do so successfully.

## Implement line following

To make your rover follow your line, you need to install Python and the Viam Python SDK and then write the logic that handles navigation along the line:

### Requirements

1. Make sure you have Python installed.
   You can double-check this by running:

   ```sh {class="command-line" data-prompt="$"}
   python --version
   ```

   or

   ```sh {class="command-line" data-prompt="$"}
   python3 --version
   ```

2. Install the [Viam Python SDK](https://python.viam.dev/) by running

   ```sh {class="command-line" data-prompt="$"}
   pip install viam-sdk
   ```

   or

   ```sh {class="command-line" data-prompt="$"}
   pip3 install viam-sdk
   ```

### Code for line following

1. Download the [robot line follower code](https://github.com/viam-labs/line-follower/blob/main/rgb_follower.py).

1. From your robot’s page, go to the **CONNECT** tab's **Code sample** page and select **Python**.

   {{% snippet "show-secret.md" %}}

   Copy the machine's address and API key and paste them into the definition for the `connect()` function, replacing the placeholders shown there.

   Also, add the following import to the beginning of your code:

   ```python {class="line-numbers linkable-line-numbers"}
   from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image
   ```

   You use these helper functions in your program to convert images captured.

1. You can run the program from your computer or from your Pi.
   If you would like to get your program onto your Pi, you have a few options.
   If you’re just trying to get this running as quickly as possible, do the following:

   1. In your Pi terminal, navigate to the directory where you’d like to save your code.
      Run, <file>nano rgb_follower.py</file> (or replace <file>rgb_follower</file> with the your desired filename).
   2. Paste all your code into this file.
      Press **CTRL + X** to close the file.
      Type **Y** to confirm file modification, then press enter to finish.

   {{< alert title="Tip" color="tip" >}}
   If you intend to make lots of tweaks to the code over time it may be most convenient for you to set up a [Mutagen Sync](https://mutagen.io/documentation/introduction/getting-started/) session from a directory on your computer to a directory on your Pi.
   {{< /alert >}}

1. If you used different component names to the ones mentioned in the tutorial (`scuttlebase`, `my_camera`, and `green_detector`), change the code to use your component names.

The code you are using has several functions:

- `is_color_in_front`: Checks if the color is detected in the front center of the camera's view.

  ```python {class="line-numbers linkable-line-numbers"}
  async def is_color_in_front(camera, detector):
      """
      Returns whether the appropriate path color is detected in front of the
      center of the robot.
      """
      frame = await camera.get_image(mime_type="image/jpeg")

      # Convert to PIL Image
      pil_frame = viam_to_pil_image(frame)
      x, y = pil_frame.size[0], pil_frame.size[1]

      # Crop the image to get only the middle fifth of the top third of the
      # original image
      cropped_pil_frame = pil_frame.crop((x / 2.5, 0, x / 1.25, y / 3))

      # Convert back to ViamImage
      cropped_frame = pil_to_viam_image(cropped_pil_frame)

      detections = await detector.get_detections(cropped_frame)

      if detections != []:
          return True
      return False
  ```

- `is_color_there`: Returns whether the appropriate path color is detected to the left/right of the robot's front.

  ```python {class="line-numbers linkable-line-numbers"}
  async def is_color_there(camera, detector, location):
      """
      Returns whether the appropriate path color is detected to the left/right
      of the robot's front.
      """
      frame = await camera.get_image(mime_type="image/jpeg")

      # Convert to PIL image
      pil_frame = viam_to_pil_image(frame)
      x, y = pil_frame.size[0], pil_frame.size[1]

      if location == "left":
          # Crop image to get only the left two fifths of the original image
          cropped_pil_frame = pil_frame.crop((0, 0, x / 2.5, y))

          # Convert back to PIL Image
          cropped_frame = pil_to_viam_image(cropped_pil_frame)

          detections = await detector.get_detections(cropped_frame)

      elif location == "right":
          # Crop image to get only the right two fifths of the original image
          cropped_pil_frame = pil_frame.crop((x / 1.25, 0, x, y))

          # Convert back to ViamImage
          cropped_frame = pil_to_viam_image(cropped_pil_frame)

          detections = await detector.get_detections(cropped_frame)

      if detections != []:
          return True
      return False
  ```

- `stop_robot`: Stops the robot's motion.

  ```python {class="line-numbers linkable-line-numbers"}
  async def stop_robot(machine):
    """
    Stop the robot's motion.
    """
    base = Base.from_robot(machine, "scuttlebase")
    await base.stop()
  ```

The `main` function connects to the robot and initializes each component, then performs the following tasks:

1. If the color of the line is detected in the top center of the camera frame, the rover drives forward.
2. If the color is not detected in the top center, it checks the left side of the camera frame for the color.
   If it detects the color on the left, the robot turns left.
   If it doesn’t detect the color on the left, it checks the right side of the camera frame, and turns right if it detects the color.
3. Once the line is back in the center front of the camera frame, the rover continues forward.
4. When the rover no longer sees any of the line color anywhere in the front portion of the camera frame, it stops and the program ends.

```python {class="line-numbers linkable-line-numbers"}
async def main():
    """
    Main line follower function.
    """
    machine = await connect()
    print("connected")
    camera = Camera.from_robot(machine, "my_camera")
    base = Base.from_robot(machine, "scuttlebase")

    # Put your detector name in place of "green_detector"
    green_detector = VisionClient.from_robot(machine, "green_detector")

    # counter to increase robustness
    counter = 0

    # Speed parameters to experiment with
    linear_power = 0.35
    angular_power = 0.3

    # The main control loop
    while counter <= 3:
        while await is_color_in_front(camera, green_detector):
            print("going straight")
            # Moves the base slowly forward in a straight line
            await base.set_power(Vector3(y=linear_power), Vector3())
            counter == 0
        # If there is green to the left, turns the base left at a continuous,
        # slow speed
        if await is_color_there(camera, green_detector, "left"):
            print("going left")
            await base.set_power(Vector3(), Vector3(z=angular_power))
            counter == 0
        # If there is green to the right, turns the base right at a continuous,
        # slow speed
        elif await is_color_there(camera, green_detector, "right"):
            print("going right")
            await base.set_power(Vector3(), Vector3(z=-angular_power))
            counter == 0
        else:
            counter += 1

    print("The path is behind us and forward is only open wasteland.")

    await stop_robot(machine)
    await machine.close()
```

To run the program:

1. Position the rover so that its camera can see the colored line.
2. If you have saved the code on your Pi, SSH into it by running:

   ```sh {class="command-line" data-prompt="$"}
   ssh <your_username>@<your_pi’s_name>.local
   ```

   Replace the angle brackets and the example text with your actual Pi username and the name of your Pi.
   Remember to delete the angle brackets!

   Then, run the code

   ```sh {class="command-line" data-prompt="$"}
   python3 rgb_follower.py
   ```

   The robot should continue moving along the line until it no longer sees the color of your detector except at the back of the frame, at which point it should stop moving and the code will terminate.

   {{<gif webm_src="/tutorials/webcam-line-follower/lf-tape-follow3.webm" mp4_src="/tutorials/webcam-line-follower/lf-tape-follow3.mp4" alt="The green line the camera sees as the rover moves along it." class="aligncenter" max-width="300px">}}

## Next steps

You now have a rover following a path of your choice, anywhere you want it to go!
Along the way, you have learned how to configure a wheeled base, camera, and color detector with Viam and how to test them from the **CONTROL** tab.

If you are wondering what to do next, why not try one of the following ideas:

1. Automatically detect what color line the robot is on and follow that.
2. Use two differently colored lines that intersect and make the robot switch from one line to the other.
3. Put two rovers on intersecting lines and write code to keep them from crashing into each other.

## Troubleshooting

### Issue: The rover moves too fast to track the line

If your rover keeps driving off the line so fast that the color detector can’t keep up, you can try two things:

- Slow down the forward movement and turning speeds of the rover by decreasing the values of `linear_power` and `angular_power` respectively.
  - Conversely, if your rover is moving too slowly or stalling, increase the numbers (closer to `1.0` which represents full power).
- Position the camera differently, perhaps so that it is higher above the floor but still pointing downward.
  This will give it a wider field of view so it takes longer for the line to go out of view.

### Issue: The robot is not detecting the color accurately

Things to try:

- Add a [`saturation_cutoff_pct` or a `value_cutoff_percent`](/operate/reference/services/vision/color_detector/) to your vision service parameters.
- Try to achieve more consistent lighting on and around the line.
- Try a different color of line, or a different background.
  Be sure to update your `detect_color` parameter accordingly.

You can find additional assistance in the [Troubleshooting section](/manage/troubleshoot/troubleshoot/).

{{< snippet "social.md" >}}
