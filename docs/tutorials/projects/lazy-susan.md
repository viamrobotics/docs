---
title: "Single Component Tutorial: How to Create a Lazy Susan Using a DC Motor"
linkTitle: "Lazy Susan"
weight: 50
type: "docs"
description: "Wire a DC motor to a motor driver and a board, connect to viam-server and use the Python SDK and Viam motor API methods to turn and control the motor with a circular plate attached to the top."
webmSrc: "/tutorials/img/lazy-susan/preview.webm"
videoAlt: "A circular wooden board slowly spinning clockwise with 3 bowls on top filled with snacks."
images: ["/tutorials/img/lazy-susan/preview.gif"]
tags: ["motor", "python"]
no_list: true
# Author: DevRel
---

![Video of a circular wooden board slowly spinning clockwise with 3 bowls on top filled with snacks.](/tutorials/img/lazy-susan/preview.webm)

Welcome to the robotic world of culinary comfort and supreme convenience!
Are you sick of straining your arms to transfer plates around the dinner table? Are you tired of being taken away from your delicious meal to pass the rolls?
Have you ever dreamed of a spinning device to do this chore?

This tutorial is part of **Viam’s Single Component Tutorial series**, where you can learn how to use different components with Viam.
By the end of this tutorial, you will have learned how to wire a motor and motor driver to a Raspberry Pi, install [`viam-server`](/installation/) on your Raspberry Pi, and how to configure your robot in the Viam app to create your own Lazy Susan for your dinner table!

