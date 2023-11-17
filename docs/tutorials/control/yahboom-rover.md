---
title: "Drive a Yahboom Rover with a Gamepad"
linkTitle: "Drive a Yahboom Rover with a Gamepad"
type: "docs"
description: "Drive a Yahboom 4WD Rover with a bluetooth gamepad from the Viam app."
image: "/tutorials/yahboom-rover/bluetoothpair-connect.png"
imageAlt: "A Pi terminal showing the bluetoothctl commands and their outputs."
images: ["/tutorials/yahboom-rover/bluetoothpair-connect.png"]
aliases:
  - /tutorials/yahboom-rover/
tags: ["base", "gamepad", "yahboom", "app", "rover"]
authors: ["Hazal Mestci"]
languages: []
viamresources: ["base", "input_controller", "motor", "base_remote_control"]
level: "Intermediate"
date: "2022-08-10"
# updated: ""
cost: 260
---

## Requirements

- A Raspberry Pi 4 running an instance of `viam-server`.
  See our [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/) for instructions.
- A [Yahboom 4WD Smart Robot](https://category.yahboom.net/collections/robotics/products/4wdrobot)
- A Bluetooth gamepad controller. For this tutorial we used an 8BitDo controller.

## Configuring the Board

Go to the Viam app ([app.viam.com](https://app.viam.com)) in a web browser, and navigate to the **Config** tab of the robot associated with your Raspberry Pi.
To create a new component you'll be working within the **Create Component** section of the **Components** subtab.

![A screenshot of the config builder UI on app.viam.com showing the Create Component box filled out with name=local, type=board and model=pi.](/tutorials/yahboom-rover/config.png)

The first component you will add is the [board](/components/board/) which represents the Raspberry Pi to which the other components are wired.
For component `Type`, select `board`.
Then you can name the `board` whatever you like as long as you are consistent when referring to it later; `local` is a good name since it is the `board` you will communicate with directly.
For `Model`, select `pi`.
Click the **Create Component** button.
You don't need to add any attributes for this one, so your configured board will look something like this:

![A screenshot of the board's configuration card on app.viam.com.](/tutorials/yahboom-rover/board.png)

## Configuring the Motors and Wheels

Since both right side motors of the Yahboom rover are wired together to a single motor driver, the right side motors are configured as a single [motor component](/components/motor/) in the Viam config file.
Later we will configure both left side motors as another motor.

As with all other components, find the **Create Component** box at the bottom of the **Config** tab.
Start with the right set of wheels, and name the component `right`.
For the `Type`, select `motor`.
For the `Model`, select `gpio`.
Click **Create Component**.
Click the **Board** dropdown and select `local` since that is what this motor driver is wired to.

You will need to tell Viam how this motor is wired to the Pi.
In the **Component Pin Assignment** section of the right motor card, toggle the **Type** to **In1/In2** because that is the compatible mode for this motor driver.
If the Yahboom setup instructions are followed correctly, the following `pins` should be correct: set `a` to `35`, `b` to `37`, and `pwm` (pulse-width modulation) to `33`.
You should leave `dir` pin blank, because Yahboom's motor driver uses an a/b/pwm configuration.

Click **Show more** and set `max_rpm` to `300`.
You can ignore the other optional attributes.

Save the config by clicking **Save Config** at the bottom of the page.

{{% alert title="Important" color="note" %}}
If you are using a motor with encoders, you need to specify the ticks per rotation.
{{% /alert %}}

![A screenshot of the right motor configuration showing pin assignment and Max RPM set to 300.](/tutorials/yahboom-rover/rightmotor.png)

Having configured these two components, you should now be able to actuate your motor.
Click **Control** at the top of the page to navigate to the Control tab.
There, you should see a panel for the right motor: you can use this panel to set the motor's power level.

Please be careful when activating your robot! Start with the power level set to 10% and increase it incrementally (about 10% each time), activating the motor at each step until the wheels are rotating at a reasonable rate.
Ensure the rover has sufficient space to drive around without hitting anyone or anything.
Consider possibly holding your robot off the ground so it cannot run away or collide with anything unexpected.

![A screenshot of the CONTROL tab UI with buttons to control the right motor.](/tutorials/yahboom-rover/control-rightmotor.png)

At this point, the wheels on one side of your robot should be working.
Now try to add the other set of wheels using the same steps and see if you can get this robot driving with all of the components working together.
To do this, we’ll have to add the other `motor` component and link them together with a `base`.

To do this, go back to the **Config** tab and find the **Create Component** box.
The config attributes for this `motor` will be very similar to the `right` motor, which makes sense as the hardware is the same and it is connected to the same `board`.
The only difference will be the `Name` which will be `left` and the pins it is connected to, which should be set as follows: `a` (In1) to `38`, `b` (In2) to `40`, and `pwm` to `36`.

![A screenshot of the left motor configuration showing pin assignment and Max RPM set to 300.](/tutorials/yahboom-rover/leftmotor.png)

Save the config and hop over to the control view again.
You should now see two motors and be able to make each set of wheels spin.

![A screenshot of the CONTROL tab UI with buttons to control both sets of motors.](/tutorials/yahboom-rover/motors.png)

## Configuring the Base

Unite these wheel sets with a [base component](/components/base/), which is used to describe the physical structure onto which your components are mounted.
Configuring a {{% glossary_tooltip term_id="base" text="base"%}} will also give you a nice UI for moving the rover around.

In the **Create Component** box, name the component `yahboom-base`.
For the `Type` select `base` and for the `Model` select `wheeled`.
Click **Create Component**.
For **Right Motors** select `right` (the name we cleverly gave to the motor on the right side).
For **Left Motors** select `left`.
For `width_mm`, use `150`, which is the approximate distance between the right and left wheels.
For `wheel_circumference_mm` use `220`.

If you click **Go to Advanced** you can see that the Attributes field now contains the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "width_mm": 150,
  "wheel_circumference_mm": 220,
  "left": ["left"],
  "right": ["right"]
}
```

The whole base card will look something like this:

![A screenshot of the Yahboom base configuration on the Viam app.](/tutorials/yahboom-rover/base.png)

When you save the config and switch to the control view once more, you should have new buttons for the `base` functionality.
On the **Keyboard** tab of the base control card you can enable keyboard control to drive the rover with the WASD keys.
Also check out the **Discrete** tab of the base control area for a different type of control.
Try playing around with these and get a sense of how the base moves.

![A screenshot of the CONTROL tab UI with buttons to make the base move.](/tutorials/yahboom-rover/baseui.png)

Awesome! Now you have a rover which you can drive using a webUI.
But wouldn’t it be more fun to drive it around like an RC car? Now you can try attaching a Bluetooth controller and using that to control the rover.
If you’ve ever connected a Bluetooth device using the Linux command line, great! If not, strap in, it’s going to be a bit of a ride.
If you would like to skip adding a Bluetooth controller, [jump ahead to the Configuring the Camera Component section](#configuring-the-camera-component) of the tutorial.

## Connecting a Bluetooth Controller

Make sure the 8bitdo controller mode switch is set to S, hold down Start for a few seconds, and when the LED underneath the controller changes to green, press the pair button for 3 seconds.
For more information about the controller buttons and Bluetooth modes, consult the manual included with the controller.

Run `sudo bluetoothctl scan on` to list all Bluetooth devices within reach of the Raspberry Pi.
As you do this, in terminal make sure you are in your Pi and not in your computer.
This command will scan all the devices but the 8bitdo controller will have a MAC address that begins E4:17:D8.

![A screenshot of a Mac command prompt with the command ssh hazal_pi@hazal_pi.local.](/tutorials/yahboom-rover/ssh-pilocal.png)

![A screenshot of a Raspberry Pi terminal with the following command: sudo bluetoothctl scan on. The results of the command are displayed: a list of device MAC addresses.](/tutorials/yahboom-rover/bluetooth-scan.png)

If you see a large log of devices, to see the addresses that only begin with E4:17:D8 you can use the `grep` command line tool.
It is an acronym that stands for Global Regular Expression Print and allows to search for a string of characters in a specified file: `sudo bluetoothctl scan on | grep "E4:17:D8"`

![A screenshot of a Rasperry Pi terminal with the 'sudo bluetoothctl scan on | grep "E4:17:D8"' command at the top, followed by a list of device MAC addresses all beginning in "E4:17:D8".](/tutorials/yahboom-rover/bluetooth-grep.png)

Once you find it in the listings, pair with the controller: `sudo bluetoothctl pair <8bitdo-mac-address>`.
Do not forget to take the < and > symbols out as you paste your address.

Then connect the controller: `sudo bluetoothctl connect <8bitdo-mac-address>`

Lastly trust the controller, which makes reconnecting easier in the future: `sudo bluetoothctl trust <8bitdo-mac-address>`

To confirm the connection, you can list connected devices with: `sudo bluetoothctl devices | cut -f2 -d| while read uuid; do sudo bluetoothctl info $uuid; done|grep -e "Device\|Connected\|Name"`

![A screenshot of a Pi terminal showing the above bluetoothctl commands and their outputs.](/tutorials/yahboom-rover/bluetoothpair-connect.png)

If you would like a stronger understanding of `bluetoothctl` and managing Bluetooth devices in Linux, we recommend [this guide](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/).

Now you can add this controller to the robot’s config.
In the next **Create Component** field, name the component `8bit-do-controller`.
For the `Type` select `input_controller` and for the `Model` select `gamepad`.
Click **Create Component**.
Lastly, you can set the `auto_reconnect` attribute to `true`.
This config adds the controller to the robot, but doesn’t give it any functionality yet.

![A screenshot of the 8BitDo controller configuration in the Viam app. Other than the name, type and model, it contains only the attribute auto_reconnect = true.](/tutorials/yahboom-rover/8bit-do.png)

To link the controller input to the four-wheel base functionality, you need to add our first `service`.
Services are the software packages which provide our robots with cool and powerful functionality.

Until this point we've been working on the **Components** subtab of the **Config** tab, but now we'll switch to the **Services** subtab.
Click **Services** at the top of the **Config** tab.
You will be using the **Create Service** card here.
You can `name` this service `yahboom_gamepad_control` and give it the `type` `base_remote_control`, which is a service Viam provides for driving a rover with a gamepad.
Click **Create Service**.
You will need to configure the following attributes for this service: `base` should be `yahboom-base` and `input_controller` should be `8bit-do-controller`:

```json {class="line-numbers linkable-line-numbers"}
{
  "base": "yahboom-base",
  "input_controller": "8bit-do-controller"
}
```

![A screenshot of the SERVICES subtab of the CONFIG tab on app.viam.com, showing the configured base remote control service.](/tutorials/yahboom-rover/serviceattributes.png)

If you can not see a section where you can add the attributes, you can go to **Raw JSON** mode, and add this code:

```json {class="line-numbers linkable-line-numbers"}
  "services": [
    {
      "name": "yahboom-gamepad-control",
      "type": "base_remote_control",
      "attributes": {
        "base": "yahboom-base",
        "input_controller": "8bit-do-controller"
      }
    }
  ]
```

Save the config and visit the **Control** tab.
You should have a panel for the controller which indicates whether or not it is connected.
At this point moving the left analogue stick should result in movement of the rover!

## Configuring the Camera Component

But wait!
This rover has a camera on it.

Once again, find the **Create Component** section at the bottom of the **Config** tab.
Follow [these instructions on how to connect and configure a camera](/components/camera/webcam/).
Don't worry about calibrating the camera; it is not necessary for this tutorial.
That should be enough to get the `camera` streaming to the webUI.

![A screenshot of the camera configuration with video_path set to "video0".](/tutorials/yahboom-rover/rover-camera.png)

If you click on your webUI, you will be able to see your camera streaming.

![A screenshot of the camera output in the CONTROL tab. The camera feed displays the view out the window of one building, consisting of an apartment building wall across the street.](/tutorials/yahboom-rover/camerastream.png)

## Configuring the Servo Components

You may have noticed that the camera is mounted on a pair of [servos](/components/servo/) which control the pan and tilt of the camera.
Go to the **Create Component** section at the bottom of **Config**.
Set the `Name` to `pan`, the `Type` to `servo`, the `Model` to `pi`, and click **Create Component**. Set `Depends On` to `local`, and `pin` to `23`, which is the pin the servo is wired to.

![A screenshot fron the CONFIG tab of the pan servo configuration showing pin set to 23.](/tutorials/yahboom-rover/panservo.png)

Finally, add the tilt `servo` as well.
This will be the same process as the first `servo`, but with the `Name` set to `tilt` and the `pin` to `21`.

![A screenshot of the tilt servo configuration showing pin set to 21.](/tutorials/yahboom-rover/tiltservo.png)

Saving the config and moving to the control UI, you should notice two new panels for adjusting these servos.

![A screenshot of the servo control card on the CONTROL tab. There are buttons to change the angles of the pan and tilt servos, independently.](/tutorials/yahboom-rover/servos.png)

Congratulations, you have successfully configured your rover with Viam!
But for now, all the control is manual.
You can use the [Python SDK](https://python.viam.dev) to write your own code to control it, or check out one of our other [tutorials](../../)!
