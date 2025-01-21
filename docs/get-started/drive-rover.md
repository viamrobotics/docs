---
title: "Drive a rover in a square in 2 minutes"
linkTitle: "Drive a rover (2 min)"
type: "docs"
images: ["/general/code.png"]
description: "Use a Viam SDK to program a rover to move in a square."
videos:
  ["/tutorials/try-viam-sdk/image1.webm", "/tutorials/try-viam-sdk/image1.mp4"]
videoAlt: "A Viam Rover driving in a square"
images: ["/tutorials/try-viam-sdk/image1.gif"]
aliases:
  - /tutorials/appendix/try-viam-sdk
  - /tutorials/viam-rover/try-viam-sdk
  - /tutorials/viam-rover/try-viam-sdk
  - "/try-viam/try-viam-tutorial/"
  - "/get-started/try-viam/try-viam-tutorial/"
  - "/get-started/quickstarts/drive-rover/"
tags: ["base", "viam rover", "try viam", "sdk", "python", "flutter"]
level: "Beginner"
authors: []
weight: 10
no_list: true
date: "2024-07-31"
cost: "0"
resource: "quickstart"
languages: ["python", "go", "typescript", "flutter", "c++"]
viamresources: ["base"]
platformarea: ["core"]
level: "Beginner"
date: "2022-12-08"
# updated: ""
cost: "0"
---


This is the first of a few quickstarts which will guide you through the concepts you need to know to get started with Viam.
In this guide you'll write code that makes a rover drive in a square.

{{< alert title="You will learn" color="tip" >}}

- How to run SDK code
- How to use the base API to move a rover in a square
- How to use a vision service to find a color with your rover 

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/daU5iNsSO0w">}}

## Requirements

You don't need to buy or own any hardware to complete this tutorial.
You only need the following:

