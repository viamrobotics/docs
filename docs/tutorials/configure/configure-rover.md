---
title: "Configure a Rover like Yahboom or SCUTTLE"
linkTitle: "Configure a Rover"
type: "docs"
description: "Configure a rover like the a Yahboom 4WD Rover or a SCUTTLE robot on the Viam platform."
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
level: "Beginner"
date: "2022-08-02"
updated: "2024-04-17"
cost: 540
---

This tutorial will guide you through configuring a rover.
If you are using a SCUTTLE, a Yahboom rover, or a different rover, this tutorial covers instructions for your rover model.

{{< alert title="Viam Rover" color="note" >}}
If you are using a Viam Rover, use the [Viam Rover tutorial fragment](/get-started/try-viam/rover-resources/rover-tutorial-fragments/) instead.
{{< /alert >}}

## Requirements

- A Raspberry Pi running an instance of `viam-server`.
  See our [Raspberry Pi Setup Guide](/get-started/installation/prepare/rpi-setup/) for instructions.
- A rover like the [SCUTTLE robot](https://www.scuttlerobot.org/shop/) or the [Yahboom 4WD Smart Robot](https://category.yahboom.net/collections/robotics/products/4wdrobot)

## Start configuring your robot

{{% snippet "setup.md" %}}

Once connected, navigate to the machine's **CONFIGURE** tab.

![A SCUTTLE robot on a carpeted floor.](/tutorials/scuttlebot/scuttle-on-floor.png)

The configuration for each rover is different depending on which {{< glossary_tooltip term_id="component" text="components" >}} your rover is componsed of.
In the following, you can see two popular examples with components that are present on most rovers:

## Configure the board

The first component you will add is the [board](/components/board/) which represents the Raspberry Pi to which the other components are wired.

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `pi` model.
Enter `local` as the name and click **Create**.
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

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `encoder` type, then select the `AMS-AS5048` model.
Enter `renc` as the name and click **Create**.

Click the **board** dropdown list and select the name of your board, `local`.

In the **i2c bus** field type `1`, and in the **i2c address** field type `65`.

#### Left encoder

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `encoder` type, then select the `AMS-AS5048` model.
Enter `lenc` as the name for your encoder and click **Create**.

Click the **board** dropdown list and select the name of your board, `local`.

In the **i2c bus** field type `1`, and in the **i2c address** field type `64`.

{{% /tab %}}
{{% tab name="JSON" %}}

Add the following JSON objects to the `components` array:

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "lenc",
    "model": "AMS-AS5048",
    "type": "encoder",
    "namespace": "rdk",
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
    "model": "AMS-AS5048",
    "type": "encoder",
    "namespace": "rdk",
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

Follow the instructions for the [model of encoder](/components/encoder/#supported-models) your rover uses to configure your encoders and configure at least a `right` and a `left` encoder.

{{% /tab %}}
{{< /tabs >}}

### Configure the motors

{{< tabs name="motors-config">}}
{{% tab name="SCUTTLE" %}}

{{< tabs name="gpio-config">}}
{{% tab name="Config Builder" %}}

Start with the right motor:

#### Right motor

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `motor` type, then select the `gpio` model.
Enter `right` as the name or use the suggested name for your motor and click **Create**.

Then from the **Board** dropdown, select `local`, the Raspberry Pi the motor is wired to.

Select `Encoded` in the **Encoder** section and select `renc` as the **encoder** and set **ticks per rotation** to `2`.

Next, describe how the motor is wired to the Pi:

1. Switch the Component Pin Assignment Type to `In1/In2`.
2. Set **A/In1** to `16`.
3. Set **B/In2** to `15`.
4. Leave the `pwm` (pulse-width modulation) pin blank, because this specific motor driver's configuration does not require a separate PWM pin.

![The motor config panel.](/tutorials/scuttlebot/pi-wheel.png)

#### Left motor

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `motor` type, then select the `gpio` model.
Enter `left` as the name or use the suggested name for your motor and click **Create**.

Then select `local` from the **Board** dropdown to choose the Raspberry Pi the motor is wired to.

Select `Encoded` in the **Encoder** section and select `lenc` as the **encoder** and set **ticks per rotation** to `2`.

Next, describe how the motor is wired to the Pi:

1. Switch the Component Pin Assignment Type to `In1/In2`.
2. Set **A/In1** to `12`.
3. Set **B/In2** to `11`.
4. Leave the `pwm` (pulse-width modulation) pin blank, because this specific motor driver's configuration does not require a separate PWM pin.

{{% /tab %}}
{{% tab name="JSON" %}}

Add the following JSON objects to the `components` array:

```json
{
  "name": "right",
  "model": "gpio",
  "type": "motor",
  "namespace": "rdk",
  "attributes": {
    "pins": {
      "a": "16",
      "b": "15",
      "pwm": "",
      "dir": ""
    },
    "board": "local",
    "dir_flip": false,
    "ticks_per_rotation": 2
  },
  "depends_on": [ "local" ]
},
{
  "name": "left",
  "model": "gpio",
  "type": "motor",
  "namespace": "rdk",
  "attributes": {
    "pins": {
      "a": "12",
      "b": "11",
      "pwm": ""
    },
    "board": "local",
    "dir_flip": false,
    "ticks_per_rotation": 2
  },
  "depends_on": [ "local" ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Yahboom" %}}

Since both right (and left) side motors of the Yahboom rover are wired together to a single motor driver, you configure the right (and left) side motors as a single [motor component](/components/motor/).

Start with the right set of wheels.

#### Right motor

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `motor` type, then select the `gpio` model.
Enter `right` as the name or use the suggested name for your motor and click **Create**.

![G P I O motor config in the builder UI with the In1 and In2 pins configured and the PWM pin field left blank.](/components/motor/gpio-config-ui.png)

Click the **Board** dropdown and select `local` as the board the motor driver is wired to.
Next, configure the **Component Pin Assignment** section to represent how the motor is wired to the board.
In the **Component Pin Assignment** section of the right motor card, toggle the **Type** to **In1/In2** to use the compatible mode for this motor driver.

If you followed the setup instructions for putting together your Yahboom rover correctly, you can set the **pins** as follows:

- `a` to `35`
- `b` to `37`
- `pwm` (pulse-width modulation) to `33`.

Leave `dir` pin blank, because Yahboom's motor driver uses an a/b/pwm configuration.

Click **Show more** and set `max_rpm` to `300`.
You can ignore the other optional attributes.

#### Left motor

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `motor` type, then select the `gpio` model.
Enter `left` as the name or use the suggested name for your motor and click **Create**.

Click the **Board** dropdown and select `local` as the board the motor driver is wired to.
Next, configure the **Component Pin Assignment** section to represent how the motor is wired to the board.
In the **Component Pin Assignment** section of the right motor card, toggle the **Type** to **In1/In2** to use the compatible mode for this motor driver.

If you followed the setup instructions for putting together your Yahboom rover correctly, you can set the **pins** as follows:

- `a` to `38`
- `b` to `40`
- `pwm` (pulse-width modulation) to `36`.

Leave `dir` pin blank, because Yahboom's motor driver uses an a/b/pwm configuration.

Click **Show more** and set `max_rpm` to `300`.
You can ignore the other optional attributes.

{{% /tab %}}
{{% tab name="Other" %}}

Follow the instructions for the [model of motor](/components/motor/#supported-models) your rover uses to configure your motors and configure at least a `right` and a `left` motor.

{{% /tab %}}
{{< /tabs >}}

#### Test the motor configuration

{{< alert title="Caution" color="caution" >}}

Ensure the rover has sufficient space to drive around without hitting anyone or anything.

If you don't have enough space, consider holding your robot off the ground so it cannot collide with anything unexpected.

{{< /alert >}}

Now that you have configured your motors, you can actuate them.
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

If your wheel turns in reverse when it should turn forward, add the `dir_flip` attribute to the motor's configuration, by clicking **Show more** and setting the attribute to "true."

There, you should see a panel for the right motor: you can use this panel to set the motor's power level.

## (Optional) Configure the camera

Optionally, add a camera to your rover.

{{< tabs name="Configure a Webcam" >}}
{{% tab name="Config Builder" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

{{< imgproc src="/components/camera/configure-webcam.png" alt="Configuration of a webcam camera in the Viam app config builder." resize="1200x" style="width=600x" >}}

If you click on the **Video Path** field while your robot is live, a dropdown autopopulates with identified camera paths.

{{% /tab %}}
{{% tab name="JSON" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "Webcam",
  "model": "webcam",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "video_path": "<PATH_TO_YOUR_WEBCAM>"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

If your rover has its camera mounted on a pair of [servos](/components/servo/), like the Yahboom rover, you can use these to control the pan and tilt of the camera.

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `servo` type, then select the `pi` model.
Enter `pan` as the name and click **Create**.

Set `Depends On` to `local`, and `pin` to the pin the servo is wired to (`23` for the Yahboom rover).

Finally, add the tilt `servo` as well.
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `servo` type, then select the `pi` model.
Enter `tilt` as the name and click **Create**.

Set `Depends On` to `local`, and `pin` to the pin the servo is wired to (`21` for the Yahboom rover).

### Test the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Configure the base

Next, configure the [base component](/components/base/), which describes the geometry of your chassis and wheels so that the software can calculate how to steer the rover in a coordinated way.
Configuring a {{% glossary_tooltip term_id="base" text="base"%}} component also provides you with a nice UI for moving the rover around.

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="Config Builder" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `base` type, then select the `wheeled` model.
Enter a name or use the suggested name for your base and click **Create**.

{{< tabs >}}
{{% tab name="SCUTTLE" %}}

1. Select the motors attached to the base in the fields as your **right** and **left** motors.
2. Enter `250` for `wheel_circumference_mm`.
3. Enter `400` for `width_mm` (measured between the midpoints of the wheels).

{{% /tab %}}
{{% tab name="Yahboom" %}}

1. Select the motors attached to the base in the fields as your **right** and **left** motors.
2. Enter `220` for `wheel_circumference_mm`.
3. Enter `150` for `width_mm` (measured between the midpoints of the wheels).

{{% /tab %}}
{{% tab name="Other" %}}

1. Select the motors attached to the base in the fields as your **right** and **left** motors.
2. Measure the wheel circumference in mm and enter it in the field for `wheel_circumference_mm`.
3. Measure the width in mm between the midpoints of the wheels and enter it in the field for `width_mm` (measured between the midpoints of the wheels).

{{% /tab %}}
{{< /tabs >}}

{{< imgproc src="/components/base/wheeled-base-ui-config.png" alt="An example configuration for a wheeled base in the Viam app config builder, with Attributes & Depends On dropdowns and the option to add a frame." resize="1200x" style="width: 900px" >}}

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
      "type": "motor"
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
      "type": "motor"
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
      "type": "base"
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