You will even learn to take your creation a step further and fine-tune the controls of your Lazy Susan using the motor [API methods](/components/motor/#api) in the [Python SDK](https://python.viam.dev/).  

## Requirements

### Hardware

This project requires the following hardware:

* [Raspberry Pi](https://a.co/d/bxEdcAT)
* [microSD card](https://a.co/d/j4fp6aA)
* microSD card reader
* DC motor (we used [this motor](https://www.digikey.com/en/products/detail/seeed-technology-co.,-ltd/114090046/10385097?utm_adgroup=Seeed%20Technology%20Co.%2C%20LTD.&utm_source=google&utm_medium=cpc&utm_campaign=Shopping_DK%2BSupplier_Tier%201%20-%20Block%202&utm_term=&utm_content=Seeed%20Technology%20Co.%2C%20LTD.&gclid=CjwKCAjw9pGjBhB-EiwAa5jl3JM4MaGC5NOvh6Q4eRcPJJUii3bgPdp52WWpQ2O5aINUJ3Rj2X9BhhoC5rAQAvD_BwE))
* Motor driver (we used [this driver](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6))
* Appropriate flange coupler for your motor (we used a [6mm flange coupler](https://a.co/d/fRFsu90))
* M3 Screws to fit the flange coupler to the board
* [Jumper wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY/ref=sr_1_1_sspa?crid=107AKOXZK7HUP&keywords=jumper+wires&qid=1679848574&sprefix=jumper+wires%2Caps%2C90&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFETERTUzEzQ1c4UTYmZW5jcnlwdGVkSWQ9QTA3MDk4MDcyTlJIR0hBNklXTzY2JmVuY3J5cHRlZEFkSWQ9QTA5NDU0MzYxSkE3VExKQkZEQUxaJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==)
* Stranded wire for the motors (we used [16 gauge stranded wire](https://a.co/d/aDKOGkR))
* A circular board or plate (we used a [14 inch wood round board](https://a.co/d/3RzQsrr))
* A power supply for the motor driver
* A power supply for the Raspberry Pi

### Tools

You will also need the following tools:

* Philips head screwdriver
* Double-sided tape (optional, but recommended)
* Wire cutters/scissors

### Software

Your computer should have the following software installed:

* [Python 3](https://www.python.org/download/releases/3.0/)
* [pip](https://pip.pypa.io/en/stable/#)

## Setup

### Hardware Setup

A brushed DC motor is a motor that converts electrical current into mechanical energy.
In a brushed DC motor, the rotor spins 180-degrees when an electric current is applied.
In order to travel beyond the initial 180 degrees, the poles of the electromagnet must flip.
Carbon brushes contact the stator as the rotor spins, flipping the magnetic field and enabling the rotor to spin 360-degrees continuously.
This brushed motor has a high starting torque which means it can reach a high speed quickly, it is low cost, and can sustain a larger load, perfect for your Lazy Susan!

A motor driver is a device that takes signals from your board and sends power to a motor based on those signals.
Motor drivers allow you to start and stop the motor, select clockwise or counterclockwise rotation, and speed it up or slow it down.

A {{< glossary_tooltip term_id="board" text="board" >}} is the hardware that sends digital signals to control your robot.
Your board allows you to send PWM (pulse width modulation) signals to the motor driver to control the motor speed.
PWM controls motor speed by sending electrical current in pulses - the more frequently pulses are sent in a given time period, the faster the motor will move.
The board sends PWM signals to the motor driver through GPIO (general-purpose input/output) pins, which are digital pins that the board provides to allow you to flexibly communicate with various devices.

You will also use the board to deploy code, run `viam-server`, and connect your robot to the internet and the cloud.

Use the following diagram to wire your hardware together. Make sure your board is turned off and unplugged before wiring!

![Wiring diagram for the Lazy Susan showing colored wires connecting the assembled components.](/tutorials/img/lazy-susan/wiring-diagram.png)

{{% alert title="Note" color="primary" %}}
The Raspberry Pi and the 12V power supply share the same GND on the L298N motor driver. The Raspberry Pi is powered by its own 5V power cable.
{{% /alert %}}

Turn on the board when you’re done wiring.

### Software Setup

If you have not already done so, follow the [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/) to prepare your Pi to begin connecting your robot to the Viam app.
Once your Pi is ready, start an `ssh` session to it from your computer.

In your web browser, go to [the Viam app](https://app.viam.com) and create a new robot instance in your desired organization.
Name your robot whatever you like and head to the **Setup** tab.
Follow the steps there to download the Viam app config and download and install `viam-server` to your Pi.
Wait a moment and your robot will now be connected to the Viam app!

## Configure your robot

### 1. Configure the board

First, configure your {{< glossary_tooltip term_id="board" text="board" >}} component.
Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com).
Add a new component with the following attributes:

   ![Screenshot of the Viam app config page showing the board component being created with the name local, type board, and  model pi.](/tutorials/img/lazy-susan/config-board.png)

* **Name**: `local`  - you can name this whatever you want: remember that you will reference it later in your code.
* **Type**: `board`
* **Model**: `pi`

### 2. Configure the motor

Next, add a new motor component:

   ![Screenshot of the Viam app config page showing the motor component being built with the name dcmotor, type motor, and model gpio.](/tutorials/img/lazy-susan/config-motor.png)

* **Name**:  `dcmotor`
* **Type**:  `motor`
* **Model**:  `gpio`

After creating your motor component, fill in the [required attributes for a gpio motor](/components/motor/gpio/).

For **board**, click the dropdown box and select local (or whatever you named your board!).

![Screenshot of the Viam app config page showing the motor component attribute panel with local selected for the board.](/tutorials/img/lazy-susan/config-motor-attribute.png)

* For **Max RPM**, enter `100`.
  RPM stands for revolutions per minute: it's roughly a measure of how fast any machine is operating at a given time.
  We chose `100` so the motor moves at a moderate speed.
  We can fine tune this later in our custom code.
* Toggle the slider to **In1/In2** motor type.
  The reason why we are selecting this mode is because the specific motor driver we are using expects this pin configuration.
  During wiring, notice that we connected pins on the Pi to two ports called IN1 and IN2, and a third pin to ENA.

![Screenshot of the Viam app config page showing the motor component attribute panel with the Component pin assignment area. Type has two options: direction and In1/In2 and In1/In2 is toggled on.](/tutorials/img/lazy-susan/config-motor-pin1.png)

* When you toggle the **In1/In2** motor type, it opens three dropdown menus below it.
  Use these to specify the board pins that each motor driver pin is wired to:

  * **A/In1**: use 16 GPIO 23
  * **B/In2**: use 18 GPIO 24
  * **PWM**: use 22 GPIO 25- this is the pin you attached the PWM (pulse-width modulation) jumper wire to.
  On the motor driver we used, it is labeled as **ENA**.

![Screenshot of the Viam app config page showing the motor component attribute panel under the Component pin assignment area and 16 GPIO 23 has been selected for A/In1, 18 GPIO 24 has been selected for B/In2, and 22 GPIO 25 has been selected for PWM.](/tutorials/img/lazy-susan/config-motor-pin2.png)

* For **Depends On** click **local.** This ensures that the board is initialized before the motor.

![Screenshot of the Viam app config page showing the motor component attribute panel. At the bottom of the page for “Depends on”, local is selected.](/tutorials/img/lazy-susan/config-motor-depends.png)

### 3. Save config

Click the **Save Config** button.

![A gif of the save button and a finger clicking it.](/tutorials/img/lazy-susan/config-save.webm)

## Test the motor in the Viam app

Navigate to the **Control** tab and click on the top of the **dcmotor** card to open the motor controls.

![A gif of the Viam app Control tab and clicking the dcmotor dropdown card to reveal the controls.](/tutorials/img/lazy-susan/control-dcmotor.webm)

Here, you can change the direction of rotation of the motor by toggling the **Forwards** and **Backwards** button.

You can also adjust how fast the motor rotates by adjusting the **Power %** slider.

![A gif of the controls in the Control tab for the dcmotor. The gif shows there is a toggle for direction of rotation and below that is a Power % slider and below the slider on the left is the run button.](/tutorials/img/lazy-susan/control-power.webm)

When you’ve adjusted your settings, hit the **RUN** button!

Test your motor to find the perfect settings that suit your Lazy Susan prototype.

![A gif of the Control tab as discussed above, and an overlay video of the actual motor running with the changing of the power % in the Viam app.](/tutorials/img/lazy-susan/control-video.webm)

When you’re done testing your motor, press the **STOP** button in the upper right corner to stop your motor.

![A GIF of the stop button and a finger clicking it.](/tutorials/img/lazy-susan/control-stop.webm)

## Using the Python SDK to control the motor

First, run this command in your existing `ssh` session to your Pi to install the `pip` package manager.
Type "yes" when it asks if you want to continue.
`pip` is a package-management system written in Python and is used to install and manage software packages and their dependencies during deployment.

```sh
sudo apt install python3-pip                                                                                            
```

The [Viam Python SDK](https://python.viam.dev/) allows you to write programs in the Python programming language to operate robots using Viam.
To install the Python SDK on your Raspberry Pi, run the following command in your existing `ssh` session to your Pi:

```sh
pip3 install viam-sdk
```

Installing with `pip` ensures you are using the latest version of `viam-sdk`, and makes updating it in the future easy.

On the [Viam app](https://app.viam.com/), select the **Code Sample** tab, and set **Python** as the language.

![Screenshot of the Language portion of the Control tab at the very top.](/tutorials/img/lazy-susan/python-language.png)

Since you just installed the Python SDK, you can skip the first step.
Copy the code from step 2.

![Screenshot of the Viam app Control tab with an arrow pointing to the Copy code button.](/tutorials/img/lazy-susan/python-code.png)

The copied code needs to go in a Python file on the Raspberry Pi.
You can do so by creating a file on the Raspberry Pi and editing the file with `nano`.

`ssh` into your Pi and run the following command to create a folder in your home directory to put your files in. We named ours `lazysusan`:

```sh
mkdir ~/lazysusan
```

Next, navigate to the new project directory:

```sh
cd ~/lazysusan
```

Create a file using `nano` by choosing a file name and ending it with `.py`.
We’ll call ours `turnsusan.py`:

```sh
nano turnsusan.py
```

Paste the code you got from the **Code Sample** tab on the Viam app into `nano`.
Press CTRL-X to save and exit.
Enter `y` to confirm, and then hit return to accept the same filename.

Next, run the following command to get the resource information to check the connection, and to see if there are any errors.

```sh
python3 turnsusan.py                                                                                                     
```

![Screenshot of the resources printed out in the terminal showing no errors.](/tutorials/img/lazy-susan/python-resources.png)

There are no errors in the resources above, so you have confirmed a good software connection between the Python SDK and your Viam robot!

## Use motor API methods

Now let’s move on to using API methods to fine tune the control of our motor.
For our simple Lazy Susan we want it to rotate slowly so people can enjoy the food.
Head to the Motor API in the [Python SDK documentation](https://python.viam.dev/autoapi/viam/components/motor/index.html).

[SetPower](/components/motor/#setpower) adjusts speed by adjusting the power to the motor.
This may feel familiar from when you were testing the hardware in the Viam app and adjusted the **Power %** and **Forward** and **Backward** toggle.
The difference here is we aren’t using a toggle to adjust the motor direction, instead we use either positive or negative numbers to 100.

At the bottom of these definitions, it gives an example on how to implement the API method into our code (`turnsusan.py`).

[GoFor](/components/motor/#gofor) allows us to control how fast we spin the motor by allowing us to set the revolutions per minute (or RPMs).
This allows us to have more control over how fast and how long we spin the motor.
If you want to have your motor spin backwards, one of these parameters (not both) needs to be negative.

If you have a project that needs to be below a certain speed, you can help safeguard this by setting the **Max RPM** in the Viam app like we did during configuration.
One extra “0” in your API method could mean you’re picking sunflower seeds from every corner of the room at midnight.

For the purposes of this tutorial, let’s start with the `SetPower` method and assume that we need the Lazy Susan to run for an undetermined amount of time.

Open the `turnsusan.py` file with `nano` within your terminal.

```sh
nano turnsusan.py                                                                                                   
```

Reference the [SetPower API Method example](/components/motor/#setpower) for more information on how this is executed.
Here is some demo code that you can use to get started to insert in your sample code imported from the Viam app:

```python
    # Some code that already exists in your app-provided code sample 

    dc_motor = Motor.from_robot(robot, "dcmotor")
    dc_motor_return_value = await dc_motor.is_moving()
    print(f"dc_Motor is_moving return value: {dc_motor_return_value}")
    my_board = Board.from_robot(robot, "local")
    my_board_return_value = await my_board.gpio_pin_by_name("16")
    print(f"local gpio_pin_by_name return value: {my_board_return_value.get()}

    #Use the set power method before you close the code loop 

    await dc_motor.set_power(power = 0.2)

    # Don't forget to close the robot when you're done!
    await robot.close()

    #Run the main fuction

if __name__ == '__main__':
    asyncio.run(main())

```

Enter CTRL+X to save and exit: press y when prompted to accept changes, and the return key to accept the original filename.

Run your code!

```sh
python3  turnsusan.py                                                                                                     
```

Your Lazy Susan should spin at the speed you indicated.
Because we didn’t set any parameters for how long this will run for, we will need to stop it using the Viam app button for now.

![A GIF of the stop button and a finger clicking it.](/tutorials/img/lazy-susan/control-stop.webm)

However, there is an API method for [Stop](/components/motor/#stop) you can use!
Add the following to your code to stop the motor:

```python
#Import time to add a sleep function to the top of your code 
import time 

   await dc_motor.set_power(power = 0.2)
#Add a sleep of 10 seconds to make the motor spin for 10 seconds 
   time.sleep(10)
#Stop the motor 
   await dc_motor.stop()
```

If you would like to have the same effect but use even less code, you can reference the [GoFor API Method example](/components/motor/#gofor).
This makes sure that you can rotate your motor for a set amount of time at a set speed (in revolutions per minute).
Comment out your `sleep` and `setPower` methods:

```python
  # await dc_motor.set_power(power = 0.2)
    # time.sleep(10)
    # await dc_motor.stop()

    # Turn the motor 7.2 revolutions at 60 RPM.
    await dc_motor.go_for(rpm=60, revolutions=7.2)

    # Don't forget to close the robot when you're done!
    await robot.close()
if __name__ == '__main__':
    asyncio.run(main())
```

Enter CTRL+X to save and exit.
Press Y when prompted to accept changes, and the return key to accept the original filename.

Congratulations! You have now successfully completed the code and hardware testing and have learned how to turn your motor using the Viam app and with code using the Python SDK.

Now you can go ahead and put your robot together with the turntable.
Connect the wood to your motor and make any other aesthetic design choices you want to make your Lazy Susan a hit at your next dinner party!

![Video of a circular wooden board slowly spinning clockwise with 3 bowls on top filled with snacks.](/tutorials/img/lazy-susan/preview.webm)

## Next steps

Here are some ideas for adding another component to this project:

* An [input controller component](/components/input-controller/) so you can turn and stop the Lazy Susan with a gamepad.
* A [camera component](/components/camera/) and a trained ML model that recognizes your friends’ faces and stops the Lazy Susan precisely where they can reach their favorite food, or takes their photo as it rotates, so you all can have candid memories and everyone picks up their phones less to take photos.
* A [sensor component](/components/sensor/) that turns the Lazy Susan on only when it detects movement around it.

Or you can head over to our [Tutorials](/tutorials/) page and try one of our other tutorials to continue building robots.
Let us know how you do and make sure to show off your project in our [Community Discord](https://discord.gg/viam)!

{{< snippet "social.md" >}}
