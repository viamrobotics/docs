---
linkTitle: "Sensor"
title: "Add a sensor"
weight: 70
layout: "docs"
type: "docs"
description: "Add and configure a sensor to read environmental data like temperature, humidity, or distance."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-sensor/
---

Add a sensor to your machine's configuration so you can read environmental data from the Viam app and from code.

## Concepts

The sensor component provides a single method: `GetReadings`, which returns a
map of key-value pairs. This simple interface works for any sensor that
produces named measurements.

Most physical sensors in Viam come from **modules in the registry** rather than
built-in models. This is because the sensor ecosystem is enormous. Thousands
of different devices with different communication protocols exist, and modules cover
specific hardware while keeping the same `GetReadings` API.

## Steps

### 1. Add a sensor component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your sensor hardware. Search by
   sensor name or chip (for example, **DHT22**, **BME280**, **SHT31**). For I2C
   or serial sensors, you can also search by protocol or manufacturer.
4. Name your sensor (for example, `temperature-sensor`) and click **Create**.

If no model exists for your sensor, you can
[write a driver module](/build-modules/write-a-driver-module/) to add support.

### 2. Configure sensor attributes

Attributes vary by sensor module. Common patterns:

**I2C sensor (for example, BME280, SHT31):**

```json
{
  "board": "my-board",
  "i2c_bus": "1",
  "i2c_address": 119
}
```

**Serial sensor (for example, air quality monitors):**

```json
{
  "serial_path": "/dev/ttyUSB0",
  "baud_rate": 9600
}
```

**GPIO sensor (for example, ultrasonic distance):**

```json
{
  "board": "my-board",
  "trigger_pin": "11",
  "echo_pin": "13"
}
```

Check the module's documentation in the registry for the exact attributes your
sensor needs.

### 3. Save and test

Click **Save**, then expand the **TEST** section.

- The test panel shows the output of `GetReadings`, a table of named values.
- Verify the readings make sense (for example, room temperature should be roughly
  20-25°C).

## Try it

Read sensor data programmatically and print it.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.
When you run the code below, you'll see sensor readings printed once per second. Verify the values make sense for your environment.
{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

Save this as `sensor_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    sensor = Sensor.from_robot(robot, "temperature-sensor")

    # Get readings 5 times, once per second
    for i in range(5):
        readings = await sensor.get_readings()
        print(f"Reading {i + 1}: {readings}")
        await asyncio.sleep(1)

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python sensor_test.py
```

You should see output like:

```text
Reading 1: {'temperature_celsius': 22.5, 'humidity_percent': 45.2}
Reading 2: {'temperature_celsius': 22.5, 'humidity_percent': 45.3}
...
```

The exact keys and values depend on your sensor.

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir sensor-test && cd sensor-test
go mod init sensor-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "time"

    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("sensor-test")

    robot, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithCredentials(utils.Credentials{
            Type:    utils.CredentialsTypeAPIKey,
            Payload: "YOUR-API-KEY",
        }),
        client.WithAPIKeyID("YOUR-API-KEY-ID"),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)

    s, err := sensor.FromProvider(robot, "temperature-sensor")
    if err != nil {
        logger.Fatal(err)
    }

    // Get readings 5 times, once per second
    for i := 0; i < 5; i++ {
        readings, err := s.Readings(ctx, nil)
        if err != nil {
            logger.Fatal(err)
        }
        fmt.Printf("Reading %d: %v\n", i+1, readings)
        time.Sleep(1 * time.Second)
    }
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "No readings appear" >}}

- Check physical connections: power, ground, and data lines.
- For I2C sensors, verify the I2C address. Run `i2cdetect -y 1` on Linux to
  scan the bus and confirm the device is visible.
- For serial sensors, check the device path (`ls /dev/ttyUSB*` or
  `ls /dev/ttyACM*`).

{{< /expand >}}

{{< expand "Readings are all zeros or nonsensical" >}}

- The I2C address may be wrong. Some sensors use different addresses depending
  on a jumper or pin configuration.
- The sensor may need a warmup period. Some environmental sensors take
  several seconds to produce valid readings after power-on.

{{< /expand >}}

{{< expand "Module not found in registry" >}}

- Try broader search terms. Module names don't always match sensor model
  numbers exactly.
- If your sensor uses a common protocol (I2C, SPI, serial), there may be a
  generic module that works. Check the registry for protocol-based modules.

{{< /expand >}}

## What's next

- [Sensor API reference](/dev/reference/apis/components/sensor/): full method documentation.
- [Capture and Sync Data](/data/capture-sync/capture-and-sync-data/): automatically
  capture sensor readings and sync them to the cloud.
- [What is a module?](/build-modules/from-hardware-to-logic/): write a module that
  takes action based on sensor readings.
