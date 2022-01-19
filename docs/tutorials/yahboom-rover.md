---
title: Setting up Yahboom 4WD Rover on VIAM
summary: Instructions for getting a Yahboom 4WD Rover driving with a Bluetooth Gamepad with viam.
authors:
    - Matt Dannenberg
date: 2022-01-19
---
# Configuring a Four Wheeled Rover Controlled by Gamepad
Robot configs at viam are JSON files. These configs have two top-level fields; `“components”`, which will contain descriptions of the physical hardware of your robot and `“services”`, which will contain the software libraries of your robot. Let’s start with an empty robot config:
```json
{
  "components": [],
  "services": []
}
```

The first component we will add will be our `board`, since all other components hang off of it in this case. The config for the `board` looks like:
```json
{
  "model": "pi",
  "name": "local",
  "type": "board"
}
```
You can name the `board` whatever you like so long as you are consistent about it throughout the config.

Next we’ll add one of the `motor` controllers and see if we can make the wheel spin. If you wired up the yahboom rover correctly, the following config should match your right side wheels:
```json
{
  "name": "right",
  "type": "motor",
  "model": "pi",
  "attributes": {
    "board": "local",
    "max_rpm": 300,
    "pins": {
      "a": "35",
      "b": "37",
      "pwm": "33"
    }
  },
  "depends_on": [
    "local"
  ]
}
```
You could rename this `motor`, say if the left and right sides of your rover are reversed. But again being consistent with the name throughout the config is essential. Most components have an attribute object which describes the attributes of that component (eg, the pins a component is connected to). Most components will have a `depends_on` array which contains the names of the other components which they are a part of. Here this is simply the `board` the `motor` is connected to.

Having entered these two components, you should save the config and try clicking through to the control page for your robot on app.viam. There you should see a panel for the right `motor`, which you can use to set its rotation speed. Please be careful when activating your robot! Ensure it has sufficient space to drive around without hitting anyone or anything. Consider possibly holding your robot off the ground so it cannot run away or collide with anything unexpected.

At this point, the wheels on one side of your robot should be working through app.viam. Very cool! Now let’s try to add the other set of wheels and see if we can get this bot driving in a coordinated manner. To do this, we’ll have to add the other `motor` controller and link them together with a `base`. First the other motor config:
```json
{
  "name": "left",
  "type": "motor",
  "model": "pi",
  "attributes": {
    "board": "local",
    "max_rpm": 300,
    "pins": {
      "a": "38",
      "b": "40",
      "pwm": "36"
    }
  },
  "depends_on": [
    "local"
  ]
}
```
As you can see, this is very similar to the first one, which makes sense as the hardware is the same and it is connected to the same `board`. The differences are its name and the pins to which it is connected. If you save the config and hop over to the control view again, you should now see two motors and be able to make both sets of wheels spin.

Now let’s add the base:
```json
{
  "name": "yahboom-base",
  "type": "base",
  "model": "four-wheel",
  "attributes": {
    "backLeft": "left",
    "backRight": "right",
    "board": "local",
    "frontLeft": "left",
    "frontRight": "right",
    "wheelCircumferenceMillis": 160,
    "widthMillis": 20
  },
  "depends_on": [
    "local",
    "left",
    "right"
  ]
}
```
The `base` component is used to describe the physical structure onto which components are mounted. The `four-wheel` model of the `base` component expects attributes to describe which components are each of its wheels. Since the yahboom rover only has two driving `motor` controllers (one for each side instead of one for each wheel), we list each `motor` twice (once as front and once as back). When you save the config and switch to the control view once more, you should have new buttons for the `base` functionality including `BaseSpin`, `BaseArcMove`, and similar. Try playing around with these and getting a sense for what they do.

Awesome! Now we have a rover which we can drive via a webUI. But wouldn’t it be more fun to drive it around like an RC car? Let’s try attaching a bluetooth controller and using that to control the rover. If you’ve ever connected a bluetooth device via the linux command line, great! If not, strap in, it’s a bit of a pain. We recommend [this guide](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/).

 Now let’s add that controller to the robot’s config: 
```json
{
  "name": "8bit-do-controller",
  "type": "input_controller",
  "model": "gamepad",
  "attributes": {
    "auto_reconnect": true
  }
}
```
This config adds the controller to the robot, but doesn’t wire it up to any functionality. To link the controller input to the four-wheel base functionality, we need to add our first `service`. Services are the software packages which provide our robots with cool and powerful functionality. Here’s the config for the base_remote_control package, which will map the left analoglue stick to movement of our four-wheeled base:
```json
{
  "name": "base_remote_control",
  "type": "base_remote_control",
  "attributes": {
    "base": "yahboom-base",
    "input_controller": "8bit-do-controller"
  }
}
```
Save the config and visit the control UI. At this point moving the left analogue stick should result in movement of the rover!

