---
title: "Deploy an ML Model with the ML Model Service"
linkTitle: "Deploy Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
  - /services/ml/
description: "Deploy Machine Learning models to a machine and use the vision service to detect or classify images or to create point clouds of identified objects."
modulescript: true
icon: true
no_list: true
images: ["/services/icons/ml.svg"]
# SME: Aaron Casas
---

The Machine Learning (ML) model service allows you to deploy machine learning models to your machine.
This can mean deploying:

- a model you [trained](/ml/train-model/)
- a model from [the registry](https://app.viam.com/registry) that another user has shared publicly
- a model trained outside the Viam platform that you have [uploaded](/ml/upload-model/) to the registry privately or publicly
- a model trained outside the Viam platform that's already available on your machine

After deploying your model, you need to configure an additional service to use the deployed model.
For example, you can configure an [`mlmodel` vision service](/ml/vision/) and a [`transform` camera](/components/camera/transform/) to visualize the predictions your model makes.

## Supported models

### Built-in models

You can use the following built-in model of the service:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`tflite_cpu`](./tflite_cpu/) | Runs a TensorFlow Lite model that you have [trained](/ml/train-model/) or [uploaded](/ml/upload-model/) on the CPU of your machine. |

### Modular resources

{{<modular-resources api="rdk:service:mlmodel" type="ML model">}}

{{< alert title="Add support for other models" color="tip" >}}
If none of the existing models of the ML model service fit your use case, you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

ML models must be designed in particular shapes to work with the `mlmodel` [classification](/ml/vision/mlmodel/) or [detection](/ml/vision/mlmodel/) model of Viam's [vision service](/ml/vision/).
Follow [these instructions](/registry/advanced/mlmodel-design/) to design your modular ML model service with models that work with vision.
{{< /alert >}}

{{< alert title="Note" color="note" >}}
For some models of the ML model service, like the [Triton ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton/tree/main/) for Jetson boards, you can configure the service to use either the available CPU or a dedicated GPU.
{{< /alert >}}

## Used with

{{< cards >}}
{{< relatedcard link="/ml/vision/">}}
{{< relatedcard link="/components/board/">}}
{{< relatedcard link="/components/camera/">}}
{{< /cards >}}

## Models from registry

You can search the machine learning models that are available to deploy on this service from the registry here:

<div id="searchboxML"></div>
<p>
<div id="searchstatsML"></div></p>
<div class="mr-model" id="">
  <div class="modellistheader">
    <div class="name">Model</div>
    <div>Description</div>
  </div>
<div id="hitsML" class="modellist">
</div>
<div id="paginationML"></div>
</div>

## Versioning for deployed models

If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the machine.
If you do not want Viam to automatically deploy the `latest` version of the model, you can edit the `"packages"` array in the [JSON configuration](/build/configure/#the-configure-tab) of your machine.
This array is automatically created when you deploy the model and is not embedded in your service configuration.

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.
The model package config looks like this:

```json
"packages": [
  {
    "package": "<model_id>/<model_name>",
    "version": "YYYY-MM-DDThh-mm-ss",
    "name": "<model_name>",
    "type": "ml_model"
  }
]
```

## API

The MLModel service supports the following methods:

{{< readfile "/static/include/services/apis/ml.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with an `MLModel` service, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab's **Code sample** page on the [Viam app](https://app.viam.com) for boilerplate code to connect to your machine.

{{% /alert %}}

### Infer

Take an already ordered input tensor as an array, make an inference on the model, and return an output tensor map.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `input_tensors` [(Dict[str, NDArray])](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html): A dictionary of input flat tensors, as specified in the metadata.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(`Dict[str, NDArray]`)](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html): A dictionary of output flat tensors as specified in the metadata, after being run through an inference engine.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.infer).

```python {class="line-numbers linkable-line-numbers"}
import numpy as np

my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

nd_array = np.array([1, 2, 3], dtype=np.float64)
input_tensors = {"0": nd_array}

output_tensors = await my_mlmodel.infer(input_tensors)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `tensors` [(ml.Tensors)](https://pkg.go.dev/go.viam.com/rdk@v0.11.1/ml#Tensors): The input map of tensors, as specified in the metadata.

**Returns:**

- [(ml.Tensors)](https://pkg.go.dev/go.viam.com/rdk@v0.11.1/ml#Tensors): The output map of tensors, as specified in the metadata, after being run through an inference engine.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

```go {class="line-numbers linkable-line-numbers"}
myMLModel, err := mlmodel.FromRobot(robot, "my_mlmodel_service")

input_tensors := ml.Tensors{"0": tensor.New(tensor.WithShape(1, 2, 3), tensor.WithBacking(6))}

output_tensors, err := myMLModel.Infer(ctx.Background(), input_tensors)
```

{{% /tab %}}
{{< /tabs >}}

### Metadata

Get the metadata: name, data type, expected tensor/array shape, inputs, and outputs associated with the ML model.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(`Metadata`)](https://python.viam.dev/autoapi/viam/gen/service/mlmodel/v1/mlmodel_pb2/index.html#viam.gen.service.mlmodel.v1.mlmodel_pb2.Metadata): Name, type, expected tensor/array shape, inputs, and outputs associated with the ML model.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.metadata).

```python {class="line-numbers linkable-line-numbers"}
my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

metadata = await my_mlmodel.metadata()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(MLMetadata)](https://pkg.go.dev/go.viam.com/rdk@v0.11.1/services/mlmodel#MLMetadata): Struct containing the metadata of the model file, such as the name of the model, what kind of model it is, and the expected tensor/array shape and types of the inputs and outputs of the model.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/mlmodel#Service).

```go {class="line-numbers linkable-line-numbers"}
myMLModel, err := mlmodel.FromRobot(robot, "my_mlmodel_service")

metadata, err := myMLModel.Metadata(ctx.Background())
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own navigation service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

**Raises:**

- `NotImplementedError`: Raised if the Resource does not support arbitrary commands.

```python {class="line-numbers linkable-line-numbers"}
my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await my_mlmodel.do_command(my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myMLModel, err := mlmodel.FromRobot(robot, "my_mlmodel_service")

resp, err := myMLModel.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_mlmodel = MLModelClient.from_robot(robot, "my_mlmodel_service")

await my_mlmodel.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myMLModel, err := mlmodel.FromRobot(robot, "my_mlmodel_service")

err := myMLModel.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Use the ML model service with the Viam Python SDK

To use the ML model service from the [Viam Python SDK](https://python.viam.dev/), install the Python SDK using the `mlmodel` extra:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

You can also run this command on an existing Python SDK install to add support for the ML model service.

See the [Python documentation](https://python.viam.dev/autoapi/viam/services/mlmodel/mlmodel/index.html#viam.services.mlmodel.mlmodel.MLModel) for more information about the `MLModel` service in Python.

See [Program a machine](/build/program/) for more information about using an SDK to control your machine.

## Next steps

To make use of your model with your machine, add a [vision service](/ml/vision/) or a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}:

{{< cards >}}

{{% manualcard link="/ml/vision/mlmodel/"%}}

<h4>Create a detector with your model</h4>

Configure an `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/ml/vision/mlmodel/"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{% card link="/registry/examples/tflite-module/" customTitle="Example: TensorFlow Lite Modular Service" %}}

{{< /cards >}}
