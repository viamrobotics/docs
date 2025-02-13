---
linkTitle: "Deploy software"
title: "Deploy software packages to machines (OTA)"
weight: 30
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "Deploy code packages with machine control logic to one or more machines."
languages: []
viamresources: []
platformarea: ["registry", "fleet"]
level: "Intermediate"
date: "2025-02-05"
aliases:
  - /how-tos/deploy-packages/
  - /manage/software/deploy-packages/
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

{{< glossary_tooltip term_id="module" text="Modules" >}} are code packages that provide most of the functionality on your machines: drivers, integrations, and control logic.

The following steps show you how to create modules with control logic and how to deploy and manage all of your machine's modules over the air (OTA):

1. [Create a module with machine control logic](#create-a-module-with-machine-control-logic)
2. [Create a configuration fragment with the modules for your machine](#create-a-fragment)
3. [Add the fragment to one or more machines](#add-the-fragment-to-your-machines)

## Prerequisites

Start by [setting up one machine](/operate/get-started/setup/).
Then, [configure any hardware and software resources](/operate/get-started/supported-hardware/) that you will use with your machine and that you want to drive with your control logic.

## Create a module with machine control logic

One method of operating your machine is by running control logic on another device, such as an app.
With {{< glossary_tooltip term_id="module" text="modules" >}}, you can run your control logic on the machine itself.

{{% alert title="OTA updates for microcontrollers" color="note" %}}
The following steps cover how to create a module for machines running `viam-server`.
For microcontrollers, see [Micro-RDK modules](/operate/get-started/other-hardware/micro-module/) and [Over-the-air firmware updates](/operate/get-started/other-hardware/micro-module/#over-the-air-updates).
{{% /alert %}}

{{< table >}}
{{% tablestep link="/operate/get-started/other-hardware/" %}}
**1. Generate stub files**

Run the `module generate` command in your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --resource-subtype=generic-component
```

Follow the prompts, selecting the following options:

- Module name: Your choice, for example `my-control-logic`
- Language: Your choice
- Visibility: `Private`
- Namespace/Organization ID: In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page.
  Find the **Public namespace** and copy that string.
  In the example snippets below, the namespace is `naomi`.
- Resource to be added to the module: `Generic Component`.[^generic]
- Model name: Your choice, for example `control-logic`
- Enable cloud build: Choose `Yes` if you are using GitHub or want to use cloud build.
- Register module: `Yes`

Press the Enter key and the generator will create a folder for your control logic component.

[^generic]:
    For simplicity, this guide uses the generic component.
    You can choose a different resource type to add your control logic to.
    For example, for logic controlling a camera, you may wish to use the camera component.
    You must implement any required API methods for the chosen component.

{{% /tablestep %}}
{{% tablestep %}}
**2. Add your control logic**

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
- [`detectio-dock`](https://github.com/viam-labs/detection-dock)

{{% /tablestep %}}
{{% tablestep link="/operate/get-started/other-hardware/manage-modules/#update-an-existing-module-using-a-github-action" %}}
**3. Package your control logic**

Once you have implemented your control logic, commit and push your changes to a GitHub repository.

If you are not using GitHub, see [Upload your module](/operate/get-started/other-hardware/#upload-your-module) and [Update an existing module](/operate/get-started/other-hardware/manage-modules/#update-an-existing-module-using-a-github-action) for more information on alternatives.

Follow the steps in [Upload your module](/operate/get-started/other-hardware/#upload-your-module) using cloud build.

Then [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github) with a tag of the form `1.0.0`.
Your module will now be built, packaged and pushed to the Viam Registry.

{{% /tablestep %}}
{{< /table >}}

## Create a fragment

Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for using the same configuration on multiple machines.
When deploying or updating software on many machines, you should use fragments to deploy your modules OTA to your machines.

The following example starts with a machine with a camera and a servo and adds the [control logic module](#create-a-module-with-machine-control-logic).
The resulting machine configuration gets used to create the fragment for reuse on other machines.

{{< table >}}
{{% tablestep link="/operate/get-started/supported-hardware/" %}}
**1. Configure your software**

Go to your [machine](#prerequisites) in the [Viam app](https://app.viam.com).

Then add your control logic module.

{{<imgproc src="/how-tos/deploy-packages/add-package.png" resize="800x" class="fill aligncenter" style="width: 500px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Set the version and update strategy**

Scroll to the module card for your control logic module and select the pinned version type.
You can select a specific version or set the machine to always update to the latest major, minor, patch, or pre-release version once new versions are available.
For more information on these configuration options, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

{{<imgproc src="/how-tos/deploy-packages/version.png" resize="800x" class="fill aligncenter" style="width: 500px" declaredimensions=true alt="Module card UI">}}

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If the module cannot be interrupted, the module will not be upgraded.
{{% /alert %}}

{{% /tablestep %}}

{{% tablestep %}}
**3. Copy the raw JSON**

In your machine's **CONFIGURE** tab, switch to **JSON** and copy the raw JSON.

The following example shows a machine with a configured camera and the control logic module.
Your machine will have different resources.

{{<imgproc src="/how-tos/deploy-packages/json-config.png" resize="800x" class="fill aligncenter" style="width: 600px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep link="/manage/fleet/reuse-configuration/" %}}
**4. Create a fragment**

Go to [app.viam.com/fragments](https://app.viam.com/fragments).

Add a fragment, and paste the copied JSON configuration into it.

{{<imgproc src="/how-tos/deploy-packages/fragment.png" resize="1000x" alt="Configuration builder UI">}}

Set your privacy settings.
There are three options for this:

- **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
- **Private:** No user outside of your organization will be able to view or use this fragment.
- **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

Click **Save**.

If you want to edit the fragment later, do it from this screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/delete.png" class="fill alignleft" resize="500x" style="width: 200px" declaredimensions=true alt="Delete">}}
**5. Delete the original machine configuration (optional)**

Now that the configuration is saved as a fragment, you can delete the machine you created in step 1.
We only created this machine to easily generate the JSON config for the fragment.

{{% /tablestep %}}
{{< /table >}}

## Add the fragment to your machines

Generally, fragments are used with [provisioning](/manage/fleet/provision/setup/) to deploy and manage softwareon many machines.

You can also add the fragment manually to the machines that need it:

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/how-tos/deploy-packages/insert.png" resize="800x" class="fill alignleft imgzoom" style="width: 250px" declaredimensions=true alt="Add fragment">}}
**Add the fragment to one machine**

On your machine's **CONFIGURE** tab, click the **+** button and select **Insert fragment**.
Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{< alert title="Tip" color="tip" >}}
You can also add multiple fragments to one machine.
{{< /alert >}}

{{% /tablestep %}}
{{< /table >}}
