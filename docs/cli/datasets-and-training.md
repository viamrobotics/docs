---
linkTitle: "Datasets and training"
title: "Datasets and training with the CLI"
weight: 30
layout: "docs"
type: "docs"
description: "Create datasets, manage training data, and submit ML training jobs from the command line."
capabilities: ["cli", "datasets", "ml-training"]
diataxis: how-to
---

Create and populate datasets, submit training jobs, manage training scripts, and run inference from the command line or in automation scripts.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

To find your organization ID:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

To list datasets and find dataset IDs:

```sh {class="command-line" data-prompt="$"}
viam dataset list --org-id=<org-id>
```

To list training containers and find container IDs, including your organization's custom containers:

```sh {class="command-line" data-prompt="$"}
viam train containers list --org-id=<org-id>
```

The `--org-id` flag is optional.
Without it, the command lists only Viam-managed containers.

## Manage datasets

### Create a dataset

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=my-dataset
```

The CLI prints the new dataset's name and ID:

```sh {class="command-line" data-prompt="$" data-output="1"}
Created dataset my-dataset with dataset ID: abcdef12-3456-7890-abcd-ef1234567890
```

Save the dataset ID for subsequent commands.

### List datasets

List all datasets in your organization:

```sh {class="command-line" data-prompt="$"}
viam dataset list --org-id=<org-id>
```

List specific datasets by ID:

```sh {class="command-line" data-prompt="$"}
viam dataset list --dataset-ids=abc,def
```

### Add images to a dataset

Adding images to a dataset creates references to the binary data items, it does not copy the data.
Removing images removes the references without deleting the underlying data.

Add images matching a filter (uses the same filter flags as [data export](/cli/manage-data/#export-images-and-binary-files)):

```sh {class="command-line" data-prompt="$"}
viam dataset data add filter \
  --dataset-id=<dataset-id> \
  --org-ids=<org-id> \
  --location-ids=<location-id> \
  --tags=defective \
  --start=2026-01-01T00:00:00Z \
  --end=2026-03-01T00:00:00Z
```

Add specific images by ID:

```sh {class="command-line" data-prompt="$"}
viam dataset data add ids \
  --dataset-id=<dataset-id> \
  --binary-data-ids=aaa,bbb,ccc
```

### Remove images from a dataset

By filter:

```sh {class="command-line" data-prompt="$"}
viam dataset data remove filter \
  --dataset-id=<dataset-id> \
  --tags=low-quality
```

By ID:

```sh {class="command-line" data-prompt="$"}
viam dataset data remove ids \
  --dataset-id=<dataset-id> \
  --binary-data-ids=aaa,bbb
```

### Export a dataset

Download all data from a dataset to a local directory.
The export includes the binary files plus a `dataset.jsonl` file with annotation metadata (classification labels, bounding boxes, timestamps, file paths) that Viam's training infrastructure consumes.

```sh {class="command-line" data-prompt="$"}
viam dataset export \
  --dataset-id=<dataset-id> \
  --destination=./my-dataset
```

To export only the metadata without downloading binary files (useful for inspecting annotations):

```sh {class="command-line" data-prompt="$"}
viam dataset export \
  --dataset-id=<dataset-id> \
  --destination=./my-dataset \
  --only-jsonl
```

For a sequence dataset, `export` starts an export job, waits for it, and writes `<dataset-id>.zip` (three Parquet files) plus a `binary_data/` folder of images to the destination.
Add `--only-parquet` to skip the images.
See [Export a sequence dataset](/train/create-a-dataset/#export-a-sequence-dataset).

### Merge datasets

Combine multiple datasets into a new one:

```sh {class="command-line" data-prompt="$"}
viam dataset merge \
  --name=combined-dataset \
  --dataset-ids=abc,def,ghi
```

### Rename and delete datasets

```sh {class="command-line" data-prompt="$"}
viam dataset rename --dataset-id=<dataset-id> --name=new-name
```

Deleting a dataset removes the dataset and its references, but does not delete the underlying binary data.

```sh {class="command-line" data-prompt="$"}
viam dataset delete --dataset-id=<dataset-id>
```

## Submit training jobs

### Train with a built-in model type

Submit a managed training job using one of Viam's built-in model types:

```sh {class="command-line" data-prompt="$"}
viam train submit managed \
  --dataset-id=<dataset-id> \
  --model-org-id=<org-id> \
  --model-name=my-detector \
  --model-type=single_label_classification \
  --model-framework=tflite \
  --model-labels=defective,good
