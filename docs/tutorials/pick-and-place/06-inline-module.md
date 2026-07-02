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
languages: ["python"]
---

This phase is optional. Phase 5 already gave you a complete pick-and-place loop that runs from your own laptop: detection, the frame transform, planned motion, and a reliable place. This phase packages that same loop as a module so it runs on the robot directly, with no laptop connection required once it is deployed.

{{< workshop-phases >}}

## Why bother with a module

A script you run from your laptop is a complete result. It is not a lesser version of a module, and nothing about Phase 5 was a placeholder waiting for this phase to finish it. Reach for a module only when one of these is true for your setup:

- The cycle has to keep running after you close your laptop or walk away.
- The cycle has to restart on its own if it crashes or the robot reboots.
- You want to deploy an updated version to the robot without pushing code from a laptop by hand.
- You want the cycle to run on a schedule instead of a manual trigger.

If none of those apply, stop here. You have already built the thing this workshop set out to teach.

## Mostly packaging, plus one real change

Set expectations before you start: this phase is not a rewrite. The detection, the frame transform, the pose math, and the motion calls are the pick-and-place logic from Phase 5, moved into a module's lifecycle methods with no change to what they do.

One piece of that logic does genuinely change, and it is worth calling out up front so it does not surprise you partway through: how you reach `transform_pose`. In Phase 5, `transform_pose` was a method on the `machine` handle your script already held from `RobotClient.at_address`. A module does not automatically receive that same handle. The corrected pattern for reaching `transform_pose` from inside a module is in [The frame system from inside a module](#the-frame-system-from-inside-a-module) below. Everything else in this phase is packaging.

## Tier the scope

Two tiers, so you can stop at whichever one matches what you came here for:

- **A minimal viable module.** Repackage the Phase 5 logic into a module, and add a `do_command` handler you trigger by hand to run one pick-and-place cycle. This is the core path for the rest of this phase.
- **Level 2: scheduled and autonomous operation.** Once the minimal module runs a cycle on command, wiring it to a timer or a fully autonomous loop is a small additional step, covered briefly at the end of this phase as a low-effort on-ramp, not a requirement.

## Open the inline module editor

Before you start pasting code, know what to expect: saving an inline Python module triggers a cloud build, and that build takes about a minute. It is not instant the way rerunning a local script is, so give it that minute rather than assuming a save failed.

Open your machine's **CONFIGURE** tab and add a new module. Choose to create a local module with an inline editor rather than pulling one from the registry, and select Python as the language. The Viam app opens a code editor in your browser with a generated module skeleton, so there is no local project setup to do first.

Replace the skeleton's logic with your Phase 5 pick-and-place code: the connection to typed resource handles, the detection call, the frame transform, the pose math, and the motion calls, moved into the module's lifecycle methods as described below. Save the module. The Viam app packages your code and deploys it to the machine, and the **LOGS** tab shows the build progress the same way it showed module downloads back in Phase 2.

{{< checkpoint >}}
The module finishes its cloud build and starts without errors in the **LOGS** tab, and its resource shows online on the **CONFIGURE** tab. If the build fails, read the build log for the specific error; a missing import or a syntax error carried over from the script is the most common cause.
{{< /checkpoint >}}

## Dependency injection

A script builds its resource handles once, right after it connects, by calling `Arm.from_robot(machine, "arm-1")` and similar for each resource it needs. A module does not connect to itself, so it cannot call `from_robot` the same way. Instead, the module framework hands your module its dependencies.

Two lifecycle methods carry this pattern:

- `validate_config` runs before your module starts and declares which resources it depends on, so `viam-server` knows to hold your module back until those resources are online, the same dependency ordering you already saw between `gripper-1` and `arm-1` in Phase 2.
- `reconfigure` receives the resolved dependencies as a mapping keyed by resource name, and this is where you build the typed handles your pick-and-place logic calls.

A small illustrative sketch of that mapping, not a complete implementation:

```python
from typing import cast
from viam.components.arm import Arm

def reconfigure(self, config, dependencies):
    self.arm = cast(Arm, dependencies[Arm.get_resource_name("arm-1")])
```

Keep the rest of your `reconfigure` close to this shape: look up each resource your Phase 5 script used, cast it to its typed client, and store it on `self` so your pick-and-place logic can call it later.

## The frame system from inside a module

This is the one genuine change from Phase 5, so read it carefully even if you skim the rest of this phase.

No injected dependency gives you frame-system access the way `dependencies[Arm.get_resource_name("arm-1")]` gives you the arm; there is no such dependency to inject. `transform_pose` lives on the machine-management API, and a module reaches that API the same way a script does: through a `RobotClient`. The difference is that a module has to build that `RobotClient` itself, from credentials in its own environment, rather than receiving one as a dependency.

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

# self.robot_client is initialized to None in __init__/reconfigure
# in logic, create once and reuse:
if not self.robot_client:
    self.robot_client = await create_robot_client_from_module()
world_pose = await self.robot_client.transform_pose(obj_in_cam, "world")
```

Four rules go with this pattern:

- Create exactly one `RobotClient` and reuse it. Do not open a new connection on every `do_command` call or every pick cycle; check `self.robot_client` first, the same way the snippet does, and only connect if it is not already set.
- Do not hardcode the API key, key ID, or machine address in your module's code. The operator sets `VIAM_API_KEY`, `VIAM_API_KEY_ID`, and `VIAM_MACHINE_FQDN` as environment variables in the module's configuration on the machine; they are not automatically injected the way component dependencies are.
- Close the connection on module shutdown by calling `await self.robot_client.close()`, the same cleanup discipline you would apply to any open connection.
- Everything else your module needs (the arm, the gripper, the vision service, the pose switches) still comes through the injected dependencies described above. `transform_pose` is the one exception, reached through this in-module `RobotClient` instead.

See [Use the machine management API from a module](/build-modules/platform-apis/#use-the-machine-management-api-from-a-module) for the full reference on this pattern.

{{< alert title="Same resource names, different retrieval" color="note" >}}
Do not let the change above convince you that everything is different inside a module. It is not. Compare how you got the arm handle in Phase 4 against how you get it inside the module:

- Local script (Phases 4-5): `arm = Arm.from_robot(machine, "arm-1")`.
- Module: `arm = cast(Arm, dependencies[Arm.get_resource_name("arm-1")])`.

The resource name, `"arm-1"`, is identical in both, and the same is true of `gripper-1`, `cam-1`, every pose switch, and `vision-segment`. Only the retrieval mechanism changes, from calling `from_robot` on a connected `machine` handle to looking the resource up in the `dependencies` mapping `reconfigure` received. `transform_pose` is the only resource access in this workshop that does not follow this pattern, for the reason described above.
{{< /alert >}}

## do_command and a scheduled job

With dependencies wired up and `transform_pose` reachable, assemble your Phase 5 pick-and-place logic into a single method on the module, the same detection, transform, pose math, and motion calls, unchanged. What differs is how that method gets triggered.

For the minimal viable module, trigger it through `do_command`. `do_command` is a generic handler every module exposes for commands that do not fit the typed component or service APIs. A small illustrative sketch:

```python
async def do_command(self, command, *, timeout=None, **kwargs):
    if command.get("action") == "pick_cycle":
        success = await self.run_pick_cycle()
        return {"success": success}
    return {}
```

From the **CONTROL** tab, find your module's test card and send a command such as `{"action": "pick_cycle"}` to run one full pick-and-place cycle on demand, the same cycle you watched run from your script in Phase 5, now running on the robot instead of your laptop.

{{< checkpoint >}}
Sending a `do_command` trigger runs one complete pick-and-place cycle: detection, transform, approach, grasp, travel, and place, ending with a block in the bin. This is the same sequence from Phase 5's checkpoint, now triggered from the CONTROL tab instead of a script you ran locally.
{{< /checkpoint >}}

That manual trigger is the whole minimal viable module. Level 2 is wiring the same trigger to something other than your own hand: an internal loop that sleeps between cycles and calls `run_pick_cycle` on a cadence, or an external scheduler that sends the same `do_command` on a timer. Either approach reuses everything you already built in this phase; only the thing that calls `run_pick_cycle` changes, from a person on the CONTROL tab to a clock.

## Where you landed

You now have the same pick-and-place loop running two ways: as a script you control from your own laptop, and as a module that keeps running on the robot without one. Phase 5 gave you the complete win. This phase gave you the option to deploy it. There is no next phase; the workshop ends here.

{{< workshop-nav >}}
