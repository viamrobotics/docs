---
title: "Phase 4: Control the robot from Python"
linkTitle: "4. Control from Python"
type: "docs"
slug: "control-the-robot-from-python"
weight: 40
description: "Connect from your laptop and drive the saved static pick-and-place sequence from a Python script."
workshop: "pick-and-place"
toc_hide: true
phase: 4
phase_total: 6
time_estimate: "15 minutes"
prev: "/tutorials/pick-and-place/static-positions/"
next: "/tutorials/pick-and-place/perception-guided-picking/"
aliases:
  - /tutorials/pick-and-place/local-python-script/
languages: ["python"]
---

In this phase you write and run a Python script on your laptop that connects to the robot and executes the static pick-and-place sequence from Phase 3. This proves your connection, environment, and named positions work end to end before you add perception in Phase 5.

## Why a script before a module

Everything you did in Phase 3 happened by clicking test cards on the **CONTROL** tab. That is a fine way to verify hardware, but it does not scale: you cannot loop, branch on a sensor reading, or retry a failed grasp from a button. A local Python script gives you those things, plus fast iteration, a local debugger, and the ability to sprinkle in `print` statements wherever you need visibility into what the robot is doing.

A script is also the right starting point before you package anything as a module. A module has to satisfy a defined lifecycle and run inside `viam-server`, which makes it slower to iterate on and harder to debug. In Phase 6 you package this same logic as a module. For now, a script you run from your own terminal, that you can stop, edit, and rerun in seconds, is the faster path to a working pick-and-place loop.

This phase is worth the detour because of what it buys you. Every control you clicked in Phases 2 and 3 maps directly onto an SDK method: the arm card's joint sliders become `Arm` methods, **Grab** and **Open** on the gripper card become `gripper.grab()` and `gripper.open()`, and setting a switch to position 2 becomes `switch.set_position(2)`. Once you can call those methods from code, you can compose them into logic no UI card lets you express by clicking.

## Get the companion project

The workshop's companion repository, [viam-devrel/pick-and-place](https://github.com/viam-devrel/pick-and-place), has a `scripts/` project with a starter script already set up for this phase. Clone or download the repository, then work from the `scripts/` directory:

```sh
git clone https://github.com/viam-devrel/pick-and-place.git
cd pick-and-place/scripts
```

Your environment was already validated in the workshop prerequisites, so this phase is about connecting and running, not debugging Python installs. Run the starter script with `uv`, the primary path for this workshop:

```sh
uv run python starter-script.py
```

`uv` reads the project's `pyproject.toml` and `.python-version` and resolves `viam-sdk` for you automatically, so there is no separate install step. If you are not using `uv`, pip works as a fallback once you have installed the project's dependencies yourself:

```sh
pip install viam-sdk
python3 starter-script.py
```

## Connect to your robot

<!-- ASSET P0 connect-tab-boilerplate (UI+): CONNECT -> Python SDK, connection block highlighted, credentials REDACTED. See plans/2026-07-02-pick-and-place-shot-list.md -->

Open `starter-script.py` and find the `connect()` function. It mirrors the boilerplate the Viam app generates for you on the machine's **CONNECT** tab, under **Python SDK**:

```python
MACHINE_ADDRESS = "<paste from Connect tab>"
API_KEY = "<paste from Connect tab>"
API_KEY_ID = "<paste from Connect tab>"


async def connect() -> RobotClient:
    return await RobotClient.at_address(
        MACHINE_ADDRESS,
        options=RobotClient.Options.with_api_key(
            api_key=API_KEY,
            api_key_id=API_KEY_ID,
        ),
    )
```

Open the **CONNECT** tab on your machine's page in the Viam app, select **Python SDK**, and copy the three values it shows you: the machine address and an API key and key ID pair. Paste them into `MACHINE_ADDRESS`, `API_KEY`, and `API_KEY_ID` at the top of the script. You are reading and understanding this boilerplate rather than writing it from scratch, the same connection code every Viam Python script starts with.

{{< alert title="Handle your API key like a secret" color="note" >}}
Your API key grants control of the robot to anyone who has it. Do not commit it to version control. The companion repo's `.gitignore` already excludes the starter script's typical edit locations, but the safer pattern is to read the key from an environment variable instead of pasting it directly into the file, for example `API_KEY = os.environ["VIAM_API_KEY"]`.
{{< /alert >}}

## Get typed resource handles

After the connection opens, the script builds typed handles for each resource you drive in this phase:

```python
arm = Arm.from_robot(machine, "arm-1")
gripper = Gripper.from_robot(machine, "gripper-1")

home = Switch.from_robot(machine, "home-pose")
approach = Switch.from_robot(machine, "approach-pose")
grasp = Switch.from_robot(machine, "grasp-pose")
travel = Switch.from_robot(machine, "travel-pose")
place_pose = Switch.from_robot(machine, "place-pose")
```

