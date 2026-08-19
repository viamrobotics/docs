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

## API

{{< readfile "/static/include/services/apis/generated/world_state_store.md" >}}