```

On success, the CLI prints the job ID:

```sh {class="command-line" data-prompt="$" data-output="1"}
Submitted training job with ID abcdef12-3456-7890-abcd-ef1234567890
```

Model types: `single_label_classification`, `multi_label_classification`, `object_detection`.

### Train with a custom training script

Submit a job using a custom script from the registry:

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry \
  --dataset-id=<dataset-id> \
  --model-name=my-custom-model \
  --org-id=<org-id> \
  --script-name=<training-script-name> \
  --version=<script-version> \
  --container-id=<container-id>
```

`--version` is the version of the training script, not of the model. To set the model version, pass `--model-version`; it defaults to the current timestamp. To pass arguments to the training script, use `--args` with a comma-separated list of `key=value` pairs, for example `--args=num_epochs=3,model_type=multi_label`.

Submit a custom script by uploading it directly:

```sh {class="command-line" data-prompt="$"}
viam train submit custom with-upload \
  --dataset-id=<dataset-id> \
  --model-name=my-custom-model \
  --model-org-id=<org-id> \
  --script-name=my-training-script \
  --path=./my-training-script/ \
  --framework=tflite \
  --container-id=<container-id>
```

### Monitor training jobs

List training jobs in your organization:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<org-id>
```

Filter by status:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<org-id> --job-status=completed
```

Get details on a specific job (use the job ID from `train submit` or `train list`):

```sh {class="command-line" data-prompt="$"}
viam train get --job-id=<job-id>
```

View training logs:

```sh {class="command-line" data-prompt="$"}
viam train logs --job-id=<job-id>
```

Cancel a running job:

```sh {class="command-line" data-prompt="$"}
viam train cancel --job-id=<job-id>
```

## Manage training scripts

Upload a custom training script to the registry:

```sh {class="command-line" data-prompt="$"}
viam training-script upload \
  --path=./my-training-script/ \
  --script-name=my-training-script \
  --framework=tflite
```

Update script visibility:

```sh {class="command-line" data-prompt="$"}
viam training-script update \
  --script-name=my-training-script \
  --visibility=public
```

Test a training script locally before uploading (use `viam train containers list --org-id=<org-id>` to find container IDs).
Local testing runs in a Docker container that mirrors the cloud training environment.
The container validates that your script directory contains `setup.py` and `model/training.py`.

{{< alert title="Note" color="note" >}}
Training containers are linux/x86_64 only.
On ARM Macs, Docker runs them through Rosetta emulation, which may be slower.
{{< /alert >}}

```sh {class="command-line" data-prompt="$"}
viam training-script test-local \
  --dataset-root=./my-dataset/ \
  --training-script-directory=./my-training-script/ \
  --dataset-file=dataset.jsonl \
  --container-id=<container-id> \
  --model-output-directory=./output/
```

## Manage training containers

For requirements and how custom containers work, see [Custom training containers](/train/custom-containers/).
To list containers, see [Find your IDs](#find-your-ids).

Register an image:

```sh {class="command-line" data-prompt="$"}
viam train containers register \
  --uri=docker.io/<your-username>/<image>:<tag> \
  --description="My training environment" \
  --org-id=<org-id>
```

The CLI prints the new container's ID.
Pass that ID as `--container-id` when you submit a training job or test a script locally.

Delete a custom container:

```sh {class="command-line" data-prompt="$"}
viam train containers delete --id=<container-id>
```

## Run inference

Run inference on a single image using a trained model:

```sh {class="command-line" data-prompt="$"}
viam infer \
  --binary-data-id=<binary-data-id> \
  --model-org-id=<org-id> \
  --model-name=my-detector \
  --model-version=latest
```

To find binary data IDs, export data with `viam data export` or browse the DATA page in the Viam app.

## Related pages

- [Create a dataset](/train/create-a-dataset/) for step-by-step dataset creation with the Viam app
- [Train a model](/train/train-a-model/) for training with the Viam app
- [Custom training scripts](/train/custom-training-scripts/) for writing custom training logic
- [CLI reference](/cli/) for the complete `train` command reference
