---
title: "Phase 5: Perception-guided picking"
linkTitle: "5. Perception-guided picking"
type: "docs"
slug: "perception-guided-picking"
weight: 50
description: "Add the vision pipeline and write the perception loop that detects a block, transforms it to the world frame, and picks it with motion planning."
workshop: "pick-and-place"
toc_hide: true
phase: 5
phase_total: 6
time_estimate: "22 minutes"
prev: "/tutorials/pick-and-place/control-the-robot-from-python/"
next: "/tutorials/pick-and-place/inline-module/"
languages: ["python"]
---

In this phase you replace the fixed approach and grasp poses with live data from the camera: a vision service detects a block, the robot transforms the block's position as coordinates in the world, and the motion service plans a collision-free pick.

## Configure the vision pipeline

On the **CONFIGURE** tab, click the **+** icon and select **Blocks**. Search for `shape-finder` and select the `devrel:shape-finder:detector` vision model. Name it `shape-detector` and set its attribute:

```json
{
  "camera_name": "cam-1"
}
```

The `camera_name` attribute is also a dependency: `shape-detector` cannot run until `cam-1` is online, the same dependency pattern you have already seen with `gripper-1` and `arm-1`. This service reads color frames from `cam-1` and finds blocks by shape.

<!-- ASSET P1 configure-vision-pipeline (UI): the shape-detector and vision-segment service configs -->

{{<imgproc src="/tutorials/pick-and-place/configure-vision-pipeline.png" resize="1200x" declaredimensions=true alt="The shape-detector vision service config with its camera_name attribute.">}}

Add the second service the same way. Click the **+** icon and select **Blocks**, search for `detections-to-segments`, and select the `viam:vision:detections-to-segments` model. Name it `vision-segment` and set its attributes:

```json
{
  "detector_name": "shape-detector",
  "camera_name": "cam-1",
  "mean_k": 5,
  "sigma": 1.25
}
```

`vision-segment` depends on `shape-detector` and `cam-1`, the same graph relationship as before: it takes each 2D shape detection, pulls the matching depth points from `cam-1`, filters noisy points out with the `mean_k` and `sigma` attributes, and fuses the result into a 3D object point cloud per detected block. A 2D detection alone cannot tell you how far away a block is or where it sits in space; `vision-segment` is what turns "a block-shaped region of pixels" into "a block at this point in three dimensions."

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

## The frame system and transform_pose

<!-- ASSET P0 diagram-frame-transform (DIAGRAM): block position in the cam-1 frame vs world, wrist camera on the arm -->

```text
Frame tree (rooted at world):

world  (origin at the arm base)
└─ arm-1
   ├─ gripper-1   (z +105 from the arm end)
   └─ cam-1       (wrist-mounted)

Detected block:
  pose in the cam-1 frame  ──(transform_pose)──→  pose in the world frame
  transform_pose walks the frame tree above.
```

Every pose that `vision-segment` returns is expressed in the `cam-1` frame. That is the only frame the vision service knows about: it looked at pixels and depth values coming out of one camera, so the coordinates it hands back describe where a block sits relative to that camera's own origin and orientation.

The motion service plans in the `world` frame, the same frame your obstacle geometry was defined against. To hand a detected pose to the motion service, you first have to express it in `world` instead of `cam-1`.

This is the frame system you see visualized in 3D scene tab, when the `cam-1` frame visibly moved as you jogged joint 1. `viam-server` maintains that same relationship as a graph: the camera's offset from the wrist, the wrist's offset from the next joint, and so on, all the way down to the arm's base at the world origin. `RobotClient.transform_pose` walks that graph for you. Give it a pose tagged with its source reference frame and a destination frame, and it returns the equivalent pose in the destination frame:

```python
# geometry is a detected object from vision-segment; geometry.center is its pose
obj_in_cam = PoseInFrame(reference_frame="cam-1", pose=geometry.center)
obj_in_world = await machine.transform_pose(obj_in_cam, "world")
```

`PoseInFrame` pairs a `Pose` with the name of the frame it is expressed in. `transform_pose` reads that source frame, reads the destination frame you passed as the second argument, and returns a new `PoseInFrame` with the same physical point re-expressed in the destination frame. The example above takes the detected object's pose in the `cam-1` frame and transforms it to `world`. You will wire this into the full detection code in the next section, once there is an actual `geometry.center` to transform.

## Detect from home (the wrist-camera rule)

<!-- ASSET P0 diagram-detect-from-home (DIAGRAM): same block, two arm poses, two different world answers -->

