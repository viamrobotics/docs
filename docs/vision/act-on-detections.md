---
linkTitle: "Act on detections"
title: "Act on detections"
weight: 60
layout: "docs"
type: "docs"
description: "Build a module that uses vision service results to control machine behavior."
aliases:
  - /vision/act/
  - /vision/how-to/act-on-detections/
  - /data-ai/ai/act/
date: "2026-04-14"
---

You have a vision service detecting or classifying objects, but you need your machine to respond automatically -- stop an arm when a person is nearby, sort items by color, or trigger an action when an anomaly appears. This guide shows you how to build a module that reads vision results and controls other resources based on what it sees.

## Concepts

### The wrapper pattern

The most common approach is to create a module that wraps an existing resource. The wrapper intercepts API calls, checks vision results, and decides whether to pass the call through or block it.

For example, a "safe arm" module wraps a real arm. When your code calls `move_to_position`, the wrapper first checks the vision service for people in the frame. If no one is detected, it passes the command to the real arm. If a person is detected, it raises an error.

This pattern works with any resource type: arms, bases, motors, or even other services.

### Choosing a resource type

Your module must implement a resource API. Pick the type that matches what you are controlling:

| Scenario                                  | Resource type                                |
| ----------------------------------------- | -------------------------------------------- |
| Gate movement commands based on vision    | The component being gated (arm, base, motor) |
| Classify images with custom logic         | Vision service                               |
| Trigger actions across multiple resources | Generic service                              |

The choice determines which API methods you must implement. A wrapper around an arm implements the arm API. A standalone logic service might implement the generic service API.

### Dependencies

Your module needs access to the vision service, a camera, and whatever resource it controls. Viam's dependency system handles this: you declare required dependencies in `validate_config`, and `viam-server` ensures they are available before your module starts.

## Steps

### 1. Generate the module scaffold

Install the [Viam CLI](/cli/) and generate a module template. Replace `<ORGANIZATION-ID>` with your organization ID.

```sh {class="command-line" data-prompt="$"}
viam module generate --language python --model-name safe-arm \
  --name my-vision-module --public-namespace <ORGANIZATION-ID> --public
```

The CLI creates a project directory with the files you need. The only file you need to modify is the model file in `src/models/`.

### 2. Add imports

Open the generated model file (for example, `src/models/safe-arm.py`) and add imports for the vision service and any resources you will control:

```python
from typing import cast
from viam.services.vision import *
```

Import additional resource types as needed. For the safe arm example:

```python
from viam.components.arm import Arm
```

### 3. Validate configuration

The `validate_config` method parses your module's configuration and returns a list of required dependencies. This tells `viam-server` to wait until all dependencies are available before starting your module.

Your module needs at minimum a camera name and a vision service name:

```python
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

Add validation for any other resources your module wraps. For the safe arm, add `arm_name` to the required dependencies the same way.

### 4. Initialize dependencies in reconfigure

The `reconfigure` method runs when the module starts and whenever configuration changes. Use it to get references to your dependencies:

```python
def reconfigure(
    self, config: ComponentConfig,
    dependencies: Mapping[ResourceName, ResourceBase]
):
    camera_name = config.attributes.fields["camera_name"].string_value
    vision_name = config.attributes.fields["vision_name"].string_value

    vision_resource_name = VisionClient.get_resource_name(vision_name)
    if vision_resource_name not in dependencies:
        raise KeyError(f"Vision service '{vision_name}' not found in "
                       f"dependencies. Available: "
                       f"{list(dependencies.keys())}")

    self.vision_service = cast(VisionClient,
                               dependencies[vision_resource_name])
    self.camera_name = camera_name

    return super().reconfigure(config, dependencies)
```

For the safe arm, also initialize the arm reference:

```python
    arm_name = config.attributes.fields["arm_name"].string_value
    arm_resource_name = Arm.get_resource_name(arm_name)
    self.arm = cast(Arm, dependencies[arm_resource_name])
```

### 5. Implement the vision check

Create a helper method that queries the vision service and returns a decision:

{{< tabs >}}
{{% tab name="Detections" %}}

```python
async def _is_safe(self):
    detections = await self.vision_service.get_detections_from_camera(
        self.camera_name)
    for d in detections:
        if d.confidence > 0.4 and d.class_name == "Person":
            self.logger.warn(
                f"Detected {d.class_name} "
                f"with confidence {d.confidence}.")
            return False
    return True
