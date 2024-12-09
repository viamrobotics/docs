---
linkTitle: "Create a dataset"
title: "Create a dataset"
weight: 10
layout: "docs"
type: "docs"
no_list: true
description: "Create a dataset to train a machine learning model."
---

Collect images from your machine as it monitors its environment and add these images to a dataset.
By creating a dataset from your images, you can then train a machine learning model.
To ensure the model you create performs well, you need to train it on a variety of images that cover the range of things your machine should be able to recognize.

To capture image data from a machine, you will use the data management service.

{{% expand "Just testing and want a dataset to get started with? Click here." %}}

We have two datasets you can use for testing, one with shapes and the other with a wooden figure:

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:400px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-dataset.png" style="width:400px" alt="The datasets subtab of the data tab in the Viam app, showing a custom 'viam-figure' dataset of 25 images, most containing the wooden Viam figure" class="imgzoom fill aligncenter" resize="1400x" >}}

1. [Download the shapes dataset](https://storage.googleapis.com/docs-blog/dataset-shapes.zip) or [download the wooden figure dataset](https://storage.googleapis.com/docs-blog/dataset-figure.zip).
1. Unzip the download.
1. Open a terminal and go to the dataset folder.
1. Create a python script in the dataset's folder with the following contents:

   ```python {class="line-numbers linkable-line-numbers"}
   # Assumption: The dataset was exported using the `viam dataset export` command.
   # This script is being run from the `destination` directory.

   import asyncio
   import os
   import json
   import argparse

   from viam.rpc.dial import DialOptions, Credentials
   from viam.app.viam_client import ViamClient
   from viam.proto.app.data import BinaryID

   async def connect(args) -> ViamClient:
       dial_options = DialOptions(
           credentials=Credentials(
               type="api-key",
               payload=args.api_key,
           ),
           auth_entity=args.api_key_id
       )
       return await ViamClient.create_from_dial_options(dial_options)


   async def main():
       parser = argparse.ArgumentParser(
           description='Upload images, metadata, and tags to a new dataset')
       parser.add_argument('-org-id', dest='org_id', action='store',
                           required=True, help='Org Id')
       parser.add_argument('-api-key', dest='api_key', action='store',
                           required=True, help='API KEY with org admin access')
       parser.add_argument('-api-key-id', dest='api_key_id', action='store',
                           required=True, help='API KEY ID with org admin access')
       parser.add_argument('-machine-part-id', dest='machine_part_id',
                           action='store', required=True,
                           help='Machine part id for image metadata')
       parser.add_argument('-location-id', dest='location_id', action='store',
                           required=True, help='Location id for image metadata')
       parser.add_argument('-dataset-name', dest='dataset_name', action='store',
                           required=True,
                           help='Name of the data to create and upload to')
       args = parser.parse_args()


       # Make a ViamClient
       viam_client = await connect(args)
       # Instantiate a DataClient to run data client API methods on
       data_client = viam_client.data_client

       # Create dataset
       try:
           dataset_id = await data_client.create_dataset(
               name=args.dataset_name,
               organization_id=args.org_id
           )
           print("Created dataset: " + dataset_id)
       except Exception:
           print("Error. Check that the dataset name does not already exist.")
           print("See: https://app.viam.com/data/datasets")
           return 1

       file_ids = []

       for file_name in os.listdir("metadata/"):
           with open("metadata/" + file_name) as f:
               data = json.load(f)
               tags = None
               if "tags" in data["captureMetadata"].keys():
                   tags = data["captureMetadata"]["tags"]

               annotations = None
               if "annotations" in data.keys():
                   annotations = data["annotations"]

               image_file = data["fileName"]

               print("Uploading: " + image_file)

               id = await data_client.file_upload_from_path(
                   part_id=args.machine_part_id,
                   tags=tags,
                   filepath=os.path.join("data/", image_file)
               )
               print("FileID: " + id)

               binary_id = BinaryID(
                   file_id=id,
                   organization_id=args.org_id,
                   location_id=args.location_id
               )

               if annotations:
                   bboxes = annotations["bboxes"]
                   for box in bboxes:
                       await data_client.add_bounding_box_to_image_by_id(
                           binary_id=binary_id,
                           label=box["label"],
                           x_min_normalized=box["xMinNormalized"],
                           y_min_normalized=box["yMinNormalized"],
                           x_max_normalized=box["xMaxNormalized"],
                           y_max_normalized=box["yMaxNormalized"]
                       )

               file_ids.append(binary_id)

       await data_client.add_binary_data_to_dataset_by_ids(
           binary_ids=file_ids,
           dataset_id=dataset_id
       )
       print("Added files to dataset.")
       print("https://app.viam.com/data/datasets?id=" + dataset_id)

       viam_client.close()

   if __name__ == '__main__':
       asyncio.run(main())
   ```

1. Run the script to upload the images and their metadata into a dataset in Viam app providing the following input:

   ```sh {class="command-line" data-prompt="$" }
   python upload_data.py -org-id <ORG-ID> -api-key <API-KEY> \
      -api-key-id <API-KEY-ID> -machine-part-id <MACHINE-PART-ID> \
      -location-id <LOCATION-ID> -dataset-name <NAME>
   ```

1. Continue to [Train a tflite machine learning model](/data-ai/ai/train-tflite/).

{{% /expand%}}

{{< gif webm_src="/how-tos/capture-images.webm" mp4_src="/how-tos/capture-images.mp4" alt="Configuring data management for a camera in the viam app" max-width="600px" class="aligncenter" >}}

{{< table >}}
{{% tablestep link="/services/data/" %}}
**1. Enable the data management service**

In the configuration pane for your configured camera component, find the **Data capture** section.
Click **Add method**.

When the **Create a data management service** prompt appears, click it to add the service to your machine.
You can leave the default data manager settings.

{{% /tablestep %}}
{{% tablestep %}}
**2. Capture data**

With the data management service configured on your machine, configure how the camera component captures data:

In the **Data capture** panel of your camera's configuration, select `ReadImage` from the method selector.

Set your desired capture frequency.
For example, set it to `0.05` to capture an image every 20 seconds.

Set the MIME type to your desired image format, for example `image/jpeg`.

{{% /tablestep %}}
{{% tablestep %}}
**3. Save to start capturing**

Save the config.

With cloud sync enabled, your machine automatically uploads captured data to the Viam app after a short delay.

{{% /tablestep %}}
{{% tablestep %}}
**4. View data in the Viam app**

Click on the **...** menu of the camera component and click on **View captured data**.
This takes you to the data tab.

![View captured data option in the component menu](/get-started/quickstarts/collect-data/cam-capt-data.png)

If you do not see images from your camera, try waiting a minute and refreshing the page to allow time for the images to be captured and then synced to the app at the interval you configured.

If no data appears after the sync interval, check the **LOGS** tab for errors.

{{% /tablestep %}}
{{% tablestep %}}
**5. Capture a variety of data**

Your camera now saves images at the configured time interval.
When training machine learning models, it is important to supply a variety of images.
The dataset you create should represent the possible range of visual input.
This may include capturing images of different angles, different configurations of objects and different lighting conditions.
The more varied the provided dataset, the more accurate the resulting model becomes.

Capture at least 10 images of anything you want your machine to recognize.

{{< expand "For more tips and tricks on improving model accuracy, click here." >}}

- **More data means better models:** Incorporate as much data as you practically can to improve your model’s overall performance.
- **Include counterexamples:** Include images with and without the object you’re looking to classify.
  This helps the model distinguish the target object from the background and reduces the chances of false positives by teaching it what the object is not.
- **Avoid class imbalance:** Don’t train excessively on one specific type or class, make sure each category has a roughly equal number of images.
  For instance, if you're training a dog detector, include images of various dog breeds to avoid bias towards one breed.
  An imbalanced dataset can lead the model to favor one class over others, reducing its overall accuracy.
- **Match your training images to your intended use case:** Use images that reflect the quality and conditions of your production environment.
  For example, if you plan to use a low-quality camera in production, train with low-quality images.
  Similarly, if your model will run all day, capture images in both daylight and nighttime conditions.
- **Vary your angles and distances:** Include image examples from every angle and distance that the model will see in normal use.
- **Ensure labelling accuracy:** Make sure the labels or bounding box annotations you give are accurate.

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep %}}
**6. Label your images**

