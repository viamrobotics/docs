### Infer

Take an already ordered input tensor as an array, make an inference on the model, and return an output tensor map.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `input_tensors` (Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [typing.NDArray](https://numpy.org/doc/stable/reference/typing.html#numpy.typing.NDArray)]) (required): A dictionary of input flat tensors as specified in the metadata.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Dict[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), [typing.NDArray](https://numpy.org/doc/stable/reference/typing.html#numpy.typing.NDArray)]): A dictionary of output flat tensors as specified in the metadata.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
import numpy as np

my_mlmodel = MLModelClient.from_robot(robot=machine, name="my_mlmodel_service")

image_data = np.zeros((1, 384, 384, 3), dtype=np.uint8)

# Create the input tensors dictionary
input_tensors = {
    "image": image_data
}

output_tensors = await my_mlmodel.infer(input_tensors)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.infer).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `tensors` [(ml.Tensors)](https://pkg.go.dev/go.viam.com/rdk/ml#Tensors): The input map of tensors, as specified in the metadata.

**Returns:**

- [(ml.Tensors)](https://pkg.go.dev/go.viam.com/rdk/ml#Tensors): The output map of tensors, as specified in the metadata, after being run through an inference engine.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/ml"
  "gorgonia.org/tensor"
 )

myMLModel, err := mlmodel.FromRobot(machine, "my_mlmodel")

input_tensors := ml.Tensors{
  "image": tensor.New(
    tensor.Of(tensor.Uint8),
    tensor.WithShape(1, 384, 384, 3),
          tensor.WithBacking(make([]uint8, 1*384*384*3)),
  ),
}

output_tensors, err := myMLModel.Infer(context.Background(), input_tensors)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

{{% /tab %}}
{{< /tabs >}}

### Metadata

Get the metadata: name, data type, expected tensor/array shape, inputs, and outputs associated with the ML model.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.services.mlmodel.mlmodel.Metadata): The metadata.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_mlmodel = MLModelClient.from_robot(robot=machine, name="my_mlmodel_service")

metadata = await my_mlmodel.metadata()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(MLMetadata)](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#MLMetadata): Name, type, expected tensor/array shape, inputs, and outputs associated with the ML model.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myMLModel, err := mlmodel.FromRobot(machine, "my_mlmodel")
metadata, err := myMLModel.Metadata(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own ML model service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myMlmodelSvc, err := mlmodel.FromRobot(machine, "my_mlmodel_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myMlmodelSvc.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the ML model service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_mlmodel_svc_name = MLModelClient.get_resource_name("my_mlmodel_svc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
my_mlmodel, err := mlmodel.FromRobot(machine, "my_ml_model")

err := my_mlmodel.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

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
my_mlmodel_svc = MLModelClient.from_robot(robot=machine, name="my_mlmodel_svc")
await my_mlmodel_svc.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
my_mlmodel, err := mlmodel.FromRobot(machine, "my_ml_model")

err := my_mlmodel.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
