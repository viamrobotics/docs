---
title: "Build an outdoor rover: simple, useful and affordable"
linkTitle: "Outdoor Rover"
type: "docs"
tags: ["base", "outdoor", "solar", "rover"]
description: "Build and control an affordable, functional outdoor rover (choose 3)."
image: "/tutorials/outdoor-rover-boxbot/completed-rover.jpg"
images: ["/tutorials/outdoor-rover-boxbot/completed-rover.jpg"]
aliases: /tutorials/build-an-outdoor-rover/
imageAlt: "Rover with mounted solar panel."
authors: ["Matt Vella"]
languages: []
viamresources: ["board", "motor", "base", "camera"]
level: "Intermediate"
date: "2023-03-29"
# updated: ""
cost: 420
no_list: true
---

Approaching robotics can be daunting.
Many of us who have tried have ended up with empty wallets, life to catch up on, and spare parts in our closets.
Some of us have had some success starting with robotic kits or learning robots.
You know - the ones that are fairly easy to get up and running, but ultimately are expensive toys?
In my humble opinion, these robots are somewhat missing the point: people want to create robots _that_ _do real things, that solve real-life problems_.
What to do?
Well, you _can_ certainly purchase a very capable outdoor robotic rover for upwards of 12 thousand dollars.
It will still be hard to learn how to expand and program it, but it's at least capable, right?

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/9OzwozzckdY">}}

Fortunately I work at Viam, where we are building a platform that makes robotics and robotic automation approachable, and therefore much easier to build useful robots.
Now, when I am an employee at _any_ company one of the most important things is that I truly believe in the product.
Therefore, I challenged myself with the following proof: _"Can I build a weatherproof, outdoor rover that is capable of doing useful things for under $500?"_

**Good news: the answer is yes, and it can be done in less than a day.**

## Overall Boxbot design

The success of this project was based on two key factors:

1. Hoverboard hub motors are sealed and waterproof, can carry a good payload, are capable of navigating outdoor terrain like gravel and grass, and are somewhat readily available.

2. Pelican-style plastic boxes are not only able to protect your electronics against the elements, but are also sturdy enough for hub motors to be directly bolted on, and able to carry additional payload on top.

Regardless of what future tasks you might have in mind for your outdoor robotic base, these parts are required for this design.
Other advantages of using a case of this type is that you can easily open and close it to make adjustments, and you can conveniently carry the entire robot with the case's handle.

## Parts list for your Boxbot

Some of the equipment listed here is optional.
For example, you might not need a night-vision camera if you won't operate it at night and you will not need a solar panel and charge controller if you plan on using your rover occasionally and charging it in-between.

