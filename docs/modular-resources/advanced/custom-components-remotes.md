---
title: "Add Custom Components as Remotes of Your Robot"
linkTitle: "Custom Components as Remotes"
weight: 99
type: "docs"
tags: ["server", "sdk"]
aliases:
  - "/program/extend/sdk-as-server/"
  - "/program/extend/custom-components-remotes/"
  - "/extend/custom-components-remotes/"
description: "If you are unable to use modular resources, you can implement custom components and register them on a server configured as a remote of your robot."
---

Running {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} on the [board](/components/board/) directly connected to your components is the preferred way of managing and controlling custom components.

However, if you are unable to use [modular resources](/modular-resources/) because you need to host `viam-server` on a non-Linux system or have an issue with compilation, you can use a [Viam SDK](/program/apis/) to code a custom resource implementation, host it on a server, and add it as a [remote](/manage/parts-and-remotes/) of your robot.

Once you have coded your custom component and configured the remote servers, you can control and monitor your component with the Viam SDKs, like any other component.

To show how to create a custom resource, the following example creates an arm as a custom component and registers the new arm model with a Viam SDK.
Then you can control it as part of your robot with the same [API methods](/components/arm/#api) available for [arm models built into the RDK](/components/arm/#supported-models).

## Instructions

To add a custom resource as a [remote](/manage/parts-and-remotes/):

{{< tabs >}}
{{% tab name="Go" %}}

1. Code a new model of a built-in resource type.
   You can do this by creating a new interface that implements required methods.
   The new model must implement any functions of the built-in resource type marked as required in its [RDK API definition](/modular-resources/create/#valid-apis-to-implement-in-your-model).
2. Register the custom component on a new gRPC server instance and start the server.
3. Add the server as a [remote](/manage/parts-and-remotes/) of your robot.
4. (Optional) [Configure a process](/manage/configuration/#processes) to launch this remote server to ensure the remote server is always running alongside the rest of your robot.

Each remote server can host one or many custom components.

{{% /tab %}}
{{% tab name="Python" %}}

{{< alert title="Tip" color="tip" >}}
For more detailed instructions, see the full example in the [Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).
{{< /alert >}}

1. Code a new model of a built-in resource type.
   You can do this by subclassing a built in resource type like `sensor` or `arm`.
   The new model must implement any methods of the built-in resource type marked as required in its [RDK API definition](/modular-resources/create/#valid-apis-to-implement-in-your-model).
1. Register the custom component on a new gRPC server instance and start the server.
   You can do this with the [`viam.rpc` library](https://python.viam.dev/autoapi/viam/rpc/index.html) by creating a new `rpc.server.Server` instance.
1. Add the server as a [remote](/manage/parts-and-remotes/) of your robot.
1. (Optional) [Configure a process](/manage/configuration/#processes) to launch this remote server to ensure the remote server is always running alongside the rest of your robot.

Each remote server can host one or many custom components.

{{% /tab %}}
{{% /tabs %}}

{{% alert title="Important" color="note" %}}

You must define all methods belonging to a built-in resource type when defining a new model.
Otherwise, the class will not instantiate.

- If you are using the Python SDK, raise an `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented`.
- Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}
