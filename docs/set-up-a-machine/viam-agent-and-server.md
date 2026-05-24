---
linkTitle: "viam-agent and viam-server"
title: "viam-agent and viam-server"
weight: 10
layout: "docs"
type: "docs"
description: "The two programs that run on every Viam machine: what each does, how they relate, and how they run modules."
date: "2026-04-17"
---

When you install Viam on a computer, two programs land on the machine: `viam-agent` and `viam-server`. They have distinct jobs.

## viam-server

`viam-server` is the runtime that gives your machine its behavior.
It reads the machine's configuration, loads each component and service, and exposes them through APIs so your code, the Viam app, and other machines can control them.
`viam-server` listens on gRPC, HTTP, and (when signaled) WebRTC. That is how an SDK connects to the machine.

Most of what people mean by "Viam running on my robot" is `viam-server`. When you write SDK code that calls `Motor.from_robot(...)`, that connection terminates at `viam-server` on the machine.

## viam-agent

`viam-agent` is a process manager that sits above `viam-server`.
It runs as a system service (systemd on Linux, launchd on macOS) and manages three subsystems:

- **viam-server**: launches it, restarts it on unexpected exit, and applies version updates from the cloud.
- **networking**: helps with connectivity when the machine boots, including Wi-Fi provisioning on supported platforms.
- **syscfg**: applies machine-level system configuration.

`viam-agent` is the always-on layer. If the machine reboots, `viam-agent` comes up first and starts `viam-server`. If `viam-server` crashes, `viam-agent` restarts it.

## How they work together

At a typical startup, the OS starts the systemd or launchd service, which runs `viam-agent`. `viam-agent` starts `viam-server` as a subprocess, monitors it, and handles restarts. If a new `viam-server` version is released and your cloud config permits it, `viam-agent` downloads and installs the update, then restarts `viam-server` on the new version.

You interact with `viam-server` through the Viam app, the CLI, and SDKs. You do not typically interact with `viam-agent` directly unless you are troubleshooting install or version-update issues.

## How viam-server runs modules

A **module** is a code package that provides one or more models (implementations of Viam component or service APIs for specific hardware or software).
Most hardware support comes from modules in the [Viam registry](https://app.viam.com/registry), not from built-ins.

### Pulling and caching

When `viam-server` receives a config from the cloud, it looks at the `modules` block.
For each registry module, `viam-server` asks the Viam package service where to download the module, fetches it over HTTP, and caches it locally under the machine's packages directory.

Subsequent config syncs check which packages have changed.
Unchanged modules are not re-downloaded; `viam-server` reuses the local copy.
This is what lets a machine reboot or reconnect after a network outage without pulling everything again.

### Launching modules as subprocesses

Each module runs as a separate subprocess, not as library code inside `viam-server`.
`viam-server` opens a UNIX domain socket in a temporary directory, passes the socket path to the module when it launches, and the module connects back over gRPC on that socket.
The parent-child relationship keeps module crashes from bringing down `viam-server`.

### Restarting a module

If a module exits unexpectedly, `viam-server` restarts it automatically.
If you change the module's config (version, attributes, or anything else that changes the module's identity), `viam-server` stops the old process and starts a new one.
You can also trigger a restart manually from the app or through the SDK's `RestartModule` call, useful when you have pushed new module code and want to pick it up without touching anything else.

### Offline operation

Once modules are cached, the machine can keep running if the internet drops:

- `viam-server` continues to serve requests locally.
- Modules keep talking to `viam-server` over the local UNIX sockets.
- Components and services configured on the machine continue to work.

Cloud-dependent operations pause during an outage.
Data sync to Viam Cloud pauses, remote resources on other machines become unreachable, and config changes pushed from the cloud do not reach the machine until it reconnects.

### Local inter-module communication

Modules do not talk to each other directly.
When one module depends on another module's resource (for example, a custom camera module that depends on a built-in board for GPIO), the dependency is resolved by name and the request flows through `viam-server`.
From the module's perspective it calls a gRPC client; under the hood, that client connects to `viam-server`, which routes the call to the resource's actual owner.

This keeps the architecture simple. There is no N-by-N mesh of module sockets, and you can replace any module without rewiring the others.

## Related

- [What is a module?](/build-modules/overview/): the module side of this picture, including module anatomy and how to write one.
- [What is Viam?](/what-is-viam/): where `viam-agent` and `viam-server` sit in the broader platform architecture.
