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
description: "Implement custom components and register them on a server configured as a remote of your robot."
---

{{% alert title="Tip" color="tip" %}}

[Modular resources](/modular-resources/) provided by custom {{< glossary_tooltip term_id="module" text="modules" >}} are the preferred method of creating custom resource implementations.

This option is provided for advanced users who are unable to use the modular resource system with the robot deployments.

{{% /alert %}}

If a type or model of [component](/components/) you are working with is not [built-in to the Viam RDK](/internals/rdk/), or [available from the Viam registry as a module](/modular-resources/key-concepts/), you can use a [Viam SDK](/program/apis/) to code a custom resource implementation, host it on a server, and add it as a [remote](/manage/parts-and-remotes/) of your robot.

Once you have coded your custom component and configured the remote servers, you can control and monitor your component with the Viam SDKs, like any other component.

For example, you may have a robotic arm that is not one of the models supported by [Viam’s arm component](/components/arm/), and you want to integrate it with Viam.
To use is with Viam, you can create a custom component and register the new arm model with a Viam SDK.
Then you can control it as part of your robot with the same [API methods](/components/arm/#api) available for [arm models built-in to the RDK](/components/arm/#supported-models).

This example is available in the [Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).

## Instructions

To add a custom resource as a [remote](/manage/parts-and-remotes/):

{{< tabs >}}
{{% tab name="Go" %}}

1. Code a new model of a built-in resource type. You can do this by creating a new interface that implements required methods. The new model must implement any functions of the built-in resource type marked as required in its RDK API definition.
2. Register the custom component on a new gRPC server instance and start the server.
3. Add the server as a [remote](/manage/parts-and-remotes/) of your robot.
4. Configure a command to launch this remote server as a {{< glossary_tooltip term_id="process" text="process" >}} of your robot to make sure the remote server is always running alongside the rest of your robot.

Each remote server can host one or many custom components.

{{% /tab %}}
{{% tab name="Python" %}}

1. Code a new model of a built-in resource type.
   You can do this by subclassing a built in resource type like `sensor` or `arm`.
   The new model must implement any functions of the built-in resource type marked as required in its RDK API definition.
1. Register the custom component on a new gRPC server instance and start the server.
   You can do this with the [`viam.rpc` library](https://python.viam.dev/autoapi/viam/rpc/index.html) by creating a new `rpc.server.Server` instance.
1. Add the server as a [remote](/manage/parts-and-remotes/) of your robot.
1. Configure a command to launch this remote server as a {{< glossary_tooltip term_id="process" text="process" >}} of your robot to make sure the remote server is always running alongside the rest of your robot.

Each remote server can host one or many custom components.

{{% /tab %}}
{{% /tabs %}}

{{% alert title="Important" color="note" %}}

You must define all functions belonging to a built-in resource type if defining a new model.
Otherwise, the class won’t instantiate.

- If you are using the Python SDK, raise an `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented`.
- Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

The following tutorial also explains how to add a custom component as a remote:

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot" %}}
{{< /cards >}}
