---
title: "Phase 5: Avoid placed cubes"
linkTitle: "5. Avoid placed cubes"
type: "docs"
slug: "avoid-placed-cubes"
weight: 50
description: "Model placed cubes and the held cube in WorldState so the planner stacks the full two layers collision-free."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 5
phase_total: 6
prev: "/tutorials/so-arm101-palletizing/pack-from-python/"
next: "/tutorials/so-arm101-palletizing/inline-module/"
languages: ["python"]
draft: true
---

In this phase you teach the motion service about the cubes already on the pallet and the cube in the gripper, so it plans around them instead of through them. Finishing this phase is milestone two: a full, collision-free two-layer pack.

## Why the planner collides

The motion service only avoids what you hand it. Every call to `motion.move` takes a `world_state` argument, and the planner routes around exactly what that `world_state` describes, nothing more. In Phase 4, `move_gripper` always passed `world_state=None`, and that was fine: the bottom layer is flat, so nothing the arm carried or passed over could collide with anything else on the pallet.

The second layer breaks that assumption. To stack a cube in a top-layer cell, the arm and the cube in its gripper now travel over cubes already sitting in the bottom layer. If you keep passing `world_state=None`, the planner has no idea those cubes exist and plans a path straight through them, because as far as it knows, the space above the pallet is empty.

