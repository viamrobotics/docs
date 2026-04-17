---
linkTitle: "Automate annotation"
title: "Automate annotation"
weight: 17
layout: "docs"
type: "docs"
description: "Use ML models to auto-label images and programmatically build annotated datasets."
date: "2025-01-30"
---

Manually labeling hundreds of images is slow. If you already have a trained ML
model -- even a rough first version -- you can use it to generate label
predictions automatically. You review and correct the predictions instead of
labeling from scratch.

You can also use the SDKs to annotate images programmatically, or combine
capture, annotation, and dataset management into a single script for continuous
dataset improvement.

## Auto-predict labels

Use an existing ML model to generate predictions for images in a dataset,
then review each prediction. This works with both classification models
(which generate tags) and object detection models (which generate bounding boxes).

1. Navigate to your [dataset's page](https://app.viam.com/datasets/).
1. Click **Get auto-predictions**.
1. **Select** a model to generate predictions with.
1. Set the **confidence threshold** above which to create a label prediction.
1. Click **Get predictions**.
1. Once predictions have finished generating, click **Review predictions**.
1. For each image, **Accept (A)** or **Reject (R)** each prediction.

## Programmatic tagging with SDKs

Use an ML model to generate tags for images, then pass the tags and image IDs
to the data client API.

{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/tag-images.snippet.tag-images.py" lang="python" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/tag-images.snippet.tag-images.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/tag-images.snippet.tag-images.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

## Programmatic bounding boxes with SDKs

Use an ML model to generate bounding boxes for images, then pass each bounding
box and image ID to the data client API.

{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/label-images.snippet.label-images.py" lang="python" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/label-images.snippet.label-images.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/label-images.snippet.label-images.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

## Capture, annotate, and add to dataset in one script

The following example captures an image, uses an ML model to generate
annotations, and adds the image to a dataset -- all in a single script. Use
this pattern to expand and improve your datasets continuously over time.
Check annotation accuracy in the **DATA** tab, then retrain your ML model on
the improved dataset.

{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/capture-annotate-dataset.snippet.capture-annotate-dataset.py" lang="python" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/capture-annotate-dataset.snippet.capture-annotate-dataset.go" lang="go" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/capture-annotate-dataset.snippet.capture-annotate-dataset.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="" >}}

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Train a model](/train/train-a-model/) -- use your labeled dataset to
  train a classification or object detection model.
