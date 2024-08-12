---
title: "Train a Model with a Custom Python Training Script"
linkTitle: "Use a Custom Training Script"
weight: 90
type: "docs"
tags: ["data management", "ml", "model training"]
description: "How to write and upload a custom machine learning model training script to the Viam registry and use it to submit training jobs."
no_service: true
# SME: Tahiya S.
---

You can create your own custom Python training script that trains ML models to your specifications using the Machine Learning framework of your choice (PyTorch, Tensorflow, TFLite, ONNX, or any other framework).
Once added to the [Viam registry](https://app.viam.com/registry?type=Training+Script), you can use the training script to build ML models based on your datasets.

{{< alert title="Note" color="note" >}}
For a no-code approach, you can [train TFLite classification and object detection models](/services/ml/train-model/) on the [Viam app **DATA** page](https://app.viam.com) or use existing [training scripts](https://app.viam.com/registry?type=Training+Script) from the Viam Registry.
{{< /alert >}}

Follow this guide to create, upload, and submit a Python script that loads a training dataset, trains an ML model, and produces a model artifact.

## Create a training script

1. Create a folder for the training-script, for example <file>my-training</file>.
1. Inside the top level folder (in this example <file>my-training</file>), create a file called `setup.py` with the following contents:

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

   Ensure you add additional required packages on line 11.

1. Inside the top level folder (in this example <file>my-training</file>), create a folder called <file>model</file> and create an empty file called <file>\_\_init\_\_.py</file> inside it.
1. Inside the <file>model</file> folder, create a file called <file>training.py</file>.

   {{< alert title="Using Viam APIs in a training script" color="note" >}}
   If you need to access any of the [Viam APIs](/appendix/apis/) within a custom training script, you can use the environment variables `API_KEY` and `API_KEY_ID` to establish a connection.
   {{< /alert >}}

   Copy this template into <file>training.py</file>:

   ```python {class="line-numbers linkable-line-numbers" }
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
       """Dataset file and model output directory are required parameters. These must be parsed as command line
           arguments and then used as the model input and output, respectively.
       """
       parser = argparse.ArgumentParser()
       parser.add_argument("--dataset_file", dest="data_json", type=str)
       parser.add_argument("--model_output_directory", dest="model_dir", type=str)
       args = parser.parse_args()
       return args.data_json, args.model_dir

   # This is used for parsing the dataset file (produced and stored in Viam),
   # parse it to get the label annotations
   # Used for training classifiction models
   def parse_filenames_and_labels_from_json(
       filename: str, all_labels: ty.List[str], model_type: str
   ) -> ty.Tuple[ty.List[str], ty.List[str]]:
       """Load and parse JSON file to return image filenames and corresponding labels.
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
           labels: list of string lists, where each string list contains up to N_LABEL labels associated with an image
           model_type: string single_label or multi_label
           input_shape: 3D shape of input
       """

       # TODO: Add logic to build and compile model

       return model

   def save_labels(labels: ty.List[str], model_dir: str) -> None:
       """Saves a label.txt of output labels to the specified model directory.
       Args:
           labels: list of string lists, where each string list contains up to N_LABEL labels associated with an image
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

       # The model type can be changed based on whether you want the model to output one label per image or multiple labels per image
       model_type = multi_label
       image_filenames, image_labels = parse_filenames_and_labels_from_json(DATA_JSON, LABELS, model_type)

       # Build and compile model on data
       model = build_and_compile_model()

       # Save labels.txt file
       save_labels(LABELS + [unknown_label], MODEL_DIR)
       # Convert the model to tflite
       save_model(
           model, MODEL_DIR, "classification_model", IMG_SIZE + (3,)
       )
   ```

### Template script explained

{{%expand "Parsing command line inputs" %}}

The script you are creating must take the following command line inputs:

- `dataset_file`: a file containing the data and metadata for the training job
- `model_output_directory`: the location where the produced model artifacts are saved to

The `parse_args()` function in the template parses your arguments.

{{% /expand%}}
{{%expand "Parsing annotations from dataset file" %}}

The `dataset_file` is a file that the Viam platform will pass to the training script when you train an ML model with it.
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
{{%expand "Logic to produce model artifact" %}}

The next part of the script depends on the type of ML training you are creating.
In this part of the script, you use the data from the dataset and the annotations from the dataset file to build a Machine Learning model.

As an example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb) that trains a classification model using TensorFlow and Keras.

{{% alert title="Tip" color="tip" %}}
You must log in to the [Viam app](https://app.viam.com/) to download the package containing the classification training script from the registry.
{{% /alert %}}

{{% /expand%}}
{{%expand "Saving the model artifact the script produces" %}}

The `save_model()` and the `save_labels()` functions in the template before the `main` function save the model artifact your training job produces to the `model_output_directory` in the cloud.

Once a training job is complete, Viam checks the output directory and creates a package with all of the contents of the directory, creating or updating a registry item for the ML model.

As an example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb) that trains a classification model using TensorFlow and Keras.

```python {class="line-numbers linkable-line-numbers"}
# Save the labels file which is used in conjunctions with the ML model
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


# Save the model artifact to the Viam registry using the provided
# ML model name and version
def save_tflite_classification(
    model: Model,
    model_dir: str,
    model_name: str,
    target_shape: ty.Tuple[int, int, int],
) -> None:
    """Save model as a TFLite model.
    Args:
        model: trained model
        model_dir: output directory for model artifacts
        model_name: name of saved model
        target_shape: desired output shape of predictions from model
    """
    # Convert the model to tflite, with batch size 1 so the graph does not have
    # dynamic-sized tensors.
    input = tf.keras.Input(target_shape, batch_size=1, dtype=tf.uint8)
    output = model(input, training=False)
    wrapped_model = tf.keras.Model(inputs=input, outputs=output)
    converter = tf.lite.TFLiteConverter.from_keras_model(wrapped_model)
    converter.target_spec.supported_ops = TFLITE_OPS
    tflite_model = converter.convert()

    # Save the model to the output directory.
    filename = os.path.join(model_dir, f"{model_name}.tflite")
    with open(filename, "wb") as f:
        f.write(tflite_model)
```

{{% /expand%}}
{{%expand "The main function" %}}

The main function runs the training job by:

1. parsing command line inputs,
2. parsing the dataset and annotations from the dataset file,
3. producing the model artifact, and
4. saving the model artifact.

The `main()` function is executed when a training job runs.

As an example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb) that trains a classification model using TensorFlow and Keras.

