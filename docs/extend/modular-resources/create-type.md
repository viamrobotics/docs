---
title: "Define a New Resource Type"
linkTitle: "New API Type"
weight: 30
type: "docs"
tags: ["rdk", "extending viam", "modular resources", "API"]
description: "Define an API for a new type of resource."
no_list: true
---

You need to define a new {{% glossary_tooltip term_id="resource" text="resource" %}} *type* (and an API for that type) if:

- You have a {{% glossary_tooltip term_id="resource" text="resource" %}} that does not fit into any of the existing [component](/components/) or [service](/services/) types.
- You have a resource that could fit into an existing type, for example, [base](/components/base/), but you want to define an API with different endpoints than the ones in the standard Viam [API](/program/apis/) for that type.

{{% alert title="Tip" color="tip" %}}

If you want to use most of an existing API but need just a few other functions, try using the [`DoCommand`](/program/apis/#docommand) endpoint to add custom functionality to an existing type.

{{% /alert %}}

In either case, you need to do the following:

1. Decide whether your type is a component or a service.
  If it is hardware, it is a component.
  If it is a software package, it is a service.
1. Choose a name for your type.
  For example, "gizmo."
1. 

Define the messages and methods of the new API in [protobuf](https://github.com/protocolbuffers/protobuf), then generate code in Python or Go and use the generated code to implement the higher level server and client functions required.