This is exactly the WorldState idea from [Phase 1](/tutorials/so-arm101-palletizing/platform-mental-model/#three-robotics-concepts-to-learn): obstacles are the things to avoid, and transforms are the things that move with the arm. This phase builds both kinds of WorldState content from `self.placed`, the list your `place` method already appends to. See [Obstacles and WorldState](/motion-planning/obstacles/) for the full reference.

## Model placed cubes as obstacles

Every pose in `self.placed` is a cube already sitting on the pallet. Turn each one into a `RectangularPrism` geometry the planner should avoid on the current move.

Replace the `viam.proto.common` import from Phase 4 with this expanded block; it re-lists `Pose` and `PoseInFrame` so there is no duplicate import line:

```python
from viam.proto.common import (
    Pose,
    PoseInFrame,
    WorldState,
    GeometriesInFrame,
    Geometry,
    RectangularPrism,
    Vector3,
    Transform,
)
```

Then add an `obstacles` method to the `Palletizer` class:

```python
    def obstacles(self, held=False):
        """Build the WorldState for this move: placed cubes as obstacles, and
        the carried cube as a transform that rides the gripper."""
        placed = [
            GeometriesInFrame(
                reference_frame="world",
                geometries=[
                    Geometry(
                        center=Pose(x=p.x, y=p.y, z=p.z, o_x=0, o_y=0, o_z=1, theta=0),
                        box=RectangularPrism(dims_mm=Vector3(x=CUBE, y=CUBE, z=CUBE)),
                        label=f"placed-{i}",
                    )
                ],
            )
            for i, p in enumerate(self.placed)
        ]
        transforms = []
        if held:
            transforms.append(
                Transform(
                    reference_frame="held-cube",
                    pose_in_observer_frame=PoseInFrame(
                        reference_frame=helpers.GRIPPER,
                        pose=Pose(x=0, y=0, z=CUBE / 2, o_x=0, o_y=0, o_z=1, theta=0),
                    ),
                    physical_object=Geometry(
                        center=Pose(x=0, y=0, z=0),
                        box=RectangularPrism(dims_mm=Vector3(x=CUBE, y=CUBE, z=CUBE)),
                        label="held-cube",
                    ),
                )
            )
        if not placed and not transforms:
            return None
        return WorldState(obstacles=placed, transforms=transforms)
```

Each placed cube becomes a cube-shaped box, `CUBE` millimeters on every side, in the `world` frame. Pay attention to `center`: a `Geometry`'s `center` pose is the middle of the box, not its base. `self.placed` stores the tool pose you released the cube at, the arm's end-point pose from Phase 3, so each box is centered on that same x, y, z. On real hardware, the true cube center sits a little off that point, roughly half the cube's height up; this phase keeps the math simple and treats it as close enough, but if the arm clips a placed cube's top edge, that is the first number to tune.

These obstacles exist only for the duration of one move. They are not something you add to the machine's static configuration, because they change every cycle as `self.placed` grows; a config obstacle is fixed, but a `world_state` argument is built fresh on every call. That is why `obstacles` is a method that reads `self.placed` live rather than a value computed once.

Update `move_gripper` to accept a `world_state` and forward it, replacing the hardcoded `None` from Phase 4:

```python
    async def move_gripper(self, pose: Pose, world_state=None):
        destination = PoseInFrame(reference_frame="world", pose=pose)
        await self.motion.move(
            component_name=helpers.ARM,
            destination=destination,
            world_state=world_state,
        )
```

`move_gripper` still defaults to no obstacles, so any call that does not pass a `world_state` behaves exactly as it did in Phase 4. The next two sections update `pick`, `place`, and `pack` to actually pass one.

## Model the held cube

`obstacles` also models the cube currently in the gripper, when you call it with `held=True`. Between a `pick` and the matching `place`, the cube in the gripper is not on the pallet, it moves wherever the arm moves. Modeling it as an obstacle in the `world` frame would be wrong: obstacles given in a component frame are resolved to world coordinates once, at the start of planning, and then stay fixed, so a "held" obstacle would not ride the gripper as the arm moves.

The carried cube belongs in `WorldState.transforms` instead, as a `Transform` whose parent frame is the gripper. A `Transform` adds a new frame to the planner's world for the duration of the move: `pose_in_observer_frame` names the parent frame (`helpers.GRIPPER`) and the pose of the new `held-cube` frame relative to it, and `physical_object` gives that frame a cube-shaped geometry for collision checking. Because the parent frame is the gripper, the new frame moves with the arm, so the planner tracks the carried cube through the whole motion instead of freezing it in place. This is the transform half of WorldState from Phase 1, and it is the same runtime attach pattern described in [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/). Placed cubes stay in `obstacles`; only the carried cube goes in `transforms`.

The offset `(0, 0, CUBE / 2)` in `pose_in_observer_frame` approximates the cube's center sitting just past the gripper's fingertips; like the placed-cube pose above, it is a reasonable starting guess, not a measured value, and you may need to nudge it on hardware if the carried cube's model does not line up with where it actually rides.

{{< alert title="If the first carry move fails on a collision" color="note" >}}
Because the held-cube geometry sits right at the gripper (`z=CUBE / 2`), the first move that passes `held=True` can fail with a "start state in collision" error: the cube geometry overlaps the gripper's own fingers at the start pose. That specific pair of shapes is allowed to touch, so you tell the planner to ignore it with a collision specification that names the gripper and the `held-cube` frame. See [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/) for that pattern; this draft leaves it out to keep the code short.
{{< /alert >}}

Passing `held=True` folds the carried cube into the same `WorldState` as the placed cubes, so a single `world_state` argument covers both: the obstacles already on the pallet, and the transform the gripper is carrying right now.

## Run the full two-layer pack

With `obstacles` in place, update `pick`, `place`, and `pack` to pass it, and extend the loop from four cubes to all eight:

```python
    async def pick(self):
        """Pick the cube waiting on the staging spot and lift it clear."""
        staging = helpers.STAGING_POSE
        hover = down_pose(staging.x, staging.y, staging.z + APPROACH)
        grasp = down_pose(staging.x, staging.y, staging.z - GRASP_DEPTH)
        await self.move_gripper(hover, self.obstacles())
        await self.move_gripper(grasp, self.obstacles())
        await self.gripper.grab()
        await self.move_gripper(hover, self.obstacles(held=True))

    async def place(self, seq: int):
        """Place the held cube into grid cell `seq`."""
        target = helpers.grid(helpers.PALLET_ORIGIN, PITCH, CUBE)[seq]
        hover = down_pose(target.x, target.y, target.z + APPROACH)
        await self.move_gripper(hover, self.obstacles(held=True))
        await self.move_gripper(down_pose(target.x, target.y, target.z), self.obstacles())
        await self.gripper.open()
        await self.move_gripper(hover, self.obstacles())
        self.placed.append(target)

    async def pack(self):
        """Pack both layers: eight cubes, cells 0 through 7."""
        for seq in range(8):
            input(f"Place a cube on the staging spot, then press Enter (cell {seq})... ")
            await self.pick()
            await self.place(seq)
        print(f"packed {len(self.placed)} cubes")
```

Look at where `held=True` shows up and where it does not. The last hover in `pick` and the first hover in `place` both carry the cube across open space toward or away from the pallet, so both pass `self.obstacles(held=True)`: the planner needs to know about the cube riding in the gripper while it is in transit. The final descent into an empty cell in `place`, and the lift straight back up afterward, drop the `held` flag and use `self.obstacles()` alone. By that point the cube is either about to be released or already released, so modeling it as still held would have the planner route around a cube that, from the planner's point of view, is about to overlap the cell it is being placed into. `self.placed.append(target)` still runs after the release, so the next cycle's `obstacles()` call sees this cube too.

Run the full pack:

```sh
uv run palletizer.py pack
```

Hand-feed a cube to the staging spot for each of the eight prompts, the same rhythm as Phase 4. Keep the **3D scene** tab open while it runs; each time `place` appends to `self.placed`, the next move's obstacles include one more cube, and you can watch the set of avoided geometries grow cell by cell as the pallet fills.

<!-- ASSET 3dscene-obstacles (UI): 3D scene showing placed-cube obstacles accumulating -->

{{< checkpoint >}}
After eight cycles, `pack` prints `packed 8 cubes` and both layers of the pallet are full, four cubes on the bottom and four stacked directly above them, with no collisions along the way. If the arm clips a placed cube, first confirm every call to `move_gripper` in `pick` and `place` passes a `world_state`, none should fall back to the `None` default; then confirm `self.placed.append(target)` runs after each successful `place`, so later cycles actually see the cubes placed before them.
{{< /checkpoint >}}

## Milestone two

You now drive a full, collision-free two-layer pack: eight cubes, planned around each other automatically because you model placed cubes as obstacles and the held cube as a transform on every move. That is the complete robotics result this workshop set out to teach. Phase 6 is optional: it takes this same pack loop off your laptop and runs it as a module on the machine itself.

{{< workshop-nav >}}
