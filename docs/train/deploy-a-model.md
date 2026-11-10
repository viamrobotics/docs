---
linkTitle: "Deploy a model"
title: "Deploy a model to a machine"
weight: 30
layout: "docs"
type: "docs"
description: "Add a trained model and the resource that runs it to a machine's configuration, from the Viam app or with the Fleet API."
capabilities: ["ml-models", "vision-service"]
diataxis: how-to
---

Deploy a model to add it to a machine's configuration, along with the resource that runs it and the module that provides that resource.
The machine downloads the model and starts the resource.

## Prerequisites

- A model in your organization or the registry, trained on Viam or [uploaded](/vision/deploy-and-maintain/deploy-custom-model/).
- A machine running on a platform that a module for your model's framework supports. See [What runs the model](#what-runs-the-model).

## What runs the model {#what-runs-the-model}

A model's [framework](/train/overview/#framework) decides which resource runs it:

| Framework      | Module                                                                   | Resource model                         | Hardware                                             |
| -------------- | ------------------------------------------------------------------------ | -------------------------------------- | ---------------------------------------------------- |
| **TFLite**     | [`viam:tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu)         | `viam:mlmodel-tflite:tflite_cpu`       | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 |
| **TensorFlow** | [`viam:tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu) | `viam:mlmodel:tensorflow-cpu`          | linux/amd64, linux/arm64, darwin/arm64               |
| **PyTorch**    | [`viam:torch-cpu`](https://app.viam.com/module/viam/torch-cpu)           | `viam:mlmodel:torch-cpu`               | linux/arm64, darwin/arm64                            |
| **ONNX**       | [`viam:onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu)             | `viam:mlmodel:onnx-cpu`                | linux/amd64, linux/arm64, darwin/arm64               |
| **Registry**   | The module the training script names                                     | The resource the training script names | Whatever the module supports                         |

The first four are ML model services (API `rdk:service:mlmodel`).
To run a TensorFlow, PyTorch or ONNX model on an Nvidia Jetson GPU, configure the [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) ML model service instead.
You can configure `triton` to use either the CPU or the GPU at runtime.
Each module's README lists the model files and tensor shapes it expects.

A **Registry** model runs in the module resources its training script named when the script was uploaded to the registry.
Models the script trains carry that list, and deploying adds those resources.
They can use any API, such as an arm or a generic service, and don't need an ML model service.

## Deploy the model

Deploying adds three entries to the machine part's configuration: the module, the model package, and the resource that runs the model.

{{< tabs >}}
{{% tab name="Viam app" %}}

Deploy from the model's page, or add the model to a machine from the machine's **CONFIGURE** tab.
Both add the same configuration.

**From the model's page:**

1. Go to **DATA** > **MODELS** and click the model, or open a public model's page in the registry.
1. In the model header, click **Deploy**.
1. Select a **Version**, **Location**, **Machine** and **Part**, then click **Continue**.
   The version defaults to **Latest**; see [Choose a model version](#choose-a-model-version).
1. Name the resource that runs the model.
   For a TFLite, TensorFlow, PyTorch or ONNX model, this is the ML model service.
   For a **Registry** model, there's one name for each module resource the training script specified.
   Expand **supporting modules** to see the modules that will be installed on the machine.
1. Click **Continue**, or **Deploy** for a **Registry** model.
1. Optional, for classification and detection models: keep **Include Vision service** on to add a vision service that turns the model's output into labels and bounding boxes.
   It uses an existing camera on your machine.
   To configure it yourself later, or for any other model, turn it off.
   See [Configure a vision pipeline](/vision/configure/).
1. Click **Deploy**.

**From the machine's CONFIGURE tab:**

1. Click **+** and select **Blocks**.
1. Search for the model by name and select it.
   Models show an **ML model file** badge.
1. Name the resource that runs the model.
   For a classification or detection model, this also adds a vision service; name it too.
1. Click **Add to machine**, then click **Save**.

{{% /tab %}}
{{% tab name="Python" %}}

Read the part's configuration, add the module, the package and the resource, and write it back with [`update_robot_part`](/reference/apis/fleet/#updaterobotpart).
`update_robot_part` replaces the part's whole configuration.
Pass `last_known_update` so the call fails, instead of overwriting, if someone else changed the configuration since you read it.

- In the package entry, `package` is `<org-id>/<model-name>` and `version` is a version or `latest`.
  See [Choose a model version](#choose-a-model-version).
- The resource finds the model through `${packages.ml_model.<package-name>}`.
  For a TFLite, PyTorch or ONNX model, `model_path` appends the model file name.
  For a TensorFlow SavedModel, `model_path` is the package directory.
  `label_path`, if the model has a labels file, points to that file the same way.

```python
PART_ID = "<part-id>"
PACKAGE = "<org-id>/my-model"

# viam_client is a connected ViamClient
cloud = viam_client.app_client

part = await cloud.get_robot_part(robot_part_id=PART_ID)
config = part.robot_config or {}

config.setdefault("modules", []).append({
    "type": "registry",
    "name": "viam_tflite_cpu",
    "module_id": "viam:tflite_cpu",
    "version": "latest",
})
config.setdefault("packages", []).append({
    "name": "my-model",
    "package": PACKAGE,
    "type": "ml_model",
    "version": "latest",
})
config.setdefault("services", []).append({
    "name": "my-ml-model",
    "api": "rdk:service:mlmodel",
    "model": "viam:mlmodel-tflite:tflite_cpu",
    "attributes": {
        "package_reference": PACKAGE,
        "model_path": "${packages.ml_model.my-model}/<model-file>.tflite",
        "label_path": "${packages.ml_model.my-model}/labels.txt",
    },
})

await cloud.update_robot_part(
    robot_part_id=PART_ID,
    name=part.name,
    robot_config=config,
    last_known_update=part.last_updated,
)
```

Skip the `modules` entry if the part already has that module.

For a **Registry** model, use the module and resource model its training script named, and the API that module declares for that model; the module's registry page lists them.
Set only `model_path`, to the package directory: `"${packages.ml_model.<package-name>}"`.
A component goes under `components` instead of `services`.
The module's README lists any other attributes the resource needs.

{{% /tab %}}
{{% tab name="Go" %}}

Read the part's configuration, add the module, the package and the resource, and write it back with [`UpdateRobotPart`](/reference/apis/fleet/#updaterobotpart).
`UpdateRobotPart` replaces the part's whole configuration, and the Go SDK doesn't check whether someone else changed it since you read it.

```go
// viamClient is a connected *app.ViamClient
appClient := viamClient.AppClient()

partID := "<part-id>"
pkg := "<org-id>/my-model"

part, _, err := appClient.GetRobotPart(ctx, partID)
if err != nil {
    logger.Fatal(err)
}
config := part.RobotConfig
if config == nil {
    config = map[string]interface{}{}
}

appendEntry := func(key string, entry map[string]interface{}) {
    list, _ := config[key].([]interface{})
    config[key] = append(list, entry)
}
appendEntry("modules", map[string]interface{}{
    "type":      "registry",
    "name":      "viam_tflite_cpu",
    "module_id": "viam:tflite_cpu",
    "version":   "latest",
})
appendEntry("packages", map[string]interface{}{
    "name":    "my-model",
    "package": pkg,
    "type":    "ml_model",
    "version": "latest",
})
appendEntry("services", map[string]interface{}{
    "name":  "my-ml-model",
    "api":   "rdk:service:mlmodel",
    "model": "viam:mlmodel-tflite:tflite_cpu",
    "attributes": map[string]interface{}{
        "package_reference": pkg,
        "model_path":        "${packages.ml_model.my-model}/<model-file>.tflite",
        "label_path":        "${packages.ml_model.my-model}/labels.txt",
    },
})

if _, err := appClient.UpdateRobotPart(ctx, partID, part.Name, config); err != nil {
    logger.Fatal(err)
}
```

The entries are the same as in the **Python** tab, which also covers **Registry** models.

{{% /tab %}}
{{< /tabs >}}

To deploy the same model to many machines, add these entries to a fragment instead.
See [Deploy ML models across your fleet](/fleet/deploy-ml-models/).

## Choose a model version {#choose-a-model-version}

Each time you train or upload a model under the same name, the registry gets a new version of it.
When you deploy the model, you choose which version the machine runs:

- **Latest** moves the machine to each new version as soon as it's published, with no change to its configuration.
  This is the default.
  Use it during development, so every training run reaches your test machine.
- **A specific version** keeps the machine on that version until you change it.
  Use it in production, so a new version reaches your machines only when you decide.

The choice is stored as the `version` of the model's entry in the machine's `packages`, either `latest` or a version name:

```json
{
  "packages": [
    {
      "name": "my-model",
      "package": "<org-id>/my-model",
      "version": "2026-04-10T12-00-00",
      "type": "ml_model"
    }
  ]
}
```

The resource's attributes, such as `model_path`, stay the same across versions.

### Update or roll back a deployed model {#update-a-deployed-model}

A machine on **Latest** updates by itself.
To move a machine pinned to a specific version, change the version:

1. On the machine's **CONFIGURE** tab, open the ML model service's configuration card.
1. Select the new version from the **Version** dropdown.
   For a **Registry** model, switch to **JSON** mode and change `version` on the model's entry in `packages` instead.
1. Click **Save**.

The machine downloads the new version and reloads the resource that runs it.
A vision service that uses the model, and your code, don't need to change.
To roll back, select the previous version the same way.

Test a new version on one machine before you move the rest.
To update many machines at once, or in stages, see [Deploy ML models across your fleet](/fleet/deploy-ml-models/).

## Verify the model loaded

1. On the machine's **CONFIGURE** tab, check that the new resource shows no errors.
   The first start can take a few minutes while the machine downloads the module and the model.
1. On the **CONTROL** tab, open the resource.
   For an ML model service, call `metadata` from code to see the model's input and output tensors.
   See the [ML model service API](/reference/apis/services/ml/#metadata).

<!-- When "Run a robot policy" (DOCS-5063 N3) exists, link it here for Registry robot policy models. -->

## Troubleshooting

{{< expand "The model doesn't load" >}}

- **Check the package path.** `model_path` must name the package's `name` from `packages`, and, for TFLite, PyTorch and ONNX, a file that's in the model version you deployed.
- **Check the platform.** The module must support the machine's platform. See [What runs the model](#what-runs-the-model).
- **Check the machine is online.** The machine downloads the module and the model from the cloud.
- **Check the logs.** The machine's **LOGS** tab shows errors from the module.

{{< /expand >}}

## What's next

- Classification and detection models: [Configure a vision pipeline](/vision/configure/), then [Detect objects](/vision/object-detection/detect/) or [Classify images](/vision/classify/).
- Any model in an ML model service: run it with `infer` from the [ML model service API](/reference/apis/services/ml/).
- Many machines: [Deploy ML models across your fleet](/fleet/deploy-ml-models/).
