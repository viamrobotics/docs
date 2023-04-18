---
title: "Build a Line Follower with a Rover and a Webcam"
linkTitle: "RGB Line Follower"
weight: 50
type: "docs"
description: "Build a line-following robot that relies on a webcam and color detection."
tags: ["base", "vision", "detector", "camera", "services", "python"]
webmSrc: "/tutorials/img/webcam-line-follower/lf-tape-follow3.webm"
mp4Src: "/tutorials/img/webcam-line-follower/lf-tape-follow3.mp4"
videoAlt: "The green line the camera sees as the rover moves along it."
---



<div class="td-max-width-on-larger-screens">
 <div class="alignright" style="max-width:150px;">
  {{<gif webm_src="../../img/webcam-line-follower/lf-following1.webm" mp4_src="../../img/webcam-line-follower/lf-following1.mp4" alt="Robot following a line">}}
  </div>
</div>

Many line-following robots rely on a dedicated array of infrared sensors to follow a dark line on a light background or a light line on a dark background.
This tutorial uses a standard webcam in place of these sensors, and allows a robot to follow a line of any color that is at least somewhat different from the background.

**Goal**: To make a wheeled robot follow a colored line along the floor using a webcam and the Viam <a href="/services/vision/detection">Vision Service color detector</a>.

**What you will learn**:

