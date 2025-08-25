---
linkTitle: "Move a gantry"
title: "Move a gantry"
weight: 60
layout: "docs"
type: "docs"
description: "Move a gantry with linear actuator positions or automated motion planning."
---

You have two options for moving a [gantry](/operate/reference/components/gantry/):

- Move each axis of the gantry directly with the [gantry API](/dev/reference/apis/components/gantry/)
- Use automated complex motion planning with the [motion planning service API](/dev/reference/apis/services/motion/)

## Prerequisites

{{% expand "A running machine connected to Viam. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

## Configure and connect to your gantry

{{< table >}}
{{% tablestep start=1 %}}
**Configure the gantry's motor components**

First, connect the gantry's motors to your machine.

Then, navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Search for and select a model that supports your motor.

Complete the motor configuration and use the **TEST** panel in the configuration card to test that the motor is working.

Repeat this for each motor of your gantry.

{{% /tablestep %}}
{{% tablestep %}}
**Configure a gantry component**

Use the **+** button again to add gantry components.

If you have a multi-axis gantry, [configure a single-axis gantry](/operate/reference/components/gantry/single-axis/) for each axis, and then [configure a multi-axis gantry](/operate/reference/components/gantry/multi-axis/) to combine them all into one coordinated unit.

{{% /tablestep %}}
{{% tablestep %}}
**Connect code to your gantry**

Go to your machine's **CONNECT** tab.
Select your preferred programming language and copy the code snippet.

See [Create a web app](/operate/control/web-app/), [Create a mobile app](/operate/control/mobile-app/), or [Create a headless app](/operate/control/headless-app/) for more information, depending on your use case.

{{% /tablestep %}}
{{< /table >}}

## Control each axis

The following is an example Python script using the gantry API.
For more methods and code snippets in more languages, see [Gantry API](/dev/reference/apis/components/gantry/).

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.gantry import Gantry


async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with
        # your machine's API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with
        # your machine's API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address("<MACHINE-ADDRESS>", opts)


async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)

    # get gantry-1
    gantry_1 = Gantry.from_robot(machine, "gantry-1")
    gantry_1_return_value = await gantry_1.get_lengths()
    print(f"gantry-1 get_lengths return value: {gantry_1_return_value}")

    # Home the gantry
    await gantry_1.home()

    # Move this three-axis gantry to a position 5mm in the
    # positive Y direction from (0,0,0)
    # and set the speed of each axis to 8 mm/sec
    await gantry_1.move_to_position([0, 5, 0], [8, 8, 8])

    # Don't forget to close the machine when you're done!
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## Use automated complex motion planning

{{% alert title="Important" color="note" %}}

Before using the motion service with a gantry, you must [define your gantry's reference frame](/operate/reference/services/frame-system/).

{{% /alert %}}

The following is an example Python script using the motion planning API.
For more methods and code snippets in more languages, see [Motion API](/dev/reference/apis/services/motion/).

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.gantry import Gantry
from viam.services.motion import MotionClient
from viam.proto.common import Pose, PoseInFrame


async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with
        # your machine's API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with
        # your machine's API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address("<MACHINE-ADDRESS>", opts)


async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)

    # get gantry-1
    gantry_1 = Gantry.from_robot(machine, "gantry-1")
    gantry_1_return_value = await gantry_1.get_lengths()
    print(f"gantry-1 get_lengths return value: {gantry_1_return_value}")

    motion = MotionClient.from_robot(robot=machine, name="builtin")

    goal_pose = Pose(x=0, y=0, z=300, o_x=0, o_y=0, o_z=1, theta=0)
    # Move the gantry
    await motion.move(
        component_name=gantry_1,
        destination=PoseInFrame(reference_frame="myFrame", pose=goal_pose))

    # Don't forget to close the machine when you're done!
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```
