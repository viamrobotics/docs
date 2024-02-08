---
title: "Generic Service"
linkTitle: "Generic"
childTitleEndOverwrite: "Generic Service"
weight: 55
type: "docs"
description: "A service that does not fit any of the other APIs."
tags: ["generic", "services"]
icon: "/icons/components/generic.svg"
images: ["/icons/components/generic.svg"]
no_list: true
modulescript: true
# SMEs:
---

The _generic_ service {{< glossary_tooltip term_id="subtype" text="subtype" >}} enables you to add support for unique types of services that do not already have an [appropriate API](/build/program/apis/#service-apis) defined for them.

For example, when writing code to manage [simultaneous localization and mapping (SLAM)](/mobility/slam/) for your machine, it makes sense to use the existing [SLAM API](/mobility/slam/#api), which provides specific functionality required for generating accurate maps of an environment.
However, if you want to create a new service to monitor your machine's CPU and RAM usage for example, you need very different functionality that isn't currently exposed in any API.
Instead, you can use the generic service API to add support for your unique type of service, like local system monitoring, to your machine.

There are no built-in generic service models (other than `fake`).
Use generic for a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} model that represents a unique type of service.

{{% alert title="Important" color="note" %}}

The generic service API only supports the `DoCommand` method.
If you use the generic subtype, your module needs to define any and all service functionality and pass it through `DoCommand`.

Whenever possible, it is best to use an [existing service API](/services/) instead of generic so that you do not have to replicate code.
If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and extra parameters to add custom functionality to an [existing subtype](/services/), instead of using the generic service.

{{% /alert %}}

## Supported models

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
Model | Description
----- | -----------
[`fake`](fake/) | A model used for testing a generic service.

## Control your machine with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `generic` service from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

Be sure to import the generic service package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.generic import Generic
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/generic"
)
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
#include <viam/sdk/services/generic/generic.hpp>
```

{{% /tab %}}
{{< /tabs >}}

## API

The generic service supports the following method:

{{< readfile "/static/include/services/apis/generic.md" >}}

### DoCommand

Execute model-specific commands.
If you are implementing your own generic service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_generic = Generic.from_robot(robot=robot, name="my_generic_service")

raw_dict = {
  "command": "raw",
  "raw_input": "home"
}
await my_generic.do_command(raw_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/generic/client/index.html#viam.services.generic.client.GenericClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myGeneric, err := generic.FromRobot(robot, "my_generic_service")

resp, err := myGeneric.DoCommand(ctx, map[string]interface{}{"command": "example"})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/api/blob/main/service/generic/v1/generic_grpc.pb.go).

{{% /tab %}}
{{% tab name="C++" %}}

**Parameters:**

- `command` [(AttributeMap)](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/common/proto_type.hpp#L13): The command to execute.

**Returns:**

- [(AttributeMap)](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/common/proto_type.hpp#L13): Result of the executed command.

```cpp {class="line-numbers linkable-line-numbers"}
auto my_generic = robot->resource_by_name<GenericService>("my_generic_service");
auto example = std::make_shared<ProtoType>(std::string("example"));
AttributeMap command =
    std::make_shared<std::unordered_map<std::string, std::shared_ptr<ProtoType>>>();
command->insert({{std::string("command"), example}});
auto resp = my_generic->do_command(command);
```

For more information, see the [C++ SDK Docs](https://cpp.viam.dev/classviam_1_1sdk_1_1GenericService.html)

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_generic = Generic.from_robot(robot, "my_generic")

await my_generic.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/generic/client/index.html#viam.services.generic.client.GenericClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred. Close will never return an error for a generic resource.

```go {class="line-numbers linkable-line-numbers"}
myGeneric, err := generic.FromRobot(robot, "my_generic")

err := myGeneric.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#TriviallyCloseable).

{{% /tab %}}
{{% tab name="C++" %}}

There is no need to explicitly close a generic service's resource in C++, as resource destruction is handled automatically by the generic service's class destructor when variables exit scope.

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