- A Linux, macOS or Windows computer that can run SDK code.
- A [borrowed Viam Rover](https://app.viam.com/try), [your own Viam Rover](/appendix/try-viam/rover-resources/), or [another mobile robot](/tutorials/configure/configure-rover/).
  You can use [Try Viam](https://app.viam.com/try) to borrow a rover online at no cost which is already configured with all the components you need.
  If you have your own rover on hand, whether it's a [Viam rover](https://www.viam.com/resources/rover) or not, these instructions work for any wheeled robot that can be configured as a [base component](/components/base/wheeled/).

## Instructions

Follow these steps to get your rover ready inside the Viam app and write code to control it:

{{< expand "Step 1: Borrow a Viam Rover" >}}

Go to [Try Viam](https://app.viam.com/try) and borrow a rover.
If a rover is available, the rover will take up to 30 seconds to be configured for you.

{{< alert title="Tip" color="tip" >}}
If you are running out of time during your session, you can [extend your rover session](/appendix/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

{{< /expand >}}
{{< expand "Step 2: Copy and run the sample code" >}}

The sample code on the **CONNECT** tab will show you how to authenticate and connect to a machine, as well as some of the methods you can use on your configured components and services.

{{< tabs >}}
{{% tab name="Python" %}}

Go to the **CONNECT** tab and select **Python**.
Save your API key and API key ID as environment variables or include them in the code:

Copy the code into a file called <FILE>square.py</FILE> and run the sample code to connect to your machine:

```sh {class="command-line" data-prompt="$"}
python3 square.py
```

The program prints an array of resources.
These are the components and services that the machine is configured with in the Viam app.

```sh {class="command-line" data-prompt="$" data-output="2-75"}
python3 square.py
2024-08-09 13:21:52,423    INFO    viam.rpc.dial (dial.py:293)    Connecting to socket: /tmp/proxy-BzFWLZQ2.sock
Resources:
[<viam.proto.common.ResourceName rdk:service:sensors/builtin at 0x105b12700>, <viam.proto.common.ResourceName rdk:component:motor/left at 0x105b122a0>, <viam.proto.common.ResourceName rdk:component:camera/cam at 0x105b12390>, <viam.proto.common.ResourceName rdk:component:board/local at 0x105b129d0>, <viam.proto.common.ResourceName rdk:component:base/viam_base at 0x105b12610>, <viam.proto.common.ResourceName rdk:service:motion/builtin at 0x105b12a20>, <viam.proto.common.ResourceName rdk:component:encoder/Lenc at 0x105b12a70>, <viam.proto.common.ResourceName rdk:component:motor/right at 0x105b12ac0>, <viam.proto.common.ResourceName rdk:component:encoder/Renc at 0x105b12b10>]
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}
{{< expand "Step 3: Drive a rover in a square" >}}

Now that you have connected the rover to Viam with the SDK, you can write code to move the rover in a square:

{{< tabs >}}
{{% tab name="Python" %}}

The base is responsible for controlling the motors attached to the base of the rover.
Ensure that the `Base` class is being imported:

```python
from viam.components.base import Base
```

Then paste this snippet above your `main()` function, it will move any base passed to it in a square:

```python
async def moveInSquare(base):
    for _ in range(5):
        # moves the rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500)
        print("move straight")
        # spins the rover 90 degrees at 120 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")
```

{{% alert title="Tip" color="tip" %}}

If you are interested to learn about what other commands you can give to a base, see the standardized [base API](/components/base/#api) for a full list of available API methods. 
{{% /alert %}}

Next, remove all the code in the `main()` function between where the machine connection is established and closed and instead initialize your `base` and invoke the `moveInSquare()` function.

On the Try Viam rovers, the default base name is `viam_base`.
If you have a different base name, update the name in your code.

```python {class="line-numbers linkable-line-numbers" data-line="4-8"}
async def main():
    machine = await connect()

    # Get the base component from the rover
    roverBase = Base.from_robot(machine, 'viam_base')

    # Move the rover in a square
    await moveInASquare("roverBase")

    # await machine.close()
```

If you have a borrowed Try Viam rover, navigate to your machine's **CONTROL** tab, which allows you to interact with your machine's {{< glossary_tooltip term_id="resource" text="resources" >}}.

Click on one of the camera panels and toggle the camera stream on so you can observe the rover's movements.

Then run your code and watch your rover move in a square.

<div class="td-max-width-on-larger-screens">
{{<gif webm_src="/tutorials/try-viam-sdk/image2.webm" mp4_src="../../try-viam-sdk/image2.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square on the left, and on the right, a terminal window shows the output of running the square function as the rover moves in a square.">}}
</div>

{{% /tab %}}
{{< /tabs >}}
{{< /expand>}}

{{< expand "Step 4: Add a vision service" >}}

As you have seen from the **CONTROL** tab, your rover has cameras.
You can use these cameras to adjust your rovers behaviour.

We will start by adding a vision service called `color_detector`.
Go to your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com).

Click the add component button and add the `color_detector` vision service.
Configure it to detect dark blue (`#1b2c69`).
Set **Hue tolerance** to 0.05 and **segment size** to 100.

Use the **TEST** panel to check that vision service works as expected.

{{< /expand >}}
{{< expand "Step 5: Test your rover's vision" >}}

If you haven't yet, move your rover into the middle of its enclosure.

Start by writing the code to detect the color:

```python {class="line-numbers linkable-line-numbers"}
async def check_detections(camera_name, detector):
    detections = await detector.get_detections_from_camera(camera_name)
    print(detections)
    for d in detections:
        if d.confidence > 0.6:
            print("detected")
            return true
    return false
```

Now we'll slowly make the rover spin until it detects the configured color.

```python {class="line-numbers linkable-line-numbers"}
async def spin_slowly_until_color_detected(base, camera, detector):
    # spins the rover 5 degrees at 10 degrees per second
    white True:
      await base.spins(velocity=100, angle=5)
      print("spin 5 degrees")
      time.sleep(0.1)
      ret = await check_detections(camera, detector)
      if ret:
        return

```

Once it has found the color, let's make the rover do a small victory dance by making it move forward and backwards twice and then spinning in a circle for a random time.
Since the rover's victory dance will make the rover lose focus of the color, it will then need to recommence finding its color.

```python {class="line-numbers linkable-line-numbers"}
from random import randint

async def victory_dance(base):
    print("performing victory dance")
    await base.move_straight(velocity=500, distance=100)
    await base.move_straight(velocity=500, distance=-100)
    await base.move_straight(velocity=500, distance=100)
    await base.move_straight(velocity=500, distance=-100)

    rand_angle = randint(500,2000)
    print("spinning: {}".format(rand_angle))
    await base.spin(velocity=500, angle=rand_angle)
```

Use this code in a loop:

```python {class="line-numbers linkable-line-numbers" data-line="5"}
import time

    detector = VisionClient.from_robot(machine, "vision-1")

    while True:
      await spin_slowly_until_color_detected(roverBase, "cam", detector)
      await victory_dance(roverBase)
      time.sleep(3)

```

{{< /expand >}}


## Next steps

Now that you have run your first code to control a machine running Viam code to control your machine, move to the next quickstart to learn how to configure and control a motor:

{{< cards >}}
{{% card link="/get-started/control-motor/" %}}
{{< /cards >}}
