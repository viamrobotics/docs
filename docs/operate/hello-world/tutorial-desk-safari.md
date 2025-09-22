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

TODO: Show video of the game

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

In the <FILE>hello-world-game/src/models/game_logic.py</FILE> file, find the `Push` method to set the `start` attribute to `True` when pushed.

```python {class="line-numbers linkable-line-numbers" data-line="9" data-start="66" }
    async def push(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> None:
        self.logger.info("`push` is called")
        self.new_game = True
```

The attribute `self.new_game` needs to be initialized.
You can initialize instance parameters in the `reconfigure` method, that way they reset whenever you change the configuration of the button.

```python {class="line-numbers linkable-line-numbers" data-line="5" data-start="55" }
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        # Game state
        self.new_game: bool = False

        return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the DoCommand method.**

{{< tabs >}}
{{% tab name="Python" %}}

In the same file, change the implementation of the `do_command` method to return the game state when receiving the command parameters `{"action": "get_data" }`:

```python {class="line-numbers linkable-line-numbers" data-line="8-15" data-start="79" }
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {}
        for name, args in command.items():
            if name == "action" and args == "get_data":
                result["score"] = self.score
                result["time_round_start"] = str(self.time_round_start)
                result["item_to_detect"] = self.item_to_detect
                return result
        return {}
```

Add the other parameters to the `reconfigure` method:

```python {class="line-numbers linkable-line-numbers" data-line="6-8" data-start="55" }
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        # Game state
        self.new_game: bool = False
        self.score: int = 0
        self.time_round_start: Optional[datetime] = None
        self.item_to_detect: str = ""

        return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the game loop.**

You have implemented the methods that constitute the Button API.
Now you'll add the code that uses the vision service and camera to implement the game logic.

{{< tabs >}}
{{% tab name="Python" %}}

In the <FILE>hello-world-game/src/models/game_logic.py</FILE> file, add the following imports:

```python {class="line-numbers linkable-line-numbers" }
import asyncio
import random
from datetime import datetime, timedelta
from threading import Event

from typing import cast
from viam.components.camera import *
from viam.services.vision import *
```

Add class attributes for the labels that the model supports:

```python {class="line-numbers linkable-line-numbers" data-start="22" }
class GameLogic(Button, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("naomi", "hello-world-game-py"), "game-logic"
    )

    POSSIBLE_OPTIONS: ClassVar[List[str]] = [
        "Person", "Cat", "Dog", "Hat", "Backpack", "Umbrella", "Shoe",
        "Eye glasses", "Handbag", "Tie", "Suitcase", "Frisbee", "Sportsball",
        "Plate", "Cup", "Fork", "Knife", "Spoon", "Bowl", "Banana", "Apple",
        "Sandwich", "Orange", "Broccoli", "Carrot", "Pizza", "Donut", "Cake",
        "Chair", "Couch", "Potted plant", "Mirror", "Desk", "Door", "Tv",
        "Laptop", "Mouse", "Keyboard", "Cellphone", "Blender", "Book", "Clock",
        "Vase", "Scissors", "Teddy bear", "Hair drier", "Toothbrush",
        "Hair brush"
    ]
```

Next, update the `validate_config` method.
The button needs to have access to the camera and vision service, therefore, it will need to receive those in its configuration.
This method makes sure they are present and raises errors if they are not provided:

```python {class="line-numbers linkable-line-numbers" data-start="57" }
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        req_deps = []
        fields = config.attributes.fields
        if "camera_name" not in fields:
            raise Exception("missing required camera_name attribute")
        elif not fields["camera_name"].HasField("string_value"):
            raise Exception("camera_name must be a string")
        camera_name = fields["camera_name"].string_value
        if not camera_name:
            raise ValueError("camera_name cannot be empty")
        req_deps.append(camera_name)
        if "detector_name" not in fields:
            raise Exception("missing required detector_name attribute")
        elif not fields["detector_name"].HasField("string_value"):
            raise Exception("detector_name must be a string")
        detector_name = fields["detector_name"].string_value
        if not detector_name:
            raise ValueError("detector_name cannot be empty")
        req_deps.append(detector_name)
        return req_deps, []
```

Underneath the `reconfigure` method, add these helper methods.
They implement the event loop and run the game:

