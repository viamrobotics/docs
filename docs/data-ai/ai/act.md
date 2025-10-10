---
linkTitle: "Act based on inferences"
title: "Act based on inferences"
weight: 70
layout: "docs"
type: "docs"
description: "Use the vision service API to act based on inferences."
date: "2025-10-09"
---

You can use the [vision service API](/dev/reference/apis/services/vision/) to get information about your machine's inferences and program behavior based on that.

This guide will walk you through the steps to create logic for acting based on inferences.
At the end of each step, you'll learn how to apply the step to a fictional example where you want to stop an arm from moving, when a person is detected in the arm's surroundings.

## Prerequisites

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "A configured camera and vision service." >}}

Follow the instructions to [configure a camera](/operate/reference/components/camera/) and [run inference](/data-ai/ai/run-inference/).

{{< /expand >}}

{{% expand "The Viam CLI." %}}

{{< table >}}
{{% tablestep start=1 %}}
**Install the CLI.**

You must have the Viam CLI installed to generate and upload modules:

{{< readfile "/static/include/how-to/install-cli.md" >}}
{{% /tablestep %}}
{{% tablestep %}}
**Log in with the CLI.**

Run the following command to log in:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam login
```

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
{{< /table >}}

{{% /expand%}}

## Create a module

To program your machine's behavior based on the output of a vision service, create a resource that makes use of the vision service as input and controls the resources that should actuate based on the input.

{{< table >}}

{{% tablestep start=1 %}}
**Generate the module template.**

Replace `<ORGANIZATION-ID>` with your organization ID, which resembles: `a12b3c4d-1234-123a-12a3-a1b23c45d67e`.

{{< tabs >}}
{{% tab name="Python" %}}

```sh {class="command-line" data-prompt="$" data-output="4-10"}
viam module generate --language python --model-name intelligent-resource \
  --name vision-intelligence --public-namespace <ORGANIZATION-ID> --public
```

{{% /tab %}}
{{< /tabs >}}

You can use **any resource type**.
The choice of resource type affects the API methods that you must implement.
If you will use the vision service to change the behavior of one resource, choose that resource type.
If none fits, use the vision service resource type and implement the logic in the `GetClassifications` or `GetDetections` methods.

**Safe arm example**:
For the use case of using a vision service to stop arm movement when a person is nearby, using the `arm` resource type makes sense.
Essentially, the resource will wrap the existing arm component's API methods and check for people before moving.

{{% /tablestep %}}
{{% tablestep %}}
**Set up the imports for the resource.**

The CLI generated several files, but you'll only need to modify the file in the <FILE>src/models/</FILE> folder, <FILE>intelligent-resource.py</FILE>, to implement your logic.

Open <FILE>vision-intelligence/src/models/intelligent-resource.py</FILE>.
This is the template for the resource API to which you will add logic.

To use the vision service, you must import these Python packages:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" }
from typing import cast
from viam.services.vision import *
```

{{% /tab %}}
{{< /tabs >}}

You must also import packages for any other resources you wish to control.

{{% /tablestep %}}
{{% tablestep %}}
**Validate the resource's config.**

Your resource needs to know the name of the vision service to get inferences from, as well as the camera name to use the vision service with.
You also need to add configuration fields for any other resources you wish to access or control.

The `validate_config` method parses the configuration for the resource and ensures it is valid.
It also returns a list of required dependencies that informs `viam-server` to ensure this resource only starts once all dependencies are available.

{{< tabs >}}
{{% tab name="Python" %}}

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
        if "vision_name" not in fields:
            raise Exception("missing required vision_name attribute")
        elif not fields["vision_name"].HasField("string_value"):
            raise Exception("vision_name must be a string")
        vision_name = fields["vision_name"].string_value
        if not vision_name:
            raise ValueError("vision_name cannot be empty")
        req_deps.append(vision_name)
        return req_deps, []
```

{{% /tab %}}
{{< /tabs >}}

**Safe arm example**:
For the safe arm example, you also need to get the name of the existing arm resource which this resource will wrap:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-start="55" }
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        req_deps = []
        fields = config.attributes.fields
        # ...
        if "arm_name" not in fields:
            raise Exception("missing required arm_name attribute")
        elif not fields["arm_name"].HasField("string_value"):
            raise Exception("arm_name must be a string")
        arm_name = fields["arm_name"].string_value
        if not arm_name:
            raise ValueError("arm_name cannot be empty")
        req_deps.append(arm_name)
        return req_deps, []
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Initialize all variables.**

`viam-server` calls the `reconfigure` method whenever the module starts or a configuration change occurs.
Use this method to initialize the vision service and camera name, as well as any other resources you plan to use.
The dependencies parameter contains all the resources this component can access.
By using `cast`, you tell Python the type of the resource.

Update the `reconfigure` method to initialize all the variables:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-start="79" }
    def reconfigure(
        self, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ):
        camera_name = config.attributes.fields["camera_name"].string_value
        vision_name = config.attributes.fields["vision_name"].string_value

        # Get the full resource name for the vision service
        # (rdk:service:vision/object-detector)
        vision_resource_name = VisionClient.get_resource_name(vision_name)

        # Check if the vision resource exists in dependencies
        if vision_resource_name not in dependencies:
            raise KeyError(f"Vision service '{vision_name}' not found in "
                           f"dependencies. Available resources: "
                           f"{list(dependencies.keys())}")

        vision_resource = dependencies[vision_resource_name]
        self.vision_service = cast(VisionClient, vision_resource)
        self.camera_name = camera_name

        return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{< /tabs >}}

**Safe arm example**: For the safe arm example, you also need to initialize the arm:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-start="79" }
    def reconfigure(
        self, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ):
        # ...
        arm_name = config.attributes.fields["arm_name"].string_value
        arm_resource_name = Arm.get_resource_name(arm_name)

        if arm_resource_name not in dependencies:
            raise KeyError(f"Arm component '{arm_name}' not found in "
                           f"dependencies. Available resources: "
                           f"{list(dependencies.keys())}")

        arm_resource = dependencies[arm_resource_name]
        self.arm = cast(Arm, arm_resource)

        return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Implement the API methods.**

{{< tabs >}}
{{% tab name="Python" %}}

In the <FILE>vision-intelligence/src/models/intelligent-resource.py</FILE> file, find the API methods that you wish to change and add the logic.

Depending on if your vision service implements `GetDetections` or `GetClassifications`, use the relevant method and implement the logic.

{{< tabs >}}
{{% tab name="Detections" %}}

```python
detections = await self.vision_service.get_detections_from_camera(self.camera_name)
for d in detections:
    if d.confidence > 0.6 and d.class_name == "LABEL":
        self.logger.info(f"Detection {d.class_name} with confidence {d.confidence}.")
        # DO SOMETHING
