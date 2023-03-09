---
title: "How to Make a Plant Watering Robot with the ESP32"
linkTitle: "Make a Plant Watering Robot with the ESP32"
weight: 50
type: "docs"
description: "Instructions for creating a plant watering robot with an ESP-32 microcontroller and Viam's micro-RDK."
tags: ["base", "microcontrollers", "app", "esp32"]
---

## Hardware Requirements

- An [ESP-32 microcontroller with a development board](https://www.amazon.com/gp/product/B087TNPQCV/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1).

<!-- TODO: extension boards etc, may need to consult further with nick m. -->

Each of these requirements are for creating one Plant Watering unit.

- One or more plants in a planter box.
- A box filled with water.
- An analog [soil moisture sensor](https://www.amazon.com/gp/product/B07SYBSHGX/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1) (connected to ESP32).
- An analog [water level sensor](https://www.amazon.com/CQRobot-Consumption-Resistance-Temperature-Properties/dp/B07ZMGW3QJ/ref=sr_1_4?crid=1542UHAWN6D43&keywords=water+immersion+sensor+arduino&qid=1678306219&sprefix=water+immersion+sensor+arduino%2Caps%2C92&sr=8-4) (connected to ESP32).
- [DC 5V Mini Water Pump](https://www.amazon.com/gp/product/B09TGK9N5Q/ref=ppx_yo_dt_b_asin_title_o03_s01?ie=UTF8&psc=1) (connected to ESP-32).
<!-- power supplies? water level reader?

raspberry pi?  -->

## Hardware Setup

<!-- TODO: steps and pictures for getting all the hardware pieced together -->
<!-- - add in a note saying to write down what GPIO pins you've connected the pumps etc. to, can show where you'll put them in / link back and forth in between nested dictionaries setup below & main.RS pin exposing
- add in a note saying not to connect to power supply until you're doing the software setup with your micro-RDK-- can link to section from microcontroller setup guide -->

## Getting Started

First, see our [Microcontroller Setup: the Micro-RDK](../../installation/microcontrollers/) guide to creating an ESP32-backed robot with Viam.

That guide provides detailed instructions on getting all the necessary prerequisites for this tutorial installed on your local development machine, creating a project with the micro-RDK to upload onto your microcontroller, connecting it to Viam as a robot, and adding that robot as a remote of another robot running `viam-server`.

When following this tutorial, you will modify the <file>Main.rs</file> Rust code from the [project template you generated when following these instructions](../../installation/microcontrollers#generate-a-new-project-from-the-micro-rdk-template), and add a Python file utilizing the Viam Python SDK to control the plant watering robot.

### Edit `Main.rs` from the Micro-RDK Template

Make sure that when following these instructions, you have not yet modified your code from the template available [here](https://github.com/viamrobotics/micro-rdk-template/blob/main/src/main.rs).

If you have already modified it, use an [online Diff checker](https://www.diffchecker.com/) or `git diff main1.rs main2.rs` to find the differences between your <file>Main.rs</file> and the [example](#full-example-code) <file>Main.rs</file>.

You can also copy the example <file>Main.rs</file> code from [here](#full-example-code) to use as your <file>Main.rs</file> if you do not wish to make individual modifications.

1. Delete the `use` declarations (lines 7-25) from your <file>Main.rs</file> and replace with the following code:

    {{%expand "use declarations" %}}

    ``` rust {class="line-numbers linkable-line-numbers"}

    use anyhow::bail;
    use esp_idf_hal::gpio::OutputPin;
    use esp_idf_hal::prelude::Peripherals;
    use esp_idf_hal::task::notify;
    use esp_idf_svc::eventloop::EspSystemEventLoop;
    use esp_idf_svc::mdns::EspMdns;
    use esp_idf_svc::netif::{EspNetif, EspNetifWait};
    use esp_idf_svc::wifi::EspWifi;
    use esp_idf_sys::esp_wifi_set_ps;
    use esp_idf_sys::vTaskDelay;
    use esp_idf_sys::{self as _, TaskHandle_t}; // If using the `binstart` feature of `esp-idf-sys`, always keep this module imported
    use futures_lite::future::block_on;
    use hyper::server::conn::Http;
    use log::*;
    use mini_rdk::esp32::exec::Esp32Executor;
    use mini_rdk::esp32::grpc::GrpcServer;
    use mini_rdk::esp32::robot::Esp32Robot;
    use mini_rdk::esp32::robot::ResourceType;
    use mini_rdk::esp32::robot_client::RobotClientConfig;
    use mini_rdk::esp32::tcp::Esp32Listener;
    use mini_rdk::esp32::tls::{Esp32Tls, Esp32TlsServerConfig};
    use mini_rdk::proto::common::v1::ResourceName;
    use std::cell::RefCell;
    use std::collections::HashMap;
    use std::net::SocketAddr;
    use std::rc::Rc;
    use std::sync::Arc;
    use std::sync::Mutex;
    use std::time::Duration;

    ```

    {{% /expand%}}

2. Delete lines 42-106 in `main()` and replace with the following code:

    {{%expand "let robot = { ... }" %}}

    ``` rust {class="line-numbers linkable-line-numbers"}
    let robot = {
            use esp_idf_hal::adc::config::Config;
            use esp_idf_hal::adc::{self, AdcChannelDriver, AdcDriver, Atten11dB};
            use esp_idf_hal::gpio::PinDriver;
            use mini_rdk::esp32::analog::Esp32AnalogReader;
            use mini_rdk::esp32::board::EspBoard;

            let pins = vec![
                PinDriver::output(periph.pins.gpio18.downgrade_output())?,
                PinDriver::output(periph.pins.gpio19.downgrade_output())?,
                PinDriver::output(periph.pins.gpio21.downgrade_output())?,
            ];

            let adc1 = Rc::new(RefCell::new(AdcDriver::new(
                periph.adc1,
                &Config::new().calibration(true),
            )?));

            let adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
                AdcChannelDriver::new(periph.pins.gpio34)?;
            let analog1 = Esp32AnalogReader::new("Plant5".to_string(), adc_chan, adc1.clone());

            let adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
                AdcChannelDriver::new(periph.pins.gpio32)?;
            let analog2 = Esp32AnalogReader::new("Plant3".to_string(), adc_chan, adc1.clone());
            let adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
                AdcChannelDriver::new(periph.pins.gpio33)?;
            let analog3 = Esp32AnalogReader::new("Plant4".to_string(), adc_chan, adc1.clone());

            let board = EspBoard::new(
                pins,
                vec![
                    Rc::new(RefCell::new(analog1)),
                    Rc::new(RefCell::new(analog2)),
                    Rc::new(RefCell::new(analog3)),
                ],
            );

            let board = Arc::new(Mutex::new(board));

            let mut res: mini_rdk::esp32::robot::ResourceMap = HashMap::with_capacity(1);

            res.insert(
                ResourceName {
                    namespace: "rdk".to_string(),
                    r#type: "component".to_string(),
                    subtype: "board".to_string(),
                    name: "board".to_string(),
                },
                ResourceType::Board(board),
            );

            Esp32Robot::new(res)
        };

        let (ip, _wifi) = {
            let wifi = start_wifi(periph.modem, sys_loop_stack)?;
            (wifi.sta_netif().get_ip_info()?.ip, wifi)
        };

        let client_cfg = { RobotClientConfig::new(ROBOT_SECRET.to_string(), ROBOT_ID.to_string(), ip) };

        let hnd = match mini_rdk::esp32::robot_client::start(client_cfg) {
            Err(e) => {
                log::error!("couldn't start robot client {:?} will start the server", e);
                None
            }
            Ok(hnd) => Some(hnd),
        };

        // start mdns service
        let _mdms = {
            let mut mdns = EspMdns::take()?;
            mdns.set_hostname(ROBOT_NAME)?;
            mdns.set_instance_name(ROBOT_NAME)?;
            mdns.add_service(None, "_rpc", "_tcp", 80, &[])?;
            mdns
        };

        if let Err(e) = runserver(robot, hnd) {
            log::error!("robot server failed with error {:?}", e);
            panic!()
        }

        panic!()
    }
    ```

    {{% /expand%}}

3. Add a new `runserver()` function in between `main()` and `start_wifi()` with the following code:

    {{%expand "runserver()" %}}

    ``` rust {class="line-numbers linkable-line-numbers"}
    fn runserver(robot: Esp32Robot, client_handle: Option<TaskHandle_t>) -> anyhow::Result<()> {
        let cfg = {
            let cert = include_bytes!(concat!(env!("OUT_DIR"), "/ca.crt"));
            let key = include_bytes!(concat!(env!("OUT_DIR"), "/key.key"));
            Esp32TlsServerConfig::new(
                cert.as_ptr(),
                cert.len() as u32,
                key.as_ptr(),
                key.len() as u32,
            )
        };
        let tls = Box::new(Esp32Tls::new_server(&cfg));
        let address: SocketAddr = "0.0.0.0:80".parse().unwrap();
        let mut listener = Esp32Listener::new(address.into(), Some(tls))?;
        let exec = Esp32Executor::new();
        let srv = GrpcServer::new(Arc::new(Mutex::new(robot)));
        if let Some(hnd) = client_handle {
            if unsafe { notify(hnd, 1) } {
                log::info!("successfully notified client task");
                unsafe {
                    vTaskDelay(1000);
                };
            } else {
                log::error!("failed to notity client task had handle {:?}", hnd);
            }
        } else {
            log::error!("no handle")
        }
        loop {
            let stream = listener.accept()?;
            block_on(exec.run(async {
                let err = Http::new()
                    .with_executor(exec.clone())
                    .http2_max_concurrent_streams(1)
                    .serve_connection(stream, srv.clone())
                    .await;
                if err.is_err() {
                    log::error!("server error {}", err.err().unwrap());
                }
            }));
        }
    }
    ```

    {{% /expand%}}

## Add Python Control Code

Now, to control your ESP32 backed robot, add Python control code to run on your ESP32.

While setting up your ESP32 backed robot, you should have added it as a remote of another robot that is controlled by a computer with the necessary processing power to run the full version of `viam-server`.

- This might be just your local development machine.
Find instructions for installing and running `viam-server` on MacOs or Linux machines [here.](../../installation/install/)
- In the example code for this tutorial, we are using a Raspberry Pi single-board computer to act as our secondary robot instance.
See our [Raspberry Pi Setup Guide](../../installation/prepare/rpi-setup/) for information on how to get `viam-server` up and running on your Raspberry Pi.

Make sure this robot is running an instance of `viam-server` and has a live connection, with the ESP32 backed-robot [added as a remote](../../installation/microcontrollers#configure-the-esp32-as-a-remote).

Follow the below instructions to start working on your Python Control Code:

1. Navigate to your `viam-server` robot's page in [the Viam app](https://app.viam.com), and click on the **CONTROL** tab.
Follow the instructions in this tab.

   - Install the Python SDK if you have not already.
   - Then, click **COPY CODE** to copy a code sample that establishes a connection with this robot when run.

2. Paste this code sample into a new file in the directory where you have saved your micro-RDK template code, using your preferred IDE.

   - Name the file whatever you want, and save it.
   - In the [example code](#full-example-code) this tutorial follows, the control code is named <file>Water-esp32.py</file>.

The beginning of your new file should look similar to the following:

``` python {class="line-numbers linkable-line-numbers"}
import asyncio
import datetime
import signal

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='xyz12345678910somerobotlocationsecret') // Your robot location secret
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('some-robot-name-main.123xyz.viam.cloud', opts) // Your robot address

```

<br>
Add the following imports to the beginning of your file if they are not already present:

``` python {class="line-numbers linkable-line-numbers"}
import datetime
import signal

from viam.components.board import Board
```

### `WaterLevelUnit` Class

Now, after `async def connect()`, add a new class for your water level analog reader units.

Create this class with two attributes: a `reader` and a `threshold`.

``` python {class="line-numbers linkable-line-numbers"}
class WaterLevelUnit:
    reader : Board.AnalogReader
    threshold : int
    def __init__(self, r: Board.AnalogReader, t):
        self.reader = r
        self.threshold = t
    async def isWaterLevelOk(self):
        val = await self.reader.read()
        if val < self.threshold:
            return False
        return True    

```

### `PumpUnit` Class

Now, add a new class for your water pump units.

Create this class with four attributes: a `Board`, a `pin`, a `pumpTime`, and a `name`.
<!-- TODO: could possibly make above a table with definitions for each attribute  -->

``` python {class="line-numbers linkable-line-numbers"}
class PumpUnit:
    board : Board # Your ESP32 board.
    pin : int # The GPIO pin number on your ESP32 board that the pump is connected to.
    pumpTime : int # Time to sleep in between running the pump, in milliseconds. 
    name: str # The name you want to give the PumpUnit.

    def __init__(self, b : Board, pin, p, name):
        self.board = b
        self.pin = pin
        self.pumpTime = p
        self.name = name
    
```

Define a `runPump` and a `stopPump` function to belong to this class.
<br>

`runPump` sets the ESP32 GPIO pin identified by the PumpUnit's `pin` attribute to `True` (HIGH), giving power to the pump and turning it  on.

- If an exception occurs, a `CancelledError` is raised, and the pin's power is set to `False` (LOW).

`stopPump` sets the ESP32 GPIO pin identified by the PumpUnit's `pin` attribute to `False` (LOW), turning the power to the pump off.

``` python {class="line-numbers linkable-line-numbers"}
    async def runPump(self):
        print("Running the pump {} {}".format(self.name,self.pin))
        pin = await self.board.gpio_pin_by_name(self.pin) # Get the GPIO pin of the specified ID number from the ESP32 board.
        try:
            await pin.set(True)
            await asyncio.sleep(self.pumpTime) # Wait PumpUnit.pumpTime milliseconds before running the pump again.
        except asyncio.CancelledError:
            await pin.set(False)
            raise
        await pin.set(False) # Set the GPIO pin back to False (LOW), turning it off, before running the pump again.

    async def stopPump(self):
        try :
            await pin.set(False) # Set the GPIO pin back to False (LOW), turning it off. 
        except:
            raise # Raise an error if setting the pin to False fails.
```

### `PlantUnit` Class

Now, add a new class, `PlantUnit` to define each of your plants you want to water.

Create this class with six attributes: `reader`, `pump`, `cooldown`, `next_allowed_activation`, `min_moisture`, and `name`.

Add two functions to belong to this class: `waterPlant()` and `stop()`.

- `waterPlant()` runs in each `PlantUnit` you create at an interval defined by `cooldown` and `next_allowed_activation`, as long as the moisture level (*mm*) read by the moisture reader is found to be greater than the minimum moisture level specified by `min_moisture`.
- `stop()` stops watering the plant, calling to the pump's `stop()` function.

``` python {class="line-numbers linkable-line-numbers"}
class PlantUnit:
    reader : Board.AnalogReader # The analog moisture reader for this plant unit, connected to your ESP32 board.
    pump: PumpUnit # The pump for this plant unit, connected to your ESP32 board. 
    cooldown: int # Time in seconds to wait in between watering the plant with waterPlant().
    next_allowed_activation: datetime.datetime # Set dynamically on each run of waterPlant(): Exact date and time to water the plant next.
    min_moisture : int # Minimum moisture level, in mm, required to run the pump with runPump() when waterPlant() is run.
    name: str # The name you want to give this PlantUnit(). 
    
    def __init__(self, r : Board.AnalogReader, p : PumpUnit, cooldown, mm, name):
        self.reader = r
        self.pump = p
        self.cooldown = cooldown
        self.next_allowed_activation = datetime.datetime.now()
        self.min_moisture = mm
        self.name = name

    # Water the plant with the PlantUnit's pump, using PumpUnit's runPump().
    async def waterPlant(self):
        print("Running waterPlant for plant {}".format(self.name))

        # Check to see if the current date & time is past the date & time required for the next allowed activation of the watering system. 
        if self.next_allowed_activation < datetime.datetime.now():
            val = await self.reader.read() # Read the current moisture level.
            print("Current moisture level is {} min is {}".format(val,self.min_moisture)) # Print out the current moisture level (mm).

            # If the current moisture level is greater than the minimum moisture level required, run the pump for this unit.
            if val > self.min_moisture:
                await self.pump.runPump()

            # Set the next date & time required for the next allowed activation of the watering system. 
            self.next_allowed_activation = datetime.datetime.now() + datetime.timedelta(seconds=self.cooldown)

            # Print out the date and time of the next allowed activation of the watering system. 
            print("Plant {} next run is {}".format(self.name,self.next_allowed_activation))

    # Stop watering the plant with the PlantUnit's pump, using PumpUnit's stop().
    async def stop(self):
        await self.pump.stop()
```

### Define your Board's Whole Configuration with a Nested Dictionary

Now, you can used nested dictionaries to define the configuration of the hardware units that you have connected to your ESP32 board, adding all the required attributes for the `WaterLevelUnit`, `PumpUnit`, and `PlantUnit` classes.

For example, the following code defines an ESP32 board named `esp1` connected to one `WaterLevelUnit` with a water level reader and water box, and two plant boxes (`PlantUnit`), each with 1 pump (`PumpUnit`) and 1 soil moisture reader.

<!-- Modify this example code to your specifics for [TODO: minimum and maximum moisture levels, pumps, cooldown, pins]. -->

``` python {class="line-numbers linkable-line-numbers"}
esp1 = {"esp1" : {"name" : "esp32-plant-1-main:board",
                   "attributes" : {"WaterLevel" : {"type" : "level",
                                                   "min" : 700,
                                                   "max" : 2200},
                                   "Plant1" : {"type" :"plant",
                                               "min" : 1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump1","pin" : "19",
                                                         "max" : 5}},
                                   "Plant2" : {"type" :"plant",
                                               "min" :1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump2","pin" : "18",
                                                         "max" : 5}},
                                   }
                   }
    }
```

### `WateringSystem` Class

Now that you've defined the `WaterLevelUnit`, `PumpUnit`, and `PlantUnit` classes, and added all the required attributes to your ESP32 board nested dictionary, you can define a class for the `WateringSystem` as a whole.

Create this class with four attributes: `waterLevel`, `plantUnits`, `robot`, and `config`.

``` python {class="line-numbers linkable-line-numbers"}
class WateringSystem:
    waterLevel : WaterLevelUnit  # The WaterLevelUnit in this watering systems
    plantUnits : list[PlantUnit] # A list of the plantUnits in this watering system
    robot = RobotClient # The robot that your ESP32-backed robot controlling this watering system is configured as a remote of
    config: dict # Your controlling ESP32's configuration as a nested dictionary

    def __init__(self, robot: RobotClient, config):
        self.plantUnits = list()
        self.waterLevel = None
        self.robot = robot
        self.config = config

    async def configure(self):
        waterLevel = None
        plantUnits = list()
        for k,v in self.config.items():
            board = Board.from_robot(robot=self.robot,name=v["name"])
            attrs = v["attributes"]
            for k,v in attrs.items():
                if v["type"] == "level":
                    waterLevelreader = await board.analog_reader_by_name(name=k)
                    waterLevel = WaterLevelUnit(waterLevelreader,v["min"])
                if v["type"] == "plant":
                    pumpCfg = v["pump"]
                    pump = PumpUnit(b=board,pin=pumpCfg["pin"],p=pumpCfg["max"],name=pumpCfg["name"])
                    moistureReader = await board.analog_reader_by_name(name=k)
                    plant = PlantUnit(r=moistureReader,p=pump,cooldown=v["cooldown"],mm=v["min"],name=k)
                    plantUnits.append(plant)
        self.waterLevel = waterLevel
        self.plantUnits = plantUnits

    async def runOnce(self):
        if self.waterLevel == None:
            return
        print("Checking if water level is ok")

        if await self.waterLevel.isWaterLevelOk() == False:
            print("Not enough water")

        print("water level good")
        for plant in self.plantUnits:
            await plant.waterPlant()

    async def stop(self):
        for plant in self.plantUnits:
            await plant.stop()
```

### Put it All Together in `main()` and `shutdown()`

Now, it's time to write the code that will run on your ESP32-backed robot into the `main()` function of your Python control file.

``` python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect() # Connect the ESP32-remote robot

    water = WateringSystem(robot, esp1) # Create a new WateringSystem instance with the ESP32-remote robot and the ESP32 config dictionary

    await water.configure() # Wait for the new WateringSystem to configure

    # Run this until you raise a CancelledError and stop the WateringSystem
    while True:
        try:
            await water.runOnce()
            await asyncio.sleep(30) # Sleep for 30 seconds in between each run of the WateringSystem's runOnce function
        except asyncio.CancelledError:
            await water.stop() # Stop the WateringSystem
            break; # Break out of the while loop

    print("done with watering!")
    await robot.close() # Close your connection to the ESP32-remote robot
```

Then, you might want to add a `shutdown` function to shut down all the tasks that were running:

``` python
async def shutdown(signal, loop):
    """Clean-up tasks."""
    print("killing loops")

    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    [task.cancel() for task in tasks]

    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

```

Now, add this `if` statement at the bottom of your control file to make `main()` run if the Python file is running, and `shutdown()` happen when the Python file stops running:

``` python
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Catching and handling 
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
        print("Successfully shut down!")
```

## Run Your Python Control Code

Open the terminal of the computer that is controlling the robot running `viam-server` that your ESP32-backed robot is a remote of.

If the computer is a single-board computer like a Raspberry Pi, ssh into it from your local development machine.

Run the following command, replacing the brackets `<>` with your chosen file path and file name: `python <path-to-your-file>/<your-control-file-name>.py`

Now, your plant watering system is up and running!

{{< alert title="Tip" color="tip" >}}

`Ctrl+C` to exit out of the Python program.

{{% /alert %}}

If you are not sure what your file path is, try running `pwd` in your terminal after `cd`ing to the directory where your file is stored.

For example:

``` shell
~ % cd Desktop/micro-rdk 
micro-rdk % pwd
/Users/myusername/Desktop/micro-rdk
```

## Full Example Code

<file>Main.rs</file>:

{{%expand "Click to view the full Main.rs Example Code" %}}

``` rust  {class="line-numbers linkable-line-numbers"}
const SSID: &str = env!("MINI_RDK_WIFI_SSID");
const PASS: &str = env!("MINI_RDK_WIFI_PASSWORD");

// Generated robot config during build process
include!(concat!(env!("OUT_DIR"), "/robot_secret.rs"));

use anyhow::bail;
use esp_idf_hal::gpio::OutputPin;
use esp_idf_hal::prelude::Peripherals;
use esp_idf_hal::task::notify;
use esp_idf_svc::eventloop::EspSystemEventLoop;
use esp_idf_svc::mdns::EspMdns;
use esp_idf_svc::netif::{EspNetif, EspNetifWait};
use esp_idf_svc::wifi::EspWifi;
use esp_idf_sys::esp_wifi_set_ps;
use esp_idf_sys::vTaskDelay;
use esp_idf_sys::{self as _, TaskHandle_t}; // If using the `binstart` feature of `esp-idf-sys`, always keep this module imported
use futures_lite::future::block_on;
use hyper::server::conn::Http;
use log::*;
use mini_rdk::esp32::exec::Esp32Executor;
use mini_rdk::esp32::grpc::GrpcServer;
use mini_rdk::esp32::robot::Esp32Robot;
use mini_rdk::esp32::robot::ResourceType;
use mini_rdk::esp32::robot_client::RobotClientConfig;
use mini_rdk::esp32::tcp::Esp32Listener;
use mini_rdk::esp32::tls::{Esp32Tls, Esp32TlsServerConfig};
use mini_rdk::proto::common::v1::ResourceName;
use std::cell::RefCell;
use std::collections::HashMap;
use std::net::SocketAddr;
use std::rc::Rc;
use std::sync::Arc;
use std::sync::Mutex;
use std::time::Duration;

fn main() -> anyhow::Result<()> {
    esp_idf_sys::link_patches();

    esp_idf_svc::log::EspLogger::initialize_default();
    let sys_loop_stack = EspSystemEventLoop::take().unwrap();
    {
        esp_idf_sys::esp!(unsafe {
            esp_idf_sys::esp_vfs_eventfd_register(&esp_idf_sys::esp_vfs_eventfd_config_t {
                max_fds: 5,
            })
        })?;
    }

    let periph = Peripherals::take().unwrap();

    let robot = {
        use esp_idf_hal::adc::config::Config;
        use esp_idf_hal::adc::{self, AdcChannelDriver, AdcDriver, Atten11dB};
        use esp_idf_hal::gpio::PinDriver;
        use mini_rdk::esp32::analog::Esp32AnalogReader;
        use mini_rdk::esp32::board::EspBoard;

        let pins = vec![
            PinDriver::output(periph.pins.gpio18.downgrade_output())?,
            PinDriver::output(periph.pins.gpio19.downgrade_output())?,
            PinDriver::output(periph.pins.gpio21.downgrade_output())?,
        ];

        let adc1 = Rc::new(RefCell::new(AdcDriver::new(
            periph.adc1,
            &Config::new().calibration(true),
        )?));

        let adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
            AdcChannelDriver::new(periph.pins.gpio34)?;
        let analog1 = Esp32AnalogReader::new("Plant5".to_string(), adc_chan, adc1.clone());

        let adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
            AdcChannelDriver::new(periph.pins.gpio32)?;
        let analog2 = Esp32AnalogReader::new("Plant3".to_string(), adc_chan, adc1.clone());
        let adc_chan: AdcChannelDriver<_, Atten11dB<adc::ADC1>> =
            AdcChannelDriver::new(periph.pins.gpio33)?;
        let analog3 = Esp32AnalogReader::new("Plant4".to_string(), adc_chan, adc1.clone());

        let board = EspBoard::new(
            pins,
            vec![
                Rc::new(RefCell::new(analog1)),
                Rc::new(RefCell::new(analog2)),
                Rc::new(RefCell::new(analog3)),
            ],
        );

        let board = Arc::new(Mutex::new(board));

        let mut res: mini_rdk::esp32::robot::ResourceMap = HashMap::with_capacity(1);

        res.insert(
            ResourceName {
                namespace: "rdk".to_string(),
                r#type: "component".to_string(),
                subtype: "board".to_string(),
                name: "board".to_string(),
            },
            ResourceType::Board(board),
        );

        Esp32Robot::new(res)
    };

    let (ip, _wifi) = {
        let wifi = start_wifi(periph.modem, sys_loop_stack)?;
        (wifi.sta_netif().get_ip_info()?.ip, wifi)
    };

    let client_cfg = { RobotClientConfig::new(ROBOT_SECRET.to_string(), ROBOT_ID.to_string(), ip) };

    let hnd = match mini_rdk::esp32::robot_client::start(client_cfg) {
        Err(e) => {
            log::error!("couldn't start robot client {:?} will start the server", e);
            None
        }
        Ok(hnd) => Some(hnd),
    };

    // start mdns service
    let _mdms = {
        let mut mdns = EspMdns::take()?;
        mdns.set_hostname(ROBOT_NAME)?;
        mdns.set_instance_name(ROBOT_NAME)?;
        mdns.add_service(None, "_rpc", "_tcp", 80, &[])?;
        mdns
    };

    if let Err(e) = runserver(robot, hnd) {
        log::error!("robot server failed with error {:?}", e);
        panic!()
    }

    panic!()
}

fn runserver(robot: Esp32Robot, client_handle: Option<TaskHandle_t>) -> anyhow::Result<()> {
    let cfg = {
        let cert = include_bytes!(concat!(env!("OUT_DIR"), "/ca.crt"));
        let key = include_bytes!(concat!(env!("OUT_DIR"), "/key.key"));
        Esp32TlsServerConfig::new(
            cert.as_ptr(),
            cert.len() as u32,
            key.as_ptr(),
            key.len() as u32,
        )
    };
    let tls = Box::new(Esp32Tls::new_server(&cfg));
    let address: SocketAddr = "0.0.0.0:80".parse().unwrap();
    let mut listener = Esp32Listener::new(address.into(), Some(tls))?;
    let exec = Esp32Executor::new();
    let srv = GrpcServer::new(Arc::new(Mutex::new(robot)));
    if let Some(hnd) = client_handle {
        if unsafe { notify(hnd, 1) } {
            log::info!("successfully notified client task");
            unsafe {
                vTaskDelay(1000);
            };
        } else {
            log::error!("failed to notity client task had handle {:?}", hnd);
        }
    } else {
        log::error!("no handle")
    }
    loop {
        let stream = listener.accept()?;
        block_on(exec.run(async {
            let err = Http::new()
                .with_executor(exec.clone())
                .http2_max_concurrent_streams(1)
                .serve_connection(stream, srv.clone())
                .await;
            if err.is_err() {
                log::error!("server error {}", err.err().unwrap());
            }
        }));
    }
}

fn start_wifi(
    modem: impl esp_idf_hal::peripheral::Peripheral<P = esp_idf_hal::modem::Modem> + 'static,
    sl_stack: EspSystemEventLoop,
) -> anyhow::Result<Box<EspWifi<'static>>> {
    use embedded_svc::wifi::{ClientConfiguration, Wifi};
    use esp_idf_svc::wifi::WifiWait;
    use std::net::Ipv4Addr;

    let mut wifi = Box::new(EspWifi::new(modem, sl_stack.clone(), None)?);

    info!("scanning");
    let aps = wifi.scan()?;
    let foundap = aps.into_iter().find(|x| x.ssid == SSID);

    let channel = if let Some(foundap) = foundap {
        info!("{} channel is {}", "Viam", foundap.channel);
        Some(foundap.channel)
    } else {
        None
    };
    let client_config = ClientConfiguration {
        ssid: SSID.into(),
        password: PASS.into(),
        channel,
        ..Default::default()
    };
    wifi.set_configuration(&embedded_svc::wifi::Configuration::Client(client_config))?; //&Configuration::Client(client_config)

    wifi.start()?;

    if !WifiWait::new(&sl_stack)?
        .wait_with_timeout(Duration::from_secs(20), || wifi.is_started().unwrap())
    {
        bail!("couldn't start wifi")
    }

    wifi.connect()?;

    if !EspNetifWait::new::<EspNetif>(wifi.sta_netif(), &sl_stack)?.wait_with_timeout(
        Duration::from_secs(20),
        || {
            wifi.is_connected().unwrap()
                && wifi.sta_netif().get_ip_info().unwrap().ip != Ipv4Addr::new(0, 0, 0, 0)
        },
    ) {
        bail!("wifi couldn't connect")
    }

    let ip_info = wifi.sta_netif().get_ip_info()?;

    info!("Wifi DHCP info: {:?}", ip_info);

    esp_idf_sys::esp!(unsafe { esp_wifi_set_ps(esp_idf_sys::wifi_ps_type_t_WIFI_PS_NONE) })?;

    Ok(wifi)
}
```

{{% /expand%}}

<file>Water-esp32.py</file>:

{{%expand "Click to view the full Water-esp32.py Example Code" %}}

``` python  {class="line-numbers linkable-line-numbers"}
import asyncio
import datetime
import signal

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='n7eaqp57d1gx667h2rdupgkfaoxi7aci1jea2l19nvdgyi1b')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('pi-control-main.r91xx900p0.viam.cloud', opts)


esp1 = {"esp1" : {"name" : "esp32-plant-1-main:board",
                   "attributes" : {"WaterLevel" : {"type" : "level",
                                                   "min" : 700,
                                                   "max" : 2200},
                                   "Plant1" : {"type" :"plant",
                                               "min" : 1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump1","pin" : "19",
                                                         "max" : 5}},
                                   "Plant2" : {"type" :"plant",
                                               "min" :1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump2","pin" : "18",
                                                         "max" : 5}},
                                   }
                   },
        "esp2" : {"name" : "esp32-plant-2-main:board",
                   "attributes" : {"Plant3" : {"type" :"plant",
                                               "min" : 1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump3","pin" : "18",
                                                         "max" : 5}},
                                   "Plant4" : {"type" :"plant",
                                               "min" : 1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump4","pin" : "19",
                                                         "max" : 5}},
                                   "Plant5" : {"type" :"plant",
                                               "min" : 1850,
                                               "max" : 2700,
                                               "cooldown":60,
                                               "pump" : {"name":"Pump5","pin" : "21",
                                                         "max" : 3}},
                                   }
                   }
        }

class WaterLevelUnit:
    reader : Board.AnalogReader
    threshold : int
    def __init__(self, r: Board.AnalogReader, t):
        self.reader = r
        self.threshold = t
    async def isWaterLevelOk(self):
        val = await self.reader.read()
        if val < self.threshold:
            return False
        return True    

class PumpUnit:
    board : Board
    pin : int
    pumpTime : int
    name: str

    def __init__(self, b : Board, pin, p, name):
        self.board = b
        self.pin = pin
        self.pumpTime = p
        self.name = name
    async def runPump(self):
        print("running pump {} {}".format(self.name,self.pin))
        pin = await self.board.gpio_pin_by_name(self.pin)
        try:
            await pin.set(True)
            await asyncio.sleep(self.pumpTime)
        except asyncio.CancelledError:
            await pin.set(False)
            raise
        await pin.set(False)
    async def stop(self):
        try :
            await pin.set(False)
        except:
            raise

class PlantUnit:
    reader : Board.AnalogReader
    pump: PumpUnit
    cooldown: int
    next_allowed_activation: datetime.datetime
    min_moisture : int
    name: str
    
    def __init__(self, r : Board.AnalogReader, p : PumpUnit, cooldown, mm, name):
        self.reader = r
        self.pump = p
        self.cooldown = cooldown
        self.next_allowed_activation = datetime.datetime.now()
        self.min_moisture = mm
        self.name = name
    async def waterPlant(self):
        print("Running plant {}".format(self.name))
        if self.next_allowed_activation < datetime.datetime.now():
            val = await self.reader.read()
            print("Current moisture level is {} min is {}".format(val,self.min_moisture))
            if val > self.min_moisture:
                await self.pump.runPump()
            self.next_allowed_activation = datetime.datetime.now() + datetime.timedelta(seconds=self.cooldown)
            print("Plant {} next run is {}".format(self.name,self.next_allowed_activation))
    async def stop(self):
        await self.pump.stop()

class WateringSystem:
    waterLevel : WaterLevelUnit
    plantUnits : list[PlantUnit]
    robot = RobotClient
    config: dict
    def __init__(self, robot: RobotClient, config):
        self.plantUnits = list()
        self.waterLevel = None
        self.robot = robot
        self.config = config
    async def configure(self):
        waterLevel = None
        plantUnits = list()
        for k,v in self.config.items():
            board = Board.from_robot(robot=self.robot,name=v["name"])
            attrs = v["attributes"]
            for k,v in attrs.items():
                if v["type"] == "level":
                    waterLevelreader = await board.analog_reader_by_name(name=k)
                    waterLevel = WaterLevelUnit(waterLevelreader,v["min"])
                if v["type"] == "plant":
                    pumpCfg = v["pump"]
                    pump = PumpUnit(b=board,pin=pumpCfg["pin"],p=pumpCfg["max"],name=pumpCfg["name"])
                    moistureReader = await board.analog_reader_by_name(name=k)
                    plant = PlantUnit(r=moistureReader,p=pump,cooldown=v["cooldown"],mm=v["min"],name=k)
                    plantUnits.append(plant)
        self.waterLevel = waterLevel
        self.plantUnits = plantUnits
    async def runOnce(self):
        if self.waterLevel == None:
            return
        print("Checking if water level is ok")
        if await self.waterLevel.isWaterLevelOk() == False:
            print("Not enough water")
        print("water level good")
        for plant in self.plantUnits:
            await plant.waterPlant()
    async def stop(self):
        for plant in self.plantUnits:
            await plant.stop()

async def main():
    robot = await connect()

    water = WateringSystem(robot,esp1)

    await water.configure()
    while True:
        try:
            await water.runOnce()
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            await water.stop()
            break;
    print("done with watering!")
    await robot.close()
async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    print("killing loops")

    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    [task.cancel() for task in tasks]

    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # May want to catch other signals too
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
        print("Successfully shutdown the Mayhem service.")
```

{{% /expand%}}

## Next Steps

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, head over to the <a href="https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw" target="_blank">Viam Community Slack</a>.
