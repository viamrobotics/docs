---
title: SDK (Software Development Kit)
id: sdk
full_link: /program/sdk-as-client/
short_description: Viam provides an SDK to help you write client applications, and create support for custom component types.
aka:
---

Viam provides an SDK to help you write client applications, and create support for custom {{< glossary_tooltip term_id="component" text="component" >}} types.

- One per language.
- Can be used as a server for a custom component implementation.
  - Hosts a gRPC server implementing the Viam Robot API.
  - That serves functionality for all registered resources.
- Can be used as a client.
  - To connect to a robot implementing the Viam Robot API.
- Effectively, non-golang versions of {{< glossary_tooltip term_id="rdk" text="RDK" >}}’s resource authoring and activation functionality.
