---
linkTitle: "Track objects"
title: "Track objects across frames"
weight: 40
layout: "docs"
type: "docs"
description: "Match detections across consecutive frames using IoU, assign stable track IDs, and count entries and exits."
date: "2025-01-30"
aliases:
  - /build/vision-detection/track-objects-across-frames/
  - /vision-detection/track-objects-across-frames/
---

Viam's vision service provides per-frame detections but does not include built-in tracking. Detection gives you a snapshot: in this frame, there are three people. In the next frame, there are still three people. But are they the same three people? Tracking solves this by matching detections across consecutive frames and assigning stable IDs, so you can answer questions like: how long has this person been standing here? How many cars have passed through this intersection?

## Concepts

### The tracking problem

Object detection operates on single frames. It tells you what is in the image right now, but nothing about what was in the previous image. When you run detections at 5 frames per second, you get 5 independent lists of bounding boxes. Without tracking, you cannot tell whether a detection in frame 2 corresponds to the same object as a detection in frame 1.

Tracking bridges this gap by maintaining a set of active tracks, each with a unique ID. On each new frame, you match new detections to existing tracks. Unmatched detections become new tracks. Tracks with no matching detection for several frames are considered lost.

### Intersection over Union (IoU)

IoU is the standard metric for measuring how much two bounding boxes overlap. It is the area of their intersection divided by the area of their union.

- **IoU = 1.0**: the boxes are identical.
- **IoU = 0.0**: the boxes do not overlap at all.
- **IoU > 0.3**: the boxes likely refer to the same object.

IoU works well for frame-to-frame matching because objects typically move only a small amount between consecutive frames. A person detected at position (100, 200)-(200, 400) in frame N will likely be at approximately (105, 202)-(205, 402) in frame N+1, giving a high IoU.

### Track lifecycle

Each track goes through three phases:

1. **Created**: a new detection appears that does not match any existing track. A new track ID is assigned.
2. **Active**: the track is matched to a detection in the current frame. Its position is updated.
3. **Lost**: the track has not been matched for a configurable number of frames. It is removed.

Tracking how many tracks are created and lost over time gives you entry/exit counts.

## Steps

### 1. Understand the IoU calculation

Before building the tracker, understand how IoU works. Here is the calculation in both languages.

{{< tabs >}}
{{% tab name="Python" %}}

