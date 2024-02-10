---
title: Process
id: process
full_link:
short_description: Processes are commands such as binaries or scripts that run on a part.
aka:
---

Processes are binaries, scripts, or other commands that run on a {{< glossary_tooltip term_id="part" text="part" >}}.

You can use processes to create a new local instance of `viam-server` to implement drivers for custom {{< glossary_tooltip term_id="component" text="components" >}}, or to run a client application, for example.
They provide an OS-specific process managed by `viam-server` to either run once or indefinitely.
For example, you could use a process to run a camera server.

Find more information in [Configure a Process to Run on Your Machine](/build/configure/processes/).
