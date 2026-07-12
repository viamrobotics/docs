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
prev: "/tutorials/so-arm101-palletizing/avoid-placed-cubes/"
next: "/tutorials/so-arm101-palletizing/wrap-up/"
languages: ["python"]
draft: true
---

This phase is optional. It takes the working pack loop from Phase 5 off your laptop and onto the machine, where it runs as a module and can be triggered on demand instead of from a script.

## From script to module

<!-- TODO: explain why wrap the loop in a module: it runs on the machine instead of depending on a connected laptop, and something else (the test card, another program) can trigger it through DoCommand. -->

<!-- TODO (content fidelity): the finger gripper's grab() returns whether it actually closed on something; use that return value to verify the hold before lifting, rather than assuming the grasp succeeded. -->

## Scaffold the inline module

<!-- TODO: use `viam module generate` to scaffold an inline module, move the palletizer logic into it, and expose a `pack` action through DoCommand. -->

## Reload and run on the machine

<!-- TODO: use `viam module reload` to push changes during development, then trigger `pack` from the CONTROL tab's test card or with `viam machines part run`. -->

{{< workshop-nav >}}
