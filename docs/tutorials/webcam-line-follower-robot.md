---
title: "How to Build a Line Follower with a Rover and a Webcam"
linkTitle: "RGB Line Follower"
weight: 35
type: "docs"
description: "Build a line-following robot that relies on a webcam and color detection."
---
Many line-following robots rely on a dedicated array of infrared sensors to follow a dark line on a light background or a light line on a dark background.
This tutorial uses a standard webcam in place of these sensors, and allows a robot to follow a line of any color that is at least somewhat different from the background.

<div style="column-count:2;column-gap-40px">
<div>
<p><strong>Goal</strong>: To make a wheeled robot follow a colored line along the floor using a webcam and the Viam <a href="/services/vision#detection">vision service color detector</a>.
</p></div>
<div><img src="/tutorials/img/webcam-line-follower/lf-following1.gif" /></div>
</div>

**What you will learn**:<BR>

- How to use the Viam vision service including color detectors
- How to use the [Viam Python SDK](https://github.com/viamrobotics/viam-python-sdk)[^psdk], including:
    - How to establish communication between the code you write and your robot
    - How to send commands to components of your robot

[^psdk]: Viam Python SDK: <a href="https://github.com/viamrobotics/viam-python-sdk/" target="_blank">ht<span></span>tps://github.com/viamrobotics/viam-python-sdk</a>

<a href="https://github.com/viam-labs/line-follower/" target="_blank">**Line Follower Code on GitHub**</a>[^repo]

[^repo]: Line Follower GitHub repo: <a href="https://github.com/viam-labs/line-follower/" target="_blank">ht<span></span>tps://github.com/viam-labs/line-follower/</a>

## What you'll need

- A single board computer [running an instance of viam-server](../../getting-started/rpi-setup/)
    - This tutorial assumes the use of a Raspberry Pi running a 64-bit Linux distribution, but these instructions could potentially be adapted for other boards.
- [A wheeled base component](../../components/base/)
    - We used a <a href="https://www.scuttlerobot.org/shop/" target="_blank" />SCUTTLE Robot</a>[^sr] for this project, but any number of other wheeled bases could work, as long as they can carry the compute module and camera, and can turn in place.
- RGB camera
    - A common off-the-shelf webcam [(such as this)](https://www.amazon.com/Webcam-Streaming-Recording-Built-Correction/dp/B07M6Y7355/ref=sr_1_5?keywords=webcam&qid=1658796392&sr=8-5&th=1) connected to the Pi’s USB port, or something like an [ArduCam](https://www.uctronics.com/arducam-for-raspberry-pi-camera-module-with-case-5mp-1080p-for-raspberry-pi-3-3-b-and-more.html/) with a ribbon connector to the Pi’s camera module port.
    - You must mount the camera to the front of the rover pointing down towards the floor.
- Colored tape and floor space
    - Any color is suitable as long as its color is somewhat different from the floor color.
    For our tutorial, we used green electrical tape.
    - Non-shiny floors tend to work best.
[^sr]: SCUTTLE Robot <a href="https://www.scuttlerobot.org/shop/" target="_blank" />https://www.scuttlerobot.org/shop/</a>

<p class="Mycaption" ><em>Figure 1: A SCUTTLE robot base with a camera mounted on the front, pointing mostly down and slightly forwards.</em><br>
<img src="/tutorials/img/webcam-line-follower/lf-scuttle2.png" width="600" /></p>

## Configuration using Viam

If you haven’t already, please set up the Raspberry Pi per [these instructions](../../getting-started/rpi-setup/).

### Configuring the hardware components

Configure the board per the [Board Component topic](/components/board/).
We named ours `local`.
Use type `board` and model `pi` if you're using a Raspberry Pi.

Configure the wheeled base per the [Base Component topic](../../components/base/).
We named ours `scuttlebase`.
	
Configure the [camera](../../components/camera/) as described in this tutorial: [Connect and configure a webcam](../../tutorials/configure-a-camera/#connect-and-configure-a-webcam).
You can skip the section on camera calibration since it is not needed for the line follower.

Your webcam configuration in the Config Builder will look something like this:

![A screenshot of the webcam configuration UI with video_path set to video0.](/tutorials/img/webcam-line-follower/lf-cam-config.png)

Or if you prefer the raw JSON:

```json-viam
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

### Configuring the vision service

We’ll use the Viam [vision service color detector](/services/vision/#detection) to identify the line to follow.

In the **SERVICES** section of the **CONFIG** tab, configure a color detector for the color of your tape line.

- Use a color picker like <a href="https://colorpicker.me/" target="_blank">colorpicker.me</a>[^colorpick] to approximate the color of your line and get the corresponding hexadecimal hash to put in your config.
Put this hash in the `detect_color` parameter.
We used #19FFD9 to represent the color of green electrical tape.

[^colorpick]: Color picker: <a href="https://colorpicker.me/" target="_blank">https://colorpicker.me/</a>
  
- We used a segment size of 100 pixels, and a tolerance of 0.06, but you can tweak these later to fine tune your line follower.

What this will look like in the Config Builder:

![A screenshot of the vision service configuration on the SERVICES sub-tab of the CONFIG tab. The attributes field has been populated with raw JSON identical to that in the copy-pasteable JSON field below.](/tutorials/img/webcam-line-follower/lf-vis-config.png)

Raw JSON:

```json-viam
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

This step is optional, but if you'd like to see the bounding boxes that the color detector comes up with, you'll need to configure a [transform camera](/components/camera/#transform).
This isn't another piece of hardware, but rather a virtual "camera" that takes in the stream from the webcam we just configured and outputs a stream overlaid with bounding boxes representing the color detections.

In the **CONFIG** tab, make a new component with name `show_detections`, type `camera` and model `transform`.
Set the `stream` to `"color"` and set the `source` to `"my_camera"` or whatever you named your webcam.

You'll need to edit the `pipeline` section as well with `type` set to `"detections"`, and `detector_name` set to the name of your color detector (`"green_detector"` in our case).

You can paste the following into the **Attributes** section of the `show_detections` config builder:

```json
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

If you save the config and go to the **CONTROL** tab, you should now be able to view the camera feed with color detector overlays superimposed on the image.

![A screenshot of the CONTROL tab showing the base card with the show_detections transform camera stream displayed. A green line crosses the left portion of the camera image, and a red box around it is labeled "cyan: 1.00".](/tutorials/img/webcam-line-follower/bounding.png)

### Full example config

Below is an example JSON file that includes the board, base and camera components, and a vision service color detector.
You may have different pin numbers and other attributes depending on your hardware setup.

{{%expand "Click to view JSON" %}}
```json-viam
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

<p class="Mycaption"><em>Figure 2: A GIF of what the camera sees as the rover moves along a green line.</em><br>
<img class="center" src="/tutorials/img/webcam-line-follower/lf-tape-follow3.gif" width="300" /></p>

## Let’s write some code!

<ol><li class="spacing">Make sure you have Python installed.
You can double-check this by running:

```bash
python --version
```
or if you have multiple versions of Python installed, try
```bash
python3.9 --version
```
We at Viam are running Python 3.9.2 for this tutorial.</li>
<li class="spacing">Make sure you have the Viam Python SDK installed (<a href="https://python.viam.dev/">click for instructions</a>).</li>

<li class="spacing">Open a file in your favorite IDE and paste in <a href="https://github.com/viam-labs/line-follower/blob/main/rgb_follower.py" target="_blank">the code from the earlier referenced repo</a>.</li>
<li class="spacing">Adjust the components names to match the component names you created in your config file.
In this case, the component names that you may need to change are <strong>scuttlebase</strong>, <strong>my_camera</strong>, and <strong>green_detector</strong>.</li>
<li class="spacing">From your robot’s page on the Viam app (<a href="https://app.viam.com/">https://app.viam.com</a>), go to the Connect tab.
Find the Python SDK field and copy the robot address (which will likely have the form
<span class="file">robotName-main.1234abcd.local.viam.cloud:8080</span>) and payload (a nonsensical string of numbers and letters) from it into the corresponding fields towards the top of your command file.
This allows your code to connect to your robot.</li>
<li class="spacing">Save the code in a directory of your choice.</li>
<li class="spacing">To get the code onto the Pi you have a few options.
If you intend to make lots of tweaks to the code over time it may be most convenient for you to set up a <a href="https://mutagen.io/documentation/introduction/getting-started/">Mutagen Sync</a> session from a directory on your computer to a directory on your Pi.
If you’re just trying to get this running as quickly as possible, do the following:</li>
<ol>
<li class="spacing" style="list-style-type:lower-alpha">In your Pi terminal, navigate to the directory where you’d like to save your code.
Run,</br><span class="file">nano rgb_follower.py</span></br>(or replace <span class="file">rgb_follower</span> with the your desired filename).</li>
<li class="spacing" style="list-style-type:lower-alpha">Paste all your code into this file.</li>
<li class="spacing" style="list-style-type:lower-alpha">Type <strong>CTRL + X</strong> to close the file.
Type <strong>Y</strong> to confirm file modification, then press enter to finish.</li>
</ol></ol>

**References**:
* Line Follower Code on GitHub: <a href="" target="_blank">ht<span><span>tps://github.com/viam-labs/line-follower/blob/main/rgb_follower.py</a>
* Mutagen Sync: <a href="https://mutagen.io/documentation/introduction/getting-started/" target="_blank">ht<span><span>tps://mutagen.io/documentation/introduction/getting-started</a>

## Controlling your rover with Viam

<ol><li class="spacing">Go to your robot’s page on the Viam app (<a href="https://app.viam.com/">https://app.viam.com</a>).
Verify that it’s connected by refreshing the page and ensuring that <strong>Last Online</strong> (in the top banner) says, “Live.”</li>
<li class="spacing">Go to the <strong>CONTROL</strong> tab and try viewing the camera and also  pressing buttons in the Base section to move your robot around.
Ensure that the base moves as expected.
If one or both drive motors are going backwards, you can power down the Pi by running `sudo poweroff`, unplug the battery, and switch the wires to the motor before powering it back on.</li>
<p  class="Mycaption"><em>Figure 3: Driving the base from the Viam app's CONTROL tab.</em><br>
<img class="spacing" src="/tutorials/img/webcam-line-follower/lf-viamapp-base-view5.gif" width="600" /></p></li>
<li class="spacing">Now for the creative part: Use your colored tape to make a path for your robot to follow.
Perhaps a circle or other shape, or perhaps a path from one point of interest to another.
Sharp corners will be more challenging for the robot to follow so consider creating more gentle curves.</li>
<li class="spacing">Set your robot on the line such that the line appears in the front of the camera’s view.
Verify that the camera sees the line by viewing the camera feed on the <strong>CONTROL</strong> tab of the robot page.</li>
<p class="Mycaption"><em>Figure 4: The camera view in the <strong>CONTROL</strong> tab on the robot page.</em><br>
<img  class="spacing" src="/tutorials/img/webcam-line-follower/lf-cam-view6.png" width="600" /></p>

<li class="spacing">In a terminal window, SSH to your Pi by running:<br>

```bash
ssh <your_username>@<your_pi’s_name>.local
```
replacing the angle brackets and the example text with your actual Pi username and the name of your Pi.
Remember to delete the angle brackets!</li>

<li class="spacing">In this Pi terminal go ahead and run the code:

```bash
python ~/myCode/rgb_follower.py
```
Be sure to replace <span class="file">~/myCode</span> with the path to the directory where you saved your Python script, and <span class="file">rgb_follower.py</span> with whatever you named your Python script file.
You may need to call “python3.9” instead of “python,” depending on how you configured your Pi.</li>
</ol></ol>
The robot should continue moving along the line until it no longer sees the color of your detector except at the back of the frame, at which point it should stop moving and the code will terminate.

## Summary

By now you have learned how to configure a wheeled base and camera with Viam.
You have access to the **CONTROL** tab from which you can drive your rover around with WASD keys.
You have learned to use the Viam vision service color detector, which can be useful in many other projects.
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

- Add a `saturation_cutoff_pct` and/or a `value_cutoff_percent` [(documented here)](/services/vision/#color-detector-parameters) to your vision service parameters.
- Try to achieve more consistent lighting on and around the line.
- Try a different color of line, or a different background.
Be sure to update your `detect_color` parameter accordingly.

## Additional Troubleshooting

You can find additional assistance in the [Troubleshooting section](../../appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](http://viamrobotics.slack.com/) and we will be happy to help.

## Bonus Challenges!
1. Automatically detect what color line the robot is on and follow that.
2. Use two differently colored lines that intersect and make the robot switch from one line to the other.
3. Put two rovers on intersecting lines and write code to keep them from crashing into each other.
