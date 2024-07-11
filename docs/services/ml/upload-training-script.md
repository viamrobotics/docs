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
Once added to the [Viam registry](https://app.viam.com/registry/), you can use the training script to build models for your datasets.

{{< alert title="Note" color="note" >}}
For a lower-code approach, you can [train TFLite classification and object detection models](/services/ml/train-model/) on the [Viam app **DATA** page](https://app.viam.com).
{{< /alert >}}

Follow this guide to create, upload, and submit a Python script that loads a training dataset, trains an ML model, and produces a model artifact.

## Create a training script

To start, create an entrypoint file called <file>training.py</file> in a folder called <file>model</file>.
This file will contain the main logic of your training script.

Add the following logic to your code in <file>training.py</file>:

{{%expand "Step 1: Parse command line inputs" %}}

The script you are creating must take the following command line inputs:

- `dataset_file`: a file containing the data and metadata for the training job
- `model_output_directory`: the location where the produced model artifacts are saved to

Parse these arguments in your training script with the following method:

```python {class="line-numbers linkable-line-numbers" data-line="364"}
# This parses the required args for the training script.
# The model_dir variable will contain the output directory where
# the ML model that this scrips creates should be stored.
# The data_json variable will contain the metadata for the dataset
# that you should use to train the model.
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", dest="data_json", type=str)
    parser.add_argument("--model_output_directory", dest="model_dir", type=str)
    args = parser.parse_args()
    model_dir = args.model_dir
    data_json = args.data_json
    return model_dir, data_json
```

{{% /expand%}}
{{%expand "Step 2: Parse annotations from dataset file" %}}

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
Depending on if you are training a classification or detection model, use the following functions:

```python {class="line-numbers linkable-line-numbers"}
# This is used for parsing the dataset file (produced and stored in Viam),
# parse it to get the label annotations
# Used for training classifiction models
def parse_filenames_and_labels_from_json(
    filename: str, all_labels: ty.List[str]
) -> ty.Tuple[ty.List[str], ty.List[str]]:
    """Load and parse JSON file to return image filenames and
    corresponding labels.
    Args:
        filename: JSONLines file containing filenames and labels
        all_labels: list of all labels present in dataset
    """
    image_filenames = []
    image_labels = []

    with open(filename, "rb") as f:
        for line in f:
            json_line = json.loads(line)
            image_filenames.append(json_line["image_path"])

            annotations = json_line["classification_annotations"]
            labels = []
            for annotation in annotations:
                if annotation["annotation_label"] in all_labels:
                    labels.append(annotation["annotation_label"])
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
```

{{% /expand%}}
{{%expand "Step 3: Add logic to produce model artifact" %}}

After reading in the dataset and preparing the data for training, add logic to build and compile the model using the data passed in through the data file.
The code in this part of your script depends on the type of ML training you are doing.

For example, you can refer to the logic from <file>model/training.py</file> from this [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb) that trains a classification model using TensorFlow and Keras.

The logic to build and compile the classification model looks like this:

```python {class="line-numbers linkable-line-numbers"}
# Build the Keras model
def build_and_compile_classification(
    labels: ty.List[str], model_type: str, input_shape: ty.Tuple[int, int, int]
) -> Model:
    units, activation, loss_fnc, metrics = get_neural_network_params(
        len(labels), model_type
    )

    x = tf.keras.Input(input_shape, dtype=tf.uint8)
    # Data processing
    preprocessing = preprocessing_layers_classification(input_shape[:-1])
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip(),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
        ]
    )

    # Get the pre-trained model
    base_model = tf.keras.applications.EfficientNetB0(
        input_shape=input_shape, include_top=False, weights="imagenet"
    )
    base_model.trainable = False
    # Add custom layers
    global_pooling = tf.keras.layers.GlobalAveragePooling2D()
    # Output layer
    classification = tf.keras.layers.Dense(
        units,
        activation=activation,
        name="output"
    )

    y = tf.keras.Sequential(
        [
            preprocessing,
            data_augmentation,
            base_model,
            global_pooling,
            classification,
        ]
    )(x)

    model = tf.keras.Model(x, y)

    model.compile(
        loss=loss_fnc,
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        metrics=[metrics],
    )
    return model
```

{{% alert title="Tip" color="tip" %}}
You must log in to the [Viam app](https://app.viam.com/) to download the package containing the classification training script from the registry.
{{% /alert %}}

{{% /expand%}}
{{%expand "Step 4: Save the model artifact the script produces" %}}

You also need to include logic in your <file>training.py</file> to save the model artifact your training job produces to the `model_output_directory`.
For example:

```python {class="line-numbers linkable-line-numbers"}
# Save the model artifact to the Viam registry using the provided
# ML model name and version
def save_tflite_classification(
    model: Model,
    model_dir: str,
    model_name: str,
    target_shape: ty.Tuple[int, int, int],
) -> None:
    # Convert the model to tflite, with batch size 1
    # so the graph does not have dynamic-sized tensors.
    input = tf.keras.Input(target_shape, batch_size=1, dtype=tf.uint8)
    output = model(input, training=False)
    wrapped_model = tf.keras.Model(inputs=input, outputs=output)
    converter = tf.lite.TFLiteConverter.from_keras_model(wrapped_model)
    converter.target_spec.supported_ops = TFLITE_OPS
    tflite_model = converter.convert()

    filename = os.path.join(model_dir, f"{model_name}.tflite")
    with open(filename, "wb") as f:
        f.write(tflite_model)
```

When you submit a training job with this training script, this function saves the model outputs to the `model_output_directory` in the cloud.
Once the training job is complete, Viam looks at that directory and creates a package with all of the contents of the directory, creating or updating a registry item for the ML model.

{{% /expand%}}
{{%expand "Step 4: Write main function" %}}

Now, write all the code that runs the training job invoking the previously defined helper functions.
Write this into the top level code of <file>training.py</file>, which is executed when the file runs as a script.

For example, for the [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb) that trains a classification model using TensorFlow and Keras, `__main__` looks like this:

```python {class="line-numbers linkable-line-numbers"}
if __name__ == "__main__":
    DATA_JSON, MODEL_DIR = parse_args()
    # Set up compute device strategy. If GPUs are available, they will be used
    if len(tf.config.list_physical_devices("GPU")) > 0:
        strategy = tf.distribute.OneDeviceStrategy(device="/gpu:0")
    else:
        strategy = tf.distribute.OneDeviceStrategy(device="/cpu:0")

    IMG_SIZE = (256, 256)
    # Epochs and batch size can be adjusted according to the training job.
    EPOCHS = 2
    BATCH_SIZE = 16
    SHUFFLE_BUFFER_SIZE = 32
    AUTOTUNE = (
        tf.data.experimental.AUTOTUNE
    )  # Adapt preprocessing and prefetching dynamically

    # Model constants
    NUM_WORKERS = strategy.num_replicas_in_sync
    GLOBAL_BATCH_SIZE = BATCH_SIZE * NUM_WORKERS

    # Read dataset file, labels should be changed
    # according to the desired model output.
    LABELS = ["orange_triangle", "blue_star"]
    image_filenames, image_labels = parse_filenames_and_labels_from_json(
        DATA_JSON,
        LABELS
    )
    model_type = multi_label
    # Generate 80/20 split for train and test data
    train_dataset, test_dataset = create_dataset_classification(
        filenames=image_filenames,
        labels=image_labels,
        all_labels=LABELS,
        model_type=model_type,
        img_size=IMG_SIZE,
        train_split=0.8,
        batch_size=GLOBAL_BATCH_SIZE,
        shuffle_buffer_size=SHUFFLE_BUFFER_SIZE,
        num_parallel_calls=AUTOTUNE,
        prefetch_buffer_size=AUTOTUNE,
    )

    # Build and compile model
    with strategy.scope():
        model = build_and_compile_classification(
            LABELS, model_type, IMG_SIZE + (3,)
        )

    # Train model on data
    loss_history = model.fit(
            x=train_dataset, epochs=EPOCHS,
    )

    # Save labels.txt file
    save_labels(LABELS, MODEL_DIR)
    # Convert the model to tflite
    save_tflite_classification(
        model, MODEL_DIR, "classification_model", IMG_SIZE + (3,)
    )
```

{{% /expand%}}

### Package the training script as a <file>tar.gz</file> source distribution

You must save your training script in the `tar.gz` format to run in the Viam ML training service.
Follow the instructions to [create a <file>tar.gz</file> gzip'd tar file](https://docs.python.org/3.10/distutils/sourcedist) from your project.

{{% alert title="Tip" color="tip" %}}
You can refer to the directory structure of this [example classification training script](https://app.viam.com/packages/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb/custom-training-classification/ml_training/latest/e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb).
You must log in to the Viam app to download the package.
Unzip the package and see <file>model/training.py</file> for an example entrypoint file.
{{% /alert %}}

## Upload a new training script or new version

You must use the [Viam CLI](/cli/) to upload your training script to the Registry.

You can use the [`viam training-script upload`](/cli/#training-script) command to upload a new script.

For example:

```sh {class="line-numbers linkable-line-numbers"}
viam training-script upload --path=<path-to-tar.gz> --org-id=<INSERT ORG ID> --script-name="MyCustomTrainingScript"
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

```sh {class="line-numbers linkable-line-numbers"}
viam train submit custom from-registry --dataset-id=<INSERT DATASET ID> --org-id=<INSERT ORG ID> --model-name="MyRegistryModel" --model-version="2" --version="1" --path=<path-to-tar.gz> --script-name="MyCustomTrainingScript"
```

This command submits a training job to the previously uploaded `"MyCustomTrainingScript"` with another input dataset, which trains `"MyRegistryModel"` and publishes that to the registry.

{{% /tab %}}
{{% tab name="with-upload" %}}

```sh {class="line-numbers linkable-line-numbers"}
viam train submit custom with-upload --dataset-id=<INSERT DATASET ID> --model-org-id=<INSERT ORG ID> --model-name="MyRegistryModel" --model-type="single_label_classification" --model-version="2" --version="1" --path=<path-to-tar.gz> --script-name="MyCustomTrainingScript"
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

To update the visibility of a training script, use the CLI's [`viam training-script update`](/cli/#training-script) command and set the `--visibility` flag to `public` or `private`.

## Next steps

{{< cards >}}
{{% card link="/services/ml/deploy/" %}}
{{% card link="/services/vision/mlmodel/" %}}
{{% card link="/services/ml/edit/" %}}
{{< /cards >}}
