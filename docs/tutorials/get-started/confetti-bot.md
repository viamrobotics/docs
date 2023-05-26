---
title: "Build a Confetti Bot with a Raspberry Pi"
linkTitle: "Build a Confetti Bot"
weight: 50
type: "docs"
description: "Using a red button and Python SDK to activate a GPIO pin on the board and make a confetti popper go off."
tags: ["raspberry pi", "python", "app", "board", "motor"]
webmSrc: "/tutorials/img/confetti-bot/preview.webm"
videoAlt: "A GIF of a red button being pressed and the cannon spraying confetti"
images: ["/tutorials/img/confetti-bot/preview.gif"]
# Author: Hazal Mestci
# SME: Fahmina A
---

Are you tired of boring celebrations with the same old confetti popping techniques?
Fear not, my friend!
You can now design your very own confetti-popping robot with a big red button that will make your parties a colorful blast, literally!
With this robot, you'll become the life of the party with just one press of a button.
Whether it's a birthday party, a wedding, a company launch, or just a random Wednesday night, this robot will add an extra dimension of fun and excitement to any event.

In this tutorial, we will show you how to build your very own confetti bot using Viam.
This robot turns a motor when you press a button, which then sets off a confetti cannon and makes it rain confetti.

This project is a great place to start if you are looking to move a motor based on a button press.
You can expand on this project to turn a motor based on other types of inputs, such as when a specific sensor goes high.

![GIF of a red button being pressed and the cannon spraying confetti](/tutorials/img/confetti-bot/preview.webm)

## Requirements

### Hardware

