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

This phase is optional. The previous phase already gave you a complete pick-and-place loop that runs from your own laptop: detection, planned motion, and a reliable place. This phase packages that same loop as a module so it runs on the robot directly, with no laptop connection required once it is deployed.

## Why use a module

A [module](/build-modules/) packages a resource so `viam-server` can run it directly, the same way the `ufactory` and `realsense` modules you added earlier run their drivers. Modules are the unit Viam shares and deploys: they live in a registry where they can be reused across machines, they carry versions so you can roll a deployment forward or back, and they build for each platform your fleet runs. Packaging your pick-and-place loop as a module puts your control code on that same footing as any driver.

For your own control code, reach for a module when one of these is true for your setup:

- The cycle has to keep running after you close your laptop or walk away.
- The cycle has to restart on its own if it crashes or the robot reboots.
- You want to deploy an updated version to the robot without pushing code from a laptop by hand.
- You want the cycle to run on a schedule instead of a manual trigger.

If none of those apply, stop here. You have already built the thing this workshop set out to teach.

This phase builds an **inline module**: the Viam app hosts the code and builds it for you in the cloud, with the source in an editor in your browser. A conventional module lives in its own Git repository that you build and upload yourself, and it is the better choice for code you share across many machines or maintain as a team. Inline is the faster path for a single machine's control code, so it is what you use here; everything you learn about the module lifecycle applies to both.

## What changes when you package it

The detection, the pose math, and the motion calls are the same pick-and-place logic, moved into a module's lifecycle methods with no change to what they do. Only the wiring around that logic changes, in two places:

- **How the module gets its resources.** A script calls `from_robot` after it connects; a module receives its resources through **dependency injection** instead.
- **How the logic gets triggered.** A script runs top to bottom under `__main__`; a module runs its logic behind a **`do_command`** entry point that something else calls.

The next two sections cover those two changes in turn.

## Create a control code module

On the **CONFIGURE** tab, click the **+** icon and select **Code**. Choose to create a "Viam-hosted" module with an inline editor, proceed past the information about configuring components, and select Python as the language. The Viam app creates a new configured resource with an embedded code editor in your browser with a generated module skeleton.

<!-- ASSET P0 inline-module-editor (UI+): the inline module editor open in CONFIGURE with code pasted. See plans/2026-07-02-pick-and-place-shot-list.md -->

{{<imgproc src="/tutorials/pick-and-place/inline-module-editor.png" resize="1200x" declaredimensions=true alt="The inline module code editor open in CONFIGURE with the generated Python skeleton.">}}

Control code like this is typically modeled as a **generic service**: a resource that exposes no specialized API of its own, so you can put arbitrary logic behind it. The skeleton builds that service on the `EasyResource` mixin, a convenience base class that fills in the boilerplate every resource needs and lets you override only the parts you care about. Those parts are **lifecycle methods**: functions the module framework calls at set points, such as `validate_config` when the config is checked, `new` when the resource starts, and `close` when it shuts down. One more method, **`do_command`**, is the generic service's entry point: because the service has no typed API, `do_command` is how a caller runs the actions it exposes.

Over the next two sections you move your pick-and-place code into this skeleton: the typed resource handles become dependency injection through `new`, and the detection, pose math, and motion calls gather behind the `do_command` entry point. Save and build the module at the end, once the code is in place.

## Dependency injection

The same resources reach your code differently in a script and in a module:

<!-- ASSET P1 diagram-script-vs-module (DIAGRAM): from_robot(...) vs new() attribute-named deps dependencies[Arm.get_resource_name(attrs["arm"])], resource names set once as config attributes -->

```text
Script  (Phases 4 and 5)
  connect  →  RobotClient.at_address(...)
  arm      =  Arm.from_robot(machine, "arm-1")

Module  (Phase 6)   (same logic, different wiring)
  validate_config()   declares dependencies from the config attributes
  new(config, deps)   looks up each dependency by its configured name
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

{{< alert title="Same resource names, different retrieval" color="note" >}}
Compare how you got the arm handle in the Python script against how you get it inside the module:

- Local script (Phases 4-5): `arm = Arm.from_robot(machine, "arm-1")`.
- Module: `arm = dependencies[Arm.get_resource_name(attrs["arm"])]`.

The resource name is still `"arm-1"` in both. In the module you set it once as the module's `arm` config attribute, which the operator points at `arm-1`, and `attrs["arm"]` reads it back. The same is true of the gripper, camera, every pose switch, the vision service, and the motion service. Only the retrieval mechanism changes, from calling `from_robot` on a connected `machine` handle to looking the resource up in the `dependencies` mapping `new` received.
{{< /alert >}}

## Trigger the module with do_command

With dependencies wired up, assemble your pick-and-place logic into a single `run_pick_cycle` method on the module, the same detection, pose math, and motion calls, unchanged. What differs is how that method gets triggered.

You trigger the module through `do_command`. Because a generic service has no typed API of its own, `do_command` is its entry point: the method you dispatch on to run the actions your service exposes. A small illustrative sketch:

```python
async def do_command(self, command, *, timeout=None, **kwargs):
    if command.get("action") == "pick_cycle":
        success = await self.run_pick_cycle()
        return {"success": success}
    return {}
```

{{< alert title="Module build feedback loop" color="note" >}}
Saving an inline Python module triggers a cloud build that takes about a minute. Give it that minute rather than assuming the save failed.
{{< /alert >}}

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
Sending a `do_command` trigger runs one complete pick-and-place cycle: detection, approach, grasp, travel, and place, ending with a block in the bin.
{{< /checkpoint >}}

## Where you landed

You now have the same pick-and-place loop running two ways: as a script you control from your personal computer, and as a module that keeps running on the robot. Head to the [wrap-up](/tutorials/pick-and-place/wrap-up/) to review everything you built and where to take it next.

{{< workshop-nav >}}
