---
title: "Create a Lazy Susan Using a DC Motor"
linkTitle: "Lazy Susan"
type: "docs"
description: "Wire a DC motor to a board, attach a plate on top, and control the motor to rotate the plate."
videos:
  ["/tutorials/lazy-susan/preview.webm", "/tutorials/lazy-susan/preview.mp4"]
videoAlt: "A circular wooden board slowly spinning clockwise with 3 bowls on top filled with snacks."
images: ["/tutorials/lazy-susan/preview.gif"]
tags: ["motor", "python"]
no_list: true
authors: ["Arielle Mella"]
languages: ["python"]
viamresources: ["board", "motor"]
level: "Beginner"
date: "2023-05-29"
# updated: ""
cost: 114
---

{{<gif webm_src="/tutorials/lazy-susan/lazy-susan.webm" mp4_src="/tutorials/lazy-susan/lazy-susan.mp4" alt="A circular wooden board slowly spinning clockwise with 3 bowls on top filled with snacks." max-width="350px" class="alignright">}}

Welcome to the robotic world of culinary comfort and supreme convenience!
Are you sick of straining your arms to transfer plates around the dinner table? Are you tired of being taken away from your delicious meal to pass the rolls?
Have you ever dreamed of a spinning device to do this chore?

By the end of this tutorial, you will have learned how to wire a motor and motor driver to a Raspberry Pi, install [`viam-server`](/get-started/installation/) on your Raspberry Pi, and how to configure your robot in the Viam app to create your own Lazy Susan for your dinner table!

