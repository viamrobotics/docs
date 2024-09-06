---
title: "How to train and deploy ML/computer vision models"
linkTitle: "Train computer vision models"
weight: 20
type: "docs"
tags: ["vision", "data", "services"]
images: ["/services/ml/train.svg"]
description: "Use your image data to create and label a dataset and train a computer vision ML model."
aliases:
  - /use-cases/deploy-ml/
  - /manage/ml/train-model/
  - /ml/train-model/
  - /services/ml/train-model/
  - "/tutorials/data-management-tutorial/"
  - "/tutorials/data-management/"
  - "/data-management/data-management-tutorial/"
  - "/tutorials/services/data-management-tutorial/"
languages: []
viamresources: ["data_manager", "mlmodel", "vision"]
level: "Beginner"
date: "2024-06-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You can use Viam's built-in tools to train a machine learning (ML) model on your images and then deploy computer vision on your machines.

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/how-tos/ml-vision-diagram.png)

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

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
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

1. [Download our shapes dataset](https://storage.googleapis.com/docs-blog/dataset-shapes.zip).
1. Unzip the download.
1. Open a terminal and go to the dataset folder.
1. In it you will find a Python script to upload the data to the Viam app.
1. Open the script and fill in the constants at the top of the file.
1. Run the script to upload the data into a dataset in Viam app:

   ```sh {class="command-line" data-prompt="$" }
   python3 upload_data.py
   ```

1. Continue to [Train a machine learning model](#train-a-machine-learning-ml-model).

{{% /expand%}}

{{< alert title="Tip" color="tip" >}}
For best results when training machine learning models:

- Provide at least 10 images of the same object, taken from different angles, and repeat this approach for each object you want your machine to be able to identify.
- Include some images that do not contain any of the objects you wish to identify, but do not tag these images.
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

Once you have enough images of the objects you'd like to classify, use the interface on the **DATA** tab to label your data.
If you want to train an image classifier, use image tags.
For an object detector, use bounding boxes.

<br>

{{< expand "Create image tags (for an image classifier)" >}}

You can use tags to create classification models for images.
For example, if you would like to create a model that identifies an image of a star in a set of images, tag each image containing a star with a `star` tag.
You also need images without the star tag or with another tag like `notstar`.

To tag an image, click on the image and select the **Image tags** mode in the menu that opens.

{{<gif webm_src="/services/data/tag-star.webm" mp4_src="/services/data/tag-star.mp4" alt="Tag image with a star label">}}

If you want to expand the image, click on the expand side menu arrow in the corner of the image.

Repeat this with all images in your dataset.

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

Repeat this with all images in your dataset.
To see all the images that have bounding boxes, you can filter your dataset by selecting the label from the **Bounding box labels** dropdown in the **Filters** menu.

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep link="/services/data/dataset/" %}}
**3. Create a dataset**

Use the interface on the **DATA** tab (or the [`viam data dataset add` command](/cli/#data)) to add all images you want to train the model on to a dataset.

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

The model now starts training and you can follow its process in the **Training** section of the **Models** page.

![The models tab on the data page showing a model named my-classifier-model being trained](/tutorials/data-management/model-training-progress.png)

Once the model has finished training, it becomes visible in the **Models** section of the page.
You will receive an email when your model finishes training.

![The trained model](/tutorials/data-management/trained-model.png)

{{% /tablestep %}}
{{% tablestep %}}
**4. Debug your training job**

If your training job failed you can check your job's logs with the [CLI](/cli/).

You can obtain the job's id by listing the jobs:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<INSERT ORG ID> --job-status=unspecified
```

Then use the job id to get your training job's logs:

```sh {class="command-line" data-prompt="$"}
viam train logs --job-id=<JOB ID>
```

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
If you are using a Viam rover, use the `viam_base` panel to move your rover, then click on the vision panel to check for classifications or detections.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="300x" >}}
{{< imgproc src="/tutorials/data-management/red-star.png" alt="Detected red star" resize="300x" >}}

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
