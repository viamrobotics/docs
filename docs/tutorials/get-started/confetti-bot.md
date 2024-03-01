---
title: "Build a Confetti Bot with a Raspberry Pi"
linkTitle: "Confetti Bot"
type: "docs"
description: "Use a red button to activate a GPIO pin on the board and make a confetti popper go off."
tags: ["raspberry pi", "python", "app", "board", "motor"]
videos:
  [
    "/tutorials/confetti-bot/confetti-bot-explodes.webm",
    "/tutorials/confetti-bot/confetti-bot-explodes.mp4",
  ]
videoAlt: "A GIF of a red button being pressed and the cannon spraying confetti"
images: ["/tutorials/confetti-bot/confetti-bot-explodes.gif"]
authors: ["Hazal Mestci"]
languages: ["python"]
viamresources: ["board", "motor"]
level: "Beginner"
date: "2023-05-29"
# updated: ""
cost: 145
---

{{<gif webm_src="/tutorials/confetti-bot/confetti-bot-explodes.webm" mp4_src="/tutorials/confetti-bot/confetti-bot-explodes.mp4" alt="GIF of red button being pressed and cannon of confetti bot spraying confetti" class="alignright" max-width="275px">}}

Are you tired of boring celebrations with the same old confetti popping techniques?
You can now design your very own confetti-popping robot with a big red button that will make your parties a colorful blast, literally!
With this robot, you'll become the life of the party with just one press of a button.
Whether it's a birthday party, a wedding, a company launch, or just a random Wednesday night, this robot will add an extra dimension of fun and excitement to any event.

In this tutorial, you'll learn how to build your very own confetti bot using Viam.
This robot turns a motor when you press a button, which then sets off a confetti cannon and makes it rain confetti.

You can expand on this project to turn a motor based on other types of inputs, such as when a specific sensor goes high.

## Requirements

### Hardware

