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
- You have a resource that could fit into an existing type, but you want to define an API with different endpoints than the ones in the standard Viam [API](/program/apis/) for that type.
For example, you have a [sensor](/components/sensor/) and you want to define a `Calibrate` endpoint.

{{% alert title="Tip" color="tip" %}}

If you want to use most of an existing API but need just a few other functions, try using the [`DoCommand`](/program/apis/#docommand) endpoint and [extra parameters](/program/use-extra-params/) to add custom functionality to an existing type.

{{% /alert %}}

## How to define your new resource API

Viam uses [protocol buffers](https://protobuf.dev/) for API definition.

To define a new type, you need to define the messages and methods of the new API in [protobuf](https://github.com/protocolbuffers/protobuf), generate all necessary [protobuf module files](https://buf.build/docs/generate/usage/), and then write code in Python or Go to implement the higher level server and client functions required.
The following steps guide you through this process in more detail.

1. Decide whether your type is a component or a service.
  If provides an interface to control hardware, it is a component.
  If it provides higher-level functionality, it is a service.
1. Choose a name for your type.
  For example, "gizmo."
1. Create a directory or repository for your module.
  Within that, create a directory called <file>src</file>.
1. Define your new API:

    - Write the proto methods in a `<type name>.proto` file inside your <file>src</file> directory
      - [Example component](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/module/src/proto/gizmo.proto)
      - [Example service](https://github.com/viam-labs/speech/blob/main/src/proto/speech.proto)
    - And define those methods in a protobuf-supported language such as Python or Go in a file called `api.py` (or `api.go`)
      - [Example component in Python](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/module/src/gizmo/api.py)
      - [Example service in Python](https://github.com/viam-labs/speech/blob/main/src/speech/api.py)

1. In the root directory of your module, you need to generate some boilerplate files.
You will typically need the following three files for most modules, though different files are required for some advanced use cases.
  See the [Buf documentation](https://buf.build/docs/generate/usage/) for instructions.

    - [<file>buf.gen.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
    - [<file>buf.lock</file>](https://buf.build/docs/configuration/v1/buf-lock/)
    - [<file>buf.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)

1. In the <file>/src/</file> directory of your module, use the protobuf compiler to [generate](https://buf.build/docs/tutorials/getting-started-with-buf-cli/#generate-code) all other necessary protocol buffer code, based on the `<type name>.proto` file you wrote.

    - [Example generated files for a Python-based service](https://github.com/viam-labs/speech/tree/main/src/proto)
      - (<file>speech.proto</file> was manually written, not generated)

1. Your resource API is defined.
  Now you can create a new module <!-- insert link! --> that implements your new API.

{{% alert title="Tip" color="tip" %}}

If you are writing your module using Python, you can use this [module generator tool](https://github.com/viam-labs/generator-viam-module) to generate stub files.

{{% /alert %}}
