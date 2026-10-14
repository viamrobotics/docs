---
title: "Configure a Rover like Yahboom or SCUTTLE"
linkTitle: "Configure a Rover"
type: "docs"
description: "Configure a rover like the a Yahboom 4WD Rover or a SCUTTLE robot on the Viam platform."
capabilities: ["hw-mobility", "hw-actuation", "hw-camera", "docs"]
diataxis: tutorial
images: ["/tutorials/scuttlebot/scuttle-on-floor-cropped.png"]
imageAlt: "A SCUTTLE robot on a carpeted floor."
tags: ["base", "camera", "scuttle", "yahboom"]
aliases:
  - "/tutorials/scuttlebot"
  - "/tutorials/scuttlebot/scuttlebot"
  - "/tutorials/yahboom-rover/"
  - "/tutorials/control/yahboom-rover/"
authors: ["Hazal Mestci"]
languages: ["python", "go"]
viamresources: ["board", "motor", "camera", "base", "encoder"]
platformarea: ["core"]
level: "Beginner"
date: "2022-08-02"
updated: "2024-04-17"
cost: 540
---

This tutorial will guide you through configuring a rover.

<!-- LEARNING GOAL: After following this tutorial, you will be able to configure any rover using existing built-in or modular components. -->

If you are using a SCUTTLE, a Yahboom rover, or a different rover, this tutorial covers instructions for your rover model.

{{< alert title="Viam Rover" color="note" >}}
If you are using a Viam Rover, use the [Viam Rover tutorial fragment](/reference/device-setup/viam-rover/fragments/) instead.
{{< /alert >}}

## Requirements

- A running an instance of `viam-server`.
  See our [Installation Guide](/set-up-a-machine/first-machine/) for instructions.
