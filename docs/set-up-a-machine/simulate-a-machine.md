---
linkTitle: "Simulate a machine"
title: "Simulate a machine"
weight: 3
layout: "docs"
type: "docs"
description: "Run viam-server in a simulated environment in the cloud so you can build and test a machine without its hardware."
capabilities: ["device-provisioning", "billing"]
diataxis: how-to
date: "2026-10-15"
---

<!-- TODO(draft): hold until the simulation feature is generally available. The wizard UI is behind a feature flag (viamrobotics/app#13706) and the backend is moving from Modal to GKE (viamrobotics/app#13958). Confirm the user-facing name ("simulated environment" in the wizard, Isaac Sim in the MCP tool descriptions) before publishing. -->

Run `viam-server` in a simulated environment in the cloud, so you can build and test your machine without its hardware.
A simulated machine appears in the Viam app like any other machine: you configure it from the **CONFIGURE** tab, and you can control it, view its logs, and connect to it with an SDK.

## Before you start

- **Simulation is billed by the minute.** Your organization is charged for as long as the simulation is running. <!-- TODO(draft): state the rate, or link to the pricing page. -->
- **Idle simulations time out.** If the simulated machine isn't actuating, the simulation times out after at most 60 minutes.
- **You can stop or restart a simulation at any time.**
- **Some modules need real hardware.** Modules that are drivers for physical hardware, such as specific cameras, motors, or sensors, don't work in a simulated environment. <!-- TODO(draft): confirm that built-in fake models (for example, the fake arm) work in the sandbox and link them here. -->

## Start a simulation

1. Create a machine in the Viam app. If you haven't made one before, follow [Set up your first machine](/set-up-a-machine/first-machine/) through step 1.
2. In the setup wizard, choose to simulate your machine instead of installing Viam on a device.
3. Read the notes about billing and limits, then click **Start simulation**.

The wizard shows the simulation's progress as it starts.
When it's ready, the machine comes online and you can configure it like any other machine.
See [Configure hardware](/hardware/configure-hardware/) for how to add components. <!-- TODO(draft): confirm startup time to set expectations, and what the wizard shows if the simulation fails to start. -->

If a simulation is already running for the machine, the wizard offers **View running simulation** instead of starting a second one.

## Check, stop, or restart a simulation

After you've started a simulation, the machine's page shows its status and controls to stop it.
If a simulation has run before and is no longer running, the same controls let you restart it.
Stop a simulation when you're done with it to stop the per-minute charges. <!-- TODO(draft): confirm where on the machine page these controls appear before describing them more specifically. -->

Deleting a machine also ends its simulation.

## Manage simulations from the AI assistant or MCP

The Config AI assistant and the [Viam MCP server](/reference/mcp/) can check on, start, and stop a machine's simulation:

| Tool                | What it does                                                 |
| ------------------- | ------------------------------------------------------------ |
| `read_simulation`   | Reports whether a simulation is running for a machine part.  |
| `start_simulation`  | Starts a simulation. Does nothing if one is already running. |
| `stop_simulation`   | Stops a simulation. Does nothing if none is running.         |

Each tool takes an optional part name and uses the machine's main part if you omit it.
Starting a simulation this way is billed the same as starting one from the setup wizard.

## What's next

- [Configure hardware](/hardware/configure-hardware/) to add components to your simulated machine.
- [Set up your first machine](/set-up-a-machine/first-machine/) to connect a real device.