- A macOS or Linux computer
- A [Raspberry Pi](https://a.co/d/bxEdcAT), with a [microSD card](https://www.amazon.com/Lexar-Micro-microSDHC-Memory-Adapter/dp/B08XQ7NGG1/ref=sr_1_13), set up using [these instructions](/get-started/installation/prepare/rpi-setup/).
- A big button, like [this one](https://www.amazon.com/EG-STARTS-Buttons-Illuminated-Machine/dp/B01LZMANZ7/ref=sxts_b2b_sx_reorder_acb_business).
  Check the wiring diagram for the specific model you have as you wire the button.
- A mini confetti cannon, like [this one](https://www.amazon.com/Confetti-Poppers-Party-Accessory-Pack/dp/B074SP7FZH/ref=sr_1_4)
- A gpio motor. We used the [Bemonoc 25GA370 DC Encoder Metal Gearmotor 12V](https://www.amazon.com/25GA370-Encoder-Metal-Gearmotor-150RPM/dp/B07GNFYGYQ/ref=asc_df_B07GNFYGYQ/).
  The STL files we use for 3D printing are adapted to the size of this motor, but you can update the design depending on the model you have.
- A [L298N Motor Driver](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/ref=sr_1_6)
- A [12V battery](https://www.amazon.com/ExpertPower-EXP1270-Rechargeable-Lead-Battery/dp/B003S1RQ2S/ref=sr_1_4) with a [charger](https://www.amazon.com/dp/B0BC3Y5N3Q/ref=vp_d_pd_b2b_qd_vp_pd)
- Jumper wires
- Alligator clips
- M2.5 x 16mm screws and M2.5 nuts
- A 2.4mm screwdriver
- a 3D printer and optionally a laser cutter (for the enclosure)

### Software

- [Python3](https://www.python.org/download/releases/3.0/)
- [pip](https://pip.pypa.io/en/stable/#)
- [viam-server](/get-started/installation/#install-viam-server)
- [Viam Python SDK](https://python.viam.dev/)

## Set up your hardware

### 3D Print the enclosure

3D print the enclosure using [these STL files](https://github.com/viam-labs/devrel-demos/tree/main/confetti_bot/stl-files).
If you are using a different confetti cannon, you may need to adjust the size of the 3D prints to your confetti cannon size, as the wall thickness of the holder changes between brands.
The same applies for the motor, if you are using a different model, you can adjust the size for the motor so the holder fits your motor head.

You can either laser cut or 3D print the side panels depending on your liking, and which machine you have access to.

### Wire your motor, motor driver, board, and the battery

First, attach your motor with screws to the middle of the enclosure.
Attaching the motor first makes wiring the rest easier.

Because of the model we have, we only used two screws for the top, but some motors require four which is why the enclosure has four holes.

{{<imgproc src="/tutorials/confetti-bot/install-motor-before.jpg" resize="300x" declaredimensions=true alt="The motor shown next to the enclosure before being installed." style="min-width:200px; max-width:275px" class="center-if-small">}}
{{<imgproc src="/tutorials/confetti-bot/install-motor-after.jpg" resize="300x" declaredimensions=true alt="The motor being installed inside the enclosure with screws on top." style="min-width:200px; max-width:275px" class="center-if-small">}}

Now wire all of the components according to the wiring diagram:

![Wiring Diagram for confetti bot](/tutorials/confetti-bot/wiring-diagram.png)

1. Connect your motor to the motor driver.
   There are several wires coming out of the motor, connect the black one (ground) into `Out1` terminal and the red one (power) to `Out2` terminal and screw them in tightly (a 2.4mm screwdriver works well for this).
   After you have finished screwing the block down, make sure it is secure by gently tugging on the wire.
   If it is not secure, the wire will come out.
   You can leave the other wires disconnected.

2. Connect your Raspberry Pi to the motor driver.
   Since you are using `Out1` and `Out2` on the driver, you need to use the corresponding inputs (`In1` and `In2`), as well as a PWM pin.
   Select three available [GPIO pins](https://pinout.xyz/pinout/wiringpi) on the Raspberry Pi and connect them to the `ENA` (green wire in the wiring diagram), `In1` (yellow wire in the wiring diagram), and `In2` (orange wire in the wiring diagram) pins on the motor controller.
   Take the black safety cap out from the motor driver so you can use the ENA pin.
   Make sure to remember which GPIO pin on the Raspberry Pi you connected to each of these inputs.
   In our case, we connected Pin 11, 13, and 15 respectively.

3. Connect your button to the Raspberry Pi.
   One of the connections goes to a 3.3V pin on the Raspberry Pi, and the other needs to be connected to a GPIO pin.
   We used Pin 1 for 3.3V (blue wire in wiring diagram).
   Make sure to record which GPIO pin you connect to since you will be using this in your machine configuration.
   We used Pin 37 (white wire in wiring diagram).

4. Now you can connect the button to your 12V battery, use a black alligator clip to connect the ground of the button switch to the ground of the battery.
   Then from the same ground of the battery, use a black wire to connect to the ground pin on the motor driver.
   The ground of the motor driver will be shared with the Raspberry Pi, and your battery.
   Find a [ground pin](https://pinout.xyz/pinout/ground) on your Raspberry Pi and connect it to the ground pin on the motor driver, allowing two pins to share the ground.
   Screw them tight with a screwdriver.
   We used Pin 6 on the Raspberry Pi as our ground pin, but you can use any [Raspberry Pi ground pin](https://pinout.xyz/pinout/ground).
5. Now that you have grounded your robot, you can connect the motors to power.
   Use a red alligator clip to connect the battery to the button switch, and another red alligator clip to connect the battery to the 12V input on the motor driver.
6. Your robot wiring is now complete! Put the microSD card in the Raspberry Pi and turn it on by plugging it to the wall.

{{<imgproc src="/tutorials/confetti-bot/wired-motor-driver.jpg" resize="400x" declaredimensions=true alt="Closeup photo of the motor driver after all the wiring to the motor, the board and the battery." class="center-if-small" style="min-width:275px; max-width:350px">}}

{{<imgproc src="/tutorials/confetti-bot/wired-all-components.jpg" resize="400x" declaredimensions=true alt="Motor, motor driver, board and battery all wired to each other." class="center-if-small" style="min-width:275px; max-width:350px">}}

## Configure your confetti bot with the Viam app

Now that your robot is wired, you need to configure it on the Viam app before you can program it.

In the Viam app, create a new machine and give it a name.
We named ours ConfettiBot.

![A machine page header in the Viam app, its under the location work, and named ConfettiBot.](/tutorials/confetti-bot/app-name-confettibot.png)

Then navigate to the machine’s **Config** tab to start configuring your components.

{{< tabs >}}
{{% tab name="Builder UI" %}}

### Configure the Pi as a board

Click on the **Components** subtab and click **Create component** in the lower-left corner of the page.

Add your {{< glossary_tooltip term_id="board" text="board" >}} with type `board` and model `pi`.
Enter `party` for the name of your [board component](/components/board/), then click **Create**.

You can name your board whatever you want as long as you refer to it the same way in your code; we picked `party` for fun.
Your board configuration should now look like this:

![Board component configured in the Viam app, the component tab is named party, with a type attribute board and model attribute pi.](/tutorials/confetti-bot/app-board-attribute.png)

### Configure the motor

Click on the **Components** subtab and click **Create component** in the lower-left corner of the page.
Select `motor` for the type and `gpio` for the model.
Enter `start` for the name of your [motor component](/components/motor/), then click **Create**.
Again, we named it “start” to refer to the button being pressed, but this name is up to you as long as you remember the name and use the same name in the code later.

After clicking **Create**, there is a pin assignment type toggle.
Select **In1/In2** since that is compatible with the type of input our motor controller expects.
In the dropdowns for A/In1 and B/In2, choose `13 GPIO 27` and `15 GPIO 22` and for PWM choose `11 GPIO 17` corresponding to our wiring.

In the **Board** dropdown within attributes, choose the name of the board the motor controller is wired to (“party”).
This will ensure that the board initializes before the motor driver when the robot boots up.

![Motor component configured in the Viam app, the component tab is named start, with a type attribute motor and model attribute gpio. It has the attributes as of the board as party, encoder as non-encoded, max rpm as 1000, component pin assignment type as In1/In2, enable pins as neither, a/In1 as 13 GPIO 27, b/In2 as 15 GPIO 22, pwm as 11 GPIO 17.](/tutorials/confetti-bot/app-motor-attribute.png)

Click **Save Config** at the bottom of the screen.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [**Raw JSON** tab](/build/configure/#the-config-tab), replace the configuration with the following JSON configuration for your board and your motor:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "party",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "start",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "a": "13",
          "b": "15",
          "pwm": "11"
        },
        "board": "party",
        "max_rpm": 1000
      },
      "depends_on": ["party"]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

Let’s test our configuration from the [Control tab](/fleet/machines/#control).
Go to the board panel, set the pin connected to your motor (in our case pin 37) to high, and your motor should turn.

## Attach components to the enclosure

Now that you have tested your motor in the app and confirmed that everything works, you can finish assembling your confetti bot.

1.  Attach the motor driver to the enclosure wall with four M2.5 x 16mm screws and M2.5 nuts.

{{<imgproc src="/tutorials/confetti-bot/install-driver-1.jpg" resize="400x" declaredimensions=true alt="Back view of the motor driver being installed inside the 3D printed enclosure with screws." class="center-if-small" style="min-height:275px; max-height:350px">}}

{{<imgproc src="/tutorials/confetti-bot/install-driver-2.jpg" resize="400x" declaredimensions=true alt="Front view of the motor driver being installed inside the 3D printed enclosure with screws." class="center-if-small" style="min-height:275px; max-height:350px">}}

2.  Slip the Raspberry Pi into the designated slot in the enclosure.
    Be careful of the wires during this so they don’t pop off.

{{<imgproc src="/tutorials/confetti-bot/install-pi-1.jpg" resize="400x" declaredimensions=true alt="Back view of the Raspberry Pi being installed inside the 3D printed enclosure within the designated slot." class="center-if-small" style="min-height:275px; max-height:350px">}}

{{<imgproc src="/tutorials/confetti-bot/install-pi-2.jpg" resize="400x" declaredimensions=true alt="Front view of the Raspberry Pi being installed inside the 3D printed enclosure within the designated slot." class="center-if-small" style="min-height:275px; max-height:350px">}}

3.  Add the confetti cannon to the enclosure by tightening the 3D printed holder around the confetti socket using one M2.5 x 16mm screw and a M2.5 nut.
    Then connect the enclosure to the front panel.

{{<imgproc src="/tutorials/confetti-bot/install-cannon-front.jpg" resize="400x" declaredimensions=true alt="Front photo of the confetti cannon attached to the 3D printed parts." class="center-if-small" style="min-height:275px; max-height:350px">}}

{{<imgproc src="/tutorials/confetti-bot/install-cannon-side.jpg" resize="400x" declaredimensions=true alt="Side photo of the confetti cannon attached to the 3D printed parts." class="center-if-small" style="min-height:275px; max-height:350px">}}

4.  Next, attach the 3d-printed circular holder to the base of the confetti cannon to hold its place, then to the motor.
    Secure the two together with a screw from the side.
    Depending on your motor size, you may need a different screw size.

{{<imgproc src="/tutorials/confetti-bot/install-motor-holder.jpg" resize="400x" declaredimensions=true alt="The 3D printed black piece attached to motor with a screw securing it in place over the motor head." class="center-if-small" style="min-height:275px; max-height:350px">}}

{{<imgproc src="/tutorials/confetti-bot/install-cannon-holder.jpg" resize="400x" declaredimensions=true alt="Motor attachment with a 3D printed black piece wrapped around the confetti cannon secured over the motor head." class="center-if-small" style="min-height:275px; max-height:350px">}}

{{<imgproc src="/tutorials/confetti-bot/install-cannon-enclosure.jpg" resize="400x" declaredimensions=true alt="Motor attachment with a 3D printed black piece wrapped around the confetti cannon secured over the motor head attached to the enclosure." class="center-if-small" style="min-height:275px; max-height:350px">}}

5.  Add the front section you just built to the rest of the enclosure using M2.5 x 16mm screws and M2.5 nuts.
    Make sure to do this step before closing the side walls to be able to access the slots for screws.

{{<imgproc src="/tutorials/confetti-bot/install-front-enclosure.jpg" resize="400x" declaredimensions=true alt="Side view photo of the front section attached to the rest of the enclosure." class="center-if-small" style="min-height:275px; max-height:350px">}}

### Optional: Laser cut or print the sides

Laser cut the sides of the enclosure and attach with screws.
You can find the designs [on Viam Labs' GitHub](https://github.com/viam-labs/devrel-demos/tree/main/confetti_bot/stl-files).

If you don’t have a laser cutter, you can 3D print the sides instead, or leave them empty.

{{<imgproc src="/tutorials/confetti-bot/install-lasercut-side.jpg" resize="400x" declaredimensions=true alt="Lasercut side attached to the enclosure, with few cables going out of the enclosure." class="center-if-small" style="min-height:275px; max-height:350px">}}

### Final design

The final design, fully wired and put together looks like this:

{{<imgproc src="/tutorials/confetti-bot/final-assembly-top.jpg" resize="400x" declaredimensions=true alt="Top view of the final assembly of the confetti cannon and 3D printed/laser cutted pieces, with a battery and a red button on a white table." class="center-if-small" style="min-height:275px; max-height:350px">}}

{{<imgproc src="/tutorials/confetti-bot/final-assembly-side.jpg" resize="400x" declaredimensions=true alt="Side view of the final assembly of the confetti cannon and 3D printed/laser cutted pieces, with a battery and a red button on a white table." class="center-if-small" style="min-height:275px; max-height:350px">}}

## Write Python code to control the confetti bot

The following section explains the code for the confetti bot.
The completed code for this project is available on [GitHub](https://github.com/viam-labs/devrel-demos/tree/main/confetti_bot).
If you copy the code from this link, don’t forget to change your machine address and secret so it connects to your own confetti robot.

Navigate to the **Code sample** tab on the Viam app, select **Python** as the language, and click the **Copy** button.

{{% snippet "show-secret.md" %}}

Paste this into a new Python file in your favorite code editor to connect to your machine.

At the top of the code, your board and motor components are imported:

```python
from viam.components.board import Board
from viam.components.motor import Motor
```

In your `main` function add the following code, which instantiates a variable `party` as the board and `start` as the motor:

```python {class="line-numbers linkable-line-numbers"}
party = Board.from_robot(robot, "party")
# Note that the pin supplied is the pin we use. Please change this to the pin
# you are using.
party_return_value = await party.gpio_pin_by_name("37")
print(f"party gpio_pin_by_name return value: {party_return_value.get()}")

start = Motor.from_robot(robot, "start")
start_return_value = await start.is_moving()
print(f"start is_moving return value: {start_return_value}")
```

The only other code you need to add to your `main` function is a while loop to check if the button is being pressed.
Copy this code and add it to your own code within the main function block:

```python {class="line-numbers linkable-line-numbers"}
while True:
    print(party_return_value.get())
    while (await party_return_value.get()):
        await start.set_power(.8)
        await asyncio.sleep(0.1)
        if not (await GPIO.get()):
            break
    await start.set_power(0)
```

This is all the code you need to activate the gpio pin and turn the confetti cannon that is attached to your motor!

## Next steps

In this tutorial, you learned how to turn a motor when a button is pressed and set off a confetti cannon.
You could use this same concept for any simple robot that involves turning a motor when a pin on the Raspberry Pi goes “high.”
One example of this logic would be connecting a PIR sensor to a Raspberry Pi.
You could then make a motor turn whenever you sense a person walking by.

For more robotics projects, check out our [other tutorials](/tutorials/).