```

{{% /tab %}}
{{% tab name="Classifications" %}}

```python
async def _is_safe(self):
    classifications = (
        await self.vision_service.get_classifications_from_camera(
            self.camera_name, 4))
    for c in classifications:
        if c.confidence > 0.6 and c.class_name == "UNSAFE":
            self.logger.warn(
                f"Classification {c.class_name} "
                f"with confidence {c.confidence}.")
            return False
    return True
```

{{% /tab %}}
{{< /tabs >}}

### 6. Wire the check into API methods

Override the API methods where you want vision-based gating. For the safe arm:

```python
async def move_to_position(
    self,
    pose: Pose,
    *,
    extra: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
):
    if await self._is_safe():
        await self.arm.move_to_position(
            pose, extra=extra, timeout=timeout)
    else:
        raise ValueError(
            "Person detected. Safe arm will not move.")


async def move_to_joint_positions(
    self,
    positions: JointPositions,
    *,
    extra: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
):
    if await self._is_safe():
        await self.arm.move_to_joint_positions(
            positions, extra=extra, timeout=timeout)
    else:
        raise ValueError(
            "Person detected. Safe arm will not move.")
```

Pass through all other methods to the underlying resource:

```python
async def do_command(
    self,
    command: Mapping[str, ValueTypes],
    *,
    timeout: Optional[float] = None,
    **kwargs
) -> Mapping[str, ValueTypes]:
    return await self.arm.do_command(
        command, timeout=timeout, **kwargs)
```

### 7. Test with hot reloading

Use the CLI to build and deploy your module to a machine during development:

```bash
# Build in the cloud and deploy to the machine
viam module reload --part-id <machine-part-id>

# Optionally add a resource at the same time
viam module reload --part-id <machine-part-id> \
  --model-name my-org:my-module:safe-arm
```

If your development machine and target machine share the same architecture, you can build locally instead:

```bash
# Build locally and transfer to the machine
viam module reload-local --part-id <machine-part-id>
```

After the module is deployed, configure its attributes in the Viam app:

```json {class="line-numbers linkable-line-numbers"}
{
  "camera_name": "my-camera",
  "vision_name": "my-detector",
  "arm_name": "my-arm"
}
```

**Save** and use the **TEST** panel to verify behavior.

Each time you make changes, run `viam module reload` again to rebuild and redeploy.

### 8. Upload to the [registry](https://app.viam.com/registry)

Once your module is working:

1. Commit and push your code to a GitHub repository.
2. Follow the steps to [upload your module](/build-modules/deploy-a-module/) using cloud build.

### 9. Update references

If your module wraps another resource, update any services or processes that reference the original. For example, if motion planning used `my-arm`, update it to use `safe-arm-1` so all movement commands go through the vision check.

## Try It

1. Configure a safe arm module with a person detection model and point the camera at yourself. Attempt to move the arm and verify it refuses.
2. Move out of frame and try again -- the arm should move normally.
3. Adjust the confidence threshold in `_is_safe` and observe how it affects sensitivity.
4. Try swapping detections for classifications to see how the two approaches differ.

## Troubleshooting

{{< expand "Module fails to start" >}}

- Check the **LOGS** tab for error messages.
- Verify that all dependency names in your config (`camera_name`, `vision_name`, `arm_name`) exactly match the names of configured resources.
- Ensure the `run.sh` path is correct and the file is executable (`chmod +x run.sh`).

{{< /expand >}}

{{< expand "Vision check always returns safe / unsafe" >}}

- Test the vision service independently using the **TEST** panel to confirm it produces detections.
- Check that the `class_name` in your code matches the model's output labels exactly (case-sensitive).
- Log the raw detections or classifications before filtering to see what the model returns.

{{< /expand >}}

{{< expand "Wrapper methods not being called" >}}

- Confirm that other services and processes reference the wrapper resource name, not the original resource.
- Check that your module registers the correct resource type and model triplet.

{{< /expand >}}

## What's Next

- [Alert on Detections](/vision/alert-on-detections/) -- send email or webhook notifications when specific objects are detected.
- [Deploy a Module](/build-modules/deploy-a-module/) -- package and upload your module to the Viam [registry](https://app.viam.com/registry).
- [Vision Service API Reference](/reference/apis/services/vision/) -- full API documentation for detections, classifications, and more.
