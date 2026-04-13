---
linkTitle: "Tutorial: Python monitoring service"
title: "Build a Python monitoring service"
weight: 115
layout: "docs"
type: "docs"
description: "Build a Python service that connects to a Viam machine, monitors a sensor, controls a motor based on sensor readings, and shuts down cleanly."
date: "2026-04-13"
---

In this tutorial, you will build a Python service that runs without a user interface. The finished service:

- Connects to a Viam machine at startup
- Starts a motor
- Polls a sensor every two seconds and logs the readings
- Stops the motor when a sensor reading exceeds a threshold
- Shuts down cleanly when you press Ctrl+C

You will learn the pattern that most headless Viam apps follow: connect, act, monitor, react, clean up. The same structure works for any long-running Python process that talks to a machine: a control loop, a data logger, a fleet monitor, or an integration service.

## What you need

- A configured Viam machine with a sensor and a motor. Any models work. If you do not have physical hardware, add `fake:sensor` and `fake:motor` in the Viam app's **CONFIGURE** tab.
- A completed [Python setup](../setup/python/). You should have a project directory with `viam-sdk` installed, a `.env` file holding your machine credentials, and a working `main.py` from the setup page.
- A second window open to the Viam app's **CONTROL** tab for the same machine, so you can see motor state changes as they happen.

Before continuing, confirm your setup by running `python main.py` and verifying that it shows `Connected. Found N resources.` If it does not, go back to [Python setup](../setup/python/) and fix the connection before continuing.

## Step 1: Connect and list resources

Replace the contents of `main.py` with a connection that prints the machine's resources:

```python
import asyncio
import os

from dotenv import load_dotenv
from viam.robot.client import RobotClient

load_dotenv()


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["API_KEY"],
        api_key_id=os.environ["API_KEY_ID"],
    )
    machine = await RobotClient.at_address(os.environ["MACHINE_ADDRESS"], opts)

    print(f"Connected. Resources: {[r.name for r in machine.resource_names]}")

    await machine.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```sh {class="command-line" data-prompt="$"}
python main.py
```

You should see a list of resource names that includes your sensor and motor. If the names you see do not match the names you configured, update the constants in the next step to match.

## Step 2: Get the sensor and motor, start the motor

Add imports for `Sensor` and `Motor`, get them by name, and start the motor:

```python
import asyncio
import os

from dotenv import load_dotenv
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor
from viam.components.motor import Motor

load_dotenv()

SENSOR_NAME = "my_sensor"
MOTOR_NAME = "my_motor"


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["API_KEY"],
        api_key_id=os.environ["API_KEY_ID"],
    )
    machine = await RobotClient.at_address(os.environ["MACHINE_ADDRESS"], opts)

    sensor = Sensor.from_robot(robot=machine, name=SENSOR_NAME)
    motor = Motor.from_robot(robot=machine, name=MOTOR_NAME)

    await motor.set_power(power=0.5)
    print(f"Motor '{MOTOR_NAME}' started at 50% power.")

    await machine.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Change `SENSOR_NAME` and `MOTOR_NAME` to match the names you gave these components in your machine configuration. If you used `fake:sensor` and `fake:motor`, the default names are usually `sensor` and `motor` unless you changed them.

Run it. The terminal prints `Motor 'my_motor' started at 50% power.` Check the Viam app's **CONTROL** tab: the motor's power slider should show 50%. The script connects, starts the motor, and immediately closes the connection (which stops the motor through session cleanup). In the next step, you will keep the connection open.

## Step 3: Poll the sensor in a loop

Replace the `await machine.close()` call with a polling loop that reads the sensor every two seconds:

```python
POLL_INTERVAL = 2  # seconds


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["API_KEY"],
        api_key_id=os.environ["API_KEY_ID"],
    )
    machine = await RobotClient.at_address(os.environ["MACHINE_ADDRESS"], opts)

    sensor = Sensor.from_robot(robot=machine, name=SENSOR_NAME)
    motor = Motor.from_robot(robot=machine, name=MOTOR_NAME)

    await motor.set_power(power=0.5)
    print(f"Motor '{MOTOR_NAME}' started at 50% power.")

    print(f"Monitoring sensor '{SENSOR_NAME}' every {POLL_INTERVAL}s. Press Ctrl+C to stop.")

    while True:
        readings = await sensor.get_readings()
        print(f"  {readings}")
        await asyncio.sleep(POLL_INTERVAL)
```

Run it. The terminal prints sensor readings every two seconds. For `fake:sensor`, the output is `{'a': 1, 'b': 2, 'c': 3}` on every line. For a real sensor, the values change. The motor stays running in the background because the connection is still open.

Press Ctrl+C to stop the script. The motor stops because the session ends, but the shutdown is abrupt: Python prints a traceback. The next step fixes this.

## Step 4: Add graceful shutdown

Wrap the polling loop in a try/finally block so the motor stops and the connection closes cleanly when you press Ctrl+C:

```python
async def main():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["API_KEY"],
        api_key_id=os.environ["API_KEY_ID"],
    )
    machine = await RobotClient.at_address(os.environ["MACHINE_ADDRESS"], opts)

    sensor = Sensor.from_robot(robot=machine, name=SENSOR_NAME)
    motor = Motor.from_robot(robot=machine, name=MOTOR_NAME)

    await motor.set_power(power=0.5)
    print(f"Motor '{MOTOR_NAME}' started at 50% power.")

    print(f"Monitoring sensor '{SENSOR_NAME}' every {POLL_INTERVAL}s. Press Ctrl+C to stop.")

    try:
        while True:
            readings = await sensor.get_readings()
            print(f"  {readings}")
            await asyncio.sleep(POLL_INTERVAL)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print("Shutting down...")
        await motor.stop()
        await machine.close()
        print("Motor stopped. Connection closed.")
```