Phase 4 drives only the arm, the gripper, and these pose switches. The starter script also declares two more handles right next to these: a `motion` handle for the `builtin` motion service, which always exists on a machine, and a `vision` handle for the `vision-segment` service. You do not configure `vision-segment` until Phase 5, and `VisionClient.from_robot` raises a `ResourceNotFoundError` when the service it names is not present. Because of that, the `vision = VisionClient.from_robot(...)` line must not run yet.

Before you run the script, make sure that line is not active. If it is uncommented, comment it out for now:

```python
# vision = VisionClient.from_robot(machine, "vision-segment")
```

You enable it in Phase 5 once the vision service exists. The `motion` handle is safe to leave as it is, since the `builtin` motion service is always present, but nothing in this phase calls it either.

## Run the script

<!-- ASSET P0 term-resource-names (TERM+): uv run output with resource_names printed; label arm-1/gripper-1/cam-1/pose switches/obstacle grippers -->

{{< alert title="The script moves the arm" color="caution" >}}
Running the script drives the arm through the full static sequence immediately after it prints the resource list. Clear the workspace and keep the e-stop within reach before you run it.
{{< /alert >}}

Run the script now with `uv run python starter-script.py`. It happens in a single run: `connect()` opens the connection, the script prints every resource on the machine, and then it immediately drives the arm through the static sequence. Watch the printed resource list scroll past in your terminal before the arm starts moving.

The first thing printed is the full resource list:

```python
print(machine.resource_names)
```

{{< checkpoint >}}
`machine.resource_names` prints a list that includes at least `arm-1`, `gripper-1`, and `cam-1`, the five poses (`home-pose`, `approach-pose`, `grasp-pose`, `travel-pose`, `place-pose`) as switches, and the three obstacles from Phase 3 as grippers. The list also contains the `builtin` motion service and other `erh:vmodutils` entries, so expect more names than just these. Seeing the obstacles listed as grippers is expected: the `erh:vmodutils:obstacle` model reuses the gripper API purely as a resource container for geometry.
{{< /checkpoint >}}

Right after the print, the script runs the static sequence. This is the same sequence you tested by hand from the **CONTROL** tab at the end of Phase 3, now expressed as code instead of button clicks. On a switch, `set_position(2)` executes the pose it has saved:

```python
await home.set_position(2)
await approach.set_position(2)
await gripper.open()
await grasp.set_position(2)
await gripper.grab()
await asyncio.sleep(0.3)  # finger gripper settle
await travel.set_position(2)
await place_pose.set_position(2)
await gripper.open()
await home.set_position(2)
```

The short sleep after `gripper.grab()` gives the finger gripper time to settle its grip on the block before the arm starts moving again; without it, the arm can begin the travel move before the fingers have finished closing.

Notice that nothing in this code mentions the table or the safety walls. The obstacles you configured in Phase 3 live in the machine config, not in this script, and the motion system applies them automatically wherever planning happens. There is no runtime `WorldState` to build or pass in here. In this static phase, movement comes entirely from the saved-pose switches, so obstacle-aware planning is not something you will see kick in yet; it becomes visible once Phase 5 introduces planned moves toward a detected block.

{{< checkpoint >}}
After the resource list prints, the same run drives the arm through the full sequence end to end: home, approach, open, grasp, grab, travel, place, open, home. The arm should complete every step without stopping, in the same order you validated manually in Phase 3.
{{< /checkpoint >}}

## Debugging guide

Most Phase 4 problems fall into one of a few categories:

- **`ResourceNotFoundError: vision-segment`** (or a similar not-found error for the vision service) means you tried to build the vision handle before configuring the vision service. That service is not added until Phase 5. Comment out the `vision = VisionClient.from_robot(...)` line for now, as described above, and rerun.
- **Connection failures.** If `connect()` raises an error or hangs, double-check the `MACHINE_ADDRESS`, `API_KEY`, and `API_KEY_ID` values against the **CONNECT** tab. A stale or mistyped API key produces an authentication error immediately; a wrong address usually times out instead. Also confirm the machine shows the green **Live** indicator in the Viam app. A machine that is not live cannot accept a connection no matter how correct your credentials are.
- **Resource-name mismatches.** If `Arm.from_robot(machine, "arm-1")` or a similar call raises a not-found error, the name in your script does not match the name on the **CONFIGURE** tab. Names are exact strings, not approximations, so `arm-1` and `arm_1` are different resources as far as the SDK is concerned. Open `resource_names` from the connection checkpoint above and compare it character for character against the names your script uses.
- **A switch does nothing on `set_position(2)`.** This means the pose was never saved. Go back to the **CONTROL** tab and set that switch to position 1 to save the current arm position, as you did in Phase 3, then rerun the script.

With `resource_names` printing everything you expect and the static sequence running end to end from your own code, you have working proof that your connection, your named resources, and your saved poses all hold up under real code, not just button clicks. In Phase 5 you replace the fixed `approach-pose` and `grasp-pose` in this sequence with positions computed from live perception, so the arm picks whichever block the camera actually detects instead of always reaching for the same spot.

{{< workshop-nav >}}
