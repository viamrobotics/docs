---
linkTitle: "Sequence dataset format"
title: "Sequence dataset format"
weight: 32
layout: "docs"
type: "docs"
description: "The Parquet files a sequence dataset exports to, and the arguments a training script receives."
capabilities: ["datasets", "sequences", "ml-training"]
diataxis: reference
date: "2026-09-29"
---

A sequence dataset exports as three [Parquet](https://parquet.apache.org/) files.
The `viam dataset export` command writes them to a zip, and a custom training job receives them as command-line arguments.
Both use the same schema.

## Export layout

Running [`viam dataset export`](/train/create-a-dataset/#export-a-sequence-dataset) on a sequence dataset writes:

```text
<destination>/
  <dataset-id>.zip
    binary_data.parquet
    tabular_data.parquet
    sequences.parquet
  binary_data/
    <binary-data-id><extension>
```

In an exported `binary_data.parquet`, the `path` column is relative to the export directory.

## `binary_data.parquet`

One row per image in each sequence.

| Column            | Type                                                      | Description                                                                |
| ----------------- | --------------------------------------------------------- | -------------------------------------------------------------------------- |
| `sequence_id`     | string                                                    | ID of the sequence the image belongs to.                                   |
| `timestamp`       | timestamp (microseconds)                                  | When Viam received the image. This isn't the time the machine captured it. |
| `part_id`         | string                                                    | ID of the machine part that captured the image.                            |
| `component_name`  | string                                                    | Name of the resource that produced the image.                              |
| `method_name`     | string                                                    | Method that produced the image, for example `GetImages`.                   |
| `path`            | string                                                    | Location of the image file. See [Export layout](#export-layout).           |
| `classifications` | list of `{label, confidence}`                             | Classification annotations on the image.                                   |
| `bounding_boxes`  | list of `{label, confidence, x_min, y_min, x_max, y_max}` | Bounding box annotations, with coordinates normalized to the image size.   |

## `tabular_data.parquet`

One row per reading in each sequence.

| Column           | Type                     | Description                                                                  |
| ---------------- | ------------------------ | ---------------------------------------------------------------------------- |
| `sequence_id`    | string                   | ID of the sequence the reading belongs to.                                   |
| `timestamp`      | timestamp (microseconds) | When Viam received the reading. This isn't the time the machine captured it. |
| `part_id`        | string                   | ID of the machine part that captured the reading.                            |
| `component_name` | string                   | Name of the resource that produced the reading.                              |
| `method_name`    | string                   | Method that produced the reading, for example `Readings`.                    |
| `payload`        | string                   | The reading, as a JSON string.                                               |

## `sequences.parquet`

One row per sequence.

| Column        | Type                     | Description                          |
| ------------- | ------------------------ | ------------------------------------ |
| `sequence_id` | string                   | ID of the sequence.                  |
| `tags`        | list of string           | The sequence's tags.                 |
| `start_at`    | timestamp (microseconds) | Start of the sequence's time window. |
| `end_at`      | timestamp (microseconds) | End of the sequence's time window.   |

The API and SDKs call these fields `start_time` and `end_time`.

## Join the files

Join `binary_data.parquet` and `tabular_data.parquet` to `sequences.parquet` on `sequence_id`.

The export doesn't resample or align the data.
Each resource keeps its own sample rate, so a script that needs images and readings at the same moments has to match them itself, for example by nearest timestamp.

## Training script arguments

A custom training job on a sequence dataset passes your script the path to each Parquet file:

| Argument                   | Description                                     |
| -------------------------- | ----------------------------------------------- |
| `--binary_data_file`       | Path to `binary_data.parquet`.                  |
| `--tabular_data_file`      | Path to `tabular_data.parquet`.                 |
| `--sequences_file`         | Path to `sequences.parquet`.                    |
| `--model_output_directory` | Where to write the trained model. Viam sets it. |

A job on a sequence dataset doesn't get `--dataset_file`, which binary datasets use.
A job on a binary dataset gets only `--dataset_file`.
Your own arguments can't reuse `--dataset_file`, `--model_output_directory`, or the three sequence file names.

See [Custom training scripts](/train/custom-training-scripts/).