Run it. The sensor readings print as before. Press Ctrl+C. Instead of a traceback, you see:

```text
Shutting down...
Motor stopped. Connection closed.
```

Check the **CONTROL** tab: the motor's power slider returns to zero. The shutdown is clean: the motor is explicitly stopped, not just abandoned when the session ends.

## Step 5: Add a threshold check

Add logic that stops the motor when a sensor reading exceeds a threshold. This is the "reads drive writes" pattern: the service observes a condition and takes an action.

Add two constants at the top of the file:

```python
READING_KEY = "a"       # The sensor reading key to monitor
THRESHOLD = 0           # Stop the motor when this value is exceeded
```

Update the polling loop to check the reading:

```python
    try:
        while True:
            readings = await sensor.get_readings()
            value = readings.get(READING_KEY)
            print(f"  {READING_KEY}={value}")

            if value is not None and value > THRESHOLD:
                print(f"  THRESHOLD EXCEEDED ({value} > {THRESHOLD})")
                break

            await asyncio.sleep(POLL_INTERVAL)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print("Shutting down...")
        await motor.stop()
        await machine.close()
        print("Motor stopped. Connection closed.")
```

`READING_KEY` is the key from the sensor's readings map to watch. `THRESHOLD` is the value that triggers the motor stop. For `fake:sensor`, set `READING_KEY` to `"a"` and `THRESHOLD` to `0`. Since `fake:sensor` returns `a=1`, the condition `1 > 0` is true on the first reading and the motor stops immediately. For a real sensor, set these to values that match your hardware.

Run it. The output shows one reading, the threshold message, and the shutdown:

```text
Motor 'my_motor' started at 50% power.
Monitoring sensor 'my_sensor' every 2s. Press Ctrl+C to stop.
  a=1
  THRESHOLD EXCEEDED (1 > 0)
Shutting down...
Motor stopped. Connection closed.
```

To see the monitoring loop run for longer, raise `THRESHOLD` above the sensor's maximum value. The service polls indefinitely until you press Ctrl+C or the threshold triggers.

## The complete script

Here is the full `main.py`:

```python
import asyncio
import os

from dotenv import load_dotenv
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor
from viam.components.motor import Motor

load_dotenv()

SENSOR_NAME = "my_sensor"
MOTOR_NAME = "my_motor"
READING_KEY = "a"
THRESHOLD = 0
POLL_INTERVAL = 2


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["API_KEY"],
        api_key_id=os.environ["API_KEY_ID"],
    )
    machine = await RobotClient.at_address(os.environ["MACHINE_ADDRESS"], opts)

    sensor = Sensor.from_robot(robot=machine, name=SENSOR_NAME)
    motor = Motor.from_robot(robot=machine, name=MOTOR_NAME)

    await motor.set_power(power=0.5)
    print(f"Motor '{MOTOR_NAME}' started at 50% power.")

    print(f"Monitoring sensor '{SENSOR_NAME}' every {POLL_INTERVAL}s. Press Ctrl+C to stop.")

    try:
        while True:
            readings = await sensor.get_readings()
            value = readings.get(READING_KEY)
            print(f"  {READING_KEY}={value}")

            if value is not None and value > THRESHOLD:
                print(f"  THRESHOLD EXCEEDED ({value} > {THRESHOLD})")
                break

            await asyncio.sleep(POLL_INTERVAL)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print("Shutting down...")
        await motor.stop()
        await machine.close()
        print("Motor stopped. Connection closed.")


if __name__ == "__main__":
    asyncio.run(main())
```

The full script is 50 lines. Five constants at the top configure the behavior. One async function handles the full lifecycle: connect, start, monitor, react, clean up.

## What you built

You now have a Python service that:

- Connects to a Viam machine using an API key from environment variables
- Starts a motor and monitors a sensor in a polling loop
- Stops the motor when a sensor reading exceeds a configurable threshold
- Shuts down cleanly on Ctrl+C, explicitly stopping the motor and closing the connection

This is the pattern for any headless Viam app: connect, do something, monitor something, react to conditions, clean up on exit. The specifics change (different sensors, different actions, different conditions), but the structure stays the same.

## Next steps

Extend the service in one of these directions:

- **Monitor multiple sensors.** Get additional sensors with `Sensor.from_robot` and read from all of them in the same loop. Log each one separately.
- **Add hysteresis.** Instead of stopping the motor permanently when the threshold is exceeded, restart it when the reading drops back below a lower threshold. This prevents rapid start-stop cycling around the boundary.
- **Log to a file or external system.** Replace `print()` with Python's `logging` module, or send readings to a database, Prometheus, or a notification service.
- **Run as a system service.** Deploy the script as a systemd unit so it starts on boot and restarts on failure. The graceful shutdown pattern you built in Step 4 handles `SIGTERM` from systemd the same way it handles Ctrl+C.
- **Connect to the Viam cloud instead of one machine.** Switch from `RobotClient.at_address` to `ViamClient.create_from_dial_options` to monitor sensors across a fleet. See [Connect to the Viam cloud](../tasks/connect-to-cloud/).
