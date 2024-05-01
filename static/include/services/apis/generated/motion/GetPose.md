### GetPose

{{< tabs >}}
{{% tab name="Python" %}}

Get the Pose and observer [frame](/mobility/frame-system/) for any given component on a robot. A component_name can be created like this:

**Parameters:**

- `component_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName) (required): Name of a component on a robot.
- `destination_frame` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the desired reference frame.
- `supplemental_transforms` [(List[viam.proto.common.Transform])](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Transform) (optional): Transforms used to augment the robot’s frame while calculating pose.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(viam.proto.common.PoseInFrame)](INSERT RETURN TYPE LINK): Pose of the given component and the frame in which it was observed.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_pose).

``` python {class="line-numbers linkable-line-numbers"}
component_name = Arm.get_resource_name("arm")

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `componentName`[(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/resource#componentName):
- `destinationFrame`[(string)](<INSERT PARAM TYPE LINK>)
- `referenceframe`[(LinkInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/referenceframe#referenceframe):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.
- [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `referenceframe`[(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/referenceframe#referenceframe):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `componentName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)> (required):
- `destinationFrame` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)> (required):
- `extra` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)> (required):
- `name` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)> (required):
- `supplementalTransforms` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Transform](https://flutter.viam.dev/viam_protos.common.common/Transform-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/getPose.html).

{{% /tab %}}
{{< /tabs >}}
