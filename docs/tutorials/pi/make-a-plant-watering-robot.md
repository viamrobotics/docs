---
title: "Plant Watering Robot with a Raspberry Pi"
linkTitle: "Watering Robot"
weight: 50
type: "docs"
description: "Create a plant watering robot with a Raspberry Pi single-board computer."
tags: ["raspberry pi", "app", "board", "motor"]
# SMES: Olivia Miller
---

![Picture of the plant watering robot on a desk.](../../img/plant-watering-pi/plant-watering-robot.png)

Building a useful robot doesn't have to require complicated code or expensive equipment.
With a Raspberry Pi and some cheap, basic hardware, you can keep your plants healthy and happy from anywhere in the world!

Follow this tutorial to learn how to set up an automatic plant watering system:

1.  [Complete the physical assembly and wiring](/#set-up-your-plant-watering-robot).
2. [Create and connect to the robot](#configure-the-components-of-your-robot-in-the-viam-app).
3. [Configure your robot's components](#configure-the-components-of-your-robot-in-the-viam-app).
4. [Configure a custom Capacitive Soil Moisture sensor component](#configure-the-capacitive-soil-moisture-sensor-as-a-custom-sensor-component-model).
5. [Write code utilizing the Viam Python SDK to control the plant watering robot](#add-python-control-code).

The tutorial uses the following hardware, but you can adjust it as needed:

- A Raspberry Pi with SD card
- A [Capacitive Soil Moisture Sensor](https://www.amazon.com/KeeYees-Sensitivity-Moisture-Watering-Manager/dp/B07QXZC8TQ/ref=asc_df_B07QXZC8TQ/?tag=hyprod-20&linkCode=df0&hvadid=343238573411&hvpos=&hvnetw=g&hvrand=14606440922488452520&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-757549749596&psc=1&tag=&ref=&adgrpid=71762478951&hvpone=&hvptwo=&hvadid=343238573411&hvpos=&hvnetw=g&hvrand=14606440922488452520&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-757549749596)
- A [Peristaltic Pump](https://www.amazon.com/Gikfun-Peristaltic-Connector-Aquarium-Analytic/dp/B01IUVHB8E/ref=asc_df_B01IUVHB8E/?tag=hyprod-20&linkCode=df0&hvadid=198093101467&hvpos=&hvnetw=g&hvrand=13835398343702336934&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-384674250225&psc=1) motor and [tubing](https://www.amazon.com/dp/B08H1ZD5VZ?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- An [Adafruit MCP3008 ADC](https://www.amazon.com/dp/B00NAY3RB2?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- A [Motor Speed Controller](https://www.amazon.com/CHENBO-Trigger-Adjustment-Electronic-Controller/dp/B099RF72R1/ref=asc_df_B099RF72R1/?tag=hyprod-20&linkCode=df0&hvadid=532384528241&hvpos=&hvnetw=g&hvrand=11376239784428845641&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-1410298730875&th=1)
- A Breadboard
- 9V Battery
- Plant Box
- Water Cup or Box

Before starting this tutorial, follow the [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/) to prepare your Pi to run `viam-server`.
Make sure your Pi is flashed with a Viam-compatible operating system, and that you are able to SSH into it.

## Set Up your Plant Watering Robot

Before programming the Pi to make the plant watering robot functional, you need to physically set up the plant watering robot by wiring the different parts together.
You will set up the robot to receive signals from the capacitive soil moisture sensor and signal to the peristaltic pump when it is time to pump water from the water's box to the plant's box.

### Wire your ADC

The analog-to-digital converter (ADC) between your capacitive soil moisture sensor and Pi converts the analog signals created by the capacitive soil moisture sensor's readings to digital signals that can be processed by your Pi, which expects digital signals to come to it through its GPIO pins.

Start by wiring your ADC to your Raspberry Pi board.

Start by wiring your ADC to your Raspberry Pi board according to the following pinout diagram for your MCP3008 Analog to Digital Converter:

![Pinout diagram for the ADC.](../../img/plant-watering-pi/adc-pinout.png)

Consult your Raspberry Pi's data sheet or [pinout.xyz](https://pinout.xyz/pinout/3v3_power) for your board's pinout diagram.

Wire the pins as follows:

| MCP3008 ADC Pin | Raspberry Pi Pin |
| ----------- | ---------------- |
| VDD | 3.3V |
| VREF | 3.3V |
| AGND | GND |
| DGND | GND |
| CLK | SCLK |
| DOUT | MISO |
| DIN | MOSI |
| CS/SHDN | GPIO25 |

#### Wiring Diagram

![The full wiring diagram for all the hardware for the Plant Watering Robot.](../../img/plant-watering-pi/full-wiring.png)

### Wire your Soil Moisture Sensor

Next, wire your capacitive soil moisture sensor to your Pi and ADC.

Refer to the following pinout diagram for your capacitive soil moisture sensor:

![Pinout diagram for the capacitive soil moisture sensor.](../../img/plant-watering-pi/moisture-sensor-pinout.png)

Wire the pins as follows:

| Pi | ADC |
|--|--|
|<table> <tr><th>Moisture Sensor Pin</th><th>Raspberry Pi Pin</th></tr><tr><td>VCC</td><td>3.3V</td></tr><tr><td>GND</td><td>GND</td></tr> </table>| <table> <tr><th>Moisture Sensor Pin</th><th>MCP3008 ADC Pin</th></tr><tr><td>A0 (Analog Signal Output)</td><td>CH0</td></tr> </table>|

Put the soil moisture sensor inside of your plant box.

Refer to the following full wiring diagram for your hardware setup: [**Wiring Diagram**](#wiring-diagram)

### Wire your Pump

Now, wire and power your Peristaltic Pump [motor](/components/motor/) to complete your hardware setup.

1. Connect your battery to the DC power pins on your motor speed controller.
2. Then, connect the output pins on your motor speed controller to the pump.
3. Connect the GND pin on the pump to the breadboard and terminal.
4. Connect the PWM pin on the pump to [Pin 12](https://pinout.xyz/pinout/pin12_gpio18) of the Pi.
5. Connect the plastic tubing to the pump. Put the suction end inside of your water box, and the output end inside of your plant box.

Refer to the following full wiring diagram for your hardware setup: [**Wiring Diagram**](#wiring-diagram)

## Program Your Plant Watering Robot

### Enable SPI on your Pi

Now that you have wired your ADC and Moisture Sensor, make sure that the Serial Peripheral Interface (SPI) is enabled on your Pi.

SSH into your Pi and run the following command:

``` shell
sudo raspi-config
```

Once the `raspi-config` interface is open, navigate to **Interface Options**:

![Raspi-config Tool interface with Interface Options selected.](../../img/plant-watering-pi/interface-options.png)

Then, select **SPI**:

![Raspi-config Tool interface with SPI selected.](../../img/plant-watering-pi/spi.png)

Now, select **Yes** to enable SPI:

![Raspi-config Tool interface with Yes selected for SPI enablement.](../../img/plant-watering-pi/spi-enabled.png)

Finally, select **Finish**.
Restart your Pi using `sudo reboot` to make these changes take effect.

### Test your Soil Moisture readings on your Pi

Next, install the Adafruit ADC library [`Adafruit_CircuitPython_MCP3xxx`](https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/) on your Pi.

Before installation, make sure any packages on your Pi are up to date:

``` shell
sudo apt update
sudo apt upgrade
```

Make sure you have `pip` installed for Python 3:

``` shell
pip --version
```

If not, run the following command:

``` shell
sudo apt install python3-pip
```

Run the following command while connected to your Pi with SSH to install [`Adafruit_CircuitPython_MCP3xxx`](https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/):

``` shell
sudo pip3 install adafruit-circuitpython-mcp3xxx
```

Create a new directory for your plant watering robot's files and navigate to this directory in your terminal session.
For example, run the following commands:

``` shell
mkdir plant-watering-robot
cd plant-watering-robot
```

After navigating to this directory, create a new Python file called <file>adctesting.py</file> and open up the file.
For example, run the following commands:

``` shell
touch adctesting.py
nano adctesting.py
```

Now, add the following Python code to <file>adctesting.py</file> to test reading values from your capacitive soil moisture sensor through your MCP3008 ADC:

``` python
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D25)

# Create the MCP3008 object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on Pin 0
chan = AnalogIn(mcp, MCP.P0)

print('Reading MCP3008 values, press Ctrl-C to quit...')
while True:
    print('Raw ADC Value: ', chan.value)
    time.sleep(1)
```

Run the code as follows:

``` shell
sudo python3 adctesting.py
```

{{% alert title="Tip" color="tip" %}}

If running this code returns `ImportError: No module named busio`, try again after reinstalling `adafruit-blinka`:

``` shell
sudo pip3 install --force-reinstall adafruit-blinka
```

{{% /alert %}}

Now, you should see the Moisture Sensor values outputted by the MCP3008 in the range of `0` to `1023`.
Test your sensor by putting it in air, water, and different soils to see how the values change.


![Terminal output of capacitive soil moisture sensor values.](../../img/plant-watering-pi/moisture-sensor-output.png)

### Configure the Components of your Robot in the Viam app

Follow [this guide](/installation/install/) to install `viam-server` on your pi, create a new robot, and connect to it on [the Viam app](https://app.viam.com).

Then, navigate to your new robot's page on the app and click on the **CONFIG** tab.

First, add your Pi as a [board component](/components/board/) by creating a new component with **type** `board` and **model** `pi`:

{{< tabs name="Configure an Pi Board" >}}
{{% tab name="Config Builder" %}}

<img src="../../img/plant-watering-pi/pi-board-config-builder.png" alt="Creation of a pi board in the Viam app config builder." style="max-width:800px" />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {},
      "depends_on": []
    }, // Motor JSON ...
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

<br>

Then, add your pump as a [motor component](/components/motor/) by adding a new component with **type** `motor` and **model** `gpio`.

Add your board (in this example, named `local`) to this component's dependencies (`depends_on`) and set the attributes **Max RPM** to `1000` and **PWM**  to `12` (the pin # that you wired the PWM to).

{{< tabs name="Configure an Pump Motor" >}}
{{% tab name="Config Builder" %}}

<img src="../../img/plant-watering-pi/pump-motor-config-builder.png" alt="Creation of a pump motor in the Viam app config builder." style="max-width:800px" />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// Board JSON ... },
{
    "name": "water-pump",
    "type": "motor",
    "model": "gpio",
    "attributes": {
    "pins": {
        "a": "",
        "b": "",
        "dir": "",
        "pwm": "12"
    },
    "board": "local",
    "max_rpm": 1000
    },
    "depends_on": [
    "local"
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

### Configure the Capacitive Soil Moisture Sensor as a Custom Sensor Component Model

As the capacitive soil moisture sensor is not currently one of Viam's built-in [sensor component](/components/sensor/) models, you now must use the Viam Python SDK to configure this sensor as a [custom resource](/program/extend/sdk-as-server/).

In this case, the custom resource is a custom component model that extends the Viam [sensor class](https://python.viam.dev/autoapi/viam/components/sensor/sensor/index.html).
To use the custom component, you create a server using the `viam.rpc.server` class and once the server is running you add the server as a remote part of your `plant-watering-robot`.

If you haven't already, install the Viam Python SDK by following the instructions [here](https://python.viam.dev/).

Navigate to the directory you created when [testing your soil moisture readings](#test-your-soil-moisture-readings-on-your-pi), `plant-watering-robot`, and create a new file, <file>sensor.py</file>.

For example, run the following commands to create and open the file:

``` shell
cd plant-watering-robot
touch sensor.py
nano sensor.py
```

Paste the following code into <file>sensor.py</file>:

```python
import asyncio

from viam.components.sensor import Sensor
from viam.rpc.server import Server

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

class MoistureSensor(Sensor):

   def __init__(self, name: str):
        super(MoistureSensor,self).__init__(name)
        sensor_pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor_pin, GPIO.IN)


    # Implement the Viam Sensor API's get_readings() method
    async def get_readings(self):
        x = 0
        input = []

        # Create the SPI bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # Create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D25)

        # Create the MCP3008 object
        mcp = MCP.MCP3008(spi, cs)

        # Create an analog input channel on Pin 0
        chan = AnalogIn(mcp, MCP.P0)

        while x<10:
            # read adc channel 0
            reading = chan.value
            input.append(reading)
            x+=1

        return input

async def main():
   srv = Server(components=[MoistureSensor("moisture_sensor")])
   await srv.serve()

if __name__ == "__main__":
   asyncio.run(main())
```

You can modify this example code as necessary.

Now, go back to your robot's page on [the Viam app](https://app.viam.com) and navigate to the **CONFIG** tab, then to the **REMOTES** sub-tab.

Add your sensor server as a remote part, called `my-sensor-server`:

{{< tabs >}}
{{% tab name="Config Builder" %}}

<img src="../../img/plant-watering-pi/sensor-remote-config-builder.png" alt="Creation of a custom sensor remote in the Viam app config builder." style="max-width:800px" />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "components": [ board & motor ... ],
"remotes": [
    {
      "name": "my-sensor-server",
      "address": "localhost:9090"
    }
]
```

{{% /tab %}}
{{< /tabs >}}

<br>

Then, navigate to the **PROCESSES** subtab and create a process called `run-sensor-server`:

{{< tabs >}}
{{% tab name="Config Builder" %}}

<img src="../../img/plant-watering-pi/sensor-process-config-builder.png" alt="Creation of a pump motor in the Viam app config builder." style="max-width:800px" />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  // "components": [ board & motor ... ] ,
  // "remotes" [ my-sensor-server ... ] ,
  "processes": [
    {
      "id": "run-sensor-server",
      "log": true,
      "name": "sudo",
      "args": [
        "-u",
        "<my_username>",
        "python",
        "sensor.py"
      ],
      "cwd": "/home/<my_username>/plant-watering-robot"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

### Add Python Control Code

Follow these instructions to start working on your Python Control Code:

1. Navigate to your robot's page in [the Viam app](https://app.viam.com), and click on the **CODE SAMPLE** tab.
Follow the instructions in this tab.
2. Click **COPY CODE** to copy a code sample that establishes a connection with your robot when run.
3. Paste this code sample into a new file in your `plant-watering-robot` directory.
4. Name the file <file>plant-watering-robot.py</file>, and save it.
  
For example, run the following commands to create and open the file:

``` shell
cd plant-watering-robot
touch plant-watering-robot.py
nano plant-watering-robot.py
```

Now, you can add code into <file>plant-watering-robot.py</file> to write the logic that defines your plant watering system.

<img src="../../img/plant-watering-pi/main-py.png" alt="The main.py function from your robot's Code Sample tab, ready to edit." style="max-width:800px" />

<br>
</br>

Use the Viam [motor](/components/motor#api) and [sensor](/components/sensor#control-your-sensor-with-viams-client-sdk-libraries) API methods.
Determine at what [analog value from the Soil Moisture readings](#test-your-soil-moisture-readings-on-your-pi) you want to water your plant, as your thirsty plant's average moisture reading might differ from our example value of `950`.
Also, consider how often you would like to check the moisture levels of the plant, and how long the plant should be watered.

You can get your components from the robot like this:

```python
sensor = Sensor.from_robot(robot=robot, name='moisture_sensor') # Note that this name, `moisture_sensor`, is defined in sensor.py
water_pump = Motor.from_robot(robot=robot, name='water_pump')
```

And you can add your system logic to run continuously like this:

```python
 while True:

    # Get moisture sensor readings
    readings = await sensor.get_readings()
    print(readings)
    avg = sum(readings) / len(readings)
    sleep(1)

    if(avg > 950):
    print('needs water')

    # Run for 20 seconds
    await water_pump.go_for(1000,200)

    # Wait for the water to soak in
    sleep(5)

    # Recheck the avg
    readings = await sensor.get_readings()
    print(readings)
    avg = sum(readings) / len(readings)
    sleep(1)
```

## Next Steps

Now that you have created your automatic plant watering system with a capacitive soil moisture sensor, you can easily use Viam to automate other aspects of your garden.
For example, you can use a [light sensor](https://www.amazon.com/Sensor-Module-Raspberry-Integrated-Circuits/dp/B07L15M5JG) or a [temperature sensor](https://www.amazon.com/KY-011-Cathode-Arduino-Starter-2-color/dp/B07869PKKF/ref=as_li_ss_tl?keywords=arduino+two+color+led+module&qid=1556591832&s=gateway&sr=8-2&th=1&linkCode=sl1&tag=murraynet-20&linkId=c36cd98be29498a9883b656c7011b6bb&language=en_US)!
If you build something based on this please share it in our [Community Discord](https://discord.gg/viam)  - we'd love to see it.
