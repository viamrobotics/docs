---
linkTitle: "Publish visuals from a module"
title: "Publish custom visuals from a module"
weight: 20
layout: "docs"
type: "docs"
description: "Implement a world state store service that pulls data from other resources, builds transforms with the draw library, and streams them to the 3D scene."
---

The 3D scene shows your frame system and configured geometry by default. To draw
anything else, a detected object, a planned path, a sensor's live readings as
shapes, you implement a **world state store service**. A module that implements
this service is a producer: it reads data from other resources, turns that data
into transforms, and streams them to the scene as they change.

This page covers when to implement the service, the methods to implement, how
to build transforms with the `draw` library, and the poll-and-update loop that
keeps the scene in sync. The pattern throughout is **pull**: the module depends
on the resources it visualizes and reads their data, rather than having those
resources push into it.

## When to implement a world state store service

Implement one when you want custom visuals in the 3D scene beyond the default
content. The scene already draws component frames and configured geometry on its
own. A module adds anything computed or sensed at runtime: a vision service's
detections, a sensor's obstacle readings, a motion plan's trajectory, or any
annotation specific to your application.

## Implement the service methods

The world state store service exposes three read methods, which the 3D scene
calls to discover and follow your visuals:

- `ListUUIDs`: return the UUID of every transform you currently publish.
- `GetTransform`: return the transform for a given UUID.
- `StreamTransformChanges`: return a stream of change events so the scene
  follows additions, updates, and removals without re-fetching everything.

A typical implementation keeps the current transforms in a map keyed by UUID,
serves `ListUUIDs` and `GetTransform` from that map, and fans out change events
to subscribers from `StreamTransformChanges`.

```go
func (s *visualizer) ListUUIDs(
    ctx context.Context, extra map[string]any,
) ([][]byte, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    uuids := make([][]byte, 0, len(s.transforms))
    for id := range s.transforms {
        uuids = append(uuids, []byte(id))
    }
    return uuids, nil
}
```

## Build transforms with the draw library

Rather than assembling `commonpb.Transform` protos by hand, use the `draw`
library from `github.com/viam-labs/motion-tools/draw`. You wrap a
`spatialmath.Geometry` with styling, then `Draw` it with an ID and pose to get a
`*commonpb.Transform`:

```go
import (
    "github.com/viam-labs/motion-tools/draw"
    "go.viam.com/rdk/spatialmath"
)

func buildTransform(o obstacle) (*commonpb.Transform, error) {
    box, err := spatialmath.NewBox(o.Pose, o.Dims, o.ID)
    if err != nil {
        return nil, err
    }
    drawn, err := draw.NewDrawnGeometry(box, draw.WithGeometryColor(colorFor(o)))
    if err != nil {
        return nil, err
    }
    return drawn.Draw(o.ID, draw.WithID(o.ID), draw.WithPose(o.Pose))
}
```

The library produces standard `commonpb.Transform` values, the same type the
service methods return, so the transforms you build this way flow straight
through `ListUUIDs`, `GetTransform`, and `StreamTransformChanges` to the scene.

## Drive a poll-and-update loop

The module owns its update cadence. A ticker drives a loop that reads the
module's dependencies, builds the current set of transforms, diffs it against the
cached set, and emits one change event per difference:

```go
func (s *visualizer) pollLoop() {
    for range s.ticker.C {
        readings, err := s.sensor.Readings(s.ctx, nil)
        if err != nil {
            continue
        }
        next := buildTransforms(readings)

        // Diff next against s.last and emit one event per change.
        for id, tf := range next {
            if prev, ok := s.last[id]; !ok {
                s.emit(tf, pb.TransformChangeType_TRANSFORM_CHANGE_TYPE_ADDED, nil)
            } else if changed(prev, tf) {
                s.emit(tf, pb.TransformChangeType_TRANSFORM_CHANGE_TYPE_UPDATED, changedFields(prev, tf))
            }
        }
        for id, tf := range s.last {
            if _, ok := next[id]; !ok {
                s.emit(tf, pb.TransformChangeType_TRANSFORM_CHANGE_TYPE_REMOVED, nil)
            }
        }
        s.last = next
    }
}
```

Emitting added, updated, and removed events (with `UpdatedFields` on updates)
lets the scene apply incremental changes instead of re-rendering. The diff
against cached state is what turns a full snapshot each tick into a stream of
minimal updates.

## Pull from the resources you visualize

The module is the producer, and the resources it visualizes are its
dependencies. The 3D scene reads only the world state store service; the service
reads everything else. Data flows one way:

> dependency resources → world state store module (reads, builds transforms) → 3D scene

This is why the loop above calls `s.sensor.Readings(...)`: the sensor is a
dependency, and the module pulls from it. The same pattern visualizes any other
resource. A module whose primary job is something else (an arm, a sensor, a
planner) stays focused on that job. To visualize it, you write a separate world
state store module that takes that resource as a dependency and pulls from its
existing API:

- a sensor's `Readings`
- a component's geometry getters
- any resource's `DoCommand`

The visualized resource needs no changes and no awareness that it is being drawn.
The store depends on it, not the other way around.

```go
func newVisualizer(deps resource.Dependencies, conf resource.Config) (worldstatestore.Service, error) {
    obstacleSensor, err := sensor.FromProvider(deps, "obstacle-sensor")
    if err != nil {
        return nil, fmt.Errorf("getting obstacle-sensor: %w", err)
    }
    // The module depends on obstacle-sensor and pulls its readings on a loop.
    return startVisualizer(obstacleSensor), nil
}
```

## What's next

- [Visuals and collisions](/visualization/visuals-and-collisions/):
  what a transform contains, and which geometry the planner collision-checks.
- [The drawing library and Viam visualization](/visualization/drawing-library/):
  the `draw` primitives and the standalone visualizer app.
- [Frame system](/motion-planning/frame-system/): position the transforms you
  publish.
