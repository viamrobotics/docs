---
title: "Unbox and Set Up your Viam Rover"
linkTitle: "Unbox and Set Up your Viam Rover"
weight: 10
type: "docs"
tags: ["rover", "tutorial"]
---

## Unbox and set up your Viam Rover

The Viam Rover comes preassembled with two encoded motors with suspension, a webcam with an integrated microphone, and a 3D accelerometer module.
You must purchase a Raspberry Pi 4 and four 18650 batteries (with charger) separately.
This guide covers what's inside the kit (and what is not), describes each component, provides instructions for wiring your rover, and includes links for additional hardware.

<img src="../img/viam-rover/rover-front.jpg" style="max-width:400px;width:100%" alt="The front of the assembled Viam Rover" />

### What's inside the kit

1. One assembled Viam Rover.

    <img src="../img/viam-rover/rover-side.jpg" style="max-width:400px;width:100%" alt="The side of the assembled Viam Rover" />

2. Four M2.5 screws for mounting your Raspberry Pi.

    <img src="../img/viam-rover/screws.jpg" style="max-width:400px;width:100%" alt="Four screws" />

3. Two spare stiffer suspension springs.
   You can swap them out with the springs that come with the rover if you need stiffer suspension for higher payload applications.

    <img src="../img/viam-rover/suspension-springs.jpg" style="max-width:400px;width:100%" alt="Two suspension springs" />

4. Three different Allen wrenches (1.5 mm, 2 mm, and 2.5 mm) to unscrew the top and mount the Raspberry Pi.

  <img src="../img/viam-rover/allen-wrenches.png" style="max-width:180px;width:100%" alt="Three allen wrenches" />

1. Ten female-to-female jumper wires.
   All of the wires' colors correspond to the included wiring diagram.
   Six are for the motor controller and four are for the accelerometer.

  <img src="../img/viam-rover/jumper-wires.jpg" style="max-width:400px;width:100%" alt="Ten colorful jumper wires" />

All together, your kit looks like this:

<img src="../img/viam-rover/box-contents.jpg" style="max-width:400px;width:100%" alt="A Viam Rover shipping box contents" />

### Rover components

#### Dual drive motors with suspension and integrated motor encoders

<img src="../img/viam-rover/encoder-motors.jpg" style="max-width:400px;width:100%" alt="two motors with encoders" />