You will also learn to take your creation a step further and fine-tune the controls of your Lazy Susan using the [Python motor API methods](/components/motor/#api).

## Requirements

### Hardware

This project requires the following hardware:

- [Raspberry Pi](https://a.co/d/bxEdcAT)
- [microSD card](https://a.co/d/j4fp6aA)
- microSD card reader
- DC motor (for example [this motor](https://www.digikey.com/en/products/detail/seeed-technology-co.-ltd/114090046/10385097))
- Motor driver (for example [this driver](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6))
- Appropriate flange coupler for your motor (for example [6mm flange coupler](https://a.co/d/fRFsu90))
- M3 Screws to fit the flange coupler to the board
- [Jumper wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY/ref=sr_1_1_sspa)
- Stranded wire for the motors (for example [16 gauge stranded wire](https://a.co/d/aDKOGkR))
- A circular board or plate (for example [14 inch wood round board](https://a.co/d/3RzQsrr))
- A power supply for the motor driver
- A power supply for the Raspberry Pi

### Tools

You will also need the following tools:

- Philips head screwdriver
- Double-sided tape (optional, but recommended)
- Wire cutters/scissors

## Hardware setup

A brushed DC motor is a motor that converts electrical current into mechanical energy.
In a brushed DC motor, the rotor spins 180-degrees when an electric current is applied.
In order to travel beyond the initial 180 degrees, the poles of the electromagnet must flip.
Carbon brushes contact the stator as the rotor spins, flipping the magnetic field and enabling the rotor to spin 360-degrees continuously.
The brushed motor we are using has a high starting torque which means it can reach a high speed quickly, it is low cost, and can sustain a larger load, perfect for a Lazy Susan!

A motor driver is a device that takes signals from your board and sends power to a motor based on those signals.
Motor drivers allow you to start and stop the motor, select clockwise or counterclockwise rotation, and speed it up or slow it down.

A {{< glossary_tooltip term_id="board" text="board" >}} is the hardware that sends digital signals to control your machine.
Your board allows you to send PWM (pulse width modulation) signals to the motor driver to control the motor speed.
PWM controls motor speed by sending electrical current in pulses - the more frequently pulses are sent in a given time period, the faster the motor will move.
The board sends PWM signals to the motor driver through GPIO (general-purpose input/output) pins, which are digital pins that the board provides to allow you to flexibly communicate with various devices.

You will also use the board to deploy code, run `viam-server`, and connect your robot to the internet and the cloud.

Use the following diagram to wire your hardware together.
Make sure your board is turned off and unplugged before wiring!

![Wiring diagram for the Lazy Susan showing colored wires connecting the assembled components.](/tutorials/lazy-susan/wiring-diagram.png)

{{% alert title="Important" color="note" %}}
The Raspberry Pi and the 12V power supply share the same GND on the L298N motor driver.
The Raspberry Pi is powered by its own 5V power cable.
{{% /alert %}}

Connect the flange coupler to your motor, and use the M3 screws and screwdriver to fix the flange coupler to your circular board or plate.
Turn on the Raspberry Pi and move on to setting up your software.

### Software setup

If you have not already done so, follow the [Raspberry Pi Setup Guide](/get-started/installation/prepare/rpi-setup/) to prepare your Pi to connect your robot to the Viam app.
Once your Pi is ready, `ssh` into it from your computer.

In your web browser, go to [the Viam app](https://app.viam.com) and create a new machine instance.
Name your robot whatever you like and head to the **Setup** tab.
On your Pi, follow the steps there to download the Viam app config and download and install `viam-server`.
Wait a moment until your robot connects to the Viam app.

## Configure your robot

{{< tabs >}}
{{% tab name="Builder UI" %}}

1. **Configure the board**

   First, configure your {{< glossary_tooltip term_id="board" text="board" >}} component:

   Navigate to the **Config** tab of your robot’s page in the [Viam app](https://app.viam.com).
   Click the **Components** subtab, then click **Create component** in the lower-left corner.

   Select `board` for type and `pi` for model.

   Enter `local` as the name for your board, then click **Create**.

2. **Configure the motor**

   Next, add a [motor component](/components/motor/):

   Navigate to the **Components** subtab and click **Create component** in the lower-left corner.

   Select `motor` for type and `gpio` for model.

   Enter `dcmotor` as the name for your motor, then click **Create**.

   After creating your motor component, fill in the [required attributes for a gpio motor](/components/motor/gpio/):

   - For **board**, click the dropdown box and select local (or whatever you named your board!).

     ![The motor component attribute panel with local selected for the board.](/tutorials/lazy-susan/config-motor-attribute.png)

   - For **Max RPM**, enter `100`.
     RPM stands for revolutions per minute: it's roughly a measure of how fast any machine is operating at a given time.
     Enter `100` so the motor moves at a moderate speed.
     You can fine tune this later in our custom code.
   - Toggle the slider to **In1/In2** motor type.
     The specific driver you are using expects this pin configuration.

     ![The motor component attribute panel with the Component pin assignment area. Type has two options: direction and In1/In2 and In1/In2 is toggled on.](/tutorials/lazy-susan/config-motor-pin1.png)

   - During wiring, you connected pins on the Pi to two ports called IN1 and IN2, and a third pin to ENA.
     When you toggle the **In1/In2** motor type, the UI opens three dropdown fields below it.
     Use these to specify the board pins that each motor driver pin is wired to:

     - **A/In1**: use 16 GPIO 23
     - **B/In2**: use 18 GPIO 24
     - **PWM**: use 22 GPIO 25 - this is the pin you attached the PWM (pulse-width modulation) jumper wire to.
       On the motor driver we used, it is labeled as **ENA**.

      <br>

     ![The motor component attribute panel under the Component pin assignment area and 16 GPIO 23 has been selected for A/In1, 18 GPIO 24 has been selected for B/In2, and 22 GPIO 25 has been selected for PWM.](/tutorials/lazy-susan/config-motor-pin2.png)

   - For **Depends On** select **local**. This ensures that the board is initialized before the motor.

     ![The motor component attribute panel. At the bottom of the page for “Depends on”, local is selected.](/tutorials/lazy-susan/config-motor-depends.png)

Click the **Save Config** button.

{{<gif webm_src="/tutorials/lazy-susan/config-save.webm" mp4_src="/tutorials/lazy-susan/config-save.mp4" alt="Click the save button" max-width="150px">}}

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/build/configure/#the-configure-tab), replace the configuration with the following JSON configuration for your board and motor:

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
      "name": "dcmotor",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "a": "16",
          "b": "18",
          "pwm": "22"
        },
        "board": "local",
        "max_rpm": 100
      },
      "depends_on": ["local"]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{<gif webm_src="/tutorials/lazy-susan/config-save.webm" mp4_src="/tutorials/lazy-susan/config-save.mp4" alt="Click the save button" max-width="150px">}}

{{% /tab %}}
{{< /tabs >}}

## Test the motor in the Viam app

Navigate to the **Control** tab and click on the top of the **dcmotor** card to open the motor controls.

{{<gif webm_src="/tutorials/lazy-susan/control-dcmotor.webm" mp4_src="/tutorials/lazy-susan/control-dcmotor.mp4" alt="The Viam app Control tab and clicking the dcmotor dropdown card to reveal the controls.">}}

You can change the direction of rotation of the motor by toggling the **Forwards** and **Backwards** button.

You can also adjust how fast the motor rotates by adjusting the **Power %** slider.

{{<gif webm_src="/tutorials/lazy-susan/control-power.webm" mp4_src="/tutorials/lazy-susan/control-power.mp4" alt="The controls in the Control tab for the dcmotor. The gif shows there is a toggle for direction of rotation and below that is a Power % slider and below the slider on the left is the run button." max-width="400px">}}

Hit the **RUN** button when you're ready and check that your motor runs!

Adjust your settings and test your motor to find the perfect settings that suit your Lazy Susan prototype.

{{<gif webm_src="/tutorials/lazy-susan/control-video.webm" mp4_src="/tutorials/lazy-susan/control-video.mp4" alt="The Control tab as discussed above, and an overlay video of the actual motor running with the changing of the power % in the Viam app.">}}

When you’re done testing your motor, press the **STOP** button in the upper right corner to stop your motor.

{{<gif webm_src="/tutorials/lazy-susan/control-stop.webm" mp4_src="/tutorials/lazy-susan/control-stop.mp4" alt="Click the stop button" max-width="150px">}}

## Use the Python SDK to control the motor

`pip` is a package-management system written in Python and is used to install and manage software packages and their dependencies during deployment.

`ssh` into your Pi or use your existing `ssh` session to install the `pip` package manager.
Run the following command and type "yes" when it asks if you want to continue:

```sh
sudo apt install python3-pip
```

The [Viam Python SDK](https://python.viam.dev/) allows you to write programs in the Python programming language to operate robots using Viam.
To install the Python SDK on your Raspberry Pi, run the following command in your existing `ssh` session to your Pi:

```sh
pip3 install viam-sdk
```

Installing with `pip` ensures you are using the latest version of `viam-sdk`, and makes updating it in the future easy.

On the [Viam app](https://app.viam.com/), select the **Code sample** tab and set **Python** as the language.

![The Language portion of the Code Sample tab.](/tutorials/lazy-susan/python-language.png)

{{% snippet "show-secret.md" %}}

Copy the code:

![The Viam app Code Sample tab with language set to Python](/tutorials/lazy-susan/python-code.png)

Create a new python file called `lazysusan.py` on your Raspberry Pi and paste the copied code into it:

```sh
nano turnsusan.py
```

Press CTRL-X to save and exit.
Enter `y` to confirm, and then hit return to accept the same filename.

Next, run the following command to check the connection, and to see if there are any errors:

```sh
python3 turnsusan.py
```

The output should show a list of resources:

![The resources printed out in the terminal showing no errors.](/tutorials/lazy-susan/python-resources.png)

If there are no errors, you have successfully connected to your robot and run some code!

## Use motor API methods

Now let's move on to write code to fine tune the control of your motor.
It would be nice if the lazy susan rotated slowly so people can grab some food.
Head to the Motor API in the [Python SDK documentation](https://python.viam.dev/autoapi/viam/components/motor/index.html).

[SetPower](/components/motor/#setpower) adjusts speed by adjusting the power to the motor.
This may feel familiar from when you were testing the hardware in the Viam app and adjusted the **Power %** and **Forward** and **Backward** toggle.
Instead of using a toggle to adjust the motor direction, you now use either positive or negative numbers up to 100.

Reference the [SetPower API Method example](/components/motor/#setpower) for more information.

[GoFor](/components/motor/#gofor) allows you to control how fast the motor spins by allowing you to set the revolutions per minute (or RPMs).
This allows you to have more control over how fast and how long you spin the motor for.
If you want to have your motor spin backwards, one of these parameters (not both) needs to be negative.

If you have a project that needs to be below a certain speed, you can set the **Max RPM** in the Viam app as we did during configuration.
One extra "0" in your API method could mean you’re picking sunflower seeds from every corner of the room at midnight.

For the purposes of this tutorial, let's start with the `SetPower` method and assume that we need the Lazy Susan to run for an undetermined amount of time.

Open the `turnsusan.py` file with `nano` within your terminal.

```sh
nano turnsusan.py
```

You can start by adding this call to `set_power` to your `main function` above the line that closes the robot connection with `robot.close()`:

```python
# Use the set power method before you close the code loop
await dc_motor.set_power(power=0.2)
```

Enter CTRL+X to save and exit: press y when prompted to accept changes, and the return key to accept the original filename.

Now, run your code:

```sh
python3  turnsusan.py
```

Your Lazy Susan should now spin at the speed you indicated.
Because we didn’t set any parameters for how long this will run for, we will need to stop it using the Viam app button on the **Control** tab for now.

{{<gif webm_src="/tutorials/lazy-susan/control-stop.webm" mp4_src="/tutorials/lazy-susan/control-stop.mp4" alt="Click the stop button" max-width="150px">}}

However, there is also an API method you can use to [Stop](/components/motor/#stop) the motor!

Add the following import statement at the top of your code:

```python
# Import time to add a sleep function to the top of your code
import time
```

Then add the following code underneath the code that sets the power of the motor:

```python
# Wait 10 seconds to make the motor spin for 10 seconds
time.sleep(10)
# Stop the motor
await dc_motor.stop()
```

If you would like to have the same effect but use even less code, you can use the [GoFor API Method](/components/motor/#gofor).
Remove the code you have just added or comment it out and add the following code instead:

```python
# await dc_motor.set_power(power = 0.2)
# time.sleep(10)
# await dc_motor.stop()

# Turn the motor 7.2 revolutions at 60 RPM.
await dc_motor.go_for(rpm=60, revolutions=7.2)
```

Enter CTRL+X to save and exit.
Press Y when prompted to accept changes, and the return key to accept the original filename.

You have now successfully completed the code for your Lazy Susan and have learned how to turn your motor using the Viam app and with code using the Python SDK.

Now you can go ahead and put your robot together with the turntable.
Connect the wood to your motor and decorate it as you wish to make your Lazy Susan a hit at your next dinner party!

{{<gif webm_src="/tutorials/lazy-susan/preview.webm" mp4_src="/tutorials/lazy-susan/preview.mp4" alt="A circular wooden board slowly spinning clockwise with 3 bowls on top filled with snacks." max-width="300px" class="aligncenter">}}

## Next steps

This is not where your Lazy Susan project has to end - here are some ideas for adding more components to this project:

- An [input controller component](/components/input-controller/) so you can turn and stop the Lazy Susan with a gamepad.
- A [camera component](/components/camera/) and an [ML model](/ml/) that recognizes your friends' faces and stops the Lazy Susan precisely where they can reach their favorite food, or takes their photo as it rotates, so you all can have candid memories.
- A [sensor component](/components/sensor/), so your Lazy Susan only spins when it detects movement around it.

Or you can head over to our [Tutorials](/tutorials/) page and try one of our other tutorials to continue building robots.

Let us know how you do and make sure to show off your project in our [Community Discord](https://discord.gg/viam)!
