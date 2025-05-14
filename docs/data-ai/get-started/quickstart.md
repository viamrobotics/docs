---
linkTitle: "Quickstart"
title: "Quickstart"
weight: 10
layout: "docs"
type: "docs"
description: "Select and ready a machine for use with the Viam platform"
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
