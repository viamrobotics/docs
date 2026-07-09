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

In this phase you replace the fixed approach and grasp poses with live data from the camera: a vision service detects a block, and the motion service takes the block's camera-frame position and plans a collision-free pick.

## Configure the vision pipeline

Perception here is a two-stage pipeline. A **detector** finds blocks in the camera's 2D color image and returns a labeled bounding box for each. A **segmenter** then takes those 2D boxes, pulls the matching depth points from the camera, and fuses each into a 3D object point cloud with a real-world position. A 2D detection alone cannot tell you how far away a block is or where it sits in space; the segmenter is what turns "a block-shaped region of pixels" into "a block at this point in three dimensions." You configure the two as separate vision services, wired so the segmenter depends on the detector.

### Add the shape detector

`devrel:shape-finder:detector` is a vision model that finds known block shapes in a color image and returns a labeled bounding box for each. On the **CONFIGURE** tab, click the **+** icon and select **Blocks**, search for `shape-finder`, select the `devrel:shape-finder:detector` model, and name it `shape-detector`. Set its one attribute:

```json
{
  "camera_name": "cam-1"
}
```

`camera_name` tells the detector which camera to read color frames from, and it is also a dependency: `shape-detector` cannot run until `cam-1` is online, the same dependency pattern you have already seen with `gripper-1` and `arm-1`.

<!-- ASSET P1 configure-vision-pipeline (UI): the shape-detector and vision-segment service configs -->

{{<imgproc src="/tutorials/pick-and-place/configure-vision-pipeline.png" resize="1200x" declaredimensions=true alt="The shape-detector vision service config with its camera_name attribute.">}}

### Add the segmenter

`viam:vision:detections-to-segments` is a builtin vision model that reads a detector's output together with the camera's depth data and produces one point cloud per detection, each with an estimated size and 3D position. Add it the same way: click the **+** icon and select **Blocks**, search for `detections-to-segments`, select the `viam:vision:detections-to-segments` model, and name it `vision-segment`. Set its attributes:

```json
{
  "detector_name": "shape-detector",
  "camera_name": "cam-1",
  "mean_k": 5,
  "sigma": 1.25
}
```

`detector_name` and `camera_name` are dependencies, so `vision-segment` waits for both `shape-detector` and `cam-1` before it starts. `mean_k` and `sigma` tune a statistical outlier filter that cleans up the depth points before fusion: `mean_k` is how many neighbors each point is compared against, and `sigma` is how far from the local average a point may sit before it is dropped as noise. The values here are sensible defaults; see [detections-to-segments](/reference/services/vision/detections-to-segments/) for the full attribute reference.

Save the config and open the **CONTROL** tab. Find the `vision-segment` test card. You should see the detections coming from the `shape-detector` service and one or more segmented objects under the **Object point clouds** section after toggling **Show object point clouds**. Each segmented object is displayed as a small point cloud with a label matching the paired bounding-box detection, with estimated dimensions and 3D position from the perspective of the camera.

<!-- ASSET P0 control-vision-detections (UI+): CONTROL vision card showing detected blocks with boxes + labels. See plans/2026-07-02-pick-and-place-shot-list.md -->

{{<imgproc src="/tutorials/pick-and-place/control-vision-detections.png" resize="1200x" declaredimensions=true alt="The shape-detector vision card showing a detected block with a bounding box and label.">}}

<!-- ASSET P1 control-vision-segment-object (UI): vision-segment Object point clouds view, one segmented object with dimensions and position -->

{{<imgproc src="/tutorials/pick-and-place/control-vision-segment-object.png" resize="1200x" declaredimensions=true alt="A vision-segment object point cloud labeled square-red (box) with its estimated dimensions and 3D position in the camera frame.">}}

{{< checkpoint >}}
The `vision-segment` test card returns at least one object when a block is in view. If it returns nothing, confirm a block actually sits in the camera's field of view, then check the `shape-detector` card on its own: if that also returns nothing, the problem is upstream in shape detection.
{{< /checkpoint >}}

With the service live, go back to `starter-script.py` and uncomment the vision handle you commented out in Phase 4:

```python
vision = VisionClient.from_robot(machine, "vision-segment")
```

## Let the motion service place the gripper

Every pose that `vision-segment` returns is expressed in the `cam-1` frame. That is the only frame the vision service knows about: it looked at pixels and depth values coming out of one camera, so the coordinates it hands back describe where a block sits relative to that camera's own origin and orientation.

