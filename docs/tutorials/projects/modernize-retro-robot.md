---
title: "Modernize a 1980s robot"
linkTitle: "Modernize a 1980s Robot"
type: "docs"
webmSrc: "/tutorials/maiv/maiv_front.webm"
mp4Src: "/tutorials/maiv/maiv_front.mp4"
images: ["/tutorials/maiv/maiv_front.gif"]
tags:
  ["base", "retro", "vision", "computer vision", "camera", "motor", "python"]
no_list: true
description: "Modernize the Omnibot 2000 from the 1980s with Viam and AI."
imageAlt: "The front of the Ombibot 2000 robot"
authors: ["Matt Vella"]
languages: []
viamresources: ["board", "motor", "base", "camera"]
level: "Intermediate"
date: "2023-05-04"
# updated: ""
cost: 580
---

From Star Wars to Short Circuit, Go-bots to Transformers - the 1980s was a time in pop culture where people thought a lot about how robots might exist alongside us in the future.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/omnibot_ad.png" resize="400x" declaredimensions=true alt="1984 advertisement for the Omnibot 2000." class="alignleft" style="max-width: 350px">}}
</div>

Along with robots appearing in mass media, a good number of toy robots made their way into homes.
While these robots certainly were fun for those fortunate enough to have one, they were often a fairly crude combination of common tech of the times.
Cross a remote control car with a cassette player, walkie-talkie, and alarm clock - you had the top of the line toy robot of the 1980s: the Tomy Omnibot 2000.

Let’s bring the Omnibot 2000 closer to the home robot vision that many had (and still have) by bringing in new technology and rename it the Omnibot MAIV (Modernized with AI and Viam).

We will keep the original housing, style and motors where possible - but bring it into the modern era with:

- Programmatic control
- Secure internet communication
- Upgraded sensors
- Computer vision
- Machine learning and AI

By the end of this tutorial, you'll be able to securely control your Omnibot from anywhere, and leverage machine learning capabilities to have MAIV interact with the world.

## Parts list

Other than the Omnibot 2000, which you'll need to find on a used marketplace like eBay, the rest are commodity parts you can find easily:

