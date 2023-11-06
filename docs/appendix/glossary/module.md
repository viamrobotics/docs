---
title: Module
id: module
full_link:
short_description: A module provides one or more modular resources, which add resource types or models that are not built into Viam.
aka:
---

A _module_ provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, which add {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="type" text="types" >}} or {{< glossary_tooltip term_id="model" text="models" >}} that are not built into Viam.
Modules run alongside `viam-server` as separate process, communicating with `viam-server` over UNIX sockets.
When the module initializes, it registers those pairs on your robot, making the functionality defined by that pair available for use.

You can [create your own module](/registry/create/) or [add existing modules from the Viam registry](/registry/configure/).

For more information see the [modular resource documentation](/registry/).
