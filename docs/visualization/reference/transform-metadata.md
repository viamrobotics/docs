---
linkTitle: "Transform metadata"
title: "Transform metadata"
weight: 20
layout: "docs"
type: "docs"
description: "The metadata keys the 3D scene reads from a transform, with the wire format for each: colors, opacities, axes helper, and visibility."
---

A transform's `metadata` field is a protobuf `Struct` of rendering attributes. The 3D
scene reads seven keys from it and ignores every other key. If a visual renders with
default styling, check the key names and formats on this page first: an unrecognized
key fails silently.

Metadata affects rendering only. The motion planner reads its geometry from the frame
system and the [`WorldState`](/visualization/reference/world-state/) you pass to `Move`,
so no metadata key changes what the planner plans around.

## The keys the scene reads

| Key                | Type            | What it controls                                                                  |
| ------------------ | --------------- | --------------------------------------------------------------------------------- |
| `colors`           | string (base64) | Fill color, or one color per point for point cloud geometry.                      |
| `color_format`     | number          | How the color bytes are laid out. The `draw` library writes the RGB format.       |
| `opacities`        | string (base64) | Transparency, `0` (invisible) to `255` (opaque). One byte, or one byte per point. |
| `show_axes_helper` | bool            | Draws a coordinate triad at the visual's origin.                                  |
| `invisible`        | bool            | Hides the visual by default; the viewer can re-enable it in the World panel.      |
| `chunks`           | object          | Streams a large entity in pieces: `chunk_size`, `total`, and `stride`.            |
| `relationships`    | list            | Links this entity to others, which powers features such as HoverLink.             |

## Color and opacity wire format

The binary values travel as base64-encoded strings, because a protobuf `Struct` has no
bytes type:

- `colors` packs 3 bytes per color, in R, G, B order. A single color styles the whole
  shape; for point cloud geometry, supply one color per point.
- `opacities` packs 1 byte per value. A single byte applies one opacity to the whole
  visual; a byte per point sets per-point transparency.

## Produce metadata with the draw library

The [`draw` library](https://github.com/viam-labs/motion-tools) encodes these formats
for you, so producer code sets options instead of packing bytes:

```go
import "github.com/viam-labs/motion-tools/draw"

// Red at half opacity. WithName, WithHex, WithRGB, and WithHSV also build colors.
drawn, err := draw.NewDrawnGeometry(
    box,
    draw.WithGeometryColor(draw.NewColor(draw.WithRGBA(255, 0, 0, 128))),
)
```

`WithMetadataColors`, `WithMetadataAxesHelper`, and `WithMetadataInvisible` set the
corresponding keys on a drawing. When you assemble the `Struct` in another language,
follow the wire formats in the table above.

## What's next

- [Visuals and collisions](/visualization/visuals-and-collisions/): the transform the
  metadata belongs to, and which geometry the planner collision-checks.
- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/): serve
  styled transforms to the 3D scene.
