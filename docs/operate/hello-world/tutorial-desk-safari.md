---
linkTitle: "Tutorial: Desk Safari"
title: "Tutorial: Desk Safari"
weight: 20
layout: "docs"
type: "docs"
videos: ["/build/game-preview.webm", "/build/game-preview.mp4"]
videoAlt: "Desk Safari game preview"
images: ["/build/game-preview.gif"]
imageAlt: "Desk Safari game preview"
level: "Beginner"
languages: ["python"]
viamresources: ["camera", "vision", "button"]
cost: "0"
date: "2025-09-24"
no_list: false
description: "Follow this tutorial to learn about Viam while building a game."
authors: ["Naomi Pentrel"]
---

This tutorial assumes no prior knowledge of Viam and will teach you the fundamentals that allow you to build any machine that interacts with the physical world:

- [Device setup](#device-setup) will walk you through installing Viam on your computer.
- [Use a webcam](#use-a-webcam) will guide you through configuring and testing camera resources in Viam.
- [Add computer vision](#add-computer-vision) will show you how to integrate higher-level services such as ML model and vision services.
- [Program your game](#program-your-game) will teach you to build custom modules and implement the game control logic.
- [Play the game](#play-the-game) will let you test and interact with your completed game.

## Game overview

The Desk Safari game you will build works as follows:

1. **Game Start**: The player presses a button to begin
2. **Round Duration**: Each round lasts up to 60 seconds
3. **Item Detection**: The player must show a prompted item to the camera
4. **Scoring**: If the item is detected with ≥50% confidence, the player scores a point and gets a new item
5. **Game End**: If no item is detected within 60 seconds, the round ends
6. **Restart**: The player can press the button again to start a new game

{{<video webm_src="/build/game.webm" mp4_src="/build/game.mp4" poster="/build/game.jpg" alt="A game of Desk Safari where the player holds up different items to the camera to score points">}}

## Prerequisites

- A laptop or desktop computer with a webcam (USB, built-in, or wireless)
- Python 3.8+ installed on your computer
- Basic familiarity with Python programming
- Basic familiarity with command line/terminal usage

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
You can create more organizations and locations to organize your machines, but for this tutorial you can use the automatically created ones.

{{% /tablestep %}}
{{% tablestep %}}
**Create a new machine.**

Click **+ Add machine** to create your first machine and name it `hello-world`.

A {{< glossary_tooltip term_id="machine" text="machine" >}} represents at least one computer running `viam-server` along with all the hardware components and software services that the computer controls.

{{% /tablestep %}}
{{% tablestep %}}
**Install `viam-server`.**

On the machine's page, follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} to install `viam-server` on the computer you're using for your project.

Wait until your machine has successfully connected to Viam.

{{<imgproc src="/tutorials/hello-world/connected.png" resize="800x" style="width: 500px" declaredimensions=true alt="A machine showing a successful connection." class="imgzoom shadow">}}

{{% /tablestep %}}
{{< /table >}}

By installing `viam-server` on your device, you've turned your computer into a Viam {{< glossary_tooltip term_id="machine" text="machine" >}}.

At this point, your machine only runs the Viam software.
To make your machine do something interesting, you must add functionality to it.

When you use Viam to build a machine, you mix and match different building blocks to make the machine do exactly what you need.
The building blocks you'll use in this tutorial are **components**, **services**, and **modules**.
These are the main building blocks that make up all machines.

Let's start by adding a component.

## Use a webcam

{{< glossary_tooltip term_id="component" text="Components" >}} are the resources that your machine uses to sense and interact with the world, such as cameras, motors, sensors, and more.

For this tutorial, you can use any webcam that is connected to your computer: a USB webcam, a built-in one, or a wireless one.

{{< table >}}
{{% tablestep start=1 %}}
**Navigate to the CONFIGURE tab of your machine's page.**

This page is where you configure all hardware and software for a machine.
There are different kinds of {{< glossary_tooltip term_id="resource" text="resources" >}} you can use.

{{% /tablestep %}}

{{% tablestep %}}
**Configure the webcam to use for the Desk Safari game.**

Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `camera` type, then select the `webcam` model.
Enter the name `webcam` for your camera and click **Create**.

{{% /tablestep %}}
{{% tablestep %}}
**Save your config.**

Always save your config before testing.
This will apply your changes to your machine.

{{% /tablestep %}}
{{% tablestep %}}
**Test the camera stream.**

Click on the camera's **TEST** panel to see the camera stream.

The **TEST** panel is a good tool to ensure {{< glossary_tooltip term_id="resource" text="resources" >}} are working as expected.

{{< imgproc src="/components/camera/example_camera_2.png" alt="Example Camera view" resize="800x" style="width:500px" class="imgzoom shadow" >}}

If your camera is not working, see [Troubleshooting](/operate/reference/components/camera/webcam/#troubleshooting) and [Common errors](/operate/reference/components/camera/webcam/#common-errors).

{{% /tablestep %}}
{{< /table >}}

You can now see your camera stream on Viam.
Next, you’ll apply computer vision to this stream.

## Add computer vision

{{< glossary_tooltip term_id="service" text="Services" >}} are higher-level software capabilities that process and interpret data or interact with the world.
Viam provides many different services, including ones to run machine learning models and computer vision.

For this tutorial, you will use:

- a model called `EfficientDet-COCO`, which is publicly available. The model can detect a variety of objects. You can see all objects in the <file>[labels.txt](/tutorials/labels.txt)</file> file.
- an ML model service, which runs a machine learning model on your machine and returns inferences.
- a vision service, which uses the machine learning model, applies it to the camera stream, and returns any objects it identifies.

Let's configure all these:

{{< table >}}
{{% tablestep start=1 %}}
**Add multiple resources in one step.**

On the **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Insert fragment**.
Select the `HelloWorldMLResources` fragment by the `Robot Land` organization.
Click **Insert fragment**.
This adds a vision service named `object-detector` and a model for it.
Save your config.

{{% /tablestep %}}
{{% tablestep %}}
**Investigate the new resources.**

A {{< glossary_tooltip term_id="fragment" text="fragment" >}} constitutes a set of {{< glossary_tooltip term_id="resource" text="resources" >}} which are often used together.
In this case, the fragment contains the module that contains the ML model service which runs the model, as well as a vision service that applies the model to the camera stream.

Review the config for each new resource and click on their **TEST** panels to try them.

{{% /tablestep %}}
{{< /table >}}

If you check the resources added by the fragment, you'll see an additional resource called `tflite_cpu`.
This is a {{< glossary_tooltip term_id="module" text="module" >}}.
Modules are packages of code that contain components and services.
They're like plugins that expand what your machine can do without modifying Viam's core software.

Viam has a registry of modules that contain resources you can use when building your machines.
Of course, you can also build your own modules and resources.
In fact, you will create a resource for the game's control logic in the next step.

## Program your game

The game loop works as follows:

- The player presses a button to start the game.
- The game provides the player with a prompt showing an item to find and hold up to the camera within 60 seconds.
- If the vision service detects a matching object within 60 seconds, the player scores a point and a new round begins with a new item.
- If no matching object is detected within 60 seconds, the current round ends and the game stops.
- The player can press the button again to start a new game with a fresh score.

Now that you have the camera and vision service working, you need to create the game logic that ties them together.
This logic will implement the game mechanics.

To implement the logic, you'll create your own {{< glossary_tooltip term_id="resource" text="resource" >}} and package it inside a {{< glossary_tooltip term_id="module" text="module" >}}.

Viam provides a range of standardized component and service APIs.
When you create a resource, you implement the API among them that most closely fits your needs.

The Button API fits perfectly for the game as it provides the methods `Push` and `DoCommand`.

The `Push` method works great for starting the game. If you think about it, when a player starts the game, they're essentially pushing a button to issue the start command.

`DoCommand` is often used to implement control logic, as you can pass commands as arbitrary JSON objects, such as `{"action": "run_game_loop"}`.
You can use the `DoCommand` method to implement everything that doesn't fit into other API methods.

In the next steps, you'll create your own module which implements the game logic using the Button API.

To create your game logic module, you'll use the Viam CLI to generate code that already includes the Button API template.
This saves you from writing boilerplate code.

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

Replace `<ORGANIZATION-ID>` with your organization ID, which resembles: `a12b3c4d-1234-123a-12a3-a1b23c45d67e`.

{{< tabs >}}
{{% tab name="Python" %}}

```sh {class="command-line" data-prompt="$" data-output="4-10"}
viam module generate --language python --model-name game-logic \
  --name hello-world-game-py --public-namespace <ORGANIZATION-ID> \
  --resource-subtype=button
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Inspect the generated files.**

{{< tabs >}}
{{% tab name="Python" %}}

The module generator creates the following files:

```treeview
hello-world-game-py/
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

The CLI generated several files, but you'll only need to modify <FILE>game_logic.py</FILE> to implement your game.
If you want to understand the module structure, here's what each file does:

- **<FILE>README.md</FILE>**: Documentation template that gets uploaded to the registry when you upload the module.
- **<FILE>meta.json</FILE>**: Module metadata that gets uploaded to the registry when you upload the module.
- **<FILE>main.py</FILE>** and **<FILE>game_logic.py</FILE>**: Core code that registers the module and resource and provides the model implementation.
- **<FILE>setup.sh</FILE>** and **<FILE>requirements.txt</FILE>**: Setup script that creates a virtual environment and installs the dependencies listed in <FILE>requirements.txt</FILE>.
- **<FILE>build.sh</FILE>**: Build script that packages the code for upload.
- **<FILE>run.sh</FILE>**: Script that runs <FILE>setup.sh</FILE> and then executes the module from <FILE>main.py</FILE>.

{{< alert title="Full code" color="tip" >}}

The following steps walk through each step to change the code.
You can also reference the full code [on GitHub](https://github.com/viam-labs/hello-world-game-module).

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Setup the imports for the game.**

Open <FILE>hello-world-game-py/src/models/game_logic.py</FILE>.
This is the template for the Button API to which you will add the game logic.

To implement the game mechanics, you'll need these Python packages:

```python {class="line-numbers linkable-line-numbers" }
import random
from datetime import datetime, timedelta

from typing import cast
from viam.services.vision import *
```

The packages allow you to:

- pick a random item
- implement the time logic for the game
- use the vision package

{{% /tablestep %}}
{{% tablestep %}}
**Add class attributes for the game.**

Class attributes are variables that belong to the class itself rather than to any specific instance of the class.
They are shared among all instances of the class and are defined at the class level.

For the Desk Safari game, you need to provide the game with a list of items to choose from for the prompt.
This list should not change between instances, so it can be defined as a class variable.
You can remove any items you don't have in your home from the list.

```python {class="line-numbers linkable-line-numbers" data-start="20" data-line="8-20" }
class GameLogic(Button, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug
    # option, or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("<namespace>", "hello-world-game-py"), "game-logic"
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

{{% /tablestep %}}
{{% tablestep %}}
**Validate the button's config.**

Your game needs to know which camera and vision service to use.
While you could hardcode these names, you'll get them from the button's configuration. This makes your game flexible if you change component names later.

To get parameters from the configuration object, you use the `validate_config` method.
`viam-server` calls the `validate_config` method before calling `reconfigure` to:

1. Ensure the expected fields are in the config and have the right type.
   This method makes sure the camera name and vision service name are present and raises errors if they are not provided.
2. Find out if the resource has required dependencies (`req_deps`).
   The `validate_config` method returns a list of required dependencies and a list of optional dependencies.
   If the resource requires other components or services to function, as in this case the camera and the vision service, you must return them as the first array from the method.

   `viam-server` waits until those dependencies are available before starting the button component.

```python {class="line-numbers linkable-line-numbers" data-start="55" }
    @classmethod
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

{{% /tablestep %}}
{{% tablestep %}}
**Implement the Push method.**

{{< tabs >}}
{{% tab name="Python" %}}

In the <FILE>hello-world-game-py/src/models/game_logic.py</FILE> file, find the `push` method to set the `new_game` attribute to `True` when pushed.

```python {class="line-numbers linkable-line-numbers" data-line="8-9" data-start="90" }
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

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}{{% tablestep %}}
**Initialize all variables.**

Unlike class attributes, instance attributes are unique to a single instance of the button running on your machine.
You use them to initialize instance parameters, like `self.new_game`, in the `reconfigure` method.
`viam-server` calls the `reconfigure` method whenever the module starts or a configuration change occurs.
Whenever you change the config of the button, the parameters get set to the values assigned in the reconfigure method.

You must initialize all variables that can and may be accessed before they are assigned elsewhere in the code.
For the Desk Safari game, you'll initialize the following game state variables:

- `new_game`: the value set to true when a new game should start
- `score`: the score
- `time_round_start`: the time the round started, used to determine when 60 seconds are up
- `item_to_detect`: the current item that needs to be shown to the camera.

On top of game state variables, you also need to initialize the vision service and camera name so they can be used in the rest of the code.
The dependencies parameter contains all the resources this component can access.
By using `cast` you tell Python that the vision resource is specifically a VisionClient.

Update the `reconfigure` method to initialize all the variables:

```python {class="line-numbers linkable-line-numbers" data-start="79" }
    def reconfigure(
        self, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ):
        # Game state
        self.new_game: bool = False
        self.score: int = 0
        self.time_round_start: Optional[datetime] = None
        self.item_to_detect: str = ""

        camera_name = config.attributes.fields["camera_name"].string_value
        detector_name = config.attributes.fields["detector_name"].string_value

        # Get the full resource name for the vision service
        # (rdk:service:vision/object-detector)
        vision_resource_name = VisionClient.get_resource_name(detector_name)

        # Check if the vision resource exists in dependencies
        if vision_resource_name not in dependencies:
            raise KeyError(f"Vision service '{detector_name}' not found in "
                           f"dependencies. Available resources: "
                           f"{list(dependencies.keys())}")

        vision_resource = dependencies[vision_resource_name]
        self.detector = cast(VisionClient, vision_resource)
        self.camera_name = camera_name

        return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{% tablestep %}}
**Implement the game loop with the DoCommand method.**

{{< tabs >}}
{{% tab name="Python" %}}

The last change to the code is to implement the game loop.
Change the implementation of the `do_command` method to run the game loop when receiving the command parameters `{"action": "run_game_loop"}`
To make it easy to retrieve the game data (for later parts of the tutorial), the following code will return the data for any call to `do_command`:

```python {class="line-numbers linkable-line-numbers" data-line="8-17" data-start="117" }
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {}
        for name, args in command.items():
            if name == "action" and args == "run_game_loop":
                await self._run_game_loop()
        # return the current game data for all commands
        result["score"] = self.score
        result["time_round_start"] = str(self.time_round_start)
        result["item_to_detect"] = self.item_to_detect
        self.logger.info(f"Game data: {result}")
        return result
```

The `do_command` method calls another method `_run_game_loop` which implements the game logic.
Add the `_run_game_loop` method and the other helper methods above the `do_command` method:

```python {class="line-numbers linkable-line-numbers" data-start="117" }
    async def _run_game_loop(self):
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
        """Initialize a new game round."""
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

        # start a new round
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

{{% /tablestep %}}

{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure your module as a local module.**

The next step is to run the logic on your machine.
For production purposes you would upload the module to the registry but for now, let's just test your module by running it locally on your machine.

Navigate to your machine's **CONFIGURE** page.
Make sure your machine is showing as live and connected to Viam.

Click the **+** button, select **Local module**, then select **Local module** again.

{{< tabs >}}
{{% tab name="Python" %}}

Enter the path to the <file>run.sh</file> file, for example, `/home/naomi/hello-world-game-py/run.sh` on Linux or `/Users/naomi/hello-world-game-py/run.sh` on macOS.
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

- model namespace triplet: `<namespace>:hello-world-game-py:game-logic`, you can see the full triplet in the module's <FILE>meta.json</FILE> file
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

Navigate to your machine's **CONTROL** tab and find the button's panel.

1. Click the **PUSH** button to start the game.
   You should see a log message saying "`push` is called" in the **LOGS** tab.
2. Open the `DoCommand` panel, add `{ "action": "run_game_loop" }` as the input and click **Execute**.
   This will call the game loop once and retrieve the score, the time the round started, and the current item to detect.
   You will see a response in the UI of the format:

   ```json
   {
     "score": 0,
     "time_round_start": "2025-09-24 14:07:49.599761",
     "item_to_detect": "Bowl"
   }
   ```

3. Hold up the `item_to_detect` and click the **Execute** button to test the game.
   Once successfully detected, the score increases and the `item_to_detect` changes.

4. If you wait 60 seconds, the game ends and the response you get if you then click **Execute** contains the default values for `item_to_detect` and `time_round_start` and the last score:

   ```json
   {
     "item_to_detect": "",
     "score": 1,
     "time_round_start": "None"
   }
   ```

This manual testing lets you verify the game logic works correctly.
In the final step, you'll make the game logic run continuously.

If you are encountering errors, check the **LOGS** tab for more information.

{{% /tablestep %}}
{{% tablestep %}}
**Run game logic loop automatically with a job.**

To run game logic, we'll use a {{< glossary_tooltip term_id="job" text="job" >}} which calls the `DoCommand` method periodically.

Click the **+** icon next to your machine part in the left-hand menu and select **Job**.
You can use the default name, `job-1`, and click **Create**.

In the job panel, set the **Schedule** to **Cron** and enter `* * * * * *` which will run the job every second.

Then configure the job:

- **Resource**: `button-1`
- **Method**: `DoCommand`
- **Command**: `{ "action": "run_game_loop" }`

Click save.

Now, check the **LOGS** tab; you'll see the job triggered every second.
If you now open another tab and go back to the **CONTROL** tab and click the **PUSH** button and then look at the logs in the other tab, you'll see periodic output from the running game.
To see more visual input, scroll to the vision service panel on the **CONTROL** tab which will show you current detections as you hold objects up to the camera.

{{% /tablestep %}}
{{< /table >}}

## Play the game

As you've undoubtedly noticed the Viam UI is meant for testing, not for playing games.
To give the game a better UI, we've created a small web application which is hosted as a Viam application.

You can use this application to connect to your machine and play the game.
Your machine must be online and configured before opening the app.

[Take me to play the game](https://hello-world-game-web-app_naomi.viamapplications.com/).

This tutorial does not cover creating the Viam application but you can check out the code [on GitHub](https://github.com/viam-labs/hello-world-game-module/tree/main/hello-world-game-web-app) and read up on [Viam applications](/operate/control/viam-applications/).

## Conclusion

Let's recap how the concepts you've learned in this tutorial work together in practice for the Desk Safari game:

- **Your machine** (your laptop or desktop computer) runs the Viam software
- A **component**, a webcam, provides access to a camera stream.
- The publicly-available machine learning model that can identify items is run by a **service**.
- Your machine has a **module** installed that provides the vision **service** which applies the machine learning model to the camera stream.
- You've created a **module** containing a button **component** which starts and runs the control logic for the game.

## Next steps

You now know how to build a machine using {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, and {{< glossary_tooltip term_id="module" text="modules" >}}.
You can use these tools to **build any kind of machine** with Viam.

If you want to continue working on your game, consider:

- Building your own [Viam application, mobile app, or headless app.](/operate/control/viam-applications/)
- Taking photos when an item is successfully detected by [capturing data from your machines](/data-ai/capture-data/capture-sync/)
- [Training your own TF or TFLite model](/data-ai/train/train-tf-tflite/) to recognize more or other items

## Troubleshooting

### Camera not working

- Check that your webcam is properly connected
- Ensure no other applications are using the camera
- Try restarting `viam-server`
- See [Camera troubleshooting guide](/operate/reference/components/camera/webcam/#troubleshooting)

### Module not loading

- Verify the path to `run.sh` is correct
- Review the **LOGS** tab for error messages

### Game not detecting items

- Ensure good lighting conditions
- Hold items clearly in front of the camera
- Reduce the **Minimum confidence threshold** in the vision service's attributes and use the vision service's **TEST** panel to check if it would detect the item at a lower confidence threshold.
  If so, keep the lower value and update your value to also use the lower threshold instead of `0.5`.
- If you cannot get the item to be recognized, the model may not work well enough.
  Remove it from the `POSSIBLE_OPTIONS` or [train your own model](/data-ai/train/train-tf-tflite/).

### Job or game logic not running

- Confirm the cron schedule is set correctly (`* * * * * *`)
- Check that the resource name matches exactly (`button-1`)
- Verify the command format: `{ "action": "run_game_loop" }`
