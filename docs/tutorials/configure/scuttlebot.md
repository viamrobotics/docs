---
title: "Configure a SCUTTLE Robot"
linkTitle: "Configure a SCUTTLE Robot"
type: "docs"
description: "Configure a SCUTTLE robot on the Viam platform."
image: "/tutorials/scuttlebot/scuttle-on-floor-cropped.png"
images: ["/tutorials/scuttlebot/scuttle-on-floor-cropped.png"]
imageAlt: "A SCUTTLE robot on a carpeted floor."
tags: ["base", "camera", "raspberry pi", "scuttle"]
aliases:
  - "/tutorials/scuttlebot"
  - "/tutorials/scuttlebot/scuttlebot"
authors: []
languages: ["python", "go"]
viamresources: ["board", "motor", "camera", "base", "encoder"]
level: "Beginner"
date: "2022-08-02"
updated: "2023-08-05"
cost: 540
---

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/LAMxYci242E">}}

## Requirements

- A Raspberry Pi with [Raspberry Pi OS 64-bit Lite installed](/get-started/installation/prepare/rpi-setup/#install-raspberry-pi-os)
- [A SCUTTLE robot](https://www.scuttlerobot.org/shop/)

## Start configuring your robot

1. Go to [the Viam app](https://app.viam.com).
1. Create a _robot_ and follow the setup instructions until the robot successfully connects to the Viam app.
1. Navigate to the robot's **Config** tab.

![A SCUTTLE robot on a carpeted floor.](/tutorials/scuttlebot/scuttle-on-floor.png)

## Configure the encoders

Configure the left and right encoders as follows:

{{< tabs name="Configure AMS-AS5048 Encoders" >}}
{{% tab name="Config Builder" %}}

### Left encoder

Click **Create component**.
Select the `encoder` type, then select the `AMS-AS5048` model.
Enter `lenc` as the name for your encoder and click **Create**.

Click the **board** dropdown list and select the name of your board, `local`.

In the **i2c bus** field type `1`, and in the **i2c address** field type `64`.

![Configuration of an AMS-AS5048 encoder in the Viam app config builder.](/tutorials/scuttlebot/create-encoder.png)

### Right encoder

Click **Create component**.
Select the `encoder` type, then select the `AMS-AS5048` model.
Enter `renc` as the name for your encoder and click **Create**.

Click the **board** dropdown list and select the name of your board, `local`.

In the **i2c bus** field type `1`, and in the **i2c address** field type `65`.

Click **Save config**.

{{% /tab %}}
{{% tab name="JSON Template" %}}

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

## Configure the motors

The next step is to add the motors and make them spin the wheels.

{{< tabs name="gpio-config">}}
{{% tab name="Config Builder" %}}

### Right motor

Click **Create component**.
Select the `motor` type, then select the `gpio` model.
Enter `right` as the name for your encoder and click **Create**.

Then from the **Board** dropdown, select `local`, the Raspberry Pi the motor is wired to.

Select `Encoded` in the **Encoder** section and select `renc` as the **encoder** and set **ticks per rotation** to `2`.

Next, describe how the motor is wired to the Pi:

1. Switch the Component Pin Assignment Type to `In1/In2`.
2. Set **A/In1** to `16`.
3. Set **B/In2** to `15`.
4. Leave the `pwm` (pulse-width modulation) pin blank, because this specific motor driver's configuration does not require a separate PWM pin.

![The motor config panel.](/tutorials/scuttlebot/pi-wheel.png)

### Left motor

Click **Create component**.
Select the `motor` type, then select the `gpio` model.
Enter `left` as the name for your encoder and click **Create**.

Then select `local` from the **Board** dropdown to choose the Raspberry Pi the motor is wired to.

Select `Encoded` in the **Encoder** section and select `lenc` as the **encoder** and set **ticks per rotation** to `2`.

Next, describe how the motor is wired to the Pi:

1. Switch the Component Pin Assignment Type to `In1/In2`.
2. Set **A/In1** to `12`.
3. Set **B/In2** to `11`.
4. Leave the `pwm` (pulse-width modulation) pin blank, because this specific motor driver's configuration does not require a separate PWM pin.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

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

Save the config by clicking **Save config** at the bottom of the page.

### Test the motor configuration

Now that you have configured your board, encoders, and motors, you can actuate your motors.
Navigate to the **Control** tab.

You'll see a panel for each configured component.

![Motor panels](/tutorials/scuttlebot/scuttle-bothmotors.png)

Click on the panel for the right `motor`.

![Power level adjustment](/tutorials/scuttlebot/pi-moverhmotor.png)

Try changing the motor's **power** level and click **Run**.

{{< alert title="Caution" color="caution" >}}
Be careful when using your motors!
Start with the power level set to 20% and increase it incrementally until the wheel rotates at a reasonable speed, clicking **Run** at each increment.
If you hear a "whining" sound from the motor, the power level is not high enough to turn the armature.
If this happens, increase the power level by 10% increments until it starts to turn.
{{< /alert >}}

If your wheel turns in reverse when it should turn forward, add the `dir_flip` attribute to the motor's configuration, by clicking **Show more** and setting the attribute to "true."

## Configure the base

Next, configure the [base component](/components/base/), which describes the geometry of your chassis and wheels so that the software can calculate how to steer the rover in a coordinated way.
Configuring a base component also provides you with a nice UI for moving the rover around.

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `wheeled` model.
Enter a name for your base and click **Create**.

{{< imgproc src="/components/base/wheeled-base-ui-config.png" alt="An example configuration for a wheeled base." resize="600x" >}}

1. Select `right` as the **Right Motor** and `left` as the **Left Motor**.
2. Enter `250` in **Wheel Circumference (mm)**.
3. Enter `400` in **Width (mm)** (measured between the midpoints of the wheels).

{{% /tab %}}
{{% tab name="Raw JSON" %}}

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

Save the config by clicking **Save config** at the bottom of the page.

### Test the base

Now that you have configured the base you can try moving the SCUTTLE robot with your keyboard.
Navigate to the **Control** tab.

Click on the panel for the `base`.

{{<imgproc src="/tutorials/scuttlebot/pi-kybrd-control.png" resize="300x" declaredimensions=true alt="WASD controls">}}

On the **Keyboard** tab, toggle the keyboard control to active.
Use **W** and **S** to go forward and back, and **A** and **D** to arc and spin.

Try driving your SCUTTLE robot around using the WASD keyboard controls.

{{% alert title="Caution" color="caution" %}}
Ensure that your robot has sufficient space to drive around without hitting anyone or anything.
{{% /alert %}}

If you navigate to the **Discrete** tab, you can use movement modes such as `Straight` and `Spin` and different movement types such as `Continuous` and `Discrete` and directions such as `Forwards` and `Backwards`.

![Discrete controls](/tutorials/scuttlebot/pi-discrete.png)

## Configure the camera

Finally, add a camera to your SCUTTLE robot.

{{< tabs name="Configure a Webcam" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `webcam` model.
Enter a name for your camera and click **Create**.

{{< imgproc src="/components/camera/configure-webcam.png" alt="Configuration of a webcam camera in the Viam app config builder." resize="600x" >}}

If you click on the **Video Path** field while your robot is live, a dropdown autopopulates with identified camera paths.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "Webcam",
  "model": "webcam",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "video_path": "video0"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

## View the camera stream

Now that you have configured the base you can try moving the SCUTTLE robot with your keyboard.
Navigate to the **Control** tab.

Click on the panel for the `camera`.
Then toggle the camera view to ON.

If everything is configured correctly, you will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

{{< imgproc src="/components/camera/example_camera_image.png" alt="Example Camera view inside Viam app" resize="700x" >}}

## Next steps

Now that you have fully configured your SCUTTLE robot, you can drive it around and view its camera stream.

To take things to the next level, check out one of the following tutorials:

{{< cards >}}
{{% card link="/tutorials/services/color-detection-scuttle" %}}
{{% card link="/tutorials/control/scuttle-gamepad/" %}}
{{% card link="/tutorials/services/webcam-line-follower-robot/" %}}
{{< /cards >}}