```python
def compute_iou(box_a, box_b):
    """Compute Intersection over Union between two bounding boxes.

    Each box is a tuple (x_min, y_min, x_max, y_max).
    """
    x_min = max(box_a[0], box_b[0])
    y_min = max(box_a[1], box_b[1])
    x_max = min(box_a[2], box_b[2])
    y_max = min(box_a[3], box_b[3])

    intersection = max(0, x_max - x_min) * max(0, y_max - y_min)
    if intersection == 0:
        return 0.0

    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union = area_a + area_b - intersection

    return intersection / union
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
type BBox struct {
    XMin, YMin, XMax, YMax int
}

func computeIoU(a, b BBox) float64 {
    xMin := max(a.XMin, b.XMin)
    yMin := max(a.YMin, b.YMin)
    xMax := min(a.XMax, b.XMax)
    yMax := min(a.YMax, b.YMax)

    intersectionW := max(0, xMax-xMin)
    intersectionH := max(0, yMax-yMin)
    intersection := float64(intersectionW * intersectionH)
    if intersection == 0 {
        return 0.0
    }

    areaA := float64((a.XMax - a.XMin) * (a.YMax - a.YMin))
    areaB := float64((b.XMax - b.XMin) * (b.YMax - b.YMin))
    union := areaA + areaB - intersection

    return intersection / union
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Build the tracker

The tracker maintains a list of active tracks and matches new detections to them on each frame.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import time


class Track:
    def __init__(self, track_id, detection):
        self.track_id = track_id
        self.class_name = detection.class_name
        self.box = (detection.x_min, detection.y_min,
                    detection.x_max, detection.y_max)
        self.confidence = detection.confidence
        self.frames_since_seen = 0
        self.created_at = time.time()
        self.last_seen = time.time()

    def update(self, detection):
        self.box = (detection.x_min, detection.y_min,
                    detection.x_max, detection.y_max)
        self.confidence = detection.confidence
        self.class_name = detection.class_name
        self.frames_since_seen = 0
        self.last_seen = time.time()


class SimpleTracker:
    def __init__(self, iou_threshold=0.3, max_lost_frames=10):
        self.tracks = []
        self.next_id = 1
        self.iou_threshold = iou_threshold
        self.max_lost_frames = max_lost_frames
        self.total_entered = 0
        self.total_exited = 0

    def update(self, detections):
        """Match detections to existing tracks and return results."""
        new_objects = []
        lost_objects = []

        # Build bounding boxes for current detections
        det_boxes = [
            (d.x_min, d.y_min, d.x_max, d.y_max)
            for d in detections
        ]

        # Match detections to tracks using IoU
        matched_tracks = set()
        matched_detections = set()

        for t_idx, track in enumerate(self.tracks):
            best_iou = 0.0
            best_d_idx = -1

            for d_idx, det_box in enumerate(det_boxes):
                if d_idx in matched_detections:
                    continue
                iou = compute_iou(track.box, det_box)
                if iou > best_iou:
                    best_iou = iou
                    best_d_idx = d_idx

            if best_iou >= self.iou_threshold:
                track.update(detections[best_d_idx])
                matched_tracks.add(t_idx)
                matched_detections.add(best_d_idx)

        # Create new tracks for unmatched detections
        for d_idx, detection in enumerate(detections):
            if d_idx not in matched_detections:
                new_track = Track(self.next_id, detection)
                self.tracks.append(new_track)
                new_objects.append(new_track)
                self.next_id += 1
                self.total_entered += 1

        # Mark unmatched tracks as lost
        for t_idx, track in enumerate(self.tracks):
            if t_idx not in matched_tracks:
                track.frames_since_seen += 1

        # Remove tracks that have been lost too long
        surviving_tracks = []
        for track in self.tracks:
            if track.frames_since_seen > self.max_lost_frames:
                lost_objects.append(track)
                self.total_exited += 1
            else:
                surviving_tracks.append(track)
        self.tracks = surviving_tracks

        return new_objects, lost_objects
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "time"
)

type Track struct {
    TrackID        int
    ClassName      string
    Box            BBox
    Confidence     float64
    FramesSinceSeen int
    CreatedAt      time.Time
    LastSeen       time.Time
}

type SimpleTracker struct {
    Tracks         []*Track
    nextID         int
    IoUThreshold   float64
    MaxLostFrames  int
    TotalEntered   int
    TotalExited    int
}

func NewSimpleTracker(iouThreshold float64, maxLostFrames int) *SimpleTracker {
    return &SimpleTracker{
        nextID:        1,
        IoUThreshold:  iouThreshold,
        MaxLostFrames: maxLostFrames,
    }
}

func (t *SimpleTracker) Update(
    detections []objectdetection.Detection,
) (newObjects []*Track, lostObjects []*Track) {
    // Build bounding boxes for current detections
    detBoxes := make([]BBox, len(detections))
    for i, d := range detections {
        bb := d.BoundingBox()
        detBoxes[i] = BBox{
            XMin: bb.Min.X, YMin: bb.Min.Y,
            XMax: bb.Max.X, YMax: bb.Max.Y,
        }
    }

    matchedTracks := make(map[int]bool)
    matchedDetections := make(map[int]bool)

    // Match detections to tracks using IoU
    for tIdx, track := range t.Tracks {
        bestIoU := 0.0
        bestDIdx := -1

        for dIdx, detBox := range detBoxes {
            if matchedDetections[dIdx] {
                continue
            }
            iou := computeIoU(track.Box, detBox)
            if iou > bestIoU {
                bestIoU = iou
                bestDIdx = dIdx
            }
        }

        if bestIoU >= t.IoUThreshold && bestDIdx >= 0 {
            bb := detections[bestDIdx].BoundingBox()
            track.Box = BBox{
                XMin: bb.Min.X, YMin: bb.Min.Y,
                XMax: bb.Max.X, YMax: bb.Max.Y,
            }
            track.Confidence = detections[bestDIdx].Score()
            track.ClassName = detections[bestDIdx].Label()
            track.FramesSinceSeen = 0
            track.LastSeen = time.Now()
            matchedTracks[tIdx] = true
            matchedDetections[bestDIdx] = true
        }
    }

    // Create new tracks for unmatched detections
    for dIdx, d := range detections {
        if matchedDetections[dIdx] {
            continue
        }
        bb := d.BoundingBox()
        newTrack := &Track{
            TrackID:    t.nextID,
            ClassName:  d.Label(),
            Box:        BBox{XMin: bb.Min.X, YMin: bb.Min.Y,
                             XMax: bb.Max.X, YMax: bb.Max.Y},
            Confidence: d.Score(),
            CreatedAt:  time.Now(),
            LastSeen:   time.Now(),
        }
        t.Tracks = append(t.Tracks, newTrack)
        newObjects = append(newObjects, newTrack)
        t.nextID++
        t.TotalEntered++
    }

    // Mark unmatched tracks
    for tIdx := range t.Tracks {
        if !matchedTracks[tIdx] {
            t.Tracks[tIdx].FramesSinceSeen++
        }
    }

    // Remove lost tracks
    var surviving []*Track
    for _, track := range t.Tracks {
        if track.FramesSinceSeen > t.MaxLostFrames {
            lostObjects = append(lostObjects, track)
            t.TotalExited++
        } else {
            surviving = append(surviving, track)
        }
    }
    t.Tracks = surviving

    return newObjects, lostObjects
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Run the tracker with live detections

Connect the tracker to your vision service and run it in a loop.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    detector = VisionClient.from_robot(robot, "my-detector")
    tracker = SimpleTracker(iou_threshold=0.3, max_lost_frames=10)

    confidence_threshold = 0.5

    while True:
        detections = await detector.get_detections_from_camera("my-camera")

        # Filter by confidence before tracking
        confident = [
            d for d in detections
            if d.confidence >= confidence_threshold
        ]

        new_objects, lost_objects = tracker.update(confident)

        for obj in new_objects:
            print(f"NEW: Track {obj.track_id} ({obj.class_name})")

        for obj in lost_objects:
            duration = obj.last_seen - obj.created_at
            print(f"LOST: Track {obj.track_id} ({obj.class_name}), "
                  f"visible for {duration:.1f}s")

        active_count = len(tracker.tracks)
        print(f"Active: {active_count} | "
              f"Entered: {tracker.total_entered} | "
              f"Exited: {tracker.total_exited}")

        await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"
    "time"

    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/services/vision"
    "go.viam.com/rdk/vision/objectdetection"
    "go.viam.com/utils/rpc"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("tracker")

    machine, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            "YOUR-API-KEY-ID",
            rpc.Credentials{
                Type:    rpc.CredentialsTypeAPIKey,
                Payload: "YOUR-API-KEY",
            })),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer machine.Close(ctx)

    detector, err := vision.FromProvider(machine, "my-detector")
    if err != nil {
        logger.Fatal(err)
    }

    tracker := NewSimpleTracker(0.3, 10)
    confidenceThreshold := 0.5

    for {
        detections, err := detector.DetectionsFromCamera(
            ctx, "my-camera", nil,
        )
        if err != nil {
            logger.Error(err)
            time.Sleep(time.Second)
            continue
        }

        // Filter by confidence before tracking
        var confident []objectdetection.Detection
        for _, d := range detections {
            if d.Score() >= confidenceThreshold {
                confident = append(confident, d)
            }
        }

        newObjects, lostObjects := tracker.Update(confident)

        for _, obj := range newObjects {
            fmt.Printf("NEW: Track %d (%s)\n",
                obj.TrackID, obj.ClassName)
        }

        for _, obj := range lostObjects {
            duration := obj.LastSeen.Sub(obj.CreatedAt)
            fmt.Printf("LOST: Track %d (%s), visible for %v\n",
                obj.TrackID, obj.ClassName, duration.Round(time.Second))
        }

        fmt.Printf("Active: %d | Entered: %d | Exited: %d\n",
            len(tracker.Tracks), tracker.TotalEntered, tracker.TotalExited)

        time.Sleep(200 * time.Millisecond)
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Count entries and exits

The tracker already maintains `total_entered` and `total_exited` counters. Use them to count traffic through a monitored area.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# After running the tracker for a while:
print(f"Total objects entered: {tracker.total_entered}")
print(f"Total objects exited: {tracker.total_exited}")
print(f"Currently in scene: {len(tracker.tracks)}")

# You can also count by class
class_counts = {}
for track in tracker.tracks:
    class_counts[track.class_name] = (
        class_counts.get(track.class_name, 0) + 1
    )
for cls, count in class_counts.items():
    print(f"  {cls}: {count} active")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
fmt.Printf("Total objects entered: %d\n", tracker.TotalEntered)
fmt.Printf("Total objects exited: %d\n", tracker.TotalExited)
fmt.Printf("Currently in scene: %d\n", len(tracker.Tracks))

classCounts := make(map[string]int)
for _, track := range tracker.Tracks {
    classCounts[track.ClassName]++
}
for cls, count := range classCounts {
    fmt.Printf("  %s: %d active\n", cls, count)
}
```