- How to use the Viam Vision Service including color detectors
- How to use the [Viam Python SDK](https://github.com/viamrobotics/viam-python-sdk), including:
  - How to establish communication between the code you write and your robot
  - How to send commands to components of your robot

[**Line Follower Code on GitHub**](https://github.com/viam-labs/line-follower/)

## What you'll need

- A single board computer [running an instance of `viam-server`](/installation/prepare/rpi-setup/)
  - This tutorial assumes the use of a Raspberry Pi running a 64-bit Linux distribution, but these instructions could potentially be adapted for other boards.
- [A wheeled base component](/components/base/)
  - We used a [SCUTTLE Robot](https://www.scuttlerobot.org/shop/) for this project, but any number of other wheeled bases could work, as long as they can carry the compute module and camera, and can turn in place.
- RGB camera
  - A common off-the-shelf webcam [(such as this)](https://www.amazon.com/Webcam-Streaming-Recording-Built-Correction/dp/B07M6Y7355/ref=sr_1_5?keywords=webcam&qid=1658796392&sr=8-5&th=1) connected to the Pi’s USB port, or something like an [ArduCam](https://www.uctronics.com/arducam-for-raspberry-pi-camera-module-with-case-5mp-1080p-for-raspberry-pi-3-3-b-and-more.html/) with a ribbon connector to the Pi’s camera module port.
  - You must mount the camera to the front of the rover pointing down towards the floor.
- Colored tape and floor space
  - Any color is suitable as long as its color is somewhat different from the floor color.
    For our tutorial, we used green electrical tape.
  - Non-shiny floors tend to work best.

<img src="/tutorials/img/webcam-line-follower/lf-scuttle2.png" alt="A SCUTTLE Robot base with a camera mounted on the front, pointing mostly down and slightly forwards." width="600" />

## Configuration using Viam

If you haven’t already, please set up the Raspberry Pi per [these instructions](/installation/prepare/rpi-setup/).

### Configuring the hardware components

Configure the board per the [Board Component topic](/components/board/).
We named ours `local`.
Use type `board` and model `pi` if you're using a Raspberry Pi.

Configure the wheeled base per the [Base Component documentation](/components/base/).
We named ours `scuttlebase`.

[Configure the camera as a webcam](/components/camera/webcam).

Your webcam configuration will look something like this:

![The webcam configuration UI with video_path set to video0.](/tutorials/img/webcam-line-follower/lf-cam-config.png)

Or if you prefer the raw JSON:

```json {class="line-numbers linkable-line-numbers"}
    {
      "name": "my_camera",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    }
```

### Configuring the Vision Service

We’ll use the Viam [Vision Service color detector](/services/vision/detection) to identify the line to follow.

In the **Services** section of the **config** tab, configure a color detector for the color of your tape line.

- Use a color picker like [colorpicker.me](https://colorpicker.me/) to approximate the color of your line and get the corresponding hexadecimal hash to put in your config.
Put this hash in the `detect_color` parameter.
We used #19FFD9 to represent the color of green electrical tape.

- We used a segment size of 100 pixels, and a tolerance of 0.06, but you can tweak these later to fine tune your line follower.

Copy

{
  "register_models": [
    {
      "parameters": {
        "segment_size_px": 100,
        "hue_tolerance_pct": 0.06,
        "detect_color": "#19FFD9"
      },
      "type": "color_detector",
      "name": "green_detector"
    }
  ]
}

![A screenshot of the Vision Service configuration on the SERVICES sub-tab of the CONFIG tab. The attributes field has been populated with raw JSON identical to that in the copy-pasteable JSON field below.](/tutorials/img/webcam-line-follower/lf-vis-config.png)

Raw JSON:

```json {class="line-numbers linkable-line-numbers"}
{
  "register_models": [
    {
      "parameters": {
        "segment_size_px": 100,
        "hue_tolerance_pct": 0.06,
        "detect_color": "#19FFD9"
      },
      "type": "color_detector",
      "name": "green_detector"
    }
  ]
}
```

### Configuring the visualizer

This step is optional, but if you'd like to see the bounding boxes that the color detector identifies, you'll need to configure a [transform camera](/components/camera/transform).
This isn't another piece of hardware, but rather a virtual "camera" that takes in the stream from the webcam we just configured and outputs a stream overlaid with bounding boxes representing the color detections.

In the **config** tab, make a new component with name `show_detections`, type `camera` and model `transform`.
Set the `stream` to `"color"` and set the `source` to `"my_camera"` or whatever you named your webcam.

You'll need to edit the `pipeline` section as well with `type` set to `"detections"`, and `detector_name` set to the name of your color detector (`"green_detector"` in our case).

You can paste the following into the **Attributes** section of the `show_detections` config builder:

```json {class="line-numbers linkable-line-numbers"}
{
  "stream": "color",
  "source": "my_camera",
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "detector_name": "green_detector"
      }
    }
  ]
}
```

If you save the config and go to the **control** tab, you should now be able to view the camera feed with color detector overlays superimposed on the image.

![A screenshot of the CONTROL tab showing the base card with the show_detections transform camera stream displayed. A green line crosses the left portion of the camera image, and a red box around it is labeled "cyan: 1.00".](/tutorials/img/webcam-line-follower/bounding.png)

### Full example config

Below is an example JSON file that includes the board, base and camera components, and a Vision Service color detector.
You may have different pin numbers and other attributes depending on your hardware setup.

{{%expand "Click to view JSON" %}}

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
      "name": "leftm",
      "type": "motor",
      "model": "gpio",
      "attributes": {
        "pins": {
          "a": "15",
          "b": "16"
        },
        "board": "local",
        "max_rpm": 200
      },
      "depends_on": [
        "local"
      ]
    },
    {
      "name": "rightm",
      "type": "motor",
      "model": "gpio",
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
      "depends_on": [
        "local"
      ]
    },
    {
      "name": "scuttlebase",
      "type": "base",
      "model": "wheeled",
      "attributes": {
        "width_mm": 400,
        "wheel_circumference_mm": 258,
        "left": [
          "leftm"
        ],
        "right": [
          "rightm"
        ]
      },
      "depends_on": [
        "leftm",
        "rightm"
      ]
    },
    {
      "name": "my_camera",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    },
    {
      "name": "show_detections",
      "type": "camera",
      "model": "transform",
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
      "name": "",
      "type": "vision",
      "attributes": {
        "register_models": [
          {
            "type": "color_detector",
            "parameters": {
              "detect_color": "#19FFD9",
              "segment_size_px": 100,
              "hue_tolerance_pct": 0.06
            },
            "name": "green_detector"
          }
        ]
      }
    }
  ]
}
```

{{% /expand %}}

## How line following works

You position the rover so that its camera can see the colored line.

If the color of the line is detected in the top center of the camera frame, the rover will drive forward.
When it doesn’t see the line color there, it will search for the color in the left side of the camera frame.
If it detects the color there, it will turn to the left.
If it doesn’t see the color there it’ll repeat the process on the right.
Once the line is back in the center front of the camera frame, the rover continues forward.

When the rover no longer sees any of the line color anywhere in the front portion of the camera frame, it stops and the program ends.

{{<gif webm_src="/tutorials/img/webcam-line-follower/lf-tape-follow3.webm" mp4_src="/tutorials/img/webcam-line-follower/lf-tape-follow3.mp4" alt="The green line the camera sees as the rover moves along it." max-width="300px">}}

## Let’s write some code

1. Make sure you have Python installed.
   You can double-check this by running:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   python --version
   ```

   or if you have multiple versions of Python installed, try

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   python3.9 --version
   ```

   or

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   python3.8 --version
   ```

   We at Viam are running Python 3.9.2 (Python 3.8 is also supported) for this tutorial.

2. Make sure you have the [Viam Python SDK](https://python.viam.dev/) installed.
3. Open a file in your favorite IDE and paste in [the code from the earlier referenced repo](https://github.com/viam-labs/line-follower/blob/main/rgb_follower.py).
4. Adjust the component names to match the component names you created in your config file.
   In this case, the component names that you may need to change are **scuttlebase**, **my_camera**, and **green_detector**.
5. From your robot’s page on the [Viam app](https://app.viam.com/), go to the **code sample** tab.
   Find the Python SDK field and copy the robot address (which will likely have the form <file>robotName-main.1234abcd.local.viam.cloud:8080</file>) and payload (a nonsensical string of numbers and letters) from it into the corresponding fields towards the top of your command file.
   This allows your code to connect to your robot.

   {{% alert title="Caution" color="caution" %}}
   Do not share your robot secret or robot address publicly.
   Sharing this information compromises your system security by allowing unauthorized access to your computer.
   {{% /alert %}}

6. Save the code in a directory of your choice.
7. To get the code onto the Pi you have a few options.
   If you intend to make lots of tweaks to the code over time it may be most convenient for you to set up a [Mutagen Sync](https://mutagen.io/documentation/introduction/getting-started/) session from a directory on your computer to a directory on your Pi.
   If you’re just trying to get this running as quickly as possible, do the following:

   1. In your Pi terminal, navigate to the directory where you’d like to save your code.
      Run, <file>nano rgb_follower.py</file> (or replace <file>rgb_follower</file> with the your desired filename).
   2. Paste all your code into this file.
      Type **CTRL + X** to close the file.
      Type **Y** to confirm file modification, then press enter to finish.

## Controlling your rover with Viam

1. Go to your robot’s page on [the Viam app](https://app.viam.com/).
   Verify that it’s connected by refreshing the page and ensuring that **Last Online** (in the top banner) says, "Live."
2. Go to the **control** tab and try viewing the camera and also  pressing buttons in the Base section to move your robot around.
   Ensure that the base moves as expected.
   If one or both drive motors are going backwards, you can power down the Pi by running `sudo poweroff`, unplug the battery, and switch the wires to the motor before powering it back on.

   {{<gif webm_src="/tutorials/img/webcam-line-follower/lf-viamapp-base-view5.webm" mp4_src="/tutorials/img/webcam-line-follower/lf-viamapp-base-view5.mp4" alt="Driving the base from the Viam app's CONTROL tab." max-width="600px">}}

3. Now for the creative part: Use your colored tape to make a path for your robot to follow.
   Perhaps a circle or other shape, or perhaps a path from one point of interest to another.
   Sharp corners will be more challenging for the robot to follow so consider creating more gentle curves.
4. Set your robot on the line such that the line appears in the front of the camera’s view.
   Verify that the camera sees the line by viewing the camera feed on the **control** tab of the robot page.
   <img src="/tutorials/img/webcam-line-follower/lf-cam-view6.png" alt="The camera view in the control tab on the robot page" width="600" />
5. In a terminal window, SSH to your Pi by running:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   ssh <your_username>@<your_pi’s_name>.local
   ```

   Replace the angle brackets and the example text with your actual Pi username and the name of your Pi.
   Remember to delete the angle brackets!

6. In this Pi terminal go ahead and run the code:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   python ~/myCode/rgb_follower.py
   ```

   Be sure to replace <span class="file">~/myCode</span> with the path to the directory where you saved your Python script, and <file>rgb_follower.py</file> with whatever you named your Python script file.
   You may need to call `python3.9` or `python3.8` instead of `python`, depending on how you configured your Pi.

The robot should continue moving along the line until it no longer sees the color of your detector except at the back of the frame, at which point it should stop moving and the code will terminate.

## Summary

By now you have learned how to configure a wheeled base and camera with Viam.
You have access to the **control** tab from which you can drive your rover around with WASD keys.
You have learned to use the Viam Vision Service color detector, which can be useful in many other projects.
You have a rover following a path of your choice, anywhere you want it to go!

## Troubleshooting

### Issue: The rover moves too fast to track the line

If your rover keeps driving off the line so fast that the color detector can’t keep up, you can try two things:

- Slow down the move straight and turning speeds of the rover by decreasing the values of `linear_power` and `angular_power`.
  - Conversely, if your rover is moving too slowly or stalling, increase the numbers (closer to 1.0 which represents full power).</li>
- Position the camera differently, perhaps so that it is higher above the floor but still pointing downward.
This will give it a wider field of view so it takes longer for the line to go out of view.

### Issue: The robot is not detecting the color accurately

Things to try:

- Add a `saturation_cutoff_pct` and/or a `value_cutoff_percent` [(documented here)](/services/vision/detection#color_detector) to your Vision Service parameters.
- Try to achieve more consistent lighting on and around the line.
- Try a different color of line, or a different background.
Be sure to update your `detect_color` parameter accordingly.

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Bonus Challenges

1. Automatically detect what color line the robot is on and follow that.
2. Use two differently colored lines that intersect and make the robot switch from one line to the other.
3. Put two rovers on intersecting lines and write code to keep them from crashing into each other.
