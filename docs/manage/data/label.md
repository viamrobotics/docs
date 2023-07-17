---
title: "Label Data"
linkTitle: "Label Data"
description: "Label image data on the DATA page in the Viam Cloud."
weight: 39
type: "docs"
tags: ["data management", "cloud", "sync"]
images: [ "/manage/data/label-dog.gif" ]
# SME: Tahiya Salam and Alexis Wei
---

To label data in a dataset, go to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.

On the **Images** subtab, you can filter available images, using the **Filtering** menu and select the attributes that match where, how, and when the data was collected.

{{< alert title="Info" color="info" >}}
Filtered datasets are views and not materialized.
That means the data you are viewing may change as you label and train on the dataset.
If the underlying data matching the filter changes because data is deleted or more data is added, the dataset will also change.
{{< /alert >}}

You can label you data with:

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

Repeat this with all images in your dataset.

To delete a tag, click the cross next to the corresponding label.

## Next Steps

{{< cards >}}
  {{% card link="/manage/ml/train-model/" %}}
  {{% card link="/tutorials/projects/pet-treat-dispenser/" %}}
{{< /cards >}}
