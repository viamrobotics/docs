---
linkTitle: "Move a base"
title: "Move a wheeled robot base"
weight: 40
layout: "docs"
type: "docs"
description: "Move a mobile robot with manual or autonomous navigation."
aliases:
  - /how-tos/navigate/
  - /use-cases/navigate/
---

You have three options for moving a mobile robot [base](/operate/reference/components/base/):

- Give direct commands such as `Spin` and `MoveStraight` using the [base API](/dev/reference/apis/components/base/)
- Send the base to a destination on a SLAM map or to a GPS coordinate using the [motion planning service API's](/dev/reference/apis/services/motion/) `MoveOnMap` or `MoveOnGlobe` commands, respectively
- Define waypoints and move your base along those waypoints while avoiding obstacles, using the [navigation service API](/dev/reference/apis/services/navigation/)

## Prerequisites

{{% expand "A running machine connected to Viam. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

## Configure and connect to your base

{{< table >}}
{{% tablestep start=1 %}}
**Configure the base's motor components**

First, connect the base's motors to your machine.

Then, navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Search for and select a model that supports your motor.

Complete the motor configuration and use the **TEST** panel in the configuration card to test that the motor is working.

Repeat this for each motor of your base.

{{% /tablestep %}}
{{% tablestep %}}
**Configure a base component**

The base component allows you to more easily coordinate the motion of the motors to move the robot's as a whole.

Use the **+** button again to add a base component.
The `wheeled-base` model supports robotic bases with motors on both sides for differential steering.

{{% /tablestep %}}
{{% tablestep %}}
**Connect code to your base**

Go to your machine's **CONNECT** tab.
Select your preferred programming language and copy the code snippet.

See [Create a web app](/operate/control/web-app/), [Create a mobile app](/operate/control/mobile-app/), or [Create a headless app](/operate/control/headless-app/) for more information, depending on your use case.

{{% /tablestep %}}
{{< /table >}}

## Move your base using the base API

The following example script drives a rover in a square.
For code examples in more languages, see [Drive a rover in a square](/tutorials/control/drive-rover/).

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions


async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with your machine's
        # API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address("<MACHINE-ADDRESS>", opts)


async def moveInSquare(base):
    for _ in range(4):
        # moves the rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")


async def main():
    machine = await connect()

    roverBase = Base.from_robot(machine, 'viam_base')

    # Move the rover in a square
    await moveInSquare(roverBase)

    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
    "context"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils")

func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // moves the rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
    }
}

func main() {
    logger := logging.NewLogger("client")
    machine, err := client.New(
      context.Background(),
      // TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
      "<MACHINE-ADDRESS>",
      logger,
      client.WithDialOptions(utils.WithEntityCredentials(
      // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
      // API key ID
      "<API-KEY-ID>",
      utils.Credentials{
          Type:    utils.CredentialsTypeAPIKey,
          // TODO: Replace "<API-KEY>" (including brackets) with your machine's
          // API key
          Payload: "<API-KEY>",
      })),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer machine.Close(context.Background())

    // Get the base from the rover
    roverBase, err := base.FromRobot(machine, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    // Move the rover in a square
    moveInSquare(context.Background(), roverBase, logger)
}
```

{{% /tab %}}
{{< /tabs >}}

## Move your base using GPS

To move a base component directly to a destination GPS point, you can use the motion service API's [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) command.

If you'd like to plan a more detailed path through a series of waypoints, use the [navigation service API](/dev/reference/apis/services/navigation/).
The following tutorial demonstrates how to use GPS navigation with a robot base:

{{< cards >}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}

## Move your base on a SLAM map

To move a base component to a destination pose on a SLAM map, use the motion service API's [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) command.