The pick uses the **motion service** to move the arm to that block. You never configured it: the motion service is one of a handful of services the RDK builds into `viam-server` itself, so it is present on every machine under the reserved name `builtin`, which is why `builtin` appeared in `machine.resource_names` even though there is no motion component on the **CONFIGURE** tab to point at. Uncomment its handle in the script, the same way you uncommented the vision handle earlier in this phase:

```python
motion = MotionClient.from_robot(machine, "builtin")
```

You do not convert the detected pose to the `world` frame yourself. `motion.move` takes a `PoseInFrame`: a `Pose` paired with the name of the frame it is expressed in. Tag the detected pose with `reference_frame="cam-1"` and the motion service walks the frame graph for you, the same graph you watched move in the **3D scene** tab when the `cam-1` frame swung with the arm as you jogged joint 1. It knows the camera's offset from the wrist, the wrist's offset from the next joint, and so on down to the arm's base at the world origin, so it can plan a collision-free path in `world` from a goal you hand it in `cam-1`.

<!-- ASSET P0 diagram-frame-transform (DIAGRAM): wrist camera on the arm; block pose reported in cam-1, motion.move resolves it against world -->

```text
Frame tree (rooted at world):

world  (origin at the arm base)
└─ arm-1
   ├─ gripper-1   (z +105 from the arm end — the TCP motion.move drives)
   └─ cam-1       (wrist-mounted — the frame vision-segment reports in)

motion.move plans in world from a goal you give it in cam-1;
the motion service walks this tree for you.
```

It also matters exactly what `motion.move` moves. Two motions that sound similar are not the same thing:

- The **CONTROL** tab's arm card, and a direct `Arm` method, move the arm's own end frame: the flange at the end of the last joint.
- `motion.move(component_name="gripper-1", ...)` moves the `gripper-1` frame instead: the gripper's tool center point (TCP), which sits further down the kinematic chain because the gripper is bolted on past the arm's end.

A `motion.move` call names that component and a goal pose tagged with its reference frame:

```python
await motion.move(
    component_name="gripper-1",
    destination=PoseInFrame(reference_frame="cam-1", pose=target_pose),
)
```

Because you move `gripper-1`, every offset you compute later is measured to where you want the gripper's TCP to end up, not the arm's end. Keep that distinction in mind or the offset math will not make sense.

{{< alert title="Seeing a pose in world coordinates" color="note" >}}
`motion.move` does not need a world-frame pose, but you might still want one to check a detection by eye. `RobotClient.transform_pose` converts a `PoseInFrame` from one frame to another: `world_pose = await machine.transform_pose(PoseInFrame(reference_frame="cam-1", pose=geometry.center), "world")` returns the block's center in `world`, where a `z` near the table surface and `x`/`y` over the table confirm the detection landed where you expect.
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

The `home-pose` provides a good view of the workspace for the camera to detect objects to be picked up by the arm. Each pick-and-place cycle, the arm moves to the home pose and the `shape-detector` looks for known shapes. If it has detections, it provides them to the `vision-segment` service, which you query with `vision.get_object_point_clouds`. You replace the static `approach` and `grasp` poses with poses derived from the point cloud segments:

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

Add a `print(obj_in_cam.pose)` and run the script. Watch the x, y, and z values it prints as you move a block around the table.

{{< checkpoint >}}
`obj_in_cam.pose` prints coordinates in the camera's own frame: a `z` of roughly the camera-to-block distance, a few hundred millimeters, with small `x`/`y` values near the optical center. To check the detection against the workspace instead, use the `transform_pose` tip above to print the pose in `world`. If the numbers look wrong, the most common cause is a detection that was not taken from `home-pose`. Confirm the arm returns to `home-pose` (the `await home.set_position(2)` call) before every `get_object_point_clouds` call.
{{< /checkpoint >}}

## Compute the approach and grasp poses

<!-- ASSET P0 diagram-approach-grasp-offsets (DIAGRAM): block center in cam-1; approach -100mm toward camera; grasp = gripper-1 TCP one gripper-length (-60mm) toward camera; gripper-1 TCP vs arm end -->

```text
Offsets applied to obj_in_cam.pose (the block center, in the cam-1 frame).
In the camera frame, +z points out of the lens into the scene, so moving
toward the camera, up and away from the block, is a negative z offset:

  (toward the camera)  ▲  -z
                       │
  -100 mm  ── approach pose  (APPROACH_MM): standoff between camera and block
        │
        │  descend
        │
   -60 mm  ── grasp pose     (GRIPPER_LENGTH_MM): the gripper-1 TCP, offset so
        │                     the fingertips land on the block center
        │
     0 mm  ── block center   (obj_in_cam.pose)
                       │
  (deeper into scene)  ▼  +z
```

