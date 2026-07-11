---
title: "Phase 6: Wrap the loop in a module"
linkTitle: "6. Inline module"
type: "docs"
slug: "inline-module"
weight: 60
description: "Wrap the working pack loop in an inline module so it runs on the machine and can be triggered through DoCommand."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 6
phase_total: 6
time_estimate: "15 minutes"
prev: "/tutorials/so-arm101-palletizing/avoid-placed-cubes/"
languages: ["python"]
draft: true
---

This phase is optional. It takes the working pack loop from phase 5 off your laptop and onto the machine, where it runs as a module and can be triggered on demand instead of from a script.

## From script to module

<!-- TODO: explain why wrap the loop in a module: it runs on the machine instead of depending on a connected laptop, and something else (the test card, another program) can trigger it through DoCommand. Source: seed 06-inline-module.md. -->

<!-- TODO (content fidelity): the finger gripper's grab() returns whether it actually closed on something; use that return value to verify the hold before lifting, rather than assuming the grasp succeeded. -->

## Scaffold the inline module

<!-- TODO: use `viam module generate` to scaffold an inline module, move the palletizer logic into it, and expose a `pack` action through DoCommand. Source: seed phase 6 + Viam 101 08-scaffold.md. -->

## Reload and run on the machine

<!-- TODO: use `viam module reload` to push changes during development, then trigger `pack` from the CONTROL tab's test card or with `viam machines part run`. -->

{{< workshop-nav >}}
