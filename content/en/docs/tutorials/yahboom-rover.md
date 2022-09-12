---
title: "Setting up a Yahboom 4WD Rover on Viam"
linkTitle: "Setting up a Yahboom 4WD Rover on Viam"
weight: 50
type: "docs"
description: "Instructions for getting a Yahboom 4WD Rover driving with a Bluetooth Gamepad and the Viam App."
---
# Configuring a Four Wheeled Rover Controlled by Gamepad
TODO: introduce the config concept, attributes, and depends_on.

#### Configuring the Board 

Go to the Viam App ([https://app.viam.com](https://app.viam.com)) in a web browser, and navigate to the robot's config.

![config](../img/config.png)

The first component you will add is the `board` which represents the Single Board Computer, the Raspberry Pi,  into which you are wiring all other components.
To create a new component, select `NEW COMPONENT`.
For component `Type`, select `board`.
Then you can name the `board` whatever you like as long as you are consistent when referring to it later; name this component `local` since it is the `board` you will communicate with directly.
For `Model`, select `pi`:

![board](../img/board.png)

#### Configuring the Motor and Wheels 

Next, add one of the `motor` controllers and see if you can make the wheel spin.
As with all other components, the first step is to select `NEW COMPONENT`.
Start with the right set of wheels, and name the component `right`.
For the `Type` select `motor`, for the `Model` select `pi`, and for `Depends On` select `local` since that is what this motor is wired to.

You will need to tell Viam how this motor is wired to the Pi.
If the Yahboom setup instructions are followed correctly, the following `pins` should be correct: set `a` to `35`, `b` to `37`, and `pwm` (pulse-width modulation) to `33`.
You should leave `dir` pin blank, because Yahboom's motor driver uses an a/b/pwm configuration.
For the `board` again put `local`, and `max_rpm` should be `300`.
You should leave `ticks_per_rotation` at zero.
Note: if you are using a motor with encoders, you need to specify the ticks per rotation.

![rightmotor](../img/rightmotor.png)

Having entered these two components, you should now be able to actuate your motor.
Save the config by clicking `SAVE CONFIG` at the bottom of the page.
Click `CONTROL` at the top of the page to navigate to the Control Page.
There, you should see a panel for the right `motor`: you can use this panel to set the motor's `power` level.

Please be careful when activating your robot! Start with the power level set to 10% and increase it incrementally (about 10% each time), activating the motor at each step until the wheels are rotating at a reasonable rate.
Ensure the rover has sufficient space to drive around without hitting anyone or anything.
Consider possibly holding your robot off the ground so it cannot run away or collide with anything unexpected.

![control_rightmotor](../img/control-rightmotor.png)

At this point, the wheels on one side of your robot should be working through the Viam App ([https://app.viam.com](https://app.viam.com)).
Now try to add the other set of wheels using the same sets and see if you can get this bot driving with all of the components working together.
To do this, we’ll have to add the other `motor` controller and link them together with a `base`.

To do this, begin by selecting `NEW COMPONENT`.
The config attributes for this `motor` will be very similar to the `right` motor, which makes sense as the hardware is the same and it is connected to the same `board`.
The only difference will be the `Name` which will be `left` and the pins it is connected to, which should be set as follows: `a` to `38`, `b` to `40`, and `pwm` to `36`.

![leftmotor](../img/leftmotor.png)

Save the config and hop over to the control view again, you should now see two motors and be able to make each set of wheels spin.

![motors](../img/motors.png)

#### Configuring the Base 

Unite these wheel sets with a `base` component, which is used to describe the physical structure onto which your components are mounted.
Configuring a `base` component will also give you a nice UI for moving the rover around.

To configure a base, select `NEW COMPONENT`.
Name the component `yahboom-base`.
For the `Type` select `base`, for the `Model` select `wheeled`, and for `Depends On` select `local`, `left`, and `right` since these are the components that comprise our `base`.
For `width_mm`, use `150` (the board is 230mm in height, 180mm in the longest side of the width, and 120mm in the shortest side of the width since the shape of the base is irregular,  with an average width of 150mm).
For `wheel_circumference_mm` use `220`.
The `left` and `right` attributes are intended to be the set of motors corresponding to the left and right sides of the rover.
Since you were clever about naming our motors, you can simply add one item to each of `left` and `right` which will be your motors `left` and `right`, respectively.

![base](../img/base.png)

When you save the config and switch to the control view once more, you should have new buttons for the `base` functionality including `Forward`,`Backward`, `Arc Forward`, `Spin Clockwise` and similar.
Try playing around with these and the `Speed`, `Distances`, and `Angle` fields below them to get a sense for what they do.
Something you can try is: 300mm per sec for the speed, 500mm for the distances, and 0 degree for the angle.

![baseui](../img/baseui.png)

Awesome! Now you have a rover which you can drive via a webUI.
But wouldn’t it be more fun to drive it around like an RC car? Now you can try attaching a Bluetooth controller and using that to control the rover.
If you’ve ever connected a Bluetooth device via the linux command line, great! If not, strap in, it’s going to be a bit of a ride.
If you would like to skip adding a Bluetooth controller, jump ahead to the Configuring the Camera Component section of the tutorial.

#### Connecting a Bluetooth Controller

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

If you would like a stronger understanding of `bluetoothctl` and managing Bluetooth devices in linux, we recommend [this guide](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/).

Now you can add this controller to the robot’s config.
Click on `NEW COMPONENT`.
You can name the component `8bit-do-controller`.
For the `Type` select `input_controller` and for the `Model` select `gamepad`.
Lastly, you can set the `auto_reconnect` attribute to `true`.
This config adds the controller to the robot, but doesn’t wire it up to any functionality.

![8bit-do](../img/8bit-do.png)

To link the controller input to the four-wheel base functionality, you need to add our first `service`.
Services are the software packages which provide our robots with cool and powerful functionality.

This time around you will have to click `ADD ITEM` under `services` on the top of the page.
You can `name` this service `yahboom_gamepad_control` and give it the `type` `base_remote_control`, which is a service Viam provides for driving a rover with a gamepad.
You will need to configure the following attributes for this services as follows: `base` should be `yahboom-base` and `input_controller` should be `8bit-do-controller`.

![serviceattributes](../img/serviceattributes.png)

If you can not see a section where you can add the attributes, you can go to your raw json mode, and add this code: 

![serviceattributesjson](../img/serviceattributesjson.png)

Save the config and visit the control UI.
You should have a panel for the controller which indicates whether or not it is connected.
At this point moving the left analogue stick should result in movement of the rover!

#### Configuring the Camera Component 

But wait! This rover has a `camera` on it.
Once again, click `NEW COMPONENT`.
You can name this camera `rover_cam`.
For the `Type` select `camera` and for `Model` select `webcam`.
Lastly, you should set the `path` attribute to the linux path where the device is mounted, which should be `/dev/video0`.
If you can not see the attributes, you can click object properties and select path, and then add the path.
That should be enough to get the `camera` streaming to the webUI.

![rover-camera](../img/rover-camera.png)

If you click on your webUI, you will be able to see your camera streaming.

![camerastream](../img/camerastream.png)

You may have noticed that the `camera` is mounted on a pair of `servo`s which control the pan and tilt of the `camera`.
Again, you should click `NEW COMPONENT`.
Set the `Name` to `pan`, the `Type` to `servo`, the `Model` to `pi`, `Depends On` to `local`, and `pin` to `23`, which is the pin the servo is wired to.

![panservo](../img/panservo.png)

Finally, add the tilt `servo` as well.
This will be the same process as the first `servo`, but with the `Name` set to `tilt` and the `pin` to `21`.

![tiltservo](../img/tiltservo.png)

Saving the config and moving to the control UI, you should notice two new panels for adjusting these servos.

![servos](../img/servos.png)

Congratulations, you have successfully configured your rover to Viam! But for now, all the control is manual.
Now that you've completed the Yahboom rover tutorial, try one of our other [tutorials](../tutorials)! 