---
linkTitle: "Custom training scripts"
title: "Custom training scripts"
tags: ["data management", "ml", "model training"]
weight: 30
layout: "docs"
type: "docs"
languages: ["python"]
viamresources: ["mlmodel", "data_manager"]
platformarea: ["ml"]
description: "Use or write custom training scripts to train ML models on the Viam platform with any framework or logic."
date: "2024-12-04"
updated: "2025-10-13"
---

Viam's [managed training](/train/train-a-model/) handles TensorFlow and TFLite classification and detection out of the box.
For anything else, you can use a custom training script: a different framework, custom preprocessing, non-image data, or a training pipeline you want to share with your organization.

Before writing your own, check the [registry](https://app.viam.com/registry?type=Training+Script) for existing training scripts and [pre-trained models](https://app.viam.com/registry?type=ML+Model) you can deploy directly.
If a training script there fits your needs, skip ahead to [Submit a training job](#submit-a-training-job).

## How custom training scripts work

When you submit a custom training job, Viam:

1. Pulls your dataset and writes a JSONLines metadata file plus the
   underlying image files into the container.
2. Runs your script inside a Viam-hosted Docker container with GPU access
   and a framework version you select.
3. Packages the artifacts your script writes to the output directory and
   publishes them as a new model version in your organization's registry.

Because the script runs in a known container and receives standardized
inputs, you can retrain on new datasets without changing the script or
redeploying code.

## Write a training script

A training script is a Python project that the Viam platform runs in the cloud.
The platform provides your script with a dataset and an output directory; your script produces a trained model.

### File structure

```treeview
my-training/
├── model/
│   ├── training.py
│   └── __init__.py
└── setup.py
```

`setup.py` declares your dependencies:

```python {class="line-numbers linkable-line-numbers"}
from setuptools import find_packages, setup

setup(
    name="my-training",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add your dependencies here, for example:
        # "tensorflow>=2.11",
        # "numpy",
    ],
)
```

### training.py

Your script receives two required command-line arguments from the platform:

| Argument                   | Description                                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `--dataset_file`           | Path to a [JSONLines](https://jsonlines.org/) file containing dataset metadata: file paths and annotations for each data point. |
| `--model_output_directory` | Directory where your script must save its model artifacts.                                                                      |

You can add custom arguments (like `--num_epochs` or `--labels`) and pass them when you submit the training job.

Here is the overall shape of a training script:

```python {class="line-numbers linkable-line-numbers"}
import argparse
import json
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", dest="data_json",
                        type=str, required=True)
    parser.add_argument("--model_output_directory", dest="model_dir",
                        type=str, required=True)
    # Add custom arguments as needed:
    parser.add_argument("--num_epochs", dest="num_epochs",
                        type=int, default=200)
    return parser.parse_args()


def load_dataset(data_json):
    """Parse the JSONLines dataset file."""
    entries = []
    with open(data_json, "r") as f:
        for line in f:
            entries.append(json.loads(line))
    return entries


if __name__ == "__main__":
    args = parse_args()
    dataset = load_dataset(args.data_json)

    # --- Your training logic goes here ---
    # Use the dataset entries to train a model with
    # whatever framework fits your use case.
    model = ...
    labels = ...

    # Save model artifacts to the output directory.
    # The format must match what your ML model service expects.
    # For example, tflite_cpu expects a .tflite file and labels.txt.
    with open(os.path.join(args.model_dir, "model.tflite"), "wb") as f:
        f.write(model)
    with open(os.path.join(args.model_dir, "labels.txt"), "w") as f:
        f.write("\n".join(labels))
```

The critical parts:

- **Parse arguments**: Accept `--dataset_file` and `--model_output_directory` at minimum.
- **Read the dataset**: Each line in the JSONLines file is a JSON object. For image datasets, each object has an `image_path` and either `classification_annotations`, `bounding_box_annotations`, or both. Non-image datasets will have a different structure depending on how the data was captured.
- **Save to the output directory**: When the job completes, Viam packages everything in this directory and publishes it to the registry as a new model version. Files in a `tmp/` subdirectory are excluded: use it for intermediate work.

If the script exits with a non-zero status or produces no files in the output directory, the training job is marked as failed.

### Dataset file format

Each line of the dataset file is a JSON object like this:

```json
{
  "image_path": "/path/to/data/img1.jpeg",
  "classification_annotations": [{ "annotation_label": "blue_star" }],
  "bounding_box_annotations": [
    {
      "annotation_label": "blue_star",
      "x_min_normalized": 0.382,
      "x_max_normalized": 0.51,
      "y_min_normalized": 0.356,
      "y_max_normalized": 0.527
    }
  ]
}
```

Bounding box coordinates are normalized to the range 0.0-1.0 relative to image dimensions.
For classification, read `classification_annotations`.
For object detection, read `bounding_box_annotations`.
See the [example training script](https://github.com/viam-modules/classification-tflite) for complete parsing functions that handle both annotation types.

### Accessing Viam APIs

The platform provides `API_KEY` and `API_KEY_ID` environment variables if your script needs to call [Viam APIs](/reference/apis/) during training, for example, to query additional data:

```python
import os
from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions.with_api_key(
        os.environ.get("API_KEY"), os.environ.get("API_KEY_ID")
    )
    return await ViamClient.create_from_dial_options(dial_options)
```

### Match your output to an ML model service

After training, Viam packages your output directory and publishes it as a
model version in your organization's registry. To run the model on a
machine, the [ML model service](/train/deploy-a-model/) you deploy with it
must be able to load the files your script wrote.

For TFLite models loaded with `tflite_cpu`, save a `model.tflite` file and
a `labels.txt` listing each label on its own line. This is what the
[classification-tflite example](https://github.com/viam-modules/classification-tflite)
produces.

For other frameworks, consult the module's README on the registry -- for
example, [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu),
[`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu), or
[`torch-cpu`](https://app.viam.com/module/viam/torch-cpu) -- for the file
format and tensor shape expectations. Write your output in that format so
the deployed model loads correctly.

After uploading, follow [Deploy a model to a machine](/train/deploy-a-model/)
to add the matching ML model service and vision service to your machine.

### Complete example

For a full working training script, see the [classification-tflite example](https://github.com/viam-modules/classification-tflite) on GitHub.
It trains a TFLite single-label classification model using TensorFlow and Keras.

## Test and upload

Before submitting a cloud training job, test your script locally against an exported dataset.

### Export a dataset

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=<destination> --dataset-id=<dataset-id>
```

This downloads the binary data files and a `dataset.jsonl` metadata file.
To download only the JSONL file without binary data, add `--only-jsonl`.

You can get the dataset ID from the [**DATASETS** tab](https://app.viam.com/data/datasets) or by running [`viam dataset list`](/cli/datasets-and-training/#list-datasets).

### Test locally with Docker

The `test-local` command runs your training script inside the same Docker container that cloud training uses.
This catches problems that plain Python testing misses: missing system dependencies, Python version differences, and package conflicts.

```sh {class="command-line" data-prompt="$"}
viam training-script test-local \
  --training-script-directory=my-training/ \
  --dataset-file=dataset.jsonl \
  --dataset-root=<destination> \
  --model-output-directory=<output-dir>
```

The `--dataset-file` path is relative to `--dataset-root`.
The command mounts your script, dataset, and output directories into the container.

To match a specific cloud container version, use `--container-version`.
Run `viam train containers list` to list available container versions with their framework versions and end-of-life dates.

You can pass custom arguments with `--custom-args`:

```sh {class="command-line" data-prompt="$"}
viam training-script test-local \
  --training-script-directory=my-training/ \
  --dataset-file=dataset.jsonl \
  --dataset-root=<destination> \
  --model-output-directory=<output-dir> \
  --custom-args=num_epochs=5,labels="label1 label2"
```

{{% alert title="Note" color="note" %}}
The training containers are built for linux/x86_64 (amd64).
On ARM systems like Apple Silicon Macs, Docker uses Rosetta 2 emulation automatically, which may be slower but ensures your script runs in the same environment as cloud training.
{{% /alert %}}

If you prefer a quick check without Docker, you can run your script directly:

```sh {class="command-line" data-prompt="$"}
python3 -m model.training --dataset_file=<path/to/dataset.jsonl> \
    --model_output_directory=<output-dir>
```

### Package and upload

```sh {class="command-line" data-prompt="$"}
tar -czvf my-training.tar.gz my-training/
viam training-script upload --path=my-training.tar.gz \
  --org-id=<org-id> --script-name=my-training-script
```

You can also specify `--framework`, `--type`, `--visibility`, and `--description` when uploading.
Scripts default to private (visible only within your organization). Set `--visibility=public` to share with other organizations through the [registry](https://app.viam.com/registry?type=Training+Script).
See the [CLI reference](/cli/overview/) for the full list of flags.

To find your organization ID, run `viam organization list`.

After uploading, your script appears in the [registry](https://app.viam.com/registry?type=Training+Script).

## Submit a training job

Once a training script is in the registry, whether you uploaded it or are using someone else's, submit a training job to run it against a dataset.

Every custom training job runs inside a Viam-hosted container on GPU-backed
cloud infrastructure. Containers are based on Python 3.10 with TensorFlow
pre-installed. The currently supported versions are `tf:2.16` and `tf:2.17`.
To use a different framework (PyTorch, scikit-learn, or anything installable
with pip), add it to the `install_requires` list in `setup.py`; Viam
installs the packages in the container before running your script.

Custom training is part of the Viam platform; see [pricing](https://www.viam.com/product/pricing)
for plan details.

To list available containers with their framework versions and end-of-life
dates, run:

```sh {class="command-line" data-prompt="$"}
viam train containers list
```

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Go to your [**DATASETS**](https://app.viam.com/data/datasets) and select the dataset you want to train on.
2. Click **Train model**.
3. Select **Train on a custom training script** and follow the prompts.
4. Select a **Container version** that matches the framework your training script uses.
   The UI shows a warning if the selected container is approaching its end-of-life date.
5. Optionally, add custom arguments as key-value pairs in the **Arguments** section.

{{% /tab %}}
{{% tab name="CLI" %}}

Use [`viam train submit custom from-registry`](/cli/datasets-and-training/#train-with-a-custom-training-script):

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<dataset-id> \
  --org-id=<org-id> --model-name=my-model \
  --model-version=1 --version=1 \
  --script-name=<namespace>:<script-name> \
  --container-version=<container-version> \
  --args=num_epochs=100,labels="'label1 label2'"
```

You can get the dataset ID from the [**DATASETS** tab](https://app.viam.com/data/datasets) or by running [`viam dataset list`](/cli/datasets-and-training/#list-datasets).

{{% /tab %}}
{{% tab name="API" %}}

Use the [ML Training Client API](/reference/apis/ml-training-client/#submittrainingjob) to submit training jobs programmatically.

{{% /tab %}}
{{< /tabs >}}

## Monitor and debug

{{< tabs >}}
{{% tab name="Web UI" %}}

In the Viam app, go to the **DATA** page, click the [**MODELS** tab](https://app.viam.com/models), and expand **Active Training**.
Click a job ID to view its logs.

{{% /tab %}}
{{% tab name="CLI" %}}

List training jobs:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<org-id> --job-status=unspecified
```

View logs for a specific job:

```sh {class="command-line" data-prompt="$"}
viam train logs --job-id=<job-id>
```

{{% /tab %}}
{{< /tabs >}}

Training logs expire after 7 days.
You will receive an email when your training job completes.

If a job fails, check the logs first: the error message usually indicates the problem.
Note that training scripts may emit log lines at the error level and still succeed; check the final job status rather than individual log lines.
