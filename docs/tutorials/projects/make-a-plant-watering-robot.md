---
title: "Plant Watering Robot with a Raspberry Pi"
linkTitle: "Plant Watering Robot"
weight: 50
type: "docs"
description: "Create a plant watering robot with a Raspberry Pi."
tags: ["raspberry pi", "app", "board", "motor"]
image: "/tutorials/img/plant-watering-pi/preview.png"
imageAlt: "Picture of the plant watering robot"
images: ["/tutorials/img/plant-watering-pi/preview.png"]
authors: [ "Sierra Guequierre" ]
languages: [ "python" ]
viamresources: [ "board", "motor", "sensor" ]
level: "Beginner"
date: "29 March 2023"
cost: 150
# SMES: Olivia Miller
---

![Picture of the plant watering robot on a desk.](../../img/plant-watering-pi/plant-watering-robot.png)

Building a useful robot doesn't have to require complicated code or expensive equipment.
With a Raspberry Pi and some cheap, basic hardware, you can keep your plants healthy and happy from anywhere in the world!

Follow this tutorial to learn how to set up an automatic plant watering system:

1. [Complete the physical assembly and wiring](#set-up-your-plant-watering-robot).
2. [Create and connect to the robot](#configure-the-components-of-your-robot-in-the-viam-app).
3. [Configure your robot's components](#configure-the-components-of-your-robot-in-the-viam-app).
4. [Configure the capacitive soil moisture sensor as a custom resource](#configure-the-capacitive-soil-moisture-sensor-as-a-custom-resource).
5. [Write code utilizing the Viam Python SDK to control the plant watering robot](#add-python-control-code).

The tutorial uses the following hardware, but you can adjust it as needed:

- A Raspberry Pi 3B or 4B with SD card and [5V USB power supply](https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Listed/dp/B00MARDJZ4)
- A [capacitive soil moisture sensor](https://www.amazon.com/KeeYees-Sensitivity-Moisture-Watering-Manager/dp/B07QXZC8TQ)
- A [peristaltic pump](https://www.amazon.com/Gikfun-Peristaltic-Connector-Aquarium-Analytic/dp/B01IUVHB8E) motor and [tubing](https://www.amazon.com/dp/B08H1ZD5VZ?psc=1&)
- An [Adafruit MCP3008 ADC](https://a.co/d/csRaIHE)
- A [motor speed controller](https://www.amazon.com/High-Power-Transistor-Controller-MELIFE-Electronic/dp/B09XKCD8HS)
- A [breadboard](https://www.amazon.com/SunFounder-Raspberry-Breadboard-solderless-Circuit/dp/B07ZYR7R8X)
- A [9V battery](https://www.amazon.com/dp/B08BRJQQSL/)
  - Optional: [wire leads](https://www.amazon.com/Battery-Hard-Shell-Connector-Insulated-Wires/dp/B07WTYS1PM/) in place of alligator clips for wiring the battery
- Assorted [breadboard jumper wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY/), including wires with [alligator clips](https://www.amazon.com/Goupchn-Alligator-Breadboard-Flexible-Electrical/dp/B08M5P6LHR/)
- A planter box or flower pot
- A water container
- A screwdriver

Before starting this tutorial, follow the [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/) to prepare your Pi to run `viam-server`.
Connect your Pi to its power supply to power it on.
Make sure your Pi is flashed with a Viam-compatible operating system, and that you are able to SSH into it.

## Set Up your Plant Watering Robot

Before programming the Pi to make the plant watering robot functional, you need to physically set up the plant watering robot by wiring the different components together.
You will set up the robot to receive signals from the capacitive soil moisture sensor and signal to the peristaltic pump when it is time to pump water from the water's container to the plant's container.

### Full Wiring Diagram

Refer back to this diagram as you complete the steps to wire your hardware.

![The full wiring diagram for all the hardware for the Plant Watering Robot.](../../img/plant-watering-pi/full-wiring.png)

### Wire your ADC

The analog-to-digital converter (ADC) converts the capacitive soil moisture sensor's analog readings to digital signals that can be processed by your Pi, which expects digital signals to come to it through its GPIO pins.

Start by wiring your ADC to your Raspberry Pi board.

You can find a Raspberry Pi pinout diagram at [pinout.xyz](https://pinout.xyz/pinout/3v3_power).
Reference the following pinout diagram for your MCP3008 analog-to-digital converter:

![Pinout diagram for the ADC.](../../img/plant-watering-pi/adc-pinout.png)

{{% alert title="Tip" color="tip" %}}
The half circle shown in the pinout diagram above should be physically present on your ADC.
Use this to orient the ADC to determine the location to insert your wires.
{{% /alert %}}

Insert the MCP3008 into your breadboard so that it bridges both sides of the divide.
Then, use the rows on the side of your MCP3008's pins and the GPIO pins on your PI to connect the pins with wires as follows:

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

### Wire your Capacitive Soil Moisture Sensor

Next, wire your [capacitive soil moisture sensor](https://www.amazon.com/KeeYees-Sensitivity-Moisture-Watering-Manager/dp/B07QXZC8TQ) to your Pi and ADC.

Reference this diagram of the blue module part of the sensor:

![Pinout diagram for the capacitive soil moisture sensor.](../../img/plant-watering-pi/moisture-sensor-pinout.png)

Start by connecting the female jumper wires at the end of the sensor prongs to the blue module where the diagram shown above is labeled "Connect with Probe."

Then, wire the rest of the pins on the module to the Pi and ADC as follows:

| Pi | ADC |
|--|--|
|<table> <tr><th>Moisture Sensor Pin</th><th>Raspberry Pi Pin</th></tr><tr><td>VCC</td><td>3.3V</td></tr><tr><td>GND</td><td>GND</td></tr> </table>| <table> <tr><th>Moisture Sensor Pin</th><th>MCP3008 ADC Pin</th></tr><tr><td>A0 (Analog Signal Output)</td><td>CH0</td></tr> </table>|

Put the soil moisture sensor inside of the container holding your plant.

### Wire your Pump

Now, wire and power your Peristaltic Pump [motor](/components/motor/) and [motor speed controller](https://www.amazon.com/High-Power-Transistor-Controller-MELIFE-Electronic/dp/B09XKCD8HS) to complete your hardware setup.

Reference this diagram of the motor speed controller:

![Pinout diagram for the motor speed controller.](../../img/plant-watering-pi/motor-speed-controller-diagram.png)

1. Attach [alligator wire clips](https://www.amazon.com/Goupchn-Alligator-Breadboard-Flexible-Electrical/dp/B08M5P6LHR/) to your battery to connect it to the DC power pins on your motor speed controller.
Match the **+** notation on the battery to the **+** DC power pin.
2. Attach [alligator wire clips](https://www.amazon.com/Goupchn-Alligator-Breadboard-Flexible-Electrical/dp/B08M5P6LHR/) to the pump to connect the output pins on your motor speed controller to the pump.
3. Connect the GND pin hole on the controller to GND on the Pi.
4. Connect the PWM pin hole on the pump to [Pin 12 (GPIO 18)](https://pinout.xyz/pinout/pin12_gpio18) of the Pi.
Note that the controller does not come with header pins.

{{% alert title="Tip" color="tip" %}}

To complete steps 2 and 3, you must insert the end of the jumper wires into the DC and output pin gates on the motor speed controller and tighten the screws on these gates with your screwdriver to close the wires inside.

For steps 3 and 4, note that the motor speed controller linked does not come with header pins.
You can either bend or soldier the jumper wire here to make the connection between the jumper wire and the PWM hole of the controller.

{{% /alert %}}

## Program Your Plant Watering Robot

{{<gif webm_src="/tutorials/img/plant-watering-pi/plant-watering-video.webm" mp4_src="/tutorials/img/plant-watering-pi/plant-watering-video.mp4" alt="The plant watering robot on a white desk. Camera goes up to the watering tube and pulls it out, showing the drip.">}}

### Enable SPI on your Pi

Now that you have wired your ADC and moisture sensor, make sure that the Serial Peripheral Interface (SPI) is enabled on your Pi.
Enabling this protocol is necessary to allow the Pi to communicate with the moisture sensor peripheral.

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

Now, you should see the moisture sensor values outputted by the MCP3008.

Test your sensor by putting it in air, water, and different soils to see how the values change to determine your baseline for wet and dry values.

![Terminal output of capacitive soil moisture sensor values.](../../img/plant-watering-pi/moisture-sensor-output.png)

### Configure the Components of your Robot in the Viam app

Follow [this guide](/installation/#install-viam-server) to install `viam-server` on your pi, create a new robot, and connect to it on [the Viam app](https://app.viam.com).

Then, navigate to your new robot's page on the app and click on the **Config** tab.

First, add your Pi as a [board component](/components/board/) by creating a new component with **type** `board` and **model** `pi`:

{{< tabs name="Configure an Pi Board" >}}
{{% tab name="Config Builder" %}}

![Creation of a pi board in the Viam app config builder.](../../img/plant-watering-pi/pi-board-config-builder.png)

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

Then, add your pump as a [motor component](/components/motor/) by adding a new component with **type** `motor` and **model** `gpio`.

Set the motor's attributes **Max RPM** to `1000` and **PWM**  to `12 GPIO 18` (the number and GPIO number of the pin that you wired the pump's PWM to).

{{< tabs name="Configure an Pump Motor" >}}
{{% tab name="Config Builder" %}}

![Creation of a pump motor in the Viam app config builder.](../../img/plant-watering-pi/pump-motor-config-builder.png)

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
    "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

Click **Save config**.

Now, if you navigate to your robot's **Control** tab, you should be able to control the motor by setting the power and direction of rotation and clicking the **RUN** button:

![Creation of a pump motor in the Viam app config builder.](../../img/plant-watering-pi/pump-motor-control.png)

{{% alert title="Tip" color="tip" %}}

Now that you have set up your robot and are able to control your motor, you can put the suction tube of your pump into the water cup, and the output tube into the plant!

{{% /alert %}}

### Configure the Capacitive Soil Moisture Sensor as a Custom Resource

*Resources* refer to the different [components](/components/) and [services](/services/) Viam provides for robots to use.
*Components* refer to types of hardware, and each component's built-in `models` support the most common models of this hardware.
For example, the [sensor component](/components/sensor/) has an `ultrasonic` model built in for the ubiquitous [ultrasonic sensor](https://www.sparkfun.com/products/15569).

However, there are many different types of sensors used for sensing different things across the [Internet of Things](https://medium.com/@siddharth.parakh/the-complete-list-of-types-of-sensors-used-in-iot-63b4003ab6b3).
Although the capacitive soil moisture sensor is not currently one of Viam's built-in models, you can use the Viam Python SDK to configure this sensor as a [custom resource](/extend/custom-components-remotes/) implementing the Viam [sensor class](https://python.viam.dev/autoapi/viam/components/sensor/sensor/index.html), making it a model of sensor available for you to use on your robot.

Create your custom sensor resource in 3 steps:

1. Code a `MoistureSensor` class implementing the `GetReadings()` method that belongs to all members of the Viam sensor class, and instantiate this class on a RPC server in the `main()` function of your code.
2. Add this "sensor server" as a [remote part](/manage/parts-and-remotes/) of your `plant-watering-robot`.
3. Add a command that runs the program you coded instantiating the "sensor server" as a *process* of your robot.

#### Code the `MoistureSensor` Class

If you haven't already, install the Viam Python SDK by following the instructions [on GitHub](https://python.viam.dev/).

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

from typing import Any, Dict, List, Mapping, Optional

class MoistureSensor(Sensor):

    def __init__(self, name: str):
        super(MoistureSensor,self).__init__(name)
        sensor_pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor_pin, GPIO.IN)


    # Implement the Viam Sensor API's get_readings() method
    async def get_readings(self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
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

        return {'moisture': input}

async def main():
   srv = Server(components=[MoistureSensor("moisture_sensor")])
   await srv.serve()

if __name__ == "__main__":
   asyncio.run(main())
```

You can modify this example code as necessary.

#### Add the `MoistureSensor` Remote

Now, go back to your robot's page on [the Viam app](https://app.viam.com) and navigate to the **Config** tab, then to the **Remotes** subtab.

Add your sensor server as a [remote part](/manage/parts-and-remotes/) called `my-sensor-server`:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "components": [ board & motor ... ],
"remotes": [
    {
      "name": "my-sensor-server",
      "insecure": true,
      "address": "localhost:9090"
    }
]
```

{{% /tab %}}
{{% tab name="Config Builder" %}}

![Creation of a custom sensor remote in the Viam app config builder."](../../img/plant-watering-pi/sensor-remote-config-builder.png)

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Important" color="note" %}}

If you use the Config Builder to make your remote, make sure you have still added the line: `"insecure": true,` to the Raw JSON.
This line determines that your server does need an SSL certificate.

{{% /alert %}}

#### Add the `MoistureSensor` Process

Then, navigate to the **Processes** subtab and create a process called `run-sensor-server`:

{{< tabs >}}
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
{{% tab name="Config Builder" %}}

![Creation of a process to run the sensor remote server in the Viam app config builder.](../../img/plant-watering-pi/sensor-process-config-builder.png)

{{% /tab %}}
{{< /tabs >}}

Modify the `"args"` and `"cwd"` to match the path to your `plant-watering-robot` directory on your Pi.

Click **Save config**.
Now, when you navigate to your robot's **Control** tab, you should be able to see your sensor readings:

![Readings from a soil moisture sensor in the Viam app CONTROL tab.](../../img/plant-watering-pi/sensor-reading-control.png)

{{% alert title="Tip" color="tip" %}}

If you are having trouble seeing your sensor readings, check the **Logs** table and filter by the **error** level to get more information about the issue.

Make sure that you have modified `<my_username>` in the JSON template above to match your username on your Pi.
You can run `pwd` in your terminal after SSH'ing into your Pi to see what your username is.

{{% /alert %}}

### Add Python Control Code

Follow these instructions to start working on your Python control code:

1. Navigate to your robot's page in [the Viam app](https://app.viam.com), and click on the **Code sample** tab.
2. Select **Python** as the language.
3. Click **Copy** to copy the generated code sample, which establishes a connection with your robot when run.

   {{% snippet "show-secret.md" %}}

4. Paste this code sample into a new file in the `plant-watering-robot` directory you created on your Pi.
5. Name the file <file>plant-watering-robot.py</file>, and save it.

For example, run the following commands on your Pi to create and open the file:

``` shell
cd plant-watering-robot
touch plant-watering-robot.py
nano plant-watering-robot.py
```

Now, you can add code into <file>plant-watering-robot.py</file> to write the logic that defines your plant watering system.

To start, add your system logic code into the `main()` function of the program.
Use the Viam [motor](/components/motor/#api) and [sensor](/components/sensor/#control-your-sensor-with-viams-client-sdk-libraries) API methods.

You can get your components from the robot like this:

```python
sensor = Sensor.from_robot(robot=robot, name='moisture_sensor') # Note that this name, `moisture_sensor`, is defined in sensor.py
water_pump = Motor.from_robot(robot=robot, name='water-pump')
```

And you can add your system logic to run continuously like this:

```python
while True:

      # Get the moisture sensor's readings
      readings = await sensor.get_readings()
      soil_moisture = readings.get('moisture')

      # Calculate average moisture reading from the list of readings, to account for outliers
      avg_moisture = sum(soil_moisture) / len(soil_moisture)

      # If the average moisture reading is greater than 60000, trigger pump watering
      if(avg_moisture > 60000):
          print('this plant is too thirsty! giving it more water')

          # Run the water pump for 100 rev. at 1000 rpm
          await water_pump.go_for(rpm=1000, revolutions=1000)

          # Wait 60 seconds so that the water can soak into the soil a bit before trying to water again
          print('waiting a little bit for water to soak in')
          time.sleep(60)
```

{{% alert title="Tip" color="tip" %}}
Make sure to import `time` at the beginning of your version of <file>plant-watering-robot.py</file> to be able to use `sleep()`!
Also, make sure to import `viam.components.sensor`.
{{% /alert %}}

See the motor component's [API documentation](/components/motor/#gofor) for more information about `water_pump.go_for()`.

Save your <file>plant-watering-robot.py</file> program with this logic added in, and then run it on your Pi like this:

``` shell
sudo python3 plant-watering-robot.py
```

To tinker this example code to work best for you, determine at what [analog value from the Soil Moisture readings](#test-your-soil-moisture-readings-on-your-pi) you want to water your plant, as your thirsty plant's average moisture reading might differ from our example value of `60000`.
Also, consider how often you would like to check the moisture levels of the plant, and how long the plant should be watered.

## Next Steps

Now that you have created your automatic plant watering system with a capacitive soil moisture sensor, you can easily use Viam to automate other aspects of your garden.
For example, you can use a [light sensor](https://www.amazon.com/Sensor-Module-Raspberry-Integrated-Circuits/dp/B07L15M5JG) or a [temperature sensor](https://www.amazon.com/KY-011-Cathode-Arduino-Starter-2-color/dp/B07869PKKF/ref=as_li_ss_tl?keywords=arduino+two+color+led+module&qid=1556591832&s=gateway&sr=8-2&th=1&linkCode=sl1&tag=murraynet-20&linkId=c36cd98be29498a9883b656c7011b6bb&language=en_US)!
If you build something based on this please share it in our [Community Discord](https://discord.gg/viam)  - we'd love to see it.
