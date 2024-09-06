---
title: "Capture Data and Train a Model"
linkTitle: "Capture Data and Train a Model"
weight: 4
type: "docs"
description: "Configure data capture and cloud sync, filter and tag captured data, and train an ML model."
imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
images: ["/services/ml/training.png"]
aliases:
tags: ["data management", "data", "mlmodel", "vision", "services", "try viam"]
authors: []
languages: []
viamresources: ["data_manager", "mlmodel", "vision", "camera"]
level: "Beginner"
date: "2023-02-08"
cost: "0"
no_list: true
draft: true
---

In this tutorial, you will use three Viam services together to enable your machine to recognize specific objects in the world around it:

- The [data management service](#the-data-management-service), to capture images from a camera on your machine and sync them to the cloud.
- The [ML model service](#the-ml-model-service), to manage and deploy a machine learning (ML) model based on these images, once you have added tags to the images matching the objects you want to detect.
- The [vision service](/services/vision/), to enable your machine's camera to detect objects defined in the ML model on its own.

With all three services working together, your machine will be able to analyze its camera feed for the presence of specific shapes, such as a red star or blue circle.
When it detects a likely match, it will overlay a confidence score onto the camera feed alongside the name of the detected shape, indicating how closely the shape in the camera frame matches a shape it has seen before.

{{< alert title="Tip" color="tip" >}}
To get started without any hardware, you can borrow a rover through [Try Viam](https://app.viam.com/try), which is pre-configured with everything you need to begin this tutorial.
Rover rentals are 10 minutes in length, but you can [extend your session](/appendix/try-viam/reserve-a-rover/#can-i-extend-my-time) as needed, or [reuse a configuration from a previous session](/appendix/try-viam/reserve-a-rover/#how-can-i-reuse-my-borrowed-rover) if your time expires and you want to start a new session.

You can also use your own Viam machine as long as you have followed the prerequisite steps.
{{< /alert >}}

## The data management service

You can manage how your machine works with data files and images by using the _data management service_.

The [data management](/services/data/) service has two parts: [data capture](/services/data/capture/) and [cloud sync](/services/data/cloud-sync/).

- **Data capture** allows you to capture data locally from specific components on your machine running Viam.
  You can choose the components, corresponding methods, and the frequency of the data capture from the [Viam app](https://app.viam.com/).

- **Cloud sync** runs in the background and uploads your machine's captured data to the Viam app at a defined frequency.
  Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your machine has low network bandwidth.
  With cloud sync enabled for a component, data captured locally to your machine is automatically deleted after a successful sync.
  Data synced between your machine and the Viam app is encrypted in transit (over the wire) and when stored in the cloud (at rest).

Data capture and data sync are frequently used together, and are both enabled by default when you add the data management service to your machine.
However, if you want to manage your machine's captured data yourself, you can enable data capture but disable data sync.
If you are capturing data to a device with limited storage, or intend to capture a large amount of data, see [automatic data deletion](/services/data/capture/#automatic-data-deletion).

To capture data from your machine and sync to the Viam app, add the data management service and configure data capture for at least one component.

### Add the data management service

First, add the data management service to your machine to be able capture and sync data:

1. On your machine's **CONFIGURE** page in the [Viam app](https://app.viam.com), navigate to the **Services** tab.
1. Click the **Create service** button at the bottom of the page, and select **Data Management**.
1. Use the suggested name for your service or give it a name, like `viam-data-manager`, then click **Create Service**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data locally to the <file>~/.viam/capture</file> directory, and syncs captured data files to the Viam app every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save Config** at the bottom of the screen to save your changes.

   {{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="The data management service configuration pane with default settings shown for both capturing and syncing" resize="900x" >}}

For more information, see [Add the data management service](/services/data/capture/#add-the-data-management-service).

### Configure data capture for a component

Once you have added the data management service, you can configure data capture for specific components on your machine.
For this tutorial, you will configure data capture for images from a [camera](/components/camera/) component, but other data types such as sensor data or SLAM map data from other types of [components](/components/) can be captured as well.

To enable image data capture for a camera component:

1. Navigate to your machine's **CONFIGURE** page in the [Viam app](https://app.viam.com).

1. In the configuration pane for your configured camera component, find the **Data capture** section, and click the **Add method** button to configure data capture for this camera.

   - Set the **Method** to `ReadImage` and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     You can adjust the capture frequency if you want the camera to capture more or less image data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

   - Set the **MIME type** to `image/jpeg` to configure image data capture.

     {{< imgproc src="/tutorials/data-management/camera-data-capture.png" alt="The camera component configuration pane with data capture configuration enabled using type ReadImage and a capture frequency of 0.333" resize="600x" >}}

   - Make sure the **On/Off** toggle is switched to **On**.

1. Click **Save** at the top right of the window to save your changes.

For more information see [Configure data capture](/services/data/capture/#configure-data-capture-for-individual-resources) and [Configure cloud sync](/services/data/cloud-sync/).

### View and filter captured data

Now that you have configured data capture on your camera component, you can view the resulting data files in the Viam app.

Click on the menu icon on the camera configuration pane and select **View captured data**.

{{<imgproc src="/services/data/capture-data-menu.png" resize="500x" declaredimensions=true alt="Resource menu with the options Rename, Duplicate, View captured data, and Delete" class="aligncenter">}}

Here you can view the images captured so far from the camera on your machine.
New images should appear roughly every six seconds as cloud sync uploads them from your machine.

You can use the filters on the left side of the screen to filter your images by machine, component, date range, and more.

If you have a lot of images, filter them by limiting the displayed images to a specific date and time range:

{{< imgproc src="/tutorials/data-management/filter-date-range.png" alt="The data tab displaying images filtered by date and time range" resize="1200x" >}}

## The ML model service

Once your machine is capturing and syncing images to the Viam app, you are ready to train a machine learning (ML) model using those images.
You can use an ML model to help your machine adapt its behavior to the world around it.

For this tutorial, you will train an ML model to be able to recognize specific shapes (for example, red and blue stars), and then deploy that model to your machine using the _ML (machine learning) model service_.
With a model deployed to your machine, you can use the [ML model](/services/ml/) service together with the [vision](/services/vision/) service to analyze newly-detected objects for a possible match to a known shape.

To train a model from your captured data, first tag your images with appropriate labels and add them to a dataset.
Then train a model based on your dataset and labels and deploy the model to your machine.

Feel free to return to your machine's **Control** tab to position your camera (and rover) to capture additional images from a variety of different angles, or with different lighting or background compositions.
Generally, the more different perspectives of a given object you tag, the more likely your model will be able to identify it, even under differing conditions.
The following is an example of a good selection of images containing the `blue_star` tag, taken from a variety of angles:

{{< imgproc src="/tutorials/data-management/filter-by-blue-star.png" alt="The data tab showing images that contain blue stars from various angles, with a search filter for blue_star applied to only show images tagged with that label" resize="1200x" >}}

If you want to remove a tag, click the **X** icon to the right of the tag name below the **Tags** field.

## Troubleshooting

If your machine isn't capturing data and syncing it to the Viam app, ensure that both the data management service (named `viam-data-manager` in this tutorial) and the **Data capture** configuration for your camera (`cam` on the Try Viam rover) are enabled.

If your transform camera is not matching objects you have tagged, try lowering the `confidence_threshold`, or adding and tagging more images.

## Next steps

In this tutorial, you learned:

- how to use the [data management](/services/data/) service to capture images from your machine's camera and sync them to the Viam app
- how to filter and tag your synced images according to the objects you wanted to detect
