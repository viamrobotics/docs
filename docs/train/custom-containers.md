---
linkTitle: "Custom training containers"
title: "Custom training containers"
tags: ["data management", "ml", "model training"]
weight: 31
layout: "docs"
type: "docs"
languages: ["python"]
platformarea: ["ml"]
description: "Register a Docker Hub image with Viam so custom training jobs run in an environment with your dependencies already installed."
capabilities: ["ml-training"]
diataxis: how-to
date: "2026-10-12"
updated: "2026-10-12"
---

A custom training container is a Docker Hub image that your organization registers with Viam.
When you start a [custom training job](/train/custom-training-scripts/), you can run it in your custom container instead of one of the Viam-managed containers.

Viam-managed containers come with Python and TensorFlow.
Any other dependency your training script lists in `setup.py` gets installed with pip at the start of every job, on billed GPU time.
For large dependency stacks, such as the libraries for fine-tuning a vision-language-action (VLA) model, that install can take a long time.
A custom container has those dependencies built in, so each job starts training right away.

The container holds only the environment.
Your training script stays in the registry and works without changes: the same `setup.py` and `model/training.py` structure runs in a custom container just as it does in a Viam-managed one.

## Requirements

Your image must:

- Be on Docker Hub (`docker.io`). Other registries aren't supported.
- Be **public**, so anyone can pull it without credentials.
- Be built for the `linux/amd64` platform.
- Have `bash`, `python3`, and `pip` on the `PATH`.

The image doesn't need any Viam-specific contents.
Viam starts each job with its own launcher command, so the image's `ENTRYPOINT` and `CMD` are ignored.
Environment variables you set with `ENV` still apply.

To register or delete a custom container, you must be an [organization owner](/organization/rbac/).

{{< alert title="Caution" color="caution" >}}
Your image is public, so anyone can pull it and read everything in it.
Don't put secrets, credentials, API keys, or proprietary code in the image.
Keep your training code in your training script, which stays private to your organization unless you make it public.
{{< /alert >}}

## Build and push an image

Start from an NVIDIA CUDA base image so your dependencies can use the GPU that training jobs run on.
Then install Python, pip, and the packages your training script needs.

For example, this `Dockerfile` installs PyTorch and Hugging Face Transformers:

```dockerfile {class="line-numbers linkable-line-numbers"}
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir torch transformers
```

Build the image for `linux/amd64` and push it to Docker Hub:

```sh {class="command-line" data-prompt="$"}
docker buildx build --platform linux/amd64 \
  -t docker.io/<your-username>/<image>:<tag> --push .
```

Make sure the repository is public on Docker Hub.

