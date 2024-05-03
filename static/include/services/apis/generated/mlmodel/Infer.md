### Infer

{{< tabs >}}
{{% tab name="Python" %}}

Take an already ordered input tensor as an array, make an inference on the model, and return an output tensor map.

**Parameters:**

- `input_tensors` [(Dict[str, numpy.typing.NDArray])](<INSERT PARAM TYPE LINK>) (required): A dictionary of input flat tensors as specified in the metadata
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Dict[str, numpy.typing.NDArray])](INSERT RETURN TYPE LINK): A dictionary of output flat tensors as specified in the metadata

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.infer).

``` python {class="line-numbers linkable-line-numbers"}
import numpy as np

my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

nd_array = np.array([1, 2, 3], dtype=np.float64)
input_tensors = {"0": nd_array}

output_tensors = await my_mlmodel.infer(input_tensors)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `tensors` [(Tensors)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/ml#Tensors):

**Returns:**

- `ml` [(Tensors)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/ml#Tensors):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `inputTensors` [(FlatTensors)](https://flutter.viam.dev/viam_protos.service.mlmodel/FlatTensors-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.mlmodel/MLModelServiceClient/infer.html).

{{% /tab %}}
{{< /tabs >}}
