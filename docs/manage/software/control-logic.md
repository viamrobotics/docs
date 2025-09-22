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

One method of operating your machine is by [running client code, such as an app](/operate/control/headless-app/), on the machine itself or on another device.
However, to deploy code directly onto multiple machines, you can package and version the control logic as a {{< glossary_tooltip term_id="module" text="module" >}}.
These are the same modules that provide functionality like drivers and integrations to your machines.

The following steps show you how to create modules with control logic and how to deploy them to individual machines using `viam-server`.

For microcontrollers, see [Micro-RDK modules](/operate/modules/other-hardware/micro-module/) and [Over-the-air firmware updates](/operate/install/setup-micro/#configure-over-the-air-updates) instead.

## Prerequisites

Start by [setting up one machine](/operate/install/setup/).
Then, [configure any hardware and software resources](/operate/modules/supported-hardware/) that you will use with your machine and that you want to drive with your control logic.

## Generate stub files

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate --resource-subtype=generic-component
   ```

2. Follow the prompts, selecting the following options:

   - Module name: Your choice, for example `my-control-logic`
   - Language: Your choice
   - Visibility: `Private`
   - Namespace/Organization ID: Navigate to your organization settings through the menu in upper right corner of the page.
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

For example, in Python, start your logic in the `reconfigure()` method of <FILE>src/models/control_logic.py</FILE>:

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
        await asyncio.sleep(10)

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
        for name, args in command.items():
            if name == "action" and args == "start":
                self.start()
                result[name] = True
            if name == "action" and args == "stop":
                self.stop()
                result[name] = True
        return result


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
```

For complete examples that implement control logic, see:

- [`event-manager`](https://app.viam.com/module/viam/event-manager)
- [`refill-controller`](https://app.viam.com/module/viam-demo/refill-controller)
- [`re-id-object-tracking`](https://app.viam.com/module/viam/re-id-object-tracking)
- [`detection-dock`](https://app.viam.com/module/viam-labs/detection-dock)

## Package your control logic

Once you have implemented your control logic, commit and push your changes to a GitHub repository.

Follow the steps in [Upload your module](/operate/modules/other-hardware/create-module/#upload-your-module) using cloud build.
When you create a release, your module will be built, packaged and pushed to the Viam Registry.

If you are not using GitHub or cloud build, see [Upload your module](/operate/modules/other-hardware/create-module/#upload-your-module) and [Update an existing module](/operate/modules/other-hardware/manage-modules/#update-automatically-from-a-github-repo-with-cloud-build) for more information on alternatives.

## Deploy your control logic

1. Navigate to the machine you want to deploy your control logic to.
1. Go to the **CONFIGURE** tab.
1. Click the **+** button.
1. Click **Component or service** and select your control logic component.
1. Click **Add module**.
1. Add a **Name** and click **Create**.
1. If you added configuration attributes, configure your control logic component.
1. Click **Save**.

Your control logic will now be added to your machine.

## Start and stop your control logic with Viam SDKs

You can start and stop your control logic with the Viam SDKs by calling `DoCommand()`.

For example, in Python, you can start and stop your control logic with the following code:

```python
# Start your control logic
await control_logic.do_command({"action": "start"})

# Stop your control logic
await control_logic.do_command({"action": "stop"})
```

## Start and stop your control logic from the web UI

You can start and stop your control logic from your machine's **CONTROL** tab:

{{<imgproc src="/components/generic/generic-control.png" alt="The generic component in the test panel." resize="900x" style="width:500px" class="imgzoom shadow">}}<br>

1. To start your control logic, copy and paste the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "start"
   }
   ```

   To stop your control logic, use the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "stop"
   }
   ```

2. Click **Execute** to call `DoCommand()` on your machine.
