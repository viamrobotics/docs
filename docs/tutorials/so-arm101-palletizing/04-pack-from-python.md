---
title: "Phase 4: Pack from Python"
linkTitle: "4. Pack from Python"
type: "docs"
slug: "pack-from-python"
weight: 40
description: "Build palletizer.py method by method and drive a static bottom-layer pack from your own code."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 4
phase_total: 6
prev: "/tutorials/so-arm101-palletizing/teach-the-cell/"
next: "/tutorials/so-arm101-palletizing/avoid-placed-cubes/"
languages: ["python"]
draft: true
---

In this phase you write `palletizer.py`, a Python script that reads back the two anchor poses from Phase 3 and drives the arm through a packing routine for each of the four bottom-layer cells. Getting through this phase is milestone one: you drive the arm through a static pack from your own code, on real hardware.

## Set up the companion project

Clone the workshop's companion repository and work from it for the rest of this phase:

```sh
git clone https://github.com/viam-devrel/mini-palletizer.git
cd mini-palletizer
```

The project ships with a `pyproject.toml`, so `uv run` resolves and installs the Viam Python SDK (software development kit) for you the first time you run any script in the directory. If you are not using `uv`, install `viam-sdk` yourself and use `python3` instead.

Open the machine's **CONNECT** tab in the Viam app, select **Python SDK**, toggle **Include API key**, and copy the machine address and the application programming interface (API) key and key ID pair it shows you. `helpers.py` reads these from constants near the top of the file; paste your own values in before you run anything.

Open `helpers.py` and set the two constants `STAGING_POSE` and `PALLET_ORIGIN` to the two poses you captured by hand in Phase 3. `palletizer.py` reads both from `helpers.py`, so this is where the numbers you recorded become the code's picking and stacking targets.

`helpers.py` is provided for you as part of the companion project. You write `palletizer.py` yourself in this phase, starting from an empty file in the same directory.

## What the helpers give you

