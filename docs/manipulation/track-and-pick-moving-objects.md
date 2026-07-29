---
linkTitle: "Track and pick moving objects"
title: "Track and pick moving objects"
weight: 20
layout: "docs"
type: "docs"
description: "Build a control loop that tracks a part moving on a conveyor, predicts where it will be, and picks it with a robot arm."
---

A part rides down a conveyor at a steady speed. Your arm has to reach the belt,
close the gripper on the part, and lift it away before the part passes out of
reach. Because the part keeps moving while the arm plans and travels, aiming the
arm at where the camera last saw the part places the gripper behind the target.
This guide shows you how to build a pick loop that measures the part's motion,
predicts where it will be at the moment of the grasp, and commands the arm to
that predicted pose.

## Prerequisites

- A configured [camera](/reference/components/camera/) viewing the belt
- A configured vision service detector that recognizes the part. See
  [Detect objects](/vision/object-detection/detect/).
- A configured [arm](/reference/components/arm/) and
  [gripper](/reference/components/gripper/) that reach the belt
- The [motion service](/reference/apis/services/motion/) and a
  [frame system](/motion-planning/frame-system/) that relates the
  camera, arm, and belt in one coordinate space

## Steps

### 1. Detect the part

Run the detector on the live camera feed. Each call returns the current
bounding boxes for parts in view.

```python
from viam.services.vision import VisionClient

detector = VisionClient.from_robot(machine, "belt-detector")
detections = await detector.get_detections_from_camera("belt-camera")
```

For the full parameter list and language-specific signatures, see
[`GetDetectionsFromCamera`](/reference/apis/services/vision/#getdetectionsfromcamera).
Detection alone reports what is in a single frame; it does not connect a box in
this frame to the same part in the next frame.

### 2. Track the part across frames

To follow one part through the stream, give each detection a persistent ID. The
[`viam:object-tracker` module](/vision/object-detection/track/) wraps your detector
and camera, matches detections between consecutive frames, and assigns each part
a stable track ID such as `part_0_20260701_143052`. Configure it as described in
[Track objects across frames](/vision/object-detection/track/), then read its
detections the same way you read any detector.

With a stable ID you can measure motion. Record the part's position and the
capture time on two frames, then estimate belt velocity from the difference:

```python
import time

# Two observations of the same track ID, in world coordinates (mm)
p0, t0 = observe(track_id)   # returns ((x, y, z), timestamp_seconds)
p1, t1 = observe(track_id)

dt = t1 - t0
velocity = tuple((b - a) / dt for a, b in zip(p0, p1))  # mm per second
```

Average several frame pairs to smooth out per-frame detection noise. On a
conveyor the motion is dominated by one axis, so the velocity estimate reduces
to belt speed along that axis.

### 3. Predict the intercept pose

Estimate how long the pick will take from the moment you commit: the time to
plan the arm move plus the time for the arm to travel and the gripper to close.
Call this `t_pick`. Extrapolate the part's position forward by that interval to
get the intercept point:

```python
t_pick = 0.9  # seconds: planning + arm travel + grasp, measured on your cell

intercept = tuple(p + v * t_pick for p, v in zip(p1, velocity))
```

Keep `t_pick` realistic. If the true pick takes longer than your estimate, the
part overshoots the intercept point and the gripper closes behind it.

### 4. Plan the arm move to the predicted pose

Hand the intercept point to the [motion service](/reference/apis/services/motion/),
which plans a collision-free path and moves the arm. Orient the gripper for a
top-down grasp on the belt.

```python
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

x, y, z = intercept
destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=x, y=y, z=z, o_x=0, o_y=0, o_z=-1, theta=0),
)
await motion_service.move(component_name="belt-arm", destination=destination)
```

For the move signature and options such as passing a `WorldState` of obstacles,
see [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/).

### 5. Time the grasp

The arm arrives ahead of the part and the part travels into the open gripper.
Close the gripper when the part reaches the intercept point, then lift clear of
the belt:

```python
from viam.components.gripper import Gripper

gripper = Gripper.from_robot(machine, "belt-gripper")
await gripper.grab()
# Retract the arm to a safe pose above the belt with another motion_service.move
```

Wrap steps 1 through 5 in a loop so the cell processes one part per cycle. Track
whether each grasp succeeds and log the part IDs you pick so a missed part can be
retried on the next pass.

## Diagnose the latency budget

The maximum belt speed your cell can handle follows directly from `t_pick`. The
total pick latency is the sum of three stages:

- **Inference:** capture a frame and run the detector and tracker on it.
- **Planning:** the motion service solves for a path to the intercept pose.
- **Arm move and grasp:** the arm travels and the gripper closes.

During that whole interval the part keeps moving. If the part travels farther
than your prediction covers before the gripper closes, the grasp misses, so the
belt speed and the pick latency are linked: the faster the belt, the less time
you have, and the farther a prediction error carries the part off target.

To raise the belt speed, shrink the latency budget: use a faster detector,
reduce planning time by constraining the workspace, or shorten arm travel by
starting each cycle from a pose near the belt. Measure each stage separately so
you tune the one that dominates. For how inference time enters this budget and
how to measure it, see [Inference latency](/ai-control/inference-latency/).

If picks miss intermittently, compare your assumed `t_pick` against the measured
end-to-end time under load. A budget that holds at rest often grows once the
detector, planner, and arm run concurrently, which pushes the real intercept
point past where you aimed.

## Next steps

- [Detect objects](/vision/object-detection/detect/)
- [Track objects across frames](/vision/object-detection/track/)
- [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/)
- [Motion service API](/reference/apis/services/motion/)