<!-- prettier-ignore -->
|Part  | Price | Notes |
| --- | --- | --- |
[Omnibot 2000](https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2047675.m570.l1312&_nkw=omnibot+2000&_sacat=0)|$250|Prices can vary dramatically - we paid about $200 for an "as-is, non-working" copy. You do not need one with the remote control or tray included.|
[12V to 5V DC USB Type-C step-down power converter](https://www.amazon.com/dp/B0BNQ9XXCZ/)|$7.99|To power the Pi from a 12V battery.|
[12V power supply](https://www.amazon.com/TMEZON-Power-Adapter-Supply-2-1mm/dp/B00Q2E5IXW)|$8.09|To charge the battery.|
[L298N motor drive controller board 2-pack](https://www.amazon.com/DAOKI-Controller-H-Bridge-Stepper-Mega2560/dp/B085XSLKFQ/r)|$8.31|To control the base and head motors.|
[LED E10 bulbs](https://www.amazon.com/Ruiandsion-6000K-Flashlight-Headlight-Negative/dp/B08SLQBZGN)|$7.99|You'll need 2 LED bulbs to light up the eyes.|
[Webcam](https://www.amazon.com/gp/product/B08PTNVPKX)|$36.15|A webcam that can be placed as a "nose", there are many options.|
[12V Battery pack](https://www.amazon.com/5200mAh-Lithium-57-72Wh-Rechange-Connectors/dp/B08D1SHJDC)|$59.00|The Omnibot had a battery pack, but it likely will not work after almost 40 years; ours was missing. You do not need to use lithium ion batteries, but if your battery pack does not fit in the battery compartment you will need to house it elsewhere and route wires differently than in this tutorial. If you have the know-how, you could alternately build a 12V battery pack with 18650s and a spot welder.|
[Ultrasonic sensor](https://www.amazon.com/WWZMDiB-HC-SR04-Ultrasonic-Distance-Measuring/dp/B0B1MJJLJP)|$3.50|For obstacle avoidance.|
[Raspberry Pi 4B](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X)|$125.00|You can use any Pi or supported SBC that runs 64 bit Linux.|
[DC barrel pigtail connectors](https://www.amazon.com/43x2pcs-Connectors-Security-Lighting-MILAPEAK/dp/B072BXB2Y8)|$9.79|For connecting the battery pack to the robot.|
[Assorted breadboard wires](https://www.amazon.com/EDGELEC-Optional-Breadboard-Assorted-Multicolored/dp/B07GD17ZF3)|$19.98|Various lengths will be helpful.|
[18 gauge stranded wire](https://www.amazon.com/American-Gauge-Primary-Black-Available/dp/B07D74RGVM)|$11.38|For connecting various components that don't have pins.|
[Quick wire connectors](https://www.amazon.com/Quick-Connect-Wire-Connectors-Kit/dp/B0BRQD257H/)|$25.00|Not required, but these make wire connections secure and simple.|
[Velcro tape](https://www.amazon.com/Double-Sided-Adhesive-Strong-Self-Adhesive-Fastener/dp/B07TVZB1GL)|$9.99|This will help us organize the components we add to the robot base.|

You'll also need some basic tools and supplies:

- Screwdrivers
- Drill and drill bits
- Wire cutters/strippers
- Soldering iron and solder
- Paper towels
- Window cleaner or other cleaner to remove dust, etc.
- Multimeter

## Introduce yourself to Omnibot 2000

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_here.jpg" resize="300x" declaredimensions=true alt="The Omnibot 2000." class="alignright" style="max-width: 250px">}}
</div>

Your Omnibot 2000 arrival will likely be both exciting _and_ full of dust.
Get out your window cleaner and paper towels and get to know it while giving it a good cleaning.

The Omnibot is driven by two wheels on each side, with a third un-powered wheel per side.
The powered wheels have treads - you'll want to see if yours are intact and usable as they are important for traction.
Ours were in decent shape - if yours are not you can find them for sale on [eBay](https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=omnibot+2000+treads&_sacat=0&LH_TitleDesc=0&_odkw=omnibot+2000&_osacat=0) or 3D-printable at [Thingiverse](https://www.thingiverse.com/thing:4779479).

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_wheels.jpg" resize="300x" declaredimensions=true alt="Omnibot 2000 wheels." class="alignleft" style="max-width: 200px">}}
</div>

Note that Omnibot seems to be right-handed - its right arm and hand are motorized, while the left is manually posable.
This tutorial does not cover how to control its arm and gripper.

The tape player is an interesting device to have built-into a robot - and it certainly adds to the retro look.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_unscrew_battery_cover.jpg" resize="250x" declaredimensions=true alt="Omnibot 2000 battery cover being opened." class="alignright" style="max-width: 170px;">}}
</div>

It is powered separately from the rest of the robot.
We won't attempt to resurrect it, but if you do tell us how it goes!

There is a panel in the middle of Omnibot's back with a few switches and a number of ports.
With a screwdriver, open this panel.
This compartment is a good size for our battery pack, and you will see a barrel jack that we'll later use to plug the battery pack into.
Leave this panel open as we move to the next steps.

## Transformation

Now is the time to start transforming Omnibot into MAIV (Modernized with AI and Viam).
This will take some surgery - but fortunately its all low-risk.
Just remember to set aside any screws you remove in a place where they remain organized and will not get lost.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_surgery.jpg" resize="500x" declaredimensions=true alt="Omnibot 2000 taken apart." style="max-width: 400px;">}}
</div>

### Inside MAIV's base

Start by placing MAIV face-down on a large table or floor, and find the six screw locations on the bottom near the wheels.
Unscrew each screw (if yours has all of its screws intact, ours was missing a few), detach the lower base and place it wheels-down.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_base_open.jpg" resize="300x" declaredimensions=true alt="Omnibot MAIV base opened." class="alignleft" style="max-width: 250px;">}}
</div>

The first thing you may notice is that inside the base, there is a good amount of room to work.
We'll be adding electronic components here, as this is also a fairly easy place to access.
In the rear, there is a thick plastic box.
Locate the screws, and carefully open it.

Inside you'll see 3 motors and some gears that drive the base's left and right wheels.
Inside this gearbox is probably one of the cleanest places within your robot - we were amazed to see clear, clean grease on the gears.
Be sure to keep it this way!

#### Mark MAIV's base motors

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_motor_wires_labeled.PNG" resize="300x" declaredimensions=true alt="Omnibot MAIV base opened." style="max-width: 250px;" class="alignright">}}
</div>

You will see two wires leading to each motor.
Trace them to the outside of the gearbox, and mark them left, right, and front - we used masking tape and a marker.

The front motor allows a switch from high to low gear.
We won't wire this as part of this tutorial - if you want to shift the gear, you can do so manually with the gearbox cover off.

Once you've marked the wires, close up the gearbox with the screws you removed earlier.

#### Wire MAIV's base motors to the motor driver

We have now reached the part of the tutorial where we will begin to actually modify the robot.
If you hesitate at the thought of physically modifying an Omnibot 2000, remember that it was in someone's attic gathering dust for years.
Plus, we will re-use the motors and gears and leave the original circuit boards in-place (albeit no longer used).
It's a [restomod](https://www.goldeagle.com/tips-tools/what-is-a-restomod/)!

Let's get started with wiring the left and right motors to a motor controller and Raspberry Pi - this will allow your Omnibot to be controlled with Viam as a [wheeled base](/components/base/wheeled/).

First, detach the left and right base motor's wires from the small printed circuit board.
Orient your L298N so that the `OUT1` and `OUT2` terminals are on the left side.
Using a screwdriver, attach the 2 wires from the left motor to the `OUT1` and `OUT2` terminals.
Now, attach the 2 wires from the right motor to the `OUT3` and `OUT4` terminals.

![Omnibot MAIV base wiring diagram.](/tutorials/maiv/viam-omnibot-wiring-01.png)

Ensure your Raspberry Pi is powered off, and connect GPIO pins for the left motor with female-to-female jumper wires.
You can use any GPIO pins, but we connected pin 32 to `IN1`, pin 38 to `IN2`, and pin 35 to `ENA`.
Now, do the same for the right motor, connecting pin 31 to `IN3`, pin 36 to `IN4` and pin 22 to `ENB`.
Cut off one end of a jumper wire, strip it and connect pin 34 (ground) to the common ground terminal `GND` on the L298N.

### Powering MAIV

Conveniently, MAIV has easy-to-access external switches, a barrel jack in the battery compartment, and a barrel jack on the exterior.
Spending a little time now repurposing these will make it easy for you to power up, power down, and charge your robot.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_switch_solder.jpg" resize="300x" declaredimensions=true alt="Omnibot MAIV switch wires soldered." style="max-width: 150px;" class="alignright" >}}
</div>

#### Power switch and battery

Behind the battery panel door, you'll see a cover with 4 screws.
Unscrew the cover to access the circuit board.
We will use the top switch on this circuit board to power our robot.
Soldier two wires (50 cm each or so) to the outer top two pins on the backside of the switch.

We are not going to use any of the existing wires coming out of this switch panel, so you can cut them.
In case you want to connect to them later, leave enough length before the cut to do so.
Now, screw the cover back on with all wires extending out through the bottom of the cover.
Feed the two wires you just added into the center cavity of the robot through one of the openings at the back side of the battery panel.

If your battery pack does not have a barrel jack connector, you'll need to add one.
Cut off any existing connector, and solder the red wire of a male barrel connector pigtail to the positive battery wire, the black wire from the pigtail connector to the negative battery wire.

{{< alert title="Caution" color="caution" >}}
Don't plug the battery in just yet.
{{< /alert >}}

#### Wire the power sources

You now need to open the center/torso compartment of MAIV in order to access the wiring within.
From the top portion of the already open base, locate any screws that attach the lower base to the torso and remove them.
Then, locate the screws on the sides of MAIV's torso and remove them.
You should now be able to remove the back portion of the torso.
Turn this over so that the wires coming out of the battery box and switches are facing upwards.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_main_board.jpg" resize="300x" declaredimensions=true alt="Omnibot MAIV power wiring." style="max-width: 250px" class="alignleft" >}}
</div>

At the top of the torso, you'll notice a large printed circuit board that was originally the main digital control center of the Omnibot 2000.
We'll won't use it at all as we modernize MAIV, but we can leave it intact.

Now, using wire cutters and quick wire connectors, connect the battery, switch, and charger wires as shown.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_power_wiring.jpg" resize="300x" declaredimensions=true alt="Omnibot MAIV power wiring." style="max-width: 400px;" class="alignright" >}}
</div>

One 3-terminal quick connect joins the negative wire from the battery, the negative wire from the charging port, and a new wire that you need to run from the torso into the base to power the robot.

Another 3-terminal quick connect will join one end of the power switch, the positive wire from the battery, and the positive wire from the charging port.

Finally, run the unconnected wire from the switch (the positive to power the robot) into the base through one of the holes in the top portion of the base (in the picture we have a 2-terminal quick connect in order to extend the length of our wire - yours is likely long enough to avoid this).

#### Connect the power sources to the motors and Pi

Working in the robot base, use a 4-terminal quick connector to connect the positive power supply wire (from the previous step) to the step down converter _positive_ input wire.
Using a length of 18 gauge wire, connect another terminal in this quick connector to the 12V VCC screw terminal on the L298N motor driver to which you previously connected the base motors and Pi.
One of the terminals to the quick connector is empty.
This is expected, you will use it later.

Now use another 4-terminal quick connector to connect the negative power supply wire from the torso to the step down converter _negative_ wire.
Using a length of 18 gauge wire, connect another terminal in this quick connector to the GND screw terminal on the L298N motor driver to which you previously connected the base motors and Pi.
As with the positive connector, one of the negative terminals will be left empty.

Finally, plug the USB-C output from the step down converter into the Raspberry Pi.

![Omnibot MAIV powered wiring diagram.](/tutorials/maiv/viam-omnibot-wiring-02.png)

#### Power MAIV on

Now you can test that your wiring is correct.
Ensure the power switch you just wired is off, and your battery is charged.
Plug the battery into the barrel connector inside the battery compartment, then turn on the power switch.
You should see LEDs on the motor driver and Pi light up!

{{% alert title="Troubleshooting" color= "info" %}}

If you do not see the LEDs light up, turn the power switch off.

Check your wiring, use a multimeter to ensure that your battery has enough power, and that the positive and negative polarity is as expected.
You can also try unplugging the battery and powering it instead with the wall adaptor.

{{% /alert %}}

## Add Viam and AI capabilities

Merging 40-year-old tech with modern tech to light up LEDs is exciting, but we need to configure our robotic base before we can get to the true prize of controlling MAIV through the internet and programmatically.
For now, turn the power switch to the off position.
In just a few minutes, you'll have it back on.

Go to the [Viam app](https://app.viam.com) and create a new machine called `MAIV`.

Go to the **Setup** tab of your new machine's page and follow the steps [to install `viam-server` on your Raspberry Pi](/get-started/installation/).

### Configure the components

{{< tabs >}}
{{% tab name="Builder UI" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab.

1. **Add the board**.

   Click the **Create component** button in the lower-left corner of the page.
   Select the type `board`, then select the `pi` model.
   Enter `local` as the name for your [board component](/components/board/), then click **Create**.

2. **Add the left motor.**

   Click **Create component** to add the [motor component](/components/motor/) on the left side of the robot base.
   Select the type `motor`, and select the `gpio` model.
   Enter `base-l` for the name, then click **Create**.

   Next, select `local` for the board attribute.
   Set `Max RPM` to 200.
   Toggle `Direction Flip` on (depending on how you wired your motor, you may need to turn this off later).
   Toggle `Type` to `In1/In2`.

   Now, select `32 GPIO 12` for `A/In1`.
   Select `38 GPIO 20` for `B/In2`.
   Select `35 GPIO 19` for `PWM`.

   Finally, add `local` to `Depends on` - this ensures that the `local` board component is fully initialize prior to this motor.

3. **Add the right motor**

   Click **Create component**.
   For your right base [motor component](/components/motor/), select the type `motor`, and select the `gpio` model.
   Enter `base-r` for the name, then click **Create**.

   Next, select `local` for the board attribute.
   Set `Max RPM` to 200.
   Leave `Direction Flip` off (depending on how you wired your motor, you may need to turn this off later).
   Toggle `Type` to `In1/In2`.

   Now, select `31 GPIO 6` for `A/In1`.
   Select `36 GPIO 16` for `B/In2`.
   Select `22 GPIO 25` for `PWM`.

   Finally, add `local` to `Depends on`.

4. **Add the base**

   Configuring a [base component](/components/base/) allows you to create an interface to control the movement of MAIV withing needing to send individual motor commands.

   Click **Create component**.
   Select the type `base`, and select the `wheeled` model.
   Enter `base` for the name for your base, then click **Create**.

   Next, add `base-r` to `Right Motors` and add `base-l` to `Left Motors`.

   Now, set `Wheel Circumference` to `90` and `Width` to `220`.

   Finally, add `base-l` and `base-r` to `Depends on`.

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/build/configure/#the-config-tab), replace the configuration with the following JSON configuration for your board, left motor, right motor, and base:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "depends_on": ["local"],
      "model": "gpio",
      "name": "base-l",
      "type": "motor",
      "attributes": {
        "pins": {
          "a": "32",
          "b": "38",
          "pwm": "35"
        },
        "board": "local",
        "dir_flip": true,
        "max_rpm": 200
      }
    },
    {
      "depends_on": ["local"],
      "model": "gpio",
      "name": "base-r",
      "type": "motor",
      "attributes": {
        "pins": {
          "a": "31",
          "b": "36",
          "pwm": "22"
        },
        "board": "local",
        "dir_flip": false,
        "max_rpm": 200
      }
    },
    {
      "model": "wheeled",
      "name": "base",
      "type": "base",
      "attributes": {
        "left": ["base-l"],
        "right": ["base-r"],
        "wheel_circumference_mm": 90,
        "width_mm": 220
      },
      "depends_on": ["base-l", "base-r"]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

### Test the base and motor components

MAIV is still in pieces, but its time to ensure that the motors and base controls are working.
Check to see if you might have something that you can use to set MAIV's base upon so the motorized wheels can spin freely.
Or, if the wires between the base and the torso are long enough to allow small movements of the base you can leave the base on the flat surface.

Navigate to your machine's [Control](/fleet/machines/#control) tab.
Click on the base panel and use the arrows to control the base.
Ensure the motors on both sides are working, and that the wheels are spinning as expected.
If the wheels on a given side are spinning in the opposite direction of what you would expect, go back to the **Config** tab, toggle `Direction Flip` for the appropriate motor, **Save config** and repeat the test steps.

{{<video webm_src="/tutorials/maiv/maiv_base_test.webm" mp4_src="/tutorials/maiv/maiv_base_test.mp4" poster="/tutorials/maiv/maiv_base_test.jpg" alt="MAIV base test movements" max-width="300px">}}

From the **Control** tab you can also test the individual motors directly.
First select the desired direction and power percent, then start the motor by clicking `RUN` and stop the motor by clicking `STOP`.

## MAIV's head

In order to give MAIV a bit more personality and capability, let's wire MAIV's neck motor and eyes.
We'll also add a camera so MAIV can see the world.

### Convert MAIV's eyes to LEDs

Because MAIV's torso is already open, the neck and head is detached.
Turn the head over, locate and unscrew the two screws holding MAIV's face plate.
You will be replacing the current incandescent bulbs with more energy-efficient LEDs that can be controlled directly from your Raspberry Pi.
In order to access the eye wiring, locate the screws on the underside of the head and unscrew them.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_eyes.jpg" resize="300x" declaredimensions=true alt="Omnibot MAIV eye plate." class="alignleft" style="max-width: 250px;" >}}
</div>

Remove the eye shield, unscrew the incandescent bulbs and screw in the LED bulbs.

The original wires to the eye bulb sockets won't be long enough to reach the Raspberry Pi.
Cut the original wires (leave some length) and strip the ends.
You will control both eyes at once, so use a 3-terminal quick connect to connect both eyes positive wires and a third long breadboard wire.
Repeat the same with another 3-terminal quick connect for the negative wires.

Now, run the long breadboard wires through the robot neck, torso, and into the base.

With the robot powered off:

- Plug the positive breadboard wire into pin 1 on the Raspberry Pi (3.3V).
- Plug the negative breadboard wire into pin 18 (GPIO 24) on the Pi.

Power your robot back on to test the eyes.
You will use GPIO directly to control the eyes through the `board` component you already configured.
Once `viam-server` is running (it will take a minute or so to initialize), go to the **Control** tab and open the _local_ board card.
From here, you can test MAIV's eyes by setting GPIO pin 18 to high (to turn the eyes on) or low (to turn the eyes off).

{{<video webm_src="/tutorials/maiv/maiv_eye_test.webm" mp4_src="/tutorials/maiv/maiv_eye_test.mp4" poster="/tutorials/maiv/maiv_eye_test.jpg" alt="MAIV eye flashing test" max-width="300px">}}

### Connect and test the neck motor

The Omnibot 2000 has a motor that allows the head to turn from side-to-side.
This motor is a simple DC motor like those found in its base; the motor is not encoded nor is it a stepper motor so precise control is not an option.

You will notice that there are two wires that are running to some sort of limit switch and two wires that are running to the motor.
Ignore those running to the limit switch.
Extend the wires running to the neck motor through the torso and into the base.

Again, power off your robot.

Take another L298N motor driver and using a screwdriver, attach the 2 wires from the neck motor to the `OUT1` and `OUT2` terminals.

Using a length of 18 gauge wire, connect the final terminal of the positive quick connector to the 12V VCC screw terminal on the L298N.
Connect the final terminal of the negative quick connector to the GND terminal on the L298N.

Connect GPIO pins for the neck motor with female-to-female jumper wires.
You can use any free GPIO pins, but we connected pin 16 to `IN1`, pin 37 to `IN2`, and pin 29 to `ENA`.

![Omnibot MAIV complete wiring diagram.](/tutorials/maiv/viam-omnibot-wiring-03.png)

{{< tabs >}}
{{% tab name="Builder UI" %}}
To add the neck motor, navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Navigate to the **Components** subtab and click **Create component** in the lower-left corner.

To create your [motor component](/components/motor/), select the type `motor`, and select the `gpio` model.
Enter `neck` as the name for your neck motor, then click **Create**.

Next, select `local` for the board attribute.
Set `Max RPM` to 200.
Leave `Direction Flip` off.
Toggle `Type` to `In1/In2`.

Now, select `16 GPIO 23` for `A/In1`.
Select `37 GPIO 26` for `B/In2`.
Select `29 GPIO 5` for `PWM`.

Finally, add `local` to `Depends on`.

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

If you are editing the configuration of MAIV using JSON directly, add the neck motor by adding the following within the components list in your configuration.

```JSON
    {
      "type": "motor",
      "model": "gpio",
      "name": "neck",
      "attributes": {
        "max_rpm": 200,
        "pins": {
          "a": "16",
          "b": "37",
          "pwm": "29"
        },
        "board": "local"
      },
      "depends_on": [
        "local"
      ]
    }
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

Power your robot back on and use the **Control** tab to test that the neck motor is connected properly and can be powered on and off.

### Add a camera "nose"

Before re-assembling MAIV, you can add a camera to your robot's face.
We can use this camera to stream video and capture images, as well as leverage it for computer vision and machine learning.

Take MAIV's gray face plate and measure to find the center between and below the eye sockets.

{{% alert title="Warning" color= "warning " %}}

Be careful not to crack MAIV's face plate when drilling (as we did).

Use a sharp (non-spade bit) at high RPM.
Covering both sides with masking tape before drilling (remove afterwards) can also help.

{{% /alert %}}

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/maiv/maiv_eye_sockets.jpg" resize="300x" declaredimensions=true alt="Omnibot MAIV face plate with camera." style="max-width: 250px;" class="alignright" >}}
</div>

Find a drill bit that is about the same circumference as the USB camera you purchased and carefully drill a hole through the face plate.

Ensure that the camera fits.

Run the USB wire through the robot neck, torso and into the base.
Plug it into the Raspberry Pi.

Now re-assemble MAIV's head, eye plate, and face plate with the screws you removed earlier.
Fit MAIV's neck into the torso, and re-assemble the torso.

{{< tabs >}}
{{% tab name="Builder UI" %}}
Add the [camera component](/components/camera/) to your robot by navigating to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click the **Create component** button in the lower-left corner.

Select the type `camera`, and select the `webcam` model.
Enter `face-cam` for the name, then click **Create**.

Being that this is the only camera currently configured for MAIV, keep 'video path' blank, and viam-server will auto-detect the path on startup or reconfiguration.

Finally, add `local` to `Depends on`.

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

If you are editing the configuration of MAIV using JSON directly, add the camera by adding the following within the components list in your configuration.

```JSON
    {
      "attributes": {
        "video_path": ""
      },
      "depends_on": ["local"],
      "model": "webcam",
      "name": "face-cam",
      "type": "camera"
    }
```

{{% /tab %}}
{{< /tabs >}}

Test your camera by navigating to the **Control** tab, opening the camera card, and turning on the video stream.
Turning MAIV's head while streaming video will give you a sense of how MAIV is starting to see the world!

{{<video webm_src="/tutorials/maiv/maiv_head_test.webm" mp4_src="/tutorials/maiv/maiv_head_test.mp4" poster="/tutorials/maiv/maiv_head_test.jpg" alt="MAIV head test" max-width="300px">}}

## MAIV in the world

Now that you've wired, configured, and tested all the components, put MAIV back together:

- Screw the upper base to the torso.
- Screw the lower base to the upper base.

Now MAIV is ready to interact with the world!

{{<video webm_src="/tutorials/maiv/maiv_driving.webm" mp4_src="/tutorials/maiv/maiv_driving.mp4" poster="/tutorials/maiv/maiv_driving.jpg" alt="MAIV driving, in one of our home offices - so not quite the world, yet" max-width="350px">}}

## Next steps

Start by driving MAIV through the **Control** panel, then try writing some code.
A simple first exercise would be to have MAIV [drive in a square](/tutorials/get-started/try-viam-sdk/).
The same code that works with any configured base will work with MAIV, you'll just need to update the robot location, robot API key and key ID and any component names that differ in the code.

Since MAIV has a camera, you could also [set up a color detector](/tutorials/services/webcam-line-follower-robot/) or detect objects using a [machine learning model](/tutorials/projects/send-security-photo/).

There's a lot more you can do with MAIV - for inspiration, check out our other [tutorials](/tutorials/).

If you end up building your own MAIV or another retro robot, we’d love to hear - let us and the [Viam community](https://discord.gg/viam) know!
