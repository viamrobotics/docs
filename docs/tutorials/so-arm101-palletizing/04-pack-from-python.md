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
phase_total: 5
prev: "/tutorials/so-arm101-palletizing/teach-the-cell/"
next: "/tutorials/so-arm101-palletizing/avoid-placed-cubes/"
languages: ["python"]
---

In this phase you write `palletizer.py`, a Python script that uses the two anchor poses from Phase 3 to drive the arm through a packing routine for each of the four bottom-layer cells.

## Set up the companion project

Clone the workshop's companion repository and work from it for the rest of this phase:

```sh
git clone https://github.com/viam-devrel/mini-palletizer.git
cd mini-palletizer
```

The shell commands in this tutorial are designed to use [`uv`](https://docs.astral.sh/uv/). The project ships with a `pyproject.toml`, so `uv run` resolves and installs the Viam Python SDK (software development kit) for you the first time you run any script in the directory. If you are not using `uv`, install `viam-sdk` yourself and use `python3` instead.

[`helpers.py`](https://github.com/viam-devrel/mini-palletizer/blob/main/helpers.py) is provided for you as part of the companion project. You set five variables in this file for use in your procedural code.

First, open the machine's **CONNECT** tab in the Viam app, select **Python SDK**, toggle **Include API key**, and copy the machine address and the API key and key ID pair it shows you. Paste these values into `MACHINE_ADDRESS`, `API_KEY_ID`, and `API_KEY` in `helpers.py`.

Next, set the x, y, and z of the two constants `STAGING_POSE` and `PALLET_ORIGIN` to the two gripper poses you captured by hand in Phase 3. `palletizer.py` reads both from `helpers.py`, so this is where the numbers you recorded become the code's picking and stacking targets.

{{< alert color="note" >}}
`helpers.py` sets `ARM` and `GRIPPER` to `arm-1` and `gripper-1`, the names you gave these components in Phase 2. If you named yours differently, change these two values to match. `MOTION` should remain set to "builtin".
{{< /alert >}}

## What the helpers give you

You will import `helpers.py` to handle connection code and grid math. It gives you:

- `helpers.connect()`, an `async` function that returns a connected `RobotClient`.
- The component and service names, as plain strings: `helpers.GRIPPER`, which you pass both to the motion service and to `from_robot`; `helpers.MOTION`, the motion service; and `helpers.ARM`, for arm-level calls you do not need in this workshop.
- `down_pose(x, y, z)`, which returns a `Pose` at that position with the tool pointing straight down.
- `helpers.grid(origin, pitch, cube)`, which expands one origin corner into the eight target poses of a two-layer, four-cell pallet (explained in the next section).
- `helpers.STAGING_POSE` and `helpers.PALLET_ORIGIN`, the two anchor poses you captured by hand in Phase 3.

`palletizer.py` imports these names and composes them into motion calls.

{{< expand "Learn more about the grid helper" >}}

## The pallet grid

You captured one pallet corner in Phase 3. The other seven target poses follow from two constants: the center-to-center spacing between cells, and the cube's size, which sets the gap between the two stacked layers.

```python
PITCH = 30  # mm, center-to-center spacing between adjacent pallet cells
CUBE = 16  # mm, cube side length, and the z offset between layers
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

{{< /expand >}}

## Build palletizer.py

Create a file in the same directory called `palletizer.py`. Build the file up one method at a time. Each piece below is small enough to test on its own before you move to the next.

### The class and connection

Start with the imports, the constants needed in this phase, and a `Palletizer` class that holds a motion client and a gripper handle:

```python
import asyncio
import sys

from viam.components.gripper import Gripper
from viam.services.motion import MotionClient
from viam.proto.common import Pose, PoseInFrame

import helpers
from helpers import down_pose

PITCH = 30  # mm, center-to-center spacing between adjacent pallet cells
CUBE = 16  # mm, cube side length, and the z offset between layers
APPROACH = 40  # mm, hover height above a pose before descending
GRASP_DEPTH = 9  # mm, how far below the cube's top face the fingertips descend before closing
GRIP_PERCENTAGE = 20  # percentage, the gripper width that holds your cubes; start wide, calibrate down

class Palletizer:
    def __init__(self, robot):
        self.robot = robot
        self.motion = MotionClient.from_robot(robot, helpers.MOTION)
        self.gripper = Gripper.from_robot(robot, helpers.GRIPPER)
        self.placed = []
```

`PITCH` and `CUBE` are the constants for the pallet grid. `APPROACH` and `GRASP_DEPTH` are new: `APPROACH` is how high above a target pose the gripper hovers before descending, and `GRASP_DEPTH` is how far below a cube's top face the fingertips go before the jaws close on it. Your anchor poses put the fingertips level with a cube's top face, so every grasp and release descends `GRASP_DEPTH` below the taught height.

`GRASP_DEPTH` and `GRIP_PERCENTAGE` are calibration values that depend on your cubes and your arm, and you test and adjust both later in this phase. `GRIP_PERCENTAGE` starts deliberately wide: you narrow it until the jaws hold a cube, because gripping too tightly can overload the gripper servo.

`self.robot` accepts a connection to your Viam machine, provided by `helpers.py`. `self.motion` and `self.gripper` hold client objects for those aspects of your machine.

`self.placed` tracks which grid cells already hold a cube.

### Command line plumbing

Below the `Palletizer` class, add a `main` function you'll use to give your robot instructions from the command line.

```python
STEPS = {
    # Expose Palletizer methods as commands
}

async def main(verb):
    robot = await helpers.connect()
    palletizer = Palletizer(robot)
    try:
        step = STEPS.get(verb)
        if step is None:
            print(f"Unknown step '{verb}'. Steps: {', '.join(STEPS)}")
            return
        await step(palletizer)
    except BaseException:
        await robot.stop_all()
        raise
    finally:
        await robot.close()

if __name__ == "__main__":
    verb = sys.argv[1] if len(sys.argv) > 1 else "pack"
    asyncio.run(main(verb))
```

The `except` block is a safety net for later, once the arm is moving. If a step raises an error, or you press Ctrl+C to interrupt it, `robot.stop_all()` tells every component on the machine to stop before the script disconnects, because closing the connection is not guaranteed to halt a motion already in progress. `raise` then passes the error along, so you still see what went wrong. `BaseException` catches Ctrl+C as well as ordinary errors.

At this point, you can run the program to ensure your connection is correctly configured:

```shell
uv run palletizer.py
```

You should see the "Unknown step" message configured in `main`. If the script raises a connection error, recheck the machine address and API key in `helpers.py` against the CONNECT tab.

### move_gripper

Every arm motion in this workshop follows the same pattern: give the motion service a destination pose and let it plan a path to the destination. Add this method to the `Palletizer` class:

```python
    async def move_gripper(self, pose: Pose):
        destination = PoseInFrame(reference_frame="world", pose=pose)
        await self.motion.move(
            component_name=helpers.GRIPPER,
            destination=destination,
            world_state=None,
        )
```

The motion service moves the gripper, specifically the point between its fingertips, to the `pose` you provide, working out the arm joint motions needed to get it there. This is the same gripper frame you read your anchor poses in, so the taught numbers carry over unchanged. The planner also accounts for the gripper's shape. `world_state=None` because this phase has no obstacles to avoid yet; Phase 5 adds them.

Add a small `test` method to the class: scratch space you rewrite each time you want to try out a piece as you build it. Start it off with a pose returned from the `down_pose` helper:

```python
    async def test(self):
        """Scratch space for testing individual pieces as you build them."""
        await self.move_gripper(down_pose(160, 0, 60))
```

Add the method in `STEPS` to expose it in your command line plumbing:

```python
STEPS = {
    "test": Palletizer.test
}
```

And test it by providing "test" as an argument:

```shell
uv run palletizer.py test
```

{{< checkpoint >}}
You should see the arm move the gripper to a point 160mm in front of the base and 60mm above the table, pointing straight down. If it raises a planning error such as "zero IK solutions produced", the pose is out of reach. With the gripper pointing straight down, the SO-ARM101 can only reach a limited height, roughly 60 to 80mm above the table, so lower the z value before you change x or y.
{{< /checkpoint >}}

### grip_percentage

Viam's [gripper component API](https://docs.viam.com/reference/apis/components/gripper/) provides several commands as part of the gripper module. You can test `Open` and `Grab` from your gripper's **Control** card in the Viam app.

Packing a pallet tightly requires more precise gripper control. The module also enables the `do_command` method, which is used to communicate commands to a component outside of standard API functions. We can use `set_position` to open or close the gripper to a specific percentage.

Add a method to your class to accept a percentage, from 0 (fully closed) to 100 (fully open):

```python
    async def grip_percentage(self, percentage: float):
        await self.gripper.do_command({
                "command": "set_position",
                "percentage": percentage
            })
```

To test, replace the body of `test` with a call to `grip_percentage` and run the program again:

```python
    async def test(self):
        """Scratch space for testing individual pieces as you build them."""
        await self.grip_percentage(22)
```

```shell
uv run palletizer.py test
```

The SO-101's gripper servo can overload if commanded to grip a solid object more tightly than the space allows. Hold one of your cubes between the gripper jaws and adjust the value you provide to `grip_percentage` in small increments to determine the precise percentage needed to grip one of your cubes. You can also use `do_command` with the same JSON syntax directly from the gripper's test card in the Viam app.

Once you have determined the appropriate percentage, adjust the `GRIP_PERCENTAGE` constant in your program.

### pick

`pick` reads the fixed staging pose, then uses the `move_gripper` and `grip_percentage` methods to hover above it, descend onto the cube, close the gripper to the percentage you determined in the last step, and lift back clear. Add it to the `Palletizer` class:

```python
    async def pick(self):
        """Pick the cube waiting on the staging spot and lift it clear."""
        staging = helpers.STAGING_POSE
        hover = down_pose(staging.x, staging.y, staging.z + APPROACH)
        grasp = down_pose(staging.x, staging.y, staging.z - GRASP_DEPTH)
        await self.move_gripper(hover)
        await self.grip_percentage(GRIP_PERCENTAGE * 3) # open the gripper wider than the cube
        await self.move_gripper(grasp)
        await self.grip_percentage(GRIP_PERCENTAGE) # close the gripper on the cube
        await asyncio.sleep(.5)
        await self.move_gripper(hover)
```

The staging spot is a single fixed pose, and you hand-feed one cube to it before every call to `pick`. Note the grasp target is `staging.z - GRASP_DEPTH`: your staging pose puts the fingertips level with the cube's top face, so the grasp lowers them `GRASP_DEPTH` millimeters down the cube's sides before the jaws close.

Add "pick" to your list of command line arguments in `STEPS`:

```python
STEPS = {
    "test": Palletizer.test,
    "pick": Palletizer.pick
}
```

Place a cube on the staging spot, then run the program with the "pick" argument:

```shell
uv run palletizer.py pick
```

{{< checkpoint >}}
The gripper hovers above the staging pose, descends, closes on the cube, and lifts it back to the hover height. If the fingers close on air, check that the cube is centered under `helpers.STAGING_POSE`. If the jaws close too high on the cube, or the cube slips as it lifts, increase `GRASP_DEPTH` a millimeter at a time; if the grip is loose, lower `GRIP_PERCENTAGE` by one.
{{< /checkpoint >}}

### place

`place` takes a grid cell index and sets the held cube down at that cell. Add it to the `Palletizer` class:

```python
    async def place(self, seq: int):
        """Place the held cube into bottom-layer grid cell `seq`."""
        target = helpers.grid(helpers.PALLET_ORIGIN, PITCH, CUBE)[seq]
        hover = down_pose(target.x, target.y, target.z + APPROACH)
        await self.move_gripper(hover)
        await self.move_gripper(down_pose(target.x, target.y, target.z - GRASP_DEPTH))
        await self.grip_percentage(GRIP_PERCENTAGE + 2) # release the cube
        await self.move_gripper(hover)
        self.placed.append(target)
```

`helpers.grid` returns all eight target poses, bottom layer followed by top layer; `seq` indexes into that list. The hover-then-descend pattern mirrors `pick`: transit above the cell first, then lower straight down, so the cube does not drag across neighboring cells on its way in. The descent also mirrors `pick`'s depth: the cube was gripped `GRASP_DEPTH` below its top face, so releasing it at that same depth sets it down instead of dropping it. `self.placed` records each filled cell's pose; Phase 5 uses it.

{{< checkpoint >}}
`place` takes a `seq` argument, so there is no standalone step for it in `STEPS`; you verify it as the first cycle of `pack`, in the next section. When you run `pack`, the first cube is lowered into grid cell 0 and released. The cube should land inside the marked cell, not on top of an edge or a neighboring cell. If it lands off-center, recheck the pallet origin pose you captured in Phase 3, or confirm `PITCH` and `CUBE` match your measured cube spacing.
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

With the class complete, add "pack" to the command-line plumbing:

```python
STEPS = {
    "test": Palletizer.test,
    "pick": Palletizer.pick,
    "pack": Palletizer.pack,
}
```

## Run it

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
