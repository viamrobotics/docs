---
title: "Phase 5: Perception-guided picking"
linkTitle: "5. Perception-guided picking"
type: "docs"
slug: "perception-guided-picking"
weight: 50
description: "Add the vision pipeline and write the perception loop that detects a block, hands its camera-frame pose to the motion service, and picks it with motion planning."
workshop: "pick-and-place"
toc_hide: true
phase: 5
phase_total: 6
time_estimate: "22 minutes"
prev: "/tutorials/pick-and-place/control-the-robot-from-python/"
next: "/tutorials/pick-and-place/inline-module/"
languages: ["python"]
---

In this phase you replace the fixed approach and grasp poses with live data from the camera: a vision service detects a block in the camera's own frame, you convert that detection to the arm's static world frame, and the motion service plans a collision-free pick against it.

## Configure the vision pipeline

Perception here is a two-stage pipeline. A **detector** finds blocks in the camera's 2D color image and returns a labeled bounding box for each. A **segmenter** then takes those 2D boxes, pulls the matching depth points from the camera, and fuses each into a 3D object point cloud with a real-world position. A 2D detection alone cannot tell you how far away a block is or where it sits in space; the segmenter is what turns "a block-shaped region of pixels" into "a block at this point in three dimensions." You configure the two as separate vision services, wired so the segmenter depends on the detector.

### Add the shape detector

`shape-finder/detector` is a vision model that finds known block shapes in a color image and returns a labeled bounding box for each. On the **Configure** tab, click the **+** icon and select **Blocks**, search for `shape-finder`, select the `shape-finder/detector` model, and name it `shape-detector`. Set its one attribute:

```json
{
  "camera_name": "cam-1"
}
```

`camera_name` tells the detector which camera to read color frames from, and it is also a dependency: `shape-detector` cannot run until `cam-1` is online, the same dependency pattern you have already seen with `gripper-1` and `arm-1`.

<!-- ASSET P1 configure-vision-pipeline (UI): the shape-detector and vision-segment service configs -->

{{<imgproc src="/tutorials/pick-and-place/configure-vision-pipeline.png" resize="1200x" declaredimensions=true alt="The shape-detector vision service config with its camera_name attribute.">}}

### Add the segmenter

`detections-to-segments` reads a detector's output together with the camera's depth data and produces one point cloud per detection, each with an estimated size and 3D position. It is not a builtin: unlike the `builtin` motion service you meet later in this phase, this model does not ship inside `viam-server`; it comes from its own module, so saving this config triggers a new module download the same way `viam:ufactory` and `viam:realsense` did earlier in the workshop. Add it the same way you added the shape detector: click the **+** icon and select **Blocks**, search for `detections-to-segments`, select the `vision/detections-to-segments` result, and name it `vision-segment`. Set its attributes:

```json
{
  "detector_name": "shape-detector",
  "camera_name": "cam-1",
  "mean_k": 5,
  "sigma": 1.25
}
```

`detector_name` and `camera_name` are dependencies, so `vision-segment` waits for both `shape-detector` and `cam-1` before it starts. `mean_k` and `sigma` tune a statistical outlier filter that cleans up the depth points before fusion: `mean_k` is how many neighbors each point is compared against, and `sigma` is how far from the local average a point may sit before it is dropped as noise. The values here are sensible defaults; see [detections-to-segments](/reference/services/vision/detections-to-segments/) for the full attribute reference.

Save the config and open the **Control** tab. Find the `vision-segment` test card. You should see the detections coming from the `shape-detector` service and one or more segmented objects under the **Object point clouds** section after toggling **Show object point clouds**. Each segmented object is displayed as a small point cloud with a label matching the paired bounding-box detection, with estimated dimensions and 3D position from the perspective of the camera.

<!-- ASSET P0 control-vision-detections (UI+): Control vision card showing detected blocks with boxes + labels. See plans/2026-07-02-pick-and-place-shot-list.md -->

