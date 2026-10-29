---
title: "Phase 1: Set up your environment"
linkTitle: "1. Set up your environment"
type: "docs"
slug: "setting-up-your-environment"
weight: 10
description: "Set up Viam, the agentic workflows, and the companion scripts for the Cosmos workshop."
capabilities: ["mcp", "machine-config", "docs"]
diataxis: tutorial
workshop: "cosmos"
toc_hide: true
phase: 1
phase_total: 5
prev: "/tutorials/cosmos/"
next: "/tutorials/cosmos/design-your-robot-and-tasks/"
languages: ["python"]
draft: false
---

All you need for this tutorial is a laptop with a web browser, a terminal that can run python, and a coding harness like Codex or Claude Code.

## Viam

You’ll be using Viam to configure and control your simulated robot. Head to app.viam.com and create an account if you don’t have one.

## Harness setup

Install our agentic workflows and MCP server in your harness:

1. Type /plugins, navigating to the ‘Marketplaces’ or ‘Add marketplace’ tab (with the right arrow key), hitting Enter to add a marketplace, then using `viamrobotics/viam-agentic-kit` as the source.
1. That should take you to the plugins list for our marketplace. There’s only one (viam-agentic-kit), hit enter to install it.
1. The plugin registers an MCP server for Viam, but doesn’t authenticate for you. Run /mcp, scroll down to plugin:viam-agentic-kit:viam, hit enter, and follow the prompts.

This installs a set of skills and subagent definitions that understand the end-to-end workcell design and training process, and can route to frontier models for visual and spatial tasks.

## Clone the tutorial scripts

Some of the steps here, like your robot’s action and episode capture, will be controlled by code running on your laptop. We’ve created a scripts repo you will need.

Get the scripts by:

1. Open a terminal on your laptop
1. Clone the cosmos-tutorial repo with `git clone https://github.com/viam-labs/cosmos-tutorial`
1. `cd cosmos-tutorial`
1. Install the `uv` tool for python package management from the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

{{< workshop-nav >}}
