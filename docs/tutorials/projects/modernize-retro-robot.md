---
title: "Modernize a 1980s robot"
linkTitle: "Modernize a 1980s Robot"
weight: 60
type: "docs"
tags: ["base", "retro", "vision", "computer vision", "camera", "motor", "python"]
description: "Modernize a 1980s robot with Viam - Part 1"
image: ""
images: []
draft: false
imageAlt: ""
# SME: Matt Vella
---

From Star Wars to Short Circuit, Go-bots to Voltron to Transformers - the 1980s was a time of mass propagation in pop culture of how robots might exist alongside us in the future.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/omnibot_ad.png" class="alignleft" alt="1984 advertisement for the Omnibot 2000." title="1984 advertisement for the Omnibot 2000." style="max-width: 350px" />
</div>

Along with robots appearing in mass media, a good number of toy robots made their way into homes.
While these robots certainly did allow some fun for those fortunate enough to have one, they ultimately were often a fairly crude combination of common tech of the times.
Cross a remote control car with a cassette player, walkie-talkie, and alarm clock - you had the top of the line toy robot of the 1980s: the Tomy Omnibot 2000.

Let’s bring the Omnibot 2000 closer to the robot vision that many had (and still have) by bringing in new technology.
We'll also rename it Omnibot MAIV (Modernized with AI and Viam).
We will keep the original housing, style and motors where possible - but bring it into the modern era with:

* Programmatic control
* Secure internet communication
* Upgraded sensors
* Computer vision
* Machine learning and AI

*This part one of the Omnibot MAIV series, where we'll focus on getting MAIV integrated with the Viam platform.
Be sure to check back later for updates.*

## Parts list

Other than the Omnibot 2000, which you'll need to find on a used marketplace like EBay, the rest are commodity parts that can be reliably purchased.
Some of the items listed here are supplies that can be used for projects beyond this one.

