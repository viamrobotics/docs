---
title: "Label data and create datasets"
linkTitle: "Create Datasets"
description: "Label data and create datasets for managing data and creating machine learning models."
weight: 39
type: "docs"
tags: ["data management", "cloud", "sync"]
images: ["/manage/data/label-dog.gif"]
aliases:
  - "/manage/data/label"
# SME: Tahiya Salam and Alexa Greenberg
---

To manage your data you can use labels and datasets.

## Label data

To label data, go to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.

On the **Images** subtab, you can filter available images, using the **Filtering** menu and select the attributes that match where, how, and when the data was collected.

{{< alert title="Info" color="info" >}}
Filtered datasets are views and not materialized.
That means the data you are viewing may change as you label and train on the dataset.
If the underlying data matching the filter changes because data is deleted or more data is added, the dataset will also change.
{{< /alert >}}

You can label your data with:

- [Bounding boxes](#bounding-boxes), which you can use to [train object detection models](/manage/ml/train-model/#train-a-model).
- [Image tags](#image-tags), which you can use to [image classification models](/manage/ml/train-model/#train-a-model).

### Bounding boxes

You can create one or more bounding boxes for objects in each image.
If you annotate an entire dataset, you can use these bounding boxes to [create object detection models](/manage/ml/train-model/#train-a-model).
For example, if you would like to create a model that detects a dog in an image, add bounding boxes around the dog in each of your images and add or select the label `dog`.

To add a bounding box, click on the image you want to add the bounding box to.
More information about the image will open up to the right side.
Select the **Bounding Box** option.
Choose an existing label or create a new label.
Click on the image where you would like to add the bounding box and drag to where the bounding box should end.

{{<gif webm_src="/manage/data/label-dog.webm" mp4_src="/manage/data/label-dog.mp4" alt="Add a bounding box around the dog in an image">}}

If you want to expand the image, click on the expand side menu arrow in the corner of the image:

{{<gif webm_src="/manage/data/label-dog-big.webm" mp4_src="/manage/data/label-dog-big.mp4" alt="Add a bounding box around the dog in an image in a big menu">}}

Repeat this with all images in your dataset.
To see all the images that have bounding boxes, you can filter your dataset by selecting the label from the **Bounding box labels** dropdown in the **Filtering** menu.

To delete a bounding box, click the cross next to the corresponding label.

### Image Tags

You can use tags to [create classification models](../../ml/train-model/#train-a-model) for images.
For example, if you would like to create a model that identifies an image of a star in a set of images, tag each image containing a star with a `star` tag.
The filter also needs to include images without the star tag or with another tag like `notstar`.
If you add a `notstar` tag, you can filter the data in your dataset by selecting `star` and `notstar` from the **Tags** dropdown in the **Filtering** menu.
Alternatively you can use date ranges to filter for relevant data.

To tag an image, click on the image.
More information about the image will open up to the right side.
Select the **Image Tags** option.

{{<gif webm_src="/manage/data/tag-star.webm" mp4_src="/manage/data/tag-star.mp4" alt="Tag image with a star label">}}

If you want to expand the image, click on the expand side menu arrow in the corner of the image.

Repeat this with all images in your dataset.

To delete a tag, click the cross next to the corresponding label.

## Datasets

{{< alert title="Support" color="info" >}}
Datasets currently only work for images.
{{< /alert >}}

### Create a dataset

To create a dataset, go to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.

On the [**DATASETS** subtab](https://app.viam.com/data/datasets), click **Create dataset**, enter a name for your dataset and click **Create dataset** again.

![Create dataset UI](/manage/data/create-dataset.png)

You can also create a dataset when viewing image data from the Datasets dropdown.

{{<gif webm_src="/manage/data/add-to-dataset.webm" mp4_src="/manage/data/add-to-dataset.mp4" alt="Add image to dataset">}}

### Add or remove data from a dataset

To add or remove data from a dataset, go to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.

On the **Images** subtab, you can filter available images, using the **Filtering** menu and select the attributes that match where, how, and when the data was collected.

To add an image to a dataset, click on the image and select the dataset in the Datasets dropdown.
You can select an existing dataset or create a new one from this dropdown.

{{<gif webm_src="/manage/data/add-to-dataset.webm" mp4_src="/manage/data/add-to-dataset.mp4" alt="Add image to dataset">}}

To remove an image from a dataset click on the delete button next to the dataset.

{{<gif webm_src="/manage/data/delete-from-dataset.webm" mp4_src="/manage/data/delete-from-dataset.mp4" alt="Remove from dataset">}}

### View the data in a dataset

Once you have added data to your dataset, you can view the data in your dataset by clicking on your dataset's name on the image sidebar or on the [**DATASETS** subtab](https://app.viam.com/data/datasets).

You can click on any image in the dataset and use its appearing menu in order to add or remove bounding box labels or tags, or remove that image from the dataset.

### Train a model on a dataset

To train a model on a dataset, see [Train a model](/manage/ml/train-model/).

### Delete a dataset

To delete a dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets), right click on the dataset and click on the **Delete** button that appears.

## Next Steps

{{< cards >}}
{{% card link="/manage/ml/train-model/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" %}}
{{< /cards >}}