The motors come with integrated encoders.
For further information on encoders, see [Encoder Component](/components/encoder/).
For more information on encoded DC motors, see [Motor Component](/components/motor/#dc-motor-with-encoder).

The kit also includes stiffer suspension springs that you can substitute for the ones on the rover.
Generally, a stiff suspension helps with precise steering control.
In contrast, a soft suspension allows the wheels to move up and down to absorb small bumps on the rover's path.

#### Motor driver

<img src="../img/viam-rover/motor-driver.png" style="max-width:400px;width:100%" alt="A L298N motor driver" />

The kit comes with an L298N driver dual H-Bridge DC motor driver.
L298 is a high voltage and high current motor drive chip, and H-Bridge is typically used to control the rotating direction and speed of DC motors.

#### 720p webcam, with integrated microphone

<img src="../img/viam-rover/webcam.jpg" style="max-width:400px;width:100%" alt="Webcam with cables" />

The webcam that comes with the kit is a standard USB camera device and the rover has a custom camera mount for it.
To find out more, see [Camera Component](/components/camera).

#### 3D accelerometer

<img src="../img/viam-rover/accelerometer.jpg" style="max-width:400px;width:100%" alt="A ADXL345 accelerometer" />

The [ADXL345](/components/movement-sensor/#adxl345) sensor manufactured by Analog Devices is a digital 3-axis accelerometer that can read acceleration up to ±16g for high-resolution (13-bit) measurements.
You can access it with a SPI (3-wire or 4-wire) or I<sup>2</sup>C digital interface.

In Viam, you can configure it as a [movement sensor component](/components/movement-sensor/).

#### Buck converter

<img src="../img/viam-rover/buck-converter.jpg" style="max-width:400px;width:100%" alt="A mini560 buck converter" />

A buck converter is a DC-to-DC power converter and you use it to step down voltage from its input to its output.
The 5A mini560 step-down module has high conversion efficiency and low heat generation.

#### Toggle switch

<img src="../img/viam-rover/toggle-switch.jpg" style="max-width:400px;width:100%" alt="A toggle switch" />

The toggle switch comes wired to the rover and you use it to turn the power on and off.

#### Battery pack

<img src="../img/viam-rover/battery-pack.jpg" style="max-width:400px;width:100%" alt="A battery pack" />

The rover comes with a battery holder.
You must purchase four 18650 batteries (and their charger) separately.
The battery holder also has a female jack for an external DC power supply.

### What's not inside the kit

You must purchase the following pieces of hardware separately:

#### [Raspberry Pi 4 single board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)

<img src="../img/viam-rover/pi4.jpg" style="max-width:400px;width:100%" alt="Raspberry Pi 4" />

Any Raspberry Pi 4 works as long as it runs the 64-bit Raspberry Pi OS.

#### MicroSD card and an adapter/reader

In addition to the microSD card, you also need an internet-connected computer and a way to connect the microSD card to the computer (for example, a microSD slot or microSD adapter/reader).

#### Four 18650 batteries with a charger

An 18650 battery is a lithium-ion rechargeable battery.
We recommend the button-top type, though either button or flat top can work.
We have used batteries approximately 67.5mm in length, but the battery housing includes a spring to accommodate most batteries of that approximate length.
Any brand is suitable as long as you comply with the battery safety requirements.

Check the [safety](#safety) section for more information.

## Safety

Read all instructions fully before using this product.

This product is not a toy and is not suitable for children under 12.

Switch the rover off when not in use.

Warning: Lithium-ion batteries may pose a flammable hazard.
This product requires four 18650 lithium-ion batteries.
Refer to the battery manufacturer’s operating instructions to ensure safe operation of the Viam Rover.
Dispose of lithium-ion batteries per manufacturer instructions.

Warning: Damage may occur to the Raspberry Pi and/or Viam Rover if wired incorrectly.
Refer to the manufacturer’s instructions for correct wiring.

Disclaimer: This product is preliminary and experimental in nature, and is provided “AS IS” without any representation or warranty of any kind.
Viam does not make any promise or warranty that the product will meet your requirements or be error free.
Some states do not allow the exclusion or disclaimer of implied warranties, so the above exclusions may not apply to you.

## Setup

In short, you will work through the following steps.
More detailed instructions are found in the sections below.

1. Install Raspberry Pi OS and viam-server on the microSD card.
   Put it in your Pi’s slot.
2. Unscrew the top of the rover.
3. Screw the Pi to the base.
4. Wire your Pi to the motor controller and accelerometer (following the instructions in the next section).
5. Connect all the jumper wires and the USB camera.
   Make sure that the camera is on the same side of the rover as the wheels as you attach it.
6. Screw the top of the rover back on.

### Install Raspberry Pi OS and viam-server

Install the 64-bit Raspberry Pi OS using the [Raspberry Pi imager](https://www.raspberrypi.com/software/) and then install viam-server.
For more detailed instructions, check out our Raspberry Pi [installation guide](/installation/rpi-setup/).

### Attach the Raspberry Pi to the Rover

Once you have installed Raspberry Pi OS and viam-server on your SD card, and put your SD card in the slot on your Pi, you can screw the Raspberry Pi to the rover.
The rover's design allows you to reach the SD card slot at all times, so you can pop the SD card in and out whenever you need to.

The Viam Rover kit includes four screws for mounting the Raspberry Pi.
Look for them in a small plastic bag.
You can screw them into the designated spots on the rover to attach the Raspberry Pi to the rover.
The image below shows the four mounting holes for the Pi, circled in red.
Your Rover comes with four hex pegs that you can mount the Pi on.

<img src="../img/viam-rover/topless-rover.jpg" style="max-width:500px;width:100%" alt="The Viam Rover base with the top removed. The motors, chips and wires are exposed." />

### Connect the wires

![Closeup of the wiring diagram, showcasing the Pi, motor driver, accelerometer, and buck converter, wired according to the table below.](../img/viam-rover/wiring-diagram.png)

This diagram shows the acceleration tilt module, the DC motor driver, and the Raspberry Pi and how you need to connect the wires.
The following pinout corresponds to the diagram:

| Component | Component Pin | Raspberry Pi Pin | Wire Color |
| --------- | --- | ---------------- | ---------- |
| Buck Converter | GND | 39 | black |
| Buck Converter | 5V | 4 | red |
| Acceleration Tilt Module | GND | 34 | black |
| Acceleration Tilt Module | 3.3V power | 17 | red |
| Acceleration Tilt Module | SDA | 3 | maroon |
| Acceleration Tilt Module | SCL | 5 | pink |
| DC Motor Driver | En B | 22 | gray |
| DC Motor Driver | In 4 | 18 | yellow |
| DC Motor Driver | In 3 | 16 | white |
| DC Motor Driver | In 2 | 13 | green |
| DC Motor Driver | In 1 | 11 | blue |
| DC Motor Driver | En A | 15 | purple |
| DC Motor Driver | GND | 6 | black |
| DC Motor Driver | Encoder Left | 35 | yellow |
| DC Motor Driver | 3.3V power | 1 | red |
| DC Motor Driver | Encoder Right | 37 | white |

ENA and ENB pins have little plastic jumpers that needs to get removed before wiring.

![Wiring diagram showcasing the Pi, motors, driver, camera, and all other rover components.](../img/viam-rover/wiring-diagram-rover.png)

<img src="../img/viam-rover/rover-with-pi.jpg" style="max-width:600px;width:100%" alt="the Pi, motors, driver, and all other rover components" />

### Extensibility

Due to the aluminum chassis and its expandable mounting features, you can extend the Viam Rover.
With it, you can customize your rover by mounting additional sensors, lidar, robot arms...
The following are just a few ideas, but you can expand or modify the rover kit with any components you want.

For GPS navigation, we support NMEA (via serial and I<sup>2</sup>C) and RTK.
Make and model don't make a difference as long as you use these protocols.
See [Movement Sensor Component](/components/movement-sensor) for more information.

For lidar, we recommend Velodyne, or RPLIDAR (including A1, which is a sub-$100 LIDAR).

For robot arms, we tried the [Yahboom DOFBOT robotics arm](https://category.yahboom.net/products/dofbot-jetson_nano) with success.

## Next Steps

- [Add the Viam Fragment to your Robot](/try-viam/rover-resources/rover-tutorial-fragments/)
