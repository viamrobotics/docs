---
linkTitle: "draw library"
title: "draw library"
weight: 30
layout: "docs"
type: "docs"
description: "A map of the draw library's option categories: placement and identity, shapes, colors, metadata, and snapshots, with links to the full API."
---

The [`draw` library](https://pkg.go.dev/github.com/viam-labs/motion-tools/draw)
(`github.com/viam-labs/motion-tools/draw`) builds the transforms and entities that the 3D
scene and [Viam Visualization](/visualization/viam-visualization/) render. This page maps
the library's option categories to what they control. The library lives in `viam-labs` and
moves faster than the RDK, so the project's
[generated API docs](https://viamrobotics.github.io/visualization/api/draw/) and
[pkg.go.dev](https://pkg.go.dev/github.com/viam-labs/motion-tools/draw) carry the
option-by-option detail and stay current as the library changes.

## Placement and identity

`Draw` calls and `NewDrawConfig` take `DrawableOption` values that place an entity and
give it an identity: the parent reference frame (`world` by default), the pose in that
frame, and an offset at the entity's own center. Identity is the option that matters most:
pass a string ID and the library derives a stable UUID from it, so re-sending the same ID
updates the entity in place instead of adding a duplicate. Options in this category also
toggle the entity's axes helper and its default visibility.

## Shapes

`NewDrawnGeometry` wraps a `spatialmath.Geometry` with styling; its `Draw` method returns
the `*commonpb.Transform` that a world state store service serves. `NewShape` builds the
drawing primitives: arrows for directions and normals, lines for paths, points for
sampled data, mesh models, and NURBS curves, each with its own option set.

## Colors

`NewColor` composes a `Color` from one option: RGB values, RGBA with alpha carrying
opacity, a CSS color name such as `dodgerblue`, a hex string, or HSV. Each form also has a
one-call `ColorFrom*` helper.

## Metadata

`NewDrawing` and `NewTransform` take `DrawMetadataOption` values, each of which writes one
of the metadata keys the scene reads: colors and opacities, the axes helper, default
visibility, and entity relationships such as HoverLink. The key names and wire formats are
on [Transform metadata](/visualization/reference/transform-metadata/).

## Snapshots

`NewSnapshot` builds a loadable
[scene snapshot](/visualization/viam-visualization/#save-and-load-scene-snapshots); its
options set the starting scene camera, the reference grid, default point rendering, and
whether arms render as colliders, models, or both.

## What's next

- [Transform metadata](/visualization/reference/transform-metadata/): the wire formats
  behind the metadata options.
- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/): the
  library in a world state store module.
- [Viam Visualization](/visualization/viam-visualization/): the library from a script,
  pushed to the standalone visualizer.
