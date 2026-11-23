---
title: "World state store service"
linkTitle: "World state store"
weight: 85
type: "docs"
layout: "docs"
description: "Configure the built-in world state store, which holds transforms in memory for the 3D scene to draw, and change them with DoCommand."
capabilities: ["frame-system", "scene-3d"]
diataxis: reference
tags: ["world_state_store", "services"]
date: "2026-11-18"
---

A world state store service holds transforms, each a named reference frame with a pose and an optional geometry, and publishes them for the **3D SCENE** tab to draw.
For the methods a client calls to read them, see the [world state store API](/reference/apis/services/world-state-store/).

`viam-server` v1.17.0 and later include a built-in model, `rdk:builtin:builtin`, that keeps transforms in memory.
Use it when you want to put shapes in the scene from a script or another resource without writing a module.
To compute transforms in your own code and serve them from a module instead, see [Publish visuals from a module](/visualization/publish-visuals-from-a-module/).

The built-in store holds transforms for the scene to draw.
The motion planner does not plan around them; for that, see [the scene draws, the planner collision-checks](/visualization/visuals-and-collisions/#the-scene-draws-the-planner-collision-checks).

## Configure the built-in store

The built-in world state store is not added to a machine by default.
Add it to the machine's JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "world_state_store",
  "api": "rdk:service:world_state_store",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "transforms": [
      {
        "referenceFrame": "table",
        "poseInObserverFrame": {
          "referenceFrame": "world",
          "pose": { "x": 500, "y": 0, "z": -20, "oZ": 1, "theta": 0 }
        },
        "physicalObject": {
          "box": { "dimsMm": { "x": 1000, "y": 600, "z": 40 } },
          "label": "table"
        }
      }
    ]
  }
}
```

You can't name the service `builtin`, because the default motion service already uses that name.

The following attribute is available:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `transforms` | array | Optional | Transforms the store holds when it starts, for parts of the world you know ahead of time. Each is a transform in its proto JSON form, the same form the `add` command takes. A transform without a `uuid` uses its `referenceFrame` name as its UUID, so it keeps the same UUID each time the store starts. |

Every transform needs a `referenceFrame` and a `poseInObserverFrame` with its own `referenceFrame`, the frame the pose is expressed in.
Distances are in millimeters.
Orientation is an [orientation vector](/motion-planning/reference/orientation-vectors/): `oX`, `oY`, and `oZ` give the direction the frame points, and `theta` is a rotation around that direction in degrees.
If any configured transform is invalid, the configuration fails validation.

The store keeps everything in memory.
Transforms you add at runtime are lost when `viam-server` restarts or the service is rebuilt, which includes any change to its `transforms` attribute.
After that, the store starts again from its configured transforms.

## Change transforms with DoCommand

Add, update, and remove transforms at runtime with the service's `DoCommand`.
Each command takes a list of transforms, written in proto JSON.
In that form a `uuid` is base64-encoded: `"Ym94"` is the UUID `box`.
A configured transform without a `uuid` has its `referenceFrame` name as its UUID, so the `table` transform in the configuration above has the UUID `"dGFibGU="`.

<!-- prettier-ignore -->
| Command | Each item | Behavior |
| ------- | --------- | -------- |
| `add` | A whole transform | Adds it. An item without a `uuid` gets a random one, which the response reports. Adding a UUID that is already stored is an error. |
| `update` | The `uuid` and only the fields to change | Sets those fields and leaves the rest. A field sent as `null` is cleared. To name the fields to take from the item instead, add an `updatedFields` list of paths, such as `["poseInObserverFrame.pose.x"]`; then everything else in the item is ignored. A path can name a whole message, which is replaced, but can't reach inside a list or map. An update must change at least one field, and can't change the `uuid`. Updating a UUID that isn't stored is an error. |
| `remove` | Only the `uuid` | Removes the transform. Removing a UUID that isn't stored is an error. |

For example, to add a box, then set its x coordinate to 5 and leave the rest of its pose unchanged:

```json
{
  "add": [
    {
      "uuid": "Ym94",
      "referenceFrame": "box",
      "poseInObserverFrame": {
        "referenceFrame": "world",
        "pose": { "x": 0, "y": 0, "z": 100, "oZ": 1, "theta": 0 }
      },
      "physicalObject": {
        "box": { "dimsMm": { "x": 50, "y": 50, "z": 50 } }
      }
    }
  ]
}
```

```json
{
  "update": [{ "uuid": "Ym94", "poseInObserverFrame": { "pose": { "x": 5 } } }]
}
```

One call can carry any combination of the three commands.
The store applies them in the order `remove`, `add`, `update`, whatever order you write them in, so one call can replace a transform by removing it and adding it again under the same UUID.
A call applies everything it carries or nothing: if any item is invalid, the store is left unchanged, and the error names the command and the item's index, for example `update[1]: transform "box" not found`.

The response lists, for each command in the call, the base64 UUID of each transform it changed, in the order of its list:

```json
{ "add": ["Ym94"], "remove": ["b2xk"] }
```

### Send commands from Python

From the Python SDK, call `do_command` on the service, and base64-encode each UUID yourself:

```python {class="line-numbers linkable-line-numbers"}
import base64

from viam.services.worldstatestore import WorldStateStore


def b64(name: str) -> str:
    return base64.b64encode(name.encode()).decode()


store = WorldStateStore.from_robot(machine, "world_state_store")

# Add a box 100 mm above the world origin.
await store.do_command({
    "add": [{
        "uuid": b64("box"),
        "referenceFrame": "box",
        "poseInObserverFrame": {
            "referenceFrame": "world",
            "pose": {"x": 0, "y": 0, "z": 100, "oZ": 1, "theta": 0},
        },
        "physicalObject": {"box": {"dimsMm": {"x": 50, "y": 50, "z": 50}}},
    }]
})

# Raise the configured table by 10 mm. Its UUID is its frame name.
await store.do_command({
    "update": [{
        "uuid": b64("table"),
        "poseInObserverFrame": {"pose": {"z": -10}},
    }]
})
```

## What a client sees

A client that streams changes with `StreamTransformChanges`, such as the **3D SCENE** tab, first receives every transform in the store as an added change, then each later change in the order the store applied it.
The stream ends if its client falls far behind, or when the service closes; open a new stream to start again from the store's current contents.
`ListUUIDs` returns the UUIDs in no particular order, and `GetTransform` returns one transform by UUID.