<!-- prettier-ignore -->
|Part | Quantity | Price (each) | Price total | Notes |
| --- | --- | --- | --- | --- |
| [Weatherproof plastic case](https://www.alibaba.com/product-detail/Waterproof-Foam-Pu-eva-epe-xpe_1600097495864.html) | 1 | $30.50 | $30.50 | This is the key to protecting your electronics and holding the robot together. Make sure it is a thick, strong plastic and can fit the solar panel mounted on top. Finally, get one with adjustable foam inside - this is very handy for cushioning your electronic components.|
| [Night vision camera](https://www.amazon.com/gp/product/B07C1N9R4Z)|1|$40|$40|Night vision is optional, but a webcam of some sort is highly recommended.|
| Raspberry Pi 3B or 4B with microSD card|1|$100|$100|Note: Due to supply shortages, Raspberry Pi prices are fluctuating dramatically.|
| [12V Battery](https://www.amazon.com/LiFePO4-Battery-Miady-Rechargeable-Maintenance-Free/dp/B089VXSBC6)|1|$65|$65|Lots of options here - some motors might run better on 24V. You can use a battery with less storage if you don't plan to run it continuously.|
| [Brushless hub motor wheels](https://www.alibaba.com/product-detail/Electric-Wheel-Hoverboard-DC-Hub-6_60615157026.html)|2|$30|$60|Better yet - source them from a used [hoverboard](https://www.amazon.com/RIDE-SWFT-Hoverboard-Balancing-Front-Facing/dp/B08N5DSVY3) (this is what I did, sorry son).|
|[USB Gmouse GPS module](https://www.amazon.com/Navigation-External-Receiver-Raspberry-Geekstory/dp/B078Y52FGQ)|1|$20|$20|optional|
|[Solar charge controller](https://www.amazon.com/Renogy-Wanderer-Amp-12V-24V/dp/B07NPDWZJ7)|1|$20|$20|optional|
|[25w Solar panel](https://www.alibaba.com/product-detail/High-Efficiency-25W-Polycrystalline-Crystalline-Solar_60814369754.html)|1|$10|$10|optional|
[12V to 5V DC USB Type-C Right Angle Step-Down Power Converter](https://www.amazon.com/gp/product/B086KTGRH1/)|1|$13.50|$13.50|To power the Pi from a 12V battery.|
|[Brushless motor controller](https://www.amazon.com/RioRand-6-60V-Brushless-Electric-Controller/dp/B087M2378D)|2|$18|$36|
|[Caster wheel](https://www.harborfreight.com/3-inch-x-3-4-quarter-inch-stem-swivel-caster-90997.html)|2|$5|$10|
|Galvanized nuts/bolts, water sealing epoxy or caulk, washers, misc wires, brackets, etc|1|$15|$15|Bolts are for mounting your hub motors and other components. I used a bracket I had lying in my basement plus some brackets/rails from my kids' erector set to mount the solar panel.|
|**TOTAL**|-|-|$420|

You'll also need some basic tools:

- Screwdrivers
- Drill
- Drill bits
- Socket or combination wrenches
- Hack saw
- Soldering iron and solder

## Build the base of your Boxbot

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/outdoor-rover-boxbot/cut-wheel-brackets.png" resize="300x" declaredimensions=true alt="Use a hacksaw to cut the wheel brackets." class="alignright" style="max-width: 200px">}}
</div>
Hoverboard motors that come out of a toy hoverboard usually have large metal mounting brackets attached to them.
This makes it much easier for you to attach them to the plastic case, and distributes the torque of the motors across more of the plastic case bottom, making the design more durable.
However, I faced a problem that likely you will face as well: the brackets won't mount flat and flush against the bottom of the case unless you cut part of them off that is rounded.
For this, I used a hacksaw.
Hard work, but someone's gotta do it.

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/outdoor-rover-boxbot/caster-wheels.png" resize="300x" declaredimensions=true alt="Mounted caster wheels." class="alignleft" style="max-width: 200px">}}
</div>

Next, you'll mount the caster wheels to the "front" of the box (meaning what _will be_ the front of the robot, which in reality is the left or right side of the box when facing the side of the box with the handle), and the hub motors to the rear, trying to ensure that the hub motor wheels are parallel to each other, and are not too close to the sides of the case.
The caster wheels I bought had bolts attached, so I simply drilled holes through the bottom of the case, pushed them through, added washers and tightened the nuts securely.

For the hub motor mounts, drill two holes through each mount, line each one up, then drill through these holes into the bottom of the plastic case.
While doing this I realized that I'd also want to run the wires from the hub motor into the case under the mount (to better protect the wires), so I drilled a smaller hole under where each of the mounts would be for that purpose.

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/outdoor-rover-boxbot/mounted-hub-motor.png" resize="300x" declaredimensions=true alt="Mounted hub motor." class="alignright" style="max-width: 250px">}}
</div>

At this point, I want to mention that although the case is intrinsically waterproof, we'll want to make sure that we waterproof any holes that we make in the case.
For this, I used marine epoxy from the hardware store, surrounding where the bolts went through the case.
You can do the same where you pass the wires into the case; for added strength you can also use [wire pass-throughs](https://www.amazon.com/Black-Plastic-Waterproof-Cable-Connectors/dp/B0081DDUW8).

To attach the hub motors, use galvanized carriage bolts with washers inserted from the inside of the case out to the bottom, then put the bolts through the mounts, add washers and nuts and tighten securely.
The bolts I had were _way_ too long, so I had to remove the excess length with the hacksaw - you can avoid this by getting the correct length from the beginning - just measure the depth of the mount plus the case thickness, plus some excess for the washer and securing the nut!

At this point, you should have a not-yet-powered but assembled wheeled base!

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/outdoor-rover-boxbot/unpowered-base.jpg" resize="300x" declaredimensions=true alt="Assembled base, not yet powered." class="alignleft" style="max-width: 250px">}}
</div>
Try pushing your base around, but don't be too sad if it doesn't go perfectly straight; caster wheels don't exactly lend themselves to that (especially when not faced with constant forward force; you know this if you've ever let go of your shopping cart in the grocery store in the middle of a push).

If you're feeling brave, try sitting on it (carefully!) to see if it can support your weight.
This will depend wildly on your weight and the strength of the case you purchased; if you are worried you could try putting something else less heavy on top like a couple cinder blocks or barbells.

Now could be a good time to attach a camera in a similar way to how you attached the wheels, but through the top of the case.
Don't forget that wherever you decide to feed the camera wire into the case, you'll want to be sure you leave enough slack to open and close the case.
I found that the rover handles much better with the hub motors in the back, acting as rear-wheel drive.
If you are not sure if that's how you'll want to run yours, wait until after you've tested how it handles, and then mount a camera.

## Wire it up

OK, I'll be honest.
I wanted to add an exclamation point here to motivate us - because in reality, this is the hardest part of the project.
Specifically, setting up the motor controllers correctly is a bit of a challenge but I will do my best to describe how to best navigate them here.

### Brushless motor controllers

Be sure to buy motor controllers that are built specifically for brushless motors.
This is imperative because brushless DC motors (BLDC for short) have a tradeoff: while they and their controllers are more expensive and complicated to set up, they are more reliable and durable.
Brushless motors do not rely on mechanical brushes that are prone to wear; instead they require an electronic communicator in the form of a more expensive and complex motor controller.

Let's get to it.
Note that all of the steps in this section will need to be done twice, as we will be controlling two motors (one on each side of the base).
The procedure for each side will look like:

1. Solder motor controller
2. Wire the hub motor to the motor controller
3. Wire the battery to the motor controller
4. Test controlling the motor with the motor controller potentiometer
5. Wire to the Raspberry Pi

With the brushless motor controllers I used, you'll have to first solder a jumper where indicated in this diagram (label starts with "normally disconnected").
This allows the pi to control the motor with PWM.
You'll also need to solder two pins to the controller just to the left of the white wire harness mount.
(P.S. - A truly clutch solder tip for those of you who may not be very experienced with soldering: **heat the pin** with the soldering iron, **not the solder itself**!
Once the pin is hot, touch the solder to it.
When someone taught me this it changed my life.)

<div class="td-max-width-on-larger-screens" style="max-width: 500px">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/motor-controller.jpg" resize="600x" declaredimensions=true alt="Brushless motor controller" class="alignleft">}}
</div>

You'll then connect the motor phase A, B, and C wires from your hub motor to the left side of the controller, and the 5 hall sensor wires to the white wire harness on the bottom right.
It is also worth mentioning that you may need to extend the wires from your hub motors if they are not long enough to work with.
Likely, the color of the wires from your hub motor will match the diagram - at the very least the 5V and GND should.
If any of the phase wire colors don't match, you might need to swap them when testing with the potentiometer.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/wiring-diagram.png" resize="1000x" declaredimensions=true alt="Full wiring diagram.">}}
</div>

Next, add wires to the VCC and ground terminals below the motor phase wires - this will supply power to your motor.
You might find it easiest to use [battery clamps](https://www.amazon.com/Insulated-Alligator-Durable-Battery-Electric/dp/B08T1K4774) to attach these wires to your battery.

{{% alert title="Caution" color="caution" %}}
Be sure your base is on its side or otherwise supported so the wheels are free-spinning before attaching the battery!

Otherwise you might have a half-built rover flying and crashing off of your desk/workspace - this could be bad.
{{% /alert %}}

If everything is now wired up and lifted, attaching the battery and turning the potentiometer with a screwdriver should power the motor and the wheel should spin.
When you're done having fun with that, crank it back down until the motor is fully deactivated.

### Organize the wires and components

Now might be the time to figure out where you're laying everything out inside your case.
You'll need a space for:

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/outdoor-rover-boxbot/case-layout.jpg" resize="500x" declaredimensions=true alt="Brushless motor controller." class="alignright" style="max-width: 400px">}}
</div>

- Your already wired motor controllers
- Your battery
- Your Pi
- Your solar charge controller, if you're going to use solar charging

As mentioned, having a case that comes with foam that can be easily cut/shaped is very helpful.
Make a cutout for each of your components, considering how you are going to run your wires.
You don't need to match my layout pictured here, in fact it could certainly be better organized.

### Connect the motor controllers to the Pi

Once that's sorted out, we're ready to connect 3 wires from the motor controller to the Pi (you'll probably need a [Pi pinout diagram](https://pinout.xyz) handy):

1. One from the pin you added labeled **G** to any GND terminal on the Pi
2. One from the pin you added labeled **P** to any available GPIO pin on the Pi
3. One from terminal labeled **DIRExternal potentiometer** to any available GPIO pin on the Pi

Finally, you'll want to connect the wires from the 12V to the 5V Pi power converter to the battery.

At this point, you can plug in any extra components to the Pi (GPS and camera, if you are using them).
If they are USB-based (like ones in the parts list), this is straightforward.

## Bring your robot to life

### Viam config overview

We've now got all the hardware and wiring set up, so it is time to configure your robot to be controlled with software.
You might be bracing yourself, as this part is usually much harder than what you just did.
However, the Viam platform makes it relatively painless.

First, let's install [viam-server](/get-started/installation/prepare/rpi-setup/) on your Pi.
It should only take a few minutes and once you're done, you are ready to configure your robot.

The Viam platform represents both individual hardware pieces and logical groupings of hardware as [components](/components/).
Higher-level control is surfaced with [services](/services/).
For this project, we'll configure:

- One [board](/components/board/) component representing our Raspberry Pi
- Two [motor](/components/motor/) components
- One [base](/components/base/) component, referencing the two motors that make up the base

Configuring these components will allow you to control your rover through the internet both manually and programmatically.
Later, we can do more interesting things by configuring:

- A [camera](/components/camera/) component (optional but recommended)
- A [movement sensor](/components/movement-sensor/) component, which in this case represents GPS (optional)
- A [vision](/ml/vision/) service, which allows us to use machine learning models to detect various things in the robot environment

### Setting up our Boxbot config using the Viam app

#### Board component

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/board-setup.png" resize="1000x" declaredimensions=true alt="Board setup.">}}
</div>

In the [Viam app](http://app.viam.com/), navigate to **Config** within the robot you created previously, and add a new component of type "board", model "pi".
You can name it whatever you want, but you'll reference this name later.
We'll call it "local" in this example.

#### Motor component

Next, create another component of type "motor", model "gpio".
Call it "left" to represent the motor on the left side of your rover.
Now we'll need to add some attributes.
We'll need to reference the board component we created in the last step by name, and the GPIO pins we connected from this motor to our Pi.
Other attributes (Max RPM, PWM Freq) are [important for motor control](/components/motor/gpio/#brushless-dc-motor) (Note that these might vary based on your specific hub motors, check the data sheet if you have one; or you can try the ones we use in this tutorial).
Once you've configured the "left" motor, repeat for the "right" - make sure you're mapping the correct GPIO pins for each.
Finally, one of the two motors we are connecting will need the "Direction Flip" attribute set to "true".
It's ok if you are not sure which one, you can always switch them later after testing.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/motor-setup.png" resize="1000x" declaredimensions=true alt="Motor setup.">}}
</div>

At this point, you can try controlling your motors with the Viam App.
Navigate to the **Control** tab.
If all is set up correctly, you'll see cards for your left and right motors on this page.
Open one up, and if your rover is in a safe position (on the ground or propped up), try running one!

{{% alert title="Caution" color="caution" %}}
Be aware that these are powerful motors, so you don't want to start at 100% power right away.
{{% /alert %}}

If the motors don't appear on the control page, or are not running when expected, first check the **Logs** tab to see if you see any errors - which would likely point out a bad configuration (a typo, a misplaced or missing attribute, etc).
If not, double check your wiring and how it maps to the GPIO pins you've configured.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/motor-control.png" resize="1000x" declaredimensions=true alt="Motor control.">}}
</div>

#### Base component

Now, let's configure a "base" component that references both of our motors.
This will allow us to control our robot's movement through a single interface.
Add a new component of type "base", model "wheeled" - which represents a wheeled base with two powered wheels.
The "left" and "right" attributes reference the motors you've configured by name.
You can measure your wheel's circumference and width between wheels, which will allow the Viam platform to properly calculate how to steer your base.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/base-setup.png" resize="1000x" declaredimensions=true alt="Base setup.">}}
</div>

## Take your Boxbot for a drive

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/outdoor-rover-boxbot/completed-rover.jpg" resize="400x" declaredimensions=true alt="Completed rover with mounted solar panel." style="max-width: 350px" >}}
</div>

You can now have some real fun.
Try driving your rover by keyboard.
Drive your [robot programmatically](/tutorials/get-started/try-viam-sdk/), use a [color detector](/tutorials/services/try-viam-color-detection/) or a [machine learning object detector](/ml/vision/detection/) to interact with the environment.
Check out our [Python SDK documentation](https://python.viam.dev/) (or another SDK in the language of your choice) and start planning how you'll use your sturdy outdoor rover to do real things!
Or, expand what your outdoor rover can do by adding a [camera](/components/camera/), [movement sensor](/components/movement-sensor/), or other [component](/components/).

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/outdoor-rover-boxbot/matt-done.png" resize="300x" declaredimensions=true alt="Matt working on project." class="alignleft" style="max-width: 250px">}}
</div>

I had a lot of fun building this rover, and hope you did as well.
I am now programming mine to help keep unwanted animals away from my garden, garbage, and egg-laying ducks using Viam's data management, vision, and navigation services.
We are interested in hearing what you plan on doing with yours.
You can tell us all about it over in the [Viam Community Discord](https://discord.gg/viam).