{{% /expand%}}

## Package the training script as a <file>tar.gz</file> source distribution

You need to save your training script as a gzip'd tarball to run it in the Viam ML training service.
Follow the instructions to [create a <file>tar.gz</file>](https://docs.python.org/3.10/distutils/sourcedist) from your project folder.

{{% alert title="Tip" color="tip" %}}
You can refer to the directory structure of this [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb).
You must log in to the Viam app to download the package.
Unzip the package and see <file>model/training.py</file> for an example entrypoint file.
{{% /alert %}}

## Upload a new training script or new version

You must use the [Viam CLI](/cli/) to upload your training script to the Registry.

You can use the [`viam training-script upload`](/cli/#training-script) command to upload a new script.

For example:

```sh {class="command-line" data-prompt="$"}
viam training-script upload --path=<path-to-tar.gz> --org-id=<INSERT ORG ID> --script-name=<org-id-or-namespace:training-script-name>
```

To find your organization's ID, navigate to your organization's **Settings** page in [the Viam app](https://app.viam.com/).
Find **Organization ID** and click the copy icon.

Once uploaded, you can view the script by navigating to the [registry's **Training Scripts** page](https://app.viam.com/registry?type=Training+Script).

You can also simultaneously upload a training script and submit a training job with the [`viam train submit custom with-upload` command](/cli/#position-arguments-submit-custom).

## Submit a training job

After uploading the training script, you can run it by submitting a training job.

You can use [`viam train submit custom from-registry`](/cli/#positional-arguments-submit) to submit a training job from a training script already uploaded to the registry or `viam train submit custom from-upload` to upload a training script and submit a training job at the same time.

For example:

{{< tabs >}}
{{% tab name="from-registry" %}}

```sh {class="command-line" data-prompt="$"}
viam train submit custom from-registry --dataset-id=<INSERT DATASET ID> --org-id=<INSERT ORG ID> --model-name="MyRegistryModel" --model-version="2" --version="1" --script-name="mycompany:MyCustomTrainingScript"
```

This command submits a training job to the previously uploaded `"MyCustomTrainingScript"` with another input dataset, which trains `"MyRegistryModel"` and publishes that to the registry.

{{% /tab %}}
{{% tab name="with-upload" %}}

```sh {class="command-line" data-prompt="$"}
viam train submit custom with-upload --dataset-id=<INSERT DATASET ID> --model-org-id=<INSERT ORG ID> --model-name="MyRegistryModel" --model-type="single_label_classification" --model-version="2" --version="1" --path=<path-to-tar.gz> --script-name="mycompany:MyCustomTrainingScript"
```

This command uploads a script called `"MyCustomTrainingScript"` to the registry under the specified organization and also submits a training job to that script with the input dataset, which generates a new version of the single-classification ML model `"MyRegistryModel"` and publishes that to the registry.

{{% /tab %}}
{{< /tabs >}}

To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) of the **DATA** tab on the Viam app and select a dataset.
Click **...** in the left-hand menu and click **Copy dataset ID**.
To find your organization's ID, navigate to your organization's **Settings** page in [the Viam app](https://app.viam.com/).
Find **Organization ID** and click the copy icon.

Once submitted, view your training job in the **Training** section of the Viam app's **DATA** page's [**MODELS** tab](https://app.viam.com/data/models).
You can also view the uploaded ML model in the [**MODELS** tab](https://app.viam.com/data/models).

## Update the visibility of a training script

To update the visibility of a training script, use the CLI's [`viam training-script update`](/cli/#training-script) command and set the `--visibility` flag to `public`, `private`, or `draft`.

## Next steps

{{< cards >}}
{{% card link="/services/ml/deploy/" %}}
{{% card link="/services/vision/mlmodel/" %}}
{{% card link="/services/ml/edit/" %}}
{{< /cards >}}