- A rover like the [SCUTTLE robot](https://www.scuttlerobot.org/shop/) or the Yahboom 4WD Smart Robot.

Make sure your rover is assembled before starting this tutorial.

## Start configuring your robot

{{% snippet "setup.md" %}}

Once connected, navigate to the machine's **CONFIGURE** tab.

![A SCUTTLE robot on a carpeted floor.](/tutorials/scuttlebot/scuttle-on-floor.png)

The configuration for each rover is different depending on which {{< glossary_tooltip term_id="component" text="components" >}} your rover is composed of.
In the following, you can see two popular examples with components that are present on most rovers:

## Configure the board

The first component you will add is the [board](/reference/components/board/) which represents the Raspberry Pi to which the other components are wired.

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `raspberry pi`, then select the `raspberry-pi/rpi` block.
Enter `local` as the name and click **Add to machine**.
You can use a different name but will then need to adjust the name in the following steps to the name you choose.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

You don't need to add any attributes for your board.

## Configuring the motors and encoders

### Configure the encoders

{{< alert title="Note" color="note" >}}
Not all rovers require the configuration of encoders.
If your motors work without encoders, skip to [configuring your motors](#configure-the-motors).
{{< /alert >}}

Configure the left and right encoders as follows:

{{< tabs >}}
{{% tab name="SCUTTLE" %}}

{{< tabs name="Configure AMS-AS5048 Encoders" >}}
{{% tab name="Config Builder" %}}

Start with the right encoder:

#### Right encoder

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `as5048`, then select the `ams/as5048` block.
Enter `renc` as the name and click **Add to machine**.

Click the **board** dropdown list and select the name of your board, `local`.

In the **i2c bus** field type `1`, and in the **i2c address** field type `65`.

#### Left encoder

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `as5048`, then select the `ams/as5048` block.
Enter `lenc` as the name for your encoder and click **Add to machine**.

Click the **board** dropdown list and select the name of your board, `local`.

In the **i2c bus** field type `1`, and in the **i2c address** field type `64`.

{{% /tab %}}
{{% tab name="JSON" %}}

Add the following JSON objects to the `components` array:

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "lenc",
    "api": "rdk:component:encoder",
    "model": "viam:ams:as5048",
    "attributes": {
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": "1",
        "i2c_addr": 64
      }
    }
},
{
    "name": "renc",
    "api": "rdk:component:encoder",
    "model": "viam:ams:as5048",
    "attributes": {
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": "1",
        "i2c_addr": 65
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Other" %}}

Follow the instructions for the [model of encoder](/reference/components/encoder/) your rover uses to configure your encoders and configure at least a `right` and a `left` encoder.

{{% /tab %}}
{{< /tabs >}}

### Configure the motors

{{< tabs name="motors-config">}}
{{% tab name="SCUTTLE" %}}

{{< tabs name="gpio-config">}}
{{% tab name="Config Builder" %}}

Start with the right motor:

#### Right motor

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `gpio`, then select the `motor/gpio` block.
Enter `right` as the name or use the suggested name for your motor and click **Add to machine**.

In the motor card's attributes editor, enter the following attributes.
They set `local`, the Raspberry Pi the motor is wired to, as the board, use the `renc` encoder with `2` ticks per rotation, and describe how the motor is wired to the Pi in `In1/In2` mode.
Leave the `pwm` (pulse-width modulation) pin blank, because this specific motor driver's configuration does not require a separate PWM pin.

```json
{
  "board": "local",
  "pins": {
    "a": "16",
    "b": "15",
    "pwm": ""
  },
  "encoder": "renc",
  "ticks_per_rotation": 2
}
```

#### Left motor

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `gpio`, then select the `motor/gpio` block.
Enter `left` as the name or use the suggested name for your motor and click **Add to machine**.

In the motor card's attributes editor, enter the following attributes, which use the `lenc` encoder:

```json
{
  "board": "local",
  "pins": {
    "a": "12",
    "b": "11",
    "pwm": ""
  },
  "encoder": "lenc",
  "ticks_per_rotation": 2
}
```

{{% /tab %}}
{{% tab name="JSON" %}}

Add the following JSON objects to the `components` array:

```json
{
  "name": "right",
  "model": "gpio",
  "api": "rdk:component:motor",
  "attributes": {
    "pins": {
      "a": "16",
      "b": "15",
      "pwm": "",
      "dir": ""
    },
    "board": "local",
    "dir_flip": false,
    "encoder": "renc",
    "ticks_per_rotation": 2
  },
  "depends_on": [ "local" ]
},
{
  "name": "left",
  "model": "gpio",
  "api": "rdk:component:motor",
  "attributes": {
    "pins": {
      "a": "12",
      "b": "11",
      "pwm": ""
    },
    "board": "local",
    "dir_flip": false,
    "encoder": "lenc",
    "ticks_per_rotation": 2
  },
  "depends_on": [ "local" ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Yahboom" %}}

Since both right (and left) side motors of the Yahboom rover are wired together to a single motor driver, you configure the right (and left) side motors as a single [motor component](/reference/components/motor/).

Start with the right set of wheels.

#### Right motor

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `gpio`, then select the `motor/gpio` block.
Enter `right` as the name or use the suggested name for your motor and click **Add to machine**.

In the motor card's attributes editor, enter the following attributes.
They set `local` as the board the motor driver is wired to and describe how the motor is wired to the board in the A/B/PWM mode this motor driver uses.
If you followed the setup instructions for putting together your Yahboom rover correctly, the pins are as follows.
Leave out the `dir` pin, because Yahboom's motor driver uses an a/b/pwm configuration.

```json
{
  "board": "local",
  "pins": {
    "a": "35",
    "b": "37",
    "pwm": "33"
  },
  "max_rpm": 300
}
```

You can ignore the other optional attributes.

#### Left motor

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `gpio`, then select the `motor/gpio` block.
Enter `left` as the name or use the suggested name for your motor and click **Add to machine**.

In the motor card's attributes editor, enter the following attributes.
They set `local` as the board the motor driver is wired to and describe how the motor is wired to the board in the A/B/PWM mode this motor driver uses.
If you followed the setup instructions for putting together your Yahboom rover correctly, the pins are as follows.
Leave out the `dir` pin, because Yahboom's motor driver uses an a/b/pwm configuration.

```json
{
  "board": "local",
  "pins": {
    "a": "38",
    "b": "40",
    "pwm": "36"
  },
  "max_rpm": 300
}
```

You can ignore the other optional attributes.

{{% /tab %}}
{{% tab name="Other" %}}

Follow the instructions for the [model of motor](/reference/components/motor/) your rover uses to configure your motors and configure at least a `right` and a `left` motor.

{{% /tab %}}
{{< /tabs >}}

#### Test the motor configuration

{{< alert title="Caution" color="caution" >}}

Ensure the rover has sufficient space to drive around without hitting anyone or anything.

If you don't have enough space, consider holding your robot off the ground so it cannot collide with anything unexpected.

{{< /alert >}}

Now that you have configured your motors, you can actuate them.
Make sure your machine is turned on.
Navigate to the **Control** tab.

You'll see a panel for each configured component.

![Motor panels](/tutorials/scuttlebot/scuttle-bothmotors.png)

Click on the panel for the right `motor`.

![Power level adjustment](/tutorials/scuttlebot/pi-moverhmotor.png)

Try changing the motor's **power** level and click **Run**.

{{< alert title="Caution" color="caution" >}}
Be careful when using your motors!
Start with the power level set to 20% and increase it incrementally (about 10% each time) until the wheel rotates at a reasonable speed, clicking **Run** at each increment.
If you hear a "whining" sound from the motor, the power level is not high enough to turn the armature.
If this happens, increase the power level by 10% increments until it starts to turn.
{{< /alert >}}

If your wheel turns in reverse when it should turn forward, add `"dir_flip": true` to the motor's attributes.

There, you should see a panel for the right motor: you can use this panel to set the motor's power level.

## (Optional) Configure the camera

Optionally, add a camera to your rover.

{{< tabs name="Configure a Webcam" >}}
{{% tab name="Config Builder" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `webcam`, then select the `camera/webcam` block.
Enter a name or use the suggested name for your camera and click **Add to machine**.

Leave the camera's attributes empty and the camera will use the default video path for your machine.
If this doesn't work when you test your camera later, [find your camera's video path](/reference/components/camera/webcam/#using-video_path) and set it as `video_path` in the camera card's attributes editor.

{{% /tab %}}
{{% tab name="JSON" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "Webcam",
  "model": "webcam",
  "api": "rdk:component:camera",
  "attributes": {
    "video_path": "<PATH_TO_YOUR_WEBCAM>"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

If your rover has its camera mounted on a pair of [servos](/reference/components/servo/), like the Yahboom rover, you can use these to control the pan and tilt of the camera.

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `rpi-servo`, then select the `raspberry-pi/rpi-servo` block.
Enter `pan` as the name and click **Add to machine**.

Set `Depends On` to `local`, and `pin` to the pin the servo is wired to (`23` for the Yahboom rover).

Finally, add the tilt `servo` as well.
Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `rpi-servo`, then select the `raspberry-pi/rpi-servo` block.
Enter `tilt` as the name and click **Add to machine**.

Set `Depends On` to `local`, and `pin` to the pin the servo is wired to (`21` for the Yahboom rover).

### Test the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Configure the base

Next, configure the [base component](/reference/components/base/), which describes the geometry of your chassis and wheels so that the software can calculate how to steer the rover in a coordinated way.
Configuring a {{% glossary_tooltip term_id="base" text="base"%}} component also provides you with a nice UI for moving the rover around.

{{< alert title="Note" color="note" >}}
Viam supports most rovers with built-in models like the [`wheeled`](/reference/components/base/wheeled/) base.
If your rover is not supported out of the box, follow the [Create a Modular Resource to Control a Rover](/tutorials/custom/controlling-an-intermode-rover-canbus/) tutorial to create a model for your rover or mobile robot.
{{< /alert >}}

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="Config Builder" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Blocks**.
Search for `wheeled`, then select the `base/wheeled` block.
Enter a name or use the suggested name for your base and click **Add to machine**.

{{< tabs >}}
{{% tab name="SCUTTLE" %}}

In the base card's attributes editor, enter the motors attached to the base as your `right` and `left` motors, the wheel circumference, and the width between the midpoints of the wheels:

```json
{
  "right": ["right"],
  "left": ["left"],
  "wheel_circumference_mm": 250,
  "width_mm": 400
}
```

{{% /tab %}}
{{% tab name="Yahboom" %}}

In the base card's attributes editor, enter the motors attached to the base as your `right` and `left` motors, the wheel circumference, and the width between the midpoints of the wheels:

```json
{
  "right": ["right"],
  "left": ["left"],
  "wheel_circumference_mm": 220,
  "width_mm": 150
}
```

{{% /tab %}}
{{% tab name="Other" %}}

In the base card's attributes editor, set `right` and `left` to lists of the motors attached to the base.
Measure the wheel circumference in mm and set it as `wheel_circumference_mm`.
Measure the width in mm between the midpoints of the wheels and set it as `width_mm`.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON" %}}

```json
{
  "components": [
    {
      "attributes": {
        "board": "local",
        "pins": {
          "pwm": "",
          "a": "16",
          "b": "15"
        }
      },
      "model": "gpio",
      "name": "right",
      "api": "rdk:component:motor"
    },
    {
      "attributes": {
        "board": "local",
        "pins": {
          "pwm": "",
          "a": "12",
          "b": "11"
        }
      },
      "model": "gpio",
      "name": "left",
      "api": "rdk:component:motor"
    },
    {
      "attributes": {
        "left": ["left"],
        "right": ["right"],
        "wheel_circumference_mm": 250,
        "width_mm": 400
      },
      "model": "wheeled",
      "name": "your-wheeled-base",
      "api": "rdk:component:base"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Save the config by clicking **Save** at the top right of the page.

### Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

## Next steps

Now that you have fully configured your SCUTTLE robot, you can drive it around and view its camera stream.

To take things to the next level, check out one of the following tutorials:

{{< cards >}}
{{% card link="/tutorials/services/color-detection-scuttle" %}}
{{% card link="/tutorials/control/gamepad/" %}}
{{% card link="/tutorials/services/webcam-line-follower-robot/" %}}
{{< /cards >}}
