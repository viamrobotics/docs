---
title: "MCP server"
linkTitle: "MCP server"
weight: 40
layout: "docs"
type: "docs"
description: "Connect Claude or another MCP client to your Viam fleet, and reference the tools the Viam MCP server exposes."
capabilities: ["mcp"]
diataxis: reference
date: "2026-09-21"
---

The Viam MCP server exposes your Viam organizations, locations, machines, and fragments to an [MCP](https://modelcontextprotocol.io/) client such as Claude, Claude Code, ChatGPT, or Codex. Once connected, the client can look up fleet and machine information, read and edit machine and fragment configuration, and call APIs on live machines on your behalf.

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
- **Read (billable)** tools, currently only `read_machine_logs`, read data and change no configuration, but they aren't marked read-only to MCP clients: returning logs records billable data egress for the machine's organization. Many clients ask for confirmation before running them.
- **Live machine (read-only)** tools, such as `read_machine_api` and `get_world_state`, connect to an online machine and read its current state. They don't move hardware or change configuration, but they aren't marked read-only to MCP clients: connecting uses the machine's default API key and creates that key if the machine doesn't have one yet. Many clients ask for confirmation before running them. They need the machine to be reachable and can take longer to answer than the other read tools.
- **Write** tools create or add configuration. Most clients ask for confirmation before running one.
- **Write (destructive)** and **Live machine (destructive)** tools change or delete existing configuration, or act directly on a live machine (for example, moving hardware with `call_machine_api` or `run_docommand`). These save or act immediately, with no draft and no undo, so review what a tool is about to do before approving it.

The fragment tools (`create_fragment`, `add_fragment_config_item`, `update_fragment_config_item`, and `delete_fragment_config_item`), in either **Write** category, are also marked open-world to MCP clients, because the fragment they change can be public or reachable by anyone with its ID.

## Tools

{{< readfile "/static/include/app/mcpserver/generated/mcp-tools-table.md" >}}