```python {class="line-numbers linkable-line-numbers" data-start="98" }
    def start(self):
        if self.task is None:
            loop = asyncio.get_event_loop()
            self.task = loop.create_task(self._game_loop())
            self.event.clear()
            self.logger.info("Game loop started.")

    def stop(self):
        self.event.set()
        if self.task is not None:
            self.task.cancel()
            self.task = None
        self.logger.info("Game loop stopped.")

    def __del__(self):
        self.stop()

    async def close(self):
        self.stop()

    async def _game_loop(self):
        try:
            while not self.event.is_set():
                await self._process_game_state()
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            self.logger.info("Game loop cancelled.")
        except Exception as e:
            self.logger.error(f"Game loop error: {e}")
        finally:
            self.task = None

    async def _process_game_state(self):
        try:
            if self.new_game:
                await self._start_new_game()
            if self._is_game_active():
                await self._check_for_detection()
            else:
                await self._handle_game_end()

        except Exception as err:
            self.logger.error(f"Game state processing error: {err}")

    async def _start_new_game(self):
        self.new_game = False
        self.logger.info("Game is starting.")
        self.time_round_start = datetime.now()
        self.logger.info(f"Round started at {self.time_round_start.strftime('%Y-%m-%d %H:%M:%S')}")

        self.score = 0
        self.item_to_detect = random.choice(self.POSSIBLE_OPTIONS)
        self.logger.info(f"Item to detect: {self.item_to_detect}")

    def _is_game_active(self) -> bool:
        if not self.time_round_start:
            return False

        # Check if the current round is still active (within 60 seconds).
        return datetime.now() - self.time_round_start <= timedelta(seconds=60)

    async def _check_for_detection(self):
        self.logger.info("Checking for item detection")

        detections = await self.detector.get_detections_from_camera(self.camera_name)

        if self._is_target_detected(detections):
            await self._handle_successful_detection()
        else:
            self.logger.info(f"Item not detected: {self.item_to_detect}")

    def _is_target_detected(self, detections) -> bool:
        for detection in detections:
            if (detection.class_name == self.item_to_detect and
                detection.confidence > 0.5):
                return True
        return False

    async def _handle_successful_detection(self):
        self.score += 1
        self.logger.info(f"Item detected: {self.item_to_detect}")
        self.logger.info(f"Score: {self.score}")

        await self._start_new_round()

    async def _start_new_round(self):
        self.time_round_start = datetime.now()
        self.logger.info(f"Starting new round at {self.time_round_start.strftime('%Y-%m-%d %H:%M:%S')}")
        self.item_to_detect = random.choice(self.POSSIBLE_OPTIONS)
        self.logger.info(f"Item to detect: {self.item_to_detect}")

    async def _handle_game_end(self):
        if self.time_round_start:  # Only log if there was an active game
            self.logger.info(f"Round over at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info(f"Final Score: {self.score}")
            self.time_round_start = None
            self.item_to_detect = ""
```

And as a last step for the game implementation, update the reconfigure method to initialize the required variables and start the game loop:

```python {class="line-numbers linkable-line-numbers" data-start="80" }
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        # Game state
        self.new_game: bool = False
        self.score: int = 0
        self.time_round_start: Optional[datetime] = None
        self.item_to_detect: str = ""

        # Runtime control
        self.running: Optional[bool] = None
        self.event: Event = Event()
        self.task: Optional[asyncio.Task] = None

        camera_name = config.attributes.fields["camera_name"].string_value
        detector_name = config.attributes.fields["detector_name"].string_value

        # Get the resource name for the vision service
        vision_resource_name = VisionClient.get_resource_name(detector_name)

        # Check if the vision resource exists in dependencies
        if vision_resource_name not in dependencies:
            raise KeyError(f"Vision service '{detector_name}' not found in dependencies. Available resources: {list(dependencies.keys())}")

        vision_resource = dependencies[vision_resource_name]
        self.detector = cast(VisionClient, vision_resource)
        self.camera_name = camera_name

        # Start the game loop if not already running
        if self.task is None:
            self.start()
        else:
            self.logger.info("Game loop already running.")

        return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{< /tabs >}}

That's the game logic.
The `reconfigure` method starts the game loop which then starts a new game, sets an item to detect and checks periodically if the item is detected.

{{% /tablestep %}}

{{% tablestep %}}
**Configure your module as a local module.**

The next step is to run the logic on your machine.
For production purposes you would upload the module to the registry but for now, let's just test your module by running it locally on your machine.

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

[Take me to play the game](https://hello-world-game-web-app_naomi.viamapplications.com/).

This tutorial does not cover creating the Viam application but you can check out its code [on GitHub](https://github.com/viam-labs/hello-world-game-module/tree/main/hello-world-game-web-app) and read up on [Viam applications](/operate/control/viam-applications/).

## Conclusion

Here's how the concepts you've learned in this tutorial work together in practice for the Desk Safari game:

- **Your machine**, that is your laptop or desktop computer, runs the Viam software
- A **component**, a webcam, provides access to a camera stream.
- The publicly-available machine learning model that can identify items is run by a **service**.
- Your machine has a **module** installed that provides the vision **service** which applies the machine learning model to the camera stream.
- You've create a **module** containing a button **component** which starts and runs the control logic for the game.

## Next steps

You now know how to build a machine using {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, and {{< glossary_tooltip term_id="module" text="modules" >}}.
You can use these tools to **build any kind of machine** with Viam.

If you want to learn more, have a look at:

- Building a Viam application, mobile app, or headless app.
- Capturing data from your machines
- [Training your own TF or TFLite model](/data-ai/train/train-tf-tflite/).
- Sharing configuration fragments across machines