```

{{% /tab %}}
{{% tab name="Classifications" %}}

```python
classifications = await self.vision_service.get_classifications_from_camera(
    self.camera_name,
    4)
for c in classifications:
    if c.confidence > 0.6 and c.class_name == "LABEL":
        self.logger.info(f"Classification {c.class_name} with confidence {c.confidence}.")
        # DO SOMETHING
```

{{% /tab %}}
{{< /tabs >}}

**Safe arm example**:
The arm wrapper resource uses the vision service to check for people.
If a person is detected, the resource raises an error, otherwise it passes the command to the arm.

```python
    async def _is_safe_to_move(self):
        detections = await self.vision_service.get_detections_from_camera(self.camera_name)
        for d in detections:
            if d.confidence > 0.4 and d.class_name == "Person":
                self.logger.warn(f"Detected {d.class_name} with confidence {d.confidence}.")
                return False
        self.logger.warn("No person detected. Safe arm will move.")
        return True

    async def move_to_position(
        self,
        pose: Pose,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        if await self._is_safe_to_move():
            await self.arm.move_to_position(pose, extra=extra, timeout=timeout)
        else:
            raise ValueError("Person detected. Safe arm will not move.")

    async def move_to_joint_positions(
        self,
        positions: JointPositions,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        if await self._is_safe_to_move():
            await self.arm.move_to_joint_positions(positions, extra=extra, timeout=timeout)
        else:
            raise ValueError("Person detected. Safe arm will not move.")
```

All other methods pass the method call through to the `self.arm` resource.
For example:

```python
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        return await self.arm.do_command(command, timeout, **kwargs)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

## Test and use the module

{{< table >}}
{{% tablestep start=1 %}}
**Configure your module as a local module.**

The next step is to test the resource on your machine.

Navigate to your machine's **CONFIGURE** page.
Make sure your machine is showing as live and connected to Viam.

Click the **+** button, select **Local module**, then select **Local module** again.

{{< tabs >}}
{{% tab name="Python" %}}

Enter the path to the <file>run.sh</file> file, for example, `/home/naomi/vision-intelligence/run.sh` on Linux or `/Users/naomi/vision-intelligence/run.sh` on macOS.
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

- model namespace triplet: `<namespace>:vision-intelligence:intelligence-resource`, you can see the full triplet in the module's <FILE>meta.json</FILE> file
- type: `<resource-type>`
- name: `resource-1`

Configure the camera and vision service names by pasting the following in the configuration field and updating the names as needed:

```json {class="line-numbers linkable-line-numbers"}
{
  "camera_name": "camera-1",
  "vision_name": "person-detector"
}
```

Save the config.

{{% /tab %}}
{{< /tabs >}}

Use the **TEST** panel to test the resource.

If you are encountering errors, check the **LOGS** tab for more information.

{{% /tablestep %}}
{{% tablestep %}}
**Upload your module.**

Commit and push your changes to a GitHub repository.

Follow the steps in [Upload your module](/operate/modules/other-hardware/create-module/#upload-your-module) using cloud build.
When you create a release, your module will be built, packaged, and pushed to the Viam Registry.

If you are not using GitHub or cloud build, see [Upload your module](/operate/modules/other-hardware/create-module/#upload-your-module) and [Update an existing module](/operate/modules/other-hardware/manage-modules/#update-automatically-from-a-github-repo-with-cloud-build) for more information on alternatives.

Once uploaded, remove the local module and local resource, and add the resource from the registry.

{{% /tablestep %}}
{{% tablestep %}}
**Trigger the logic.**

Depending on the logic you've implemented, you must now ensure the new methods get called.

If your resource is a wrapper resource, make sure you update any references to the previous resource in components, services, triggers, and jobs that use the resource.

If your logic works differently, you need to decide how this logic gets called, whether by another component or service or by a {{< glossary_tooltip term_id="job" text="job" >}}.

**Safe arm example**:
In the arm example, the arm is moved by a motion service.
The motion service is currently configured to use the pre-existing arm.
To change that, you'd update the component name in the motion service configuration.

{{% /tablestep %}}
{{< /table >}}

## Examples

To see a different example that uses a vision service to determine behavior and has the logic triggered with a {{< glossary_tooltip term_id="job" text="job" >}}, see the [Desk Safari Tutorial](/operate/hello-world/tutorial-desk-safari/).