```text
One block, fixed on the table
        │
        ├─ read from an unfixed / unknown arm pose
        │     cam-1 frame depends on the arm pose
        │     → transform_pose to world can differ each time   (unreliable)
        │
        └─ read from home-pose (a known position)
              cam-1 frame is in a known, repeatable place
              → transform_pose to world is consistent          (reliable)
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

# The object pose is in the camera frame; the planner needs world frame.
obj_in_cam = PoseInFrame(reference_frame="cam-1", pose=geometry.center)
obj_in_world = await machine.transform_pose(obj_in_cam, "world")
```

`get_object_point_clouds` returns one entry per object `vision-segment` fused together, each carrying its own point cloud and geometry. A workspace with several blocks in view returns several entries, so you need a rule for which one to pick this cycle. `max(objects, key=lambda o: len(o.point_cloud))` picks the object with the largest point cloud, ordinarily the block closest to the camera or most fully in view. Each `point_cloud` is the object's pointcloud data (PCD) stored as raw bytes, so `len(o.point_cloud)` measures its encoded size in bytes; that grows with the number of points, which makes it a reliable proxy for object size.

Add a `print(obj_in_world.pose)` after the transform and run the script. Watch the x, y, and z values it prints as you move a block around the table.

{{< checkpoint >}}
`obj_in_world.pose` prints coordinates that make physical sense: a `z` roughly at the table surface plus the block's height, and `x`/`y` values that land somewhere over the table rather than off in empty space or underneath it. If the numbers look physically wrong, the most common cause is a detection that was not taken from `home-pose`. Confirm the arm returns to `home-pose` (the `await home.set_position(2)` call) before every `get_object_point_clouds` call.
{{< /checkpoint >}}

## Compute the approach and grasp poses

<!-- ASSET P0 diagram-approach-grasp-offsets (DIAGRAM): block center; approach = +100mm; grasp = TCP one gripper-length (60mm) above; gripper-1 TCP vs arm end -->

```text
Offsets applied to obj_in_world.pose (the block center). They move the
gripper-1 TCP, not the arm's end frame:

  +100 mm  ── approach pose  (APPROACH_MM): standoff above the block
        │
        │  descend
        ▼
   +60 mm  ── grasp pose     (GRIPPER_LENGTH_MM): the gripper-1 TCP,
        │                     one gripper-length above the fingertips
        │  fingers close here
        ▼
     0 mm  ── block center   (obj_in_world.pose)
```

The pick uses the **motion service**: it plans a collision-free path to a Cartesian (coordinates in 3D space) goal. Unlike the vision service, you never configured it. The motion service is one of a handful of services the RDK builds into `viam-server` itself, so it is present on every machine under the reserved name `builtin`, which is why `builtin` appeared in `machine.resource_names` even though there is no motion component on the **CONFIGURE** tab to point at. Uncomment its handle in the script, the same way you uncommented the vision handle earlier in this phase:

```python
motion = MotionClient.from_robot(machine, "builtin")
```

Before you turn `obj_in_world.pose` into a place to move the gripper, it matters exactly what `motion.move` moves. Two motions that sound similar are not the same thing:

- The CONTROL tab's arm card, and a direct `Arm` method, move the arm's own end frame: the flange at the end of the last joint.
- `motion.move(component_name="gripper-1", ...)` moves the `gripper-1` frame instead, the gripper's own tool center point (TCP), which sits further down the kinematic chain than the arm's end because the gripper is bolted on past it.

