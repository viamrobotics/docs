---
title: "Phase 6: Wrap the loop in a module"
linkTitle: "6. Inline module"
type: "docs"
slug: "inline-module"
weight: 60
description: "Wrap the working pack loop in an inline module so it runs on the machine and can be triggered through DoCommand."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 6
phase_total: 6
prev: "/tutorials/so-arm101-palletizing/avoid-placed-cubes/"
next: "/tutorials/so-arm101-palletizing/wrap-up/"
languages: ["python"]
---

This phase is optional. It takes the working pack loop from Phase 5 off your laptop and onto the machine, where it runs as a module and can be triggered on demand instead of from a script.

## Why use a module

A [module](/build-modules/) packages a resource so `viam-server` runs it directly, the same way the `so101` module you configured in Phase 2 runs the arm and gripper. Packaging your pack loop as a module puts your control code on that same footing.

Reach for a module when one of these is true for your setup:

- The pack has to keep running after you close your laptop.
- The pack has to restart on its own after a crash or a machine reboot.
- You want to deploy updates without pushing code from a laptop by hand.
- You want the pack to run on a schedule instead of a manual trigger.

If none of those apply, stop here. Phase 5 already gave you the complete robotics result this workshop set out to teach.

This phase builds an **inline module**: the Viam app hosts the code and builds it for you in the cloud, with the source in an editor in your browser. A conventional module lives in its own Git repository that you build and upload yourself, and it is the better choice for code you share across many machines or maintain as a team. Inline is the faster path for a single machine's control code, so it is what you use here.

## What changes when you package it

The pick, place, and pack logic from Phase 5 is unchanged, moved into a module's lifecycle methods with no change to what it does. Only the wiring around that logic changes, in two places:

- **How the module gets its resources.** Your script called `Gripper.from_robot`, `MotionClient.from_robot`, and read `helpers.ARM` after it connected. A module does not connect to itself, so it cannot call `from_robot` the same way; instead it receives its resources through **dependency injection**.
- **How the logic gets triggered.** Your script ran top to bottom under `__main__`, driven by the `STEPS` dictionary and a command-line verb. A module runs its logic behind a **`do_command`** entry point that something else calls, such as the CONTROL tab's test card.

The next three sections cover creating the module, then those two changes in turn.

## Create a control code module

On the **CONFIGURE** tab, click the **+** icon and select **Code**. Choose to create a Viam-hosted module with an inline editor, proceed past the information about configuring components, and select Python as the language. The Viam app creates a new configured resource with an embedded code editor in your browser, seeded with a generated module skeleton.

<!-- ASSET inline-module-editor (UI): inline module editor in CONFIGURE -->

Control code like this is typically modeled as a **generic service**: a resource with no specialized API of its own, so you can put arbitrary logic behind it. The skeleton builds that service on the `EasyResource` mixin, a convenience base class that fills in the boilerplate every resource needs and lets you override only the parts you care about. Those parts are **lifecycle methods**: functions the module framework calls at set points, such as `validate_config` when the config is checked, `new` when the resource starts, and `close` when it shuts down. One more method, `do_command`, is the generic service's entry point: because the service has no typed API, `do_command` is how a caller runs the actions it exposes.

Over the next two sections you move the pack loop into this skeleton: the typed resource handles you built with `from_robot` in Phase 4 become dependency injection through `new`, and `pick`, `place`, and `pack` gather behind the `do_command` entry point.

## Dependency injection

A script builds its resource handles once, right after it connects: `Gripper.from_robot(robot, helpers.GRIPPER)`, `MotionClient.from_robot(robot, helpers.MOTION)`, and `helpers.ARM` for the arm's name. A module works differently: it relies on `viam-server` to provide its dependencies to its constructor, which it declares through a configuration validation step. Two lifecycle methods carry this:

- `validate_config` runs before your module starts and declares which resources it depends on, so `viam-server` knows to hold your module back until those resources are online. It reads the module's own config attributes, where each attribute value is the name of a resource on the machine, and returns those names as required dependencies.
- `new` receives the resolved dependencies as a mapping keyed by resource name, and this is where you build the typed handles `pick`, `place`, and `pack` call. It reads the same config attributes to look each dependency up by its configured name.

The two anchor poses you taught by hand in Phase 3, staging and pallet origin, come in the same way: instead of reading `helpers.STAGING_POSE` and `helpers.PALLET_ORIGIN` from a Python file, the module reads them as config attributes.

A short illustrative sketch of both methods:

