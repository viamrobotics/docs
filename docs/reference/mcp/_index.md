---
title: "MCP server"
linkTitle: "MCP server"
weight: 40
layout: "docs"
type: "docs"
description: "Connect Claude or another MCP client to your Viam fleet to list, create, and configure machines, read logs, and operate hardware. Includes a tool reference."
capabilities: ["mcp"]
diataxis: reference
date: "2026-09-21"
---

The Viam MCP server exposes your Viam organizations, locations, machines, fragments, datasets, and training jobs to an [MCP](https://modelcontextprotocol.io/) client such as Claude, Claude Code, ChatGPT, or Codex. Once connected, the client can look up fleet and machine information, read and edit machine and fragment configuration, manage datasets and sequences, run custom training jobs, and call APIs on live machines on your behalf.

## Connect

Add the Viam MCP server to your MCP client as a remote server at:

```text
https://app.viam.com/mcp
```

The server uses OAuth: your MCP client redirects you to sign in to Viam and authorize access, then uses the resulting token for subsequent tool calls. You must accept Viam's terms of service before any tool call succeeds; if you haven't, a tool call returns an error with a link to do so.

Every tool call is scoped to the organizations, locations, and machines your Viam account can already access. The MCP server does not grant any access beyond your existing permissions.

Tools that connect to a live machine, in either **Live machine** category, use that machine's default API key, and create the key if the machine has none.

## Tool categories

Tools fall into seven groups, reflected in the **Category** column below:

- **Read-only** and **Read-only (external)** tools only read and change nothing, so most MCP clients don't prompt for confirmation before running them. Read-only tools query Viam's own data (your fleet, a machine's saved configuration). Read-only (external) tools, such as `read_viam_docs`, search an index outside Viam: a third-party search service that draws mainly on docs.viam.com and returns each passage with the URL it came from.
- **Read (billable)** tools, `read_machine_logs` and `read_training_job_logs`, read data and change no configuration, but they aren't marked read-only to MCP clients: returning logs records billable data egress for the organization that owns the machine or training job. Many clients ask for confirmation before running them. `read_training_job_logs` is also marked destructive, so clients that run non-destructive tools without asking still ask before running it.
- **Live machine (read-only)** tools, such as `read_machine_api` and `get_world_state`, connect to an online machine and read its current state. They don't move hardware or change configuration, but they aren't marked read-only to MCP clients: connecting uses the machine's default API key and creates that key if the machine doesn't have one yet. Many clients ask for confirmation before running them. They need the machine to be reachable and can take longer to answer than the other read tools.
- **Write** tools create or add configuration or data, such as a machine, a config item, or a dataset. Most clients ask for confirmation before running one.
- **Write (destructive)** and **Live machine (destructive)** tools change or delete existing configuration or data, start or cancel billable work such as a training job, or act directly on a live machine (for example, moving hardware with `call_machine_api` or `run_docommand`). These save or act immediately, with no draft and no undo, so review what a tool is about to do before approving it.

The fragment tools (`create_fragment`, `add_fragment_config_item`, `update_fragment_config_item`, and `delete_fragment_config_item`) change fragments. If a fragment is public or unlisted, users outside your organization can see and use its configuration, including your changes.

The favorite machine tools (`list_favorite_machines`, `add_favorite_machine`, and `remove_favorite_machine`) read and change your own [machine favorites](/monitor/monitor/#favorite-machines), which no one else in your organization sees. `remove_favorite_machine` is marked destructive because it deletes a favorite, but it never changes the machine itself.

`set_machine_config` and `set_machine_config_properties` are experimental and may change or be removed. `set_machine_config` replaces a machine part's entire saved configuration, and refuses the change if the configuration has changed since `read_machine_config` returned it. `set_machine_config_properties` sets individual properties by dotted path, such as `components.my-camera.attributes.fps`.

The dataset and sequence tools (`list_datasets`, `create_dataset`, `delete_dataset`, `list_sequences`, `read_sequence`, `update_sequence`, `delete_sequences`, `add_sequences_to_dataset`, and `remove_sequences_from_dataset`) manage [datasets](/train/create-a-dataset/) and their sequences. Deleting a dataset or removing sequences from it keeps the captured images, readings, and sequences; only their membership in the dataset is removed. `delete_sequences` deletes the sequences themselves but keeps the data captured during them.

The training tools (`list_training_scripts`, `list_training_containers`, `submit_training_job`, `list_training_jobs`, `read_training_job`, `read_training_job_logs`, and `cancel_training_job`) run [custom training jobs](/train/custom-training-scripts/). Each `submit_training_job` call starts a new job, billed to the dataset's organization for its GPU time, so it is marked destructive and is not safe to repeat: a call that fails or times out may still have started a job, so check `list_training_jobs` before submitting again. `cancel_training_job` cancels a pending or in-progress job; GPU time used before the cancellation is billed.

The machine and fragment config item tools also add, re-pin, and remove entries in a configuration's `packages` section, such as an ML model at a pinned version. They check that the package exists and that the version is published or `latest`, and they refuse to remove or rename a package that a resource or module still uses.

The simulation tools (`read_simulation`, `start_simulation`, and `stop_simulation`) manage a [cloud simulation](/set-up-a-machine/simulate-a-machine/) of a machine part. Starting a simulation is billed by the minute to the machine's organization, so `stop_simulation` ends the charges.

## Skills

The MCP server also serves skills: Markdown instructions that tell the AI assistant how to complete a multi-step Viam task correctly, such as which configuration entries a task needs, which tools to call in which order, and how to check the result.
Each skill has a description of when it applies, so the assistant can load the right one for your request without you naming it.
Clients that support the MCP skills extension discover the skills on their own.
Other clients read them with the `retrieve_skill` tool.

The server currently serves these skills:

- `deploy-ml-model`: deploys a trained ML model to a machine or fragment: a `packages` entry for the model, an ML model service that reads it, and, for classification and detection models, a vision service. Also covers re-pinning a model to another version and removing it.
- `set-up-obstacles`: configures static obstacles, such as tables, walls, and bins, for motion planning to avoid.
- `resource-notes`: sets or clears a resource's notes, the **Scratchpad** on its card in the builder, including on a resource that comes from a fragment.

Skills only guide the assistant. They don't add tools or permissions: every change a skill describes goes through the tools listed below, with the same confirmation prompts.

## Tools

To learn what a particular tool can do, ask an AI assistant that's connected to the Viam MCP server. See [Connect](#connect).

{{< readfile "/static/include/app/mcpserver/generated/mcp-tools-table.md" >}}
