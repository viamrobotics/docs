### DoCommand

Execute model-specific commands.
If you are implementing your own generic service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
service = SERVICE.from_robot(robot, "builtin")  # replace SERVICE with the appropriate class

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await service.do_command(command=my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/generic/client/index.html#viam.services.generic.client.GenericClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

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

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/generic/client/index.html#viam.services.generic.client.GenericClient.close).

{{% /tab %}}
{{% tab name="C++" %}}

There is no need to explicitly close a generic service's resource in C++, as resource destruction is handled automatically by the generic service's class destructor when variables exit scope.

{{% /tab %}}
{{< /tabs >}}
