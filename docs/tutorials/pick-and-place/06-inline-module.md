---
title: "Phase 6: Inline module"
linkTitle: "6. Inline module"
type: "docs"
slug: "inline-module"
weight: 60
description: "Optional: package your working script as an inline module that runs on the robot."
workshop: "pick-and-place"
toc_hide: true
phase: 6
phase_total: 6
time_estimate: "20 minutes"
prev: "/tutorials/pick-and-place/perception-guided-picking/"
next: "/tutorials/pick-and-place/wrap-up/"
languages: ["python"]
---

This phase is optional. The previous phase already gave you a complete pick-and-place loop that runs from your own laptop: detection, the frame transform, planned motion, and a reliable place. This phase packages that same loop as a module so it runs on the robot directly, with no laptop connection required once it is deployed.

## Why bother with a module

Reach for a module only when one of these is true for your setup:

- The cycle has to keep running after you close your laptop or walk away.
- The cycle has to restart on its own if it crashes or the robot reboots.
- You want to deploy an updated version to the robot without pushing code from a laptop by hand.
- You want the cycle to run on a schedule instead of a manual trigger.

If none of those apply, stop here. You have already built the thing this workshop set out to teach.

## Mostly packaging, plus one real change

Set expectations before you start: this phase should be considered a refactor. The detection, the frame transform, the pose math, and the motion calls are the same pick-and-place logic, moved into a module's lifecycle methods with no change to what they do.

