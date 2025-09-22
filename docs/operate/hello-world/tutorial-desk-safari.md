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

- [Device setup](#device-setup) will show you how to install Viam for the tutorial.
- [Overview](#overview) of the building blocks of Viam: modules, components, and services.
- [Using the webcam](#using-the-webcam) will teach you how to configure and test resources in Viam.
- [Adding computer vision](#adding-computer-vision) will teach you about higher level services.
- [Completing the game](#completing-the-game) will teach you about modules and how to add the control logic for the game.
- [Playing the game](#playing-the-game) will allow you to test your work.

## Game overview

TODO

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

By installing `viam-server` on your device, you've turned your computer into a Viam {{< glossary_tooltip term_id="machine" text="machine" >}}.

At this point, your machine only runs the Viam software.
To make your machine do something interesting, you must add functionality to it.

When you use Viam to build a machine, you mix and match different building blocks, to make the machine do exactly what you need it to.
The building blocks you'll use in this tutorial are **components**, **services**, and **modules**.
These are the main building blocks that make up all machines.

Let's start by adding a component.

## Using the webcam

{{< glossary_tooltip term_id="component" text="Components" >}} are the resources that your machine uses to sense and interact with the world, such as cameras, motors, sensors, and more.

For this tutorial, you can use any webcam that is connected to your computer, a usb-webcam, a built-in one, or a wireless one.

{{< table >}}
{{% tablestep start=1 %}}
**Navigate to the CONFIGURE tab of your machine's page.**

This page is where you configure all hardware and software for a machine.
There are different kinds of {{< glossary_tooltip term_id="resource" text="resources" >}}, you can use.

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

You can now see your camera stream on Viam.
For the game, Desk Safari, you will need to apply computer vision to the camera stream.

## Adding computer vision

{{< glossary_tooltip term_id="service" text="Services" >}} are higher-level software capabilities that process and interpret data or interact with the world.
Viam provides many different services, including ones to run machine learning models and computer vision.

For this tutorial, you will use:

- a model called `EfficientDet-COCO`, which is publicly available. The model can detect a variety of objects. You can see all objects in the <file>[labels.txt](/static/labels.txt)</file> file.
- a ML model service, which runs a machine learning model on your machine and resturns inferences.
- a vision service, which uses the machine learning model, applies it to the camera stream, and returns any objects it identifies.

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

If you check the resources added by the fragment, you'll see an additional resource called `tflite_cpu`.
This is a {{< glossary_tooltip term_id="module" text="module" >}}.
Modules are packages of code that contain components and services.
They're like plugins that expand what your machine can do without modifying Viam's core software.

Viam has a registry of modules that contain resources you can use when building your machines.
Of course, you can also build your own modules and resources.
In fact, you will create a resource for the game's control logic in the next step.

## Completing the game

You've now got the camera working and the vision service can detect objects in the camera stream.
Now you need to add the game's logic.

The game loop works as follows:

- The player does something to start the game.
- The game provides the player with a prompt, an item to get and hold up to the camera within 60 seconds.
- If the vision service detects a matching object within 60 seconds, the game continues with another prompt.
- Once the player fails to hold up a recognizable object within 60 seconds, the game ends.
- The game returns the score and the player can start a new game.

To implement this logic, you'll create your own {{< glossary_tooltip term_id="resource" text="resource" >}} and package it inside a {{< glossary_tooltip term_id="module" text="module" >}}.

Viam provides a range of standardized component and service APIs.
When you create a resource, you implement the API among them that most closely fits your needs.

For control logic, the generic service is often a good fit.
It doesn't have any methods aside from `DoCommand`.
The `DoCommand` method allows you to pass commands as JSON objects, such as `{"cmd": "start_game"}`.
You can use the `DoCommand` method to implement everything that doesn't fit into other API methods.

However, there is another API that fits out purpose, the Button API which has the methods `DoCommand` and the `Push`.
If you think about the player starting the game, the action they take is to issue some command to start the game, which is like pushing a button.

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
**Inspect the generated files.**

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

- **<FILE>README.md</FILE>**: a template for the module which gets uploaded to the registry when you upload the module.
- **<FILE>meta.json</FILE>**: metadata about the module which gets uploaded to the registry when you upload the module.
- **<FILE>main.py</FILE>** and **<FILE>game_logic.py</FILE>**: the code that registers the module and resource and provides the model implementation.
- **<FILE>setup.sh</FILE>** and **<FILE>requirements.txt</FILE>**: a script that creates a virtual environment and installs the dependencies listed in <FILE>requirements.txt</FILE>.
- **<FILE>build.sh</FILE>**: Packages the code for upload.
- **<FILE>run.sh</FILE>**: Runs <FILE>setup.sh</FILE> and then runs the module from <FILE>main.py</FILE>.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the Push method.**

Open <FILE>hello-world-game/src/models/game_logic.py</FILE>.
This is the template for the Button API that you will add the game logic.

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
**Configure your module as a local module.**

Before uploading your module, you can run it locally on your machine to test it.

Navigate to your machine's **CONFIGURE** page.
Make sure your machine's is showing as live and connected to Viam.

Click the **+** button, select **Local module**, then again select **Local module**.

{{< tabs >}}
{{% tab name="Python" %}}

Enter the path to the <file>run.sh</file> file, for example, `/home/naomi/hello-world-game-py/run.sh` on Linux or `/Users/naomi/hello-world-game-py/run.sh`.
Click **Create**.

Save your config.
{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure your button as a local component.**

{{< tabs >}}
{{% tab name="Python" %}}

Click **+**, click **Local module**, then click **Local component** and fill in the fields as follows:

- model namespace triplet: `<namespace>:hello-world-game-py:game-logic`
- type: `button`
- name: `button-1`

Configure the camera and vision service names by pasting the following in the attributes field:

```json {class="line-numbers linkable-line-numbers"}
{
  "camera_name": "webcam",
  "detector_name": "object-detector"
}
```

Save the config.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Test your game logic.**

Click the **TEST** section of the button's configuration card.

Click the button to start a game.

Check the **LOGS** tab, you'll see the prompt logged there and can follow the logs to see if an object is identified or not.
To see more visual input, use the **TEST** section of the vision service as you hold objects up to the camera.

If you are encountering errors, check the **LOGS** tab for more information.

If you want to test the `DoCommand` method, open the **CONTROL** tab and click on the `DoCommand` panel.
Send `{ "action": "get_data" }` to retrieve the score, the time the round started, and the current item to detect.

{{% /tablestep %}}
{{< /table >}}

## Playing the game

As you've undoubtedly noticed, the game UI isn't ideal.
To address that, we've created a small web application which is hosted as a Viam application.

You can use this application to connect to your machine and play the game.

[Take me to play the game](TODO).

This tutorial does not cover creating the Viam application but you can check out its code [on GitHub](TODO) and read up on [Viam applications](/operate/control/viam-applications/).

TODO preview

## Notes

{{< alert title="Want to train your own model instead?" color="note" >}}
If you wish to train your own ML model, see [Train a TF or TFLite model](/data-ai/train/train-tf-tflite/).
{{< /alert >}}

Here's how these concepts work together in practice for this tutorial:

- **Your machine**, that is your laptop or desktop computer, runs the Viam software
- A **component**, a webcam, provides access to a camera stream.
- A **service** runs a publicly-available machine learning model, and another service uses the running model and the camera stream to detect objects.
- **Modules** are the plugins that provide the two services.
  You will also create a module for the game logic.

1. From there, you have many options including:

   - Capturing data from your machines
   - Training and deploying an AI model
   - Using an SDK of your choice to write an app to interact with your machines
   - Deploying control logic
   - Sharing the configuration across many machines
