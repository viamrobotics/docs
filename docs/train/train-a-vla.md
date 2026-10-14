---
linkTitle: "Train a VLA"
title: "Train a vision-language-action (VLA) model"
weight: 33
layout: "docs"
type: "docs"
description: "Record robot demonstrations as sequences, fine-tune a vision-language-action (VLA) policy such as SmolVLA on a Viam cloud GPU, and run it on your machine."
capabilities: ["sequences", "datasets", "ml-training", "hw-arm"]
diataxis: how-to
languages: ["python"]
viamresources: ["arm", "camera", "data_manager", "generic"]
platformarea: ["ml", "data"]
tags: ["ml", "model training", "sequences", "vla", "imitation learning"]
date: "2026-10-13"
---

A vision-language-action (VLA) model is a robot policy.
It takes camera images, the robot's joint positions, and a natural-language instruction such as "open the box", and it outputs the next joint positions for the arm.
You train one by imitation learning: you record demonstrations of the task, then fine-tune a pretrained VLA on them.

This page fine-tunes [SmolVLA](https://huggingface.co/lerobot/smolvla_base), using Hugging Face's [LeRobot](https://huggingface.co/docs/lerobot) library, on demonstrations you record with Viam.
Viam handles every step around the model: capturing demonstrations, organizing them into a dataset, training on a cloud GPU, and running the trained policy on your machine.
The steps work with any arm that has a Viam module.

For an example, this video shows a robot that opens cardboard boxes with visual servoing and a VLA fine-tuned on demonstrations recorded with Viam:

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/zSAkvyvphqg">}}

## How the pieces fit

| Step                         | What you use                                                                                                                                                    | What it produces                                                 |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Record demonstrations        | [Data capture](/data/capture-sync/capture-and-sync-data/) and [sequences](/data/sequences/)                                                                     | One sequence per demonstration, tagged with its instruction      |
| Build a dataset              | [Sequence dataset](/train/create-a-dataset/)                                                                                                                    | Your demonstrations, as three Parquet files                      |
| Fine-tune                    | [Custom training script](/train/custom-training-scripts/) and the [`viam-sequence-to-lerobot`](https://github.com/viam-labs/viam-sequence-to-lerobot) converter | A SmolVLA checkpoint, published to your organization's registry  |
| Speed up training (optional) | [Custom training container](/train/custom-containers/)                                                                                                          | A registered container with LeRobot preinstalled                 |
| Run the policy               | The [`viam-labs:vla`](https://github.com/viam-labs/vla-inference-service) module                                                                                | A control loop that drives the arm from the policy's predictions |

## Prerequisites

- A machine with an [arm](/reference/components/arm/) and one or two [cameras](/reference/components/camera/), configured and working.
  A fixed camera that sees the workspace plus a wrist camera is a common setup.
- A way to teleoperate the arm while you record, such as a leader arm, a VR or gamepad controller, or moving the arm by hand.
- To run the trained policy, a computer with an NVIDIA GPU attached to the machine, such as an NVIDIA Jetson Orin.
- Optionally, [Docker](https://docs.docker.com/get-docker/) and a [Docker Hub](https://hub.docker.com/) account, to build a custom training container.
- The [Viam CLI](/cli/), logged in.

## 1. Plan what to capture

Each demonstration needs images and joint positions, captured at the same steady rate:

- **Images** from each camera's `GetImages` method. Sequences include only JPEG and PNG images.
- **Joint positions** from the arm's `JointPositions` method.
  If your gripper is one of the arm's joints, as on many low-cost arms, the gripper is included.
  For a separate gripper component, see the gripper options in the [`viam-labs:vla` README](https://github.com/viam-labs/vla-inference-service#gripper-variants).
- **One rate for everything**, which is also the rate the policy runs at.
  10 to 30 Hz is typical.

You don't need to capture actions separately.
The converter uses each frame's next joint positions as its action.

## 2. Record each demonstration as a sequence

Each demonstration becomes one [sequence](/data/sequences/), tagged with the instruction the policy should learn.
The `capture-control` module starts capture and opens a sequence when you send it a command.

1. [Add the `capture-control` sensor](/data/capture-sync/capture-on-demand/#add-the-sensor) to your machine, list the cameras' `GetImages` and the arm's `JointPositions`, and [point the data manager at the sensor](/data/capture-sync/capture-on-demand/#point-the-data-manager-at-the-sensor).
2. Before each demonstration, start capture with your chosen rate and a `cmd:` tag holding the instruction:

   ```json
   { "start_capture": true, "frequency_hz": 10, "tags": ["cmd:open the box"] }
   ```

3. Teleoperate the arm through the task.
4. Send `{"stop_capture": true}` to stop capture and close the sequence.

You can send these commands from the sensor's **TEST** section, or from your teleoperation code with `DoCommand`, so one button press starts and ends each demonstration.

Start with about 50 demonstrations, the number [LeRobot recommends for fine-tuning SmolVLA](https://huggingface.co/docs/lerobot/smolvla#collect-a-dataset).
Vary the objects' starting positions between demonstrations, and record several demonstrations of each variation.
If the policy struggles after training, record more.

The policy learns to imitate everything in your demonstrations, including mistakes.
Review the sequences on the **DATA** tab, and delete any sequence in which the task wasn't completed, or in which the arm fumbled, paused for a long time, or collided with something.
To train one policy on several related tasks, give each demonstration the `cmd:` tag for its own task.

## 3. Collect the demonstrations into a dataset

Add the sequences to a [sequence dataset](/train/create-a-dataset/).

LeRobot trains on its own dataset format, not on Viam's Parquet export.
The [`viam-sequence-to-lerobot`](https://github.com/viam-labs/viam-sequence-to-lerobot) converter turns each sequence into a LeRobot episode: it matches each camera frame with the nearest joint positions, uses the next frame's joint positions as the action, and takes the episode's instruction from the sequence's `cmd:` tag.
Your training script runs the converter in step 4.

{{< alert title="Caution" color="caution" >}}
`viam-sequence-to-lerobot` is an experimental tool from Viam Labs.
Its options and output may change between versions.
Check the [converter's README](https://github.com/viam-labs/viam-sequence-to-lerobot) for the current options.
{{< /alert >}}

Before you spend GPU time, export the dataset and run the converter on your own computer to check that every sequence converts:

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=my-export --dataset-id=<dataset-id>
pip install git+https://github.com/viam-labs/viam-sequence-to-lerobot
viam-seq-to-lerobot my-export --arm=<arm-name> --camera=<camera-1> --camera=<camera-2> --fps=10
```

The converter logs any sequence it skips, and why, for example a missing camera or too few frames.
The first `--camera` sets the frame clock, and `--fps` must match your capture rate.
Run `viam-seq-to-lerobot --help` for all options.

## 4. Write the training script

The training script converts the dataset into LeRobot's format, fine-tunes SmolVLA on it, and saves the checkpoint where Viam publishes it.
It runs in a Viam-managed container, which installs its dependencies from `setup.py` at the start of each job:

```python {class="line-numbers linkable-line-numbers"}
# setup.py
from setuptools import find_packages, setup

setup(
    name="vla-training",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "lerobot[smolvla]",
        "viam-sequence-to-lerobot @ git+https://github.com/viam-labs/viam-sequence-to-lerobot",
    ],
)
```

See [File structure](/train/custom-training-scripts/#file-structure) for where `setup.py` and `model/training.py` go.

```python {class="line-numbers linkable-line-numbers"}
# model/training.py
import argparse
import shutil
import subprocess
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary_data_file", required=True)
    parser.add_argument("--tabular_data_file", required=True)
    parser.add_argument("--sequences_file", required=True)
    parser.add_argument("--model_output_directory", required=True)
    parser.add_argument("--arm", required=True)
    parser.add_argument("--cameras", required=True,
                        help="Space-separated camera names")
    parser.add_argument("--fps", default="10")
    parser.add_argument("--steps", default="20000")
    parser.add_argument("--batch_size", default="32")
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.model_output_directory)
    # Viam doesn't publish files under tmp/.
    work_dir = output_dir / "tmp"

    # Lay the Parquet files out the way the converter reads an export.
    export_dir = work_dir / "export"
    export_dir.mkdir(parents=True)
    (export_dir / "binary_data.parquet").symlink_to(args.binary_data_file)
    (export_dir / "tabular_data.parquet").symlink_to(args.tabular_data_file)
    (export_dir / "sequences.parquet").symlink_to(args.sequences_file)

    # Convert each sequence into a LeRobot episode.
    dataset_dir = work_dir / "dataset"
    camera_flags = [f"--camera={name}" for name in args.cameras.split()]
    subprocess.run(
        ["viam-seq-to-lerobot", str(export_dir), f"--arm={args.arm}",
         *camera_flags, f"--fps={args.fps}", "--repo-id=local/demos",
         f"--output-root={dataset_dir}"],
        check=True,
    )

    # Fine-tune SmolVLA on the converted dataset.
    train_dir = work_dir / "train"
    subprocess.run(
        ["lerobot-train", "--policy.path=lerobot/smolvla_base",
         "--policy.input_features=null", "--policy.push_to_hub=false",
         "--policy.use_amp=true", "--dataset.repo_id=local/demos",
         f"--dataset.root={dataset_dir}", f"--output_dir={train_dir}",
         f"--steps={args.steps}", f"--batch_size={args.batch_size}"],
        check=True,
    )

    # Publish the final checkpoint.
    shutil.copytree(train_dir / "checkpoints" / "last" / "pretrained_model",
                    output_dir, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
```

`--policy.input_features=null` makes the checkpoint declare your own cameras instead of the three that `smolvla_base` declares.
The [converter's README](https://github.com/viam-labs/viam-sequence-to-lerobot#camera-keys) explains why this matters.

Package the script and upload it:

```sh {class="command-line" data-prompt="$"}
tar -czvf vla-training.tar.gz model/ setup.py
viam training-script upload --path=vla-training.tar.gz \
  --org-id=<org-id> --script-name=vla-training
```

## 5. (Optional) Build a custom training container

Viam-managed containers come with Python 3.10 and TensorFlow, so every job starts by installing PyTorch, LeRobot, and their dependencies with pip.
That install takes a long time, and you pay for it as GPU time.
The latest LeRobot releases also need Python 3.12, so a Viam-managed container installs the most recent LeRobot release that supports Python 3.10.

To skip the install and use the latest LeRobot, run your jobs in a [custom training container](/train/custom-containers/) with the dependencies already installed.
Hugging Face publishes a GPU image with LeRobot, [`huggingface/lerobot-gpu`](https://hub.docker.com/r/huggingface/lerobot-gpu).
Build on it to add `pip`, which Viam uses to install your training script, and the converter:

```dockerfile {class="line-numbers linkable-line-numbers"}
FROM huggingface/lerobot-gpu:latest

RUN uv pip install --python /lerobot/.venv/bin/python pip \
    "viam-sequence-to-lerobot @ git+https://github.com/viam-labs/viam-sequence-to-lerobot"
```

Build and push the image to a public Docker Hub repository, then register it:

```sh {class="command-line" data-prompt="$"}
docker buildx build --platform linux/amd64 \
  -t docker.io/<your-username>/lerobot-viam:1 --push .
viam train containers register \
  --uri=docker.io/<your-username>/lerobot-viam:1 \
  --description="LeRobot for VLA training" \
  --org-id=<org-id>
```

Save the container ID that registration prints.
To build reproducible images, pin the base image by digest instead of `latest`.
Your `setup.py` doesn't need to change: its dependencies are already installed in the container.
See [Custom training containers](/train/custom-containers/) for the image requirements.

## 6. Train on a Viam cloud GPU

Find the ID of the container to train in.
To use a Viam-managed container, pick the newest one from the list.
If you built a custom container in step 5, use the ID that registration printed.

```sh {class="command-line" data-prompt="$"}
viam train containers list --org-id=<org-id>
```

Submit a training job on your sequence dataset:

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<dataset-id> \
  --org-id=<org-id> --model-name=my-vla \
  --model-version=1 --version=1 \
  --script-name=<namespace>:vla-training \
  --container-id=<container-id> \
  --args=arm=<arm-name>,cameras="'<camera-1> <camera-2>'",fps=10
```

You can also submit a training job through the web UI: on the [**DATASETS**](https://app.viam.com/data/datasets) page, select your dataset, click **Train model**, select **Train on a custom training script**, select the container in the **Container version** dropdown, and add the `arm`, `cameras`, and `fps` arguments under **Arguments**.
See [Submit a training job](/train/custom-training-scripts/#submit-a-training-job).

Fine-tuning takes hours: LeRobot reports that 20,000 steps take about four hours on one A100 GPU.
Custom training jobs run on premium GPUs and are billed for that time. See [pricing](https://www.viam.com/product/pricing) for rates.
To follow the job's progress and read its logs while it runs, see [Monitor and debug](/train/custom-training-scripts/#monitor-and-debug).

When the job finishes, the checkpoint is published to your organization's registry as the `my-vla` model.

## 7. Run the policy on your machine

The [`viam-labs:vla`](https://github.com/viam-labs/vla-inference-service) module runs LeRobot policies on a Viam machine.

{{< alert title="Caution" color="caution" >}}
`viam-labs:vla` is an experimental module from Viam Labs.
Its configuration and behavior may change between releases.
Check the [module README](https://github.com/viam-labs/vla-inference-service) for the current configuration before you upgrade.
{{< /alert >}}

It provides two generic services:

- `viam-labs:vla:policy` loads the checkpoint and runs inference.
- `viam-labs:vla:controller` runs the control loop: it reads the cameras and the arm, asks the policy for actions, and moves the arm within safety limits you set.

1. Add the trained model to your machine's configuration as a package, and point the policy service at it:

   ```json
   {
     "packages": [
       {
         "name": "my-vla",
         "package": "<org-id>/my-vla",
         "version": "latest",
         "type": "ml_model"
       }
     ],
     "services": [
       {
         "name": "vla-policy",
         "api": "rdk:service:generic",
         "model": "viam-labs:vla:policy",
         "attributes": {
           "model_path": "${packages.ml_model.my-vla}"
         }
       }
     ]
   }
   ```

2. Add a `viam-labs:vla:controller` service that names the policy service, the arm, and a camera for each of the policy's image inputs.
   Send the policy service `{"command": "specs"}` to see which image inputs and state size it expects.
   See the [module README](https://github.com/viam-labs/vla-inference-service#controller) for the controller's attributes, including joint mapping, units, and safety limits.
3. Start the policy by sending the controller an instruction:

   ```json
   { "command": "start", "task": "open the box" }
   ```

   Send `{"command": "stop"}` to stop it.

## 8. Improve the policy

Keep data capture running while the policy runs, and record each run as a sequence.
Add successful runs, and runs you corrected by hand, to the dataset, then train a new model version.

## Learn more

- [Custom training containers](/train/custom-containers/): image requirements, registration, and managing containers.
- [Custom training scripts](/train/custom-training-scripts/): script structure, arguments, and job options.
- [Sequence dataset format](/train/sequence-dataset-format/): every column in the Parquet files.
- [Sequences tutorial](/data/sequences-tutorial/): record, review, and export sequences without hardware.
