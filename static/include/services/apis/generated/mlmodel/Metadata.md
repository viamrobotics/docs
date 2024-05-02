### Metadata

{{< tabs >}}
{{% tab name="Python" %}}

Get the metadata (such as name, type, expected tensor/array shape, inputs, and outputs) associated with the ML model.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.services.mlmodel.mlmodel.Metadata)](INSERT RETURN TYPE LINK): The metadata

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.metadata).

``` python {class="line-numbers linkable-line-numbers"}
my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

metadata = await my_mlmodel.metadata()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):

**Returns:**

- [(MLMetadata)](https://pkg.go.dev#MLMetadata):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.mlmodel/MLModelServiceClient/metadata.html).

{{% /tab %}}
{{< /tabs >}}