* A macOS or Linux computer
* A [Raspberry Pi](https://a.co/d/bxEdcAT), with a [microSD card](https://www.amazon.com/Lexar-Micro-microSDHC-Memory-Adapter/dp/B08XQ7NGG1/ref=sr_1_13?crid=2MYQRKA7TX2KM&keywords=microsd%2Bcard%2Bwith%2Badaptor&qid=1682364645&sprefix=microsd%2Bcard%2Bwith%2Badaptor%2Caps%2C79&sr=8-13&th=1), setup per [these instructions](https://docs.viam.com/installation/prepare/rpi-setup/).
You may need an adaptor depending on your computer model.
* A big button, like [this one](https://www.amazon.com/EG-STARTS-Buttons-Illuminated-Machine/dp/B01LZMANZ7/ref=sxts_b2b_sx_reorder_acb_business?content-id=amzn1.sym.44ecadb3-1930-4ae5-8e7f-c0670e7d86ce%3Aamzn1.sym.44ecadb3-1930-4ae5-8e7f-c0670e7d86ce&crid=14C1UV9WJPU5A&cv_ct_cx=big+dome+push+button+12v&keywords=big+dome+push+button+12v&pd_rd_i=B01LZMANZ7&pd_rd_r=86ae5517-579e-43f9-a445-1289fb0bb628&pd_rd_w=GD1Uv&pd_rd_wg=lMOgX&pf_rd_p=44ecadb3-1930-4ae5-8e7f-c0670e7d86ce&pf_rd_r=VMN1H6MB507W0RJFED5Q&qid=1684785044&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=big+dome+push+button+12v%2Caps%2C90&sr=1-1-62d64017-76a9-4f2a-8002-d7ec97456eea).
Check the wiring diagram for the specific model you have as you wire the button.
* A mini confetti cannon, like [this one](https://www.amazon.com/Confetti-Poppers-Party-Accessory-Pack/dp/B074SP7FZH/ref=sr_1_4?crid=2WYP33LTAP50H&keywords=amscan+mini+confetti+poppers&qid=1684790215&sprefix=amscan+mini+confetti+poppers%2Caps%2C76&sr=8-4)
* Any gpio motor, like the [Bemonoc 25GA370 DC Encoder Metal Gearmotor 12V](https://www.amazon.com/25GA370-Encoder-Metal-Gearmotor-150RPM/dp/B07GNFYGYQ/ref=asc_df_B07GNFYGYQ/?tag=hyprod-20&linkCode=df0&hvadid=344005018279&hvpos=&hvnetw=g&hvrand=12675870996853783399&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9060354&hvtargid=pla-695812063602&psc=1&tag=&ref=&adgrpid=69357499415&hvpone=&hvptwo=&hvadid=344005018279&hvpos=&hvnetw=g&hvrand=12675870996853783399&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9060354&hvtargid=pla-695812063602).
The STL files for 3D printing is according to the sizing of this motor, but you can update the design depending on the model you have.
* A [L298N Motor Driver](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/ref=sr_1_6?)
* A [12V battery](https://www.amazon.com/ExpertPower-EXP1270-Rechargeable-Lead-Battery/dp/B003S1RQ2S/ref=sr_1_4?crid=FGUVJZV13VF7&keywords=expert+power+12v+battery&qid=1682365772&sprefix=expert+power+%2Caps%2C122&sr=8-4) with a [charger](https://www.amazon.com/dp/B0BC3Y5N3Q/ref=vp_d_pd_b2b_qd_vp_pd?_encoding=UTF8&pf_rd_p=18ac4947-fc02-409d-a460-4117e58667a4&pf_rd_r=GG6532H6SF32SEC3EZKA&pd_rd_wg=6Boz9&pd_rd_i=B0BC3Y5N3Q&pd_rd_w=u2uS7&content-id=amzn1.sym.18ac4947-fc02-409d-a460-4117e58667a4&pd_rd_r=3bf79f54-e36d-4bcc-967c-2acae5e7e98d)
* Jumper wires
* Alligator clips
* M2.5 x 16mm screws and M2.5 nuts
* A 2.4mm screwdriver
* Optional: a 3D printer and laser cutter (for the enclosure)

### Software

* [Python3](https://www.python.org/download/releases/3.0/)
* [Pip](https://pip.pypa.io/en/stable/#)
* [viam-server](https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b), installed with [these instructions](https://docs.viam.com/installation/#install-viam-server)
* [Viam Python SDK](https://python.viam.dev/)

## Set up your hardware

### 3D Print the enclosure

3D print the enclosure using these STL files.
If you are using a different confetti cannon, adjust the size of the 3D prints to your confetti cannon size, the wall thickness of the holder changes between brands.
The same applies for the motor, if you are using a different model, you can adjust the size for the motor so the holder fits your motor head.

You can either laser cut or 3D print the side panels depending on your liking, and which machine you have access to.

### Wire your motor, motor driver, board and the battery

First, attach your motor with screws to the middle of the enclosure. Attaching the motor first makes wiring the rest easier.

Because of the model we have, we only used two screws for the top, but some motors require four which is why the enclosure has four holes.

![The motor shown next to the enclosure before being installed.](/tutorials/img/confetti-bot/install-motor-before.jpg)

![The motor being installed inside the enclosure with screws on top.](/tutorials/img/confetti-bot/install-motor-after.jpg)

Now wire all of the components according to the wiring diagram:

{{< alert title="Info" color="info" >}}
Wiring diagram forthcoming.
{{< /alert >}}

1. Connect your motor to the motor driver.
There are several wires coming out of the motor, connect the black one (ground) into `Out1` terminal and the red one (power) to `Out2` terminal and screw them in tightly (a 2.4mm screwdriver works well for this).
After you have finished screwing the block down, make sure it is secure by gently tugging on the wire.
If it is not secure, the wire will come out.
You can leave the other wires disconnected.

2. Connect your Raspberry Pi to the motor driver.
Since you are using `Out1` and `Out2` on the driver, you need to use the corresponding inputs (In1 and In2), as well as a PWM pin.
Select three available [GPIO pins](https://pinout.xyz/pinout/wiringpi) on the Raspberry Pi and connect them to the `ENA` (green wire in the wiring diagram), `In1` (yellow wire in the wiring diagram), and `In2` (orange wire in the wiring diagram) pins on the motor controller.
Take the black safety cap out from the motor driver so you can use the ENA pin.
Make sure to remember which GPIO pin on the Raspberry Pi you connected to each of these inputs.
In our case, we connected Pin 11, 13, and 15 respectively.

3. Connect your button to the Raspberry Pi. One of the connections go to a 3.3V pin on the Raspberry Pi, and the other needs to be connected to a GPIO pin.
We used Pin 1 for 3.3V (blue wire in wiring diagram).
Make sure to record which GPIO pin you connect to since you will be using this in your robot configuration.
We used Pin 37 (white wire in wiring diagram).
4. Now you can connect the button to your 12V battery, use a black alligator clip to connect the ground of the button switch to the ground of the battery.
Then from the same ground of the battery, use a black wire to connect to the ground pin on the motor driver.
The ground of the motor driver will be shared with the Raspberry Pi, and your battery.
Find a ground pin on your Raspberry Pi and connect it to the ground pin on the motor driver, allowing two pins to share the ground.
Screw them tight with a screwdriver.
We used Pin 6 on the Raspberry Pi as our ground pin, but you can use any [Raspberry Pi ground pin](https://pinout.xyz/pinout/ground).
5. Now that you have grounded your robot, you can connect the motors to power.
Use a red alligator clip to connect the battery to the button switch, and another red alligator clip to connect the battery to the 12V input on the motor driver.
6. Your robot wiring is now complete! Put the microSD card in the Raspberry Pi and turn it on by plugging it to the wall.

![Closeup photo of the motor driver after all the wiring to the motor, the board and the battery.](/tutorials/img/confetti-bot/wired-motor-driver.jpg)

![Motor, motor driver, board and battery all wired to each other.](/tutorials/img/confetti-bot/wired-all-components.jpg)

## Configure your confetti bot with the Viam app

Now that your robot is wired, you need to configure it on the Viam app before you can program it.

In the Viam app, create a new robot and give it a name.
We named ours ConfettiBot.

![A robot page header in the Viam app, its under the location work, and named ConfettiBot.](/tutorials/img/confetti-bot/app-name-confettibot.png)

Then navigate to the robot’s **CONFIG** tab to start configuring your components.

### Configure the Pi as a board

Add your [board](https://docs.viam.com/components/board/) with the name `party`, type `board` and model `pi`.
Click **Create Component**.

![Create component panel, with the name attribute filled as party, type attribute filled as board and model attribute filled as pi.](/tutorials/img/confetti-bot/app-board-create.png)

You can name your board whatever you want as long as you refer to it the same way in your code, we picked `party` for fun. Your board configuration should now look like this:

![Board component configured in the Viam app, the component tab is named party, with a type attribute board and model attribute pi.](/tutorials/img/confetti-bot/app-board-attribute.png)

### Configure the motor

Add your [motor](https://docs.viam.com/components/motor/) with the name “start”, type `motor`, and model `gpio`.
Again, we named it “start” to refer to the button being pressed, but this name is up to you as long as you remember the name and use the same name in the code later.

![Create component panel, with the name attribute filled as start, type attribute filled as motor and model attribute filled as gpio.](/tutorials/img/confetti-bot/app-motor-create.png)

After clicking **Create Component**, there is a pin assignment type toggle.
Click **In1/In2** since that is compatible with the type of input our motor controller expects.
In the drop downs for A/In1 and B/In2, choose `13 GPIO 27` and `15 GPIO 22` and for PWM choose `11 GPIO 17` corresponding to our wiring.

In the **Board** drop-down within attributes, choose the name of the board the motor controller is wired to (“party”).
This will ensure that the board initializes before the motor driver when the robot boots up.

![Motor component configured in the Viam app, the component tab is named start, with a type attribute motor and model attribute gpio. It has the attributes as of the board as party, encoder as non-encoded, max rpm as 1000, component pin assignment type as In1/In2, enable pins as neither, a/In1 as 13 GPIO 27, b/In2 as 15 GPIO 22, pwm as 11 GPIO 17.](/tutorials/img/confetti-bot/app-motor-attribute.png)

Click **SAVE CONFIG** at the bottom of the screen.

Now that your robot is configured in the Viam app, let’s test our configuration from the Control tab.
Go to board panel, set pin 37 as high, and your motor should turn.

## Attach components to the enclosure

Now that you tested your motor in the app and confirmed everything works, let’s finish assembling your confetti bot.

1. Attach the motor driver to the enclosure wall with four M2.5 x 16mm screws and M2.5 nuts.

![Back view of the motor driver being installed inside the 3D printed enclosure with screws.](/tutorials/img/confetti-bot/install-driver-1.jpg)

![Front view of the motor driver being installed inside the 3D printed enclosure with screws.](/tutorials/img/confetti-bot/install-driver-2.jpg)

2. Slip the Raspberry Pi into the designated slot in the enclosure.
Be careful of the wires during this so they don’t pop off.

![Back view of the Raspberry Pi being installed inside the 3D printed enclosure within the designated slot.](/tutorials/img/confetti-bot/install-pi-1.jpg)

![Front view of the Raspberry Pi being installed inside the 3D printed enclosure within the designated slot.](/tutorials/img/confetti-bot/install-pi-2.jpg)

3. Add the confetti cannon to the enclosure by tightening the 3D printed holder around the confetti socket using one M2.5 x 16mm screw and a M2.5 nut.
Then connect this piece with the front panel.

![Front photo of the confetti cannon attached to the 3D printed parts.](/tutorials/img/confetti-bot/install-cannon-front.jpg)

![Side photo of the confetti cannon attached to the 3D printed parts.](/tutorials/img/confetti-bot/install-cannon-side.jpg)

4. Now we have to attach the other circle holder (the one that attaches to the motor head) on the base of the confetti cannon to hold its place, then the motor and secure with a screw from the side.
Depending on your motor size, the screw size may change.

![The 3D printed black piece attached to motor with a screw securing it in place over the motor head.](/tutorials/img/confetti-bot/install-motor-holder.jpg)

![Motor attachment with a 3D printed black piece wrapped around the confetti cannon secured over the motor head.](/tutorials/img/confetti-bot/install-cannon-holder.jpg)

![Motor attachment with a 3D printed black piece wrapped around the confetti cannon secured over the motor head attached to the enclosure.](/tutorials/img/confetti-bot/install-cannon-enclosure.jpg)

5. Add the front section you just built to the rest of the enclosure using M2.5 x 16mm screws and M2.5 nuts.
Make sure to do this step before closing the side walls to be able to access the slots for screws.

![Side view photo of the front section attached to the rest of the enclosure.](/tutorials/img/confetti-bot/install-front-enclosure.jpg)

### Optional: Laser cut or print the sides

Laser cut the sides of the enclosure and attach with screws. You can find the designs here:

If you don’t have a laser cutter, you can 3D print the sides instead, or leave them empty.

![Lasercut side attached to the enclosure, with few cables going out of the enclosure.](/tutorials/img/confetti-bot/install-lasercut-side.jpg)

### Final design

The final design, fully wired and put together looks like this:

![Top view of the final assembly of the confetti cannon and 3D printed/laser cutted pieces, with a battery and a red button on a white table.](/tutorials/img/confetti-bot/final-assembly-top.jpg)

![Side view of the final assembly of the confetti cannon and 3D printed/laser cutted pieces, with a battery and a red button on a white table.](/tutorials/img/confetti-bot/final-assembly-side.jpg)

## Write Python code to control the confetti bot

Navigate to the **CODE SAMPLE** tab on the Viam app, select language as Python, and scroll down to click the **Copy Code** button.
Paste this into a new Python file in your favorite code editor to connect to your robot.

On top of the code, you will see your board and motor components are getting imported from Viam.

```python
from viam.components.board import Board
from viam.components.motor import Motor
```

In your main function, it will populate “party” which is our board and “start” which is our motor.

```python
   party = Board.from_robot(robot, "party")
  # Note that the pin supplied is a placeholder. Please change this to a valid pin you are using.
   party_return_value = await party.gpio_pin_by_name("37")
   print(f"party gpio_pin_by_name return value: {party_return_value.get()}")

   start = Motor.from_robot(robot, "start")
   start_return_value = await start.is_moving()
   print(f"start is_moving return value: {start_return_value}")
```

The only code you need to add to your main function is a while loop to check if the button is being pressed.
Copy this code and add it to your own code within the main function block.

```python
 while True:
       print(party_return_value.get())
       while (await party_return_value.get()) == True:
           await start.set_power(.8)
           await asyncio.sleep(0.1)
           if (await GPIO.get()) == False:
               break
       await start.set_power(0)
```

This is all the code you need to activate the gpio pin and turn the confetti cannon that is attached to your motor!

The completed code for this project can be found [here](https://github.com/viam-labs/devrel-demos/tree/main/confetti_bot).
If you copy the code from this link, don’t forget to change your robot address and secret so it connects to your own confetti robot.

## Next steps

In this tutorial, you learned how to turn a motor on when a button is pressed, and set off a confetti cannon utilizing the button input using Viam.
You could use this same concept for any simple robot that involves turning a motor when a pin on the Raspberry Pi goes “high.”
One example of this logic would be connecting a PIR sensor to a Raspberry Pi.
You could then make a motor turn whenever you sense a person walking by.

* For more robotics projects, check out our [other tutorials](/tutorials/).
