---
linkTitle: "Drive your first base"
title: "Quickstart: drive your first base"
weight: 30
layout: "docs"
type: "docs"
description: "Configure a fake wheeled base and drive it in a square using the base API. No physical hardware required."
---

In this quickstart we will configure a fake wheeled base and drive
it through four sides of a square: forward 500 mm, turn 90 degrees,
repeat. The code is the same code you would run against a real
wheeled base; only the component model name changes.

By the end you will have:

- A fake base running on your machine.
- A Python script that issues direct `MoveStraight` and `Spin`
  commands.
- A complete square-driving loop that terminates cleanly.

Expected total time: about 10 minutes.

## 1. Add the fake base

In the [Viam app](https://app.viam.com), go to your machine's
**CONFIGURE** tab.

1. Click **+** and add a **base** component.
2. Choose the **fake** model.
3. Name it **my-base**.
4. Click **Create**.

The fake base does not need a motor component to back it. It
accepts base API calls and logs what it would do without physically
actuating anything.

## 2. Drive in a square

Create a file named `first_base.py`:

```python
import asyncio

from viam.robot.client import RobotClient
from viam.components.base import Base


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def drive_square(base):
    for side in range(4):
        print(f"side {side + 1}: forward 500 mm")
        await base.move_straight(distance=500, velocity=500)

        print(f"side {side + 1}: spin 90 degrees")
        await base.spin(angle=90, velocity=100)


async def main():
    async with await connect() as machine:
        my_base = Base.from_robot(machine, "my-base")
        await drive_square(my_base)
        print("done.")


if __name__ == "__main__":
    asyncio.run(main())
```

Replace the three placeholder strings with the machine address and
API key from your **CONNECT** tab. Then:

```sh
pip install viam-sdk
python first_base.py
```

Expected output:

```text
side 1: forward 500 mm
side 1: spin 90 degrees
side 2: forward 500 mm
side 2: spin 90 degrees
side 3: forward 500 mm
side 3: spin 90 degrees
side 4: forward 500 mm
side 4: spin 90 degrees
done.
```

Each `move_straight` and `spin` call blocks until the fake base
reports completion, then the script moves on.

## 3. What the calls do

- **`move_straight(distance, velocity)`**: drive forward the given
  distance in millimeters at the given velocity in millimeters per
  second. Positive distance and velocity both mean forward. Blocks
  until complete.
- **`spin(angle, velocity)`**: rotate in place by the given angle in
  degrees at the given angular velocity in degrees per second.
  Positive angle and velocity turn counterclockwise (left). Blocks
  until complete.

These are direct base API calls. They do not go through the motion
service or the navigation service. There is no obstacle avoidance,
no replanning, and no map awareness. For a wheeled base with a
well-defined short motion, this is what you want.

## 4. Swap to a real base later

When you have a real wheeled base, change the `model` on the `base`
component from `fake` to whatever matches your hardware (for example,
`wheeled` if you have a chassis with two motors, or a vendor module
from the registry). The Python code above does not change.

A real wheeled base also needs motor components configured and wired
to the base so the `MoveStraight` and `Spin` commands actually
actuate wheels. See the [base component documentation](/components/base/)
for the motor-side configuration.

## Where to next

- [Drive a base directly from code](/motion-planning/motion-how-to/drive-a-base/):
  the task-oriented version of this tutorial, covering `SetPower`
  and `SetVelocity` for continuous control.
- [Set up GPS waypoint navigation](/motion-planning/quickstarts/gps-waypoint-navigation/):
  the next step up from direct commands, using the navigation
  service to drive between GPS points.
- [Move your first arm](/motion-planning/quickstarts/first-arm/):
  the arm-side equivalent of this tutorial.
