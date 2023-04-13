---
title: "Add Custom Components as Remotes of Your Robot"
linkTitle: "Custom Components as Remotes"
weight: 99
type: "docs"
tags: ["server", "sdk"]
description: "Implement custom components and register them on a server configured as a remote of your robot."
webmSrc: "/tutorials/img/custom-base-dog/base-control-dog.webm"
mp4Src: "/tutorials/img/custom-base-dog/base-control-dog.mp4"
videoAlt: "A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the robot's Control tab on the Viam app open in a browser window."
---

If a type or model of [component](/components) you are working with is not built into the [Viam RDK](/internals/rdk), you can use a [Viam SDK](/program/sdk-as-client) to code a custom resource implementation, host it on a server, and add it as a [remote](/manage/parts-and-remotes) of your robot.
Then, you can configure a command to launch this remote server as a [process](/appendix/glossary/#term-process) of your robot to make sure the remote server is always running alongside the rest of your robot.

After configuring the remote server, you can control and monitor your component programmatically with the SDKs and from the [Viam app](https://app.viam.com/).

This option makes reconfiguration more difficult than programming custom [modular resources](/program/extend/modular-resources), and is a less seamless integration.

For example, let's say that you have a robotic arm that is not one of the models supported by [Viam's arm component](/components/arm/), and you want to integrate it with Viam.
You will need to create a custom component and register the new arm model in order to use it with the Viam SDK.
Once your new arm is registered, you will be able to use it remotely with Viam.

{{% alert title="Tip" color="tip" %}}
Here is an example of [how to create a custom arm component in the Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).
{{% /alert %}}

To add a custom resource as a remote:

1. Subclass a component and implement desired functions.

    You must define all functions belonging to a built-in resource type if defining a new model.
    Otherwise, the class won't instantiate.
    If you are using the Python SDK, put `pass` or `raise NotImplementedError()` in the body of functions you do not want to implement.
    If you are using the Go SDK, leave the body of functions you do not want to implement empty.

2. Register the custom component on a new `rpc.server.Server` instance and start the server.
3. Add the server as a remote of your robot.
4. Add a process to your robot that runs the server.

## See also

A complete tutorial on how to create a custom component with the Viam Python SDK is available [here](https://python.viam.dev/examples/example.html#create-custom-components).

More examples:

{{< cards >}}
    {{% card link="/tutorials/custom/custom-base-dog" size="small" %}}
    {{% card link="/tutorials/projects/make-a-plant-watering-robot" size="small" %}}
{{< /cards >}}
