---
linkTitle: "Deploy control logic"
title: "Deploy control logic to a machine"
weight: 50
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "Deploy machine control logic in a module."
languages: []
viamresources: []
platformarea: ["registry", "fleet"]
level: "Intermediate"
date: "2025-02-14"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
aliases:
  - "/manage/software/control-logic"
---

To run control logic on machines:

1. [Create a module](#create-a-module-for-your-control-logic) for the control logic
2. [Package the control logic module](#package-the-control-logic)
3. [Deploy the module](#deploy-the-control-logic) to individual machines using `viam-server`
4. [Run control logic on the module automatically](#run-control-logic-automatically-with-jobs) with one or more {{< glossary_tooltip term_id="job" text="jobs" >}}

<br>

For microcontrollers, see [Micro-RDK modules](/operate/modules/other-hardware/micro-module/) and [Over-the-air firmware updates](/operate/install/setup-micro/#configure-over-the-air-updates) instead.

## Prerequisites

Start by [setting up one machine](/operate/install/setup/).
Then, [configure any hardware and software resources](/operate/modules/supported-hardware/) that you will use with your machine and that you want to drive with your control logic.

## Create a module for your control logic

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate --resource-subtype=generic-component
   ```

2. Follow the prompts, selecting the following options:

   - Module name: Your choice, for example `control-logic`
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

Open the file <FILE>src/models/control_logic.py</FILE> to add your control logic to.

The following example shows how you might implement a counter that starts counting when you send a `start` command and stops when it receives a `stop` command.

{{< table >}}
{{% tablestep start=1 %}}
**Setup instance parameters**

When your new model gets added to your machine, its `reconfigure()` method gets called.
You can use it to store any instance variables.

The following example code initializes two instance parameters `counter` and `running`.

```python
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        self.counter = 0
        self.running = False
        return super().reconfigure(config, dependencies)
```

The `reconfigure` method gets called whenever the control logic module starts or when configuration change occurs for the resource itself.

If this is a problem, consider writing state to a file on disk and add logic to handle subsequent calls to the reconfigure method gracefully.

{{% /tablestep %}}
{{% tablestep %}}
**Write the control logic**

To add the control logic, use the `DoCommand()` method.
The method accepts arbitrary JSON objects as commands.

The following code checks the command object and for `start` and `stop`, it sets the `running` parameter to `True` or `False`.
A third command, `on_loop`, results in the `on_loop()` method being called but only if `running` is `True`.

The `on_loop()` method increments the counter.

```python
    async def on_loop(self):
        try:
            self.logger.info("Executing control logic")
            self.counter += 1
            self.logger.info(f"Counter: {self.counter}")

        except Exception as err:
            self.logger.error(err)

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
                self.running = True
                result[name] = True
            if name == "action" and args == "stop":
                self.running = False
                result[name] = True
            if name == "action" and args == "on_loop":
                if self.running:
                    await self.on_loop()
                result[name] = True
        result["counter"] = self.counter
        return result
```

{{% /tablestep %}}
{{% tablestep %}}
**Use other machine resources**

To access other machine resources from your control logic you must modify the `validate_config` and the `reconfigure` method.
Let's assume you have a sensor, that ...

{{% /tablestep %}}
{{< /table >}}

{{% expand "Click to view the entire control logic code" %}}

This is the code for <FILE>src/models/control_logic.py</FILE>:

```python {class="line-numbers linkable-line-numbers" data-line="42-43,46-53,62-75"}
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, Tuple)

from typing_extensions import Self
from viam.components.generic import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes


class ControlLogic(Generic, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("<namespace>", "control-logic"), "control-logic"
    )

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        return super().new(config, dependencies)

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        return [], []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        self.counter = 0
        self.running = False
        return super().reconfigure(config, dependencies)

    async def on_loop(self):
        try:
            self.logger.info("Executing control logic")
            self.counter += 1
            self.logger.info(f"Counter: {self.counter}")

        except Exception as err:
            self.logger.error(err)

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
                self.running = True
                result[name] = True
            if name == "action" and args == "stop":
                self.running = False
                result[name] = True
            if name == "action" and args == "on_loop":
                if self.running:
                    await self.on_loop()
                result[name] = True
        result["counter"] = self.counter
        return result

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> Sequence[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()
```

{{% /expand%}}

For a complete tutorial, see [Tutorial: Desk Safari](/operate/hello-world/tutorial-desk-safari/).
For more examples, check the [Viam registry](https://app.viam.com/registry)

## Package the control logic

Once you have implemented your control logic, commit and push your changes to a GitHub repository.

Follow the steps in [Upload your module](/operate/modules/other-hardware/create-module/#upload-your-module) using cloud build.
When you create a release, your module will be built, packaged and pushed to the Viam Registry.

If you are not using GitHub or cloud build, see [Upload your module](/operate/modules/other-hardware/create-module/#upload-your-module) and [Update an existing module](/operate/modules/other-hardware/manage-modules/#update-automatically-from-a-github-repo-with-cloud-build) for more information on alternatives.

## Deploy the control logic

1. Navigate to the machine you want to deploy your control logic to.
1. Go to the **CONFIGURE** tab.
1. Click the **+** button.
1. Click **Component or service** and select your control logic component.
1. Click **Add module**.
1. Add a **Name** and click **Create**.
1. If you added configuration attributes, configure your control logic component.
1. Click **Save**.

Your control logic will now be added to your machine.

## Test your control logic

For testing purposes use the `DoCommand` method:

{{< tabs >}}
{{% tab name="Builder mode" %}}

On the **CONTROL** or the **CONFIGURE** tab, use the `DoCommand` panel:

1. Copy and paste one of the following command inputs:

   To set `self.running` to `True`, copy and paste the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "start"
   }
   ```

   To run the control logic loop `on_loop`, copy and paste the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "on_loop"
   }
   ```

   To set `self.running` to `False`, use the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "stop"
   }
   ```

2. Click **Execute** to call `DoCommand()` with the command input on your machine.

{{<imgproc src="/components/generic/generic-control.png" alt="The generic component in the test panel." resize="900x" style="width:500px" class="imgzoom shadow">}}<br>

{{% /tab %}}
{{% tab name="Python" %}}

You can start and stop your control logic with the `DoCommand()` method from the Python SDK:

```python
# Start your control logic
await control_logic.do_command({"action": "start"})

# Run your control loop
await control_logic.do_command({"action": "on_loop"})

# Stop your control logic
await control_logic.do_command({"action": "stop"})
```

{{% /tab %}}
{{< /tabs >}}

## Run control logic automatically with jobs

To run control logic, use a {{< glossary_tooltip term_id="job" text="job" >}} which calls the `DoCommand` method periodically.

{{< table >}}
{{% tablestep start=1 %}}
**Start control logic at specific time each day**

Click the **+** icon next to your machine part in the left-hand menu and select **Job**.
You can use the default name, `job-1`, and click **Create**.

In the job panel, set the **Schedule** to **Cron** and enter `0 0 8 * * *` which will run the job at 08:00 AM.

Then configure the job:

- **Resource**: `generic-1`
- **Method**: `DoCommand`
- **Command**: `{ "action": "start" }`

Click save.

{{% /tablestep %}}
{{% tablestep %}}
**Run control logic periodically**

Configure another job:

- **Cron Schedule**: `0 1 * * * *` (every minute)
- **Resource**: `generic-1`
- **Method**: `DoCommand`
- **Command**: `{ "action": "on_loop" }`

{{% /tablestep %}}
{{% tablestep %}}
**End control logic at specific time each day**

Configure another job:

- **Cron Schedule**: `0 0 17 * * *` (at 05:00 PM)
- **Resource**: `generic-1`
- **Method**: `DoCommand`
- **Command**: `{ "action": "stop" }`

{{% /tablestep %}}
{{< /table >}}

Now, check the **LOGS** tab; you'll see the second job triggered every minute, but the counter will only increase from 8 AM to 5 PM.