|Part  | Price | Notes |
| --- | --- | --- |
[Omnibot 2000](https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2047675.m570.l1312&_nkw=omnibot+2000&_sacat=0)|$250|Prices can vary dramatically - we paid about $200 for an "as-is, non-working" copy. You do not need one with the remote control or tray included.|
[12V to 5V DC USB Type-C step-down power converter](https://www.amazon.com/dp/B0BNQ9XXCZ/)|$7.99|To power the Pi from a 12v battery.|
[12v power supply](https://www.amazon.com/TMEZON-Power-Adapter-Supply-2-1mm/dp/B00Q2E5IXW)|$8.09|To charge the battery.|
[L298N motor drive controller board 2-pack](https://www.amazon.com/DAOKI-Controller-H-Bridge-Stepper-Mega2560/dp/B085XSLKFQ/r)|$8.31|To control the base and head motors.|
[LEDs](https://www.amazon.com/ELEGOO-Diffused-Assorted-Colors-Arduino/dp/B0739RYXVC/)|$11.98|You'll need 2 LEDs to light up the eyes, smaller quantities can be purchased.|
[Webcam](https://www.amazon.com/gp/product/B08PTNVPKX)|$36.15|A webcam that can be placed as a "nose", there are many options.|
[12V Battery pack](https://www.amazon.com/5200mAh-Lithium-57-72Wh-Rechange-Connectors/dp/B08D1SHJDC)|$59.00|The Omnibot had a battery pack, but it likely will not work after almost 40 years; our was missing. You do not need to use lithium ion batteries, but if your battery pack does not fit in the battery compartment you will need to house it elsewhere and route wires differently than in this tutorial. If you have the know-how, you could alternately build a 12V battery pack with 18650s and a spot welder.|
[Ultrasonic sensor](https://www.amazon.com/WWZMDiB-HC-SR04-Ultrasonic-Distance-Measuring/dp/B0B1MJJLJP)|$3.50|For obstacle avoidance|
[Raspberry Pi 4B](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X)|$145.00|You can use any Pi or supported SBC that runs 64 bit Linux.|
[DC barrel pigtail connectors](https://www.amazon.com/43x2pcs-Connectors-Security-Lighting-MILAPEAK/dp/B072BXB2Y8)|$9.79|For connecting the battery pack to the robot|
[Assorted breadboard wires](https://www.amazon.com/EDGELEC-Optional-Breadboard-Assorted-Multicolored/dp/B07GD17ZF3)|$19.98|Various lengths will be helpful.|
[18 gauge stranded wire](https://www.amazon.com/American-Gauge-Primary-Black-Available/dp/B07D74RGVM)|$11.38|Other gauges can work, for connecting various components that don't have pins|
[Quick wire connectors](https://www.amazon.com/Quick-Connect-Wire-Connectors-Kit/dp/B0BRQD257H/)|$25.00|Not required, but will make wire connections secure and simple.|
[Velcro tape](https://www.amazon.com/Double-Sided-Adhesive-Strong-Self-Adhesive-Fastener/dp/B07TVZB1GL)|$9.99|This will help us organize the components we add to the robot base.|

You'll also need some basic tools and supplies:

* Screwdrivers
* Drill and drill bits
* Wire cutters/strippers
* Soldering iron and solder
* Paper towels
* Window cleaner
* Multimeter

## Introduce yourself to Omnibot 2000

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_here.jpg" class="alignright" alt="The Omnibot 2000." title="The Omnibot 2000." style="max-width: 250px" />
</div>

Your Omnibot 2000 arrival will likely be both exciting *and* full of dust.
So get out your window cleaner and paper towels and get to know it while giving it a good cleaning.

The Omnibot is driven by two wheels on each side, with a 3rd un-powered wheel per side.
The powered wheels have treads, you'll want to see if yours are intact and usable as they are important for traction.
Ours were in decent shape - if yours are not you can find them for sale on [Ebay](https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=omnibot+2000+treads&_sacat=0&LH_TitleDesc=0&_odkw=omnibot+2000&_osacat=0) or 3D-printable at [Thingaverse](https://www.thingiverse.com/thing:4779479).

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_wheels.jpg" class="alignleft" alt="Omnibot 2000 wheels." title="Omnibot 2000 wheels." style="max-width: 200px" />
</div>

Note that Omnibot seems to be right-handed - its right arm and hand are motorized, while the left is manually posable.
We'll take on controlling its arm and gripper in a future tutorial.

The tape player in an interesting device to have built-into a robot - and it certainly adds to the retro look.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_unscrew_battery_cover.jpg" class="alignright" alt="Omnibot 2000 battery cover being opened." title="Omnibot 2000 battery cover being opened." style="max-width: 170px;" />
</div>

It is powered separately from the rest of the robot.
We won't attempt to resurrect it, but go for it if you like, and tell us how it goes!

There is a panel in the middle of Omnibot's back with a few switches and a number of ports.
With a screwdriver, open this panel.
This compartment is a nice size for our battery pack, and you will see a barrel jack that we'll later use to plug the battery pack into.
Leave this panel open as we move to the next steps.

## Transformation

Now is the time to give the Omnibot new life as MAIV (Modernized with AI and Viam).
This will take some surgery - but fortunately its all low-risk.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_surgery.jpg" alt="Omnibot 2000 taken apart." title="Omnibot 2000 taken apart." style="max-width: 400px;" />
</div>

### Inside MAIV's base

Start by placing MAIV face-down on a large table or floor, and finding the six screw locations.
Unscrew each screw (if yours has all of its screws intact, ours was missing a few), and place the base wheels-down.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_base_open.jpg" alt="Omnibot MAIV base opened." class="alignleft" title="Omnibot MAIV base opened." style="max-width: 250px;" />
</div>

The first thing you may notice is that inside the base, there is a good amount of room to work.
We'll be adding electronic components here, as this is also a fairly easy place to access.
In the rear, there is a thick plastic box.
Locate the screw, and open carefully open it.

Inside you'll see 3 motors and some gears that drive the base's left and right wheels.
Inside this gearbox is probably one of the cleanest places within your robot - we were amazed to see clear, clean grease on the gears.
Be sure to keep it this way!

#### Mark MAIV's base motors

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_motor_wires_labeled.PNG" alt="Omnibot MAIV base opened." class="alignright" title="Omnibot MAIV base opened." style="max-width: 250px;" />
</div>

You will see two wires leading to each motor.
Trace them to the outside of the gearbox, and mark them left, right, and front - we used masking tape and a marker.
Once you've marked the wires, close up the gearbox with the screws you removed earlier.

The front motor allows a switch from high to low gear.
We won't wire this as part of this tutorial - so if you want to shift the gear, you can do so manually with the gearbox cover off.

#### Wire MAIV's base motors to the motor driver

We have now reached the part of the tutorial where we will begin to actually modify the robot.
If the thought of anything other than restoring an Omnibot 2000 to its original working condition makes you sad, we understand.
But first, remember it was in someone's attic gathering dust for years.
Second, we will re-use the motors and gears and leave the original circuit boards in-place (albeit no longer used).
It's a [restomod](https://www.goldeagle.com/tips-tools/what-is-a-restomod/)!

You will wire the left and right motors to a motor controller and our board - this will allow your Omnibot to be controlled with Viam as a [wheeled base](/components/base/wheeled/).

First, detach the left and right base motor's wires from the small printed circuit board.
Orient the L298N so that the `OUT1` and `OUT2` terminals are on the left side.
Using a screwdriver, attach the 2 wires from the left motor to the `OUT1` and `OUT2` terminals.
Now, attach the 2 wires from the right motor to the `OUT3` and `OUT4` terminals.

[TODO: need wiring diagram here]

Ensure your Raspberry Pi powered off, and connect GPIO pins for the left motor with female-to-female jumper wires.
You can use any GPIO pins, but we connected pin 32 to `IN1`, pin 38 to `IN2`, and pin 35 to `ENA`.
Now, do the same for the right motor, connecting pin 31 to `IN3`, pin 36 to `IN4` and pin 22 to `ENB`.
Cut off one end of a jumper wire, strip it and connect pin 34 (ground) to the common ground terminal `GND` on the L298N.

### Powering MAIV

Conveniently, MAIV has a easy-to-access external switches, a barrel jack in the battery compartment, and a barrel jack on the exterior.
Spending a little time now repurposing these will make it easy for you to power up, power down, and charge your robot.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_switch_solder.jpg" alt="Omnibot MAIV switch wires soldered." class="alignright" title="Omnibot MAIV switch wires soldered." style="max-width: 150px;" />
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

If your battery pack has a non-barrel jack connector, you'll need to add one.
Cut off any existing connector, and solder the red wire of a male barrel connector pigtail to the positive battery wire, the black wire from the pigtail connector to the negative battery wire.
Don't plug the battery in just yet.

#### Wire the power sources

You now need to open the center/torso part of MAIV in order to access the wiring within.
From the top portion of the already open base, locate any screws that attach lower base to the torso and remove them.
Then, locate the screws on the sides of MAIV's torso and remove them.
You should now be able to remove the back portion of the torso.
Turn it over so that the wires coming out of the battery box and switches are facing upwards.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_main_board.jpg" alt="Omnibot MAIV power wiring." class="alignleft" title="Omnibot MAIV power wiring." style="max-width: 250px;" />
</div>

At the top of the torso, you'll notice a large printed circuit board that was the originally the main digital control center of the Omnibot 2000.
We'll not use it at all as we modernize MAIV, but we can leave it intact.

Now, using wire cutters and quick wire connectors, connect the battery, switch, and charger wires as shown.

<div class="td-max-width-on-larger-screens">
<img src="../../img/maiv/maiv_power_wiring.jpg" alt="Omnibot MAIV power wiring." class="alignright" title="Omnibot MAIV power wiring." style="max-width: 400px;" />
</div>

One 3-terminal quick connect joins the negative wire from the battery, the negative wire from the charging port, and a new wire that you need to run from the torso into the base to power the robot.

Another 3-terminal quick connect will join one end of the power switch, the positive wire from the battery, and the positive wire from the charging port.

Finally, run the unconnected wire from the switch (the positive to power the robot) into the base through one of the holes in the top portion of the base (in the picture we have a two terminal quick connect in order to extend the length of our wire - yours is likely long enough to avoid this).

#### Connect the power sources to the motors and Pi

Using a 4-terminal quick connector, connect the positive power supply wire (from the previous step) to the step down converter *positive* input wire.
Using a length of 18 gauge wire, connect another terminal in this quick connector to the 12V VCC screw terminal on the L298N motor driver to which you previously connected the base motors and pi.
One of the terminals to the quick connector is empty, this is expected, you will use it later.

Now use another 4-terminal quick connector to connect the negative power supply wire from the torso to the step down converter *negative* wire.
Using a length of 18 gauge wire, connect another terminal in this quick connector to the GND screw terminal on the L298N motor driver to which you previously connected the base motors and pi.
As with the positive connector, one of the terminals will be left empty.

Finally, plug the USB-C output from the step down converter to the Raspberry Pi.

#### Power MAIV on

Now you can test that your the wiring is correct.
Ensure the power switch you just wired is off, and your battery is charged.
Plug the battery into the barrel connector inside the battery compartment, then turn on the power switch.
You should see LEDs on the motor driver and Pi light up!

{{% alert title="Troubleshooting" color= "info" %}}

If you do not see the LEDs light up, turn the power switch to off.
Check your wiring, and use a multimeter to ensure that your battery has enough power, and that the positive and negative polarity is as expected.
You can also try unplugging the battery and powering instead with the wall adaptor.

{{% /alert %}}

### Base configuration

Merging 40-year-old tech with modern tech to light up LEDs verges on exciting, but we need to configure our robotic base before we can get to the true prize of controlling MAIV through the internet and programmatically.
So, for now, turn the power switch to the off position.
In just a few minutes, you'll have it back on.

Go to the [Viam app](https://app.viam.com) and create a new robot called `MAIV`.

Go to the **Setup** tab of your new robot's page and follow the steps [to install `viam-server` on your Raspberry Pi](/installation).

#### Configure the components

{{< tabs >}}
{{% tab name="Builder UI" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.

1. **Add the board**

    Enter `local` for the name for your [board component](/components/board/), select the type `board`, and select the `pi` model.
    Then click **Create component**.

2. **Add the left base motor.**

    Enter `base-l` for the name for your left base [motor component](/components/motor/), select the type `motor`, and select the `gpio` model.
    Then click **Create component**.

    Next, select `local` for the board attribute.
    Set `Max RPM` to 200.
    Toggle `Direction Flip` on (depending on how you wired your motor, you may need to turn this off later).
    Toggle `Type` to `In1/In2`.

    Now, select `32 GPIO 12` for `A/In1`.
    Select `38 GPIO 20` for `B/In2`.
    Select `35 GPIO 19` for `PWM`.

    Finally, add `local` to `Depends on` - this ensures that the `local` board component is fully initialize prior to this motor.

3. **Add the right base motor**

    Enter `base-r` for the name for your right base [motor component](/components/motor/), select the type `motor`, and select the `gpio` model.
    Then click **Create component**.

    Next, select `local` for the board attribute.
    Set `Max RPM` to 200.
    Leave `Direction Flip` off (depending on how you wired your motor, you may need to turn this off later).
    Toggle `Type` to `In1/In2`.

    Now, select `31 GPIO 6` for `A/In1`.
    Select `36 GPIO 16` for `B/In2`.
    Select `22 GPIO 25` for `PWM`.

    Finally, add `local` to `Depends on`.

4. **Add the base**

    Configuring a [base component](/components/base) allows you to create an interface to control the movement of MAIV withing needing to send individual motor commands.

    Enter `base` for the name for your base, select the type `base`, and select the `wheeled` model.
    Then click **Create component**.

    Next, add `base-r` to `Right Motors` and add `base-l` to `Left Motors`.

    Now, set `Wheel Circumference` to `90` and `Width` to `220`.

    Finally, add `base-l` and `base-r` to `Depends on`.

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following JSON configuration for your board, left motor, right motor, and base:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {},
      "depends_on": []
    },
    {
      "depends_on": [
        "local"
      ],
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
      "depends_on": [
        "local"
      ],
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
        "left": [
          "base-l"
        ],
        "right": [
          "base-r"
        ],
        "wheel_circumference_mm": 90,
        "width_mm": 220
      },
      "depends_on": [
        "base-l",
        "base-r"
      ]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

#### Test the components

MAIV is still in pieces, but its time to ensure that the motors and base controls are working.
Check to see if you might have something that you can use to set MAIV's base upon so the motorized wheels can spin freely.
Or, if the wires between the base and the torso are long enough to allow small movements of the base you can leave the base on the flat surface.

Navigate to your robot's [Control tab](/manage/fleet/robots/#control).
Click on the base panel and use the arrows to control the base.
Ensure the motors on both side are working, and that the wheels are spinning as expected.
If the wheels on a side are spinning in the opposite direction of what you would expect, go back to the **Config** tab, toggle `Direction Flip` for the appropriate motor, **Save config** and repeat the test steps.

{{<video webm_src="../../img/maiv/maiv_base_test.webm" mp4_src="../../img/maiv/maiv_base_test.mp4" alt="MAIV base test movements" max-width="300px">}}

From the **Control tab** you can also test the individual motors directly by first selecting the direction and power percent, then starting the motor by clicking `RUN` and stopping the motor by clicking `STOP`.

### MAIV's head

In order to give MAIV a bit more personality, but also more capability, let's wire MAIV's neck motor and eyes.
You'll also add a camera so MAIV can see the world.

