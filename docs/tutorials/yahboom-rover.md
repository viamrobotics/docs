---
title: "Setting up a Yahboom 4WD Rover with a Bluetooth Gamepad on Viam"
linkTitle: "Driving a Yahboom Rover with a Gamepad"
weight: 25
type: "docs"
description: "Instructions for getting a Yahboom 4WD Rover driving with a Bluetooth Gamepad and the Viam app."
---
## Requirements

- A Raspberry Pi 4 running an instance of viam-server.
See our [Raspberry Pi Setup Guide](/getting-started/installation/) for instructions.
- A <a href="https://category.yahboom.net/collections/robotics/products/4wdrobot" target="_blank">Yahboom 4WD Smart Robot</a>[^yahboom]
- A Bluetooth gamepad controller. For this tutorial we used <a href="https://shop.8bitdo.com/products/8bitdo-pro-2-bluetooth-controller-for-switch-switch-oled-pc-macos-android-steam-raspberry-pi---nintendo-switch" target="_blank">this 8BitDo controller.</a>[^8bitdo]

[^yahboom]: Yahboom 4WD Smart Robot with AI vision features for Raspberry Pi 4B: <a href="https://category.yahboom.net/collections/robotics/products/4wdrobot" target="_blank">ht<span>tps://category.yahboom.net/collections/robotics/products/4wdrobot</a>

[^8bitdo]: 8BitDo Pro 2 Bluetooth Controller: <a href="https://shop.8bitdo.com/products/8bitdo-pro-2-bluetooth-controller-for-switch-switch-oled-pc-macos-android-steam-raspberry-pi---nintendo-switch" target="_blank">ht<span>tps://shop.8bitdo.com/products/8bitdo-pro-2-bluetooth-controller-for-switch-switch-oled-pc-macos-android-steam-raspberry-pi---nintendo-switch</a>

## Configuring the Board 

