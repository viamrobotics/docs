---
linkTitle: "Viam Visualization"
title: "Viam Visualization"
weight: 30
layout: "docs"
type: "docs"
description: "Run the standalone Viam Visualization app locally and push geometries, point clouds, and frame systems to it from a Go client."
aliases:
  - /visualization/drawing-library/
---

Viam Visualization is a standalone 3D visualizer for monitoring, testing, and debugging
spatial data: you start it locally and push visuals to it from your own Go code while
you develop. It renders the same entities the in-app **3D SCENE** tab renders, built
with the same `draw` library, so the visuals you construct work in either place.

This page covers running the app, pushing visuals from a Go client, and saving scenes
as snapshots.

## Viam Visualization versus the 3D scene tab

The two render 3D visuals, but they are different tools for different moments:

- The **3D SCENE tab** lives in the Viam app and renders a configured machine:
  its frames, geometry, point clouds, and the custom visuals published to its
  world state store service. It is the in-app view of a machine.
- **Viam Visualization** is a standalone visualizer you run on your own machine and push
  to from a client. It is for previewing and debugging spatial data while you
  develop, without deploying a module or opening the Viam app.

Reach for the 3D scene tab to inspect a running machine; reach for Viam
Visualization to iterate on spatial data from a script or test.

## Run the app

From the [motion-tools repository](https://github.com/viam-labs/motion-tools), run
`make setup` once, then `make up` to start the app at `http://localhost:5173`. It
renders in your browser. For prerequisites and incremental-rebuild details, see the
[Running locally guide](https://viamrobotics.github.io/visualization/guides/local-usage/).

To try the visualizer before installing anything, open the hosted
[playground](https://viamrobotics.github.io/visualization/playground/snapshot), which
renders a sample scene snapshot in your browser.

## Push visuals from a Go client

With the app running, push visuals to it with the client API from
`github.com/viam-labs/motion-tools/client/api`. Reusing an entity ID updates that
visual in place, so an iterating script animates state instead of piling up duplicates;
a new or empty ID adds another entity:

```go
import (
    "github.com/viam-labs/motion-tools/client/api"
    "github.com/viam-labs/motion-tools/draw"
)

// Reuse an ID to update that visual in place; change or omit it to add another.
_, err := api.DrawGeometry(api.DrawGeometryOptions{
    ID:       "obstacle-1",
    Geometry: box,
    Color:    draw.NewColor(draw.WithName("red")),
})
```

The client API has a call per data kind: geometries, point clouds, lines, NURBS, GLTF
models, single frames, and whole frame systems. Beyond plain shapes, the `draw` package
supplies the primitives you push, arrows for directions and normals, lines for paths,
points for sampled data, and styling options for each:

```go
import "github.com/viam-labs/motion-tools/draw"

shape := draw.NewShape(center, "approach", draw.WithArrows(arrows))
```

This lets you preview spatial data, a point cloud, a set of detections, a planned
path, straight from a script or test. For every call and option, see the generated
[client API reference](https://viamrobotics.github.io/visualization/api/client-api/).

## Connect to a live machine

The visualizer can also connect to a Viam machine and render its frame system, arms, and
cameras, the way the in-app **3D SCENE** tab does. Put the machine's credentials in a
<file>.env.local</file> file at the repository root, run `make up`, then pick the machine
in the machine config panel (lower right). For the credential format, see the
[Running locally guide](https://viamrobotics.github.io/visualization/guides/local-usage/#connecting-to-a-viam-machine).

## Save and load scene snapshots

A snapshot captures a scene as a JSON file you can share, commit as a test fixture, or
reload later. Build one in Go with the `draw` package, then drag the file onto either
viewer's viewport to load it:

```go
import "github.com/viam-labs/motion-tools/draw"

snapshot := draw.NewSnapshot(
    draw.WithSceneCamera(camera), // where the scene camera starts
    draw.WithGrid(true),
)
if err := snapshot.DrawGeometry(box, boxPose, "world", draw.ColorFromName("dodgerblue")); err != nil {
    return err
}
data, err := snapshot.MarshalJSON()
```

Name the output file with a `visualization_snapshot` prefix, for example
<file>visualization_snapshot_grasp_test.json</file>: the drag-and-drop loader accepts
only files that match that prefix.

## How updates reach the browser

The app runs a **draw service** that the client API calls. Each push becomes an
`AddEntity`, `UpdateEntity`, or `RemoveEntity` operation, and the service fans that
single change out over a `StreamEntity` stream the browser subscribes to. The browser
applies the one change instead of re-rendering the scene. This is the same add,
update, and remove model the world state store service uses to feed the in-app 3D
scene, so a busy scene stays in sync as your data changes.

## What's next

- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/):
  use the same `draw` library to serve transforms to the in-app 3D scene.
- [Transform metadata](/visualization/reference/transform-metadata/):
  the styling attributes behind colors, opacity, and visibility.
- [Visuals and collisions](/visualization/visuals-and-collisions/):
  what a transform contains and how the scene renders it.