You can use any tool that produces a standard Docker image.
For example, [Cog](https://cog.run/) can generate a GPU-ready image from a short configuration file.

## Register the container

Registering a container tells Viam about your image and gives it a Viam container ID.
You give Viam the Docker image URI when you register.
After that, you use the **Viam container ID**, not the Docker image URI or a Docker image ID, everywhere you choose a container.

<!-- Registration isn't available in the Viam web UI yet. Add a Web UI tab here when it is. -->

{{< tabs >}}
{{% tab name="CLI" %}}

Run [`viam train containers register`](/cli/reference/#train-containers-register):

```sh {class="command-line" data-prompt="$"}
viam train containers register \
  --uri=docker.io/<your-username>/<image>:<tag> \
  --description="My training environment" \
  --org-id=<org-id>
```

The `--description` is the name the container appears under when you pick a container for a training job.
If you omit `--org-id`, the CLI uses the default organization you set with `viam defaults set-org`.

The CLI prints the container ID:

```sh {class="command-line" data-prompt="$" data-output="1"}
Container successfully registered. Container ID: <container-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`register_custom_training_container`](/reference/apis/ml-training-client/#registercustomtrainingcontainer), which returns the container ID:

```python {class="line-numbers linkable-line-numbers"}
container_id = await ml_training_client.register_custom_training_container(
    org_id="<org-id>",
    image_uri="docker.io/<your-username>/<image>:<tag>",
    description="My training environment",
)
print(container_id)
```

Set `description`: it's the name the container appears under when you pick a container for a training job.

{{% /tab %}}
{{< /tabs >}}

When you register a container, Viam checks that the image exists on Docker Hub, is public, and is built for `linux/amd64`.
If a check fails, registration fails with an error that names the problem, for example:

- `image URI must reference an image on Docker Hub`
- `image could not be found on Docker Hub; it must exist and be public`
- `image must be built for the linux/amd64 platform`

Viam doesn't check that your image has Python, pip, or your script's dependencies.
If `python3` or `pip` is missing, the training job fails when it starts.

## Test locally (optional)

To check that your training script runs in your custom container before you start a cloud training job, pass the container ID to [`viam training-script test-local`](/train/custom-training-scripts/#test-locally-with-docker):

```sh {class="command-line" data-prompt="$"}
viam training-script test-local \
  --training-script-directory=my-training/ \
  --dataset-root=<destination> \
  --container-id=<container-id> \
  --model-output-directory=<output-dir>
```

The command pulls your image and runs your script in it with Docker, the same way a cloud training job does.

## Train with the container

Start a custom training job and choose your container.

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Go to your [**DATASETS**](https://app.viam.com/data/datasets) and select the dataset you want to train on.
2. Click **Train model**.
3. Select **Train on a custom training script** and follow the prompts.
4. In the **Container version** dropdown, select your container.
   The dropdown lists Viam-managed containers, marked **(Viam)**, followed by your organization's custom containers, marked **(Custom:** _image_**)**.
5. Optionally, add custom arguments as key-value pairs in the **Arguments** section.

{{% /tab %}}
{{% tab name="CLI" %}}

Pass the container ID to [`viam train submit custom from-registry`](/cli/reference/#train-submit-custom-from-registry):

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<dataset-id> \
  --org-id=<org-id> --model-name=my-model \
  --model-version=1 --version=1 \
  --script-name=<namespace>:<script-name> \
  --container-id=<container-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Pass the container ID as `container_id` to [`submit_custom_training_job`](/reference/apis/ml-training-client/#submitcustomtrainingjob):

```python {class="line-numbers linkable-line-numbers"}
job_id = await ml_training_client.submit_custom_training_job(
    org_id="<org-id>",
    dataset_id="<dataset-id>",
    registry_item_id="<namespace>:<script-name>",
    registry_item_version="<script-version>",
    model_name="my-model",
    model_version="1",
    container_id="<container-id>",
)
```

{{% /tab %}}
{{< /tabs >}}

Monitor the job the same way as any custom training job.
See [Monitor and debug](/train/custom-training-scripts/#monitor-and-debug).

## Check which container a job used

In the Viam app, open the training job from the [**MODELS** tab](https://app.viam.com/models).
The **Details** panel shows the container's description under **Container version** and its Viam container ID under **Container ID**.

## Manage containers

### List containers

<!-- Listing isn't available in the Viam web UI outside the training job dropdown. Add a Web UI tab here when it is. -->

{{< tabs >}}
{{% tab name="CLI" %}}

To list the Viam-managed containers together with your organization's custom containers, pass your organization ID to [`viam train containers list`](/cli/reference/#train-containers-list):

```sh {class="command-line" data-prompt="$"}
viam train containers list --org-id=<org-id>
```

Without `--org-id`, the command lists only Viam-managed containers.
Add `--include-uris` to show each container's image URI.
Each entry includes the container's `ID`, which you use to train with it or delete it.

{{% /tab %}}
{{% tab name="Python" %}}

Use [`list_containers`](/reference/apis/ml-training-client/#listcontainers):

```python {class="line-numbers linkable-line-numbers"}
containers = await ml_training_client.list_containers(org_id="<org-id>")
for container in containers:
    print(container.id, container.description)
```

{{% /tab %}}
{{< /tabs >}}

### Delete a container

<!-- Deletion isn't available in the Viam web UI yet. Add a Web UI tab here when it is. -->

Deleting a custom container removes it from your organization's list of containers, so you can't start new training jobs with it.
Training jobs that are already running finish normally, and past jobs still show which container they used.
Deleting a container doesn't delete the image from Docker Hub.

{{< tabs >}}
{{% tab name="CLI" %}}

Run [`viam train containers delete`](/cli/reference/#train-containers-delete) with the container ID:

```sh {class="command-line" data-prompt="$"}
viam train containers delete --id=<container-id>
```

{{% /tab %}}
{{% tab name="Python" %}}

Use [`delete_custom_training_container`](/reference/apis/ml-training-client/#deletecustomtrainingcontainer):

```python {class="line-numbers linkable-line-numbers"}
await ml_training_client.delete_custom_training_container(id="<container-id>")
```

{{% /tab %}}
{{< /tabs >}}

## Limitations

- Images must be public and on Docker Hub. Private images and other registries, such as GitHub Container Registry or NVIDIA NGC, aren't supported.
- Viam doesn't host a container registry or build images for you.
- A custom container belongs to the organization that registered it. You can't share it with other organizations.
- Hyperparameter tuning doesn't support custom containers.

## Next steps

{{< cards >}}
{{% card link="/train/custom-training-scripts/" %}}
{{% card link="/cli/datasets-and-training/" %}}
{{% card link="/reference/apis/ml-training-client/" %}}
{{< /cards >}}
