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
---

In this phase you teach the motion service about the cubes already on the pallet and the cube in the gripper, so it plans around them instead of through them. Finishing this phase is milestone two: a full, collision-free two-layer pack.

## What the planner already knows

The motion service already knows about every component you configured with a frame. The arm and the gripper both went into the frame system in Phase 2, so the planner accounts for their shapes on every move without you doing anything. What it does not know about is anything you did not configure, like a cube sitting on the pallet. You add those per move, through the `world_state` argument to `motion.move`: the planner routes around exactly what that WorldState describes, and nothing more.

In Phase 4, `move_gripper` always passed `world_state=None`, and that was fine. The bottom layer is flat, so nothing the arm carried or passed over could collide with anything else on the pallet. The second layer changes that. To stack a cube in a top-layer cell, the arm and the cube in its gripper travel over cubes already sitting in the bottom layer. With `world_state=None`, the planner has no idea those cubes exist and plans a path straight through them.

This is the WorldState idea from [Phase 1](/tutorials/so-arm101-palletizing/platform-mental-model/#three-robotics-concepts-to-learn): obstacles are the things to avoid, and transforms are the things that move with the arm. This phase builds both from `self.placed`, the list your `place` method already appends to. See [Obstacles and WorldState](/motion-planning/obstacles/) for the full reference.

## Keeping track of obstacles

The planner reasons about collisions using **geometries**: simple shapes, a box, a sphere, or a capsule, that stand in for the volume a real object takes up. To keep the arm clear of a cube on the pallet, you describe that cube as a box geometry so the planner knows the space is occupied.

Every pose in `self.placed` is a cube already on the pallet. Turn each one into a box geometry, a `RectangularPrism`, that the planner should avoid on the current move. Replace the `viam.proto.common` import from Phase 4 with this expanded block:

```python
from viam.proto.common import (
    Pose,
    PoseInFrame,
    WorldState,
    GeometriesInFrame,
    Geometry,
    RectangularPrism,
    Vector3,
)
```

Then add an `obstacles` method to the `Palletizer` class:

```python
    def obstacles(self):
        """Build the WorldState of placed cubes for the planner to avoid."""
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
        return WorldState(obstacles=placed) if placed else None
```

Each placed cube becomes a box, `CUBE` millimeters on every side, in the `world` frame. A `Geometry`'s `center` is the middle of the box, and `self.placed` stores the tool pose you released each cube at, so each box is centered on that same x, y, z.

These obstacles exist only for the duration of one move. They are not something you add to the machine's static configuration, because they change every cycle as `self.placed` grows. An obstacle in your machine configuration is fixed: you would configure something like the table the arm sits on that way, once, because it never moves. The cubes are different, so `obstacles` is a method that reads `self.placed` live and builds a fresh `world_state` on every call.

Update `move_gripper` to accept and forward a `world_state`, replacing the hardcoded `None` from Phase 4:

```python
    async def move_gripper(self, pose: Pose, world_state=None):
        destination = PoseInFrame(reference_frame="world", pose=pose)
        await self.motion.move(
            component_name=helpers.ARM,
            destination=destination,
            world_state=world_state,
        )
```

`move_gripper` still defaults to no obstacles, so any call that does not pass a `world_state` behaves exactly as it did before.

{{< alert title="Approximate cube centers" color="note" >}}
Each placed-cube box is centered on the pose you released the cube at, which is the arm's end point, not the exact cube center. The two are close, within about half a cube height. If the arm clips the top edge of a placed cube, this offset is the first number to tune.
{{< /alert >}}

## Model the held cube

The `obstacles` method covers the cubes on the pallet, but not the cube in the gripper. Between a `pick` and the matching `place`, the carried cube is not on the pallet, it moves wherever the arm moves. Modeling it as a fixed `world` obstacle would be wrong: obstacles are resolved to world coordinates once, at the start of planning, and then stay put.

The carried cube belongs in `WorldState.transforms` instead. A `Transform` adds a new frame to the planner's world for the duration of a move, and because you parent that frame to the gripper, it moves with the arm. Add `Transform` to the import block, then extend `obstacles` to take a `held` flag:

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

In the `Transform`, `pose_in_observer_frame` names the parent frame (`helpers.GRIPPER`) and the pose of the new `held-cube` frame relative to it, and `physical_object` gives that frame a cube-shaped geometry for collision checking. Because the parent is the gripper, the new frame rides the arm, so the planner tracks the carried cube through the whole motion instead of freezing it in place. This is the transform half of WorldState from Phase 1, the same runtime attach pattern described in [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/). Placed cubes stay in `obstacles`; only the carried cube goes in `transforms`.

The offset `(0, 0, CUBE / 2)` places the cube just past the gripper's fingertips. Like the placed-cube center, it is a reasonable starting guess you may need to nudge.

{{< alert title="If the first carry move fails on a collision" color="note" >}}
Because the held-cube geometry sits right at the gripper (`z=CUBE / 2`), the first move that passes `held=True` can fail with a "start state in collision" error: the cube geometry overlaps the gripper's own fingers at the start pose. That pair of shapes is allowed to touch, so you tell the planner to ignore it with a collision specification that names the gripper and the `held-cube` frame. See [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/) for that pattern; this draft leaves it out to keep the code short.
{{< /alert >}}

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

Look at where `held=True` shows up and where it does not. The last hover in `pick` and the first hover in `place` both carry the cube across open space toward or away from the pallet, so both pass `self.obstacles(held=True)`: the planner needs to know about the cube riding in the gripper while it is in transit. The final descent into an empty cell in `place`, and the lift straight back up afterward, drop the `held` flag and use `self.obstacles()` alone. By that point the cube is either about to be released or already released, so modeling it as still held would have the planner route around a cube that is about to overlap the cell it is being placed into. `self.placed.append(target)` still runs after the release, so the next cycle's `obstacles()` call sees this cube too.

Run the full pack:

```sh
uv run palletizer.py pack
```

Hand-feed a cube to the staging spot for each of the eight prompts, the same rhythm as Phase 4. Keep the **3D scene** tab open while it runs; each time `place` appends to `self.placed`, the next move's obstacles include one more cube, and you can watch the set of avoided geometries grow cell by cell as the pallet fills.

<!-- ASSET 3dscene-obstacles (UI): 3D scene showing placed-cube obstacles accumulating -->
<!-- ASSET pack-two-layer (VIDEO): the full eight-cube two-layer pack running collision-free, the arm routing over placed cubes (milestone two hero) -->

{{< checkpoint >}}
After eight cycles, `pack` prints `packed 8 cubes` and both layers of the pallet are full, four cubes on the bottom and four stacked directly above them, with no collisions along the way. If the arm clips a placed cube, first confirm every call to `move_gripper` in `pick` and `place` passes a `world_state`, none should fall back to the `None` default; then confirm `self.placed.append(target)` runs after each successful `place`, so later cycles actually see the cubes placed before them.
{{< /checkpoint >}}

## Milestone two

You now drive a full, collision-free two-layer pack: eight cubes, planned around each other automatically because you model placed cubes as obstacles and the held cube as a transform on every move. That is the complete robotics result this workshop set out to teach. Phase 6 is optional: it takes this same pack loop off your laptop and runs it as a module on the machine itself.

{{< workshop-nav >}}
