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

You can upload a custom training script to the [Viam registry](https://app.viam.com/registry/) to train your ML model.
Follow this guide to create, upload, and submit your Python script that loads a training dataset, trains an ML model, and produces a model artifact.

## Create a training script

You must save your training script in the `tar.gz` format to run in the Viam ML training service.
Create a Python source distribution `tar.gz` file that contains all of the training code for training your model:

1. Include an entrypoint file that contains the main logic at a predetermined location like <file>model/training.py</file>.
   This script must take as command line inputs a `dataset_file` and `model_output_directory` and output the model artifacts it generates to the `model_output_directory`.

- The `dataset_file` is a file containing the GCS blob paths and annotations associated with the dataset ID on which the user is training.
- The `model_output_directory` is the location where the user saves the model artifacts (the TFLite, PyTorch, TF, ONNX files) they produce from training.

  Parse these within your training script (see line 364).
  Then, read in the dataset and prepare the data for training, build and compile the model, train the model on the data, and save the model artifact to Google Container Storage (GCS).

  For example:

{{%expand "Click to view example training.py" %}}

```python {class="line-numbers linkable-line-numbers" data-line="364"}
import argparse
import json
import os
import typing as ty
import tensorflow as tf
from keras import Model, callbacks
import numpy as np

single_label = "MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION"
multi_label = "MODEL_TYPE_MULTI_LABEL_CLASSIFICATION"
metrics_filename = "model_metrics.json"
labels_filename = "labels.txt"

TFLITE_OPS = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS,  # enable TensorFlow ops.
]

TFLITE_OPTIMIZATIONS = [tf.lite.Optimize.DEFAULT]

ROUNDING_DIGITS = 5

# Normalization parameters are required when reprocessing the image.
_INPUT_NORM_MEAN = 127.5
_INPUT_NORM_STD = 127.5

# IMPORTANT: One of the following two helper functions must be included in your training script
#  depending on the type of model you're training.
#  This is used for parsing the dataset file produced and stored in Viam.

def parse_filenames_and_labels_from_json(filename: str, all_labels: ty.List[str]) -> ty.Tuple[ty.List[str], ty.List[str]]:
    """Load and parse the dataset JSON file to return image filenames and corresponding labels.
    Args:
        filename: JSONLines file containing filenames and labels
        model_type: either 'single_label' or 'multi_label'
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

def parse_filenames_and_bboxes_from_json(
    filename: str,
    all_labels: ty.List[str],
) -> ty.Tuple[ty.List[str], ty.List[str], ty.List[ty.List[float]]]:
    """Load and parse the dataset JSON file to return image filenames and corresponding labels with bboxes.
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
                    # Store coordinates in rel_yxyx format so that we can use the keras_cv function
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

def get_neural_network_params(
    num_classes: int, model_type: str
) -> ty.Tuple[str, str, str, str]:
    """Function that returns units and activation used for the last layer
        and loss function for the model, based on number of classes and model type.
    Args:
        labels: list of labels corresponding to images
        model_type: string single-label or multi-label for desired output
    """
    # Single-label Classification
    if model_type == single_label:
        units = num_classes
        activation = "softmax"
        loss = tf.keras.losses.categorical_crossentropy
        metrics = (
            tf.keras.metrics.CategoricalAccuracy(),
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall(),
        )
    # Multi-label Classification
    elif model_type == multi_label:
        units = num_classes
        activation = "sigmoid"
        loss = tf.keras.losses.binary_crossentropy
        metrics = (
            tf.keras.metrics.BinaryAccuracy(),
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall(),
        )
    return units, activation, loss, metrics

def preprocessing_layers_classification(
    img_size: ty.Tuple[int, int] = (256, 256)
) -> ty.Tuple[tf.Tensor, tf.Tensor]:
    """Preprocessing steps to apply to all images passed through the model.
    Args:
        img_size: optional 2D shape of image
    """
    preprocessing = tf.keras.Sequential(
        [
            tf.keras.layers.Resizing(
                img_size[0], img_size[1], crop_to_aspect_ratio=False
            ),
        ]
    )
    return preprocessing

def decode_image(image):
    """Decodes the image as an uint8 dense vector
    Args:
        image: the image file contents as a tensor
    """
    return tf.image.decode_image(
        image,
        channels=3,
        expand_animations=False,
        dtype=tf.dtypes.uint8,
    )

def check_type_and_decode_image(image_string_tensor):
    """Parse an image from gcs and decode it. Ungzip the image from gcs if zipped
    Args:
        image_string_tensor: the tensored form of an image gcs string
    """
    # Read an image from gcs
    image_string = tf.io.read_file(image_string_tensor)
    return decode_image(image_string)

def encoded_labels(
    image_labels: ty.List[str], all_labels: ty.List[str], model_type: str
) -> tf.Tensor:
    if model_type == single_label:
        encoder = tf.keras.layers.StringLookup(
            vocabulary=all_labels, num_oov_indices=0, output_mode="one_hot"
        )
    elif model_type == multi_label:
        encoder = tf.keras.layers.StringLookup(
            vocabulary=all_labels, num_oov_indices=0, output_mode="multi_hot"
        )
    return encoder(image_labels)

def parse_image_and_encode_labels(
    filename: str,
    labels: ty.List[str],
    all_labels: ty.List[str],
    model_type: str,
    img_size: ty.Tuple[int, int] = (256, 256),
) -> ty.Tuple[tf.Tensor, tf.Tensor]:
    """Returns a tuple of normalized image array and hot encoded labels array.
    Args:
        filename: string representing path to image
        labels: list of up to N_LABELS associated with image
        all_labels: list of all N_LABELS
        model_type: string single_label or multi_label
    """
    image_decoded = check_type_and_decode_image(filename)

    # Resize it to fixed shape
    image_resized = tf.image.resize(image_decoded, [img_size[0], img_size[1]])
    # Convert string labels to encoded labels
    labels_encoded = encoded_labels(labels, all_labels, model_type)
    return image_resized, labels_encoded


def create_dataset_classification(
    filenames: ty.List[str],
    labels: ty.List[str],
    all_labels: ty.List[str],
    model_type: str,
    img_size: ty.Tuple[int, int] = (256, 256),
    train_split: float = 0.8,
    batch_size: int = 64,
    shuffle_buffer_size: int = 1024,
    num_parallel_calls: int = tf.data.experimental.AUTOTUNE,
    prefetch_buffer_size: int = tf.data.experimental.AUTOTUNE,
) -> ty.Tuple[tf.data.Dataset, tf.data.Dataset]:
    """Load and parse dataset from Tensorflow datasets.
    Args:
        filenames: string list of image paths
        labels: list of string lists, where each string list contains up to N_LABEL labels associated with an image
        all_labels: string list of all N_LABELS
        model_type: string single_label or multi_label
    """
    # Create a first dataset of file paths and labels
    if model_type == single_label:
        dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
    else:
        dataset = tf.data.Dataset.from_tensor_slices(
            (filenames, tf.ragged.constant(labels))
        )

    def mapping_fnc(x, y):
        return parse_image_and_encode_labels(x, y, all_labels, model_type, img_size)

    # Parse and preprocess observations in parallel
    dataset = dataset.map(mapping_fnc, num_parallel_calls=num_parallel_calls)

    # Shuffle the data for each buffer size
    # Disabling reshuffling ensures items from the training and test set will not get shuffled into each other
    dataset = dataset.shuffle(
        buffer_size=shuffle_buffer_size, reshuffle_each_iteration=False
    )

    train_size = int(train_split * len(filenames))

    train_dataset = dataset.take(train_size)
    test_dataset = dataset.skip(train_size)

    # Batch the data for multiple steps
    # If the size of training data is smaller than the batch size,
    # batch the data to expand the dimensions by a length 1 axis.
    # This will ensure that the training data is valid model input
    train_batch_size = batch_size if batch_size < train_size else train_size
    if model_type == single_label:
        train_dataset = train_dataset.batch(train_batch_size)
    else:
        train_dataset = train_dataset.apply(
            tf.data.experimental.dense_to_ragged_batch(train_batch_size)
        )

    # Fetch batches in the background while the model is training.
    train_dataset = train_dataset.prefetch(buffer_size=prefetch_buffer_size)

    return train_dataset, test_dataset


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
    classification = tf.keras.layers.Dense(units, activation=activation, name="output")

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

def save_labels(labels: ty.List[str], model_dir: str) -> None:
    filename = os.path.join(model_dir, labels_filename)
    with open(filename, "w") as f:
        for label in labels[:-1]:
            f.write(label + "\n")
        f.write(labels[-1])

def get_rounded_number(val: tf.Tensor, rounding_digits: int) -> tf.Tensor:
    if np.isnan(val) or np.isinf(val):
        return -1
    else:
        return float(round(val, rounding_digits))

def save_model_metrics_classification(
    loss_history: callbacks.History,
    monitored_val: ty.List[str],
    model_dir: str,
    model: Model,
    test_dataset: tf.data.Dataset,
) -> None:
    test_images = np.array([x for x, _ in test_dataset])
    test_labels = np.array([y for _, y in test_dataset])

    test_metrics = model.evaluate(test_images, test_labels)

    metrics = {}
    # Since there could be potentially many occurences of the maximum value being monitored,
    # we reverse the list storing the tracked values and take the last occurence.
    monitored_metric_max_idx = len(monitored_val) - np.argmax(monitored_val[::-1]) - 1
    for i, key in enumerate(model.metrics_names):
        metrics["train_" + key] = get_rounded_number(
            loss_history.history[key][monitored_metric_max_idx], ROUNDING_DIGITS
        )
        metrics["test_" + key] = get_rounded_number(test_metrics[i], ROUNDING_DIGITS)

    # Save the loss and test metrics as model metrics
    filename = os.path.join(model_dir, metrics_filename)
    with open(filename, "w") as f:
        json.dump(metrics, f, ensure_ascii=False)

# IMPORTANT: You must include a helper function like the following for your framework type that allows you to save  the model artifact to Viam, which will be viewable as a registry item for the ML model name and version specified.

def save_tflite_classification(
    model: Model,
    model_dir: str,
    model_name: str,
    target_shape: ty.Tuple[int, int, int],
) -> None:
    # Convert the model to tflite, with batch size 1 so the graph does not have dynamic-sized tensors.
    input = tf.keras.Input(target_shape, batch_size=1, dtype=tf.uint8)
    output = model(input, training=False)
    wrapped_model = tf.keras.Model(inputs=input, outputs=output)
    converter = tf.lite.TFLiteConverter.from_keras_model(wrapped_model)
    converter.target_spec.supported_ops = TFLITE_OPS
    tflite_model = converter.convert()

    # Save the model to GCS
    filename = os.path.join(model_dir, f"{model_name}.tflite")
    with open(filename, "wb") as f:
        f.write(tflite_model)

if __name__ == "__main__":
    # This parses the required args for running the training script.
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", dest="data_json", type=str)
    parser.add_argument("--model_output_directory", dest="model_dir", type=str)
    args = parser.parse_args()
    MODEL_DIR = args.model_dir # Use the model directory for saving model artifacts associated with the model name and version.
    DATA_JSON = args.data_json # Use the data JSON filename to parse the images and their annotations for the specified dataset.

    # Set up compute device strategy
    if len(tf.config.list_physical_devices("GPU")) > 0:
        strategy = tf.distribute.OneDeviceStrategy(device="/gpu:0")
    else:
        strategy = tf.distribute.OneDeviceStrategy(device="/cpu:0")

    IMG_SIZE = (256, 256)
    EPOCHS = 1000
    BATCH_SIZE = 128
    SHUFFLE_BUFFER_SIZE = 1024
    AUTOTUNE = (
        tf.data.experimental.AUTOTUNE
    )  # Adapt preprocessing and prefetching dynamically

    # Model constants
    NUM_WORKERS = strategy.num_replicas_in_sync
    GLOBAL_BATCH_SIZE = BATCH_SIZE * NUM_WORKERS

    # Read dataset file
    LABELS = ["orange_triangle", "blue_star"]
    image_filenames, image_labels = parse_filenames_and_labels_from_json(DATA_JSON, LABELS)
    # Generate 80/20 split for train and test data
    train_dataset, test_dataset = create_dataset_classification(
        filenames=image_filenames,
        labels=image_labels,
        all_labels=LABELS,
        model_type=multi_label,
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
            LABELS, multi_label, IMG_SIZE + (3,)
        )

    # Get callbacks for training classification
    callbackEarlyStopping = tf.keras.callbacks.EarlyStopping(
    # Stop training when `monitor` value is no longer improving
    monitor="binary_accuracy",
        # "no longer improving" being defined as "no better than 'min_delta' less"
        min_delta=1e-3,
        # "no longer improving" being further defined as "for at least 'patience' epochs"
        patience=5,
        # Restore weights from the best performing model, requires keeping track of model weights and performance.
        restore_best_weights=True,
    )
    callbackReduceLROnPlateau = tf.keras.callbacks.ReduceLROnPlateau(
        # Reduce learning rate when `loss` is no longer improving
        monitor="loss",
        # "no longer improving" being defined as "no better than 'min_delta' less"
        min_delta=1e-3,
        # "no longer improving" being further defined as "for at least 'patience' epochs"
        patience=5,
        # Default lower bound on learning rate
        min_lr=0,
    )

    print(train_dataset)

    # Train model on data
    loss_history = model.fit(
            x=train_dataset, epochs=EPOCHS, callbacks=[callbackEarlyStopping, callbackReduceLROnPlateau]
    )
    # Get the values of what is being monitored in the early stopping policy,
    # since this is what is used to restore best weights for the resulting model.
    monitored_val = callbackEarlyStopping.get_monitor_value(
        loss_history.history
    )
    # Save trained model metrics to JSON file
    save_model_metrics_classification(
        loss_history,
        monitored_val,
        MODEL_DIR,
        model,
        test_dataset,
    )
    # Save labels.txt file
    save_labels(LABELS, MODEL_DIR)
    # Convert the model to tflite
    save_tflite_classification(
        model, MODEL_DIR, "beepboop", IMG_SIZE + (3,)
    )

```

{{% /expand%}}.

2. You must also include in your tarball a <file>setup.py</file> file with installation dependencies to install in the container that runs the training script.
   For example:

{{%expand "Click to view example setup.py" %}}

```json {class="line-numbers linkable-line-numbers"}
from setuptools import find_packages, setup

setup(
    name="training",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-cloud-aiplatform",
        "google-cloud-storage",
        "keras==2.11.0",
        "keras-cv==0.5.0",
        "Keras-Preprocessing==1.1.2",
        "tflite-support",
    ],
)
```

{{% /expand%}}

3. Follow the instructions to [create a `tar.gz` gzip'd tar file from your files](https://docs.python.org/3.10/distutils/sourcedist).

You can reference the directory structure of this [example classification training script](https://app.viam.dev/packages/0fbe951e-d4c6-427f-985f-784b7b85842c/manual_testing_byots_classification/ml_training/latest/0fbe951e-d4c6-427f-985f-784b7b85842c).

## Upload a new training script or new version

You must use the Viam CLI to upload your training script to the Registry.
You can use the [`viam training-script upload`](/cli/#training-script) command in the form `viam training-script upload --path=<path-to-tarball> --org-id=<your-org-id> --script-name=<name-for-script>` to upload a new script.
You can also simultaneously upload a training script and submit a training job with the [`viam train submit custom from-upload` command](/cli/#position-arguments-submit-custom).

Follow the instructions in the [CLI documentation](/cli/) to install the CLI and formulate these commands.

Once uploaded, you can view the script by navigating to the [registry's **Training Scripts** page](https://app.viam.com/registry?type=Training+Script).

### Update the visibility of a training script

To update the visibility of a training script, use the CLi's [`viam training-script update`](/cli/#training-script) command and set the `--visibility` flag to `public` or `private`.

## Submit a training job

You can use the Viam CLI's [`viam train submit`](/cli/#positional-arguments-submit) command to submit a training job.

Referencing the [CLI documentation](/cli/#positional-arguments-submit), use `viam train submit custom from-registry` to submit a training job from a training script already in the registry and `viam train submit custom from-upload` to upload a training script and submit a training job at the same time.

Once successfully submitted, view your training job in the **Training** section of the Viam app's **DATA** page's [**MODELS** tab](https://app.viam.com/data/models).