```python
from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.services.motion import Motion
from viam.utils import struct_to_dict


@classmethod
def validate_config(cls, config):
    attrs = struct_to_dict(config.attributes)
    required_deps = []
    for key in ("arm", "gripper"):
        if key not in attrs or not attrs[key]:
            raise ValueError(f"attribute '{key}' (non-empty string) is required")
        required_deps.append(attrs[key])
    required_deps.append("builtin")  # motion service
    return required_deps, []


@classmethod
def new(cls, config, dependencies):
    self = super().new(config, dependencies)
    attrs = struct_to_dict(config.attributes)
    self.arm = dependencies[Arm.get_resource_name(attrs["arm"])]
    self.gripper = dependencies[Gripper.get_resource_name(attrs["gripper"])]
    self.motion = dependencies[Motion.get_resource_name("builtin")]
    self.staging_pose = attrs["staging_pose"]
    self.pallet_origin = attrs["pallet_origin"]
    self.placed = []
    return self
```

This sketch is illustrative, not a complete file: fill in the pose attributes with however you choose to encode `x`, `y`, and `z` in the config (a small object with three numeric fields works well), and carry over `PITCH`, `CUBE`, `APPROACH`, and `GRASP_DEPTH` as module-level constants exactly as they were in `palletizer.py`.

## Trigger the module with do_command

With dependencies wired up, assemble the pack loop into a `run_pack` method on the module, using `self.arm`, `self.gripper`, and `self.motion` in place of the resource handles a script built with `from_robot`. The pick, place, and obstacle logic from Phase 5 carries over unchanged; only the resource handles and the pose source are different.

The Phase 5 `pack` loop paused on `input()` before each cycle so you could hand-feed a cube to the staging spot. A module runs on the machine with no attached terminal, so it cannot call `input()`. Drop the pause and let `run_pack` loop straight through all eight cells; unattended operation assumes something supplies cubes to the staging spot on its own, for example a feeder, which is out of scope for this workshop.

```python
    async def run_pack(self):
        """Pack both layers: eight cubes, cells 0 through 7. No hand-feed pause."""
        for seq in range(8):
            await self.pick()
            await self.place(seq)
        return len(self.placed)
```

One robustness note worth calling out: `self.gripper.grab()` returns a boolean, and on grippers that sense their grip it reports whether the jaws actually closed on something. The SO-101's finger gripper does not sense grip, so its `grab()` returns `True` on command completion whether or not a cube is there. If your gripper does report holding state, checking that return value before lifting lets a module catch a missed grasp instead of carrying an empty gripper through the place step; treat that hold-check as an enhancement to add when your hardware supports it, rather than something the SO-101 provides on its own.

You trigger the module through `do_command`. Because a generic service has no typed API of its own, `do_command` is its entry point: the method you dispatch on to run the actions your service exposes. A small illustrative sketch:

```python
async def do_command(self, command, *, timeout=None, **kwargs):
    if command.get("action") == "pack":
        count = await self.run_pack()
        return {"packed": count}
    return {}
```

{{< alert title="Module build feedback loop" color="note" >}}
Saving an inline Python module triggers a cloud build that takes about a minute. Give it that minute rather than assuming the save failed.
{{< /alert >}}

## Run the pack sequence

Save the module. The Viam app packages it and deploys it to the machine, and the **LOGS** tab shows the build progress the same way it showed the `so101` module downloading back in Phase 2.

<!-- ASSET logs-cloud-build (UI): the LOGS tab showing the inline module's ~1 minute cloud build and start -->

{{< checkpoint >}}
The module finishes its cloud build and starts without errors in the **LOGS** tab, and its resource shows online on the **CONFIGURE** tab. If the build fails, read the build log for the specific error; a missing import or a syntax error carried over from `palletizer.py` is the most common cause.
{{< /checkpoint >}}

From the **CONTROL** tab, find your module's test card and send `{"action": "pack"}` to run a full eight-cube pack on the machine, no laptop script required. To compare your module against a finished one, read the complete [`palletizer.py` reference](https://github.com/viam-devrel/mini-palletizer/blob/main/reference/palletizer.py) in the companion repo.

<!-- ASSET control-docommand-pack (UI+): the module test card with {"action": "pack"} entered, triggering a pack on the machine -->

{{< checkpoint >}}
Sending `{"action": "pack"}` from the test card runs the eight-cell pack loop on the machine, the same collision-free motion you drove from your laptop in Phase 5, now with no laptop in the loop and no hand-feed pause. If the command errors out partway through, check the LOGS tab for the raised exception, most likely a pose attribute that does not match what you taught in Phase 3, or the start-state collision from the held-cube geometry if you carried that over without a collision specification.
{{< /checkpoint >}}

{{< workshop-nav >}}
