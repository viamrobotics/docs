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
talk to a specific piece of hardware. Every module implements one of Viam's
resource APIs. For a driver module, you pick the component API that matches
your hardware:

| API      | Use when your hardware...                           | Key methods                              |
| -------- | --------------------------------------------------- | ---------------------------------------- |
| `sensor` | Produces readings (temperature, distance, humidity) | `GetReadings`                            |
| `camera` | Produces images or point clouds                     | `GetImage`, `GetPointCloud`              |
| `motor`  | Drives rotational or linear motion                  | `SetPower`, `GoFor`, `Stop`              |
| `arm`    | Has joints and moves to poses                       | `MoveToPosition`, `MoveToJointPositions` |
| `base`   | Is a mobile platform (wheeled, tracked, legged)     | `MoveStraight`, `Spin`, `SetVelocity`    |

Viam defines over 15 component APIs and 10 service APIs. For the full list,
see [Resource APIs](/dev/reference/apis/).

Each implementation of a resource API is called a **model**. For example,
the `camera` API has models for USB cameras, CSI cameras, RTSP streams, and
others. When no existing model supports your hardware,
you write a driver module to add one. Once it exists, the hardware behaves
like any built-in component. Data capture, test panels, and the SDKs work
automatically.

### Logic modules: sense and act

A [logic module](/build-modules/write-a-logic-module/) controls your machine's
behavior. It declares dependencies on the resources it needs and implements
your application's decision-making. Many logic modules run continuously on
your machine, reading from sensors, evaluating conditions, and commanding
actuators.

Use a logic module when you need your machine to:

- **React to sensor data**: trigger an alert or an actuator when a reading
  crosses a threshold.
- **Coordinate multiple components**: read from a camera and command an arm
  based on what the camera sees.
- **Run continuous processes**: monitor, aggregate, or transform data from
  multiple sources.
- **Schedule actions**: perform operations at specific intervals or times.

Logic modules typically implement the `generic` service API. The generic API
has a single method, `DoCommand`, which accepts and returns arbitrary key-value
maps. Use it to check status, adjust parameters, or send commands to your
running module from external scripts or the Viam app:

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

**Inline modules** let you write code directly in the Viam app's
browser-based editor. Viam manages source code, builds, versioning, and
deployment. When you click **Save & Deploy**, the module builds in the cloud
and deploys to your machine automatically. Inline modules are the fastest way
to get started, especially for prototyping and simple control logic.

**Externally managed modules** are modules you develop in your own IDE, manage
in your own git repository, and deploy through the Viam CLI or GitHub Actions.
Use externally managed modules when you need your own source control, public
distribution, or custom build pipelines.

|                          | Inline                            | Externally managed                           |
| ------------------------ | --------------------------------- | -------------------------------------------- |
| **Where you write code** | Browser editor in the Viam app    | Your own IDE, locally or in a repo           |
| **Source control**       | Managed by Viam                   | Your own git repository                      |
| **Build system**         | Automatic cloud builds on save    | Cloud build (GitHub Actions) or local builds |
| **Versioning**           | Automatic (`0.0.1`, `0.0.2`, ...) | You choose semantic versions                 |
| **Visibility**           | Private to your organization      | Private or public                            |

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

## Attributes

Attributes are the user-provided configuration for your resource. When someone
adds your module to a machine, they set attributes in the Viam app or in the
machine's JSON config. Examples include a device address for a driver module,
or a polling interval and threshold for a logic module.

Your module defines which attributes it expects and validates them in its
config validation method. If validation fails, `viam-server` reports the error
and does not create the resource. Attributes are passed to your constructor
when the resource is created and again to your reconfiguration method when
the configuration changes.

For code examples, see the attribute definitions in
[Write a driver module](/build-modules/write-a-driver-module/#define-your-config-attributes)
and [Write a logic module](/build-modules/write-a-logic-module/).

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
shuts down or reconfigures. Use a cancellation signal (a context cancellation
in Go, an `asyncio.Event` in Python) to coordinate this.

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

If you want to build a client app that talks to a machine from outside `viam-server` rather than extending the server itself, see [Build apps](/build-apps/).
