---
linkTitle: "Capture and sync"
title: "Capture and sync data"
tags: ["data management", "data", "services"]
weight: 10
layout: "docs"
type: "docs"
viamresources: ["camera", "data_manager", "mlmodel", "vision"]
platformarea: ["data"]
description: "Capture images from a component on your machine and sync the data to the cloud."
no_list: true
date: "2024-12-03"
---

<!-- todo: make not just camera
make description better -->

You can use Viam's built-in data management service to capture images from a camera on your machine and sync the images to the cloud.

With your images synced to the cloud, you can view images from all your machines in the Viam app interface.
From there, you can use your image data to do things like [train ML models](/how-tos/train-deploy-ml/).

![Data view](/services/data/delete_all.png)
<br>

{{< alert title="In this page" color="tip" >}}

1. [Collect image data and sync it to the cloud](#collect-image-data-and-sync-it-to-the-cloud)
1. [Stop data capture](#stop-data-capture).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "A configured camera. Click to see instructions." %}}

First, make sure to connect your camera to your machine if it's not already connected (like with an inbuilt laptop webcam).

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a camera model](/components/camera/) that supports your camera.

If you are not sure what to use, start with a [webcam](/components/camera/webcam/) which supports most USB cameras and inbuilt laptop webcams.

{{% /expand%}}

## Collect image data and sync it to the cloud

Adding the data management service to your machine enables you to capture and sync data:

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

With the data management service configured on your machine, configure how the camera component itself captures data:

In the **Data capture** panel of your camera's configuration, select `ReadImage` from the method selector.

Set your desired capture frequency.
For example, set it to `0.05` to capture an image every 20 seconds.

Set the MIME type to your desired image format, for example `image/jpeg`.

{{% /tablestep %}}
{{% tablestep %}}
**3. Save to start capturing**

Save the config.
With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.

{{% /tablestep %}}
{{% tablestep %}}
**4. View data in the Viam app**

Click on the **...** menu of the camera component and click on **View captured data**.
This takes you to the data tab.

![View captured data option in the component menu](/get-started/quickstarts/collect-data/cam-capt-data.png)

If you do not see images from your camera, try waiting a minute and refreshing the page to allow time for the images to be captured and then synced to the app at the interval you configured.

If no data appears after the sync interval, check the [**Logs**](/cloud/machines/#logs).

{{% /tablestep %}}
{{< /table >}}

{{% alert title="Tip" color="tip" %}}
To keep your data organized, you can configure a tag in your data management service config panel.
This tag will be applied to all data synced from that machine in the future.
If you apply the same tag to all data gathered from all machines that you want to use in your dataset, you can filter by that tag in the Viam app **DATA** tab, or when querying data.

This is not required, since you can use other filters like time or machine ID in the **DATA** tab to isolate your data.
{{% /alert %}}

You now know how to capture and sync image data.
For many use cases, you may not want to capture data unless it meets certain conditions.
Consider the example of a security camera that captures data every 5 seconds.
This setup would result in a large number of images, of which most wouldn't be interesting.

In the next part of this guide, you will learn how to filter the data before capturing and syncing it.

## Stop data capture

If this is a test project or if you are continuing this how to set up filtering, make sure you stop data capture to avoid [incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of test data.

In the **Data capture** section of your camera's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## Next steps

Now that you have collected image data, you can [train new computer vision models](/data-ai/advanced/train-tflite/) or [programmatically access your data](https://docs.viam.com/appendix/apis/data-client/):

{{< cards >}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/appendix/apis/data-client/" %}}
{{< /cards >}}

To see image data filtering in action, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/configure/pet-photographer.md" %}}
{{< /cards >}}