Every offset you compute in this section is an offset from `obj_in_world.pose` to wherever you want the `gripper-1` frame to end up, not the arm's end. Keep that distinction in mind or the math below will not make sense.

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
approach_pose = offset_pose(obj_in_world.pose, APPROACH_MM)
```

`APPROACH_MM` is 100. Since every offset here is applied to `obj_in_world.pose`, which is the block's bounding-box center, this places the standoff 100 mm above the block center: enough clearance for the gripper to descend cleanly, with room to spare for a small pose error.

Now compute the grasp pose yourself. What you actually want at the block is the gripper's fingers, not its TCP: the fingers have to close around the block. The `gripper-1` TCP frame sits one gripper-length above the fingertip contact point, so to put the fingers at the block center you place the TCP one gripper-length (`GRIPPER_LENGTH_MM`) above it. Remember that `motion.move` is already driving the gripper's own TCP, not the arm's end, so this is the only offset you add here. Work out the offset before reading on.

The offset is `GRIPPER_LENGTH_MM`, the depth from the gripper's TCP down to its fingertip contact point:

```python
grasp_pose = offset_pose(obj_in_world.pose, GRIPPER_LENGTH_MM)
```

`GRIPPER_LENGTH_MM` is 60. If you used `APPROACH_MM` here by mistake, the gripper stops well above the block instead of at it; if you used zero, you would drive the TCP itself to the block center, sinking the fingers a full gripper-length past the block instead of closing them around it.

## Run the full pick loop

<!-- ASSET P0 perception-pick (MOTION): full detect -> approach -> descend -> grab -> place cycle (milestone-two hero asset) -->

With `approach_pose` and `grasp_pose` computed, assemble the full cycle:

```python
await motion.move(
    component_name="gripper-1",
    destination=PoseInFrame(reference_frame="world", pose=approach_pose),
)
await gripper.open()
await motion.move(
    component_name="gripper-1",
    destination=PoseInFrame(reference_frame="world", pose=grasp_pose),
)
await gripper.grab()
await asyncio.sleep(0.3)  # finger gripper settle
await travel.set_position(2)
await place_pose.set_position(2)
await gripper.open()
await home.set_position(2)
```

This cycle picks with `motion.move` and places with the saved-pose switches from Phase 3. The pick target moves every cycle, so it needs the Cartesian precision and obstacle-aware planning that `motion.move` provides against a freshly computed world pose. The place target never moves: it is the same bin in the same spot every time. The saved-pose switch replays fixed joint positions directly, without invoking the motion planner, so for a target that never changes it is simpler and just as reliable as planning a fresh path each cycle.

{{< alert title="The arm moves under code control" color="caution" >}}
This loop drives the arm to a computed grasp pose with `motion.move` and replays saved poses, all from your script. Keep the workspace clear and the e-stop within reach, and run it the first few times ready to stop the arm if a computed pose looks wrong.
{{< /alert >}}

Run the script and watch the sequence in stages: the approach move first, then the grasp move, then the full cycle through to a placed block.

{{< checkpoint >}}
The approach move completes without a planning error, positioning the gripper above the block. If it fails here, open the **3D scene** tab during the next run and check whether `approach_pose` lands inside the table or safety-wall geometry; a block detected very close to a boundary can push the arm outside the planner's reachable space.
{{< /checkpoint >}}

{{< checkpoint >}}
The grasp move completes and **Grab** closes the fingers around the block, holding it through the lift into `travel-pose`. If the gripper closes on empty air, the block likely shifted between detection and grasp, or the grasp offset is off; revisit the offset math above.
{{< /checkpoint >}}

{{< checkpoint >}}
The full loop runs end to end: approach, open, grasp, grab, travel, place, open, home, with the block landing in the bin. This is the same sequence you drove by hand in the UI and by fixed poses in the initial Python script, now driven by a pose your code computed from a live detection.
{{< /checkpoint >}}

## Debugging guide

<!-- ASSET P1 3dscene-planned-path (UI): 3D scene during a move, arm path relative to the Phase 3 obstacles -->

Work through these in order. The first one causes most of the rest. If you get stuck, compare your loop against the complete [`reference-solution.py`](https://github.com/viam-devrel/pick-and-place/blob/main/scripts/reference-solution.py) in the companion repo.

- **Did you detect from `home-pose`?** This is the first thing to check for nearly every perception symptom below. If the `await home.set_position(2)` guard is missing before a `get_object_point_clouds` call, or if you added a second detection somewhere that skips it, every downstream pose is computed against the wrong camera position.
- **No objects detected.** Open the **CONTROL** tab and run the `vision-segment` card by hand while a block sits in view. If that also returns nothing, check the `shape-detector` card on its own: a detector that finds nothing means the block is out of frame, or lighting has changed enough to affect the shape detection. If `shape-detector` finds the block but `vision-segment` does not, check that a block is close enough and clearly separated from the table surface for the depth fusion step to segment it.
- **The pick point drifts from cycle to cycle, even for a block that has not moved.** This is almost always the wrist-camera rule again: some code path is detecting from a pose other than `home-pose`. Print `obj_in_world.pose` on every cycle and confirm the arm is fully settled at `home-pose` before each detection call.
- **Motion planning fails, or the target looks unreachable.** Open the **3D scene** tab during the failing move and look at where `approach_pose` or `grasp_pose` lands relative to the table and safety-wall geometry from Phase 3. A detected pose near a workspace boundary can place the standoff or the grasp point outside the region the planner is allowed to move through. If you skipped or under-measured the obstacle configuration in Phase 3, this is where it bites: geometry that does not match your physical setup makes the planner reject moves that are perfectly safe, or, worse, accept ones that are not. Revisit [Teach the planner about obstacles](/tutorials/pick-and-place/static-positions/#teach-the-planner-about-obstacles) and recheck your measurements before assuming the pose math is wrong.

With a full perception-guided pick loop running end to end, you have every piece of the workshop's core loop working from your own computer: detection, the frame transform, planned motion, and a reliable place. [The next phase](/tutorials/pick-and-place/inline-module/) picks up from here to package this same script as a module that runs on the robot directly, with no laptop connection required once it is deployed. If you are stopping here, the [wrap-up](/tutorials/pick-and-place/wrap-up/) reviews what you built and where to go next.

{{< workshop-nav >}}
