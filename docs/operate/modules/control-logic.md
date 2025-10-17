---
linkTitle: "Run control logic"
title: "Run control logic on a machine"
weight: 38
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "Deploy and run machine control logic in a module."
languages: []
viamresources: []
platformarea: ["registry", "fleet"]
level: "Intermediate"
date: "2025-02-14"
updated: "2025-09-29" # When the tutorial was last entirely checked
cost: "0"
aliases:
  - "/manage/software/control-logic"
---

To write control logic for a machine, you must wrap it in a module.
This guide shows you how to write a module with control logic for a machine:

1. [Create a module](#create-a-module-with-a-generic-component-template) with a template for the control logic
1. [Program the control logic](#program-control-logic-in-module) using the `DoCommand` method
1. [Use other components or services](#use-other-components-or-services) in the control logic
1. [Test the control logic](#test-the-control-logic) locally
1. [Run control logic on the module automatically](#run-control-logic-automatically-with-jobs) with one or more {{< glossary_tooltip term_id="job" text="jobs" >}}

<br>

For microcontrollers, see [Micro-RDK modules](/operate/modules/advanced/micro-module/) and [Over-the-air firmware updates](/operate/install/setup-micro/#configure-over-the-air-updates) instead.

## Prerequisites

You must have one machine [running `viam-server`](/operate/install/setup/).

If your control logic depends on any hardware or software resources to function, you must [configure those hardware and software resources](/operate/modules/configure-modules/).

## Create a module with a generic component template

Install the Viam CLI.
You will use the CLI to generate the template you will use to write your control logic:

{{< alert title="For testing: run on machine" color="note" >}}
If you wish to test your control logic locally, follow these instructions on the computer on which you are running `viam-server`.
{{< /alert >}}

1. **Install the CLI.**

   You must have the Viam CLI installed to generate and upload modules:

   {{< readfile "/static/include/how-to/install-cli.md" >}}

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate --resource-subtype=generic-component
   ```

1. Follow the prompts, selecting the following options:

   - Module name: Your choice, for example `control-logic`
   - Language: Your choice
   - Visibility: `Private`
   - Namespace/Organization ID: Navigate to your organization settings through the menu in upper right corner of the page.
     Find the **Public namespace** and copy that string.
     In the example snippets below, the namespace is `naomi`.
   - Resource to be added to the module: `Generic Component`.

     You can use **any resource type**.
     The choice of resource type affects the API methods that you must implement.
     You can choose any [component API](/dev/reference/apis/#component-apis) or [service API](/dev/reference/apis/#service-apis).

     If you plan to use the control logic mostly on one component or service, choose the same component or service and implement the control logic in the available API methods for that resource.
     If no resource API fits, use the `Generic` type and implement the logic in the `DoCommand` method.
     All resource APIs contain the generic `DoCommand` method to implement any functionality that does not fit into other API methods.
     `DoCommand` is often used to implement control logic, as you can pass commands as arbitrary JSON objects, such as {"action": "start"}.

     For simplicity, this guide uses the generic component which only supports the `DoCommand` method.

   - Model name: Your choice, for example `control-logic`
   - Enable cloud build: Choose `Yes` if you are using GitHub or want to use cloud build.
   - Register module: `Yes`

1. Press the Enter key and the generator will create a folder for your control logic component.

## Program control logic in module

Open the file <FILE>src/models/control_logic.py</FILE> to add your control logic to it.

The following example shows how you might implement a counter that starts counting when you send a `start` command and stops when it receives a `stop` command.

{{< table >}}
{{% tablestep start=1 %}}
**Set up instance parameters**

When your new model gets added to your machine, its `reconfigure()` method gets called.
You can use it to store any instance variables.

The following example code initializes two instance parameters `counter` and `running`.

```python
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        self.counter = 0
        self.running = False
        return super().reconfigure(config, dependencies)
```

The `reconfigure` method gets called whenever the control logic module starts or when a configuration change occurs for the resource itself.

If this is a problem, consider writing state to a file on disk and adding logic to handle subsequent calls to the reconfigure method gracefully.

{{% /tablestep %}}
{{% tablestep %}}
**Write the control logic**

To add the control logic, use the `DoCommand()` method.
The method accepts arbitrary JSON objects as commands.

The following code checks the command object and for the `start` command it sets the `running` parameter to `True` and for the `stop` command to `False`.
A third command, `run_control_logic`, results in the `_on_loop()` method being called, but only if `running` is `True`.

The `_on_loop()` method increments the counter.

```python
    async def _on_loop(self):
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
            if name == "action" and args == "run_control_logic":
                if self.running:
                    await self._on_loop()
                result[name] = True
        result["counter"] = self.counter
        return result
```

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

    async def _on_loop(self):
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
            if name == "action" and args == "run_control_logic":
                if self.running:
                    await self._on_loop()
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

## Use other components or services

Any resources that you wish to access from your control logic need to be identified and instantiated.
To keep your code loosely coupled, we recommend passing the resource names in the configuration attributes of the control logic.
We must modify the `validate_config` method to ensure all required values are passed in correctly and then instantiate the resource in the `reconfigure` method.

Let's assume you have a board, and you'd like to pull a pin high when the `start` command is received and low when the `stop` command is received.

{{< table >}}
{{% tablestep start=1 %}}
**Pass resources in configuration.**

The `validate_config` method serves two purposes:

- To ensure the expected fields are in the config.
  The `validate_config` method is called whenever the module is started or a configuration change occurs.
- To return a list of the names of all the required dependencies.
  `viam-server` waits until all returned dependencies are available before starting this component.

```python
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        req_deps = []
        fields = config.attributes.fields
        if "board_name" not in fields:
            raise Exception("missing required board_name attribute")
        elif not fields["board_name"].HasField("string_value"):
            raise Exception("board_name must be a string")
        board_name = fields["board_name"].string_value
        if not board_name:
            raise ValueError("board_name cannot be empty")
        req_deps.append(board_name)
        return req_deps, []
```

{{% /tablestep %}}
{{% tablestep %}}
**Access the resources.**

`viam-server` passes the required dependencies when the control logic resource is reconfiguring.
From these dependencies you can get the board and store it in an instance variable.

```python
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        self.board_name = config.attributes.fields["board_name"].string_value
        board_resource_name = Board.get_resource_name(self.board_name)
        board_resource = dependencies[board_resource_name]
        self.board = cast(Board, board_resource)
        self.counter = 0
        self.running = False
        return super().reconfigure(config, dependencies)
```

Add the following imports at the top of <FILE>src/models/control_logic.py</FILE>:

```python
from typing import cast
from viam.components.board import Board
```

{{% /tablestep %}}
{{% tablestep %}}
**Use the resources.**

Update your logic in the `do_command` method to use the board:

```python {class="line-numbers linkable-line-numbers" data-line="12-13,17-18"}
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
                pin = await self.board.gpio_pin_by_name(name="13")
                await pin.set(high=True)
                result[name] = True
            if name == "action" and args == "stop":
                self.running = False
                pin = await self.board.gpio_pin_by_name(name="13")
                await pin.set(high=False)
                result[name] = True
            if name == "action" and args == "run_control_logic":
                if self.running:
                    await self._on_loop()
                result[name] = True
        result["counter"] = self.counter
        return result
```

{{% /tablestep %}}
{{< /table >}}

{{% expand "Click to view the entire control logic code" %}}

This is the code for <FILE>src/models/control_logic.py</FILE>:

```python {class="line-numbers linkable-line-numbers" data-line="42-43,46-53,62-75"}
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, Tuple, cast)

from typing_extensions import Self
from viam.components.generic import *
from viam.components.board import Board
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
        ModelFamily("naomi", "test-control-logic"), "control-logic"
    )

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Generic component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both required and optional)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        req_deps = []
        fields = config.attributes.fields
        if "board_name" not in fields:
            raise Exception("missing required board_name attribute")
        elif not fields["board_name"].HasField("string_value"):
            raise Exception("board_name must be a string")
        board_name = fields["board_name"].string_value
        if not board_name:
            raise ValueError("board_name cannot be empty")
        req_deps.append(board_name)
        return req_deps, []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        self.board_name = config.attributes.fields["board_name"].string_value
        board_resource_name = Board.get_resource_name(self.board_name)
        board_resource = dependencies[board_resource_name]
        self.board = cast(Board, board_resource)
        self.counter = 0
        self.running = False
        return super().reconfigure(config, dependencies)

    async def _on_loop(self):
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
                pin = await self.board.gpio_pin_by_name(name="13")
                await pin.set(high=True)
                result[name] = True
            if name == "action" and args == "stop":
                self.running = False
                pin = await self.board.gpio_pin_by_name(name="13")
                await pin.set(high=False)
                result[name] = True
            if name == "action" and args == "run_control_logic":
                if self.running:
                    await self._on_loop()
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

For more information, see [Module dependencies](/operate/modules/advanced/dependencies/).

## Add the control logic module locally

If you have the code on the machine that runs `viam-server` you can test the module as a _local_ module:

{{< table >}}
{{% tablestep start=1 %}}
**Configure your module as a local module.**

Navigate to your machine's **CONFIGURE** page.
Make sure your machine is showing as live and connected to Viam.

Click the **+** button, select **Local module**, then select **Local module** again.

{{< tabs >}}
{{% tab name="Python" %}}

Enter the path to the <file>run.sh</file> file, for example, `/home/naomi/control-logic/run.sh` on Linux or `/Users/naomi/control-logic/run.sh` on macOS.
Click **Create**.

Save your config.
{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure your resource as a local component or service.**

{{< tabs >}}
{{% tab name="Python" %}}

Click **+**, click **Local module**, then click **Local component** or **Local service** depending on your resource type and fill in the fields as follows:

- model namespace triplet: `<namespace>:control-logic:control-logic`, you can see the full triplet in the module's <FILE>meta.json</FILE> file
- type: `<resource-type>`
- name: `resource-1`

If you use other machine resources, add their configuration values in the resource's configuration field and updating the names as needed:

```json {class="line-numbers linkable-line-numbers"}
{
  "board_name": "board-1"
}
```

Save the config.

{{% /tab %}}
{{< /tabs >}}

Use the **TEST** panel to test the resource.

If you are encountering errors, check the **LOGS** tab for more information.

{{% /tablestep %}}
{{% tablestep %}}
**Iterate.**

If you make changes to your module code, you must restart your module for the changes to take effect.

{{% /tablestep %}}
{{< /table >}}

## Test the control logic

You can use the `DoCommand` method from the web UI or from the Viam SDKs:

{{< tabs >}}
{{% tab name="Web UI" %}}

On the **CONTROL** or the **CONFIGURE** tab, use the `DoCommand` panel:

1. Copy and paste one of the following command inputs:

   To set `self.running` to `True`, copy and paste the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "start"
   }
   ```

   To run the control logic loop method `_on_loop`, copy and paste the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "run_control_logic"
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
await control_logic.do_command({"action": "run_control_logic"})

# Stop your control logic
await control_logic.do_command({"action": "stop"})
```

{{% /tab %}}
{{< /tabs >}}

These steps manually test the control logic, to run the logic automatically, see [Run control logic automatically with jobs](#run-control-logic-automatically-with-jobs).

## Run control logic automatically with jobs

To run control logic, use a {{< glossary_tooltip term_id="job" text="job" >}} which calls the `DoCommand` method periodically.

{{< table >}}
{{% tablestep start=1 %}}
**Start control logic at specific time each day**

Click the **+** icon next to your machine part in the left-hand menu and select **Job**.
You can use the default name, `job-1`, and click **Create**.

In the job panel, set the **Schedule** to **Cron** and enter `0 0 8 * * *` which will run the job at 08:00 AM.

Then configure the job to use the control logic resource using the name you gave it when you deployed it.

Lastly, select the `DoCommand` **Method** and specify the **Command** `{ "action": "start" }`.

Click **Save**.

{{% /tablestep %}}
{{% tablestep %}}
**Run control logic periodically**

Configure another job:

- **Cron Schedule**: `0 * * * * *` (every minute)
- **Resource**: `resource-1`
- **Method**: `DoCommand`
- **Command**: `{ "action": "run_control_logic" }`

{{% /tablestep %}}
{{% tablestep %}}
**End control logic at specific time each day**

Configure another job:

- **Cron Schedule**: `0 0 17 * * *` (at 05:00 PM)
- **Resource**: `resource-1`
- **Method**: `DoCommand`
- **Command**: `{ "action": "stop" }`

{{% /tablestep %}}
{{< /table >}}

Now, check the **LOGS** tab; you'll see the second job triggered every minute, but the counter will only increase once the first job to run the `start` command runs at 8 AM.
For testing purposes, you can also [send this command manually](#test-the-control-logic).

## Next steps

Once you have thoroughly tested your module, continue to [package and deploy](/operate/modules/deploy-module/) it.
