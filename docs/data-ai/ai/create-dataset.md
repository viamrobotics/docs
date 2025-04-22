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

{{% expand "A machine connected to the Viam app" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or another [camera component](/operate/reference/components/camera/), if you haven't already.

{{% /expand%}}

## Capture images

{{< tabs >}}
{{% tab name="Capture individual images directly into a dataset" %}}

You can add images to a dataset directly from a camera or vision component feed in the **CONTROL** or **CONFIGURATION** tabs of the Viam app.
This technique can help you create a dataset without filling the **DATA** tab with a large number of unhelpful empty images.

To add an image directly to a dataset from a visual feed, complete the following steps:

1. Open the **TEST** panel of any camera or vision service component to view a feed of images from the camera.
1. Click the button marked with the camera icon to save the currently displayed image to a dataset:
   {{< imgproc src="/components/camera/add_image_to_dataset_button.png" alt="A button marked with the outline of a camera, emphasized in red" resize="800x" style="width:500px" class="imgzoom" >}}
1. Select an existing dataset.
1. Click **Add** to add the image to the selected dataset.
1. When you see a success notification that reads "Saved image to dataset", you have successfully added the image to the dataset.

To view images added to your dataset, go to the **DATA** page's [**DATASETS** tab](https://app.viam.com/data/datasets) in the Viam app.
Select the dataset to view the images within that dataset.

{{< alert title="Tip" color="tip" >}}

Use this technique to manually add tricky images where your first model version fails to your training dataset.
Annotate the tricky images, then train a new version of your model to improve your model.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Capture bulk images" %}}

To capture a large number of images for training your ML models, [Capture and sync image data](/data-ai/capture-data/capture-sync/) using the data management service with your camera.

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}
{{% /tab %}}
{{< /tabs >}}

## Annotate images

Use the interface on the [**DATA** tab](https://app.viam.com/data/view) to label your images. Always follow best practices when you label your images:

- **More data means better models:** Incorporate as much data as you practically can to improve your model's overall performance.
- **Include counterexamples:** Include images with and without the object you’re looking to classify.
  This helps the model distinguish the target object from the background and reduces the chances of false positives by teaching the model what the object is _not_.
- **Avoid class imbalance:** Don't train excessively on one specific type or class, make sure each category has a roughly equal number of images.
  For instance, if you're training a dog detector, include images of various dog breeds to avoid bias towards one breed.
  An imbalanced dataset can lead the model to favor one class over others, reducing its overall accuracy.
- **Match your training images to your intended use case:** Use images that reflect the quality and conditions of your production environment.
  For example, if you plan to use a low-quality camera in production, train with low-quality images.
  Similarly, if your model will run all day, capture images in both daylight and nighttime conditions.
- **Vary your angles and distances:** Include image examples from every angle and distance that you expect the model to handle.
- **Ensure labeling accuracy:** Make sure the labels or bounding box annotations you give are accurate.

Viam supports the following machine learning training approaches:

### Tag images for classification

Classification determines a descriptive tag or set of tags for an image.
For example, classification could help you identify:

- whether an image of a food display appears `full`, `empty`, or `average`
- the quality of manufacturing output: `good` or `bad`
- what combination of toppings exists on a pizza: `pepperoni`, `sausage` and `pepper`, or `pineapple` and `ham` and `mushroom`

Viam supports single and multiple label classification.
To create a training set for classification, add tags to describe your images.

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-tortilla.webm" mp4_src="/services/data/tag-tortilla.mp4" alt="Tag image with a full label">}}

Repeat these steps for all images in the dataset.

### Label bounding boxes for object detection

Object detection identifies and determines the location of certain objects in an image.
For example, object detection could help you identify:

- how many `pizza` objects appear on a counter
- the number of `bicycle` and `pedestrian` objects on a greenway
- which `plant` objects are popular with `deer` in your garden

To create a training set for object detection, add bounding boxes to teach your model to identify objects that you want to detect in future images.

To label an object with a bounding box:

1. Click on an image, then click the **Annotate** button in right side menu.
1. Choose an existing label or create a new label.
1. Holding the command key (on macOS), or the control key (on Linux and Windows), click and drag on the image to create the bounding box:

   {{<gif webm_src="/services/data/label-magnemite.webm" mp4_src="/services/data/label-magnemite.mp4" alt="Add a bounding box around the magnemite pokemon in an image">}}

{{< alert title="Tip" color="tip" >}}

Once created, you can move, resize, or delete the bounding box.
{{< /alert >}}

Repeat these steps for all images in the dataset.

## Add tagged images to a dataset

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Open the **DATA** page of the Viam app.

1. Navigate to the **ALL DATA** tab.

1. Use the checkbox in the upper left of each image to select labeled images.

1. Click the **Add to dataset** button, select a dataset, and click the **Add ... images** button to add the selected images to the dataset.

{{% /tab %}}
{{% tab name="CLI" %}}

Use the Viam CLI to filter images by label and add the filtered images to a dataset:

1. First, run the following command to create a dataset, if you haven't already:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset create --org-id=<org-id> --name=<dataset-name>
   ```

   This command will output a dataset ID.
   Pass this dataset ID in the next step to add images to this dataset.

1. Run the following [command](/dev/tools/cli/#dataset) to add all images labeled with a subset of tags to the dataset, replacing the `<dataset-id>` placeholder with the dataset ID output by the command in the previous step:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
   ```

{{% /tab %}}
{{% tab name="Data Client API" %}}

The following script adds all images captured from a certain machine to a new dataset. Complete the following steps to use the script:

1. Copy and paste the following code into a file named <file>add_images_from_machine_to_dataset.py</file> on your machine.

   ```python {class="line-numbers linkable-line-numbers" data-line="14,18,30,54-55" }
   import asyncio

   from viam.rpc.dial import DialOptions, Credentials
   from viam.app.viam_client import ViamClient
   from viam.utils import create_filter
   from viam.proto.app.data import BinaryID


   async def connect() -> ViamClient:
       dial_options = DialOptions(
         credentials=Credentials(
           type="api-key",
           # Replace "<API-KEY>" (including brackets) with your machine's API key
           payload='<API-KEY>',
         ),
         # Replace "<API-KEY-ID>" (including brackets) with your machine's
         # API key ID
         auth_entity='<API-KEY-ID>'
       )
       return await ViamClient.create_from_dial_options(dial_options)


   async def main():
       # Make a ViamClient
       viam_client = await connect()
       # Instantiate a DataClient to run data client API methods on
       data_client = viam_client.data_client

       # Replace "<PART-ID>" (including brackets) with your machine's part id
       my_filter = create_filter(part_id="<PART-ID>")

       print("Getting data for part...")
       binary_metadata, _, _ = await data_client.binary_data_by_filter(
           my_filter,
           include_binary_data=False
       )
       my_binary_ids = []

       for obj in binary_metadata:
           my_binary_ids.append(
               BinaryID(
                   file_id=obj.metadata.id,
                   organization_id=obj.metadata.capture_metadata.organization_id,
                   location_id=obj.metadata.capture_metadata.location_id
                   )
               )
       print("Creating dataset...")
       # Create dataset
       try:
           dataset_id = await data_client.create_dataset(
               # Replace "<ORG-ID>" (including brackets) with your organization id
               # Replace "<MY-DATASET> (including brackets) with the name of the new
               # dataset that you want to add your images to
               name="<MY-DATASET>",
               organization_id="<ORG-ID>"
           )
           print("Created dataset: " + dataset_id)
       except Exception:
           print("Error. Check that the dataset name does not already exist.")
           print("See: https://app.viam.com/data/datasets")
           return 1

       print("Adding data to dataset...")
       await data_client.add_binary_data_to_dataset_by_ids(
           binary_ids=my_binary_ids,
           dataset_id=dataset_id
       )
       print("Added files to dataset.")
       print("See dataset: https://app.viam.com/data/datasets?id=" + dataset_id)

       viam_client.close()

   if __name__ == '__main__':
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
