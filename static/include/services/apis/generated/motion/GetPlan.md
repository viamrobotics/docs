### GetPlan

{{< tabs >}}
{{% tab name="Python" %}}

By default: returns the plan history of the most recent move_on_globe() or move_on_map() call to move a component.

**Parameters:**

- `component_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName) (required): The component to stop
- `last_plan_only` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): If supplied, the response will only return the last plan for the component / execution
- `execution_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): If supplied, the response will only return plans with the provided execution_id
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.proto.service.motion.GetPlanResponse)](INSERT RETURN TYPE LINK): The current PlanWithStatus & replan history which matches the request

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_plan).

``` python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
my_base_resource_name = Base.get_resource_name("my_base")
# Get the plan(s) of the base component which was instructed to move by `MoveOnGlobe()` or `MoveOnMap()`
resp = await motion.get_plan(component_name=my_base_resource_name)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `req` [(PlanHistoryReq)](https://pkg.go.dev#PlanHistoryReq):
- [())](<INSERT PARAM TYPE LINK>):

**Returns:**

- [(PlanWithStatus)](https://pkg.go.dev#PlanWithStatus):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `componentName` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html) (required):
- `executionId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `lastPlanOnly` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/getPlan.html).

{{% /tab %}}
{{< /tabs >}}
