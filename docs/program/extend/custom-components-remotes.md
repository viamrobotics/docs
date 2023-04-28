---
title: "Add Custom Components as Remotes of Your Robot"
linkTitle: "Custom Components as Remotes"
weight: 99
type: "docs"
tags: ["server", "sdk"]
aliases:
    - "program/extend/custom-components-remotes"
description: "Implement custom components and register them on a server configured as a remote of your robot."
webmSrc: "/tutorials/img/custom-base-dog/base-control-dog.webm"
mp4Src: "/tutorials/img/custom-base-dog/base-control-dog.mp4"
videoAlt: "A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the robot's Control tab on the Viam app open in a browser window."
---

{{% alert title="Caution" color="caution" %}}
{{< glossary_tooltip term_id="module" text="Modular resources" >}} are the preferred method of creating custom resource implementations for SDKs with module support unless you are hosting `viam-server` on a non-Linux platform or have another issue with compilation.

Instructions on creating and using modular resources are available [here](/program/extend/modular-resources).
{{% /alert %}}

If a type or model of [component](/components) you are working with is not built-in to the [Viam RDK](/internals/rdk), you can use a [Viam SDK](/program/get-started-sdks) to code a custom resource implementation, host it on a server, and add it as a [remote](/manage/parts-and-remotes) of your robot.

After configuring the remote server, control and monitor your component programmatically with the SDKs and from the [Viam app](https://app.viam.com/).

For example:

- You have a robotic arm that is not one of the models supported by [Viam's arm component](/components/arm/), and you want to integrate it with Viam.
- You create a custom component and register the new arm model with a Viam SDK.
- You control it remotely as part of your robot.

This example is available in the [Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).

## Instructions

To add a custom resource as a [remote](/manage/parts-and-remotes):

{{< tabs >}}
{{% tab name="Go" %}}

1. Code a new model of a built-in resource type. You can do this by creating a new interface that implements required methods. The new model must implement any functions of the built-in resource type marked as required in its RDK API definition.
2. Register the custom component on a new gRPC server instance and start the server.
3. Add the server as a [remote](/manage/parts-and-remotes) of your robot.
4. Configure a command to launch this remote server as a [process](/appendix/glossary/#term-process) of your robot to make sure the remote server is always running alongside the rest of your robot.

{{% /tab %}}
{{% tab name="Python" %}}

1. Code a new model of a built-in resource type.
You can do this by subclassing a built in resource type like `sensor` or `arm`.
The new model must implement any functions of the built-in resource type marked as required in its RDK API definition.
2. Register the custom component on a new gRPC server instance and start the server.
You can do this with the `viam.rpc.server` library.
3. Add the server as a [remote](/manage/parts-and-remotes) of your robot.
4. Configure a command to launch this remote server as a [process](/appendix/glossary/#term-process) of your robot to make sure the remote server is always running alongside the rest of your robot.

{{% /tab %}}
{{% /tabs %}}

{{% alert title="Note" color="note" %}}

You must define all functions belonging to a built-in resource type if defining a new model.
Otherwise, the class won’t instantiate.

- If you are using the Python SDK, raise an `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented`.  
- Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

The following tutorials also explain how to add custom components as remotes:

{{< cards >}}
    {{% card link="/tutorials/custom/custom-base-dog" size="small" %}}
    {{% card link="/tutorials/projects/make-a-plant-watering-robot" size="small" %}}
{{< /cards >}}
