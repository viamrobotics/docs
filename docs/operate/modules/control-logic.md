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

This guide shows you how to write a module with control logic for a machine:

1. [Create a module](#create-a-module-with-a-generic-component-template) with a template for the control logic
1. [Program the control logic](#program-control-logic-in-module) using the `DoCommand` method
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

Open the python file in the <FILE>src/models/</FILE> folder to add your control logic to it.

The following example shows how you might implement logic that toggles an LED on and off.

Any resources that you wish to access from your control logic need to be identified and instantiated.
To keep your code loosely coupled, we recommend passing the resource names in the configuration attributes of the control logic.
We must modify the `validate_config` method to ensure all required values are passed in correctly and then instantiate the resource in the `new` method.

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
        fields = config.attributes.fields
        if "board_name" not in fields:
            raise Exception("missing required board_name attribute")
        elif not fields["board_name"].HasField("string_value"):
            raise Exception("board_name must be a string")
        board_name = fields["board_name"].string_value
        if not board_name:
            raise ValueError("board_name cannot be empty")
        if "pin" not in fields:
            raise Exception("missing required pin attribute")
        elif not fields["pin"].HasField("string_value"):
            raise Exception("pin must be a string")
        pin = fields["pin"].string_value
        if not pin:
            raise ValueError("pin cannot be empty")
        # Return the board as a required dependency (just the name, not the full ResourceName)
        req_deps = [board_name]
        return req_deps, []
```

{{% /tablestep %}}
{{% tablestep %}}
**Set up instance parameters**

When your new model gets added to your machine, its `new()` method gets called.
You can use it to store any instance variables.

`viam-server` passes the required dependencies when the control logic resource is reconfiguring.
From these dependencies you can get the board and store it in an instance variable.

```python
    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        toggler = super().new(config, dependencies)
        toggler.board_name = config.attributes.fields["board_name"].string_value
        board_resource_name = Board.get_resource_name(toggler.board_name)
        board_resource = dependencies[board_resource_name]
        toggler.board = cast(Board, board_resource)
        toggler.pin = config.attributes.fields["pin"].string_value
        return toggler

```

Add the following imports at the top of <FILE>src/models/control_logic.py</FILE>:

```python
from typing import cast
from viam.components.board import Board
```

The `new` method gets called whenever the control logic module starts or when a configuration change occurs for the resource itself.

If this is a problem, consider writing state to a file on disk and adding logic to handle subsequent calls to the `new` method gracefully.

{{% /tablestep %}}
{{% tablestep %}}
**Write the control logic.**

Update your logic in the `do_command` method to use the board:

```python {class="line-numbers linkable-line-numbers" data-line="11-17"}
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for name, args in command.items():
            if name == "action" and args == "toggle":
                pin = await self.board.gpio_pin_by_name(name=self.pin)
                high = await pin.get()
                if high:
                    await pin.set(high=False)
                else:
                    await pin.set(high=True)
                result[name] = True
        return result
```

{{% /tablestep %}}
{{< /table >}}

{{% expand "Click to view the entire control logic code" %}}

This is the code for <FILE>src/models/control_logic.py</FILE>:

```python {class="line-numbers linkable-line-numbers" data-line=""}
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

from typing import cast
from viam.components.board import Board


class Toggler(Generic, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(ModelFamily("naomi", "led-toggle"), "toggler")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Generic component.
        The default implementation sets the name from the `config` parameter.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both required and optional)

        Returns:
            Self: The resource
        """
        toggler = super().new(config, dependencies)
        toggler.board_name = config.attributes.fields["board_name"].string_value
        board_resource_name = Board.get_resource_name(toggler.board_name)
        board_resource = dependencies[board_resource_name]
        toggler.board = cast(Board, board_resource)
        toggler.pin = config.attributes.fields["pin"].string_value
        return toggler

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "board_name" not in fields:
            raise Exception("missing required board_name attribute")
        elif not fields["board_name"].HasField("string_value"):
            raise Exception("board_name must be a string")
        board_name = fields["board_name"].string_value
        if not board_name:
            raise ValueError("board_name cannot be empty")
        if "pin" not in fields:
            raise Exception("missing required pin attribute")
        elif not fields["pin"].HasField("string_value"):
            raise Exception("pin must be a string")
        pin = fields["pin"].string_value
        if not pin:
            raise ValueError("pin cannot be empty")
        # Return the board as a required dependency (just the name, not the full ResourceName)
        req_deps = [board_name]
        return req_deps, []

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for name, args in command.items():
            if name == "action" and args == "toggle":
                pin = await self.board.gpio_pin_by_name(name=self.pin)
                high = await pin.get()
                if high:
                    await pin.set(high=False)
                else:
                    await pin.set(high=True)
                result[name] = True
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

For more information on accessing components and services, see [Module dependencies](/operate/modules/advanced/dependencies/).

## Test your module locally

You can test your module locally before uploading it to the [registry](https://app.viam.com/registry).

### Add module to machine

To get your module onto your machine, hot reloading builds and packages it and then uses the shell service to copy it to the machine for testing.
If your files are already on the machine, you can add the module manually instead.

{{< tabs >}}
{{% tab name="Hot reloading (recommended)" %}}

Run the following command to build the module and add it to your machine:

{{< tabs >}}
{{% tab name="Same device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload-local --cloud-config /path/to/viam.json
```

{{% /tab %}}
{{% tab name="Other device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id 123abc45-1234-432c-aabc-z1y111x23a00
```

{{% /tab %}}
{{< /tabs >}}

For more information, see the [`viam module` documentation](/dev/tools/cli/#module).

{{< expand "Reload troubleshooting" >}}

- `Error: Could not connect to machine part: context deadline exceeded; context deadline exceeded; mDNS query failed to find a candidate`

  Try specifying the `--part-id`, which you can find by clicking the **Live** indicator on your machine's page and clicking **Part ID**.

- `Error: Rpc error: code = Unknown desc = stat /root/.viam/packages-local: no such file or directory`

  Try specifying the `--home` directory, for example `/Users/yourname/` on macOS.

- `Error: Error while refreshing token, logging out. Please log in again`

  Run `viam login` to reauthenticate the CLI.

### Try using a different command

If you are still having problems with the `reload` command, you can use a different, slower method of rebuilding and then restarting the module.
Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it on your machine's **CONFIGURE** tab.
In the upper-right corner of the module's card, click the **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="width:300px" class="shadow" >}}

{{< /expand >}}

{{< alert title="Refresh" color="note" >}}

You may need to refresh your machine page for your module to show up.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Manual" %}}

Navigate to your machine's **CONFIGURE** page.

Click the **+** button, select **Local module**, then again select **Local module**.

Enter the path to the automatically-generated <file>run.sh</file> script.
Click **Create**.
For local modules, `viam-server` uses this path to start the module.

**Example module**:
For the `control-logic` module, the path should resemble `/home/yourname/control-logic/run.sh` on Linux, or `/Users/yourname/control-logic/run.sh` on macOS.

Save the config.

{{% /tab %}}
{{< /tabs >}}

{{< table >}}
{{< /table >}}

### Add local model

{{< table >}}
{{% tablestep start=1 %}}
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
  "board_name": "board-1",
  "pin": "13"
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
Click on the **...** menu near the module and select **Restart**.

{{% /tablestep %}}
{{< /table >}}

## Test the control logic

You can use the `DoCommand` method from the web UI or from the Viam SDKs:

{{< tabs >}}
{{% tab name="Web UI" %}}

On the **CONTROL** or the **CONFIGURE** tab, use the `DoCommand` panel:

1. Copy and paste the following command input:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": "toggle"
   }
   ```

2. Click **Execute** to call `DoCommand()` with the command input on your machine.

   {{<imgproc src="/components/generic/generic-control.png" alt="The generic component in the test panel." resize="900x" style="width:500px" class="imgzoom shadow">}}<br>

{{% /tab %}}
{{% tab name="Python" %}}

You can run your control logic with the `DoCommand()` method from the Python SDK:

```python
await control_logic.do_command({"action": "toggle"})
```

{{% /tab %}}
{{< /tabs >}}

These steps manually test the control logic, to run the logic automatically, see [Run control logic automatically with jobs](#run-control-logic-automatically-with-jobs).

## Run control logic automatically with jobs

To run control logic, use a {{< glossary_tooltip term_id="job" text="job" >}} which calls the `DoCommand` method periodically.

1. Click the **+** icon next to your machine part in the left-hand menu and select **Job**.
1. You can use the default name, `job-1`, and click **Create**.
1. In the job panel, set the **Schedule** to **Interval** and enter `5` seconds.
1. Then configure the job to use the control logic resource using the name you gave it when you deployed it.
1. Select the `DoCommand` **Method** and specify the **Command** `{ "action": "toggle" }`.
1. Click **Save**.

For testing purposes, you can also [send this command manually](#test-the-control-logic).

## Next steps

Once you have thoroughly tested your module, continue to [package and deploy](/operate/modules/deploy-module/) it.