{{<imgproc src="/tutorials/pick-and-place/control-vision-detections.png" resize="1200x" declaredimensions=true alt="The shape-detector vision card showing a detected block with a bounding box and label.">}}

<!-- ASSET P1 control-vision-segment-object (UI): vision-segment Object point clouds view, one segmented object with dimensions and position -->

{{<imgproc src="/tutorials/pick-and-place/control-vision-segment-object.png" resize="1200x" declaredimensions=true alt="A vision-segment object point cloud labeled square-red (box) with its estimated dimensions and 3D position in the camera frame.">}}

{{< checkpoint >}}
The `vision-segment` test card returns at least one object when a block is in view. If it returns nothing, confirm a block actually sits in the camera's field of view, then check the `shape-detector` card on its own: if that also returns nothing, the problem is upstream in shape detection.
{{< /checkpoint >}}

With the service live, go back to `starter-script.py` and uncomment the `vision` handle, the line marked `# Used in Phase 5` that you left commented in Phase 4:

```python
vision = VisionClient.from_robot(machine, "vision-segment")
```

## Let the motion service place the gripper

Every pose that `vision-segment` returns is expressed in the `cam-1` frame. That is the only frame the vision service knows about: it looked at pixels and depth values coming out of one camera, so the coordinates it hands back describe where a block sits relative to that camera's own origin and orientation.