Start from [helpers.py](https://github.com/viam-devrel/mini-palletizer/blob/main/helpers.py); import it rather than rewriting the connection and grid math. It gives you:

- `helpers.connect()`, an `async` function that returns a connected `RobotClient`.
- The arm's resource name (`helpers.ARM`), which you hand to the motion service, plus the gripper and motion-service names (`helpers.GRIPPER`, `helpers.MOTION`), which you pass to `from_robot`. All three name resources configured in Phase 2.
- `down_pose(x, y, z)`, which returns a `Pose` at that position with the tool pointing straight down.
- `helpers.grid(origin, pitch, cube)`, which expands one origin corner into the eight target poses of a two-layer, four-cell pallet (explained in the next section).
- `helpers.STAGING_POSE` and `helpers.PALLET_ORIGIN`, the two anchor poses you captured by hand in Phase 3.

`palletizer.py` imports these names and composes them into motion calls.

## The pallet grid

You captured one pallet corner in Phase 3. The other seven target poses follow from two constants: the center-to-center spacing between cells, and the cube's size, which sets the gap between the two stacked layers.

```python
PITCH = 30  # mm, center-to-center spacing between adjacent pallet cells
CUBE = 20  # mm, cube side length, and the z offset between layers
```

The four bottom-layer cells are the origin corner plus every combination of `0` and `PITCH` in x and y. The top layer repeats those four positions one `CUBE` higher in z, giving eight target poses in all: four on the pallet and four stacked directly on top.

<!-- ASSET grid-iso (DIAGRAM): isometric view of the 2x2x2 cube stack, cells 0-7, origin corner (cell 0) and the z + CUBE top layer labeled -->

{{<imgproc src="/tutorials/so-arm101-palletizing/grid-iso.png" resize="1200x" declaredimensions=true alt="Isometric view of the finished pallet: eight cubes stacked two layers of four at 30 mm pitch. The bottom layer holds cells 0 to 3 and the top layer holds cells 4 to 7, one cube height above. The origin corner, cell 0, is highlighted.">}}

`helpers.grid` builds that list of eight poses for you from the origin corner you captured:

```python
def grid(origin, pitch, cube):
    """Return the eight target poses for a two-layer, four-cell pallet,
    given the bottom-layer origin corner (cell [0, 0])."""
    bottom = [
        Pose(x=origin.x + dx, y=origin.y + dy, z=origin.z)
        for dx in (0, pitch)
        for dy in (0, pitch)
    ]
    top = [Pose(x=p.x, y=p.y, z=p.z + cube) for p in bottom]
    return bottom + top
```

These are positions only. You apply a straight-down tool orientation to each one with the `down_pose` helper before sending it to the motion service, which the `place` method does below.

The staging pose is not part of this grid. It stays a single fixed pose for the whole routine: you hand-feed one cube to that same spot at the start of every cycle, and the arm always picks from there.

## Build palletizer.py

Build the file up one method at a time. Each piece below is small enough to test on its own before you move to the next.

### The class and connection

Start with the imports, the constants this phase adds, and a `Palletizer` class that holds a motion client and a gripper handle:

```python
import asyncio
import sys

from viam.components.gripper import Gripper
from viam.services.motion import MotionClient
from viam.proto.common import Pose, PoseInFrame

import helpers
from helpers import down_pose

PITCH = 30  # mm, center-to-center spacing between adjacent pallet cells
CUBE = 20  # mm, cube side length, and the z offset between layers
APPROACH = 40  # mm, hover height above a pose before descending
GRASP_DEPTH = 5  # mm, how far the gripper descends past the cube top to close on it


class Palletizer:
    def __init__(self, robot):
        self.robot = robot
        self.motion = MotionClient.from_robot(robot, helpers.MOTION)
        self.gripper = Gripper.from_robot(robot, helpers.GRIPPER)
        self.placed = []
```

`PITCH` and `CUBE` are the constants from the pallet grid above. `APPROACH` and `GRASP_DEPTH` are new: `APPROACH` is how high above a target pose the arm hovers before descending, and `GRASP_DEPTH` is how far past a cube's top surface the gripper descends so its fingers close around the cube rather than skim its top. `self.placed` tracks which grid cells already hold a cube.

There is nothing to run yet. This class only sets up handles; the next method makes the first move.

### move_gripper

Every move in this workshop reduces to one call: hand the motion service a destination pose and let it plan a path to the arm's fingertip. Add this method to the `Palletizer` class:

```python
    async def move_gripper(self, pose: Pose):
        destination = PoseInFrame(reference_frame="world", pose=pose)
        await self.motion.move(
            component_name=helpers.ARM,
            destination=destination,
            world_state=None,
        )
```

Name the arm, `helpers.ARM`. The motion service drives the arm's end point, where the gripper mounts, to `pose`. The anchor poses you taught in Phase 3 were recorded at that same end point with the gripper's jaws in position, so replaying them returns the jaws to where you taught them. The gripper, attached to the arm in Phase 2, rides along, and the planner accounts for its shape. `world_state=None` because this phase has no obstacles to avoid yet; Phase 5 adds them.

Add a small `move` method to the same class to smoke-test this before building `pick` and `place`:

```python
    async def move(self):
        """Send the gripper to a safe pose, pointing straight down."""
        await self.move_gripper(down_pose(200, 0, 150))
```

You test this once `main` is in place, at the end of this section.

### pick

`pick` reads the fixed staging pose, hovers above it, descends onto the cube, closes the gripper, and lifts back clear. Add it to the `Palletizer` class:

```python
    async def pick(self):
        """Pick the cube waiting on the staging spot and lift it clear."""
        staging = helpers.STAGING_POSE
        hover = down_pose(staging.x, staging.y, staging.z + APPROACH)
        grasp = down_pose(staging.x, staging.y, staging.z - GRASP_DEPTH)
        await self.move_gripper(hover)
        await self.move_gripper(grasp)
        await self.gripper.grab()
        await self.move_gripper(hover)
```

The staging spot is a single fixed pose, and you hand-feed one cube to it before every call to `pick`. Hovering above the staging pose first, then descending straight down, keeps the approach vertical instead of dragging the gripper sideways into a cube that is already sitting there. Note the grasp target is `staging.z - GRASP_DEPTH`, a few millimeters below the taught height, so the fingers close around the cube rather than stopping level with its top.

{{< checkpoint >}}
Hand-feed a cube to the staging spot, then run `pick` on its own once `main` is wired up at the end of this section. The gripper hovers above the staging pose, descends, closes on the cube, and lifts it back to the hover height. If the fingers close on air, check that the cube is centered under `helpers.STAGING_POSE` and that `GRASP_DEPTH` is not so small that the fingers stop above the cube's top.
{{< /checkpoint >}}

### place

`place` takes a grid cell index and sets the held cube down at that cell. Add it to the `Palletizer` class:

```python
    async def place(self, seq: int):
        """Place the held cube into bottom-layer grid cell `seq`."""
        target = helpers.grid(helpers.PALLET_ORIGIN, PITCH, CUBE)[seq]
        hover = down_pose(target.x, target.y, target.z + APPROACH)
        await self.move_gripper(hover)
        await self.move_gripper(down_pose(target.x, target.y, target.z))
        await self.gripper.open()
        await self.move_gripper(hover)
        self.placed.append(target)
```

`helpers.grid` returns all eight target poses, bottom layer followed by top layer; `seq` indexes into that list, and this phase only ever passes `0` through `3`, the four bottom-layer cells. The hover-then-descend pattern mirrors `pick`: transit above the cell first, then lower straight down, so the cube does not drag across neighboring cells on its way in. Unlike `pick`, `place` releases at exactly `target.z`, the taught cell height, rather than pressing below it, so the cube rests on the pallet surface at the height you captured.

{{< checkpoint >}}
`place` takes a `seq` argument, so there is no standalone step for it in `STEPS` yet; you verify it as the first cycle of `pack`, in the next section. When you run `pack`, the first cube is lowered into grid cell 0 and released. The cube should land inside the marked cell, not on top of an edge or a neighboring cell. If it lands off-center, recheck the pallet origin pose you captured in Phase 3, or confirm `PITCH` and `CUBE` match your measured cube spacing.
{{< /checkpoint >}}

### Pack the bottom layer

With `pick` and `place` working individually, chain them into a loop that packs all four bottom-layer cells, pausing between cycles so you can hand-feed the next cube. Add this last method to the `Palletizer` class:

```python
    async def pack(self):
        """Pack the bottom layer: one cube per grid cell, cells 0 through 3."""
        for seq in range(4):
            input(f"Place a cube on the staging spot, then press Enter (cell {seq})... ")
            await self.pick()
            await self.place(seq)
        print(f"packed {len(self.placed)} cubes")
```

With the class complete, add the command-line plumbing at module level, outside the class, so `STEPS`, `main`, and the entry point sit at column 0:

```python
STEPS = {
    "move": Palletizer.move,
    "pick": Palletizer.pick,
    "pack": Palletizer.pack,
}


async def main(verb):
    robot = await helpers.connect()
    palletizer = Palletizer(robot)
    try:
        step = STEPS.get(verb)
        if step is None:
            print(f"unknown step '{verb}'. steps: {', '.join(STEPS)}")
            return
        await step(palletizer)
    finally:
        await robot.close()


if __name__ == "__main__":
    verb = sys.argv[1] if len(sys.argv) > 1 else "pack"
    asyncio.run(main(verb))
```

`STEPS` maps a command-line verb to a method, so you can run any single step by name instead of always running the whole pack. `pack` is the milestone-one path: it loops `seq` over the four bottom-layer cells, pausing for you to hand-feed a cube before each `pick`.

## Run it

Run each step with `uv run`, watching both the physical arm and the **3D scene** tab.

First, confirm the connection and a basic move:

```sh
uv run palletizer.py move
```

{{< checkpoint >}}
The gripper moves to a fixed pose, pointing straight down. If the script raises a connection error, recheck the machine address and API key in `helpers.py` against the CONNECT tab. If it raises a planning error, confirm `(200, 0, 150)` is inside your arm's reach; adjust the coordinates in `move` if your cell layout differs.
{{< /checkpoint >}}

Next, hand-feed one cube to the staging spot and run `pick`:

```sh
uv run palletizer.py pick
```

The arm should hover above the staging pose, descend, grab the cube, and lift it clear. Leave the cube held; you use it in the next step.

Now run the full bottom-layer pack:

```sh
uv run palletizer.py pack
```

The script prompts you before each cycle. Hand-feed a cube to the staging spot, press Enter, and watch the arm pick it up and set it into the next grid cell. After the first cycle, confirm the cube landed inside grid cell 0, not on top of an edge or a neighboring cell, before you continue to the remaining three.

{{< checkpoint >}}
After four cycles, `pack` prints `packed 4 cubes` and the bottom layer of the pallet is full: four cubes, one per cell, with no gaps or overlaps. This is milestone one.
{{< /checkpoint >}}

## Milestone one

You now drive the arm through a static pack from your own code: connect, read back the taught anchor poses, and run a pick-and-place cycle for each bottom-layer cell, with no obstacle avoidance yet. That is a complete, working result for this workshop. Phase 5 adds the second layer and teaches the motion service about the cubes already on the pallet, so it plans around them instead of through them.

{{< workshop-nav >}}
