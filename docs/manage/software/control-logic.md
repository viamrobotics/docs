---
linkTitle: "Deploy control logic"
title: "Deploy control logic to a machine"
weight: 30
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "Deploy control logic in a module to a machine."
languages: []
viamresources: []
platformarea: ["registry", "fleet"]
level: "Intermediate"
date: "2025-02-14"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

One method of operating your machine is by running control logic on another device, such as an app.
However, you can also run control logic directly on the machine itself using {{< glossary_tooltip term_id="module" text="modules" >}}.
These are the same modules that provide functionality like drivers and integrations to your machines.

The following steps show you how to create modules with control logic and how to deploy them to individual machines using `viam-server`.

For microcontrollers, see [Micro-RDK modules](/operate/get-started/other-hardware/micro-module/) and [Over-the-air firmware updates](/operate/get-started/other-hardware/micro-module/#over-the-air-updates) instead.

## Prerequisites

Start by [setting up one machine](/operate/get-started/setup/).
Then, [configure any hardware and software resources](/operate/get-started/supported-hardware/) that you will use with your machine and that you want to drive with your control logic.

## Generate stub files

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate --resource-subtype=generic-component
   ```

2. Follow the prompts, selecting the following options:

   - Module name: Your choice, for example `my-control-logic`
   - Language: Your choice
   - Visibility: `Private`
   - Namespace/Organization ID: In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page.
     Find the **Public namespace** and copy that string.
     In the example snippets below, the namespace is `naomi`.
   - Resource to be added to the module: `Generic Component`.

     For simplicity, this guide uses the generic component.
     You can choose a different resource type to add your control logic to.
     For example, for logic controlling a camera, you may wish to use the camera component.
     You must implement any required API methods for the chosen component.

   - Model name: Your choice, for example `control-logic`
   - Enable cloud build: Choose `Yes` if you are using GitHub or want to use cloud build.
   - Register module: `Yes`

3. Press the Enter key and the generator will create a folder for your control logic component.

## Add control logic to your module

When your new model gets added to your machine, its `reconfigure()` method gets called.
If you want your control logic to run in a loop in the background, you can start this loop here.
Be sure to also implement logic to handle subsequent calls to the reconfigure method gracefully.

For example, in Python, start your logic in the `reconfigure()` method of <FILE>src/main.py</FILE>:

```python {class="line-numbers linkable-line-numbers" data-line="20-28"}
# Add these imports
import asyncio
from threading import Event
from viam.logging import getLogger


LOGGER = getLogger("control-logic")


class ControlLogic(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("naomi", "my-control-logic"), "control-logic"
    )
    running = None
    task = None
    event = Event()

    # Other methods omitted for brevity

    def reconfigure(
        self, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ):
        # starts automatically
        if self.running is None:
            self.start()
        else:
            LOGGER.info("Already running control logic.")

    def start(self):
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.control_loop())
        self.event.clear()

    def stop(self):
        self.event.set()
        if self.task is not None:
            self.task.cancel()

    async def control_loop(self):
        while not self.event.is_set():
            await self.on_loop()
            await asyncio.sleep(0)

    async def on_loop(self):
        try:
            LOGGER.info("Executing control logic")
            # TODO: ADD CONTROL LOGIC

        except Exception as err:
            LOGGER.error(err)
        await asyncio.sleep(1)

    def __del__(self):
        self.stop()

    async def close(self):
        self.stop()

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for name, _args in command.items():
            if name == "start":
                self.start()
                result[name] = True
            if name == "stop":
                self.stop()
                result[name] = True
        return result


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
```

For complete examples that implement control logic, see:

- [`event-manager`](https://github.com/viam-modules/event-manager)
- [`refill-controller`](https://github.com/viam-devrel/refill-controller)
- [`re-id-object-tracking`](https://github.com/viam-modules/re-id-object-tracking)
- [`detection-dock`](https://github.com/viam-labs/detection-dock)

## Package your control logic

Once you have implemented your control logic, commit and push your changes to a GitHub repository.

If you are not using GitHub, see [Upload your module](/operate/get-started/other-hardware/#upload-your-module) and [Update an existing module](/operate/get-started/other-hardware/manage-modules/#update-automatically) for more information on alternatives.

Follow the steps in [Upload your module](/operate/get-started/other-hardware/#upload-your-module) using cloud build.

Then [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github) with a tag of the form `1.0.0`.
Your module will now be built, packaged and pushed to the Viam Registry.

## Deploy your control logic

1. In the [Viam app](https://app.viam.com), navigate to the machine you want to deploy your control logic to.
1. Go to the **CONFIGURE** tab.
1. Click the **+** button.
1. Click **Component** and select your control logic component.
1. Click **Add module**.
1. Add a **Name** and click **Create**.
1. If you added configuration attributes, configure your control logic component.
1. Click **Save**.

Your control logic will now be added to your machine.
