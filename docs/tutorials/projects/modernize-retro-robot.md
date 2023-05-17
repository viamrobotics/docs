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
[Quick wire connectors](https://www.amazon.com/Quick-Connect-Wire-Connectors-Kit/dp/B0BRQD257H/)|$25.00|Not required, but will make wire connections secure and simple.|
[Velcro tape](https://www.amazon.com/Double-Sided-Adhesive-Strong-Self-Adhesive-Fastener/dp/B07TVZB1GL)|$9.99|This will help us organize the components we add to the robot base.|

You'll also need some basic tools and supplies:

* Screwdrivers
* Drill and drill bits
* Wire strippers
* Soldering iron and solder
* Paper towels
* Window cleaner

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
<img src="../../img/maiv/maiv_surgery.jpg" alt="Omnibot 2000 taken apart." title="Omnibot 2000 taken apart." style="max-width: 250px;" />
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

You will wire the left and right motors to a motor controller and our board - this will allow your Omnibot to be controlled with Viam as a [wheeled base](/components/base/wheeled/).
The front motor allows you to change from high to low gear.
You can wire this motor later, but for now if you want to shift the gear, you can do so manually with the gearbox cover off.

#### Wire MAIV's base motors to the motor driver

We have now reached the part of the tutorial where we will begin to actually modify the robot.
If the thought of anything other than restoring an Omnibot 2000 to its original working condition makes you sad, we understand.
But first, remember it was in someone's attic gathering dust for years.
Second, we will re-use the motors and gears and leave the original circuit boards in-place (albeit no longer used).
It's a [restomod](https://www.goldeagle.com/tips-tools/what-is-a-restomod/)!

First, detach the left and right base motor's wires from the small printed circuit board.
Orient the L298N so that the `OUT1` and `OUT2` terminals are on the left side.
Using a screwdriver, attach the 2 wires from the left motor to the `OUT1` and `OUT2` terminals.
Now, attach the 2 wires from the right motor to the `OUT3` and `OUT4` terminals.

[TODO: need wiring diagram here]

Ensure your Raspberry Pi powered off, and connect GPIO pins for the left motor with female-to-female jumper wires.
You can use any GPIO pins, but we connected pin 32 to `IN1`, pin 38 to `IN2`, and pin 35 to `ENA`.
Now, do the same for the right motor, connecting pin 31 to `IN3`, pin 36 to `IN4` and pin 22 to `ENB`.
Cut off one end of a jumper wire, strip it and connect pin 34 (ground) to the common ground terminal `GND` on the L298N.

#### Supply power to the motors and Raspberry Pi

### Base configuration
