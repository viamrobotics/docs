---
linkTitle: "draw library"
title: "draw library"
weight: 30
layout: "docs"
type: "docs"
description: "Lookup tables for the draw library: placement and identity options, shape constructors, colors, metadata, and snapshot options."
---

The [`draw` library](https://pkg.go.dev/github.com/viam-labs/motion-tools/draw)
(`github.com/viam-labs/motion-tools/draw`) builds the transforms and entities that the 3D
scene and [Viam Visualization](/visualization/viam-visualization/) render. This page lists
the options you reach for while writing a producer. The library lives in `viam-labs` and
moves faster than the RDK, so treat
[pkg.go.dev](https://pkg.go.dev/github.com/viam-labs/motion-tools/draw) as the full and
current inventory.

## Placement and identity

Options for `Draw` calls and `NewDrawConfig`, all of type `DrawableOption`:

| Option           | What it sets                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------ |
| `WithParent`     | The reference frame the pose is expressed in. Defaults to `world`.                         |
| `WithPose`       | The entity's pose in the parent frame.                                                     |
| `WithCenter`     | An offset applied at the entity's own center.                                              |
| `WithID`         | A string identity; the library derives a stable UUID from it, so re-sends update in place. |
| `WithUUID`       | An explicit UUID, when you manage identity yourself.                                       |
| `WithAxesHelper` | Draws a coordinate triad at the entity's origin.                                           |
| `WithInvisible`  | Hides the entity by default; the viewer can re-enable it.                                  |

## Shapes

| Constructor                           | Builds                                                                              |
| ------------------------------------- | ----------------------------------------------------------------------------------- |
| `NewDrawnGeometry`                    | A styled `spatialmath.Geometry`; its `Draw` method returns a `*commonpb.Transform`. |
| `NewShape` + `WithArrows`             | Arrows, for directions, normals, or vectors.                                        |
| `NewShape` + `WithLine` / `NewLine`   | A line, for paths, segments, or connections.                                        |
| `NewShape` + `WithPoints`             | Points, for sampled data or markers.                                                |
| `NewShape` + `WithModel`              | A detailed 3D mesh model.                                                           |
| `NewShape` + `WithNurbs` / `NewNurbs` | A smooth NURBS curve or surface.                                                    |

Style a geometry with `WithGeometryColor` (one color) or `WithGeometryColors` (per-point
colors) when you call `NewDrawnGeometry`.

## Colors

Build a `Color` with `NewColor` plus one option, or use the one-call helpers:

| With `NewColor` | Helper          | Input                                  |
| --------------- | --------------- | -------------------------------------- |
| `WithRGB`       | `ColorFromRGB`  | `r, g, b` as 0 to 255                  |
| `WithRGBA`      | `ColorFromRGBA` | `r, g, b` plus alpha for opacity       |
| `WithName`      | `ColorFromName` | A CSS color name, such as `dodgerblue` |
| `WithHex`       | `ColorFromHex`  | A hex string                           |
| `WithHSV`       | `ColorFromHSV`  | Hue, saturation, value                 |

## Metadata

Options for `NewDrawing` and `NewTransform`, all of type `DrawMetadataOption`. Each writes
one of the [metadata keys](/visualization/reference/transform-metadata/) the scene reads:

| Option                      | Metadata it writes                           |
| --------------------------- | -------------------------------------------- |
| `WithMetadataColors`        | `colors` (and `opacities` from alpha)        |
| `WithMetadataAxesHelper`    | `show_axes_helper`                           |
| `WithMetadataInvisible`     | `invisible`                                  |
| `WithMetadataRelationships` | `relationships`, for links such as HoverLink |

## Snapshots

Options for `NewSnapshot`, which builds a loadable
[scene snapshot](/visualization/viam-visualization/#save-and-load-scene-snapshots):

| Option                                      | What it sets                                       |
| ------------------------------------------- | -------------------------------------------------- |
| `WithSceneCamera`                           | Where the scene camera starts.                     |
| `WithGrid`, `WithGridCellSize`              | The reference grid and its cell size.              |
| `WithScenePointSize`, `WithScenePointColor` | Default point rendering.                           |
| `WithRenderArmModels`                       | Whether arms render as colliders, models, or both. |

## What's next

- [Transform metadata](/visualization/reference/transform-metadata/): the wire formats
  behind the metadata options.
- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/): the
  library in a world state store module.
- [Viam Visualization](/visualization/viam-visualization/): the library from a script,
  pushed to the standalone visualizer.
