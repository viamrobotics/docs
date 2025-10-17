---
title: Module
id: module
full_link:
short_description: Modules are the code packages that provide functionality like drivers, integrations, and control logic to your machines.
---

A _module_ is a code package which provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, which add {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="type" text="types" >}} or {{< glossary_tooltip term_id="model" text="models" >}}, integrations, or control logic for your machines.
Modules run alongside `viam-server` as separate process, communicating with `viam-server` over UNIX sockets.

You can [create your own module](/operate/modules/support-hardware/) or [add existing modules from the registry](/operate/modules/configure-modules/).
