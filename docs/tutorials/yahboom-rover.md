---
title: Setting up Yahboom 4WD Rover on VIAM
summary: Instructions for getting a Yahboom 4WD Rover driving with a Bluetooth Gamepad with viam.
authors:
    - Matt Dannenberg
date: 2022-01-19
---
# Configuring a Four Wheeled Rover Controlled by Gamepad
TODO: introduce the config concept, attributes, and depends_on

The first component we will add is our `board`, which represents our Single Board Computer, the Raspberry Pi into which we are wiring all other components. To create a new component, simply click `NEW COMPONENT`.
We'll name this component `local` since it is the `board` we will communicate with directly. You can name the `board` whatever you like. For component `Type`, select `board` and for `Model`, select `pi`.


TODO: fix dir and tickets per rotation
Next we’ll add one of the `motor` controllers and see if we can make the wheel spin. As with all other components, the first step is to click `NEW COMPONENT`.
We'll start with the right wheels, so let's name the component `right`. For the `Type` select `motor`, for the `Model` select `pi`, and for `Depends On` select `local` since that is what this motor is wired to.
We'll need to tell Viam how this motor is wired up to the Pi. If the yahboom setup instructions were followed correctly, the following `pins` should be correct: set `a` to `35`, `b` to `37`, and `pwm` to `33`.
`dir`???
For the `board` we again put `local`, `ticksPerRotation` should be ``, and `max_rpm` should be `300`.

Having entered these two components, you should now be able to actuate your motor. Save the config by clicking `SAVE CONFIG` at the bottom of the page and click `CONTROL` at the top of the page to navigate to the Control Page.
There you should see a panel for the right `motor`. You can use this panel to set the motor's `power` level. Please be careful when activating your robot! Start with the power level set to 10% and incrementally increase it (about 10% each time), activating the motor at each step until the wheels are rotating at a reasonable rate. 
Ensure the rover has sufficient space to drive around without hitting anyone or anything. Consider possibly holding your robot off the ground so it cannot run away or collide with anything unexpected.

At this point, the wheels on one side of your robot should be working through app.viam. Very cool! Now let’s try to add the other set of wheels and see if we can get this bot driving in a coordinated manner. To do this, we’ll have to add the other `motor` controller and link them together with a `base`.

We'll once again click `NEW COMPONENT`. The config attributes for this `motor` will be very similar to the `right` motor, which makes sense as the hardware is the same and it is connected to the same `board`. The only difference will be the `Name` which will be `left` and the pins it's connected to, which should be set as follows: `a` to `38`, `b` to `40`, and `pwm` to `36`.
If you save the config and hop over to the control view again, you should now see two motors and be able to make each set of wheels spin.

TODO: confirm the base measurements and if board is needed as a depends_on
Now let’s unite these wheel sets with a `base` component, which is used to describe the physical structure onto which our components are mounted. I configuring a `base` component will give us a nice API for moving the rover around.

As you're likely accustomed to at this point, we'll start by clicking `NEW COMPONENT`. 
Let's name the component `yahboom-base`. For the `Type` select `base`, for the `Model` select `wheeled`, and for `Depends On` select `local`, `left`, and `right` since these are the components that comprise our `base`.
For `width_mm` we'll use `20` and for `wheel_circumference_mm` we'll use `160`. The `left` and `right` attributes are intended to be the set of motors corresponding to the left and right sides of the rover. Since we were clever about naming our motors, we can simply add one item to each of `left` and `right` which will be our motors `left` and `right`, respectively.

When you save the config and switch to the control view once more, you should have new buttons for the `base` functionality including `Forward`, `Forward Arc`, `Spin Clockwise` and similar. Try playing around with these and the `Distance` and `Angle` fields below them to get a sense for what they do.

Awesome! Now we have a rover which we can drive via a webUI. But wouldn’t it be more fun to drive it around like an RC car? Let’s try attaching a bluetooth controller and using that to control the rover. If you’ve ever connected a bluetooth device via the linux command line, great! If not, strap in, it’s a bit of a pain. 

Make sure the 8bitdo controller mode switch is set to S, hold down Start for a few seconds, and when the LED rotates press the pair button for 3 seconds. For more information about the controller buttons and bluetooth modes, consult the manual included with the controller.

Run `sudo bluetoothctl scan on` to list all Bluetooth devices within reach of the Raspberry Pi. The 8bitdo controller will have a MAC address that begins E4:17:D8.

Once you find it in the listings, pair with the controller: `sudo bluetoothctl pair <8bitdo-mac-address>`

Then connect the controller: `sudo bluetoothctl connect <8bitdo-mac-address>`

Lastly trust the controller, which make reconnecting easier in the future: `sudo bluetoothctl trust <8bitdo-mac-address>`

To confirm the connection, you can list connected devices with: `sudo bluetoothctl devices | cut -f2 -d' ' | while read uuid; do sudo bluetoothctl info $uuid; done|grep -e "Device\|Connected\|Name"`

If you'd a stronger understanding of `bluetoothctl` and managing bluetooth devices in linux, we recommend [this guide](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/)

TODO: figure out how to add attributes in this jank UI
Now let’s add this controller to the robot’s config. Click on our old friend `NEW COMPONENT`.
Let's name the component `8bit-do-controller`. For the `Type` select `input_controller` and for the `Model` select `gamepad`. Lastly, let's set the `auto_reconnect` attribute to `true`. This config adds the controller to the robot, but doesn’t wire it up to any functionality.
To link the controller input to the four-wheel base functionality, we need to add our first `service`. Services are the software packages which provide our robots with cool and powerful functionality.

TODO: figure out how to add attributes in this jank UI
This time around we'll have to click `ADD ITEM` under `services` farther down on the page. We'll `name` this service `yahboom_gamepad_control` and give it the `type` `base_remote_control`, which is a service we've provide for driving a rover with a gamepad.
We'll need to configure the following attributes for this services as follows: `base` should be `yahboom-base` and `inpute_controller` should be `8bit-do-controller`.

Save the config and visit the control UI. You should have a panel for the controller which indicates whether or not it is connected. At this point moving the left analogue stick should result in movement of the rover!

TODO: figure out how to add attributes in this jank UI
But wait! This rover has a `camera` on it. Let's see if we can get that going as well! Once again, click `NEW COMPONENT`.
Let's name this camera `rover_cam`. For the `Type` select `camera` and for `Model` select `webcam`. Lastly, we'll set the `path` attribute to the linux path where the device is mounted, which should be `/dev/video0`.
That should be enough to get the `camera` streaming to the webUI.

You may have noticed that the `camera` is mounted on a pair of `servo`s which control the pan and tilt of the `camera`.
Again, we'll click `NEW COMPONENT`. We'll set the `Name` to `pan`, the `Type` to `servo`, the `Model` to `pi`, `Depends On` to `local`, and `pin` to `23`, which is the pin the servo is wired to.
Let's add the tilt `servo` as well. Same process as the first `servo`, but with the `Name` set to `tilt` and the `pin` to `21`.
Saving the config and moving to the control UI, you should notice two new panels for adjusting these servos.

Wow! This is cool! But all the control is manual. It'd sure be nice to have the robot move in an automated manner. To learn more about that, check out our [python SDK tutorial](python-sdk-yahboom.md).
