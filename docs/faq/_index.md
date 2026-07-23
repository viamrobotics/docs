---
linkTitle: "FAQ"
title: "Frequently asked questions"
weight: 700
layout: "docs"
type: "docs"
no_list: true
description: "Answers to frequently asked questions about Viam."
date: "2026-05-26"
---

Answers to questions we hear often. Click a question to expand its answer.

{{< expand "Do Viam machines require an internet connection to run?" >}}
No, a Viam machine does not need an internet connection to run, and its
control logic does not execute in the cloud. Execution happens on the
machine itself.

Here is what that means in practice:

- **viam-server runs on the machine.** viam-server is the agent that drives
  your hardware. It runs as a process on the device, such as a single-board
  computer or an industrial PC, not on Viam's servers.
- **Your resources run locally.** On startup, viam-server reads your
  configuration and builds the components, services, and modules it
  describes, then runs them on the device. Modules, where most drivers and
  custom logic live, run as separate local processes that communicate with
  viam-server over Unix domain sockets, not over the network.
- **API calls are served on the machine.** Your application connects to
  viam-server through an SDK and calls its API. When you read a sensor or
  command a motor, viam-server handles that request on the device and sends
  it straight to the hardware. It does not round-trip through the cloud. On
  the same network, the SDK connects directly to the machine, so this works
  with no internet at all.

The cloud handles management and coordination, not the control loop, so
losing the connection does not stop the robot:

- Configuration, fleet management, remote access, data storage, and ML
  training live in Viam's cloud. These are management and coordination
  features layered on top of the machine, not part of its control loop.
- **Configuration is cached on the machine.** A cloud-managed machine writes
  its latest config to disk. If it restarts and cannot reach the cloud, it
  boots from the cached config and runs normally. You can also run
  viam-server entirely from a local config file with no cloud connection
  configured.
- **Captured data is buffered locally.** Data capture writes to disk first
  and syncs to the cloud when a connection is available. While offline, the
  data stays on the machine and uploads automatically once connectivity
  returns.

The one case that needs connectivity: a cloud-managed machine that has never
connected has no cached config yet, so it must reach the cloud once to
receive its initial configuration. After that, it can run offline.
{{< /expand >}}

<!--
To add a question, copy the block below. The text in quotes is the question
shown in the sidebar link anchor; the content between the tags is the answer
and supports normal markdown (links, code blocks, lists).

{{</* expand "Your question here?" */>}}
Your answer here.
{{</* /expand */>}}
-->
