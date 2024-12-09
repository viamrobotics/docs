---
linkTitle: "Train other models"
title: "Train other models"
tags: ["data management", "ml", "model training"]
weight: 30
layout: "docs"
type: "docs"
aliases:
  - /services/ml/upload-training-script/
  - /how-tos/create-custom-training-scripts/
no_list: true
languages: ["python"]
viamresources: ["mlmodel", "data_manager"]
platformarea: ["ml"]
description: "If you want to train models to custom specifications, write a custom training script and upload it to the Viam Registry."
date: "2024-12-04"
---

You can create custom Python training scripts that train ML models to your specifications using PyTorch, Tensorflow, TFLite, ONNX, or any other Machine Learning framework.
Once you upload a training script to the [Viam Registry](https://app.viam.com/registry?type=Training+Script), you can use it to build ML models in the Viam Cloud based on your datasets.

{{< alert title="In this page" color="tip" >}}

1. [Create a training script](#create-a-training-script) from a template.
1. [Test your training script locally](#test-your-training-script-locally) with a downloaded dataset.
1. [Upload your training script](#upload-your-training-script).
1. [Submit a training job](#submit-a-training-job) that uses the training script on a dataset to train a new ML model.

{{< /alert >}}

## Prerequisites

{{% expand "A dataset with data you can train an ML model on. Click to see instructions." %}}

For image data, you can follow the instructions to [Create a dataset and label data](/how-tos/train-deploy-ml/#create-a-dataset-and-label-data) to create a dataset.

For other data you can use the [Data Client API](/appendix/apis/data-client/) from within the training script to get data stored in the Viam Cloud.

{{% /expand%}}

{{% expand "The Viam CLI. Click to see instructions." %}}

You must have the Viam CLI installed to upload training scripts to the registry.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

## Create a training script

{{< table >}}
{{% tablestep %}}
**1. Create files**

Create the following folders and empty files:

```treeview
my-training/
├── model/
|   ├── training.py
|   └── __init__.py
└── setup.py
```

{{% /tablestep %}}
{{% tablestep %}}
**2. Add `setup.py` code**

Add the following code to `setup.py` and add additional required packages on line 11:

```python {class="line-numbers linkable-line-numbers" data-line="11"}
from setuptools import find_packages, setup

setup(
    name="my-training",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-cloud-aiplatform",
        "google-cloud-storage",
        # TODO: Add additional required packages
    ],
)
```

{{% /tablestep %}}
{{% tablestep %}}
**3. Create `__init__.py`**

If you haven't already, create a folder called <file>model</file> and create an empty file inside it called <file>\_\_init\_\_.py</file>.

{{% /tablestep %}}
{{< tablestep >}}

<p><strong>4. Add <code>training.py</code> code</strong></p>

<p>Copy this template into <file>training.py</file>:</p>

{{% expand "Click to see the template" %}}

```python {class="line-numbers linkable-line-numbers" data-line="126,170" }
import argparse
import json
import os
import typing as ty

single_label = "MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION"
multi_label = "MODEL_TYPE_MULTI_LABEL_CLASSIFICATION"
labels_filename = "labels.txt"
unknown_label = "UNKNOWN"

API_KEY = os.environ['API_KEY']
API_KEY_ID = os.environ['API_KEY_ID']


# This parses the required args for the training script.
# The model_dir variable will contain the output directory where
# the ML model that this script creates should be stored.
# The data_json variable will contain the metadata for the dataset
# that you should use to train the model.
def parse_args():
    """Returns dataset file, model output directory, and num_epochs if present.
    These must be parsed as command line arguments and then used as the model
    input and output, respectively. The number of epochs can be used to
    optionally override the default.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", dest="data_json", type=str)
    parser.add_argument("--model_output_directory", dest="model_dir", type=str)
    parser.add_argument("--num_epochs", dest="num_epochs", type=int)
    args = parser.parse_args()
    return args.data_json, args.model_dir, args.num_epochs


# This is used for parsing the dataset file (produced and stored in Viam),
# parse it to get the label annotations
# Used for training classifiction models
def parse_filenames_and_labels_from_json(
    filename: str, all_labels: ty.List[str], model_type: str
) -> ty.Tuple[ty.List[str], ty.List[str]]:
    """Load and parse JSON file to return image filenames and corresponding
    labels. The JSON file contains lines, where each line has the key
    "image_path" and "classification_annotations".
    Args:
        filename: JSONLines file containing filenames and labels
        all_labels: list of all N_LABELS
        model_type: string single_label or multi_label
    """
    image_filenames = []
    image_labels = []

    with open(filename, "rb") as f:
        for line in f:
            json_line = json.loads(line)
            image_filenames.append(json_line["image_path"])

            annotations = json_line["classification_annotations"]
            labels = [unknown_label]
            for annotation in annotations:
                if model_type == multi_label:
                    if annotation["annotation_label"] in all_labels:
                        labels.append(annotation["annotation_label"])
                # For single label model, we want at most one label.
                # If multiple valid labels are present, we arbitrarily select
                # the last one.
                if model_type == single_label:
                    if annotation["annotation_label"] in all_labels:
                        labels = [annotation["annotation_label"]]
            image_labels.append(labels)
    return image_filenames, image_labels


# Parse the dataset file (produced and stored in Viam) to get
# bounding box annotations
# Used for training object detection models
def parse_filenames_and_bboxes_from_json(
    filename: str,
    all_labels: ty.List[str],
) -> ty.Tuple[ty.List[str], ty.List[str], ty.List[ty.List[float]]]:
    """Load and parse JSON file to return image filenames
    and corresponding labels with bboxes.
    Args:
        filename: JSONLines file containing filenames and bboxes
        all_labels: list of all N_LABELS
    """
    image_filenames = []
    bbox_labels = []
    bbox_coords = []

    with open(filename, "rb") as f:
        for line in f:
            json_line = json.loads(line)
            image_filenames.append(json_line["image_path"])
            annotations = json_line["bounding_box_annotations"]
            labels = []
            coords = []
            for annotation in annotations:
                if annotation["annotation_label"] in all_labels:
                    labels.append(annotation["annotation_label"])
                    # Store coordinates in rel_yxyx format so that
                    # we can use the keras_cv function
                    coords.append(
                        [
                            annotation["y_min_normalized"],
                            annotation["x_min_normalized"],
                            annotation["y_max_normalized"],
                            annotation["x_max_normalized"],
                        ]
                    )
            bbox_labels.append(labels)
            bbox_coords.append(coords)
    return image_filenames, bbox_labels, bbox_coords


# Build the model
def build_and_compile_model(
    labels: ty.List[str], model_type: str, input_shape: ty.Tuple[int, int, int]
) -> Model:
    """Builds and compiles a model
    Args:
        labels: list of string lists, where each string list contains up to
        N_LABEL labels associated with an image
        model_type: string single_label or multi_label
        input_shape: 3D shape of input
    """

    # TODO: Add logic to build and compile model

    return model


def save_labels(labels: ty.List[str], model_dir: str) -> None:
    """Saves a label.txt of output labels to the specified model directory.
    Args:
        labels: list of string lists, where each string list contains up to
        N_LABEL labels associated with an image
        model_dir: output directory for model artifacts
    """
    filename = os.path.join(model_dir, labels_filename)
    with open(filename, "w") as f:
        for label in labels[:-1]:
            f.write(label + "\n")
        f.write(labels[-1])


def save_model(
    model: Model,
    model_dir: str,
    model_name: str,
) -> None:
    """Save model as a TFLite model.
    Args:
        model: trained model
        model_dir: output directory for model artifacts
        model_name: name of saved model
    """
    file_type = ""

    # Save the model to the output directory.
    filename = os.path.join(model_dir, f"{model_name}.{file_type}")
    with open(filename, "wb") as f:
        f.write(model)


if __name__ == "__main__":
    DATA_JSON, MODEL_DIR = parse_args()

    IMG_SIZE = (256, 256)

    # Read dataset file.
    # TODO: change labels to the desired model output.
    LABELS = ["orange_triangle", "blue_star"]

    # The model type can be changed based on whether you want the model to
    # output one label per image or multiple labels per image
    model_type = multi_label
    image_filenames, image_labels = parse_filenames_and_labels_from_json(
        DATA_JSON, LABELS, model_type)

    # Build and compile model on data
    model = build_and_compile_model()

    # Save labels.txt file
    save_labels(LABELS + [unknown_label], MODEL_DIR)
    # Convert the model to tflite
    save_model(
        model, MODEL_DIR, "classification_model", IMG_SIZE + (3,)
    )
```

{{% /expand %}}

{{% /tablestep %}}
{{< tablestep >}}

<p><strong>5. Understand template script parsing functionality</strong></p>
<p>When a training script is run, the Viam platform passes the dataset file for the training and the designated model output directory to the script.</p>
<p>The template contains functionality to parse the command line inputs and parse annotations from the dataset file.</p>

{{% expand "Click for more information on parsing command line inputs." %}}

The script you are creating must take the following command line inputs:

- `dataset_file`: a file containing the data and metadata for the training job
- `model_output_directory`: the location where the produced model artifacts are saved to

The `parse_args()` function in the template parses your arguments.

You can add additional custom command line inputs by adding them to the `parse_args()` function.

{{% /expand %}}

{{% expand "Click for more information on parsing annotations from dataset file." %}}

When you submit a training job to the Viam Cloud, Viam will pass a `dataset_file` to the training script when you train an ML model with it.
The file contains metadata from the dataset used for the training, including the file path for each data point and any annotations associated with the data.

Dataset JSON files for image datasets with bounding box labels and classification labels are formatted as follows:

```json {class="line-numbers linkable-line-numbers"}
{
    "image_path": "/path/to/data/data1.jpeg",
    "bounding_box_annotations": [
        {
            "annotation_label": "blue_star",
            "x_min_normalized": 0.38175675675675674,
            "x_max_normalized": 0.5101351351351351,
            "y_min_normalized": 0.35585585585585583,
            "y_max_normalized": 0.527027027027027
        }
    ],
    "classification_annotations": [
        {
            "annotation_label": "blue_star"
        }
    ]
}
{
    "image_path": "/path/to/data/data2.jpeg",
    "bounding_box_annotations": [
        {
            "annotation_label": "blue_star",
            "x_min_normalized": 0.2939189189189189,
            "x_max_normalized": 0.4594594594594595,
            "y_min_normalized": 0.25225225225225223,
            "y_max_normalized": 0.5495495495495496
        }
    ],
    "classification_annotations": [
        {
            "annotation_label": "blue_star"
        }
    ]
}

{
    "image_path": "/path/to/data/data3.jpeg",
    "bounding_box_annotations": [
        {
            "annotation_label": "blue_star",
            "x_min_normalized": 0.03557312252964427,
            "x_max_normalized": 0.2015810276679842,
            "y_min_normalized": 0.30526315789473685,
            "y_max_normalized": 0.5368421052631579
        },
        {
            "annotation_label": "blue_square",
            "x_min_normalized": 0.039525691699604744,
            "x_max_normalized": 0.2015810276679842,
            "y_min_normalized": 0.2578947368421053,
            "y_max_normalized": 0.5473684210526316
        }
    ],
    "classification_annotations": [
        {
            "annotation_label": "blue_star"
        },
        {
            "annotation_label": "blue_square"
        }
    ]
}
```

In your training script, you must parse the dataset file for the classification or bounding box annotations from the dataset metadata.
Depending on if you are training a classification or detection model, the template script contains the `parse_filenames_and_labels_from_json()` and the `parse_filenames_and_bboxes_from_json()` function.

{{% /expand%}}

<p>If the script you are creating does not use an image dataset, you only need the model output directory.</p>

{{% /tablestep %}}
{{% tablestep %}}
**6. Add logic to produce the model artifact**

You must fill in the `build_and_compile_model` function.
In this part of the script, you use the data from the dataset and the annotations from the dataset file to build a Machine Learning model.

As an example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://github.com/viam-modules/classification-tflite) that trains a classification model using TensorFlow and Keras.

{{% /tablestep %}}
{{% tablestep %}}
**7. Save the model artifact**

The `save_model()` and the `save_labels()` functions in the template before the `main` logic save the model artifact your training job produces to the `model_output_directory` in the cloud.

Once a training job is complete, Viam checks the output directory and creates a package with all of the contents of the directory, creating or updating a registry item for the ML model.

You must fill in these functions.

As an example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://github.com/viam-modules/classification-tflite) that trains a classification model using TensorFlow and Keras.

{{% /tablestep %}}
{{% tablestep %}}
**8. Update the main method**

Update the main to call the functions you have just created.

{{% /tablestep %}}
{{% tablestep %}}
**9. Using Viam APIs in a training script**

If you need to access any of the [Viam APIs](/appendix/apis/) within a custom training script, you can use the environment variables `API_KEY` and `API_KEY_ID` to establish a connection.
These environment variables will be available to training scripts.

```python
async def connect() -> ViamClient:
    """Returns a authenticated connection to the ViamClient for the requested
    org associated with the submitted training job."""
    # The API key and key ID can be accessed programmatically, using the
    # environment variable API_KEY and API_KEY_ID. The user does not need to
    # supply the API keys, they are provided automatically when the training
    # job is submitted.
    dial_options = DialOptions.with_api_key(
        os.environ.get("API_KEY"), os.environ.get("API_KEY_ID")
    )
    return await ViamClient.create_from_dial_options(dial_options)
```

{{% /tablestep %}}
{{< /table >}}

## Test your training script locally

You can export one of your Viam datasets to test your training script locally.

{{< table >}}
{{% tablestep %}}
**1. Export your dataset**

You can get the dataset ID from the dataset page or using the [`viam dataset list`](/cli/#dataset) command:

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=<destination> --dataset-id=<dataset-id> --include-jsonl=true
```

The dataset will be formatted like the one Viam produces for the training.
Use the `parse_filenames_and_labels_from_json` and `parse_filenames_and_bboxes_from_json` functions to get the images and annotations from your dataset file.

{{% /tablestep %}}
{{% tablestep %}}
**2. Run your training script locally**

Install any required dependencies and run your training script specifying the path to the <FILE>dataset.jsonl</FILE> file from your exported dataset:

```sh {class="command-line" data-prompt="$"}
python3 -m model.training --dataset_file=/path/to/dataset.jsonl \
    --model_output_directory=. --custom_arg=3
```

{{% /tablestep %}}
{{< /table >}}

## Upload your training script

To be able to use your training script in the Viam platform, you must upload it to the Viam Registry.

{{< table >}}
{{% tablestep %}}
**1. Package the training script as a <file>tar.gz</file> source distribution**

Before you can upload your training script to Viam, you have to compress your project folder into a tar.gz file:

```sh {class="command-line" data-prompt="$"}
tar -czvf my-training.tar.gz my-training/
```

{{% alert title="Tip" color="tip" %}}
You can refer to the directory structure of this [example classification training script](https://github.com/viam-modules/classification-tflite).
{{% /alert %}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Upload a training script**

To upload your custom training script to the registry, use the `viam training-script upload` command.

{{< tabs >}}
{{% tab name="Usage" %}}

```sh {class="command-line" data-prompt="$"}
viam training-script upload --path=<path-to-tar.gz> \
  --org-id=<org-id> --script-name=<training-script-name>
```

{{% /tab %}}
{{% tab name="Examples" %}}

```sh {class="command-line" data-prompt="$"}
viam training-script upload --path=my-training.tar.gz \
  --org-id=<ORG_ID> --script-name=my-training-script

viam training-script upload --path=my-training.tar.gz \
  --org-id=<ORG_ID> --script-name=my-training \
  --framework=tensorflow --type=single_label_classification \
  --description="Custom image classification model" \
  --visibility=private
```

{{% /tab %}}
{{< /tabs >}}

You can also [specify the version, framework, type, visibility, and description](/cli/#training-script) when uploading a custom training script.

To find your organization's ID, run the following command:

```sh {class="command-line" data-prompt="$"}
viam organization list
```

After a successful upload, the CLI displays a confirmation message with a link to view your changes online.
You can view uploaded training scripts by navigating to the [registry's **Training Scripts** page](https://app.viam.com/registry?type=Training+Script).

{{% /tablestep %}}
{{< /table >}}

## Submit a training job

After uploading the training script, you can run it by submitting a training job through the Viam app or using the Viam CLI or [ML Training client API](/appendix/apis/ml-training-client/#submittrainingjob).

{{< table >}}
{{% tablestep %}}
**1. Create the training job**

{{< tabs >}}
{{% tab name="Viam app" min-height="150px" %}}

{{<imgproc src="/services/ml/train.svg" class="fill alignleft" style="width: 200px" declaredimensions=true alt="Train models">}}

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train a model on.

Click **Train model** and select **Train on a custom training script**, then follow the prompts.

{{% /tab %}}
{{% tab name="CLI" %}}

You can use [`viam train submit custom from-registry`](/cli/#positional-arguments-submit) to submit a training job.

For example:

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<INSERT DATASET ID> \
  --org-id=<INSERT ORG ID> --model-name=MyRegistryModel \
  --model-version=2 --version=1 \
  --script-name=mycompany:MyCustomTrainingScript
  --args=custom_arg1=3,custom_arg2="'green_square blue_star'"
```

This command submits a training job to the previously uploaded `MyCustomTrainingScript` with another input dataset, which trains `MyRegistryModel` and publishes that to the registry.

You can get the dataset id from the dataset page or using the [`viam dataset list`](/cli/#dataset) command.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Check on training job process**

You can view your training job on the **DATA** page's [**TRAINING** tab](https://app.viam.com/training).

Once the model has finished training, it becomes visible on the **DATA** page's [**MODELS** tab](https://app.viam.com/data/models).

You will receive an email when your training job completes.

You can also check your training jobs and their status from the CLI:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<INSERT ORG ID> --job-status=unspecified
```

{{% /tablestep %}}
{{% tablestep %}}
**3. Debug your training job**

From the **DATA** page's [**TRAINING** tab](https://app.viam.com/training), click on your training job's ID to see its logs.

{{< alert title="Note" color="note" >}}

Your training script may output logs at the error level but still succeed.

{{< /alert >}}

You can also view your training jobs' logs with the [`viam train logs`](/cli/#train) command.

{{% /tablestep %}}
{{< /table >}}

## Next steps

To use your new model with machines, you must deploy it with the [ML model service](/services/ml/).
Then you can use another service, such as the vision service, to apply the deployed model to camera feeds.

To see models in use with machines, see one of the following resources:

{{< cards >}}
{{% card link="/how-tos/detect-people/" %}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" %}}
{{< /cards >}}