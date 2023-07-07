---
title: "Configure a SCUTTLE Robot with a Camera"
linkTitle: "Configure a SCUTTLE Robot"
weight: 15
type: "docs"
description: "Configure a SCUTTLE Robot on the Viam platform."
image: "/tutorials/img/scuttlebot/createcomponent.png"
images: ["/tutorials/img/scuttlebot/createcomponent.png"]
imageAlt: "The Viam app UI showing the CONFIG tab of a robot."
tags: ["base", "camera", "raspberry pi", "scuttle"]
aliases:
  - "/tutorials/scuttlebot"
  - "/tutorials/scuttlebot/scuttlebot"
authors: []
languages: [ "python", "go" ]
viamresources: [ "board", "arm", "motor" ]
level: "Beginner"
date: "2 August 2022"
cost: 540
---

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/LAMxYci242E">}}

## Requirements

- A Raspberry Pi with Raspberry Pi OS 64-bit Lite and the `viam-server` installed.

Refer to [Installing Raspberry Pi OS on the Raspberry Pi](/installation/prepare/rpi-setup/#install-raspberry-pi-os), if necessary.

- [A SCUTTLE Robot](https://www.scuttlerobot.org/shop/)
- A USB camera (webcam)

## Start configuring your robot

1. Go to [the Viam app](https://app.viam.com).
2. If you already created your robot in the app, navigate to its **Config** tab and skip to [Configuring the board](#configuring-the-board).
3. Create an **Organization**.
   If you already have an Organization, then this step is optional.
   If you need help with organizations and locations, see our [guide to using the Viam app](/manage/fleet/).
4. Create a **Location**.
   If you already have a Location, then this step is optional.
5. Create a **robot** and navigate to its **Config** tab.
   We will stay in **Builder** mode for this tutorial (as opposed to **Raw JSON**).
   ![A screenshot of the Viam app UI showing the CONFIG tab of a robot.](../../img/scuttlebot/createcomponent.png)

{{% alert title="Tip" color="tip" %}}
When naming components, remember to use consistent letter casing to avoid problems with "missing" components.
{{% /alert %}}

## Configuring the board

Add your first component, the [board](/components/board/) (in this case the Raspberry Pi).

1. Enter a name for your board in the **Name** field.
   In this tutorial, we've named the board "local."
   As long as you're consistent, you can name the board whatever you want.
2. Select the component **Type**, "board."
3. Select "pi" from the **Model** drop-down.
4. Click **Create Component** and the board component panel will expand.

We don't need to worry about any other attributes for this component.
![Screenshot of the component configuration panel for a board component. The name (local), type (board) and model (pi) are shown at the top of the panel. No other attributes are configured.](../../img/scuttlebot/board-empty-json.png)

## Configuring the motors

### Adding the right motor

The next step is to add a motor and make it spin a wheel.

1. Begin by adding the right motor, naming the component "right".
2. Select "motor" from the **Type** drop-down.
3. Select "gpio" from the **Model** drop-down.
4. Click **Create Component**, which will generate the motor component panel.
5. Then select `local` from the **Board** drop-down (since the motor is wired to the Raspberry Pi named "local").
6. Set **Max RPM** to `100`.
7. Next, you'll need to describe how the motor is wired to the Pi:
   1. Switch the Component Pin Assignment Type to **In1/In2**.
   2. Set **A/In1** to `16`.
   3. Set **B/In2** to `15`.
   4. Leave the `pwm` (pulse-width modulation) pin blank, because this specific motor driver’s configuration does not require a separate PWM pin.

![Screenshot of the motor config panel with the attributes set as described above.](../../img/scuttlebot/pi-rhwheel.png)
<br><br>

{{% expand "Click to view the raw JSON for the right motor" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "right",
  "type": "motor",
  "model": "gpio",
  "attributes": {
    "pins": {
      "a": "16",
      "b": "15",
      "pwm": ""
    },
    "board": "local",
    "max_rpm": 100,
    "dir_flip": false
  },
  "depends_on": []
}
```

{{% /expand %}}

{{% alert title="Tip" color="tip" %}}
If your wheel turns in reverse when it should turn forward, add the `dir_flip` attribute (found by clicking **Show more**) and set it to "true."
{{% /alert %}}

### Testing the motor configuration

Having configured a board and a motor component, you can now actuate your motor.
Save the config by clicking **Save config** at the bottom of the page, then click over to the **Control** tab.

Here you'll see a panel for the right `motor`.
You'll use this panel to set the motor's `power` level.

![Power level adjustment](../../img/scuttlebot/pi-moverhmotor.png)

Be careful when activating your robot!
Start with the power level set to 10% and increase it incrementally until the wheel rotates at a reasonable speed, clicking **Run** at each increment.

{{% alert title="Tip" color="tip" %}}
A "whining" sound emitted from the motor indicates that the power level is not high enough to turn the armature.
If this happens, increase the power level by 10% increments until it starts to turn.
{{% /alert %}}

At this point, the right-side wheel should be working.

### Adding the left motor

Now, you're ready to add the left-side motor.
This will be similar to adding the right motor.

1. Name the component "left".
2. Select "motor" from the **Type** drop-down.
3. Select "gpio" from the **Model** drop-down.
4. Click **Create Component**.
5. Select `local` from the **Board** drop-down.
6. Set the **Max RPM** attribute to `100`.
7. Configure the motor's pins:
   1. Switch the Component Pin Assignment Type to **In1/In2**.
   2. Set **A/In1** to `12`.
   3. Set **B/In2** to `11`.

{{% expand "Click to view the raw JSON for the left motor" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "left",
  "type": "motor",
  "model": "gpio",
  "attributes": {
    "pins": {
      "a": "12",
      "b": "11",
      "pwm": ""
    },
    "board": "local",
    "max_rpm": 100,
    "dir_flip": false
  },
  "depends_on": []
}
```

{{% /expand %}}

With both motors configured, the **Control** tab now display panels for both motors:

<img src="../../img/scuttlebot/scuttle-bothmotors.png" alt="Motor panels">

Viam ([app.viam.com](https://app.viam.com)) displays component panels in order of their creation.
Don't worry if your motor panels are not adjacent.

## Configuring the base

It's time to configure a [base component](/components/base/), which describes the geometry of your chassis and wheels so that the software can calculate how to steer the rover in a coordinated way.
Configuring a base component will give you a nice UI for moving the rover around.

From the **Config** tab:

1. Give your base a name.
2. Enter "base" in **Type**.
3. Enter "wheeled" in **Model**.
4. In the **Right Motors** drop-down select "right."
5. In the **Left Motors** drop-down select "left."
6. Enter "400" in `width_mm` (measured between the midpoints of the wheels).
7. Enter "250" in `wheel_circumference_mm`.

    The `left` and `right` attributes represent the motors corresponding to the left and right sides of the rover.
    Since we named the motors "left" and "right", you can simply add "left" and "right" between the brackets for your set of motors, respectively.

The attributes of your base component's config should look something like this:

```json {class="line-numbers linkable-line-numbers"}
{
 "width_mm": 400,
 "wheel_circumference_mm": 250,
 "left": ["left"],
 "right": ["right"]
}
```

When you save the config and switch to the **Control** tab, you'll see new control buttons for the base.
In the **Keyboard** tab, toggle your keyboard control to active.
Use **W** and **S** to go forward and back, and **A** and **D** to arc and spin.

<img src="../../img/scuttlebot/pi-kybrd-control.png" width="300px" alt="WASD controls">

If you click the **Discrete** tab, then you'll see different movement modes such as `Straight` and `Spin`; and different movement types such as `Continuous` and `Discrete` and directions such as `Forwards` and `Backwards`.

<img src="../../img/scuttlebot/pi-discrete.png" alt="Discrete controls">

Now you have a rover that you can drive using Viam's UI!
Awesome!

Try driving your SCUTTLE Robot around using the WASD keyboard controls described above.

{{% alert title="Caution" color="caution" %}}
Ensure that your robot has sufficient space to drive around without hitting anyone or anything.
{{% /alert %}}

## Configuring the encoders

Before configuring the encoders, you must configure I2C bus `1` on the board:

```json
{
      "name": "<board_name>",
      "type": "board",
      "model": "<model_name>"
      "attributes": {
        "i2cs": [
          {
            "bus": "1",
            "name": "main"
          }
        ]
      },
      "depends_on": [],
}
```

Now, configure the left and right encoders as follows:

- Left encoder:
  - Configure the left encoder with *Name* `lenc`, **Type** `encoder`, and **Model** `AMS-AS5048`.
  - Paste the following in the **Attributes** field, changing the board name to match the name of your board:

  ```json
  {
      "name": "<encoder_name>",
      "type": "encoder",
      "model": "AMS-AS5048"
      "board": "<board_name>",
       "attributes": {
           "board": "<board_name>",
           "connection_type": "i2c",
            "i2c_attributes": {
                "i2c_bus": "main",
                "i2c_addr": 64
            }
       }
    }
  ```

- Right encoder:
  - Configure the left encoder with *Name* `renc`, **Type** `encoder`, and **Model** `AMS-AS5048`.
  - Paste the following in the **Attributes** field, changing the board name to match the name of your board:

  ```json
  {
      "name": "<encoder_name>",
      "type": "encoder",
      "model": "AMS-AS5048"
      "board": "<board_name>",
       "attributes": {
           "board": "<board_name>",
           "connection_type": "i2c",
            "i2c_attributes": {
                "i2c_bus": "main",
                "i2c_addr": 65
            }
       }
    }
  ```

## Configuring the camera

Finally, we'll add a camera to your SCUTTLE Robot.

1. Enter a name of your choice in **Name**.
2. Enter "camera" in **Model**.
3. Click **Create Component**.

Now, you'll see the config panel for the camera component:
<img src="../../img/scuttlebot/pi-cam-control.png" alt="Camera component config panel" >

On the camera config panel, set the `video_path`.

Once you save the config, you'll be able to see your camera's stream in the **Control** tab.

## On completion

After successfully completing this tutorial, you have a fully configured SCUTTLE Robot.
You can drive it around and view its camera stream.

To take things to the next level, check out our [Color Detection with SCUTTLE Robot](/tutorials/services/color-detection-scuttle/) tutorial or create your own camera-related tutorial.
Alternatively, you can  check out our [Bluetooth Gamepad For SCUTTLE](/tutorials/control/scuttle-gamepad/) tutorial or our [Line Follower Robot tutorial](/tutorials/services/webcam-line-follower-robot/).

## Documents referenced

- [Installing Raspberry Pi OS on the Raspberry Pi](/installation/prepare/rpi-setup/#install-raspberry-pi-os)

- [Color Detection with SCUTTLE Robot on Viam](/tutorials/services/color-detection-scuttle/)

- [Controlling a SCUTTLE Robot on Viam with a Bluetooth Gamepad](/tutorials/control/scuttle-gamepad/)

- [Line Following with SCUTTLE Robot on Viam](/tutorials/services/webcam-line-follower-robot/)
