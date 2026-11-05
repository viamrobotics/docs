---
linkTitle: "Custom training"
title: "Train a model with a custom training script"
tags: ["data management", "ml", "model training"]
weight: 25
layout: "docs"
type: "docs"
languages: ["python"]
viamresources: ["mlmodel", "data_manager"]
platformarea: ["ml"]
description: "Find or write a training script, test it locally, upload it to the registry, and run it on a dataset to train an ML model."
capabilities: ["ml-training"]
diataxis: how-to
date: "2024-12-04"
updated: "2026-11-03"
---

A custom training script is Python code that Viam runs in a cloud container to train a model on one of your datasets.
Use one when [built-in training](/train/train-a-model/) can't train the model you need: for example, a robot policy, a model trained on a [sequence dataset](/train/create-a-dataset/#choose-a-dataset-type), a PyTorch or ONNX model, or an image model where you control the architecture, preprocessing, or hyperparameters.
To compare the two, see [Built-in or custom training](/train/overview/#training-method).

To train with a custom script:

1. [Find an existing training script](#find-an-existing-training-script). If one fits, skip to step 6.
2. [Plan your script](#plan-your-script): the dataset it reads, the model it produces, and the container it runs in.
3. [Write the script](#write-the-script).
4. [Test it locally](#test-locally).
5. [Package and upload it](#package-and-upload) to the registry.
6. [Submit a training job](#submit-a-training-job).
7. [Monitor and debug](#monitor-and-debug) the job.

## Find an existing training script

Before writing your own, check whether a training script in the registry already does what you need.
The registry also has [pre-trained models](https://app.viam.com/registry?type=ML+Model) you can deploy without training.

1. Open the [registry, filtered to training scripts](https://app.viam.com/registry?type=Training+Script).
   You can also filter by owner, to see scripts from Viam, the community, or your own organization.
2. Search by keyword, such as the task (`classification`, `detection`, `policy`) or the framework (`pytorch`, `onnx`).
3. Open a script and read its description to check:
   - the task type and framework of the model it produces
   - whether it trains on a binary or a sequence dataset, and what labels it expects
   - which arguments it accepts, such as the number of epochs

If a script fits, note its name in `<namespace>:<script-name>` form and skip ahead to [Submit a training job](#submit-a-training-job).
To list training scripts from code, call [`list_registry_items`](/reference/apis/fleet/#listregistryitems) with the `PACKAGE_TYPE_ML_TRAINING` type.

## Plan your script

Make three decisions before you write code.
Each one shapes the script, and you need all three to test and upload it.

### Which dataset type it reads

A script reads either a binary dataset or a sequence dataset, and Viam passes it different files for each:

- **Binary dataset:** a JSONLines file listing each file and its labels or bounding boxes, plus the files themselves.
  Use it for models that learn from individual images.
- **Sequence dataset:** three Parquet files holding images and sensor readings grouped into time-windowed sequences, plus the images.
  Use it for models that learn from what happened over time, such as robot policies.
  Built-in training can't read a sequence dataset.

For the file formats and the arguments that point to them, see [Training dataset formats](/train/dataset-formats/).

### What model it produces {#match-your-output-to-an-ml-model-service}

A script declares a task type and a framework when you upload it, and every model it trains has the same ones:

- The **task type** says what the model does: single label classification, multi label classification, object detection, robot policy, or **Other**.
  See [Types of models](/train/overview/#types-of-models).
- The **framework** says what format the model's files are in, which decides what runs the model on your machine: an ML model service for TFLite, TensorFlow, PyTorch, or ONNX, or a module for **Registry**.
  Before you write the script, check that something for your framework runs on your machines' hardware.
  See [What runs the model](/train/deploy-a-model/#what-runs-the-model).

Your script must write the files that the service or module loads.
For example, the `tflite_cpu` ML model service loads a `model.tflite` file and a `labels.txt` file listing each label on its own line, which is what the [classification-tflite example](https://github.com/viam-modules/classification-tflite) writes.
For other frameworks, the module's README lists the files and tensor shapes it expects: for example, [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu), [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu), or [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu).
For a **Registry** model, the README of the module that runs it lists the files.

### Which container it runs in {#choose-a-container}

Every custom training job runs in a container on GPU-backed cloud infrastructure, and you pick the container when you test and when you submit:

- **A Viam-managed container:** Python 3.10 with TensorFlow pre-installed, in versions `tf:2.16`, `tf:2.17`, and `tf:2.21`.
  Viam installs any other packages your script lists in `setup.py`, such as PyTorch or scikit-learn, before it runs the script.
- **A [custom training container](/train/custom-containers/)** your organization registered, with your dependencies built in.
  Use one when your dependencies take a long time to install, so each job starts training right away, or when you need a different Python version or system libraries.

To list the containers available to your organization, with their IDs, framework versions, and end-of-life dates, run:

```sh {class="command-line" data-prompt="$"}
viam train containers list --org-id=<org-id>
```

Note the ID of the container you choose.

## Write the script

A training script is a Python package.
Viam installs it in the container and runs it as `python3 -m model.training`, so it needs this layout:

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
        # "torch",
        # "pandas",
    ],
)
```

`training.py` parses its arguments, reads the dataset, trains a model, and writes the model to `--model_output_directory`.
The arguments that point to the dataset depend on its type:

{{< tabs >}}
{{% tab name="Binary dataset" %}}

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
    # Add your own arguments as needed:
    parser.add_argument("--num_epochs", dest="num_epochs",
                        type=int, default=200)
    return parser.parse_args()


def load_dataset(data_json):
    """Read one JSON object per line of the dataset file."""
    with open(data_json, "r") as f:
        return [json.loads(line) for line in f]


if __name__ == "__main__":
    args = parse_args()
    entries = load_dataset(args.data_json)

    # --- Your training logic goes here ---
    # Each entry has an image_path and its classification_annotations
    # or bounding_box_annotations.
    model = ...
    labels = ...

    # Write the files that what runs the model loads.
    # For example, tflite_cpu loads model.tflite and labels.txt.
    with open(os.path.join(args.model_dir, "model.tflite"), "wb") as f:
        f.write(model)
    with open(os.path.join(args.model_dir, "labels.txt"), "w") as f:
        f.write("\n".join(labels))
```

{{% /tab %}}
{{% tab name="Sequence dataset" %}}

```python {class="line-numbers linkable-line-numbers"}
import argparse
import os

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary_data_file", type=str, required=True)
    parser.add_argument("--tabular_data_file", type=str, required=True)
    parser.add_argument("--sequences_file", type=str, required=True)
    parser.add_argument("--model_output_directory", dest="model_dir",
                        type=str, required=True)
    # Add your own arguments as needed:
    parser.add_argument("--num_epochs", dest="num_epochs",
                        type=int, default=200)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    images = pd.read_parquet(args.binary_data_file)
    readings = pd.read_parquet(args.tabular_data_file)
    sequences = pd.read_parquet(args.sequences_file)

    # In an export, image paths are relative to the export directory.
    # In a training job, they're absolute. Resolve them so the script
    # runs in both places.
    export_dir = os.path.dirname(os.path.abspath(args.binary_data_file))
    images["path"] = images["path"].apply(
        lambda p: p if os.path.isabs(p) else os.path.join(export_dir, p))

    # --- Your training logic goes here ---
    # Join images and readings to sequences on sequence_id, and use each
    # sequence's tags to select the examples to train on.
    model = ...

    # Write the files that what runs the model loads.
    ...
```

Add `pandas` and `pyarrow` to `install_requires` in `setup.py`.
If you unzip the export somewhere other than the export directory, resolve the paths against the export directory instead.

{{% /tab %}}
{{< /tabs >}}

As you write the script:

- **Accept only the arguments you need.** Viam passes each argument you set at submit time as `--<key>=<value>`, so your parser must accept every one you plan to pass.
  For the full list of arguments Viam passes, see [Training script arguments](/train/dataset-formats/#training-script-arguments).
- **Write only the model to the output directory.** Viam publishes everything in it except a `tmp/` subdirectory, which you can use for checkpoints and other intermediate files.
- **Exit with an error when training fails.** The job fails if the script exits with a non-zero status or writes nothing to the output directory.
- **Fall back to the CPU.** Cloud jobs run on a GPU, but local tests don't, so detect the GPU rather than assuming one.

If your script needs to call Viam APIs during training, for example to query more data, see [Viam API credentials](/train/dataset-formats/#viam-api-credentials).

For a complete working script, see the [classification-tflite example](https://github.com/viam-modules/classification-tflite), which trains a TFLite single label classification model with TensorFlow and Keras.

## Test locally

Run your script against an exported dataset before you submit a cloud job.
Testing locally is free, while a cloud job bills GPU time from the moment it starts.

### Export a dataset

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=<destination> --dataset-id=<dataset-id>
```

A binary dataset exports as a `dataset.jsonl` file plus the files it lists.
A sequence dataset exports as a zip of three Parquet files plus the images; unzip it before you test.
See [Export a dataset](/train/create-a-dataset/#export-a-dataset).

To keep tests fast, export a small dataset, or pass a low epoch count.

### Test locally with Docker

`viam training-script test-local` runs your script inside the container you chose, the same one the cloud job uses.
This catches problems that running the script directly misses: missing system dependencies, a different Python version, and package conflicts.
It runs without a GPU, so the script runs on the CPU: it checks that the script runs, not how well it trains.

`test-local` passes your script only `--dataset_file`, so it works only for a script that reads a binary dataset.
To test a script for a sequence dataset, [run it directly](#run-without-docker).

Run it from the directory you ran `viam dataset export` from:

```sh {class="command-line" data-prompt="$"}
viam training-script test-local \
  --training-script-directory=my-training/ \
  --dataset-root=. \
  --dataset-file=<destination>/dataset.jsonl \
  --container-id=<container-id> \
  --model-output-directory=<output-dir> \
  --custom-args=num_epochs=1
```

`--dataset-file` is relative to `--dataset-root`, and the container's working directory is the dataset root, so the image paths in `dataset.jsonl` resolve.
`--custom-args` takes your own arguments as `key=value` pairs, separated by commas.

When it finishes, check that `<output-dir>` holds the files your framework needs.

{{% alert title="Note" color="note" %}}
Training containers are built for linux/x86_64 (amd64).
On ARM systems, such as Apple Silicon Macs, Docker runs them through Rosetta 2 emulation, which is slower.
If the container fails to start, check that Docker Desktop has Rosetta emulation turned on.
{{% /alert %}}

### Run without Docker

To check the script quickly, or to test a script for a sequence dataset, run it directly with Python, from inside `my-training/`.
This doesn't use the training container, so install your dependencies locally first.

{{< tabs >}}
{{% tab name="Binary dataset" %}}

```sh {class="command-line" data-prompt="$"}
python3 -m model.training --dataset_file=<path/to/dataset.jsonl> \
    --model_output_directory=<output-dir> --num_epochs=1
```

{{% /tab %}}
{{% tab name="Sequence dataset" %}}

```sh {class="command-line" data-prompt="$"}
python3 -m model.training \
    --binary_data_file=<export-dir>/binary_data.parquet \
    --tabular_data_file=<export-dir>/tabular_data.parquet \
    --sequences_file=<export-dir>/sequences.parquet \
    --model_output_directory=<output-dir> --num_epochs=1
```

{{% /tab %}}
{{< /tabs >}}

## Package and upload

Package the script as a tarball and upload it to your organization's registry:

```sh {class="command-line" data-prompt="$"}
tar -czvf my-training.tar.gz my-training/
viam training-script upload --path=my-training.tar.gz \
  --org-id=<org-id> --script-name=my-training-script \
  --framework=<framework> --type=<task-type>
```

The flags declare [what model the script produces](#match-your-output-to-an-ml-model-service):

- `--framework` (required): `tflite`, `tensorflow`, `pytorch`, `onnx`, `registry`, or `unspecified`.
  With `registry`, also pass `--module-resource=<namespace:module:model>` for each module resource to deploy with the trained model.
- `--type`: `single_label_classification`, `multi_label_classification`, `object_detection`, `robot_policy`, or `unspecified`, which the Viam app shows as **Other**.
  `robot_policy` needs CLI version 1.15.0 or later.

Scripts are private to your organization by default.
To share one with other organizations through the [registry](https://app.viam.com/registry?type=Training+Script), add `--visibility=public` and a `--description`.
To find your organization ID, run `viam organization list`.
For every flag, see the [CLI reference](/cli/datasets-and-training/).

After uploading, your script appears in the [registry](https://app.viam.com/registry?type=Training+Script).

{{% alert title="Tip" color="tip" %}}
While you're iterating, `viam train submit custom with-upload` uploads the tarball and submits a training job in one command.
It takes the `upload` flags, except that the task type flag is `--model-type`, plus the job's flags, such as `--dataset-id` and `--container-id`, and it always uploads the script as private.
See [Train with a custom training script](/cli/datasets-and-training/#train-with-a-custom-training-script).
{{% /alert %}}

## Submit a training job

Once a training script is in the registry, whether you uploaded it or found it there, submit a job to run it on a dataset.
The dataset must be the type the script reads.

Custom training jobs run on premium GPUs and are billed at a higher rate than built-in training jobs.
See [pricing](https://www.viam.com/product/pricing).

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Go to your [**DATASETS**](https://app.viam.com/data/datasets) and select the dataset you want to train on.
2. Click **Train model**.
3. Select **Train on a custom training script** and follow the prompts.
4. In the **Container version** dropdown, select the [container you chose](#choose-a-container).
   The dropdown lists Viam-managed containers, marked **(Viam)**, followed by your organization's custom containers, marked **(Custom:** _image_**)**.
   The UI shows a warning if the selected Viam-managed container is approaching its end-of-life date.
5. Optionally, in the **Arguments** section, add arguments to pass to your script, such as the number of epochs.
   Viam passes each key and value as a command-line argument, so `num_epochs` and `20` become `--num_epochs=20`.

{{% /tab %}}
{{% tab name="CLI" %}}

Use [`viam train submit custom from-registry`](/cli/datasets-and-training/#train-with-a-custom-training-script):

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<dataset-id> \
  --org-id=<org-id> --model-name=my-model \
  --model-version=1 --version=1 \
  --script-name=<namespace>:<script-name> \
  --container-id=<container-id> \
  --args=num_epochs=100,labels="'label1 label2'"
```

`--version` is the version of the training script to run.
You can get the dataset ID from the [**DATASETS** tab](https://app.viam.com/data/datasets) or by running [`viam dataset list`](/cli/datasets-and-training/#list-datasets).

{{% /tab %}}
{{% tab name="API" %}}

Use [`submit_custom_training_job`](/reference/apis/ml-training-client/#submitcustomtrainingjob) to submit custom training jobs programmatically.
Pass the container ID as `container_id`.

{{% /tab %}}
{{< /tabs >}}

## Monitor and debug

{{< tabs >}}
{{% tab name="Web UI" %}}

In the Viam app, go to the **DATA** page, click the [**MODELS** tab](https://app.viam.com/models), and expand **Active Training**.
Click a job ID to view its logs.
The **Details** panel shows the container the job runs in, under **Container version** and **Container ID**.

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

When a training job succeeds or fails, Viam emails the user who submitted it.
Jobs submitted with an API key send no email, so check the job status with `viam train list` or `viam train get` instead.
Training logs expire after 7 days.

If a job fails, read the logs first: the error message usually names the problem.
A script can log lines at the error level and still succeed, so check the job's final status rather than individual log lines.

{{% expand "The job fails before training starts" %}}
A package in `install_requires` failed to install, or the script failed on an argument.
Check that the job's arguments match what your parser accepts, and that the dependencies install in the container you chose: run [`test-local`](#test-locally-with-docker) with the same container.
{{% /expand %}}

{{% expand "The job fails after training finishes" %}}
The script wrote nothing to `--model_output_directory`, or wrote only to its `tmp/` subdirectory.
Check the path your script writes to.
{{% /expand %}}

{{% expand "The job succeeds but the model won't load on the machine" %}}
The files your script wrote don't match what the ML model service or module expects, or the script was uploaded with the wrong `--framework`.
See [What model it produces](#match-your-output-to-an-ml-model-service).
{{% /expand %}}

## What's next

- [Deploy a model to a machine](/train/deploy-a-model/): add the trained model and the resource that runs it to your machine.
- [Custom training containers](/train/custom-containers/): build your script's dependencies into a container so jobs start training right away.
- [Training dataset formats](/train/dataset-formats/): every column and field your script can read.
