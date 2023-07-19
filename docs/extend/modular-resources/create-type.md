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

## How to define your new resource API

Viam uses [protocol buffers](https://protobuf.dev/) for API definition.

To define a new type, you need to define the messages and methods of the new API in [protobuf](https://github.com/protocolbuffers/protobuf), generate all necessary [protobuf module files](https://buf.build/docs/generate/usage/), and then write code in Python or Go to implement the higher level server and client functions required.
The following steps guide you through this process in more detail.

{{% alert title="Tip" color="tip" %}}

If you are writing your module using Python, you can use this [module generator tool](https://github.com/viam-labs/generator-viam-module) to generate stub files for the new API as well as a new module that implements the new API.

{{% /alert %}}

1. Decide on a name for your module, in the form `namespace:type:subtype` (for example, `rdk:component:motor` or `viamlabs:component:gizmo`):

    - Decide on a namespace for your module.
    `rdk` is reserved for built-in resources, but otherwise this is up to you.
    You could name it after yourself, your company, some other designator, or use `viamlabs`.
    - Decide whether your new resource is a {{< glossary_tooltip term_id="component" text="component" >}} or a {{< glossary_tooltip term_id="service" text="service" >}}.
    If it is hardware, it is a component.
    If it is a software package, it is a service.
    This becomes the "type" piece of your API namespace triplet.
    - Choose a name for your subtype.
    For example, "gizmo."

2. Create a directory or repository for your module.
  Within that, create a directory called <file>src</file>, and a subdirectory called <file>src/proto</file>.
3. Define your new API:

    - [Write the proto](https://protobuf.dev/programming-guides/proto3/) methods in a `<subtype name>.proto` file inside your <file>src/proto</file> directory.
      - [Example modular component proto file](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/module/src/proto/gizmo.proto)
      - [Example modular service proto file](https://github.com/viam-labs/speech/blob/main/src/proto/speech.proto)
      - [Built-in Viam resource proto files for reference](https://github.com/viamrobotics/api/tree/main/proto/viam)
    - And define those methods in a protobuf-supported language such as Python or Go in a file called `api.py` (or `api.go`).
      - [Example component in Python](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/module/src/gizmo/api.py)
      - [Example service in Python](https://github.com/viam-labs/speech/blob/main/src/speech/api.py)

4. In the root directory of your module, you need to generate the following boilerplate files.
  See the [Buf documentation](https://buf.build/docs/generate/usage/) for instructions.

    - [<file>buf.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
    - [<file>buf.gen.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
    - [<file>buf.lock</file>](https://buf.build/docs/configuration/v1/buf-lock/)

5. In the <file>/src/</file> directory of your module, use the protobuf compiler to [generate](https://buf.build/docs/tutorials/getting-started-with-buf-cli/#generate-code) all other necessary protocol buffer code, based on the `<type name>.proto` file you wrote.

    - [Example generated files for a Python-based service](https://github.com/viam-labs/speech/tree/main/src/proto)
      - (<file>speech.proto</file> was manually written, not generated)

6. Your resource API is defined.
  Now you can create a new module <!-- insert link! --> that implements your new API.
