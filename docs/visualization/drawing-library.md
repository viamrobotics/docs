---
linkTitle: "Drawing library"
title: "The drawing library and Viam visualization"
weight: 30
layout: "docs"
type: "docs"
description: "Use the draw library to build visuals, and run the standalone Viam Visualization app to preview spatial data from a Go client."
---

Viam Visualization is a standalone 3D app you run yourself. Unlike the **3D
SCENE** tab in the Viam app, which renders a machine's world state store service,
Viam Visualization is a separate tool for monitoring, testing, and debugging
spatial data: you start it locally and push visuals to it from your own Go code.
It shares the same `draw` library used to build world state store transforms, so
the visuals you construct are the same either way.

This page covers what the drawing library is, the primitives it exposes, and how
to run the app and drive it from a Go client.

## Viam Visualization versus the 3D scene tab

The two render 3D visuals, but they are different tools for different moments:

- The **3D SCENE tab** lives in the Viam app and renders a machine's world state
  store service. It is the in-app view of a configured machine.
- **Viam Visualization** is a standalone app you run on your own machine and push
  to from a client. It is for previewing and debugging spatial data while you
  develop, without deploying a module or opening the Viam app.

Reach for the 3D scene tab to inspect a running machine; reach for Viam
Visualization to iterate on spatial data from a script or test.

## What the drawing library is

The `draw` library turns geometry, pose, and styling metadata into the entities
the renderer displays. Instead of assembling proto structs by hand, you describe
a shape and its appearance and the library produces a correct, fully-formed
visual with the right identifiers and metadata. The same library backs both
render targets: it builds the `commonpb.Transform` values a world state store
module serves, and the entities you push to Viam Visualization.

## Drawing primitives and styling

The library exposes a set of drawable shapes and styling options. Pick the
primitive that matches what you are drawing:

- **arrows**: directions, normals, or vectors
- **lines**: paths, segments, or connections
- **points**: sampled data or markers
- **models**: detailed 3D meshes
- **NURBS**: smooth curves and surfaces

Each visual takes styling options: color, opacity, per-point colors for point
data, and a label. Choosing the right primitive and styling keeps a busy scene
readable, for example drawing a trajectory as a line, its waypoints as points,
and approach directions as arrows.

## Construct visuals with the library

Building visuals with the library rather than by hand keeps producer code
readable and guarantees the identifiers and metadata are correct. You construct
a shape with a styling option and let the library assemble the entity:

```go
import "github.com/viam-labs/motion-tools/draw"

shape := draw.NewShape(center, "approach", draw.WithArrows(arrows))
```

Because the library owns the proto details, you work in terms of shapes and
styles, not field-by-field struct assembly.

## Run the app and push from a Go client

Viam Visualization runs locally and renders in your browser. You start the app,
then push visuals to it from Go with the client API. Reusing an entity ID updates
that visual in place; a new ID adds another:

```go
import "github.com/viam-labs/motion-tools/client/api"

// Update in place by reusing the ID; add a new entity with a different ID.
err := api.DrawGeometry(box, api.WithID("obstacle-1"), api.WithColor(red))
```

This lets you preview spatial data, a point cloud, a set of detections, a planned
path, straight from a script or test, without deploying a module or connecting
through the Viam app. For setup, the local server, and the full client API, see
the [Viam Visualization documentation](https://viamrobotics.github.io/visualization/).

## What's next

- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/):
  use the same `draw` library to serve transforms to the in-app 3D scene.
- [Visuals and collisions](/visualization/visuals-and-collisions/):
  what a transform contains and how the scene renders it.
