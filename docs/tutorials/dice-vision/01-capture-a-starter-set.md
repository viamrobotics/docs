---
title: "Phase 1: Capture a starter set from your webcam"
linkTitle: "1. Capture a starter set"
weight: 10
type: "docs"
layout: "docs"
slug: "capture-a-starter-set"
description: "Configure a webcam on your machine and add 30 images of dice to a starter dataset from the camera's control card."
capabilities: ["hw-camera", "datasets"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 1
phase_total: 10
time_estimate: "20 minutes"
prev: "/tutorials/dice-vision/"
next: "/tutorials/dice-vision/label-the-starter-set/"
toc_hide: true
---

At the end of this phase, your webcam streams in the `camera` card's **TEST** section and a dataset named `dice-starter` holds about 30 images of dice.
You start small on purpose.
In the next two phases you label these 30 images by hand and train a rough starter model on them, which then labels the rest of your images for you.

## Set up your workspace {#set-up-your-workspace}

The camera doesn't need to point straight down, but keep it at the same height and angle for the whole workshop, except where [Phase 7](/tutorials/dice-vision/build-the-test-datasets/) asks you to move it.
A model learns what dice look like from the distance and angle you train it on, so moving the camera changes what it sees.
A steep angle, closer to straight down, makes the top face of each die easier to read, for you and the model.

1. Put a plain background to roll on, such as a dice tray or a sheet of plain paper, on a table with even light.
1. Mount the webcam about 30 cm above the background, aimed at it.
1. Plug the webcam into your computer.

{{< imgproc src="/tutorials/dice-vision/hero-yahtzee-roll.jpg" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="A webcam clipped to the top of a purple post on a white desk, with dice rolled out on the desk in front of it and the USB cable taped down along the desk." >}}

## Configure your webcam {#configure-your-webcam}

The webcam discovery service lists every camera plugged into your computer and adds the one you pick as a camera component.
That way you get your webcam, not a laptop's built-in camera.

1. In the [Viam app](https://app.viam.com), open your machine and go to the **CONFIGURE** tab.
1. Click **+** and select **Blocks**.
1. Search for `find-webcams`, select the **webcam-discovery** service, and add it to your machine.
1. Click **Save** and wait a moment for the service to start.
1. Open the discovery service's **Test** section.
   It lists the cameras connected to your computer.
   The same camera can appear more than once, once for each resolution and frame rate it supports.
1. Find your webcam and click **Add component** next to one of its entries.
1. Rename the new camera component `camera`, and click **Save**.

You can delete the discovery service from your machine once the camera is working; you don't need it for the rest of the workshop.

{{< checkpoint >}}
On the **CONFIGURE** tab, the **TEST** section of the `camera` card shows a live view of the background, and the dice are sharp.
If the image is from your laptop's own camera, delete the `camera` component and add a different entry from the discovery service's **Test** section.
If the dice are blurry, raise the camera a little until the webcam can focus.
{{< /checkpoint >}}

## Create the starter dataset {#create-the-starter-dataset}

A dataset is a named collection of images in your organization, which you label and train models on.
The starter dataset is a small set of about 30 images that you label by hand in [Phase 2](/tutorials/dice-vision/label-the-starter-set/).
In [Phase 3](/tutorials/dice-vision/train-a-starter-model/) you train a rough starter model on it, and in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/) that model labels the larger training set for you, so you only correct its boxes instead of drawing every one.
The starter set lives in its own dataset because a training job rejects a dataset with more than 20% of its images unlabeled, and the training set stays mostly unlabeled until the starter model labels it.

1. Go to the **DATA** tab and click **DATASETS**.
1. Click **Create dataset**.
1. In the **Dataset Name** field, enter `dice-starter`.
1. Leave **Data type** set to **Binary Data**.
1. Click **Create dataset**.

{{< checkpoint >}}
The **DATASETS** list shows `dice-starter` with 0 images.
If the name is taken, another dataset in your organization already uses it; pick a different name and use it wherever this workshop says `dice-starter`.
{{< /checkpoint >}}

## Add 30 images from the camera {#add-30-images-from-the-camera}

Each image you add here is one you'll label in [Phase 2](/tutorials/dice-vision/label-the-starter-set/), so aim for variety rather than volume.

1. On the **CONFIGURE** tab, open the **TEST** section of the `camera` card.
1. Roll one to five dice onto the background.
1. Click **Add to dataset**, select `dice-starter`, and confirm.
1. Roll again and repeat until you've added 30 images.

{{< imgproc src="/tutorials/dice-vision/camera-test-card.png" resize="600x" declaredimensions=true class="imgzoom shadow" alt="The camera card's TEST section showing a live GetImages feed of four dice on white paper, with the Add to dataset button below the image." >}}

Vary each roll:

- Use different numbers of dice, from one to five.
- Let some dice land near the edges and some in the middle.
- Let two or three dice touch in a few images.
- Make sure every face, 1 to 6, shows up at least 10 times across the 30 images. Turn dice by hand if a face is rare.

A good starter set mixes how many dice are in each image, where they land, and whether they touch, like these three:

{{< imgproc src="/tutorials/dice-vision/starter-examples.jpg" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="Three overhead webcam images of dice on white paper: three dice spread apart, three dice near the right edge of the frame, and five dice with several touching in a row." >}}

{{< checkpoint >}}
`dice-starter` on the **DATASETS** page shows 30 images, and each one shows dice from above.
If the count is lower, check that you selected `dice-starter` each time you added an image.
{{< /checkpoint >}}

In the next phase, you draw a box around every die in these 30 images and label it with its value.

{{< workshop-nav >}}
