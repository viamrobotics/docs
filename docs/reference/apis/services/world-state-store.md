---
title: "World state store API"
linkTitle: "World state store"
weight: 90
type: "docs"
tags: ["world_state_store", "services"]
description: "List, get, and stream the transforms a world state store service publishes for the 3D scene to draw."
icon: true
images: ["/icons/components/generic.svg"]
date: "2025-09-12"
# updated: ""  # When the content was last entirely checked
aliases:
  - /dev/reference/apis/services/world-state-store/
---

The world state store service API lets a client list, get, and stream the transforms a
world state store service publishes. The **3D SCENE** tab uses this API to render a
machine's [custom visuals](/visualization/visuals-and-collisions/), and a custom
visualizer you build can consume it the same way. To implement the service in a module,
see [Publish visuals from a module](/visualization/publish-visuals-from-a-module/).

The world state store service supports the following methods:

{{< readfile "/static/include/services/apis/generated/world_state_store-table.md" >}}

## Change stream semantics

Each update from `StreamTransformChanges` carries a change type and, depending on that type, a field mask that tells a consumer what to do with the update:

- **Added**: a new transform. The field mask is empty; use the whole transform.
- **Updated**: an existing transform changed. The field mask lists the field paths that changed, so a consumer can apply a partial update instead of replacing the whole transform.
- **Removed**: a transform was removed. The field mask holds the transform's UUID path.

In the Go SDK, `StreamTransformChanges` returns a `*TransformChangeStream`, not a channel: call `Next()` repeatedly and stop on `io.EOF`, as shown in the Go example below. The Python and TypeScript SDKs expose the same stream as a native async iterator instead.

## API

{{< readfile "/static/include/services/apis/generated/world_state_store.md" >}}
