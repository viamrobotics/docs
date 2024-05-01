### ListPlanStatuses

{{< tabs >}}
{{% tab name="Python" %}}

Returns the statuses of plans created by move_on_globe() or move_on_map() calls that meet at least one of the following conditions since the motion service initialized:

**Parameters:**

- `only_active_plans` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required): If supplied, the response will filter out any plans that are not executing
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(viam.proto.service.motion.ListPlanStatusesResponse)](INSERT RETURN TYPE LINK): List of last known statuses with the associated IDs of all plans within the TTL ordered by timestamp in ascending order

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.list_plan_statuses).

``` python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
# List the plan statuses of the motion service within the TTL
resp = await motion.list_plan_statuses()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `req`[(ListPlanStatusesReq)](<INSERT PARAM TYPE LINK>)
- [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(PlanStatusWithID)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `name` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):
- `onlyActivePlans` [(bool)](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/listPlanStatuses.html).

{{% /tab %}}
{{< /tabs >}}
