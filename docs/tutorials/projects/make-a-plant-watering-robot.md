---
title: "Plant Watering Robot with a Raspberry Pi"
linkTitle: "Plant Watering Robot"
type: "docs"
description: "Create a plant watering robot with a Raspberry Pi."
tags: ["raspberry pi", "app", "board", "motor"]
imageAlt: "Picture of the plant watering robot"
images: ["/tutorials/plant-watering-pi/preview.png"]
authors: ["Sierra Guequierre"]
languages: ["python"]
viamresources: ["board", "motor", "sensor", "module"]
platformarea: ["core"]
level: "Intermediate"
date: "2023-03-29"
# updated: "2025-05-15"
cost: 150
no_list: true
# SMES: Olivia Miller, Sierra Guequierre
---

<!-- LEARNING GOALS:
After this tutorial you will understand what modules are and when to use them, and be able to build a machine from start to finish. You will be able to create machines using built-in resources as well as resources from the Viam Registry, and can write code with the SDKs to operate your machine.

Notes:
possibly extend or point to data management tutorial next? To Jessamy's in particular? and the grafana tutorial
-->

![Picture of the plant watering robot on a desk.](/tutorials/plant-watering-pi/plant-watering-robot.png)

Building a useful robot doesn't have to require complicated code or expensive equipment.
With a Raspberry Pi and some cheap, basic hardware, you can keep your plants healthy and happy from anywhere in the world!

Follow this tutorial to learn how to set up an automatic plant watering system:

