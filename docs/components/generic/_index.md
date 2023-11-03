---
title: "Generic Component"
linkTitle: "Generic"
childTitleEndOverwrite: "Generic Component"
weight: 55
type: "docs"
description: "A component that does not fit any of the other APIs."
tags: ["generic", "components"]
icon: "/icons/components/generic.svg"
images: ["/icons/components/generic.svg"]
no_list: true
# SMEs:
---

The _generic_ component {{< glossary_tooltip term_id="subtype" text="subtype" >}} enables you to add support for unique types of hardware that do not already have an [appropriate API](/program/apis/#component-apis) defined for them.

For example, when using an [arm component](/components/arm/), it makes sense to use the [arm API](/components/arm/#api), which provides specific functionality an arm component needs, such as moving to position or stopping movement.
But if you want to use an LED display, you need very different functionality that isn't currently exposed in any API.
Instead, you can use the generic component API to add support for your unique type of hardware, like LED displays, to your smart machine.

There are no built-in generic component models (other than `fake`).
Use generic for a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} model that represents a unique type of hardware.

{{% alert title="Important" color="note" %}}

The generic component API only supports the `DoCommand` method.
If you use the generic subtype, your module needs to define any and all component functionality and pass it through `DoCommand`.

Whenever possible, it is best to use an [existing component API](/components/) instead of generic so that you do not have to replicate code.
If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and extra parameters to add custom functionality to an [existing subtype](/components/), instead of using generic.

{{% /alert %}}

## Supported Models

Before creating a new generic component, check whether one of the following [modular resources](#modular-resources) supports your component.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
Model | Description
----- | -----------
[`fake`](fake/) | A model used for testing, with no physical hardware.

### Modular Resources

{{<modular-resources api="rdk:component:generic" type="generic">}}

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by getting your `generic` component from the robot with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your robot.
If your board has a different name, change the `name` in the code.

Be sure to import the generic package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.generic import Generic
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/generic"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The generic component supports the following method:

{{< readfile "/static/include/components/apis/generic.md" >}}

### DoCommand

Execute model-specific commands.
If you are implementing your own generic component and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_generic = Generic.from_robot(robot=robot, name="my_generic_component")

raw_dict = {
  "command": "raw",
  "raw_input": "home"
}
await my_generic.do_command(raw_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/generic/client/index.html#viam.components.generic.client.GenericClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myGeneric, err := generic.FromRobot(robot, "my_generic_component")

resp, err := myGeneric.DoCommand(ctx, map[string]interface{}{"command": "example"})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/api/blob/main/component/generic/v1/generic_grpc.pb.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
