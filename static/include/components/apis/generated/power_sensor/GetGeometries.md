### GetGeometries

{{< tabs >}}
{{% tab name="Python" %}}

Get all geometries associated with the Component, in their current configuration, in the [frame](/mobility/frame-system/) of the Component.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[viam.proto.common.Geometry])](INSERT RETURN TYPE LINK): The geometries associated with the Component.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_geometries).

``` python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")

```

{{% /tab %}}
