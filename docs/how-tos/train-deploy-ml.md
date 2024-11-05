---
title: "Train and deploy computer vision models"
linkTitle: "Train and deploy computer vision models"
weight: 20
type: "docs"
tags: ["vision", "data", "services"]
images: ["/services/ml/train.svg"]
description: "Use your image data to train a model, so your machines can make inferences about their environments."
aliases:
  - /use-cases/deploy-ml/
  - /manage/ml/train-model/
  - /ml/train-model/
  - /services/ml/train-model/
  - /tutorials/data-management-tutorial/
  - /tutorials/data-management/
  - /data-management/data-management-tutorial/
  - /tutorials/services/data-management-tutorial/
  - /tutorials/services/data-mlmodel-tutorial/
  - /tutorials/projects/filtered-camera/
  - /how-tos/deploy-ml/
languages: []
viamresources: ["data_manager", "mlmodel", "vision"]
platformarea: ["ml"]
emailform: true
level: "Beginner"
date: "2024-06-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

Many machines have cameras through which they can monitor their environment.
With machine leaning, you can train models on patterns within that visual data.
You can collect data from the camera stream and label any patterns within the images.

If a camera is pointed at a food display, for example, you can label the image of the display with `full` or `empty`, or label items such as individual `pizza_slice`s.

Using a model trained on such images, machines can make inferences about their environments.
Your machines can then automatically trigger alerts or perform other actions.
If a food display is empty, the machine could, for example, alert a supervisor to restock the display.

Common use cases for this are **quality assurance** and **health and safety** applications.

{{< alert title="In this page" color="tip" >}}

