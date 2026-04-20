---
linkTitle: "Advanced patterns"
title: "Advanced module patterns"
weight: 38
layout: "docs"
type: "docs"
description: "Define new resource APIs, deploy custom components as remote parts, and package modules with Docker."
date: "2026-04-20"
aliases:
  - /operate/reference/advanced-modules/
  - /operate/reference/advanced-modules/create-subtype/
  - /operate/reference/advanced-modules/custom-components-remotes/
  - /operate/reference/advanced-modules/docker-modules/
  - /program/extend/
  - /modular-resources/advanced/
  - /registry/advanced/
  - /extend/modular-resources/create/create-subtype/
  - /modular-resources/advanced/create-subtype/
  - /registry/advanced/create-subtype/
  - /program/extend/sdk-as-server/
  - /program/extend/custom-components-remotes/
  - /extend/custom-components-remotes/
  - /modular-resources/advanced/custom-components-remotes/
  - /registry/advanced/custom-components-remotes/
---

Some use cases require approaches beyond the standard module workflow. This page covers three advanced patterns: defining a new resource API, deploying custom components as remote parts, and packaging modules with Docker.

## Define a new resource API

You can define a new, custom resource API if:

- You have a resource that does not fit into any of the existing [component](/reference/apis/#component-apis) or [service](/reference/apis/#service-apis) APIs.
- You have a resource that could fit into an existing API, but you want different methods and messages.

{{% alert title="Tip" color="tip" %}}

Defining a new resource API is significantly more complex than using an existing API. In most cases, use an existing API instead.

If you want to use most of an existing API but need a few additional functions, use the `DoCommand` endpoint with [extra parameters](/reference/sdks/use-extra-params/) to add custom functionality.

If your use case uses only `DoCommand` and no other API methods, define a new model of [generic component](/reference/components/generic/) or [generic service](/reference/services/generic/).

{{% /alert %}}

### Steps to define a new API

Viam uses [protocol buffers](https://protobuf.dev/) for API definition. To define a new API:

1. Decide whether your custom API is a component (interfaces with hardware) or a service (provides higher-level functionality).

2. Choose a name for your API (called the subtype). Determine a valid API namespace triplet. For example, `your-org-namespace:component:gizmo`.

3. Create a directory for your module with a `src` subdirectory.

   {{% alert title="Tip" color="tip" %}}
   If you are writing your module in Python, you can use this [module generator tool](https://github.com/viam-labs/generator-viam-module) to generate stub files for the new API and a module that implements it.
   {{% /alert %}}

4. Write the proto methods in a `<API name>.proto` file inside `src/proto/`. For reference:

   - [Example modular component proto file](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/src/proto/gizmo.proto)
   - [Example modular service proto file](https://github.com/viam-labs/speech-service-api/blob/main/src/proto/speech.proto)
   - [Built-in Viam resource proto files](https://github.com/viamrobotics/api/tree/main/proto/viam)

5. Define the proto methods in Python or Go in a file called `api.py` or `api.go`:

   - [Example component in Python](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/complex_module/src/gizmo/api.py)
   - [Example service in Python](https://github.com/viam-labs/speech-service-api/blob/main/src/speech_service_api/api.py)

6. Generate the required configuration files (`buf.yaml`, `buf.gen.yaml`, `buf.lock`). See the [Buf documentation](https://buf.build/docs/generate/usage/).

7. Use the protobuf compiler to [generate](https://buf.build/docs/tutorials/getting-started-with-buf-cli/#generate-code) all other necessary protocol buffer code from your `.proto` file.

### After defining your API

Once your API is defined, [create a model that implements it](/build-modules/write-a-driver-module/).

Keep in mind:

- You cannot use [SDKs](/reference/sdks/) to call your new API unless you build out the client to support it. Write code against the API in the language you used to define it.
- You need a local copy of the module code on whatever machine runs client code against it.
- Import the API definition from the module directory. For example, in Python: `from path.to.module.src.gizmo import Gizmo`.

## Custom components as remote parts

Running modular resources on the computer directly connected to your components is the preferred approach. However, if you cannot use modular resources because you need to host `viam-server` on a non-Linux system or have a compilation issue, you can code a custom resource implementation, host it on a server, and add it as a [remote part](/hardware/multi-machine/add-a-remote-part/) of your machine.

Once configured, you control the custom component with the Viam SDKs like any other component.

### Steps

{{< tabs >}}
{{% tab name="Go" %}}

1. Code a new model of a built-in resource type by creating a new interface that implements the required methods from its [API definition](/reference/apis/).
2. Register the custom component on a new gRPC server instance and start the server.
3. Add the server as a [remote part](/hardware/multi-machine/add-a-remote-part/) of your machine.
4. (Optional) Ensure the remote server automatically starts when the machine boots.

Each remote server can host one or many custom components.

{{% /tab %}}
{{% tab name="Python" %}}

{{< alert title="Tip" color="tip" >}}
For detailed instructions, see the full example in the [Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).
{{< /alert >}}

1. Code a new model of a built-in resource type by subclassing it (for example, `sensor` or `arm`). Implement any required methods from its [API definition](/reference/apis/).
2. Register the custom component on a new gRPC server instance using the [`viam.rpc` library](https://python.viam.dev/autoapi/viam/rpc/index.html).
3. Add the server as a [remote part](/hardware/multi-machine/add-a-remote-part/) of your machine.
4. (Optional) Ensure the remote server automatically starts when the machine boots.

Each remote server can host one or many custom components.

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Important" color="note" %}}

You must define all methods belonging to a built-in resource type when defining a new model. Otherwise, the class will not instantiate.

- In Python, raise `NotImplementedError()` or use `pass` in methods you do not want to implement.
- In Go, return `errUnimplemented`.

{{% /alert %}}

## Deploy a module using Docker

In rare cases, you may need to package and deploy a module using Docker. Use cases include:

- Your module has complex system dependencies that cannot be easily installed on a machine.
- You use a large container image and some layers are already cached on the machine.
- You have specific security requirements.

If you deploy using Docker, create a "first run" script to handle setup. This is not recommended for modules that do not use Docker.

### Use a `first_run` script

1. Create a tarball containing:

   - The module's entrypoint script or binary:

     ```sh {class="command-line" data-prompt="$"}
     #!/bin/bash
     exec docker run <YOUR_CONTAINER_IMAGE> <YOUR_CONTAINER_OPTIONS>
     ```

   - A [meta.json](/build-modules/module-reference/#metajson-schema) file.

   - A first-run script that runs during setup:

     ```sh {class="command-line" data-prompt="$"}
     #!/usr/bin/env bash
     docker pull mongo:6
     echo "Setup complete."
     exit 0
     ```

   [This example Makefile](https://github.com/viam-labs/wifi-sensor/blob/7823b6ad3edcbbbf20b06c34b3181453f5f3f078/Makefile) builds a module binary and bundles it with a meta.json and first-run script.

2. Edit meta.json to include the `first_run` field:

   ```json
   {
     "first_run": "first_run.sh"
   }
   ```

3. Configure the module on your machine normally. The first-run script executes once when `viam-server` receives a new configuration, and once per version update.

4. (Optional) To force the first-run script to run again without changing the module version, delete the marker file at `.viam/packages/data/module/<id>/bin.first_run_succeeded`.

5. (Optional) The default first-run timeout is 1 hour. Adjust with `"first_run_timeout": "5m"` in the module configuration.
