---
title: "Define a new resource API"
linkTitle: "Custom API"
weight: 30
type: "docs"
tags: ["rdk", "extending viam", "modular resources", "API"]
description: "Define a custom API for a resource that does not fit into existing component or service APIs."
no_list: true
aliases:
  - /extend/modular-resources/create/create-subtype/
  - /modular-resources/advanced/create-subtype/
  - /registry/advanced/create-subtype/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

You can define a new, custom {{< glossary_tooltip term_id="resource" text="resource" >}} API if:

- You have a {{% glossary_tooltip term_id="resource" text="resource" %}} that does not fit into any of the existing {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}} APIs.
- You have a resource that could fit into an existing API, but you want to define an API with different methods and messages than the one in the existing [APIs](/dev/reference/apis/).

{{% alert title="Tip" color="tip" %}}

Defining a new resource API is significantly more complex than using an existing API.
In most cases, you should try to use an existing API rather than define a new one.

If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and [extra parameters](/dev/reference/sdks/use-extra-params/) to add custom functionality to an existing API.
For example, if you have a [sensor](/operate/reference/components/sensor/) and you want to define a `Calibrate` method, you can use `DoCommand`.

If your use case uses only `DoCommand` and no other API methods, you can define a new model of [generic component](/operate/reference/components/generic/) or [generic service](/operate/reference/services/generic/).

{{% /alert %}}

## Define your new resource API

Viam uses [protocol buffers](https://protobuf.dev/) for API definition.

To define a new API, you need to define the methods and messages of the API in [protobuf](https://github.com/protocolbuffers/protobuf), write code in Python or Go to implement the higher level server and client functions required, and generate all necessary [protobuf module files](https://buf.build/docs/generate/usage/).
The following steps guide you through this process in more detail:

1. Decide whether your custom API is a {{< glossary_tooltip term_id="component" text="component" >}} or a {{< glossary_tooltip term_id="service" text="service" >}}.
   If it provides an interface to control hardware, it is a component.
   If it provides higher-level functionality, it is a service.
1. Choose a name for your API.
   This is called the `{{< glossary_tooltip term_id="subtype" text="subtype" >}}` of your API.
   For example, `gizmo`.

   Determine a valid {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet" >}} based on your API name.
   You can figure out the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}} later when you [create a model that implements your custom API](/operate/modules/support-hardware/).

   {{< expand "API namespace triplet and model namespace triplet example" >}}

   The `viam-labs:audioout:pygame` model uses the module name [audioout](https://github.com/viam-labs/audioout).
   It implements the custom API `viam-labs:service:audioout`:

   ```json
   {
     "api": "viam-labs:service:audioout",
     "model": "viam-labs:audioout:pygame"
   }
   ```

   For your custom API, your API namespace triplet might be `your-org-namespace:component:gizmo` where `your-org-namespace` is your organization namespace, found in your org settings page.

   {{< /expand >}}

1. Create a directory for your module.
   Within that, create a directory called <file>src</file>.

   {{% alert title="Tip" color="tip" %}}

   If you are writing your module using Python, you can use this [module generator tool](https://github.com/viam-labs/generator-viam-module) to generate stub files for the new API as well as a new {{< glossary_tooltip term_id="module" text="module" >}} that implements the new API.

   {{% /alert %}}

1. Define your new API:

   - [Write the proto](https://protobuf.dev/programming-guides/proto3/) methods in a `<API name>.proto` file inside your <file>src/proto</file> directory.
     For reference:
     - [Example modular component proto file](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/src/proto/gizmo.proto)
     - [Example modular service proto file](https://github.com/viam-labs/speech-service-api/blob/main/src/proto/speech.proto)
     - [Built-in Viam resource proto files](https://github.com/viamrobotics/api/tree/main/proto/viam)
   - And define the proto methods in a protobuf-supported language such as Python or Go in a file called `api.py` or `api.go`, respectively.
     - [Example component in Python](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/src/gizmo/api.py)
     - [Example service in Python](https://github.com/viam-labs/speech-service-api/blob/main/src/speech_service_api/api.py)

1. In the root directory of your module, you need to generate some configuration files.
   You will typically need the following three files for most modules, though different files are required for some advanced use cases.
   See the [Buf documentation](https://buf.build/docs/generate/usage/) for instructions.

   - [<file>buf.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
   - [<file>buf.gen.yaml</file>](https://buf.build/docs/configuration/v1/buf-gen-yaml/)
   - [<file>buf.lock</file>](https://buf.build/docs/configuration/v1/buf-lock/)

1. In the <file>/src/</file> directory of your module, use the protobuf compiler to [generate](https://buf.build/docs/tutorials/getting-started-with-buf-cli/#generate-code) all other necessary protocol buffer code, based on the `<API name>.proto` file you wrote.

   - [Example generated files for a Python-based service](https://github.com/viam-labs/speech-service-api/tree/main/src/proto).
     The `buf.` files were generated.
     The <file>speech.proto</file> was manually written.

## Next steps

{{< cards >}}
{{% manualcard link="/operate/modules/support-hardware/" %}}

<h4>Implement your API</h4>

Now that your resource API is defined, create a new model that implements your new API.

{{% /manualcard %}}
{{< /cards >}}

{{% alert title="Note" color="note" %}}

After you define a new API and create a model that implements it, keep the following in mind when writing code against your new API:

- You can't use [SDKs](/dev/reference/sdks/) to call your new API unless you build out the client to support it.
  It is easiest to write code against your new API in the language you used to define it.
- Since your API doesn't have built-in SDK support, you'll need a local copy of the module code on whatever machine is running client code against it.
- Be sure to import the API definition from the module directory, for example in Python it would be of the form `from path.to.module.src.gizmo import Gizmo`.
  This example module written in Python uses a [Python script](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/client.py) to call the custom API from within the module directory.

{{% /alert %}}
