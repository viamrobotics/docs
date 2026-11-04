---
title: "Phase 5: Train an ACT policy"
linkTitle: "5. Train a policy"
type: "docs"
slug: "train-a-policy"
weight: 50
description: "Submit a custom training job that trains an ACT policy on your sequence dataset, then check the loss curve."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 5
phase_total: 7
time_estimate: "20 minutes plus a 60 to 90 minute training job"
prev: "/tutorials/xarm-act-stacking/review-and-build-a-dataset/"
next: "/tutorials/xarm-act-stacking/deploy-the-policy/"
languages: ["python"]
capabilities: ["ml-training", "sequences", "docs"]
diataxis: tutorial
draft: true
---

You have a sequence dataset of reviewed demonstrations. Now you train an ACT (Action Chunking with Transformers) policy on it. You submit one custom training job, wait for it to finish, and check that the model learned something. This is the first milestone: a trained `xarm-stacking` model in your registry.

## What the training script does

You don't write the training script. It's published to the Viam registry, and the job runs it against your dataset. For each job, the script:

1. Copies the images from your organization's data storage to local disk.
2. Joins the gripper reading to the arm reading by nearest timestamp. It scales the gripper value so that 0 is open and 1 is closed.
3. Checks that the capture rate is the same in every sequence.
4. Converts the dataset to a LeRobot dataset.
5. Trains the ACT policy with `lerobot-train`.
6. Writes the checkpoint, plus `viam_training.json` and `loss_curve.json`.

For how custom training works in general, see [Custom training scripts](/train/custom-training-scripts/).

## Submit the job in the Viam app

1. Go to your [**DATASETS**](https://app.viam.com/data/datasets) and select `xarm-stacking-v1`.
2. Click **Train model**.
3. Select **Train on a custom training script** and follow the prompts. Name the model `xarm-stacking` when asked.
4. Choose `act-xarm` as the training script. In the **Container version** dropdown, choose **LeRobot SmolVLA for SO-101 (0.1: NVIDIA driver env)**. The container is named for SmolVLA, but it has the LeRobot version that both the ACT script and the `viam-labs:vla` module use.

   <!-- TODO(dep): the act-xarm script's public registry namespace, once it's published -->

5. Leave the **Arguments** section empty, unless your setup differs from this workshop's. The script's defaults match the component names and gripper values used here. To change a setting, add its key and value, and Viam passes it to the script as a command-line argument:

   | Argument           | Default               | What it sets                                                                                |
   | ------------------ | --------------------- | ------------------------------------------------------------------------------------------- |
   | `arm`              | `xarm`                | The arm component                                                                           |
   | `gripper`          | `xarm-gripper`        | The gripper component                                                                       |
   | `gripper_read_key` | `pos`                 | The key to read from the gripper's `DoCommand` response                                     |
   | `gripper_open`     | `840`                 | The gripper reading when fully open                                                         |
   | `gripper_closed`   | `2`                   | The gripper reading when fully closed                                                       |
   | `cameras`          | `scene-cam+wrist-cam` | The camera components, separated by `+`. The first one sets the frame clock                 |
   | `steps`            | `50000`               | The number of training steps                                                                |
   | `image_size`       | `0`                   | Downscales images so the longest side is this many pixels. `0` keeps each camera's own size |

   <!-- TODO(dep): xArm gripper open/closed native values (about 840 open, 2 closed) are unverified; confirm on hardware -->

   If your gripper reports different values, set `gripper_open` and `gripper_closed` to what it reports. Read them from a gripper `DoCommand` response while the gripper is open and closed.

## Submit the job with the CLI

You need the dataset ID from Phase 4, your organization ID, and the container ID. List the containers to find the ID of **LeRobot SmolVLA for SO-101 (0.1: NVIDIA driver env)**:

```sh {class="command-line" data-prompt="$"}
viam train containers list --org-id=<org-id>
```

Then submit the job. This needs CLI version 1.12.0 or later.

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<dataset-id> \
  --org-id=<org-id> --model-name=xarm-stacking \
  --model-version=1 --version=<script-version> \
  --script-name=<namespace>:act-xarm \
  --container-id=<container-id>
```

A few things to know:

- `--version` is the version of the training script, not of the model.
- Every `--model-version` must be new. To retrain, increase it.
- The defaults match this workshop, so the command passes no `--args`. To change a setting, add `--args` with `key=value` pairs, as in `--args=steps=30000,gripper_open=850`.
- Viam splits `--args` on commas, so separate the cameras in `cameras` with `+`, as in `cameras=scene-cam+wrist-cam`. Don't add quotes. They reach the script as part of the camera name.
- The first camera in `cameras` sets the frame clock. Keep `scene-cam` first.

## Watch it run

Copy the job ID from the command's output, or find it in the app. In the Viam app, go to the **DATA** page, click the [**MODELS** tab](https://app.viam.com/models), and expand **Active Training**. Click a job ID to view its logs.

From the CLI, stream the logs:

```sh {class="command-line" data-prompt="$"}
viam train logs --job-id=<job-id>
```

Two kinds of line matter:

- **Heartbeat.** The script logs a heartbeat line every minute that says which stage is running. If the log goes quiet for several minutes, the job has stalled.
- **Capture-rate warning.** A sequence whose capture rate is more than 2 percent off the median is left out, usually because a camera dropped frames. The warning names the episodes it skipped, and `viam_training.json` lists them. If more than 10 percent of sequences are off, the job stops.

For more on job status and logs, see [Monitor and debug](/train/custom-training-scripts/#monitor-and-debug).

## Go to lunch

The job takes about 60 to 90 minutes. With the default 50,000 steps, training takes about 70 minutes on an NVIDIA A100, after a few minutes of copying and converting the data. You don't need to watch it. Viam emails you when it succeeds or fails. While you wait, read [Phase 6](/tutorials/xarm-act-stacking/deploy-the-policy/) to see how you deploy the model.

## Read the loss curve

When the job finishes, export the model version's files:

```sh {class="command-line" data-prompt="$"}
viam packages export --type=ml_model --org-id=<org-id> --name=xarm-stacking --version=<model-version> --destination=.
```

Open `loss_curve.json` from the exported files. It holds the training loss at every logged step.

- A curve that falls and then flattens is healthy. The policy learned what it could from the data.
- A curve that's flat from the start means a data problem. Check that the dataset holds enough sequences, and check that the gripper value varies across an episode.

{{< checkpoint >}}
The job shows **Completed**, and your registry has a new `xarm-stacking` model version.
{{< /checkpoint >}}

## If the job fails

The script checks its inputs and stops with a clear message. The common failures:

- **No images from the clock camera.** A name in `cameras` doesn't match any camera in the dataset. The message lists the components the dataset has. Fix the `cameras` argument and submit again with a new `--model-version`.
- **No `DoCommand` rows for the gripper.** The dataset has no gripper readings. Go back to Phase 3 and add the gripper's capture config, then record again.
- **Inconsistent capture rate.** More than 10 percent of sequences are off the median rate. Check that every episode was captured at 10 Hz, discard the outliers in [Phase 4](/tutorials/xarm-act-stacking/review-and-build-a-dataset/), and submit again with a new `--model-version`.
- **No usable GPU.** The job stopped because PyTorch can't use a GPU. Check that you chose the GPU training container. If it repeats after you resubmit, check the container choice and the logs.

{{< workshop-nav >}}
