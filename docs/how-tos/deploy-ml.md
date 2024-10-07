---
title: "Train and deploy ML/computer vision models"
linkTitle: "Train and deploy computer vision models"
weight: 20
type: "docs"
tags: ["vision", "data", "services"]
images: ["/services/ml/train.svg"]
description: "Use your image data to create and label a dataset and train and deploy a computer vision ML model."
aliases:
  - /use-cases/deploy-ml/
  - /manage/ml/train-model/
  - /ml/train-model/
  - /services/ml/train-model/
  - "/tutorials/data-management-tutorial/"
  - "/tutorials/data-management/"
  - "/data-management/data-management-tutorial/"
  - "/tutorials/services/data-management-tutorial/"
  - /tutorials/services/data-mlmodel-tutorial/
  - /tutorials/projects/filtered-camera/
languages: []
viamresources: ["data_manager", "mlmodel", "vision"]
platformarea: ["ml", "data"]
emailform: true
level: "Beginner"
date: "2024-06-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You can use Viam's built-in tools to train a machine learning (ML) model on your images and then deploy computer vision on your machines.

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/how-tos/ml-vision-diagram.png)

You can use ML models to help your machines adapt their behavior to the world around them.

For example, you can train a model to recognize your dog and detect whether they are sitting or standing.
You could then use that knowledge to [give your dog treats](https://www.viam.com/post/smart-pet-feeder) or [capture images](/tutorials/configure/pet-photographer/) only when your dog is in the camera frame so you don't capture hundreds of photos of an empty room.

{{< alert title="In this page" color="tip" >}}

1. [Create a dataset and label data](#create-a-dataset-and-label-data)
1. [Train a machine learning (ML) model](#train-a-machine-learning-ml-model)
1. [Test your ML model](#test-your-ml-model)
1. [Deploy your ML model](#deploy-an-ml-model)

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A configured camera. Click to see instructions." %}}

First, connect the camera to your machine's computer if it's not already connected (like with an inbuilt webcam on a Macbook).

Then, navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a camera model](/components/camera/) that supports your camera.

If you are not sure what to use, start with a [webcam](/components/camera/webcam/) which supports most USB cameras and inbuilt laptop webcams.

{{% /expand%}}

{{% expand "No computer or webcam?" %}}
No problem.
You don't need to buy or own any hardware to complete this guide.

Use [Try Viam](https://app.viam.com/try) to borrow a rover free of cost online.
The rover already has `viam-server` installed and is configured with some components, including a webcam.

Once you have borrowed a rover, go to its **CONTROL** tab where you can view camera streams and also drive the rover.
You should have a front-facing camera and an overhead view of your rover.
Now you know what the rover can perceive.

To change what the front-facing camera is pointed at, find the **cam** camera panel on the **CONTROL** tab and click **Toggle picture-in-picture** so you can continue to view the camera stream.
Then, find the **viam_base** panel and drive the rover around.

Now that you have seen that the cameras on your Try Viam rover work, begin by [Creating a dataset and labeling data](#create-a-dataset-and-label-data).
You can drive the rover around as you capture data to get a variety of images from different angles.

{{< alert title="Tip" color="tip" >}}
Be aware that if you are running out of time during your rental, you can [extend your rover rental](/appendix/try-viam/reserve-a-rover/#extend-your-reservation) as long as there are no other reservations.
{{< /alert >}}

{{% /expand%}}

## Create a dataset and label data

Start by assembling the dataset to train your machine learning model on.

{{% expand "Just testing and want a dataset to get started with? Click here." %}}

We have two datasets you can use for testing, one with shapes and the other with a wooden figure:

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="max-width:400px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-dataset.png" style="max-width:400px" alt="The datasets subtab of the data tab in the Viam app, showing a custom 'viam-figure' dataset of 25 images, most containing the wooden Viam figure" class="imgzoom fill aligncenter" resize="1400x" >}}

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

1. Run the script to upload the data into a dataset in Viam app providing the following input:

   ```sh {class="command-line" data-prompt="$" }
   python upload_data.py -org-id <ORG-ID> -api-key <API-KEY> \
      -api-key-id <API-KEY-ID> -machine-part-id <MACHINE-PART-ID> \
      -location-id <LOCATION-ID> -dataset-name <NAME>
   ```

1. Continue to [Train a machine learning model](#train-a-machine-learning-ml-model).

{{% /expand%}}

{{< alert title="Tip" color="tip" >}}
For best results when training machine learning models:

- Provide at least 10 images of the same object, taken from different angles, and repeat this approach for each object you want your machine to be able to identify.
  Generally, the more different perspectives of a given object you tag, the more likely it is that your model will be able to identify it, even under differing conditions.
- Include some images that do not contain any of the objects you wish to identify, but do not add labels to these images.
  Unlabelled images must not comprise more than 20% of your dataset, so if you have 25 images in your dataset, at least 20 of those must be labelled.
- If you want your machine to operate successfully in various lighting conditions, such as changing sunlight, include images of each object from varying lighting conditions.

{{< /alert >}}

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/services/ml/collect.svg" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="Collect data">}}
**1. Collect images**

Start by collecting images from your cameras and syncing it to the Viam app.
See [Collect image data and sync it to the cloud](/how-tos/image-data/#collect-image-data-and-sync-it-to-the-cloud) for instructions.

When training machine learning models, it is important to supply a variety of different data about the subject in different situations, such as from different angles or in different lighting situations.
The more varied the provided data set, the more accurate the resulting model becomes.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/label.svg" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="Label data">}}
**2. Label your images**

Once you have enough images of the objects you'd like to identify captured and synced to the Viam app, use the interface on the [**DATA** tab](https://app.viam.com/data/view) to label your data.

You can label your images to create:

- **Detection models**: Draw **bounding boxes** around distinct objects within captured images.
  The trained model will enable your machine to be able to detect those objects on its own.
- **Classification models**: Add **tags** to each of your images with class labels that describe it.
  The trained model will enable your machine to classify similar images on its own.

<br>

{{< expand "Create image tags (for an image classifier)" >}}

You can use tags to create classification models for images.
For example, if you would like to create a model that identifies an image of a star in a set of images, tag each image containing a star with a `star` tag.
You also need images without the star tag or with another tag like `notstar`.

To tag an image, click on an image and select the **Image tags** mode in the menu that opens.
Add one or more tags to your image.

{{<gif webm_src="/services/data/tag-star.webm" mp4_src="/services/data/tag-star.mp4" alt="Tag image with a star label">}}

If you want to expand the image, click on the expand side menu arrow in the corner of the image.

Repeat this with all images.

{{< /expand >}}

{{< expand "Create bounding boxes (for an object detector)" >}}

You can create one or more bounding boxes for objects in each image.
For example, if you would like to create a model that detects a dog in an image, add bounding boxes around the dog in each of your images and add or select the label `dog`.

To add a bounding box, click on an image and select the **Bounding box** mode in the menu that opens.
Choose an existing label or create a new label.
Click on the image where you would like to add the bounding box and drag to where the bounding box should end.

{{<gif webm_src="/services/data/label-dog.webm" mp4_src="/services/data/label-dog.mp4" alt="Add a bounding box around the dog in an image">}}

To expand the image, click on the expand side menu arrow in the corner of the image:

{{<gif webm_src="/services/data/label-dog-big.webm" mp4_src="/services/data/label-dog-big.mp4" alt="Add a bounding box around the dog in an image in a big menu">}}

Repeat this with all images.
To see all the images that have bounding boxes, you can filter your dataset by selecting the label from the **Bounding box labels** dropdown in the **Filters** menu.

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep link="/services/data/dataset/" %}}
**3. Create a dataset**

A [dataset](/services/data/dataset/) allows you to conveniently view, work with, and train an ML model on a collection of images.

Use the interface on the **DATA** tab (or the [`viam dataset data add` command](/cli/#dataset)) to add all images you want to train the model on to a dataset.

Click on an image you want to train your ML model.
In the **Actions** pane on the right-hand side, enter a dataset name under **Datasets**, then press return.
Repeat this with all images you want to add to your dataset.

{{<gif webm_src="/tutorials/data-mlmodel/add-to-dataset.webm" mp4_src="/tutorials/data-mlmodel/add-to-dataset.mp4" alt="Add image to dataset" max-width="600px">}}

{{< expand "Want to do this programmatically? Click here." >}}

You can also add all data with a certain label to a dataset using the [`viam dataset data add` command](/cli/#dataset) or the [Data Client API](/appendix/apis/data-client/#addtagstobinarydatabyfilter):

{{< tabs >}}
{{% tab name="CLI" %}}

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=<name>
viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
```

{{% /tab %}}
{{< tab name="Data Client API" >}}

You can run this script to add all data from your machine to a dataset:

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

To remove an image from a dataset click on the **x** button next to the dataset name.

{{% /tablestep %}}
{{< /table >}}

## Train a machine learning (ML) model

{{< table >}}
{{% tablestep %}}
**1. Train an ML model**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train on.

Click **Train model** and follow the prompts.

Select to train a new model or update an existing model.
You can train or update using **Built-in training** or using a [training script](/services/ml/training-scripts/) from the Viam Registry.

Click **Next steps**.

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="max-width:500px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Select the details for your ML model**

- Enter a name or use the suggested name for your new model.
- For built-in training scripts, select a **Model Type**.
  Depending on the training script you've chose, you may have a number of these options:
  - **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
    Select this if you only have one label on each image. Ensure that the dataset you are training on also contains unlabeled images.
  - **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
  - **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.
- For built-in classification training, select the tags you want to train your model on from the **Labels** section. Unselected tags will be ignored, and will not be part of the resulting model.
- Click **Train model**.

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" style="max-width:500px" resize="1200x" class="imgzoom fill aligncenter" >}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Wait for your model to train**

The model now starts training and you can follow its process on the **DATA** page's [**TRAINING** tab](https://app.viam.com/training).

Once the model has finished training, it becomes visible on the **DATA** page's [**MODELS** tab](https://app.viam.com/data/models).

You will receive an email when your model finishes training.

{{% /tablestep %}}
{{% tablestep %}}
**4. Debug your training job**

From the **DATA** page's [**TRAINING** tab](https://app.viam.com/training), click on your training job's ID to see its logs.

{{< alert title="Note" color="note" >}}

Your training script may output logs at the error level but still succeed.

{{< /alert >}}

You can also view your training jobs' logs with the [`viam train logs`](/cli/#train) command.

{{% /tablestep %}}
{{< /table >}}

## Test your ML model

{{<gif webm_src="/services/vision/mug-classifier.webm" mp4_src="/services/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

Once your model has finished training, you can test it with images in the Viam app:

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) and click on the **Images** subtab.
2. Click on an image to open the side menu, and select the **Actions** tab.
3. In the **Run model** section, select your model and specify a confidence threshold.
4. Click **Run model**

If the results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

When satisfied that your ML model is working well, continue to [deploy an ML model](#deploy-an-ml-model).
If the vision service is not detecting or classifying reliably, you will need to adjust your ML model by consider adding and labelling more images in your dataset.

Ideally, you want your ML model to be able to identify objects with a high level of confidence, which is dependent on a robust training dataset.

## Deploy an ML model

To use an ML model on your machine, you need to deploy it to your machine using a compatible ML model service.
The ML model service will run the model and allow a vision service to use it:

{{< table >}}
{{% tablestep link="/services/ml/deploy/" %}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Train models">}}
**1. Deploy your ML model**

Navigate to the **CONFIGURE** tab of one of your machines in [the Viam app](https://app.viam.com).
Here, add an [ML model service](/services/ml/deploy/) that supports the ML model you just trained and add the model as the **Model**.
For example use the `TFLite CPU` ML model service for TFlite ML models.
This service will deploy and run the model.

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/" %}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure a service">}}
**2. Configure an <code>mlmodel</code> vision service**

The vision service takes the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

Click **Save** to save your changes.

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/#test-your-detector-or-classifier" %}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Deploy your model">}}
**3. Use your detector or classifier**

You can test your detector by clicking on the **Test** area of the vision service's configuration panel or from the [**CONTROL** tab](/fleet/control/).

The camera stream will show classification or detections when it identifies something, depending on your model.
Try placing an object your ML model can recognize in front of the camera.
If you are using a Viam rover, use the `viam_base` panel to move your rover, then click on the vision panel to check for classifications or detections.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" >}}
{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" >}}

{{% expand "Want to limit the number of shown classifications or detections? Click here." %}}

If you are seeing a lot of classifications or detections, you can set a minimum confidence threshold.

On the configuration page of the vision service in the top right corner, click **{}** (Switch to advanced).
Add the following JSON to the JSON configuration to set the `default_minimum_confidence` of the detector:

```json
"default_minimum_confidence": 0.82
```

The full configuration for the attributes of the vision service should resemble:

```json {class="line-numbers linkable-line-numbers" data-line="3"}
{
  "mlmodel_name": "mlmodel-1",
  "default_minimum_confidence": 0.82
}
```

This optional attribute reduces your output by filtering out classifications or detections below the threshold of 82% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration, then close and reopen the **Test** panel of the vision service configuration panel.
Now if you reopen the panel, you will only see classifications or detections with a confidence value higher than the `default_minimum_confidence` attribute.

For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/services/vision/mlmodel/).

{{% /expand%}}

You can also test your detector or classifier [with code](/services/vision/mlmodel/#existing-images-on-your-machine).

{{% /tablestep %}}

{{< /table >}}

## Versioning for deployed models

If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the machine.
If you do not want Viam to automatically deploy the `latest` version of the model, you can edit the `"packages"` array in the [JSON configuration](/configure/#the-configure-tab) of your machine.
This array is automatically created when you deploy the model and is not embedded in your service configuration.

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.
The model package config looks like this:

```json
"packages": [
  {
    "package": "<model_id>/<model_name>",
    "version": "YYYY-MM-DDThh-mm-ss",
    "name": "<model_name>",
    "type": "ml_model"
  }
]
```

<div id="emailform"></div>

## Next steps

To work with datasets programmatically, see the data API which includes several methods to work with datasets:

{{< cards >}}
{{% card link="/appendix/apis/data-client/" %}}
{{< /cards >}}

See the following tutorials for examples of using machine learning models to make your machine interact intelligently based on what it detects:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
