---
linkTitle: "Run batch inference"
title: "Run batch inference on stored data"
weight: 50
layout: "docs"
type: "docs"
description: "Use the viam infer CLI command to run a deployed ML model against images already captured to the Viam Cloud. Useful for labeling assistance, dataset validation, and running large or GPU-only models."
date: "2026-04-14"
aliases:
  - /data-ai/ai/run-inference/
  - /vision/batch-inference/
---

Use `viam infer` to run a deployed ML model against an image that is already stored in the Viam Cloud. The model runs in Viam's cloud infrastructure, so this is the path to use when:

- The target machine cannot run the model locally (not enough compute, wrong architecture, or the model requires a GPU).
- You want to try a model against a large backlog of captured images without reconfiguring the machine.
- You are building a labeling-assistance pipeline: an existing model proposes initial labels on stored images, which a human then reviews.
- You need to validate a new model against historical production images before deploying it to live machines.

`viam infer` is a batch, one-image-at-a-time CLI command. For live inference on a camera feed, use a [vision service](/vision/configure/) on the machine instead.

## Prerequisites

- The [Viam CLI](/cli/) installed and authenticated (`viam login`).
- An image captured to the Viam Cloud with a known binary data ID.
- A deployed ML model in the Viam [registry](https://app.viam.com/registry) (yours or shared with you).
- Your organization ID and the model's organization ID.

## 1. Find the binary data ID

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.
2. Filter to the image you want to run inference on.
3. Click the image to open its side panel.
4. Copy the binary data ID from the panel header.

## 2. Find the model information

1. Navigate to the [**MODELS** tab](https://app.viam.com/models).
2. Find the model you want to run.
3. Note:
   - The model name.
   - The organization ID that owns the model.
   - The specific version you want to use (dropdown or timestamp).

## 3. Find your organization ID

Run:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

Copy the organization ID for the organization that should run the inference (this can be a different organization from the model's owner).

## 4. Run the command

```sh {class="command-line" data-prompt="$"}
viam infer \
  --binary-data-id <binary-data-id> \
  --model-name <model-name> \
  --model-org-id <org-that-owns-model> \
  --model-version <version> \
  --org-id <org-that-runs-inference>
```

### Flag reference

| Flag               | Required | Description                                                                                                                          |
| ------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `--binary-data-id` | Yes      | ID of the image to run the model against. From the **DATA** tab.                                                                     |
| `--model-name`     | Yes      | Model name as it appears in the **MODELS** tab.                                                                                      |
| `--model-org-id`   | Yes      | ID of the organization that owns the model.                                                                                          |
| `--model-version`  | Yes      | Specific model version to use, typically a timestamp like `2025-04-14T16-38-25`. Does not accept `latest`.                           |
| `--org-id`         | Yes      | ID of the organization that runs the inference. This can be a different organization from the model's owner; both must be specified. |

### Example output

```text
Inference Response:
Output Tensors:
  Tensor Name: num_detections
    Shape: [1]
    Values: [...]
  Tensor Name: classes
    Shape: [32 1]
    Values: [...]
  Tensor Name: boxes
    Shape: [32 1 4]
    Values: [...]
  Tensor Name: confidence
    Shape: [32 1]
    Values: [...]
Annotations:
Bounding Box Format: [x_min, y_min, x_max, y_max]
  Bounding Box ID: 0, Label: person
    Coordinates: [0.071400, 0.203500, 0.938500, 0.855100]
    Confidence: 0.9765
```

Output tensors are model-specific. The tensor names, shapes, and values shown above come from a typical TFLite object detector (fields: `classes`, `boxes`, `confidence`, `num_detections`). Your model's output shape will differ if it uses different tensor names. The `Annotations` block appears only when the model has bounding-box or classification metadata registered with the registry item; models without annotations skip the block entirely.

Bounding box coordinates are returned as proportions between `0` and `1`, with `(0, 0)` in the top-left and `(1, 1)` in the bottom-right. Multiply by the image width and height to get pixel coordinates.

## Script the command for many images

`viam infer` runs against one image per invocation. To run against many images, script the CLI call in a loop.

### Bash example

```bash
#!/usr/bin/env bash
# Run a model against every image matching a filter, print detections to JSONL.
set -euo pipefail

MODEL_NAME="person-detector"
MODEL_ORG="abcdef12-0000-0000-0000-000000000000"
MODEL_VERSION="2025-04-14T16-38-25"
ORG_ID="ghijkl34-0000-0000-0000-000000000000"

# Get binary data IDs for all images captured in a time range.
viam data export --mime-types image/jpeg \
  --start 2025-04-01T00:00:00Z --end 2025-04-07T23:59:59Z \
  --output-format ids > ids.txt

while read -r BIN_ID; do
  echo "=== $BIN_ID ==="
  viam infer \
    --binary-data-id "$BIN_ID" \
    --model-name "$MODEL_NAME" \
    --model-org-id "$MODEL_ORG" \
    --model-version "$MODEL_VERSION" \
    --org-id "$ORG_ID"
done < ids.txt
```

Run time is a few seconds per image plus cold-start time on the first call. Larger models take longer.

## Rate limits and cost

Cloud inference consumes Viam cloud compute. Check your organization's billing page before starting a large batch. For backlogs above a few thousand images, consider:

- Filtering the images to the subset that actually needs inference.
- Sampling rather than running every image.
- Running inference on-machine instead, if the machines are powerful enough.

## When not to use viam infer

- **Live camera feeds:** use a [vision service](/vision/configure/) on the machine. `viam infer` is not for real-time inference.
- **Raw tensor outputs for non-vision uses:** use the [ML model service API](/reference/apis/services/ml/) directly; `viam infer` is a CLI wrapper, not a general tensor API.
- **Modifying or retraining the model:** this command only runs inference. Training happens in the [train section](/train/).

## Next steps

- [Annotate images](/train/annotate-images/): use batch inference results to pre-label a dataset, then correct labels in the UI
- [Deploy an ML model](/vision/deploy-and-maintain/deploy-from-registry/): get a model onto a machine for live inference
- [viam CLI reference](/cli/): every `viam` subcommand
