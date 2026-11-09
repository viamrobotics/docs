---
linkTitle: "Dataset formats"
title: "Training dataset formats"
weight: 45
layout: "docs"
type: "docs"
description: "The files a custom training script receives for a binary or sequence dataset, the arguments that point to them, and the environment a training job runs in."
capabilities: ["datasets", "sequences", "ml-training"]
diataxis: reference
date: "2026-09-29"
updated: "2026-11-03"
aliases:
  - /train/sequence-dataset-format/
---

A [custom training script](/train/custom-training-scripts/) receives its dataset as files on disk.
What those files are depends on the [dataset type](/train/create-a-dataset/#choose-a-dataset-type): a binary dataset arrives as one JSONLines file plus the files it lists, and a sequence dataset arrives as three [Parquet](https://parquet.apache.org/) files plus the images.
[`viam dataset export`](/train/create-a-dataset/#export-a-dataset) writes the same formats, so you can test a script on an export before you run it in the cloud.

## Training script arguments {#training-script-arguments}

A custom training job runs your script as `python3 -m model.training` with these arguments:

| Argument                   | Dataset type | Description                                                                         |
| -------------------------- | ------------ | ----------------------------------------------------------------------------------- |
| `--model_output_directory` | Both         | Directory to write the trained model to. See [Output directory](#output-directory). |
| `--dataset_file`           | Binary       | Path to the [JSONLines file](#jsonlines-file).                                      |
| `--binary_data_file`       | Sequence     | Path to [`binary_data.parquet`](#binary-data-parquet).                              |
| `--tabular_data_file`      | Sequence     | Path to [`tabular_data.parquet`](#tabular-data-parquet).                            |
| `--sequences_file`         | Sequence     | Path to [`sequences.parquet`](#sequences-parquet).                                  |

A job on a binary dataset gets `--dataset_file` and none of the three Parquet file arguments.
A job on a sequence dataset gets the three Parquet file arguments and no `--dataset_file`.

You can add your own arguments, such as `--num_epochs`, and pass values for them when you submit the job.
Viam passes each key and value as `--<key>=<value>`.
Your own arguments can't reuse the names in the table above.

## Binary datasets {#binary-datasets}

### Export layout {#binary-export-layout}

Running `viam dataset export` on a binary dataset writes:

```text
<destination>/
  dataset.jsonl
  data/
    <file>
```

To write only `dataset.jsonl`, without the files, add `--only-jsonl`.

### JSONLines file {#jsonlines-file}

Each line of the file is a JSON object describing one file in the dataset:

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

| Field                        | Description                                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_path`                 | Location of the file.                                                                                                                           |
| `classification_annotations` | The file's labels, each as an `annotation_label`. Read these to train a classifier.                                                             |
| `bounding_box_annotations`   | The file's bounding boxes, with coordinates normalized to the range 0.0 to 1.0 of the image's width and height. Read these to train a detector. |

An exported file's lines also carry metadata about each file, such as `timestamp`, `binary_data_id`, `part_id`, and `component_name`.

In an export, `image_path` starts with the `--destination` you passed to `viam dataset export`.
If that was a relative path, it's relative to the directory you ran the command from.

For parsing functions that handle both annotation types, see the [classification-tflite example script](https://github.com/viam-modules/classification-tflite).

## Sequence datasets {#sequence-datasets}

### Export layout {#export-layout}

Running `viam dataset export` on a sequence dataset writes:

```text
<destination>/
  <dataset-id>.zip
    binary_data.parquet
    tabular_data.parquet
    sequences.parquet
  binary_data/
    <binary-data-id><extension>
```

Binary data IDs contain slashes, so the image files sit in nested folders under `binary_data/`.
To download only the zip, without the images, add `--only-parquet`.

In an exported `binary_data.parquet`, the `path` column is relative to the export directory.
In a training job, `path` is an absolute path, starting with `/gcs/`, that your script can open directly.
To produce an export you can inspect, follow the [sequences tutorial](/data/sequences-tutorial/).

### `binary_data.parquet` {#binary-data-parquet}

One row per image in each sequence.

| Column            | Type                                                      | Description                                                              |
| ----------------- | --------------------------------------------------------- | ------------------------------------------------------------------------ |
| `sequence_id`     | string                                                    | ID of the sequence the image belongs to.                                 |
| `timestamp`       | timestamp (microseconds)                                  | When the machine captured the image.                                     |
| `part_id`         | string                                                    | ID of the machine part that captured the image.                          |
| `component_name`  | string                                                    | Name of the resource that produced the image.                            |
| `method_name`     | string                                                    | Method that produced the image, for example `GetImages`.                 |
| `path`            | string                                                    | Location of the image file. See [Export layout](#export-layout).         |
| `classifications` | list of `{label, confidence}`                             | Classification annotations on the image.                                 |
| `bounding_boxes`  | list of `{label, confidence, x_min, y_min, x_max, y_max}` | Bounding box annotations, with coordinates normalized to the image size. |

### `tabular_data.parquet` {#tabular-data-parquet}

One row per reading in each sequence.

| Column           | Type                     | Description                                                                                                        |
| ---------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `sequence_id`    | string                   | ID of the sequence the reading belongs to.                                                                         |
| `timestamp`      | timestamp (microseconds) | When the machine captured the reading.                                                                             |
| `part_id`        | string                   | ID of the machine part that captured the reading.                                                                  |
| `component_name` | string                   | Name of the resource that produced the reading.                                                                    |
| `method_name`    | string                   | Method that produced the reading, for example `Readings`.                                                          |
| `payload`        | string                   | The method's response, as a JSON string. For a sensor's `Readings`, for example: `{"readings":{"a":1.0,"b":2.0}}`. |

### `sequences.parquet` {#sequences-parquet}

One row per sequence.

| Column        | Type                     | Description                          |
| ------------- | ------------------------ | ------------------------------------ |
| `sequence_id` | string                   | ID of the sequence.                  |
| `tags`        | list of string           | The sequence's tags.                 |
| `start_at`    | timestamp (microseconds) | Start of the sequence's time window. |
| `end_at`      | timestamp (microseconds) | End of the sequence's time window.   |

The API and SDKs call these fields `start_time` and `end_time`.

### Join the files {#join-the-files}

Join `binary_data.parquet` and `tabular_data.parquet` to `sequences.parquet` on `sequence_id`.

The export doesn't resample or align the data.
Each resource keeps its own sample rate, so a script that needs images and readings at the same moments has to match them itself, for example by nearest timestamp.
All timestamps are in UTC, and libraries such as pandas load them as timezone-aware UTC values.

## Training job environment {#training-job-environment}

### Output directory {#output-directory}

When the job finishes, Viam packages every file in `--model_output_directory` and publishes it to your organization's registry as a new model version.
Files in a `tmp/` subdirectory are left out, so use it for checkpoints and other intermediate files.

The job fails if your script exits with a non-zero status or writes no files to the output directory.

### Viam API credentials {#viam-api-credentials}

The job sets the `API_KEY` and `API_KEY_ID` environment variables, so your script can call [Viam APIs](/reference/apis/) during training, for example to query more data:

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

See [Train a model with a custom training script](/train/custom-training-scripts/).
