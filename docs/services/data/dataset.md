---
title: "Datasets"
linkTitle: "Datasets"
description: "Label data and create datasets for managing data and creating machine learning models."
weight: 30
type: "docs"
tags: ["data management", "cloud", "sync"]
imageAlt: "Label data and create datasets"
images: ["/services/data/label-dog.gif"]
videos: ["/services/data/label-dog.webm", "/services/data/label-dog.mp4"]
videoAlt: "Add a bounding box around the dog in an image."
aliases:
  - /manage/data/label/
  - /manage/data/dataset/
  - /data/dataset/
no_service: true
# SME: Tahiya Salam
---

A dataset is a grouping of images that you use to train machine learning models.
On the [**DATA** tab](https://app.viam.com/data/view) in the Viam app, you can create and manage datasets.

{{< alert title="Info" color="info" >}}
Filtered datasets are views and not materialized.
That means the data you are viewing may change as you label and train on the dataset.

Your dataset is also not versioned. If you train [ML models](/services/ml/ml-models/) on your dataset and the dataset changes existing models will not be affected but any new models you train will use the dataset with the data in it at the time of training.
{{< /alert >}}

## Labels

You label the images in your dataset with bounding boxes or image tags, depending on the type of model you intend to train:

- **Bounding boxes** are used to train [object detection models](/services/vision/#detections).
- **Image tags** are used to train [image classification models](/services/vision/#classifications).
  Tag names support alphanumeric characters, underscores, and hyphens.

## API

To interact with datasets programmatically, use the [data client API](/appendix/apis/data-client/), which supports the following methods for working with datasets:

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

## Sample dataset

If you are testing, you can use one of two provided sample dataset, one of shapes and the other of a wooden figure:

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" declaredimensions=true style="max-width:400px" alt="The shapes dataset." class="imgzoom fill aligncenter">}}

{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-dataset.png" style="max-width:400px" alt="The datasets subtab of the data tab in the Viam app, showing a custom 'viam-figure' dataset of 25 images, most containing the wooden Viam figure" class="imgzoom fill aligncenter" resize="1400x" >}}

1. [Download the shapes dataset](https://storage.googleapis.com/docs-blog/dataset-shapes.zip) or [download the wooden figure dataset](https://storage.googleapis.com/docs-blog/dataset-figure.zip).
1. Unzip the download.
1. Open a terminal and go to the dataset folder.
1. In it you will find a Python script to upload the data to the Viam app.
1. Open the script and fill in the constants at the top of the file.
1. Run the script to upload the data into a dataset in Viam app:

   ```sh {class="command-line" data-prompt="$" }
   python3 upload_data.py
   ```

## Next steps

The following how-to guide contains instructions on creating datasets as well as on how to train a model on a dataset:

{{< cards >}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< /cards >}}
