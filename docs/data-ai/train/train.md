---
linkTitle: "Train other models"
title: "Train other models"
tags: ["data management", "ml", "model training"]
weight: 51
layout: "docs"
type: "docs"
aliases:
  - /services/ml/upload-training-script/
  - /how-tos/create-custom-training-scripts/
  - /services/ml/training-scripts/
  - /registry/training-scripts/
  - /data-ai/ai/train/
languages: ["python"]
viamresources: ["mlmodel", "data_manager"]
platformarea: ["ml"]
description: "If you want to train models to custom specifications, write a custom training script and upload it to the Viam Registry."
date: "2024-12-04"
---

You can create custom Python training scripts that train machine learning models to your specifications using PyTorch, TensorFlow, TFLite, ONNX, or any other ML framework.
Once you upload a training script to the [registry](https://app.viam.com/registry?type=Training+Script), you can use it to build ML models in the Viam Cloud based on your datasets.

You can also use training scripts that are in the registry already.
If you wish to do this, skip to [Submit a training job](#submit-a-training-job).

## Prerequisites

{{% expand "A dataset that contains training data" %}}

For images, follow the instructions to [Create a dataset](/data-ai/train/create-dataset/) to create a dataset and label data.

For other data, use the [Data Client API](/dev/reference/apis/data-client/) from within the training script to store data in the Viam Cloud.

{{% /expand%}}

{{% expand "The Viam CLI" %}}

You must have the Viam CLI installed to upload training scripts to the registry.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

## Create a training script

{{< table >}}
{{% tablestep start=1 %}}
**Create files**

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
**Add `setup.py` code**

Add the following code to `setup.py`:

```python {class="line-numbers linkable-line-numbers"}
from setuptools import find_packages, setup

setup(
    name="my-training",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # TODO: Add additional required packages
    ],
)
```

{{% /tablestep %}}
{{< tablestep >}}

<p><strong>Add <code>training.py</code> code</strong></p>

<p>You can set up your training script to use a hard coded set of labels or allow users to pass in a set of labels when using the training script. Allowing users to pass in labels when using training scripts makes your training script more flexible for reuse.</p>
<p>Copy one of the following templates into <file>training.py</file>, depending on how you want to handle labels:</p>

{{% expand "Click to see the template without parsing labels (recommended for use with UI)" %}}

```python {class="line-numbers linkable-line-numbers" data-line="134" }
import argparse
import json
import os
import typing as ty
from tensorflow.keras import Model  # Add proper import
import tensorflow as tf  # Add proper import

single_label = "MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION"
multi_label = "MODEL_TYPE_MULTI_LABEL_CLASSIFICATION"
labels_filename = "labels.txt"
unknown_label = "UNKNOWN"

API_KEY = os.environ['API_KEY']
API_KEY_ID = os.environ['API_KEY_ID']

DEFAULT_EPOCHS = 200

# This parses the required args for the training script.
# The model_dir variable will contain the output directory where
# the ML model that this script creates should be stored.
# The data_json variable will contain the metadata for the dataset
# that you should use to train the model.


def parse_args():
    """Returns dataset file, model output directory, and num_epochs
    if present. These must be parsed as command line arguments and then used
    as the model input and output, respectively. The number of epochs can be
    used to optionally override the default.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", dest="data_json",
                        type=str, required=True)
    parser.add_argument("--model_output_directory", dest="model_dir",
                        type=str, required=True)
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
    # Save the model to the output directory
    file_type = "tflite"  # Add proper file type
    filename = os.path.join(model_dir, f"{model_name}.{file_type}")

    # Example: Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the model
    with open(filename, "wb") as f:
        f.write(tflite_model)


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

    # Validate epochs
    epochs = (
        DEFAULT_EPOCHS if NUM_EPOCHS is None
        or NUM_EPOCHS <= 0 else int(NUM_EPOCHS)
    )

    # Build and compile model on data
    model = build_and_compile_model(image_labels, model_type, IMG_SIZE + (3,))

    # Save labels.txt file
    save_labels(LABELS + [unknown_label], MODEL_DIR)
    # Convert the model to tflite
    save_model(
        model, MODEL_DIR, "classification_model"
    )
```

{{% /expand %}}

{{% expand "Click to see the template with parsed labels" %}}

```python {class="line-numbers linkable-line-numbers" data-line="148" }
import argparse
import json
import os
import typing as ty
from tensorflow.keras import Model  # Add proper import
import tensorflow as tf  # Add proper import

single_label = "MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION"
multi_label = "MODEL_TYPE_MULTI_LABEL_CLASSIFICATION"
labels_filename = "labels.txt"
unknown_label = "UNKNOWN"

API_KEY = os.environ['API_KEY']
API_KEY_ID = os.environ['API_KEY_ID']

DEFAULT_EPOCHS = 200

# This parses the required args for the training script.
# The model_dir variable will contain the output directory where
# the ML model that this script creates should be stored.
# The data_json variable will contain the metadata for the dataset
# that you should use to train the model.


def parse_args():
    """Returns dataset file, model output directory, labels, and num_epochs
    if present. These must be parsed as command line arguments and then used
    as the model input and output, respectively. The number of epochs can be
    used to optionally override the default.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", dest="data_json",
                        type=str, required=True)
    parser.add_argument("--model_output_directory", dest="model_dir",
                        type=str, required=True)
    parser.add_argument("--num_epochs", dest="num_epochs", type=int)
    parser.add_argument(
        "--labels",
        dest="labels",
        type=str,
        required=True,
        help="Space-separated list of labels, \
            enclosed in single quotes (e.g., 'label1 label2').",
    )
    args = parser.parse_args()

    if not args.labels:
        raise ValueError("Labels must be provided")

    labels = [label.strip() for label in args.labels.strip("'").split()]
    return args.data_json, args.model_dir, args.num_epochs, labels


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
    # Save the model to the output directory
    file_type = "tflite"  # Add proper file type
    filename = os.path.join(model_dir, f"{model_name}.{file_type}")

    # Example: Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the model
    with open(filename, "wb") as f:
        f.write(tflite_model)


if __name__ == "__main__":
    DATA_JSON, MODEL_DIR, NUM_EPOCHS, LABELS = parse_args()

    IMG_SIZE = (256, 256)

    # Read dataset file.
    # The model type can be changed based on whether you want the model to
    # output one label per image or multiple labels per image
    model_type = multi_label
    image_filenames, image_labels = parse_filenames_and_labels_from_json(
        DATA_JSON, LABELS, model_type)

    # Validate epochs
    epochs = (
        DEFAULT_EPOCHS if NUM_EPOCHS is None
        or NUM_EPOCHS <= 0 else int(NUM_EPOCHS)
    )

    # Build and compile model on data
    model = build_and_compile_model(image_labels, model_type, IMG_SIZE + (3,))

    # Save labels.txt file
    save_labels(LABELS + [unknown_label], MODEL_DIR)
    # Convert the model to tflite
    save_model(
        model, MODEL_DIR, "classification_model"
    )
```

{{% /expand %}}

{{% /tablestep %}}
{{< tablestep >}}

<p><strong>Understand template script parsing functionality</strong></p>
<p>When a training script is run, the Viam platform passes the dataset file for the training and the designated model output directory to the script.</p>
<p>The template contains functionality to parse the command line inputs and parse annotations from the dataset file.</p>

{{% expand "Click for more information on parsing command line inputs." %}}

The script you are creating must take the following command line inputs:

- `dataset_file`: a file containing the data and metadata for the training job
- `model_output_directory`: the location where the produced model artifacts are saved to

If you used the training script template that allows users to pass in labels, it will also take the following command line inputs:

- `labels`: space separated list of labels, enclosed in single quotes

The `parse_args()` function in the template parses your arguments.

You can add additional custom command line inputs by adding them to the `parse_args()` function.

{{% /expand %}}

{{% expand "Click for more information on parsing annotations from the dataset file." %}}

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

In your training script, you must parse the dataset file to extract classification or bounding box annotations from the dataset metadata.
Depending on if you are training a classification or detection model, the template script contains the `parse_filenames_and_labels_from_json()` and the `parse_filenames_and_bboxes_from_json()` function.

{{% /expand%}}

<p>If the script you are creating does not use an image dataset, you only need the model output directory.</p>

{{% /tablestep %}}
{{% tablestep %}}
**Add logic to produce the model artifact**

Fill in the `build_and_compile_model` function.
In this part of the script, you use data and annotations from the dataset file to build an ML model.

As an example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://github.com/viam-modules/classification-tflite) that trains a classification model using TensorFlow and Keras.

{{% /tablestep %}}
{{% tablestep %}}
**Save the model artifact**

In this example template, the training job produces a model artifact.
The `save_model()` and `save_labels()` functions save that model artifact to the `model_output_directory`.

When the training job completes, Viam checks the output directory for the model artifact, packages the model, and uploads it to the registry.

You must fill in the `save_model()` and `save_labels()` functions.

As an example, refer to the logic from <file>model/training.py</file> from this [example classification training script](https://github.com/viam-modules/classification-tflite) that trains a classification model using TensorFlow and Keras.

{{% /tablestep %}}
{{% tablestep %}}
**Update the main method**

Update the main to call the functions you have just created.

{{% /tablestep %}}
{{% tablestep %}}
**Use Viam APIs in a training script**

To access [Viam APIs](/dev/reference/apis/) within a custom training script, use the environment variables `API_KEY` and `API_KEY_ID` to establish a connection.

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
{{% tablestep start=1 %}}
**Export your dataset**

You can get the dataset ID from the dataset page or using the [`viam dataset list`](/dev/tools/cli/#dataset) command:

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=<destination> --dataset-id=<dataset-id> --include-jsonl=true
```

The dataset will be formatted like the one Viam produces for the training.
Use the `parse_filenames_and_labels_from_json` and `parse_filenames_and_bboxes_from_json` functions to get the images and annotations from your dataset file.

{{% /tablestep %}}
{{% tablestep %}}
**Run your training script locally**

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
{{% tablestep start=1 %}}
**Package the training script as a <file>tar.gz</file> source distribution**

Before you can upload your training script to Viam, you have to compress your project folder into a tar.gz file:

```sh {class="command-line" data-prompt="$"}
tar -czvf my-training.tar.gz my-training/
```

{{% alert title="Tip" color="tip" %}}
You can refer to the directory structure of this [example classification training script](https://github.com/viam-modules/classification-tflite).
{{% /alert %}}

{{% /tablestep %}}
{{% tablestep %}}
**Upload a training script**

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

You can also [specify the version, framework, type, visibility, and description](/dev/tools/cli/#training-script) when uploading a custom training script.

To find your organization's ID, run the following command:

```sh {class="command-line" data-prompt="$"}
viam organization list
```

After a successful upload, the CLI displays a confirmation message with a link to view your changes online.
You can view uploaded training scripts by navigating to the [registry's **Training Scripts** page](https://app.viam.com/registry?type=Training+Script).

{{% /tablestep %}}
{{< /table >}}

## Submit a training job

After uploading the training script, you can run it by submitting a training job using the web UI, the CLI or the [ML training client API](/dev/reference/apis/ml-training-client/#submittrainingjob).

{{< table >}}
{{% tablestep start=1 %}}
**Create the training job**

{{< tabs >}}
{{% tab name="Web UI" min-height="150px" %}}
Navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train a model on.

Click **Train model** and select **Train on a custom training script**, then follow the prompts.

{{% alert title="Tip" color="tip" %}}
If you used the version of <file>training.py</file> that allows users to pass in labels, your training job will fail with the error `ERROR training.py: error: the following arguments are required: --labels`.
To use labels, you must use the CLI.
{{% /alert %}}

{{% /tab %}}
{{% tab name="CLI" %}}

You can use [`viam train submit custom from-registry`](/dev/tools/cli/#positional-arguments-submit) to submit a training job.

For example:

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<INSERT DATASET ID> \
  --org-id=<INSERT ORG ID> --model-name=MyRegistryModel \
  --model-version=2 --version=1 \
  --script-name=mycompany:MyCustomTrainingScript \
  --args=custom_arg1=3,custom_arg2="'green_square blue_star'"
```

This command submits a training job to the previously uploaded `MyCustomTrainingScript` with another input dataset, which trains `MyRegistryModel` and publishes that to the registry.

You can get the dataset id from the **DATASET** tab of the **DATA** page or by running the [`viam dataset list`](/dev/tools/cli/#dataset) command.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Check on training job process**

You can view your training job on the **DATA** page's [**TRAINING** tab](https://app.viam.com/training).

Once the model has finished training, it becomes visible on the **DATA** page's [**MODELS** tab](https://app.viam.com/models).

You will receive an email when your training job completes.

You can also check your training jobs and their status from the CLI:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<INSERT ORG ID> --job-status=unspecified
```

{{% /tablestep %}}
{{% tablestep %}}
**Debug your training job**

From the **DATA** page's [**TRAINING** tab](https://app.viam.com/training), click on your training job's ID to see its logs.

{{< alert title="Note" color="note" >}}

Your training script may output logs at the error level but still succeed.

{{< /alert >}}

You can also view your training jobs' logs with the [`viam train logs`](/dev/tools/cli/#train) command.

Training logs expire after 7 days.

{{% /tablestep %}}
{{< /table >}}

To use your new model with machines, you must [deploy it](/data-ai/ai/deploy/) with the appropriate ML model service.
Then you can use another service, such as the vision service, to [run inference](/data-ai/ai/run-inference/).
