---
linkTitle: "Quickstart"
title: "Quickstart"
weight: 10
layout: "docs"
type: "docs"
description: "Select and ready a machine for use with the Viam platform"
aliases:
  - /data/dataset/
  - /data-ai/ai/act/
  - /data-ai/ai/advanced/
  - /data-ai/ai/advanced/upload-external-data/
  - /data-ai/ai/alert/
  - /data-ai/ai/create-dataset/
  - /data-ai/ai/deploy/
  - /data-ai/ai/
  - /data-ai/ai/run-inference/
  - /data-ai/ai/train/
  - /data-ai/ai/train-tflite/
  - /data-ai/capture-data/advanced/advanced-data-capture-sync/
  - /data-ai/capture-data/advanced/how-sync-works/
  - /data-ai/capture-data/advanced/
  - /data-ai/capture-data/capture-sync/
  - /data-ai/capture-data/conditional-sync/
  - /data-ai/capture-data/filter-before-sync/
  - /data-ai/capture-data/fleet/data-management/
  - /data-ai/capture-data/
  - /data-ai/data/advanced/alert-data/
  - /data-ai/data/advanced/
  - /data-ai/data/export/
  - /data-ai/data/
  - /data-ai/data/query/
  - /data-ai/data/visualize/
  - /data-ai/reference/data-client/
  - /data-ai/reference/data-management-client/
  - /data-ai/reference/ml-model-client/
  - /data-ai/reference/ml-training-client/
  - /data-ai/reference/vision-client/
  - /fleet/dataset/
  - /manage/data/dataset/
  - /manage/data/label/
---

To ensure a machine learning model you create performs well, you need to train it on a variety of images that cover the range of things your machine should be able to recognize.

To train a model, you need a dataset that meets the following criteria:

- the dataset contains at least 15 images
- at least 80% of the images have labels
- for each selected label, at least 10 bounding boxes exist

This quickstart explains how to create a dataset that meets these criteria for your training purposes.

## Prerequisites

TODO flesh out

- machine
- Viam account

## Connect machine to the Viam app

{{% snippet "setup.md" %}}

## Add a camera to your machine

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

TODO CARDS

1. capture
1. annotate
1. train
