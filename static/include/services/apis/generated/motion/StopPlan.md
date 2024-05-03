### StopPlan

{{< tabs >}}
{{% tab name="Python" %}}

Stop a component being moved by an in progress move_on_globe() or move_on_map() call.

**Parameters:**

- `component_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName) (required): The component to stop
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.stop_plan).

``` python {class="line-numbers linkable-line-numbers"}
# Assuming a `move_on_globe()` started the execution
# Stop the base component which was instructed to move by `move_on_globe()`
# or `move_on_map()`
my_base_resource_name = Base.get_resource_name("my_base")
await motion.stop_plan(component_name=mvmnt_sensor)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `req` [(StopPlanReq)](https://pkg.go.dev#StopPlanReq):

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `componentName` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/stopPlan.html).

{{% /tab %}}
{{< /tabs >}}
