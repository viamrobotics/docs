---
title: "Unbox and Set Up your Viam Rover 2"
linkTitle: "Unbox and Set Up your Viam Rover 2"
weight: 10
type: "docs"
tags: ["rover", "tutorial"]
images: ["/get-started/try-viam/rover-resources/viam-rover-2/box-contents.png"]
imageAlt: "A Viam Rover 2 in a box"
description: "A list of the contents of the Viam Rover 2 kit, instructions for wiring your rover, and links for additional hardware."
no_list: true
---

{{% alert title="Tip" color="tip" %}}
Another version of the Viam Rover was sold until January 2024.
If you have purchased a Viam Rover 1, follow [these instructions](/get-started/try-viam/rover-resources/rover-tutorial-1/) instead.
{{% /alert %}}

The [Viam Rover 2](https://www.viam.com/resources/rover) arrives preassembled with two encoded motors with suspension, a webcam with a microphone unit, a 6 axis IMU, power management and more.
It is primarily designed for use with a Raspberry Pi 4.
You can use it with [other types of boards](#motherboard) with some additional setup.

{{< alert title="Important" color="note" >}}
You must purchase the following hardware separately:

- A Raspberry Pi 4
- Four 18650 batteries (with charger) or a RC type battery with dimensions no greater than 142mm x 47mm x 60mm (LxWxH) (with charger)
- A MicroSD card and an adapter/reader
  {{< /alert >}}

This guide covers what's inside the kit and provides instructions for [setting up your rover](#setup).

{{< alert title="Note" color="note" >}}
The design for this rover is open source.
Find the details on [GitHub](https://github.com/viamrobotics/Viam-Rover-2).
{{< /alert >}}

## What's inside the kit

1. One assembled Viam Rover.

   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/rover-side.png" resize="400x" declaredimensions=true alt="The side of the assembled Viam Rover">}}

1. Four M2.5 screws for mounting your Raspberry Pi.

   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover/screws.jpg" resize="200x" declaredimensions=true alt="Four screws" >}}

1. Two spare stiffer suspension springs.
   You can swap them out with the springs that come with the rover if you need stiffer suspension for higher payload applications.

   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover/suspension-springs.jpg" resize="200x" declaredimensions=true alt="Two suspension springs" >}}

1. Three different Allen wrenches (1.5 mm, 2 mm, and 2.5 mm) to unscrew the top and mount the Raspberry Pi.

   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover/allen-wrenches.png" resize="180x" alt="Three allen wrenches" >}}

1. Four extenders to increase the height of the rover to house larger internal single-board computers (such as a Jetson Orin Nano).

   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/extenders.png" resize="400x" declaredimensions=true alt="Four extenders" >}}

1. Ribbon cable for connecting the Raspberry Pi 4 to the Viam Rover 2 printed circuit board.

   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/ribbon-cable.png" resize="400x" declaredimensions=true alt="Ribbon cable" >}}

All together, your kit looks like this:

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/box-contents.png" resize="400x" declaredimensions=true alt="A Viam Rover shipping box contents" >}}

## Rover components

### Dual drive motors with suspension and integrated motor encoders

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover/encoder-motors.jpg" resize="400x" declaredimensions=true alt="two motors with encoders" >}}

The motors come with integrated encoders.
For information on encoders, see [Encoder Component](/components/encoder/).
For more information on encoded DC motors, see [Encoded Motors](/components/motor/gpio/encoded-motor/).

The kit also includes stiffer suspension springs that you can substitute for the ones on the rover.
Generally, a stiff suspension helps with precise steering control.
In contrast, a soft suspension allows the wheels to move up and down to absorb small bumps on the rover's path.

### Motor driver

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover/motor-driver.png" resize="400x" declaredimensions=true alt="A L298N motor driver" >}}

The kit comes with an L298N driver dual H-Bridge DC motor driver.
L298 is a high voltage and high current motor drive chip, and H-Bridge is typically used to control the rotating direction and speed of DC motors.

### 720p webcam with integrated microphone

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover/webcam.jpg" resize="400x" declaredimensions=true alt="Webcam with cables" >}}

The webcam that comes with the kit is a standard USB camera device and the rover has a custom camera mount for it.
For more information, see [Camera Component](/components/camera/).

### Motherboard

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/motherboard.png" resize="400x" declaredimensions=true alt="Viam rover 2 motherboard" >}}

The Viam Rover 2 utilizes a motherboard to which all ancillary components (buck converter, motor driver, IMU, INA219) are mounted.
This board includes an auxiliary Raspberry Pi 4 pinout that dupont connectors can be connected to, an auxiliary power input terminal, 5V, 3.3V and Ground pins.

The motherboard also incorporates hole patterns for the following alternative single-board computers:

- Jetson Nano and Orin Nano
- Rock Pi S
- Raspberry Pi Zero 2W
- Raspberry Pi 4
- Orange Pi Zero 2

See [Alternative Board Configurations](#alternative-board-configurations) for a diagram of this.
Note that these boards require additional parts to be purchased and will not work out of the box with the Viam Rover 2.

### 6DOF IMU

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/mpu6050.png" resize="400x" declaredimensions=true alt="An MPU6050 gyroscope" >}}

The MPU6050 sensor is a digital 6-axis accelerometer or gyroscope that can read acceleration and angular velocity.
You can access it through the I2C digital interface.
You configure it with Viam on your machine as a [movement sensor](/components/movement-sensor/mpu6050/).

### INA219 power monitoring unit

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/ina219.png" resize="400x" declaredimensions=true alt="An INA219 unit" >}}

The INA219 unit measures the voltage and current from the power supply.
You can use it to measure battery life status and power consumption.
It connects to the Raspberry Pi 4 through the I2C bus.
You configure it with Viam on your machine as a [power sensor](/components/power-sensor/ina219/).

### DC-DC 5V converter

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/buck-converter.png" resize="300x" declaredimensions=true alt="A OKY3502-4 buck converter" >}}

The DC-to-DC power converter, or, buck converter, steps down voltage from its input to its output.
The OKY3502-4 has a USB output that can provide an additional 5V supply to auxiliary components.

### Switch and low voltage cutoff circuit

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/slide-switch.png" resize="400x" declaredimensions=true alt="The switch mounted on the Viam rover 2" >}}

A slide switch is connected to the rover.
Use it to turn the power on and off.

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/circuit.png" resize="400x" declaredimensions=true alt="Low-voltage cutoff circuit" >}}

Mounted above the switch is a low voltage cutoff circuit that can be set to turn off power to the rover when the input voltage drops below a pre-set threshold.
This can be helpful for preventing batteries fully discharging which can damage lithium ion batteries.

### Battery holders

The Viam Rover 2 comes with two battery holder options.
The rover nominally operates with four 18650 batteries, but a higher capacity RC-type battery can be mounted into the rear of the rover.

{{% alert title="Note" color="note" %}}
With either battery option, you must purchase a charger separately.
{{% /alert %}}

#### 18650 battery pack

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/battery-pack.png" resize="400x" declaredimensions=true alt="A battery pack" >}}

18650 batteries are the nominal power supply recommended for use with the Viam Rover 2.
An 18650 battery is a lithium-ion rechargeable battery.
We recommend the button-top type, though either button or flat top can work.
Any brand is suitable as long as you comply with the battery safety requirements.

#### Mount for RC-type battery

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/RC-mount.png" resize="400x" declaredimensions=true alt="RC battery mount" >}}

You can mount a larger capacity RC-type battery into the rover.
You must wire the appropriate connecter into the switch circuit.

RC-batteries are lithium-ion rechargeable batteries.
Caution should always be taken when using such batteries, always comply with the battery safety requirements.
Check the [safety](#safety) section for more information.

## Safety

Read all instructions fully before using this product.

This product is not a toy and is not suitable for children under 12.

Switch the rover off when not in use.

{{< alert title="Warning" color="warning" >}}
Lithium-ion batteries may pose a flammable hazard.
This product requires four 18650 lithium-ion batteries OR an RC-type battery.
DO NOT connect multiple power sources simultaneously.
Refer to the battery manufacturer’s operating instructions to ensure safe operation of the Viam Rover.
Dispose of lithium-ion batteries per manufacturer instructions.
{{< /alert >}}

{{< alert title="Caution" color="caution" >}}
Damage may occur to the Raspberry Pi and/or Viam Rover if wired incorrectly.
Refer to the manufacturer’s instructions for correct wiring.
{{< /alert >}}

Disclaimer: This product is preliminary and experimental in nature, and is provided "AS IS" without any representation or warranty of any kind.
Viam does not make any promise or warranty that the product will meet your requirements or be error free.
Some states do not allow the exclusion or disclaimer of implied warranties, so the above exclusions may not apply to you.

## Setup

{{% alert title="Important" color="tip" %}}
If you wish to use a Jetson Nano or Jetson Orin Nano, follow [this guide](./jetson-rover-setup/) instead.
{{% /alert %}}

### Install Raspberry Pi OS

{{% alert title="Tip" color="tip" %}}
If you are using another board, you can skip this step.
{{% /alert %}}

Install a 64-bit Raspberry Pi OS onto your Pi following our [Raspberry Pi installation guide](/get-started/prepare/rpi-setup/).
Follow all steps as listed, including the final step, [Enable communication protocols](/get-started/prepare/rpi-setup/#enable-communication-protocols), which is required to enable [the accelerometer](#6dof-imu) on your rover.
Once you have installed Raspberry Pi OS and `viam-server`, put your SD card in the slot on your Pi.

### Add the power supply

You can power the Viam Rover 2 using 18650 batteries or RC-type batteries.
18650 batteries are the nominal power supply recommended for use with the rover, but RC-type batteries are higher capacity.

{{< tabs >}}
{{% tab name="18650 Batteries" %}}

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/rover-underview.png" resize="400x" declaredimensions=true alt="Under view of rover with battery pack." >}}

The Viam Rover 2 arrives with the 18650 battery pack wired into the power input terminal block.
The battery pack works with batteries 67.5 mm in length, but the battery housing includes a spring to accommodate most batteries of that approximate length.

- Turn the rover over so that you can see the battery housing.
- Place four 18650 batteries (taking care to ensure correct polarity orientation) inside the battery pack to provide power to the rover, which can be turned on and off through the power switch.

{{% alert title="Tip" color="tip" %}}
Ensure that the batteries are making contact with the terminals inside the battery pack.
Some shorter batteries might need to be pushed along to ensure that contact is being made.
{{% /alert %}}

{{% /tab %}}
{{% tab name="RC-Type Battery" %}}

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/rcbattery-underneath.png" resize="400x" declaredimensions=true alt="Under view of rover with battery pack." >}}

For users who prefer a higher capacity battery option, the Viam Rover 2 can house RC-type batteries that do not exceed the following dimensions:- 142mm x 47mm x 60mm (LxWxH).
Using a RC-type battery requires some re-wiring of the Viam Rover 2 which should only be undertaken by users who are comfortable handling electrical assemblies.
Improper configuration of the power supply could result in damage to the battery and poses a fire hazard.
A 4-S RC-type battery is recommended (14.8V).
We make no recommendations regarding specific RC battery brands.

To change the rover's power supply configuration for a RC-battery:

1.  Ensure the 18650 battery holder contains no batteries
2.  Unscrew the 18650 battery leads from the power input terminal.
    Move these wires out of the way.
3.  Screw in a power lead that matches that of the selected battery.
    Common options include: EC-type connectors, XT-connectors or T-plugs.
    Ensure lead is long enough to reach the battery.
4.  Ensure that the polarity is correct (the polarity is marked on the PCB).
    **Failure to do so may result in permanent damage to your Viam Rover 2 when powered on.**
5.  Ensure that there is no short between the terminals (for example, due to a stray strand of wire). Use a multimeter to check continuity across the terminal to verify this.
    Failure to do so may result in damage to the battery and may pose a fire hazard.
6.  Place the battery in the receptacle between the two caster wheels:
    {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/RC-mount.png" resize="400x" declaredimensions=true alt="RC battery mount" >}}
    Connect the battery to the lead that is wired into the power input terminal.
    Although not necessary, slots in the bottom plate of the rover allow a velcro strap to be placed around the battery to secure it.

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Caution" color="caution" %}}
DO NOT connect both power supplies at the same time.
These suggestions are alternative configurations.
Connecting multiple batteries together may result in damage to the batteries and rover, it may also pose a fire hazard.
{{% /alert %}}

### Configure the low voltage cutoff circuit

Now that you have connected your power supply to your rover, you need to configure the [low voltage cutoff circuit](#switch-and-low-voltage-cutoff-circuit).
You must configure two settings:

1.  The low voltage cutoff
2.  The reconnect voltage

The reconnect voltage is the voltage increment above the cutoff point that is needed for the power to reconnect.
For both 18650 and RC-type battery inputs, the nominal voltage is 14.8V, so you should set the low voltage threshold to 14.7.
You can adjust this value if using a battery that has an alternative nominal voltage.

To set the low voltage cutoff and reconnect voltage:

1.  Turn on the circuit using the switch.
    The LED indicater should indicate a current voltage level of 14.8-16V depending on the battery charge status:

    {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/circuit-led.png" resize="300x" declaredimensions=true alt="LED with voltage level displayed on low voltage cutoff circuit" >}}

2.  Hold down the left button until the LED display starts flashing with the low cutoff value.
    The factory default low cutoff value is 12V.
3.  Use the left (+) and right (-) buttons to set the voltage to 14.7V (or whatever you want the cutoff to be).
4.  Wait for the indicator to stop flashing.
5.  Hold down the right button until the LED display starts flashing with the reconnect voltage value. The factory default reconnect voltage is 2.0V.
6.  Use the left (+) and right (-) buttons to set the reconnect voltage to 0.2V.
7.  Wait for the indicator to stop flashing.

Your voltage cutoff circuit is now configured.
When the voltage drops below 14.8V (or reaches the cutoff point you chose), a relay will disconnect the motherboard.
A minimum voltage of 14.9V will be needed to reconnect the power (that is, after charging the batteries).

### Connect the ribbon cable, Pi, and camera

{{% alert title="Tip" color="tip" %}}
If you are using another board, follow the instructions in [Alternative board configurations](#alternative-board-configurations) in place of this step.
{{% /alert %}}

To be able to attach the Raspberry Pi, unscrew the top of the rover with the biggest Allen key.
Then use the smallest Allen key and the provided M2.5 screws to attach the Raspberry Pi to your rover through the standoffs on the motherboard.
The Raspberry Pi 4 should be mounted such that the USB ports are to the right, as viewed from above.

Use the ribbon cable to connect the Raspberry Pi 4 to the motherboard.
The ribbon cable comes connected to the motherboard out of the box, wrap it over the top of the Raspberry Pi 4 and connect with the GPIO pins as shown:

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/ribbon-cable1.png" resize="400x" declaredimensions=true alt="Ribbon cable attached to pi" >}}
<br>
{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/ribbon-cable2.png" resize="400x" declaredimensions=true alt="Ribbon cable attached to pi" >}}

Also, connect the webcam's USB lead to any USB port on your Pi.

Assuming you are using a Raspberry Pi 4, you can skip the following section and move to [Screw the top plate back on and switch the rover on](#screw-the-top-plate-back-on-and-switch-the-rover-on).

### Alternative board configurations

This guide assumes you are using a Raspberry Pi 4, but you can use [different boards](#motherboard) with your Viam Rover 2 with some modifications while attaching the boards.

{{% alert title="Tip" color="tip" %}}
If you are using a Jetson board, you should be following [this guide](./jetson-rover-setup/).
{{% /alert %}}

Reference the appropriate alternative hole pattern provided on the motherboard:

{{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/hole-patterning.png" resize="400x" declaredimensions=true alt="Viam rover 2 motherboard hole patterns" >}}

Detach the motherboard, unscrew the standoffs, and move them to the correct holes.
Then, use the smallest Allen key and the provided M2.5 screws to attach your board to your rover through these standoffs.

If you are using a Raspberry Pi Zero 2W, you should be able to connect your ribbon cable straight to the board.
If not, you will have to take off the ribbon cable and use [dupont connectors](https://www.amazon.com/IWISS-1550PCS-Connector-Headers-Balancer/dp/B08X6C7PZM/) to wire a connection from the motherboard to the single-board computer's GPIO pins.

Then connect the webcam's USB lead to any USB port on your board.

If you need to increase the height of your rover to accommodate your board being larger than a Raspberry Pi 4, place the [height extender standoffs](#whats-inside-the-kit) now.

### Screw the top plate back on and switch the rover on

Screw the top plate back on with the biggest Allen key and use the power switch to turn the rover on.
Wait a second for the low voltage cutoff relay to trip and provide power to the rover motherboard.
If the Pi has power, the lights on the Raspberry Pi will light up.

### Enable I<sup>2</sup>C on your Pi

Enable the I<sup>2</sup>C protocol on your Pi to get readings from the power sensor when controlling your rover.

1. SSH into your Pi.
   Launch the configuration tool by running the following command:

   ```sh {class="command-line" data-prompt="$"}
   sudo raspi-config
   ```

2. Use your keyboard to select **Interface Options**, and press return.
   Select **I2C** enabled.

3. Then, to apply the changes, restart your Raspberry Pi if it hasn't already prompted you to do so.

   ```sh {class="command-line" data-prompt="$"}
   sudo reboot
   ```

### Control your rover on the Viam app

If you followed the instructions in the [Pi installation guide](/get-started/prepare/rpi-setup/), you should have already made an account on the [Viam app](https://app.viam.com), installed `viam-server` on the board, and added a new machine.

If not, make sure to [prepare your device and install `viam-server`](/get-started/installation/), and then [add a new machine](/fleet/machines/#add-a-new-machine).

To configure your rover so you can start driving it, [add a Viam Rover 2 Fragment to your machine](/get-started/try-viam/rover-resources/rover-tutorial-fragments/).

## Next steps

Before you can use your Viam rover with the Viam platform you need to configure your rover:

{{< cards >}}
{{% card link="/get-started/try-viam/rover-resources/rover-tutorial-fragments/" %}}
{{< /cards >}}

After you have configured your rover, follow one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/try-viam-sdk/" %}}
{{% card link="/tutorials/services/basic-color-detection/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}

### Extensibility

Due to the aluminum chassis and its expandable mounting features, you can extend the Viam Rover.
With it, you can customize your rover by mounting additional sensors, lidar, robot arms, or other components.
The following are just a few ideas, but you can expand or modify the rover kit with any components you want:

- For GPS navigation, we support NMEA (using serial and I<sup>2</sup>C) and RTK.
  Make and model don't make a difference as long as you use these protocols.
  See [Movement Sensor Component](/components/movement-sensor/) for more information.
- For [LiDAR laser range scanning](/mobility/slam/cartographer/), we recommend Velodyne, or RPlidar (including A1, which is a sub-$100 LIDAR).
- For robot arms, we tried the [Yahboom DOFBOT robotics arm](https://category.yahboom.net/products/dofbot-jetson_nano) with success.

### Mount an RPlidar to the rover

If you are mounting an RPlidar to your rover, be sure to position the RPlidar so that it faces forward in the direction of travel, facing in the same direction as the included webcam.
For example, if you are using the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to the Rover so that the pointed end of the RPlidar mount housing points in the direction of the front of the Rover.
This ensures that the generated {{< glossary_tooltip term_id="slam" text="SLAM" >}} map is oriented in the expected direction relative to the Rover, with the top of the generated map corresponding to the direction the RPlidar is facing when you initiate mapping.

If you need a mount plate for your RPlidar A1 model, you can 3D print an adapter plate using the following:

- [RPlidar A1 adapter STL](https://github.com/viamrobotics/Viam-Rover-2/blob/main/CAD/RPIidar_adapter_v2.STL)