1. [Complete the physical assembly and wiring](#set-up-your-plant-watering-robot).
2. [Create and connect to the robot, and configure your robot's components](#configure-the-components-of-your-robot-in-the-viam-app).
3. [Configure the ADC as a module from the registry](#configure-the-adc-as-a-module-from-the-registry).
4. [Write code utilizing the Viam Python SDK to control the plant watering robot](#add-python-control-code).

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/Q6UuUKJpDn0?start=877">}}

You can also follow a simplified version of this tutorial in this video: it eliminates the need for the ADC and the breadboard, instead using the digital pin of the moisture sensor to get “high” and “low” readings and to turn a relay on and off.
You can start with this simple version and then add the ADC to make your machine more accurate!

The tutorial uses the following hardware, but you can adjust it as needed:

- A Raspberry Pi 3B or 4B with SD card and [5V USB power supply](https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Listed/dp/B00MARDJZ4)
- A [resistive soil moisture sensor](https://www.amazon.com/KeeYees-Sensitivity-Moisture-Watering-Manager/dp/B07QXZC8TQ)
- A [5V mini water pump](https://www.amazon.com/gp/product/B09TGK9N5Q/) with clear vinyl tube
- A [MCP3008 ADC](https://a.co/d/csRaIHE)
- A [one channel relay switch](https://www.amazon.com/HiLetgo-Channel-optocoupler-Support-Trigger/dp/B00LW15A4W/)
- A [breadboard](https://www.amazon.com/SunFounder-Raspberry-Breadboard-solderless-Circuit/dp/B07ZYR7R8X)
- Assorted [breadboard jumper wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY/), including two [splicing connectors](https://www.amazon.com/Splicing-Connector-Lever-Nut-Assortment-Pocket/dp/B07NKSHVF6)
- A planter box or flower pot
- A water container
- A screwdriver

Before starting this tutorial, follow the [Raspberry Pi Setup Guide](/operate/reference/prepare/rpi-setup/) to prepare your machine to run `viam-server`.
Connect your Pi to its power supply to power it on.
Make sure your Pi is flashed with a Viam-compatible operating system, and that you are able to SSH into it.

## Set up your plant watering robot

Before programming the machine, you need to physically set up the plant watering robot by wiring the different components together.
You will set up the robot to receive signals from the resistive soil moisture sensor and signal to the peristaltic pump when it is time to pump water from the water container to the plant container.

### Full wiring diagram

Refer back to this diagram as you complete the steps to wire your hardware.
Turn your Pi off while you are wiring the hardware.

<p><img src="../../plant-watering-pi/full-wiring.png" class="imgzoom" alt="The full wiring diagram for all the hardware for the Plant Watering Robot."></p>

### Wire your ADC

The analog-to-digital converter (ADC) converts the resistive soil moisture sensor's analog readings to digital signals that can be processed by your machine, which expects digital signals to come to it through its GPIO pins.

Start by wiring your ADC to your machine.

You can find a Raspberry Pi pinout diagram at [pinout.xyz](https://pinout.xyz).
Reference the following pinout diagram for your MCP3008 analog-to-digital converter:

![Pinout diagram for the ADC.](/tutorials/plant-watering-pi/adc-pinout.png)

{{% alert title="Tip" color="tip" %}}
The half circle shown in the pinout diagram above should be physically present on your ADC.
Use this to orient the ADC to determine the location to insert your wires.
{{% /alert %}}

Insert the MCP3008 into your breadboard so that it bridges both sides of the divide.
Now you can use the breadboard points next to the MCP3008 to connect pins on the MCP3008 to your Raspberry Pi and other peripherals using jumper wires.
Begin by connecting MCP3008 pins to your Raspberry Pi:

<!-- prettier-ignore -->
| MCP3008 ADC Pin | Raspberry Pi Pin |
| ----------- | ---------------- |
| CLK | SCLK |
| DOUT | MISO |
| DIN | MOSI |
| CS/SHDN | 24GPIO8 |

Next, connect MCP3008 pins to the ground and power rails on the breadboard:

<!-- prettier-ignore -->
| MCP3008 ADC Pin | Breadboard |
| ----------- | ---------------- |
| VDD | Any point on 5V power rail (red +) |
| VREF | Any point on 5V power rail (red +) |
| AGND | Any point on GND rail (blue -) |
| DGND | Any point on GND rail (blue -) |

Finally, connect your breadboard rails to 5V power and ground on the Raspberry Pi:

<!-- prettier-ignore -->
| Breadboard rail | Raspberry Pi pin |
| ----------- | ---------------- |
| Any point on 5V power rail (red +) | [Pin 4 (a 5 volt power pin)](https://pinout.xyz/pinout/5v_power) |
| Any point on GND rail (blue -) | [pin 34 (a ground pin)](https://pinout.xyz/pinout/ground) |

### Wire your resistive soil moisture sensor

Next, wire your [resistive soil moisture sensor](https://www.amazon.com/KeeYees-Sensitivity-Moisture-Watering-Manager/dp/B07QXZC8TQ) to your Pi and ADC.

Reference this diagram of the blue module part of the sensor:

![Pinout diagram for the resistive soil moisture sensor.](/tutorials/plant-watering-pi/moisture-sensor-pinout.png)

Start by connecting the female jumper wires at the end of the sensor prongs to the blue module where the diagram shown above is labeled "Connect with Probe."
Be careful of the positive and negative sides, and make sure to match them correctly.

Then, wire the rest of the pins on the module to the breadboard as follows:

<!-- prettier-ignore -->
| Moisture Sensor Pin | Breadboard |
| ----------- | ---------------- |
| A0 (Analog Signal Output) | CH0 |
| VCC | Any point on 5V power rail (red +) |
| GND | Any point on GND rail (blue -) |

Put the soil moisture sensor inside of the container holding your plant.

### Wire your pump

Now, wire and power your pump and relay module to complete your hardware setup:

1. Use a [splicing connector](https://www.amazon.com/Splicing-Connector-Lever-Nut-Assortment-Pocket/dp/B07NKSHVF6) to connect your 5V pump motor's positive wire to a jumper wire, and connect it to the NO pin on the relay module.
   NO stands for normally open, which will keep the circuit open unless the pin is triggered.
2. Use a [splicing connector](https://www.amazon.com/Splicing-Connector-Lever-Nut-Assortment-Pocket/dp/B07NKSHVF6) to connect your 5V pump motor's negative wire to a jumper wire, and connect it to [pin 39 (ground)](https://pinout.xyz/pinout/ground) on the Raspberry Pi.
3. Connect the COM (common) pin on the relay to [pin 2 (5V)](https://pinout.xyz/pinout/5v_power) on the Pi.
4. Connect the DC+ pin on the relay to [pin 1 (3.3V)](https://pinout.xyz/pinout/3v3_power) on the Pi.
5. Connect the DC- pin on the relay to [pin 14 (ground)](https://pinout.xyz/pinout/ground) on the Pi.
6. Connect the IN pin on the relay to the [pin 8 (GPIO 14)](https://pinout.xyz/pinout/pin8_gpio14) on the Pi.

{{% alert title="Tip" color="tip" %}}

To complete the steps, insert the ends of the jumper wires into the pin gates on the relay module and tighten the screws on these gates with your screwdriver to close the wires inside.

{{% /alert %}}

## Program your plant watering robot

{{<gif webm_src="/tutorials/plant-watering-pi/plant-watering-video.webm" mp4_src="/tutorials/plant-watering-pi/plant-watering-video.mp4" alt="The plant watering robot on a white desk. Camera goes up to the watering tube and pulls it out, showing the drip.">}}

### Enable SPI on your machine

Now that you have wired your ADC and moisture sensor, make sure that the Serial Peripheral Interface (SPI) is enabled on your machine.
This protocol allows your machine to communicate with the moisture sensor peripheral.

Turn your machine back on.
SSH into your machine and run the following command:

```shell
sudo raspi-config
```

Once the `raspi-config` interface is open, navigate to **Interface Options**:

![Raspi-config Tool interface with Interface Options selected.](/tutorials/plant-watering-pi/interface-options.png)

Then, select **SPI**:

![Raspi-config Tool interface with SPI selected.](/tutorials/plant-watering-pi/spi.png)

Now, select **Yes** to enable SPI:

![Raspi-config Tool interface with Yes selected for SPI enablement.](/tutorials/plant-watering-pi/spi-enabled.png)

Finally, select **Finish**.
Restart your machine using `sudo reboot` to make these changes take effect.

### Configure the components of your robot in the Viam app

{{% snippet "setup.md" %}}

Then, navigate to the **CONFIGURE** tab of your new machine's page in the app.

First, add your machine as a [board component](/operate/reference/components/board/):

{{< tabs name="Configure a Raspberry Pi Board" >}}
{{% tab name="Config Builder" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `board` type, then select the appropriate `viam:raspberry-pi:pi` model (for example, `viam:raspberry-pi:pi4` for Raspberry Pi 4).
Enter a name for your board and click **Create**.
This tutorial uses the name `local`.

![Creation of a board in the Viam app config builder.](/tutorials/plant-watering-pi/pi-board-config-builder.png)

{{% /tab %}}
{{% tab name="JSON" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

#### Configure the ADC as a module from the registry

_Resources_ refer to the different {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} Viam provides for robots to use.
_Components_ refer to types of hardware, and each component's built-in `models` support the most common models of this hardware.
For example, the [sensor component](/operate/reference/components/sensor/) has an `ultrasonic` model built in for the ubiquitous [ultrasonic sensor](https://www.sparkfun.com/products/15569).

However, there are many different types of sensors used for sensing different things across the [Internet of Things](https://medium.com/@siddharth.parakh/the-complete-list-of-types-of-sensors-used-in-iot-63b4003ab6b3).
Although the resistive soil moisture sensor is not currently one of Viam's built-in models, you can add an analog-to-digital-converter (ADC) as a module and use it to get readings from the moisture sensor.

A _module_ provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, which add resource types ({{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}}) or models that are not built into Viam.
A module can be added to your robot from the Viam Registry.

The [Viam Registry](https://app.viam.com/registry) allows hardware and software engineers to collaborate on their robotics projects by writing and sharing custom modules with each other.
You can add a module from the Viam Registry directly from your robot’s **CONFIGURE** tab in the Viam app, using the **+** (Create) button.

To add the mcp300x-adc-sensor module to your robot, follow these steps:

1. Go to your machine's **CONFIGURE** tab.
   Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
1. Search for `mcp300x` and select `sensor / mcp300x`.
   Click **Add module**.
1. Give your module a name of your choice. We used the name `sensor`.
1. Click **Create** to add this module to your machine.
1. Find your module's card on the **CONFIGURE** page.
   Copy the following JSON object into the configuration field.

   ```json
   {
     "channel_map": {
       "moisture": 0
     },
     "sensor_pin": 8
   }
   ```

   `sensor_pin` is the GPIO pin number of the machine's pin you connected to the MCP300x chip.
   If you followed the wiring in this tutorial, this will be `8` which is pin 24, GPIO 8 (SPI Chip Select 0).
   Otherwise if you are using CS1, use `7`.

Save your config by clicking **Save** in the top right corner of the page.

On the sensor configuration panel, click on the **TEST** area to confirm you can get readings from your sensor.

This module allows you to get multiple readings at the same time from different channels of the ADC sensor.
If you wire and configure another sensor, such as a temperature sensor on channel 1, you can add the sensor to the `"channel_map"` and get a reading from it.

{{< alert title="Info" color="info" >}}
If you would like to see how the module works, you can find its code on [GitHub](https://github.com/viam-labs/mcp300x-adc-sensor).
{{< /alert >}}

Now that you have set up your robot, you can put the suction tube of your pump into the water cup, and the output tube into the plant!

### Install the Python SDK

Make sure any packages on your Pi are up to date, while connected to your Pi with SSH run:

```shell {class="command-line" data-prompt="$"}
sudo apt update
sudo apt upgrade
```

Then run the following command to create and activate the virtual environment:
If you want to read more on virtual environments, check out [the documentation](/dev/reference/sdks/python/python-venv/).

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
```

Make sure you have `pip` installed for Python 3:

```shell {class="command-line" data-prompt="$"}
pip --version
```

If not, run the following command:

```shell {class="command-line" data-prompt="$"}
sudo apt install python3-pip
```

Run the following command to install the SDK:

```sh {class="command-line" data-prompt="$"}
pip3 install viam-sdk
```

### Add Python control code

Follow these instructions to start working on your Python control code:

1. Navigate to your machine's page in the [Viam app](https://app.viam.com), and click on the **CONNECT** tab and the **Code sample** page.
2. Select **Python** as the language.
3. Follow the instructions shown under step 1 on that page to install the SDK.
4. Then, under step 2 on that page, click the copy icon to copy the generated code sample, which establishes a connection with your robot when run.

   {{% snippet "show-secret.md" %}}

5. Paste this code sample into a new file on your machine.
6. Name the file <file>plant-watering-robot.py</file>, and save it.

Run the following commands on your machine to create and open the file:

```shell
source .venv/bin/activate
touch plant-watering-robot.py
nano plant-watering-robot.py
```

Now, you can add code into <file>plant-watering-robot.py</file> to write the logic that defines your plant watering system.

To start, add your system logic code into the `main()` function of the program.
Use the Viam [board](/dev/reference/apis/components/board/) and [sensor](/dev/reference/apis/components/sensor/) API methods to read from the moisture sensor and control the pump's voltage with PWM as a GPIO pin.

You can get your components from the robot like this:

```python
# Note that this name, `sensor`, is defined when you add the mcp300x module
sensor = Sensor.from_robot(robot=robot, name='sensor')
# Note that this name, `local`, is defined when you add the board
local = Board.from_robot(machine, "local")
```

Then, add a control loop that runs continuously, similar to the following example:

```python
while True:
    # this level depends on your specific setup, replace after testing

    is_not_moist = 600

    # Get the moisture sensor's readings
    readings = await sensor.get_readings()
    soil_moisture = readings.get('moisture')

    # Calculate the average moisture reading from the list of readings
    # to account for outliers
    avg_moisture = sum(soil_moisture) / len(soil_moisture)

    # If the average moisture reading indicates moisture, trigger pump
    # watering
    if (avg_moisture > is_not_moist):
        print('this plant is too thirsty! giving it more water')

        # Get the GPIO pin with PWM output (pin number 8) the water pump is
        # wired to on the board through the relay's IN wire
        pwm_pin = await local.gpio_pin_by_name(name="8")

        # Run the water pump
        # Set the duty cycle to .8, meaning that this pin will be in the
        # high state, powering the pump motor, for 80% of the duration of the
        # PWM interval period
        await pwm_pin.set_pwm(duty=0.8)

        # Wait for 15 seconds
        print('watering')
        time.sleep(15)

        # Stop the pump by setting the duty cycle to 0%
        await pwm_pin.set_pwm(duty=0.0)

        # Wait 60 seconds so that the water can soak into the soil a bit before
        # trying to water again
        print('waiting a little bit for the water to soak in')
        time.sleep(60)
```

{{% alert title="Tip" color="tip" %}}
Make sure to import `time` at the top of <file>plant-watering-robot.py</file> to be able to use `sleep()`!
{{% /alert %}}

### Test motor

On your machine's **CONTROL** page in the Viam app, expand the **TEST** card for your board component. You should see a panel that allows you to control individual GPIO pins.

Enter `8` as a GPIO number. Set a decimal value between 0 and 1, (for example 0.8), to activate the motor and begin pumping water. Set a value of 0 to turn the motor off and stop pumping water.

### Test moisture sensor

On your machine's **CONTROL** page in the Viam app, expand the **TEST** card for your sensor to see a live observed value from your moisture sensor.
Test your sensor by putting it in air, water, and soils containing different amounts of moisture.
Use these observed values to determine an appropriate `is_not_moist` value for your setup.

### Save control code

Save <file>plant-watering-robot.py</file> with this logic added in, and then run it on your machine with the following command:

```shell {class="command-line" data-prompt="$"}
sudo python3 plant-watering-robot.py
```

## Next steps

Now that you have created your automatic plant watering system with a resistive soil moisture sensor, you can easily use Viam to automate other aspects of your garden.
For example, you can use a [light sensor](https://www.amazon.com/Sensor-Module-Raspberry-Integrated-Circuits/dp/B07L15M5JG) or a [temperature sensor](https://www.amazon.com/KY-011-Cathode-Arduino-Starter-2-color/dp/B07869PKKF/ref=as_li_ss_tl?keywords=arduino+two+color+led+module&qid=1556591832&s=gateway&sr=8-2&th=1&linkCode=sl1&tag=murraynet-20&linkId=c36cd98be29498a9883b656c7011b6bb&language=en_US), and get readings from other channels of the MCP3008!

You could set up data capture and [graph your sensor data](/tutorials/services/visualize-data-grafana/), or [create your own custom Typescript dashboard](/tutorials/control/air-quality-fleet/) to display your sensor data.

If you build something based on this please share it in our [Community Discord](https://discord.gg/viam) - we'd love to see it.