Once you have enough images, you can disable data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

Then use the interface on the [**DATA** tab](https://app.viam.com/data/view) to label your images.

Most use cases fall into one of two categories:

- Detecting certain objects and their location within an image.
  For example, you may wish to know where and how many `pizzas` there are in an image.
  In this case, add a label for each object you would like to detect.

{{< expand "For instructions to add labels, click here." >}}
To add a label, click on an image and select the **Bounding box** mode in the menu that opens.
Choose an existing label or create a new label.
Click on the image where you would like to add the bounding box and drag to where the bounding box should end.

{{<gif webm_src="/services/data/label-dog.webm" mp4_src="/services/data/label-dog.mp4" alt="Add a bounding box around the dog in an image">}}

To expand the image, click on the expand side menu arrow in the corner of the image:

{{<gif webm_src="/services/data/label-dog-big.webm" mp4_src="/services/data/label-dog-big.mp4" alt="Add a bounding box around the dog in an image in a big menu">}}

Repeat this with all images.

You can add one or more bounding boxes for objects in each image.
{{< /expand >}}

- Classifying an image as a whole.
  In other words, determining a descriptive state about an image.
  For example, you may wish to know whether an image of a food display is `full`, `empty`, or `average` or whether the quality of manufacturing output is `good` or `bad`.
  In this case, add tags to describe your images.

{{< expand "For instructions to add tags, click here." >}}
To tag an image, click on an image and select the **Image tags** mode in the menu that opens.
Add one or more tags to your image.

{{<gif webm_src="/services/data/tag-star.webm" mp4_src="/services/data/tag-star.mp4" alt="Tag image with a star label">}}

If you want to expand the image, click on the expand side menu arrow in the corner of the image.

Repeat this with all images.
{{< /expand >}}

{{% /tablestep %}}
{{% tablestep link="/fleet/dataset/" %}}
**7. Organize data into a dataset**

To train a model, your images must be in a dataset.

Use the interface on the **DATA** tab to add your labeled images to a dataset.

Also add any unlabelled images to your dataset.
Unlabelled images must not comprise more than 20% of your dataset.
If you have 25 images in your dataset, at least 20 of those must be labelled.

{{<gif webm_src="/tutorials/data-mlmodel/add-to-dataset.webm" mp4_src="/tutorials/data-mlmodel/add-to-dataset.mp4" alt="Click on an image you want to add to your dataset. In the actions pane, enter a dataset name under datasets, then press return." max-width="600px">}}

{{< expand "Want to add images to a dataset programmatically? Click here." >}}

You can also add all images with a certain label to a dataset using the [`viam dataset data add` command](/cli/#dataset) or the [Data Client API](/appendix/apis/data-client/#addtagstobinarydatabyfilter):

{{< tabs >}}
{{% tab name="CLI" %}}

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=<name>
viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
```

{{% /tab %}}
{{< tab name="Data Client API" >}}

You can run this script to add all images from your machine to a dataset:

```python {class="line-numbers linkable-line-numbers" data-line="14,18,30" }
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
            name="MyDataset",
            organization_id=ORG_ID
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

{{% /tab %}}
{{< /tabs >}}

{{% /expand%}}

{{% /tablestep %}}
{{< /table >}}