{{% /tab %}}
{{< /tabs >}}

### 5. Tune tracking parameters

Two parameters control tracking behavior:

- **`iou_threshold`** (default 0.3): Minimum IoU required to match a detection to an existing track. Lower values allow more movement between frames but increase false matches. Higher values require objects to move slowly and may cause track fragmentation.
  - **Slow-moving objects or high frame rate:** use 0.3-0.5.
  - **Fast-moving objects or low frame rate:** use 0.1-0.3.

- **`max_lost_frames`** (default 10): How many consecutive frames a track can go undetected before being removed. Higher values handle brief occlusions (object behind another object) but delay exit detection.
  - **Static camera, reliable detections:** use 5-10.
  - **Occluded scenes or unreliable detections:** use 15-30.

## Try It

1. Run the tracking loop and walk in and out of the camera's field of view. Observe how the tracker assigns IDs and reports entries/exits.
2. Place two objects of the same class in the frame and move one. Verify the tracker maintains separate IDs.
3. Briefly occlude an object (cover the camera or block the object) and see if the tracker re-identifies it when it reappears within `max_lost_frames` frames.
4. Experiment with `iou_threshold` values. Set it to 0.1 and then 0.7 and observe how matching behavior changes.

## Troubleshooting

{{< expand "Tracks keep switching IDs" >}}

