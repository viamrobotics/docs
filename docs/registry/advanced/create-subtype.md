---
title: "Define a New Resource Subtype"
linkTitle: "New API Subtype"
weight: 30
type: "docs"
tags: ["rdk", "extending viam", "modular resources", "API"]
description: "Define a new API for a resource that does not fit into existing component or service subtypes."
no_list: true
aliases:
  - "/extend/modular-resources/create/create-subtype/"
  - "/modular-resources/advanced/create-subtype"
---

You can define a new {{< glossary_tooltip term_id="resource" text="resource" >}} _{{< glossary_tooltip term_id="subtype" text="subtype" >}}_ API if:

- You have a {{% glossary_tooltip term_id="resource" text="resource" %}} that does not fit into any of the existing {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}} subtypes.
- You have a resource that could fit into an existing subtype, but you want to define an API with different methods and messages than the ones in the existing [APIs](/program/apis/) for that subtype.

  {{% alert title="Tip" color="tip" %}}

  If you want to use most of an existing API but need just a few other functions, try using the [`DoCommand`](/program/apis/#docommand) endpoint and [extra parameters](/program/use-extra-params/) to add custom functionality to an existing subtype.
  For example, if you have a [sensor](/components/sensor/) and you want to define a `Calibrate` method, you can use `DoCommand`.

  {{% /alert %}}

## Define your new resource API

Viam uses [protocol buffers](https://protobuf.dev/) for API definition.

To define a new subtype, you need to define the methods and messages of the new API in [protobuf](https://github.com/protocolbuffers/protobuf), write code in Python or Go to implement the higher level server and client functions required, and generate all necessary [protobuf module files](https://buf.build/docs/generate/usage/).
The following steps guide you through this process in more detail:

1. Decide whether your subtype is a {{< glossary_tooltip term_id="component" text="component" >}} or a {{< glossary_tooltip term_id="service" text="service" >}}.
   If it provides an interface to control hardware, it is a component.
   If it provides higher-level functionality, it is a service.
1. Choose a name for your subtype.
   For example, `gizmo`.
1. Create a directory for your module.
   Within that, create a directory called <file>src</file>.

   {{% alert title="Tip" color="tip" %}}

   If you are writing your module using Python, you can use this [module generator tool](https://github.com/viam-labs/generator-viam-module) to generate stub files for the new API as well as a new {{< glossary_tooltip term_id="module" text="module" >}} that implements the new API.

   {{% /alert %}}

1. Define your new API:

   - [Write the proto](https://protobuf.dev/programming-guides/proto3/) methods in a `<subtype name>.proto` file inside your <file>src/proto</file> directory.
     For reference:
     - [Example modular component proto file](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/src/proto/gizmo.proto)
     - [Example modular service proto file](https://github.com/viam-labs/speech/blob/main/src/speech/proto/speech.proto)
     - [Built-in Viam resource proto files](https://github.com/viamrobotics/api/tree/main/proto/viam)
   - And define the proto methods in a protobuf-supported language such as Python or Go in a file called `api.py` or `api.go`, respectively.
     - [Example component in Python](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/src/gizmo/api.py)
     - [Example service in Python](https://github.com/viam-labs/speech/blob/main/src/speech/api.py)

1. In the root directory of your module, you need to generate some boilerplate files.
   You will typically need the following three files for most modules, though different files are required for some advanced use cases.
   See the [Buf documentation](https://buf.build/docs/generate/usage/) for instructions.

   - [<file>buf.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
   - [<file>buf.gen.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
   - [<file>buf.lock</file>](https://buf.build/docs/configuration/v1/buf-lock/)

1. In the <file>/src/</file> directory of your module, use the protobuf compiler to [generate](https://buf.build/docs/tutorials/getting-started-with-buf-cli/#generate-code) all other necessary protocol buffer code, based on the `<subtype name>.proto` file you wrote.

   - [Example generated files for a Python-based service](https://github.com/viam-labs/speech/tree/main/src/speech/proto).
     The `buf.` files were generated.
     The <file>speech.proto</file> was manually written.

## Next steps

{{< cards >}}
{{% manualcard link="/registry/create/#code-a-new-resource-model"%}}

<h4>Implement your API</h4>

Now that your resource API is defined, create a new model that implements your new API.

{{% /manualcard %}}
{{< /cards >}}