The pick uses the **motion service** to move the arm to that block. You never configured it: the motion service is one of a handful of services the RDK builds into `viam-server` itself, so it is present on every machine under the reserved name `builtin`, which is why `builtin` appeared in `machine.resource_names` even though there is no motion component on the **Configure** tab to point at. This `builtin` is the same concept from [Phase 1](/tutorials/pick-and-place/platform-mental-model/#builtin-resources-and-modules): a `rdk` namespace model that ships inside `viam-server` and needs no module download, unlike `vision-segment`. Uncomment its handle in the script, the same way you uncommented the vision handle earlier in this phase:

```python
motion = MotionClient.from_robot(machine, "builtin")
```

`motion.move` takes a `PoseInFrame`: a `Pose` paired with the name of the frame it is expressed in. For a single move issued right after detection, you can tag the destination `reference_frame="cam-1"` and the motion service will walk the frame graph for you, the same graph you watched move in the **3D scene** tab when the `cam-1` frame swung with the arm as you jogged joint 1. It knows the camera's offset from the wrist, the wrist's offset from the next joint, and so on down to the arm's base at the world origin.

That works for one move, but here the arm works through two moves: approach and grasp, both built from the same detection. `cam-1` is wrist-mounted, so it moves the instant the arm does, and `motion.move` resolves a `cam-1`-tagged destination against wherever `cam-1` actually is _at the moment that specific call runs_, not where it was when you computed the pose. The first move to approach pose is fine, since the arm hasn't left `home-pose` yet. But by the second move, the arm has already traveled to the approach standoff, so `cam-1` is no longer where it was during detection. Reusing a `cam-1`-tagged pose there resolves it against the camera's new position instead of the one the offset math assumed, and the grasp drives to the wrong place. [Converting to world before you move](#convert-to-world-before-you-move), later in this phase, is how you avoid that trap.

<!-- ASSET P0 diagram-frame-transform (DIAGRAM): wrist camera on the arm; block pose reported in cam-1, transform_pose converts once to world -->

```text
Frame tree (rooted at world):

One block, fixed on the table
        │
        ├─ read from an unfixed / unknown arm pose
        │     cam-1 frame depends on the arm pose
        │     → motion.move resolves cam-1 to a different spot each time  (unreliable)
        │
        ├─ read from home-pose (a known position)
        │     cam-1 frame is in a known, repeatable place
        │     → motion.move always resolves cam-1 the same way on the first move   (reliable for first move)
        │
        └─ read from world (fixed position)
              block is in a known, repeatable place
              → motion.move does not rely on cam-1 position (reliable for subsequent moves)
```

It also matters exactly what `motion.move` moves. Two motions that sound similar are not the same thing:

- The **Control** tab's arm card, and a direct `Arm` method, move the arm's own end frame: the flange at the end of the last joint.
- `motion.move(component_name="gripper-1", ...)` moves the `gripper-1` frame instead: the gripper's tool center point (TCP), which sits further down the kinematic chain because the gripper is bolted on past the arm's end.

A `motion.move` call names that component and a goal pose tagged with its reference frame:

```python
await motion.move(
    component_name="gripper-1",
    destination=PoseInFrame(reference_frame="world", pose=target_pose),
)
```

Because you move `gripper-1`, every offset you compute later is measured to where you want the gripper's TCP to end up, not the arm's end. Keep that distinction in mind or the offset math will not make sense.

{{< alert title="Seeing a pose in world coordinates" color="note" >}}
You will use `RobotClient.transform_pose` below to convert `approach_pose` and `grasp_pose` to `world`. The same call works on any `PoseInFrame`, so you can also reach for it any time you want to eyeball a raw detection by eye: `world_pose = await machine.transform_pose(PoseInFrame(reference_frame="cam-1", pose=geometry.center), "world")` returns the block's center in `world`, where a `z` near the table surface and `x`/`y` over the table confirm the detection landed where you expect.
{{< /alert >}}

## Detect from home (the wrist-camera rule)

<!-- ASSET P0 diagram-detect-from-home (DIAGRAM): same block, two arm poses, two different world answers -->

```text
One block, fixed on the table
        │
        ├─ read from an unfixed / unknown arm pose
        │     cam-1 frame depends on the arm pose
        │     → motion.move resolves cam-1 to a different spot each time  (unreliable)
        │
        └─ read from home-pose (a known position)
              cam-1 frame is in a known, repeatable place
              → motion.move resolves cam-1 the same way every time        (reliable)
```

The `home-pose` provides a good view of the workspace for the camera to detect objects to be picked up by the arm. Each pick-and-place cycle, the arm moves to the home pose and the `shape-detector` looks for known shapes. If it has detections, it provides them to the `vision-segment` service, which you query with `vision.get_object_point_clouds`. In your script, comment out the `await approach.set_position(2)` and `await grasp.set_position(2)` lines from Phase 4. You replace them with the block below, which detects the block and computes its pose instead of replaying a fixed one:

```python
# Observe from home so the wrist-mounted camera frame is in a known position.
await home.set_position(2)

objects = await vision.get_object_point_clouds("cam-1")
if not objects:
    print("No objects detected")
    return False

# Largest object by point count. Use len(point_cloud).
obj = max(objects, key=lambda o: len(o.point_cloud))
geometry = obj.geometries.geometries[0]
label = geometry.label
print(f"Detected: {label}")

# The detected pose is already in the cam-1 frame; hand it to motion.move as-is.
obj_in_cam = PoseInFrame(reference_frame="cam-1", pose=geometry.center)
```

`get_object_point_clouds` returns one entry per object `vision-segment` fused together, each carrying its own point cloud and geometry. A workspace with several blocks in view returns several entries, so you need a rule for which one to pick this cycle. `max(objects, key=lambda o: len(o.point_cloud))` picks the object with the largest point cloud, ordinarily the block closest to the camera or most fully in view. Each `point_cloud` is the object's pointcloud data (PCD) stored as raw bytes, so `len(o.point_cloud)` measures its encoded size in bytes; that grows with the number of points, which makes it a reliable proxy for object size.

Add a `print(obj_in_cam.pose)` line right after `obj_in_cam` is set, and run the script. Watch the x, y, and z values it prints as you move a block around the table. Once the values look right, comment out or delete that print line before continuing to the next section: you are about to compute `approach_pose` and `grasp_pose` from `obj_in_cam.pose`, and the print statement was only there to sanity-check the raw detection.

{{< checkpoint >}}
`obj_in_cam.pose` prints coordinates in the camera's own frame: a `z` of roughly the camera-to-block distance, a few hundred millimeters, with small `x`/`y` values near the optical center. To check the detection against the workspace instead, use the `transform_pose` tip above to print the pose in `world`. If the numbers look wrong, the most common cause is a detection that was not taken from `home-pose`. Confirm the arm returns to `home-pose` (the `await home.set_position(2)` call) before every `get_object_point_clouds` call.
{{< /checkpoint >}}

## Compute the approach and grasp poses

<!-- ASSET P0 diagram-approach-grasp-offsets (DIAGRAM): block center in cam-1; approach -100mm toward camera; grasp = gripper-1 TCP one gripper-length (-60mm) toward camera; gripper-1 TCP vs arm end -->

{{<imgproc src="/tutorials/pick-and-place/diagram-approach-grasp-offsets.png" resize="1200x" declaredimensions=true alt="Isometric diagram of the cam-1 frame: along the camera z-axis, the approach pose sits -100 mm toward the camera and the grasp pose (the gripper-1 TCP) -60 mm above the block center at obj_in_cam.pose. -z points toward the camera and +z into the scene.">}}

Both offsets are applied to `obj_in_cam.pose`, the block center in the `cam-1` frame. In the camera frame, `+z` points out of the lens into the scene, so moving toward the camera, up and away from the block, is a negative `z` offset.

Because you observe from `home-pose` every cycle, the wrist camera looks down at the workspace from the same angle each time, so its depth axis stays roughly vertical and a `z` offset moves the target up and down as you would expect. This is one more reason the detect-from-home rule matters: it keeps the frame you are offsetting in a known orientation.

The vision service hands you the block's center, `obj_in_cam.pose`, but that is not where you send the gripper: driving its TCP to the center would sink the fingers straight through the block. Instead you derive two targets from that center, a standoff to approach from and a grasp point where the fingers close, by shifting it along `z`. The workshop's `offset_pose` helper does exactly that, moving a pose in `z` while leaving `x`, `y`, and orientation untouched:

```python
def offset_pose(pose: Pose, z_offset_mm: float) -> Pose:
    """Raise or lower a pose in z while keeping x/y/orientation fixed."""
    return Pose(
        x=pose.x,
        y=pose.y,
        z=pose.z + z_offset_mm,
        o_x=pose.o_x,
        o_y=pose.o_y,
        o_z=pose.o_z,
        theta=pose.theta,
    )
```

Shifting a detected center toward the camera looks like this:

```python
# obj_in_cam.pose.z is the block center, say 387 mm from the camera
standoff = offset_pose(obj_in_cam.pose, -50)
# standoff.z is now 337 mm: same x and y, 50 mm nearer the camera
```

The approach and grasp poses below apply this same shift with the offsets tuned for this gripper.

The approach pose is a standoff directly above the block, high enough that the gripper can descend onto it without first colliding with it sideways. That offset (APPROACH_MM / 100 mm) is provided here:

```python
approach_pose = offset_pose(obj_in_cam.pose, APPROACH_MM)
```

Applied to `obj_in_cam.pose`, the block's bounding-box center, this places the standoff 100 mm toward the camera from the block: enough clearance for the gripper to descend cleanly, with room to spare for a small pose error.

Now compute the grasp pose yourself. At the block you want the gripper's fingertips, not its TCP: the fingers have to close around the block. `motion.move` drives the `gripper-1` TCP, which sits one gripper-length back from the fingertip contact point, so to land the fingertips on the block center you stop the TCP one gripper-length short of it, toward the camera. That single offset is all you add, because `motion.move` is already driving the gripper's TCP rather than the arm's end. Work out the offset, including its sign, before expanding the answer below.

{{< expand "Reveal the grasp offset" >}}
The offset is `GRIPPER_LENGTH_MM`, the depth from the gripper's TCP out to its fingertip contact point:

```python
grasp_pose = offset_pose(obj_in_cam.pose, GRIPPER_LENGTH_MM)
```

`GRIPPER_LENGTH_MM` is `-60`. If you used `APPROACH_MM` here by mistake, the gripper stops well short of the block instead of at it; if you used zero, you would drive the TCP itself to the block center, sinking the fingers a full gripper-length past the block instead of closing them around it.
{{< /expand >}}

{{< checkpoint >}}
Before wiring up the moves, print `approach_pose` and `grasp_pose` and compare their `z` to `obj_in_cam.pose.z`: the approach `z` should sit about 100 mm toward the camera and the grasp `z` about 60 mm toward it. If either offset went the wrong way, the pick drives into or well short of the block, so fix the sign before running a move.
{{< /checkpoint >}}

## Convert to world before you move

`approach_pose` and `grasp_pose` are still expressed in the `cam-1` frame. As covered above, that frame is only trustworthy for a move issued before the arm leaves the pose the detection was taken from, and this pick issues two moves from one detection: approach, then grasp. By the second move the arm has already traveled to the approach standoff, carrying `cam-1` with it, so a `cam-1`-tagged grasp pose would resolve against the camera's new position rather than the one the offset math assumed.

`world` fixes this: it is anchored at the arm's base and never moves, no matter where the arm travels afterward. Convert both poses to `world` once, right here, while the arm is still at `home-pose` and `cam-1` is where the detection assumed it was:

```python
approach_in_world = await machine.transform_pose(
    PoseInFrame(reference_frame="cam-1", pose=approach_pose), "world"
)
grasp_in_world = await machine.transform_pose(
    PoseInFrame(reference_frame="cam-1", pose=grasp_pose), "world"
)
```

`transform_pose` returns a `PoseInFrame` already tagged `reference_frame="world"`, so `approach_in_world` and `grasp_in_world` are ready to hand to `motion.move` as-is, and they stay valid for the rest of the cycle no matter how many moves the arm makes in between.

## Run the full pick loop

<!-- ASSET P0 perception-pick (MOTION): full detect -> approach -> descend -> grab -> place cycle (milestone-two hero asset) -->

With `approach_in_world` and `grasp_in_world` computed, assemble the full cycle:

```python
await motion.move(
    component_name="gripper-1",
    destination=approach_in_world,
)
await gripper.open()
await motion.move(
    component_name="gripper-1",
    destination=grasp_in_world,
)
await gripper.grab()
await asyncio.sleep(0.3)  # finger gripper settle
await travel.set_position(2)
await place_pose.set_position(2)
await gripper.open()
await home.set_position(2)
```

This cycle picks with `motion.move` and places with the saved-pose switches from Phase 3. The pick target moves every cycle, so it needs the Cartesian precision and obstacle-aware planning that `motion.move` provides against a freshly computed grasp pose. The place target never moves: it is the same bin in the same spot every time. The saved-pose switch replays fixed joint positions directly, without invoking the motion planner, so for a target that never changes it is simpler and just as reliable as planning a fresh path each cycle.

{{< alert title="The arm moves under code control" color="caution" >}}
This loop drives the arm to a computed grasp pose with `motion.move` and replays saved poses, all from your script. Keep the workspace clear and the e-stop within reach, and run it the first few times ready to stop the arm if a computed pose looks wrong.
{{< /alert >}}

Run the script and watch the sequence come together in three stages.

First, the approach move lifts the gripper to the standoff above the detected block:

{{< checkpoint >}}
The approach move completes without a planning error, positioning the gripper above the block. If it fails here, open the **3D scene** tab during the next run and check whether `approach_pose` lands inside the table or safety-wall geometry; a block detected very close to a boundary can push the arm outside the planner's reachable space.
{{< /checkpoint >}}

Next, the grasp move descends onto the block and the gripper closes:

{{< checkpoint >}}
The grasp move completes and **Grab** closes the fingers around the block, holding it through the lift into `travel-pose`. If the gripper closes on empty air, the block likely shifted between detection and grasp, or the grasp offset is off; revisit the offset math above.
{{< /checkpoint >}}

Finally, the place and return steps carry the block to the bin and send the arm home:

{{< checkpoint >}}
The full loop runs end to end: approach, open, grasp, grab, travel, place, open, home, with the block landing in the bin. This is the same sequence you drove by hand in the UI and by fixed poses in the initial Python script, now driven by a pose your code computed from a live detection.
{{< /checkpoint >}}

## Debugging guide

<!-- ASSET P1 3dscene-planned-path (UI): 3D scene during a move, arm path relative to the Phase 3 obstacles -->

Work through these in order. The first one causes most of the rest. If you get stuck, compare your loop against the complete [`reference-solution.py`](https://github.com/viam-devrel/pick-and-place/blob/main/scripts/reference-solution.py) in the companion repo.

- **Did you detect from `home-pose`?** This is the first thing to check for nearly every perception symptom below. If the `await home.set_position(2)` guard is missing before a `get_object_point_clouds` call, or if you added a second detection somewhere that skips it, every downstream pose is computed against the wrong camera position.
- **No objects detected.** Open the **Control** tab and run the `vision-segment` card by hand while a block sits in view. If that also returns nothing, check the `shape-detector` card on its own: a detector that finds nothing means the block is out of frame, or lighting has changed enough to affect the shape detection. If `shape-detector` finds the block but `vision-segment` does not, check that a block is close enough and clearly separated from the table surface for the depth fusion step to segment it.
- **The pick point drifts from cycle to cycle, even for a block that has not moved.** This is almost always the wrist-camera rule again: some code path is detecting from a pose other than `home-pose`. Print `obj_in_cam.pose` on every cycle and confirm the arm is fully settled at `home-pose` before each detection call.
- **Motion planning fails, or the target looks unreachable.** Open the **3D scene** tab during the failing move and look at where `approach_pose` or `grasp_pose` lands relative to the table and safety-wall geometry from Phase 3. A detected pose near a workspace boundary can place the standoff or the grasp point outside the region the planner is allowed to move through. If you skipped or under-measured the obstacle configuration in Phase 3, this is where it bites: geometry that does not match your physical setup makes the planner reject moves that are perfectly safe, or, worse, accept ones that are not. Revisit [Teach the planner about obstacles](/tutorials/pick-and-place/static-positions/#teach-the-planner-about-obstacles) and recheck your measurements before assuming the pose math is wrong.
- **The grasp move plans past the block and heads into the table.** This is the signature of resolving a chained move against a stale frame: the planner reports IK solutions failing on a claws-versus-table constraint, and the arm visibly travels too far instead of stopping at the block. It happens if a destination for the second or later move in a chain is still tagged `reference_frame="cam-1"` (or any other frame that rides on the arm) instead of `reference_frame="world"`. By the time that move runs, the arm has already relocated, so the moving frame no longer matches the position the pose was computed against, and the offset gets applied again on top of a position that is already most of the way there. Confirm every `motion.move` after the first in a chain uses a pose you already converted with `transform_pose`, as in [Convert to world before you move](#convert-to-world-before-you-move).

With a full perception-guided pick loop running end to end, you have every piece of the workshop's core loop working from your own computer: detection, planned motion, and a reliable place. [The next phase](/tutorials/pick-and-place/inline-module/) picks up from here to package this same script as a module that runs on the robot directly, with no laptop connection required once it is deployed. If you are stopping here, the [wrap-up](/tutorials/pick-and-place/wrap-up/) reviews what you built and where to go next.

{{< workshop-nav >}}
