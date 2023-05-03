---
title: "Single Component Tutorial: How to Create a Mouse Mover Using a Servo"
linkTitle: "Create a Mouse Mover"
weight: 40
type: "docs"
description: "Use the Python SDK to move a continuous servo to keep a computer screen from sleeping."
webmSrc: "/tutorials/img/single-component-tutorials-servo-mousemover/pi-hole.webm"
mp4Src: "/tutorials/img/single-component-tutorials-servo-mousemover/pi-hole.mp4"
videoAlt: "A mouse mover controlled with a servo and Raspberry Pi."
images: ["/tutorials/img/single-component-tutorials-servo-mousemover/pi-hole.gif"]
tags: ["servo", "single component tutorial", "raspberry pi", "sdk", "python"]
# SME: Kacey Meier-Smith
---

Have you ever been working from home and needed to step out for a moment?
Maybe it was to clear your head, grab your lunch, answer the door, and you get in trouble because it showed you as offline?

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/sXWJE0ePHdA">}}

This tutorial will show you how to build a mouse mover using Viam, a Raspberry Pi, a servo, and an optical mouse.
This robot will turn the continuous servo that's secured inside the box, which will turn the circle under the optical mouse. This will keep your computer from falling asleep.

This project is a good place to begin if you're new to robotics and would like to learn how to use a [servo component](/components/servo/) with the Viam app and Viam's [Python SDK](https://python.viam.dev/).

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/moving.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/moving.mp4" alt="Video of a mouse running erratically on the screen in a sweeping motion in front of the Viam app Control page with an overlaid video of a mouse on top of a cardboard box with a moving cardboard circle underneath it with red swirl lines on the circle.">}}
</div>

## Requirements

### Hardware

- [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with viam-server installed per our [installation guide](/installation/)
- microSD card reader
- [Continuous rotation servo](https://a.co/d/2w0u6rK) (we used the FS90R servo)
- Wheel or arm for the servo (this comes in some of the FS90R packages)
- [Jumper wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY)
- Optical mouse - corded or uncorded

### Tools and Consumables

- Suitable sized box (box should allow servo with wheel/arm with circle cut out on top of wheel/arm to sit flush with the top of the box)
- Double sided tape
- Tape to seal the box (we used black gaffers tape)
- Box cutters
- Marker

### Software

- [Python3](https://www.python.org/download/releases/3.0/)
- [Pip](https://pip.pypa.io/en/stable/#)
- [viam-server](https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b)
- [Viam Python SDK](https://python.viam.dev/)
- [Mousemover tutorial code](https://github.com/viam-labs/tutorial-mousemover)

## Install Viam software

First, install viam-server according to our [installation guide](/installation/)

Next, run this command in your Raspberry Pi terminal to install the pip package manager. Select "yes" when it asks if you want to continue.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt-get install pip
```

The command above installs the latest version of `python3` and `pip3` on your Raspberry Pi.
To verify and get the version of the package, you can run the command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 --version
```

The [Viam Python SDK](https://python.viam.dev/) (Software Development Kit) allows you to write programs in the Python programming language to operate robots using Viam. To get the Python SDK working on the Raspberry Pi, run the following command in your Raspberry Pi terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip install viam-sdk
```

## Test the SDK with your robot

On the [Viam app](https://app.viam.com), select the **code sample** tab, then confirm that **Python** is set as the default language.

![A screenshot of the word Language with four boxes below it with Python, Golang, Typescript (Web), and Remotes in each one. Python has a black background with white text and a checkmark, the other three have white backgrounds with black text.](../../img/single-component-tutorials-servo-mousemover/choose-python.png)

Since we already installed the Python SDK, we can skip the first step. Copy the code in from step 2.

![A screenshot of the Viam app showing the CODE SAMPLE tab. On this tab it has Language: with four boxes, Python is a black background with white text and has a checkmark indicating it is selected, then there's Golang, Typescript (Web), and Remotes with white backgrounds and black text. The page next says Python SDK (Documentation) with a link to Documentation. Below that there's a place that says "pip install viam-SDK" this is how you install the Viam Python SDK. Below that instruction are the instructions to "Then copy and run the following code to connect to your robot:" with 7 lines of code seen (the screenshot is incomplete).](../../img/single-component-tutorials-servo-mousemover/code-sample-page.png)

The copied code needs to go in a Python file on the Raspberry Pi.
You can do so by creating a file on the Raspberry Pi and editing the file with nano.

Inside the Raspberry Pi Terminal, run the following command to create a folder to put our files in (name this folder whatever you want).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mkdir mousefolder
```

Go into mousefolder.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cd mousefolder
```

Create a file using nano with the .py which is the python file extension, (name this file whatever you want).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
nano anyname.py
```

Paste the code you got from the **code sample** tab in the Viam app. Press CTRL+O, then CTRL+M, then CTRL+X to save the code and exit.

![Raspberry Pi terminal showing the connect code from the previous example.](../../img/single-component-tutorials-servo-mousemover/sample-code.png)

Now, run the code using the below command to get the resource information that lets us know if the connection is good or if there are any errors.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 anyname.py
```

![The output of the code showing a list of the resources.](../../img/single-component-tutorials-servo-mousemover/resources-printed.png)

There are no errors in the resources above, so we have confirmed a good software connection between the Python SDK and your Viam robot!

## Connect the Servo

First, **turn off your Raspberry Pi**.
This will help prevent any accidents when connecting the hardware.

Now, follow this schematic diagram to attach jumper wires to the servo and Raspberry Pi.

- **GND** on servo attached to pin 6 on Pi
- **5V** on servo attached to pin 2 on Pi
- **PWM** on servo attached to pin 12 on Pi

![Computer-drawn photo schematic of a Raspberry Pi connected to a FS90R servo. It shows the yellow wire coming from the servo as the PWM wire and it's attached to pin twelve on the raspberry pi. The red wire coming from the servo is a five-volt wire and it's attached to pin two. The black wire coming from the servo is the ground wire and it's attached to pin eight.](../../img/single-component-tutorials-servo-mousemover/servo-wiring-diagram.png)

Once you have the wires connected, attach the wheel/arm to servo and turn on the Raspberry Pi.

## Configure your robot

The servo is now physically connected to the Raspberry Pi, but the Viam app hasn't been told the details of which components/services it's using yet, so it's not able to control the servo.

Go to the [Viam app](https://app.viam.com), and navigate to the **config** tab.

![This is a screenshot of the Viam app on the CONFIG page. It shows that Builder is chosen as the mode. Below that in the components tab it shows Create Component and to the far left It says Name with a box for a Name to be typed in. The next box to the right says Type and it shows a drop down list of different types of components in Viam. To the far right it says Model, but it's greyed out because none of the previous two fields have been filled in. Directly to the right of Model is a Create Component button that will create the component.](../../img/single-component-tutorials-servo-mousemover/new-component.png)

### Board component

In the **config** tab, create a new component with the following attributes:

- **Name**: `local` - you can name this whatever you want, you will reference it later.
- **Type**: `board`
- **Model**: `pi`

![This is a screenshot of the Viam app on the CONFIG page. It shows that Builder is chosen as the mode. Below that in the components tab it shows Create Component and to the far left It says Name with a box and the name local typed in. The next box to the right says Type and it shows a drop down list of different types of components in Viam with board selected. To the far right it says Model with a drop down list and pi is selected. Directly to the right of Model is a Create Component button that will create the component.](../../img/single-component-tutorials-servo-mousemover/new-board.png)

Click **Create Component** to create the pi [board component](/components/board) component.

### Servo component

After the board component, create a new [servo component](/components/servo/) with the following attributes:

- **Name**: `FS90R` - we named the servo using the model number, but you can use whatever you want, you will reference it later.
- **Type**: `servo`
- **Model**: `pi`

![This is a screenshot of the Viam app on the CONFIG page. It shows that Builder is chosen as the mode. Below that in the components tab it shows Create Component and to the far left It says Name with a box and the name FS90R typed in. The next box to the right says Type and it shows a drop down list of different types of components in Viam with servo selected. To the far right it says Model with a drop down list and pi is selected. Directly to the right of Model is a Create Component button that will create the component.](../../img/single-component-tutorials-servo-mousemover/new-servo.png)

Click **Create Component** to create the [servo component](/components/servo/).

You will then see where you can put in Attributes for the servo.
This is where you tell Viam which hardware pin to use to control the servo.

- For "pin": use "12" - this is the pin you attached the PWM (Pulse Width Modulation) jumper wire to.
- For "board": use "local"
- For **Depends On** click **local.** This ensures that the board is initialized before the servo.

The attribute section will look like this:

![This is a screenshot of the Viam app on the CONFIG page. This shows the options that populate when you create a servo with the pi Model. It shows attributes to fill out, with a JSON coding area next to it. "Pin" is filled in with "12" and "Board" is filled in with "local". Pin and board are required fields. To the right of this area is an "Attribute Guide" with optional attributes and required. Required attributes are denoted with a star before the word. To the left below the Attributes is Data Capture Configuration and to the right of this is a button that says Add Method. Below that and to the left it says Frame and to the right of Frame it has a button that says Add Frame. Below this and to the left it says Depends On and to the right of that it has a dropdown box. Below the dropdown box you can see I've chosen local, which has an x next to the word to delete it.](../../img/single-component-tutorials-servo-mousemover/servo-config.png)

Click the **Save Config** button.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/save-config.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/save-config.mp4" alt="Square button that says Save Config with a graphic of an old floppy disk in the corner. A mouse in the shape of a extended finger clicks the button." max-width="200px">}}
</div>

## Control the servo in Viam app

If everything went well, the servo started to move.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/its-alive.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/its-alive.mp4" alt="Small square .gif of black and white frankenstein clip with man with brown hair in lab coat frantically looking around and yelling while text that says \"IT'S ALIVE! IT'S ALIVE!\" is on screen. There's a very tall man with something on his head on a table behind him and another man sitting on a chair behind the table." max-width="400px">}}
</div>

Navigate to the **control** tab and press the **STOP** button on the servo card (matching what you named the servo) to stop the servo.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/stop.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/stop.mp4" alt="Red square button with the word STOP on it with an animation of a finger mouse pointer clicking it." max-width="150px">}}
</div>

Click on the top of the servo card to open the servo controls.

**Angle** will determine what speed your servo goes and in what direction.
90 degrees is the midway point and is the stopping point.
Try changing the angle to a few different settings.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/angle-100.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/angle-100.mp4" alt="A gif at the top of the CONTROL tab in the Viam app. The pointer finger is pressing the 10 button and it changes the angle from 90 to 100 repeatedly. The red STOP button is in the upper right corner. There is a blue circular arrow depicting the servo's direction as being counterclockwise. Below this is a gif of the Raspberry Pi to the left and the FS90R servo on the right. The servo stops, then spins counterclockwise repeatedly.">}}
</div>

## Assemble the mouse mover

Now that you've confirmed that the software and hardware are connected and working correctly with Viam, let's assemble the mouse mover.

### Position the Raspberry Pi and servo in the box

Put the Raspberry Pi and servo in the box and mark out where each should be, then take the Raspberry Pi out.
Now, make sure the servo is close to level with the top (leaving a tiny bit of room for the circle cut out and tape).
Tape the servo in place.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/servo-in-box.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/servo-in-box.mp4" alt="One hand holds a shallow box while the other holds a servo against the bottom and turns it to show the audience how flush the servo is to the top.">}}
</div>

### Cut a holes in the box for the Pi

Place the Raspberry Pi back in the box and mark where the USB-C plug is so that you know where it is on the outside of the box.
Take out the Raspberry Pi.
Grab a box cutter and cut out a power hole.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/pi-hole.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/pi-hole.mp4" alt="This is a sped up gif of cutting a hole for the raspberry pi. First the person puts the raspberry pi inside to mark where the power holes are, then a mark is made on the lateral side of the box, then they pull out the raspberry pi and use boxcutters to cut a hole.">}}
</div>

Since the Raspberry Pi will be in a box and won't have much ventilation, cutting a courtesy hole to allow for it to vent is the least we could do to keep it from frying.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/vent-box.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/vent-box.mp4" alt="This is sped up gif showing cutting the heat hole for the Raspberry Pi. First, they put the Raspberry Pi inside and identify where they need to cut on the bottom of the box, they then pull the Raspberry Pi out. Then they use box cutters to cut a one-inch by two-inch hole.">}}
</div>

Be sure to tape the jumper wires out of the way of the servo.

### Cut the mouse mover circle out of the box and tape to servo

The technique we used to find the center of the circle was to mark the screw on the servo.
Gently push on the box to get a mark on the inside of the box, then create a cut we could see from the other side.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/cut-box.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/cut-box.mp4" alt="This is sped up gif showing using a marker and marking the screw of the servo, then shutting the box quick and getting the marker on the lid, then opening it back up. Then using that mark to make a cut with a box cutter, and on the other side of the lid which is the outside, marking that cut hole and putting a large roll of tape down to draw a circle. Finally, cutting the circle out with box cutters.">}}
</div>

### Tape the box shut, add "babygates", and plug in the Raspberry Pi

When taping the box shut be sure the servo with the circle cut out sits fairly flush to the top of the box.
Add "babygates" or rails to keep the mouse from wandering off if it catches some friction.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/single-component-tutorials-servo-mousemover/finish-box.webm" mp4_src="../../img/single-component-tutorials-servo-mousemover/finish-box.mp4" alt="This is sped up gif showing a person plugging in the power cable to the raspberry pi through the power hole made earlier, then pushing the rocker switch to turn it on. When the Raspberry Pi is turned on, the circle turns for a millisecond. Then they draw a swirl design on the circle. Then they make the circle spin and put a mouse on it and it falls off immediately. The next thing they do is they put cardboard on two sides of the box and at the end, they place the mouse on top.">}}
</div>

### Control your robot with code

Copy the code from the [mousemover Github repository](https://github.com/viam-labs/tutorial-mousemover) into your nano file, save it, and run it.

The code uses the Python SDK to securely connect to your robot through Viam app.
Then, it enters a for loop in which **position** tells us the servo **myServo** to move to positions (angle, or speed/direction) between 80 and 93 degrees as specified in the **sequence** list.
The code uses **pause_time** to wait for a random amount of time between 5 and 20 seconds to stay at that position.

You can adjust the range (or speed/direction) by changing the two numbers in the position statement. (Currently set at 80 and 93).
You can also change the time that the servo is allowed to spin in any direction by changing the two numbers in the pause_time statement.
Experiment and have fun.

## Next steps

If you want to build more robots, head over to our documentation site and take a look at our [tutorials](/tutorials/).
And if you didn't like this tutorial and would like to speak to my manager, their name is <img src="../../img/single-component-tutorials-servo-mousemover/censor.jpg" style="width:50px;" alt="Fuzzy box meant to censor text."></img>.
(Update: apparently that's a big no no.)

You can also join us in [Viam's Discord](https://discord.gg/viam) for any issues, comments, hardware chats, banter, and debates on if pineapple belongs on pizza or not.
