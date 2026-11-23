---
title: "Composite models"
linkTitle: "Composite models"
weight: 21
type: "docs"
layout: "docs"
description: "How one model serves several resource APIs as a single device, and when a module should provide one."
capabilities: ["module-development"]
diataxis: explanation
date: "2026-11-23"
---

A composite model is one model that serves more than one resource API.
A device that is both a camera and a movement sensor can be a single composite: one config entry, one name, one running instance, reachable as a camera and as a movement sensor.

Without composites, a module author has two choices for a multi-capability device: pick one API and expose the rest through `DoCommand`, or ship one model per API and ask users to configure each one separately.
This page explains how a composite behaves on a machine, which API handles methods that more than one of its APIs share, and when to build one instead of separate models.

## One model, several APIs {#one-model-several-apis}

A module registers a composite model under every API it serves.
A user adds it to a machine with one config entry, and the `api` in that entry can be any one of the model's APIs.
`viam-server` reads the full set from the module, so the entry doesn't list the others.

On the machine, the composite is one resource with one lifecycle.
`viam-server` constructs it once, reconfigures it once, and closes it once.
It advertises the resource once per API, under the same name:

```text
rdk:component:camera/combo
rdk:component:movement_sensor/combo
```

Because resource names are unique across a machine, clients use the shared name to tell that these entries are one device.

## How clients reach each API {#how-clients-reach-each-api}

Every SDK can reach a composite through each API's usual getter, with no changes to client code.
In Go, `camera.FromProvider(machine, "combo")` returns the camera, and `movementsensor.FromProvider(machine, "combo")` returns the movement sensor of the same device.

The Go SDK also has helpers for working with the device as one handle:

| Helper                                       | What it returns                                                                                                             |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `resource.NamedFromProvider(provider, name)` | The resource with that name, without naming an API. For a composite, one handle that serves every API.                      |
| `resource.APIsOf(res)`                       | The APIs the handle serves.                                                                                                 |
| `resource.AsType[T]`                         | Called on the handle, the part of it that serves the API with interface `T`, or a `TypeError` if it doesn't serve that API. |

Other SDKs don't have these helpers yet, and composite models can only be written in Go.

## Which API handles shared methods {#which-api-handles-shared-methods}

Some methods belong to every API, such as `DoCommand` and `Status`.
A composite routes these to its canonical API: the API that sorts first alphabetically.
For a model serving `rdk:component:camera` and `rdk:component:movement_sensor`, that's the camera.

Data capture assigns each captured method to the API that owns it.
A method only one of the composite's APIs captures, such as `Readings` on a sensor, is tagged with that API, whichever API the config entry names.
A method that several of its APIs capture, such as `DoCommand`, is captured under the API in the config entry, unless the capture config names a different one.
See [Capture from a composite](/data/capture-sync/capture-and-sync-data/#capture-from-a-composite).

## Why one resource instead of several {#why-one-resource-instead-of-several}

A multi-capability device usually has one connection and one set of state: a serial port, a USB handle, a calibration.
Separate models for each capability each open that connection, or they coordinate through a shared global inside the module.
Either way, each copy can be configured, restarted, and fail on its own, while the hardware can't.

A composite keeps one owner for that state.
The module builds one object, `viam-server` manages one lifecycle for it, and the user configures it once.
Separate models are still the right choice when the capabilities are physically separable.

## Composites versus separate models {#composites-versus-separate-models}

| The device                                                                        | Build                                                       |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Is one physical unit with one connection, such as a camera with a built-in IMU    | A composite                                                 |
| Has parts that users mount, place, or replace separately                          | Separate models in one module                               |
| Needs a separate frame for each capability, such as a camera offset from a sensor | Separate models: a composite has one frame                  |
| Has capabilities some users won't want                                            | Separate models: a composite serves all of its APIs or none |
| Serves more than one of arm, gantry, and gripper                                  | Separate models: a composite can serve at most one of these |

## What composites don't do {#what-composites-dont-do}

- **Serve more than one kinematic API.** The frame system handles one kinematic part per resource, so a model that registers more than one of arm, gantry, or gripper panics when the module starts.
- **Have a frame per API.** A composite has one frame in the frame system, set in its config entry.
- **Let users turn off one API.** Every config entry for the model serves all of its APIs, whether or not the user calls them.
- **Run on older `viam-server` versions.** Composites need `viam-server` v1.17.0 or later.

## What's next {#whats-next}

- [Build a composite model](/build-modules/build-a-composite-model/): register a Go model under several APIs and declare them in `meta.json`.
- [Write a driver module](/build-modules/write-a-driver-module/): build a single-API module first, if you haven't written one.
- [Module developer reference](/build-modules/module-reference/#metajson-schema): the `apis` field in `meta.json`.