Go to the Viam app ([https://app.viam.com](https://app.viam.com)) in a web browser, and navigate to the **CONFIG** tab of the robot associated with your Raspberry Pi.
To create a new component you'll be working within the **Create Component** box of the **COMPONENTS** sub-tab.

![config](../img/config.png)

The first component you will add is the [board](/components/board/) which represents the Raspberry Pi to which the other components are wired.
For component `Type`, select `board`.
Then you can name the `board` whatever you like as long as you are consistent when referring to it later; `local` is a good name since it is the `board` you will communicate with directly.
For `Model`, select `pi`.
Click the **Create Component** button.
You don't need to add any attributes for this one, so your configured board will look something like this:

![board](../img/board.png)

## Configuring the Motor and Wheels 

Since both right side motors of the Yahboom rover are wired together to a single motor driver, the right side motors are configured as a single [motor component](/components/motor/) in the Viam config file.
Later we will configure both left side motors as another motor.

As with all other components, scroll to the **Create Component** box.
Start with the right set of wheels, and name the component `right`.
For the `Type`, select `motor`.
For the `Model`, select `gpio`.
Click **Create Component**.
Click the **Board** drop-down and select `local` since that is what this motor driver is wired to.

You will need to tell Viam how this motor is wired to the Pi.
In the **Component Pin Assignment** section of the right motor card, toggle the **Type** to **In1/In2** because that is the compatible mode for this motor driver.
If the Yahboom setup instructions are followed correctly, the following `pins` should be correct: set `a` to `35`, `b` to `37`, and `pwm` (pulse-width modulation) to `33`.
You should leave `dir` pin blank, because Yahboom's motor driver uses an a/b/pwm configuration.

Click **SHOW OPTIONAL** and set `max_rpm` to `300`.
You can ignore the other optional attributes.

At the bottom of the motor card, add `local` in the **Depends On** drop-down.
Save the config by clicking **Save Config** at the bottom of the page.

{{% alert title="Note" color="note" %}}  
If you are using a motor with encoders, you need to specify the ticks per rotation.
{{% /alert %}}

![rightmotor](../img/rightmotor.png)

Having configured these two components, you should now be able to actuate your motor.
Click **CONTROL** at the top of the page to navigate to the Control tab.
There, you should see a panel for the right motor: you can use this panel to set the motor's power level.

Please be careful when activating your robot! Start with the power level set to 10% and increase it incrementally (about 10% each time), activating the motor at each step until the wheels are rotating at a reasonable rate.
Ensure the rover has sufficient space to drive around without hitting anyone or anything.
Consider possibly holding your robot off the ground so it cannot run away or collide with anything unexpected.

![control_rightmotor](../img/control-rightmotor.png)

At this point, the wheels on one side of your robot should be working.
Now try to add the other set of wheels using the same steps and see if you can get this robot driving with all of the components working together.
To do this, we’ll have to add the other `motor` component and link them together with a `base`.

To do this, go back to the **CONFIG** tab and scroll down to the fresh **Create Component** box.
The config attributes for this `motor` will be very similar to the `right` motor, which makes sense as the hardware is the same and it is connected to the same `board`.
The only difference will be the `Name` which will be `left` and the pins it is connected to, which should be set as follows: `a` (In1) to `38`, `b` (In2) to `40`, and `pwm` to `36`.

![leftmotor](../img/leftmotor.png)

Save the config and hop over to the control view again. You should now see two motors and be able to make each set of wheels spin.

![motors](../img/motors.png)

## Configuring the Base 

Unite these wheel sets with a [base component](/components/base/), which is used to describe the physical structure onto which your components are mounted.
Configuring a base will also give you a nice UI for moving the rover around.

To configure a base, scroll down to **Create Component**.
Name the component `yahboom-base`.
For the `Type` select `base` and for the `Model` select `wheeled`.
Click **Create Component**.
For `Depends On` select `local`, `left`, and `right` since these are the components that comprise our `base`.
For `width_mm`, use `150`, which is the approximate distance between the right and left wheels.
For `wheel_circumference_mm` use `220`.
The `left` and `right` attributes are intended to be the set of motors corresponding to the left and right sides of the rover.
Since you were clever about naming your motors, you can simply add "left" to "left" and "right" to "right", so that your Attributes field contains the following:

```json
{
  "width_mm": 150,
  "wheel_circumference_mm": 220,
  "left": ["left"],
  "right": ["right"]
}
```

The whole base card will look something like this:

![base](../img/base.png)

When you save the config and switch to the control view once more, you should have new buttons for the `base` functionality including `Forward`,`Backward`, `Arc Forward`, `Spin Clockwise` and similar.
Try playing around with these and the `Speed`, `Distances`, and `Angle` fields below them to get a sense for what they do.
Something you can try is: 300mm per sec for the speed, 500mm for the distances, and 0 degree for the angle.

![baseui](../img/baseui.png)

Awesome! Now you have a rover which you can drive via a webUI.
But wouldn’t it be more fun to drive it around like an RC car? Now you can try attaching a Bluetooth controller and using that to control the rover.
If you’ve ever connected a Bluetooth device via the Linux command line, great! If not, strap in, it’s going to be a bit of a ride.
If you would like to skip adding a Bluetooth controller, jump ahead to the Configuring the Camera Component section of the tutorial.

## Connecting a Bluetooth Controller

Make sure the 8bitdo controller mode switch is set to S, hold down Start for a few seconds, and when the LED underneath the controller changes to green, press the pair button for 3 seconds.
For more information about the controller buttons and Bluetooth modes, consult the manual included with the controller.

Run `sudo bluetoothctl scan on` to list all Bluetooth devices within reach of the Raspberry Pi.
As you do this, in terminal make sure you are in your pi and not in your computer. This command will scan all the devices but the 8bitdo controller will have a MAC address that begins E4:17:D8.

![ssh-pilocal](../img/ssh-pilocal.png)

![bluetooth-scan](../img/bluetooth-scan.png)

If you see a large log of devices, to see the addresses that only begin with E4:17:D8 you can use the `grep` command line tool.
It is an acronym that stands for Global Regular Expression Print and allows to search for a string of characters in a specified file: `sudo bluetoothctl scan on | grep "E4:17:D8"`

![bluetooth-grep](../img/bluetooth-grep.png)


Once you find it in the listings, pair with the controller: `sudo bluetoothctl pair <8bitdo-mac-address>`.
Do not forget to take the < and > symbols out as you paste your address.

Then connect the controller: `sudo bluetoothctl connect <8bitdo-mac-address>`

Lastly trust the controller, which makes reconnecting easier in the future: `sudo bluetoothctl trust <8bitdo-mac-address>`

To confirm the connection, you can list connected devices with: `sudo bluetoothctl devices | cut -f2 -d</code></code>| while read uuid; do sudo bluetoothctl info $uuid; done|grep -e "Device\|Connected\|Name"`

![bluetoothpair-connect](../img/bluetoothpair-connect.png)

If you would like a stronger understanding of `bluetoothctl` and managing Bluetooth devices in Linux, we recommend [this guide](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/).

Now you can add this controller to the robot’s config.
Scroll to **Create Component**.
You can name the component `8bit-do-controller`.
For the `Type` select `input_controller` and for the `Model` select `gamepad`.
Click **Create Component**.
Lastly, you can set the `auto_reconnect` attribute to `true`.
This config adds the controller to the robot, but doesn’t give it any functionality yet.

![8bit-do](../img/8bit-do.png)

To link the controller input to the four-wheel base functionality, you need to add our first `service`.
Services are the software packages which provide our robots with cool and powerful functionality.

Scroll to the top of the page.
So far we've been working on the **COMPONENTS** sub-tab of the **CONFIG** tab, but now we'll switch to the **SERVICES** sub-tab of **CONFIG**.
You will be using the **Create Service** card here.
You can `name` this service `yahboom_gamepad_control` and give it the `type` `base_remote_control`, which is a service Viam provides for driving a rover with a gamepad.
Click **Create Service**.
You will need to configure the following attributes for this service: `base` should be `yahboom-base` and `input_controller` should be `8bit-do-controller`:

```json
{
  "base": "yahboom-base",
  "input_controller": "8bit-do-controller"
}
```

![serviceattributes](../img/serviceattributes.png)

If you can not see a section where you can add the attributes, you can go to **Raw JSON** mode, and add this code:

```json
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

Save the config and visit the **CONTROL** tab.
You should have a panel for the controller which indicates whether or not it is connected.
At this point moving the left analogue stick should result in movement of the rover!

## Configuring the Camera Component 

But wait!
This rover has a camera on it.

Once again, scroll to **Create Component** at the bottom of the **CONFIG** tab.
Follow [these instructions on how to connect and configure a camera](/tutorials/how-to-configure-a-camera/#connect-and-configure-a-webcam).
Don't worry about calibrating the camera; it is not necessary for this tutorial.
That should be enough to get the `camera` streaming to the webUI.

![rover-camera](../img/rover-camera.png)

If you click on your webUI, you will be able to see your camera streaming.

![camerastream](../img/camerastream.png)

## Configuring the Servo Components

You may have noticed that the camera is mounted on a pair of [servos](/components/servo/) which control the pan and tilt of the camera.
Scroll to **Create Component**.
Set the `Name` to `pan`, the `Type` to `servo`, the `Model` to `pi`, and click **Create Component**. Set `Depends On` to `local`, and `pin` to `23`, which is the pin the servo is wired to.

![panservo](../img/panservo.png)

Finally, add the tilt `servo` as well.
This will be the same process as the first `servo`, but with the `Name` set to `tilt` and the `pin` to `21`.

![tiltservo](../img/tiltservo.png)

Saving the config and moving to the control UI, you should notice two new panels for adjusting these servos.

![servos](../img/servos.png)

Congratulations, you have successfully configured your rover with Viam!
But for now, all the control is manual.
You can use the [Python SDK](https://python.viam.dev) to write your own code to control it, or check out one of our other [tutorials](/tutorials/)!