One piece of that logic does genuinely change: how you reach `transform_pose`. In the previous phase, `transform_pose` was a method on the `machine` handle your script already held from `RobotClient.at_address`. The pattern for reaching `transform_pose` from inside a module is in [The frame system from inside a module](#the-frame-system-from-inside-a-module) below.

## Create a control code module

{{< alert title="Module build feedback loop" color="note" >}}
Before you start pasting code, know what to expect: saving an inline Python module triggers a cloud build, and that build takes about a minute. Give it that minute rather than assuming a save failed.
{{< /alert >}}

On the **CONFIGURE** tab, click the **+** icon and select **Code**. Choose to create a "Viam-hosted" module with an inline editor, proceed past the information about configuring components, and select Python as the language. The Viam app creates a new configured resource with an embedded code editor in your browser with a generated module skeleton.

<!-- ASSET P0 inline-module-editor (UI+): the inline module editor open in CONFIGURE with code pasted. See plans/2026-07-02-pick-and-place-shot-list.md -->

{{<imgproc src="/tutorials/pick-and-place/inline-module-editor.png" resize="1200x" declaredimensions=true alt="The inline module code editor open in CONFIGURE with the generated Python skeleton.">}}

Control code for adding application logic to a robot is typically modeled as a generic service: a resource class built on the Generic service API plus the `EasyResource` convenience mixin, whose `do_command` method is its entry point. Over the next three sections you move your pick-and-place code into this skeleton's lifecycle methods: the connection to typed resource handles becomes dependency injection, reaching `transform_pose` changes, and the detection, pose math, and motion calls gather behind a `do_command` entry point. Work through them in order; you save and build the module at the end, once the code is in place.

## Dependency injection

<!-- ASSET P1 diagram-script-vs-module (DIAGRAM): from_robot(...) vs new() attribute-named deps dependencies[Arm.get_resource_name(attrs["arm"])], resource names set once as config attributes, transform_pose via in-module RobotClient -->

```text
Script  (Phases 4 and 5)
  connect  →  RobotClient.at_address(...)
  arm      =  Arm.from_robot(machine, "arm-1")
  frames   =  machine.transform_pose(...)

Module  (Phase 6)   (same logic, different wiring)
  validate_config()   declares dependencies from the config attributes
  new(config, deps)   looks up each dependency by its configured name
  transform_pose      via an in-module RobotClient
```

A script builds its resource handles once, right after it connects, by calling `Arm.from_robot(machine, "arm-1")` and similar for each resource it needs. A module does not connect to itself, so it cannot call `from_robot` the same way. Instead, the module framework hands your module its dependencies.

Two lifecycle methods carry this pattern:

- `validate_config` runs before your module starts and declares which resources it depends on, so `viam-server` knows to hold your module back until those resources are online, the same dependency ordering you already saw between `gripper-1` and `arm-1` in Phase 2. It reads the module's own config attributes, where each attribute value is the name of a resource on the machine, and returns those names as the required dependencies.
- `new` receives the resolved dependencies as a mapping keyed by resource name, and this is where you build the typed handles your pick-and-place logic calls. `new` is the `EasyResource` classmethod that constructs your resource; it reads the same config attributes to look each dependency up by its configured name.

A small illustrative sketch of both methods:

```python
from viam.components.arm import Arm
from viam.utils import struct_to_dict


@classmethod
def validate_config(cls, config):
    attrs = struct_to_dict(config.attributes)
    required_deps = []
    if "arm" not in attrs or not attrs["arm"]:
        raise ValueError("attribute 'arm' (non-empty string) is required")
    required_deps.append(attrs["arm"])
    # ...same for gripper, camera, home_pose, travel_pose, place_pose, vision...
    required_deps.append("builtin")  # motion service
    return required_deps, []


@classmethod
def new(cls, config, dependencies):
    self = super().new(config, dependencies)
    attrs = struct_to_dict(config.attributes)
    self.arm = dependencies[Arm.get_resource_name(attrs["arm"])]
    # ...look up gripper, camera, the pose switches, and vision the same way...
    return self
```

Keep the rest of your `new` close to this shape: look up each resource your existing Python script used by its configured attribute name, and store it on `self` so your pick-and-place logic can call it later.

The motion service is injected the same way. `validate_config` declares it as `"builtin"`, and `new` retrieves it with `dependencies[Motion.get_resource_name("builtin")]` (from `viam.services.motion import Motion`), so `motion.move` works straight from the injected dependencies.

## The frame system from inside a module

<!-- ASSET P0 module-env-vars (UI+): module environment config with VIAM_API_KEY / VIAM_API_KEY_ID / VIAM_MACHINE_FQDN set, values REDACTED -->

This is the one genuine change from the Python script, so read it carefully even if you skim the rest of this phase.

No injected dependency gives you frame-system access the way `dependencies[Arm.get_resource_name(attrs["arm"])]` gives you the arm; there is no such dependency to inject. `transform_pose` lives on the machine-management API, and a module reaches that API the same way a script does: through a `RobotClient`. The difference is that a module has to build that `RobotClient` itself, from credentials in its own environment, rather than receiving one as a dependency.

Use this pattern exactly as written:

```python
import os
from viam.robot.client import RobotClient


async def create_robot_client_from_module():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["VIAM_API_KEY"],
        api_key_id=os.environ["VIAM_API_KEY_ID"],
    )
    return await RobotClient.at_address(os.environ["VIAM_MACHINE_FQDN"], opts)

# self.robot_client is initialized to None in new()
# in the upcoming do_command logic, create once and reuse:
if not self.robot_client:
    self.robot_client = await create_robot_client_from_module()
world_pose = await self.robot_client.transform_pose(obj_in_cam, "world")
```

Four rules go with this pattern:

- Create exactly one `RobotClient` and reuse it. Do not open a new connection on every `do_command` call or every pick cycle; check `self.robot_client` first, the same way the snippet does, and only connect if it is not already set.
- Do not hardcode the API key, key ID, or machine address in your module's code. They are automatically injected into the environment by `viam-server`.
- Close the connection on module shutdown by calling `await self.robot_client.close()` from an overridden `close` lifecycle method on your module (the companion `module-reference.py` demonstrates this), the same cleanup discipline you would apply to any open connection.
- Everything else your module needs (the arm, the gripper, the vision service, the pose switches) still comes through the injected dependencies described above.

See [Use the machine management API from a module](/build-modules/platform-apis/#use-the-machine-management-api-from-a-module) for the full reference on this pattern.

{{< alert title="Same resource names, different retrieval" color="note" >}}
Compare how you got the arm handle in the Python script against how you get it inside the module:

- Local script (Phases 4-5): `arm = Arm.from_robot(machine, "arm-1")`.
- Module: `arm = dependencies[Arm.get_resource_name(attrs["arm"])]`.

The resource name is still `"arm-1"` in both. In the module you set it once as the module's `arm` config attribute, which the operator points at `arm-1`, and `attrs["arm"]` reads it back. The same is true of the gripper, camera, every pose switch, and the vision service. Only the retrieval mechanism changes, from calling `from_robot` on a connected `machine` handle to looking the resource up in the `dependencies` mapping `new` received. `transform_pose` is the only resource access in this workshop that does not follow this pattern, for the reason described above.
{{< /alert >}}

## Trigger the module with do_command

With dependencies wired up and `transform_pose` reachable, assemble your pick-and-place logic into a single `run_pick_cycle` method on the module, the same detection, transform, pose math, and motion calls, unchanged. What differs is how that method gets triggered.

You trigger the module through `do_command`. Because a generic service has no typed API of its own, `do_command` is its entry point: the method you dispatch on to run the actions your service exposes. A small illustrative sketch:

```python
async def do_command(self, command, *, timeout=None, **kwargs):
    if command.get("action") == "pick_cycle":
        success = await self.run_pick_cycle()
        return {"success": success}
    return {}
```

With the code in place, save the module. The Viam app packages it and deploys it to the machine, and the **LOGS** tab shows the build progress the same way it showed module downloads back in Phase 2.

<!-- ASSET P1 logs-cloud-build (UI): LOGS showing the ~1 min cloud build + module start -->

{{<imgproc src="/tutorials/pick-and-place/logs-cloud-build.png" resize="1200x" declaredimensions=true alt="The LOGS tab showing the inline module cloud build.">}}

{{< checkpoint >}}
The module finishes its cloud build and starts without errors in the **LOGS** tab, and its resource shows online on the **CONFIGURE** tab. If the build fails, read the build log for the specific error; a missing import or a syntax error carried over from the script is the most common cause.
{{< /checkpoint >}}

From the **CONTROL** tab, find your module's test card and send a command such as `{"action": "pick_cycle"}` to run one full pick-and-place cycle on demand, the same cycle you watched run from your script, now running on the robot instead of your personal computer. To compare your module against a finished one, read the complete [`module-reference.py`](https://github.com/viam-devrel/pick-and-place/blob/main/scripts/module-reference.py) in the companion repo.

<!-- ASSET P1 control-do-command (UI+): triggering the do_command from the app -->

{{<imgproc src="/tutorials/pick-and-place/control-do-command.png" resize="1200x" declaredimensions=true alt="The module DoCommand test card running the pick_cycle action.">}}

{{< checkpoint >}}
Sending a `do_command` trigger runs one complete pick-and-place cycle: detection, transform, approach, grasp, travel, and place, ending with a block in the bin.
{{< /checkpoint >}}

## Where you landed

You now have the same pick-and-place loop running two ways: as a script you control from your personal computer, and as a module that keeps running on the robot. Head to the [wrap-up](/tutorials/pick-and-place/wrap-up/) to review everything you built and where to take it next.

{{< workshop-nav >}}
