---
linkTitle: "Create a dataset"
title: "Create a dataset"
weight: 10
layout: "docs"
type: "docs"
description: "Create a dataset to train a machine learning model."
aliases:
  - /fleet/dataset/
  - /manage/data/label/
  - /manage/data/dataset/
  - /data/dataset/
---

To ensure a machine learning model you create performs well, you need to train it on a variety of images that cover the range of things your machine should be able to recognize.

To train a model, you need a dataset that meets the following criteria:

- the dataset contains at least 15 images
- at least 80% of the images have labels
- for each selected label, at least 10 bounding boxes exist

This page explains how to create a dataset that meets these criteria for your training purposes.

## Prerequisites

{{% expand "a machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "a camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

{{% /expand%}}

## Create a dataset

To create a dataset, use the CLI or the web UI:

{{< tabs >}}
{{% tab name="web UI" %}}

1. Open the [**DATASETS** tab on the **DATA** page](https://app.viam.com/data/datasets).

1. Click the **+ Create dataset** button.

   {{< imgproc src="/services/data/create-dataset.png" alt="The **DATASET** tab of the **DATA** page, showing the **+ Create dataset** button." resize="800x" style="width:500px" class="imgzoom" >}}

1. Enter a unique name for the dataset.

1. Click the **Create dataset** button to create the dataset.

{{% /tab %}}
{{% tab name="CLI" %}}

1. First, install the Viam CLI and authenticate:

   {{< readfile "/static/include/how-to/install-cli.md" >}}

1. [Log in to the CLI](/dev/tools/cli/#authenticate).

1. Run the following command to create a dataset, replacing the `<org-id>` and `<name>` placeholders with your organization ID and a unique name for the dataset:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset create --org-id=<org-id> --name=<name>
   ```

{{% /tab %}}
{{< /tabs >}}

## Capture images

{{< tabs >}}
{{% tab name="One image" %}}

You can add images to a dataset directly from a camera or vision component feed in the machine's **CONTROL** or **CONFIGURATION** tabs.

To add an image directly to a dataset from a visual feed, complete the following steps:

1. Open the **TEST** panel of any camera or vision service component to view a feed of images from the camera.
1. Click the button marked with the camera icon to save the currently displayed image to a dataset:
   {{< imgproc src="/components/camera/add_image_to_dataset_button.png" alt="A button marked with the outline of a camera, emphasized in red" resize="800x" style="width:500px" class="imgzoom" >}}
1. Select an existing dataset.
1. Click **Add** to add the image to the selected dataset.
1. When you see a success notification that reads "Saved image to dataset", you have successfully added the image to the dataset.

To view images added to your dataset, go to the **DATA** page's [**DATASETS** tab](https://app.viam.com/data/datasets) and select your dataset.

{{% /tab %}}
{{% tab name="Many images" %}}

To capture a large number of images for training an ML model, [Capture and sync image data](/data-ai/capture-data/capture-sync/) using the data management service with your camera.

Viam stores the images saved by capture and sync on the [**DATA** page](https://app.viam.com/data/), but does not add the images to a dataset.
We recommend you tag the images first and then use the CLI to [add the tagged images to a dataset](/data-ai/ai/create-dataset/#add-tagged-images-to-a-dataset).

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}
{{% /tab %}}
{{< /tabs >}}

Once you've captured enough images for training, you must annotate them to train a model.

## Annotate images

Use the interface on the [**DATA** page](https://app.viam.com/data/view) to annotate your images.
Always follow best practices when you label your images:

More data means better models

: Incorporate as much data as you practically can to improve your model's overall performance.

Include counterexamples

: Include images with and without the object you’re looking to classify.
This helps the model distinguish the target object from the background and reduces the chances of false positives by teaching the model what the object is _not_.

Avoid class imbalance

: Don't train excessively on one specific type or class, make sure each category has a roughly equal number of images.
For instance, if you're training a dog detector, include images of various dog breeds to avoid bias towards one breed.
An imbalanced dataset can lead the model to favor one class over others, reducing its overall accuracy.

Match training images to intended use case

: Use images that reflect the quality and conditions of your production environment.
For example, if you plan to use a low-quality camera in production, train with low-quality images.
Similarly, if your model will run all day, capture images in daylight, nighttime, dusk, and dawn conditions.

Vary angles and distances

: Include image examples from every angle and distance that you expect the model to handle.

Viam enables you to annotate images for the following machine learning methods:

{{< tabs >}}
{{% tab name="Classification" %}}

Classification determines a descriptive tag or set of tags for an image.
For example, classification could help you identify:

- whether an image of a food display appears `full`, `empty`, or `average`
- the quality of manufacturing output: `good` or `bad`
- what combination of toppings exists on a pizza: `pepperoni`, `sausage` and `pepper`, or `pineapple` and `ham` and `mushroom`

Viam supports single and multiple label classification.
To create a training set for classification, annotate tags to describe your images.

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-tortilla.webm" mp4_src="/services/data/tag-tortilla.mp4" alt="Tag image with a full label">}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="Object detection" %}}

Object detection identifies and determines the location of certain objects in an image.
For example, object detection could help you identify:

- how many `pizza` objects appear on a counter
- the number of `bicycle` and `pedestrian` objects on a greenway
- which `plant` objects are popular with `deer` in your garden

To create a training set for object detection, annotate bounding boxes to teach your model to identify objects that you want to detect in future images.

To label an object with a bounding box:

1. Click on an image, then click the **Annotate** button in right side menu.
1. Choose an existing label or create a new label.
1. Holding the command key (on macOS), or the control key (on Linux and Windows), click and drag on the image to create the bounding box:

   {{<gif webm_src="/services/data/label-magnemite.webm" mp4_src="/services/data/label-magnemite.mp4" alt="Add a bounding box around the magnemite pokemon in an image">}}

{{< alert title="Tip" color="tip" >}}

Once created, you can move, resize, or delete the bounding box.
{{< /alert >}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{< /tabs >}}

## Add tagged images to a dataset

{{< tabs >}}
{{% tab name="web UI" %}}

1. Open the [**DATA** page](https://app.viam.com/data/view).

1. Navigate to the **ALL DATA** tab.

1. Use the checkbox in the upper left of each image to select labeled images.

1. Click the **Add to dataset** button, select a dataset, and click the **Add ... images** button to add the selected images to the dataset.

{{% /tab %}}
{{% tab name="CLI" %}}

Use the Viam CLI to filter images by label and add the filtered images to a dataset:

1. First, [create a dataset](#create-a-dataset), if you haven't already.

1. If you just created a dataset, use the dataset ID output by the creation command.
   If your dataset already exists, run the following command to get a list of dataset names and corresponding IDs:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset list
   ```

1. Run the following [command](/dev/tools/cli/#dataset) to add all images labeled with a subset of tags to the dataset, replacing the `<dataset-id>` placeholder with the dataset ID output by the command in the previous step:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
   ```

{{% /tab %}}
{{% tab name="Data Client API" %}}

The following script adds all images captured from a certain machine to a new dataset. Complete the following steps to use the script:

1. Copy and paste the following code into a file named <file>add_images_from_machine_to_dataset.py</file> on your machine.

   ```python {class="line-numbers linkable-line-numbers" data-line="9-13" }
   import asyncio
   from typing import List, Optional

   from viam.rpc.dial import DialOptions, Credentials
   from viam.app.viam_client import ViamClient
   from viam.utils import create_filter

   # Configuration constants – replace with your actual values
   DATASET_NAME = "" # a unique, new name for the dataset you want to create
   ORG_ID = "" # your organization ID, find in your organization settings
   PART_ID = "" # id of machine that captured target images, find in machine config
   API_KEY = "" # API key, find or create in your organization settings
   API_KEY_ID = "" # API key ID, find or create in your organization settings

   # Adjust the maximum number of images to add to the dataset
   MAX_MATCHES = 500

   async def connect() -> ViamClient:
       """Establish a connection to the Viam client using API credentials."""
       dial_options = DialOptions(
           credentials=Credentials(
               type="api-key",
               payload=API_KEY,
           ),
           auth_entity=API_KEY_ID,
       )
       return await ViamClient.create_from_dial_options(dial_options)


   async def fetch_binary_data_ids(data_client, part_id: str) -> List[str]:
       """Fetch binary data metadata and return a list of BinaryData objects."""
       data_filter = create_filter(part_id=part_id)
       all_matches = []
       last: Optional[str] = None

       print("Getting data for part...")

       while len(all_matches) < MAX_MATCHES:
           print("Fetching more data...")
           data, _, last = await data_client.binary_data_by_filter(
               data_filter,
               limit=50,
               last=last,
               include_binary_data=False,
           )
           if not data:
               break
           all_matches.extend(data)

       return all_matches


   async def main() -> int:
       """Main execution function."""
       viam_client = await connect()
       data_client = viam_client.data_client

       matching_data = await fetch_binary_data_ids(data_client, PART_ID)

       print("Creating dataset...")

       try:
           dataset_id = await data_client.create_dataset(
               name=DATASET_NAME,
               organization_id=ORG_ID,
           )
           print(f"Created dataset: {dataset_id}")
       except Exception as e:
           print("Error creating dataset. It may already exist.")
           print("See: https://app.viam.com/data/datasets")
           print(f"Exception: {e}")
           return 1

       print("Adding data to dataset...")

       await data_client.add_binary_data_to_dataset_by_ids(
           binary_ids=[obj.metadata.binary_data_id for obj in matching_data],
           dataset_id=dataset_id
       )

       print("Added files to dataset.")
       print(f"See dataset: https://app.viam.com/data/datasets?id={dataset_id}")

       viam_client.close()
       return 0


   if __name__ == "__main__":
       asyncio.run(main())
   ```

1. Fill in the placeholders with values for your own organization, API key, machine, and dataset.

1. Install the [Viam Python SDK](https://python.viam.dev/) by running the following command:

   ```sh {class="command-line" data-prompt="$"}
   pip install viam-sdk
   ```

1. Finally, run the following command to add the images to the dataset:

   ```sh {class="command-line" data-prompt="$"}
   python add_images_from_machine_to_dataset.py
   ```

{{% /tab %}}
{{< /tabs >}}