1. [Create a dataset with labeled data](#create-a-dataset-and-label-data)
1. [Train a machine learning (ML) model](#train-a-machine-learning-ml-model)
1. [Test your ML model](#test-your-ml-model)
1. [Deploy your ML model](#deploy-an-ml-model)

{{< /alert >}}

![Diagram of the camera component to data management service to ML model service to vision service pipeline.](/how-tos/ml-vision-diagram.png)

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A configured camera. Click to see instructions." %}}

First, connect the camera to your machine's computer if it's not already connected (like with an inbuilt laptop webcam).

Then, navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
The `webcam` model supports most USB cameras and inbuilt laptop webcams.
You can find additional camera models in the [camera configuration](/components/camera/#configuration) documentation.

Complete the camera configuration and use the **TEST** panel in the configuration card to test that the camera is working.

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

You will start by collecting images from your machine as it monitors its environment and add these images to a dataset.
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

1. Continue to [Train a machine learning model](#train-a-machine-learning-ml-model).

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
This may include capturing images of different angles, different configurations of objects and different lighting conditions
The more varied the provided dataset, the more accurate the resulting model becomes.

Capture at least 10 images of anything you want your machine to recognize.

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

## Train a machine learning (ML) model

Now that you have a dataset with your labeled images, you are ready to train a machine learning model.

{{< table >}}
{{% tablestep %}}
**1. Train an ML model**

In the Viam app, navigate to your list of [**DATASETS**](https://app.viam.com/data/datasets) and select the one you want to train on.

Click **Train model** and follow the prompts.

You can train your model using **Built-in training** or using a [training script](/registry/training-scripts/) from the Viam Registry.

Click **Next steps**.

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="width:500px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Fill in the details for your ML model**

Enter a name for your new model.

For built-in trainings, select a **Task Type**:

- **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
  Select this if you only have one label on each image. Ensure that the dataset you are training on also contains unlabeled images.
- **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
- **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.

Select the labels you want to train your model on from the **Labels** section. Unselected labels will be ignored, and will not be part of the resulting model.

Click **Train model**.

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" style="width:500px" resize="1200x" class="imgzoom fill aligncenter" >}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Wait for your model to train**

The model now starts training and you can follow its process on the [**TRAINING** tab](https://app.viam.com/training).

Once the model has finished training, it becomes visible on the [**MODELS** tab](https://app.viam.com/data/models).

You will receive an email when your model finishes training.

{{% /tablestep %}}
{{% tablestep %}}
**4. Debug your training job**

From the [**TRAINING** tab](https://app.viam.com/training), click on your training job's ID to see its logs.

{{< alert title="Note" color="note" >}}

Your training script may output logs at the error level but still succeed.

{{< /alert >}}

You can also view your training jobs' logs with the [`viam train logs`](/cli/#train) command.

{{% /tablestep %}}
{{< /table >}}

## Test your ML model

{{<gif webm_src="/services/vision/mug-classifier.webm" mp4_src="/services/vision/mug-classifier.mp4" alt="A classification model run against an image containing a mug." max-width="250px" class="alignright">}}

Once your model has finished training, you can test it.

Ideally, you want your ML model to be able to work with a high level of confidence.
As you test it, if you notice faulty predictions or confidence scores, you will need adjust your dataset and retrain your model.

If you trained a classification model, you can test it with the following instructions.
If you trained a detection model, skip to [deploy an ML model](#deploy-an-ml-model).

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) and click on the **Images** subtab.
1. Click on an image to open the side menu, and select the **Actions** tab.
1. In the **Run model** section, select your model and specify a confidence threshold.
1. Click **Run model**

If the results exceed the confidence threshold, the **Run model** section shows a label and the responding confidence threshold.

## Deploy an ML model

You have your trained model.
Now you can deploy it to your machines and make live inferences.

To use an ML model on your machine, you need to deploy the model with an ML model service.
The ML model service will run the model.

On its own the ML model service only runs the model.
To use it to make inferences on a camera stream, you need to use it alongside a vision service.

{{< table >}}
{{% tablestep link="/services/ml/" %}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Train models">}}
**1. Deploy your ML model**

Navigate to the **CONFIGURE** tab of one of your machine in the [Viam app](https://app.viam.com).
Add an ML model service that supports the ML model you just trained and add the model as the **Model**.
For example use the `ML model / TFLite CPU` service for TFlite ML models.
If you used the built-in training, this is the ML model service you need to use.
If you used a custom training script, you may need a different [ML model service](/services/ml/).

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/" %}}
{{<imgproc src="/services/icons/vision.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Configure a service">}}
**2. Configure an <code>mlmodel</code> vision service**

The ML model service deploys and runs the model.

The vision service works with the ML model services.
It uses the ML model and applies it to the stream of images from your camera.

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured in the last step (for example, `mlmodel-1`).

**Save** your changes.

{{% /tablestep %}}
{{% tablestep link="/services/vision/mlmodel/#test-your-detector-or-classifier" %}}
{{<imgproc src="/services/ml/deploy.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Deploy your model">}}
**3. Use your vision service**

You can test your vision service by clicking on the **Test** area of its configuration panel or from the [**CONTROL** tab](/fleet/control/).

The camera stream shows when the vision service identifies something.
Try pointing the camera at a scene similar to your training data.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" >}}
{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" >}}

{{% expand "Want to limit the number of shown classifications or detections? Click here." %}}

If you are seeing a lot of classifications or detections, you can set a minimum confidence threshold.

Start by setting the value to 0.8.
This reduces your output by filtering out anything below a threshold of 80% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration, then close and reopen the **Test** panel of the vision service configuration panel.
Now if you reopen the panel, you will only see classifications or detections with a confidence value higher than the `default_minimum_confidence` attribute.

For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/services/vision/mlmodel/).

{{% /expand%}}

{{% /tablestep %}}

{{< /table >}}

<div id="emailform"></div>

## Next steps

Now your machine can make inferences about its environment. The next step is to act based on these inferences:

- Perform actions: You can use the [vision service API](/appendix/apis/services/vision/) to get information about your machine's inferences and program behavior based on that.
- Webhooks: You can use triggers to send webhooks when certain inferences are made. For an example of this, see the [Helmer Monitoring tutorial](/tutorials/projects/helmet/)

See the following tutorials for examples of using machine learning models to make your machine do thinks based on its inferences about its environment:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{< /cards >}}
