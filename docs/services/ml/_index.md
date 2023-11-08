---
title: "ML Model Service"
linkTitle: "ML Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
description: "Deploy Machine Learning models to a smart machine."
icon: "/services/icons/ml.svg"
# SME: Aaron Casas
---

Once you have [trained](/manage/ml/train-model/) or [uploaded](/manage/ml/upload-model/) your model, the Machine Learning (ML) model service allows you to deploy machine learning models to your smart machine.

You can use the following built-in model:

{{< alert title="Note" color="note" >}}
For some models, like the [Triton MLModel](/modular-resources/examples/triton/) for Jetson boards, you can configure the service to use the available CPU or GPU.
{{< /alert >}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`"tflite_cpu"` model](#create-an-ml-model-service) | Runs a tensorflow lite model that you have [trained](/manage/ml/train-model/) or [uploaded](/manage/ml/upload-model/). |

### Modular Resources

{{<modular-resources api="rdk:service:mlmodel" type="mlmodel">}}

{{< alert title="Add support for other models" color="tip" >}}
If none of the existing models fit your use case, you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

ML Models must be designed in particular shapes to work with Viam's [vision services](/services/vision/).
Follow [these instructions](/modular-resources/advanced/mlmodel-design/) to design your modular ML Model service with models that work with vision.
{{< /alert >}}

## Create an ML model service

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to your robot's **Config** tab on the [Viam app](https://app.viam.com/robots).
Click the **Services** subtab and click **Create service** in the lower-left corner.
Select the `ML Model` type, then select the `TFLite CPU` model.
Enter a name for your service and click **Create**.

You can choose to configure your service with an existing model on the smart machine or deploy a model onto your smart machine:

{{< tabs >}}
{{% tab name="Existing Model" %}}

To configure your service with an existing model on the robot, select **Path to Existing Model On Robot** for the **Deployment** field.

Then specify the absolute **Model Path** and any **Optional Settings** such as the absolute **Label Path** and the **Number of threads**.

![Create a machine learning models service with an existing model](/services/available-models.png)

{{% /tab %}}
{{% tab name="Deploy Model" %}}

To configure your service and deploy a model onto your robot, select **Deploy Model On Robot** for the **Deployment** field.

Then select the **Models** and any **Optional Settings** such as the **Number of threads**.

![Create a machine learning models service with a model to be deployed](/services/deploy-model.png)

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the `tflite_cpu` ML model object to the services array in your raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<mlmodel_name>",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.ml_model.<model_name>}/<model-name>.tflite",
      "label_path": "${packages.ml_model.<model_name>}/labels.txt",
      "num_threads": <number>
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "fruit_classifier",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.ml_model.my_fruit_model}/my_fruit_model.tflite",
      "label_path": "${packages.ml_model.my_fruit_model}/labels.txt",
      "num_threads": 1
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"tflite_cpu"` model:

<!-- prettier-ignore -->
| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `model_path` | **Required** | The absolute path to the `.tflite model` file, as a `string`. |
| `label_path` | Optional | The absolute path to a `.txt` file that holds class labels for your TFLite model, as a `string`. The SDK expects this text file to contain an ordered listing of the class labels. Without this file, classes will read as "1", "2", and so on. |
| `num_threads` | Optional | An integer that defines how many CPU threads to use to run inference. Default: `1`. |

Save the configuration and your model will be added to your robot at <file>$HOME/.viam/packages/\<model-name\>/\<file-name\></file>.

{{< alert title="Info" color="info" >}}
If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the robot.
If you do not want Viam to automatically deploy the `latest` version of the model, you can change the `packages` configuration in the [Raw JSON robot configuration](../../manage/configuration/#the-config-tab).
{{< /alert >}}

You can get the version number from a specific model version by clicking on **COPY** on the model on the models tab of the **DATA** page.
The model package config looks like this:

```json
{
  "package": "<model_id>/allblack",
  "version": "YYYYMMDDHHMMSS",
  "name": "<model_name>",
  "type": "ml_model"
}
```

### `tflite_cpu` Limitations

We strongly recommend that you package your `.tflite_cpu` model with metadata in [the standard form](https://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs).

In the absence of metadata, your `.tflite_cpu` model must satisfy the following requirements:

- A single input tensor representing the image of type UInt8 (expecting values from 0 to 255) or Float 32 (values from -1 to 1).
- At least 3 output tensors (the rest won’t be read) containing the bounding boxes, class labels, and confidence scores (in that order).
- Bounding box output tensor must be ordered [x x y y], where x is an x-boundary (xmin or xmax) of the bounding box and the same is true for y.
  Each value should be between 0 and 1, designating the percentage of the image at which the boundary can be found.

These requirements are satisfied by a few publicly available model architectures including EfficientDet, MobileNet, and SSD MobileNet V1.
You can use one of these architectures or build your own.

## API

The MLModel service supports the following methods:

{{< readfile "/static/include/services/apis/ml.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with an `MLModel` service, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code Sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Infer

Take an already ordered input tensor as an array, make an inference on the model, and return an output tensor map.

{{< tabs >}}
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
{{< /tabs >}}

### Metadata

Get the metadata: name, data type, expected tensor/array shape, inputs, and outputs associated with the ML model.

{{< tabs >}}
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
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own navigation service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
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
{{< /tabs >}}

## Use the ML model service with the Viam Python SDK

To use the ML model service from the [Viam Python SDK](https://python.viam.dev/), install the Python SDK using the `mlmodel` extra:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

You can also run this command on an existing Python SDK install to add support for the ML model service.

See the [Python documentation](https://python.viam.dev/autoapi/viam/services/mlmodel/mlmodel/index.html#viam.services.mlmodel.mlmodel.MLModel) for more information about the `MLModel` service in Python.

See [Program a smart machine](/program/) for more information about using an SDK to control your smart machine.

## Next Steps

To make use of your model with your smart machine, add a [vision service](/services/vision/) or a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}:

{{< cards >}}

{{% manualcard link="/services/vision/detection/#configure-an-mlmodel-detector"%}}

<h4>Create a detector with your model</h4>

Configure an `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/services/vision/classification/#configure-an-mlmodel-classifier"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{% card link="/modular-resources/examples/tflite-module/" customTitle="Example: TensorFlow Lite Modular Service" %}}

{{< /cards >}}
