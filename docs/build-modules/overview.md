---
linkTitle: "Overview"
title: "Build and deploy modules"
weight: 1
layout: "docs"
type: "docs"
description: "Understand the two kinds of modules and how to extend your machine with custom hardware drivers and application logic."
aliases:
  - /build-modules/from-hardware-to-logic/
---

Modules extend what your machine can do. They come in two varieties: driver
modules that add support for new hardware, and logic modules that tie
components together with decision-making code. You can develop modules in your
own IDE or write them directly in the browser using
[inline modules](#inline-and-externally-managed-modules).

If you have already [configured components](/hardware/configure-hardware/) on
your machine, each one works individually: you can test it from the Viam app,
capture its data, and call its API from a script. The next step is making
them work **together**. A camera detects an object, and a motor responds. A
temperature sensor crosses a threshold, and a notification fires. A movement
sensor reports position, and an arm adjusts.

## Two kinds of modules

### Driver modules: add hardware support

A [driver module](/build-modules/write-a-driver-module/) teaches Viam how to
talk to a specific piece of hardware. It implements a standard component API
(sensor, camera, motor, etc.) for a device that `viam-server` does not support
out of the box.

You need a driver module when you have hardware with no existing model.
Once the driver module exists, the hardware behaves like any built-in component.
Data capture, test panels, and the SDKs work automatically.

### Logic modules: sense and act

A [logic module](/build-modules/write-a-logic-module/) reads from components
and takes action based on what it finds. It runs as a service alongside
`viam-server`, declares dependencies on the resources it needs, and implements
your application's decision-making.

Use a logic module when you need your machine to:

- **React to sensor data**: trigger an alert or an actuator when a reading
  crosses a threshold.
- **Coordinate multiple components**: read from a camera and command an arm
  based on what the camera sees.
- **Run continuous processes**: monitor, aggregate, or transform data from
  multiple sources.
- **Schedule actions**: perform operations at specific intervals or times.

## Choosing a resource API

Viam defines standard APIs for common resource types. Pick the API that best
matches your hardware or service:

| API               | Use when your hardware...                             | Key methods                        |
| ----------------- | ----------------------------------------------------- | ---------------------------------- |
| `sensor`          | Produces readings (temperature, distance, humidity)   | `GetReadings`                      |
| `camera`          | Produces images or point clouds                       | `GetImage`, `GetPointCloud`        |
| `motor`           | Drives rotational or linear motion                    | `SetPower`, `GoFor`, `Stop`        |
| `servo`           | Moves to angular positions                            | `Move`, `GetPosition`              |
| `board`           | Exposes GPIO pins, analog readers, digital interrupts | `GPIOPinByName`, `AnalogByName`    |
| `encoder`         | Tracks position or rotation                           | `GetPosition`, `ResetPosition`     |
| `movement_sensor` | Reports position, orientation, velocity               | `GetPosition`, `GetLinearVelocity` |
| `generic`         | Does not fit any of the above                         | `DoCommand`                        |

For the full list of component and service APIs, see
[Resource APIs](/dev/reference/apis/).

Using the right API means data capture, test panels, and other platform
features work with your component automatically.

Every resource also has a `DoCommand` method. Use it for functionality that
does not map to the standard API methods, for example, a sensor that also has
a calibration routine. `DoCommand` accepts and returns arbitrary key-value maps.

## The generic service API

Logic modules typically implement the `generic` service API, which has a single
method: `DoCommand`. It accepts an arbitrary key-value map and returns one.
This makes it a flexible interface for custom logic: you define your own command
vocabulary.

```json
// Request
{"command": "get_alerts", "severity": "critical"}

// Response
{"alerts": [{"sensor": "temp-1", "value": 42.5, "threshold": 40.0}]}
```

Use `generic` when your module's interface does not map to an existing service
API (like `vision` or `mlmodel`).

## Inline and externally managed modules

There are two ways to develop and deploy modules:

**Inline (Viam-hosted) modules** let you write code directly in the Viam app's
browser-based editor. Viam manages source code, builds, versioning, and
deployment. When you click **Save & Deploy**, the module builds in the cloud
and deploys to your machine automatically. Inline modules are the fastest way
to get started, especially for prototyping and simple control logic.

**Externally managed modules** are modules you develop in your own IDE, manage
in your own git repository, and deploy through the Viam CLI or GitHub Actions.
Use externally managed modules for production modules, public distribution, and
complex dependencies.

|                          | Inline (Viam-hosted)                                   | Externally managed                                            |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------------------------- |
| **Where you write code** | Browser editor in the Viam app                         | Your own IDE, locally or in a repo                            |
| **Source control**       | Managed by Viam                                        | Your own git repository                                       |
| **Build system**         | Automatic cloud builds on save                         | CLI upload or GitHub Actions                                  |
| **Versioning**           | Automatic (`0.0.1`, `0.0.2`, ...)                      | You choose semantic versions                                  |
| **Visibility**           | Private to your organization                           | Private or public                                             |
| **Best for**             | Prototyping, simple control logic, no-toolchain setups | Production modules, public distribution, complex dependencies |

Both types run identically at runtime, as child processes communicating with
`viam-server` over gRPC.

## Module lifecycle

Every module goes through a defined lifecycle:

1. **Startup** -- `viam-server` launches the module as a separate process. The
   module registers its models and opens a gRPC connection back to the server.
2. **Validation** -- For each configured resource, `viam-server` calls the
   model's config validation method to check attributes and declare
   dependencies.
3. **Creation** -- If validation passes, `viam-server` calls the model's
   constructor with the resolved dependencies.
4. **Reconfiguration** -- If the user changes the configuration, `viam-server`
   calls the validation method again, then the reconfiguration method.
5. **Shutdown** -- `viam-server` calls the resource's close method. Clean up
   resources here.

For the full lifecycle reference including crash recovery, first-run scripts,
and timeouts, see [Module developer reference](/build-modules/module-reference/#module-lifecycle).

## Dependencies

Dependencies let your resource use other resources on the same machine. You
declare dependencies in your config validation method by returning the names of
resources your module needs. `viam-server` resolves these, ensures the
depended-on resources are ready, and passes them to your constructor.

- **Required** dependencies must be running before your resource starts.
- **Optional** dependencies let your resource start immediately; `viam-server`
  retries every 5 seconds and reconfigures your resource when the dependency
  becomes available.

The pattern has three steps:

1. **Declare** -- return dependency names from your validation method.
2. **Resolve** -- look up each dependency from the map in your constructor.
3. **Use** -- call methods on the resolved dependencies in your logic.

For detailed code examples, see
[Module dependencies](/build-modules/dependencies/).

## The module registry

The Viam module registry stores versioned module packages and serves them to
machines on demand. When you configure a module on a machine, `viam-server`
downloads the correct version for the machine's platform (OS and architecture).

Modules can be:

- **Private** -- visible only to your organization.
- **Public** -- visible to all Viam users.
- **Unlisted** -- usable by anyone who knows the module ID, but not shown in
  registry search results.

The registry uses semantic versioning. Machines can track the latest version
(automatic updates) or pin to a specific version.

## Background tasks

Logic modules often need to run continuously: polling sensors, checking
thresholds, updating state. You can spawn background tasks (goroutines in Go,
async tasks in Python) from your constructor or reconfiguration method.

The key requirement: your background task must stop cleanly when the module
shuts down or reconfigures. Use a cancellation signal (a channel in Go, an
`asyncio.Event` in Python) to coordinate this.

## How it fits together

1. **Configure components** ([Configure hardware](/hardware/configure-hardware/)).
   Your machine can sense and act through individual hardware.
2. **Test interactively**. Use test panels in the Viam app and SDK scripts
   to verify each component works.
3. **Capture data** ([Capture and sync data](/data/capture-sync/capture-and-sync-data/)).
   Start recording what your sensors observe.
4. **Write a module**. Tie components together with decision-making code, or
   add support for new hardware.
5. **Deploy** ([Deploy a module](/build-modules/deploy-a-module/)).
   Package your module and deploy it to one machine or a fleet.

{{< cards >}}
{{% card link="/build-modules/write-an-inline-module/" %}}
{{% card link="/build-modules/write-a-driver-module/" %}}
{{% card link="/build-modules/write-a-logic-module/" %}}
{{% card link="/build-modules/deploy-a-module/" %}}
{{% card link="/build-modules/module-reference/" %}}
{{< /cards >}}
