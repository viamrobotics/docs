### GetGeometries

{{< tabs >}}
{{% tab name="Python" %}}

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[viam.proto.common.Geometry])](INSERT RETURN TYPE LINK): The geometries associated with the Component.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_geometries).

``` python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.arm/ArmServiceClient/getGeometries.html).

{{% /tab %}}
{{< /tabs >}}