- The IoU threshold may be too low, causing detections to match the wrong track. Increase `iou_threshold` to 0.4 or 0.5.
- If objects are close together, the greedy matching algorithm may make suboptimal assignments. For crowded scenes, consider using the Hungarian algorithm for optimal matching instead of greedy matching.

{{< /expand >}}

{{< expand "Tracks are lost too quickly" >}}

- Increase `max_lost_frames`. If your detection model occasionally misses an object for a few frames, a higher value keeps the track alive through the gap.
- Check your detection confidence threshold. If it is too high, the model may intermittently fail to detect objects, causing track loss.

{{< /expand >}}

{{< expand "Too many new tracks for the same object" >}}

- This happens when the detection jitters (bounding box moves significantly between frames) and IoU drops below the threshold. Lower `iou_threshold` to be more lenient.
- If the detection model produces inconsistent bounding box sizes, the IoU can be low even when the boxes overlap. This is a model quality issue.

{{< /expand >}}

{{< expand "Entry/exit counts are wrong" >}}

- The tracker counts a new track as an entry and a lost track as an exit. If a track is lost and re-created (because the object left `max_lost_frames` without detection), it counts as one exit and one entry even though the object never left.
- For accurate counting, ensure your detection model is reliable and `max_lost_frames` is set high enough to cover temporary detection gaps.

{{< /expand >}}

## What's Next

- [Measure Depth](/vision/measure-depth/) -- combine tracking with depth data to track objects in 3D space.
- [Act on Detections](/vision/act-on-detections/) -- build modules that respond to detection or classification results.
- [Alert on Detections](/vision/alert-on-detections/) -- send alerts when tracked objects enter or exit a scene.