Because you observe from `home-pose` every cycle, the wrist camera looks down at the workspace from the same angle each time, so its depth axis stays roughly vertical and a `z` offset moves the target up and down as you would expect. This is one more reason the detect-from-home rule matters: it keeps the frame you are offsetting in a known orientation.

The workshop's `offset_pose` helper raises or lowers a pose in `z` while leaving `x`, `y`, and orientation untouched:

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

The approach pose is a standoff directly above the block, high enough that the gripper can descend onto it without first colliding with it sideways. That offset is worked for you:

```python
approach_pose = offset_pose(obj_in_cam.pose, APPROACH_MM)
```

`APPROACH_MM` is `-100`. Applied to `obj_in_cam.pose`, the block's bounding-box center, this places the standoff 100 mm toward the camera from the block: enough clearance for the gripper to descend cleanly, with room to spare for a small pose error.

Now compute the grasp pose yourself. At the block you want the gripper's fingertips, not its TCP: the fingers have to close around the block. `motion.move` drives the `gripper-1` TCP, which sits one gripper-length back from the fingertip contact point, so to land the fingertips on the block center you stop the TCP one gripper-length short of it, toward the camera. That single offset is all you add, because `motion.move` is already driving the gripper's TCP rather than the arm's end. Work out the offset before reading on.

The offset is `GRIPPER_LENGTH_MM`, the depth from the gripper's TCP out to its fingertip contact point:

```python
grasp_pose = offset_pose(obj_in_cam.pose, GRIPPER_LENGTH_MM)
```

`GRIPPER_LENGTH_MM` is `-60`. If you used `APPROACH_MM` here by mistake, the gripper stops well short of the block instead of at it; if you used zero, you would drive the TCP itself to the block center, sinking the fingers a full gripper-length past the block instead of closing them around it.

{{< checkpoint >}}
Before wiring up the moves, print `approach_pose` and `grasp_pose` and compare their `z` to `obj_in_cam.pose.z`: the approach `z` should sit about 100 mm toward the camera and the grasp `z` about 60 mm toward it. If either offset went the wrong way, the pick drives into or well short of the block, so fix the sign before running a move.
{{< /checkpoint >}}

## Run the full pick loop

<!-- ASSET P0 perception-pick (MOTION): full detect -> approach -> descend -> grab -> place cycle (milestone-two hero asset) -->

With `approach_pose` and `grasp_pose` computed, assemble the full cycle:

```python
await motion.move(
    component_name="gripper-1",
    destination=PoseInFrame(reference_frame="cam-1", pose=approach_pose),
)
await gripper.open()
await motion.move(
    component_name="gripper-1",
    destination=PoseInFrame(reference_frame="cam-1", pose=grasp_pose),
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
- **No objects detected.** Open the **CONTROL** tab and run the `vision-segment` card by hand while a block sits in view. If that also returns nothing, check the `shape-detector` card on its own: a detector that finds nothing means the block is out of frame, or lighting has changed enough to affect the shape detection. If `shape-detector` finds the block but `vision-segment` does not, check that a block is close enough and clearly separated from the table surface for the depth fusion step to segment it.
- **The pick point drifts from cycle to cycle, even for a block that has not moved.** This is almost always the wrist-camera rule again: some code path is detecting from a pose other than `home-pose`. Print `obj_in_cam.pose` on every cycle and confirm the arm is fully settled at `home-pose` before each detection call.
- **Motion planning fails, or the target looks unreachable.** Open the **3D scene** tab during the failing move and look at where `approach_pose` or `grasp_pose` lands relative to the table and safety-wall geometry from Phase 3. A detected pose near a workspace boundary can place the standoff or the grasp point outside the region the planner is allowed to move through. If you skipped or under-measured the obstacle configuration in Phase 3, this is where it bites: geometry that does not match your physical setup makes the planner reject moves that are perfectly safe, or, worse, accept ones that are not. Revisit [Teach the planner about obstacles](/tutorials/pick-and-place/static-positions/#teach-the-planner-about-obstacles) and recheck your measurements before assuming the pose math is wrong.

With a full perception-guided pick loop running end to end, you have every piece of the workshop's core loop working from your own computer: detection, planned motion, and a reliable place. [The next phase](/tutorials/pick-and-place/inline-module/) picks up from here to package this same script as a module that runs on the robot directly, with no laptop connection required once it is deployed. If you are stopping here, the [wrap-up](/tutorials/pick-and-place/wrap-up/) reviews what you built and where to go next.

{{< workshop-nav >}}
