---
title: "MCP server"
linkTitle: "MCP server"
weight: 40
layout: "docs"
type: "docs"
description: "Connect Claude or another MCP client to your Viam fleet, and reference the tools the Viam MCP server exposes."
capabilities: ["mcp"]
date: "2026-09-21"
---

The Viam MCP server exposes your Viam organizations, locations, machines, and fragments to an [MCP](https://modelcontextprotocol.io/) client such as Claude. Once connected, the client can look up fleet and machine information, read and edit machine and fragment configuration, and call APIs on live machines on your behalf.

## Connect

Add the Viam MCP server to your MCP client as a remote server at:

```text
https://app.viam.com/mcp
```

The server uses OAuth: your MCP client redirects you to sign in to Viam and authorize access, then uses the resulting token for subsequent tool calls. You must accept Viam's terms of service before any tool call succeeds; if you haven't, a tool call returns an error with a link to do so.

Every tool call is scoped to the organizations, locations, and machines your Viam account can already access. The MCP server does not grant any access beyond your existing permissions.

## Tool categories

Tools fall into three groups, reflected in the **Category** column below:

- **Read-only** tools only read data and never prompt for confirmation in most MCP clients.
- **Write** tools create or add configuration. Most clients ask for confirmation before running one.
- **Write (destructive)** and **Live machine (destructive)** tools change or delete existing configuration, or act directly on a live machine (for example, moving hardware with `call_machine_api` or `run_docommand`). These save or act immediately, with no draft and no undo, so review what a tool is about to do before approving it.

## Tools

{{< readfile "/static/include/app/mcpserver/generated/mcp-tools-table.md" >}}
