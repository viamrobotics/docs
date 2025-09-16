---
linkTitle: "Tutorial: Desk Safari"
title: "Tutorial: Desk Safari"
weight: 10
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Follow this tutorial to learn about Viam while building a game."
---

You will build a game in this tutorial in which you repeatedly have 60 seconds to go get an item and find and show it to the camera.
All you need is a laptop or desktop computer and a webcam.

This tutorial assumes no prior knowledge of Viam and will teach you the fundamentals that allow you to build any machine that interacts with the physical world.

While you build this game you will learn:

- [Device setup]() will show you how to install Viam for the tutorial.
- [Overview]() of the building blocks of Viam: modules, components, and services.
- [Using the webcam]() will teach you how to configure and test resources in Viam.
- [Adding machine learning]() will teach you about higher level services.
- [Completing the game]() will teach you how to add the control logic for the game.
- [Playing the game]() will allow you to test your work.

## Device setup

{{< table >}}
{{% tablestep start=1 %}}
**Create a Viam account and log in.**

Navigate to [Viam](https://app.viam.com) in a web browser.
Create a free account and log in.

{{% /tablestep %}}
{{% tablestep %}}
**Navigate to your first location.**

Click **FLEET** in the upper-left corner of the page and click **LOCATIONS**.
Then select the `First Location`.

Viam automatically created an {{< glossary_tooltip term_id="organization" text="organization" >}} for you and a {{< glossary_tooltip term_id="location" text="location" >}} called `First Location`.
You can create more organizations and locations to organize your machines into but for this tutorial you can use the automatically created ones.

{{% /tablestep %}}
{{% tablestep %}}
**Create a new machine.**

Click **+ Add machine** to create your first machine and name it `hello-world`.

A {{< glossary_tooltip term_id="machine" text="machine" >}} represents one or more computers running `viam-server`, the software that manages all connected hardware and any software running on the machine.

{{% /tablestep %}}
{{% tablestep %}}
**Install `viam-server`.**

On the machine's page, follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} to install `viam-server` on the computer you're using for your project.

Wait until your machine has successfully connected to Viam.

{{<imgproc src="/tutorials/hello-world/connected.png" resize="800x" style="width: 500px" declaredimensions=true alt="A machine showing a successfult connection." class="imgzoom shadow">}}

{{% /tablestep %}}
{{< /table >}}

## Overview

TODO: Explain modules, components, services?

## Using the webcam

You can use any webcam that is connected to your computer, a usb-webcam, a built-in one, or a wireless one.

{{< table >}}
{{% tablestep start=1 %}}
**Navigate to the CONFIGURE tab of your machine's page.**

This page is where you configure all hardware and software for a machine.
There are different kinds of {{< glossary_tooltip term_id="resource" text="resources" >}}, you can use.
For this tutorial you will use a {{< glossary_tooltip term_id="component" text="component" >}} and several {{< glossary_tooltip term_id="service" text="services" >}}.

{{% /tablestep %}}

{{% tablestep %}}
**Configure the webcam to use for the Desk safari game.**

Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `camera` type, then select the `webcam` model or another model if you are using a different camera.
Enter the name `webcam` for your camera and click **Create**.

{{% /tablestep %}}
{{% tablestep %}}
**Save your configuration**

Always save your configuration before testing.
This will apply your changes to your machine.

{{% /tablestep %}}
{{% tablestep %}}
**Test the camera stream.**

Click on the camera's **TEST** panel to see the camera stream.

The **TEST** panel is a good tool to ensure {{< glossary_tooltip term_id="resource" text="resources" >}} are working as expected.

If your camera is not working, see [Troubleshooting](/operate/reference/components/camera/webcam/#troubleshooting) and [Common errors](/operate/reference/components/camera/webcam/#common-errors)

{{% /tablestep %}}
{{< /table >}}

## Adding machine learning

You can now see your camera stream on Viam.
For the game, Desk Safari, we will need to apply computer vision to the camera stream.
Viam provides many different machine learning models and computer vision {{< glossary_tooltip term_id="service" text="services" >}}.

For this tutorial, you will use:

- the `EfficientDet-COCO` model from the Viam Registry. The model can detect a variety of objects. You can see all objects in the <file>[labels.txt](/static/labels.txt)</file> file.
- the ML model service, which runs the machine learning model on your machine and resturns inferences.
- the vision service, which uses the machine learning model, applies it to the camera stream and returns any objects it identifies.

Let's configure all these:

{{< table >}}
{{% tablestep start=1 %}}
**Add multiple resources in one step.**

On the **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Insert fragment**.
Select the `HelloWorldMLResources` fragment by the `Robot Land` organization.
Click **Insert fragment**.

{{% /tablestep %}}
{{% tablestep %}}
**Investigate the new resources.**

A {{< glossary_tooltip term_id="fragment" text="fragment" >}} is a set of {{< glossary_tooltip term_id="resource" text="resources" >}} which are often used together.
In this case, the fragment contains the module that contains the ML model service which runs the model, as well as a vision service that applies the model to the camera stream.

Review the configuration for each new resource and click on their **TEST** panels to try them.

{{% /tablestep %}}
{{< /table >}}

## Completing the game

You've now got the camera working and the vision service can detect objects in the camera stream.
Now you need to add the game's logic.

The game loop works as follows:

- The player does something to start the game.
- The game provides the player with a prompt, an item to get and hold up to the camera within 60 seconds.
  If a matching object is detected within 60 seconds, the game continues with another prompt.
  Once the player fails to hold up a recognizable object in the given time frame, the game ends.
- A score is reported.

To implement this logic, you'll create your own {{< glossary_tooltip term_id="resource" text="resource" >}} and {{< glossary_tooltip term_id="module" text="module" >}}.

Viam supports standardized component and service APIs.
For control logic, you often implement the generic service, which only has one method that you need to implement: `DoCommand`.
The `DoCommand` method allows you to pass any JSON objects, such as `{"cmd": "start_game"}`.
If implemented the resource will execute the logic associated with that command when passed this command.

However, there is another API that fits out purpose, the Button API.
If you think about the player starting the game, the action they take is to issue some command to start the game, which is like pushing a button.
We can therefore use the Button API which allows you to implement both the `DoCommand` and the `Push` method.

{{< table >}}
{{% tablestep start=1 %}}
**Install the CLI.**

You must have the Viam CLI installed to generate and upload modules:

{{< readfile "/static/include/how-to/install-cli.md" >}}
{{% /tablestep %}}
{{% tablestep %}}
**Find your organization ID.**

Run the following command to list your organizations and their IDs:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organization list
Organizations for "user@viam.com":
	User's org (id: a12b3c4d-1234-123a-12a3-a1b23c45d67e)
```

{{% /tablestep %}}
{{% tablestep %}}
**Generate the module template.**

<!-- Choose your preferred programming language and execute the respective command. -->

Replace `<ORGANIZATION-ID>` with your organization ID, which resembles: `a12b3c4d-1234-123a-12a3-a1b23c45d67e`.

{{< tabs >}}
{{% tab name="Python" %}}

```sh {class="command-line" data-prompt="$" data-output="4-10"}
viam module generate --language python --model-name game-logic \
  --name hello-world-game-py --public-namespace <ORGANIZATION-ID> \
  --register true
```

{{% /tab %}}
{{< /tabs >}}

A UI will show.
Press enter to confirm each option.

For **Select a resource to be added to the module**, select **Button Component**

{{% /tablestep %}}
{{% tablestep %}}
**Open the generated files.**

{{< tabs >}}
{{% tab name="Python" %}}

The module generator has created the following files:

```treeview
hello-world-game/
└── src/
|   ├── models/
|   |   └── game_logic.py
|   └── main.py
└── README.md
└── build.sh
└── meta.json
└── requirements.txt
└── run.sh
└── setup.sh
```

Open <FILE>hello-world-game/src/models/game_logic.py</FILE>.
This is the template for the Button API that you will add the game logic.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the Push method.**

{{< tabs >}}
{{% tab name="Python" %}}

In the <FILE>hello-world-game/src/models/game_logic.py</FILE> file, find the `class GameLogic` at the top of the file.
Add a class attribute to set to `True` for the game to start.
When you build the game loop you will use this attribute to start the game.

```python {class="line-numbers linkable-line-numbers" data-line="7" data-start="15" }
class GameLogic(Button, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("naomi", "hello-world-game-py"), "game-logic"
    )
    start = None
```

Then implement the `Push` method to set the `start` attribute to `True` when pushed.

```python {class="line-numbers linkable-line-numbers" data-line="8-10" data-start="67" }
    async def push(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> None:
        self.logger.info("`push` is called")
        self.start = True
        self.logger.info("Game is starting.")

```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the game loop.**

{{< tabs >}}
{{% tab name="Python" %}}

In the <FILE>hello-world-game/src/models/game_logic.py</FILE> file, add the following imports:

```python {class="line-numbers linkable-line-numbers" }
import asyncio
from threading import Event
```

Add class attributes for the counter and :

```python {class="line-numbers linkable-line-numbers" data-line="7" data-start="17" }
class GameLogic(Button, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("naomi", "hello-world-game-py"), "game-logic"
    )
    start = None
    counter = 0
    event = Event()
```

Add

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the DoCommand method.**

{{< tabs >}}
{{% tab name="Python" %}}

In the <FILE>hello-world-game/src/models/game_logic.py</FILE> file,

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Test your module.**

{{< tabs >}}
{{% tab name="Python" %}}
TODO
{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Upload your module.**

{{< tabs >}}
{{% tab name="Python" %}}
TODO
{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure your module.**

TODO

{{% /tablestep %}}
{{< /table >}}

## Playing the game

TODO

- mention viam applications
- mention the test panel (?)
- provide a viam application for testing
- point to github code for the Viam application

TODO preview

TODO - what's next

{{< alert title="Want to train your own model instead?" color="note" >}}
If you wish to train your own ML model, see [Train a TF or TFLite model](/data-ai/train/train-tf-tflite/).
{{< /alert >}}
