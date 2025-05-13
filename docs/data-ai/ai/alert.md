---
linkTitle: "Alert on inferences"
title: "Alert on inferences"
weight: 60
layout: "docs"
type: "docs"
description: "Use triggers to send email notifications when inferences are made."
---

At this point, you should have already set up and tested [computer vision functionality](/data-ai/ai/run-inference/).
On this page, you'll learn how to use triggers to send alerts in the form of email notifications or webhook requests when certain detections or classifications are made.

You will build a system that can monitor camera feeds and detect situations that require review.
In other words, this system performs anomaly detection.
Whenever the system detects an anomaly, it will send an email notification.

First, you'll set up data capture and sync to record images with the anomaly and upload them to the cloud.
Next, you'll configure a trigger to send email notifications or webhook requests when the anomaly is detected.

### Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "A configured camera and vision service. Click to see instructions." >}}

Follow the instructions to [configure a camera](/operate/reference/components/camera/) and [run inference](/data-ai/ai/run-inference/).

{{< /expand >}}

## Configure a filtered camera

Your physical camera is working and your vision service is set up.
Now you will pull them together to filter out only images where an inference is made with the [`filtered-camera`](https://app.viam.com/module/erh/filtered-camera) {{< glossary_tooltip term_id="module" text="module" >}}.
This camera module takes the vision service and applies it to your webcam feed, filtering the output so that later, when you configure data management, you can save only the images that contain people inferred to match the filtering criteria rather than all images the camera captures.

Configure the camera module with classification or object labels according to the labels your ML model provides that you want to alert on.
Follow the instructions in the [`filtered-camera` module readme](https://github.com/erh/filtered_camera).
For example, if using the YOLOv8 model (named `yolo`) for hardhat detection, you would configure the module like the following:

{{% expand "Instructions for configuring the filtered-camera module to detect people without a hardhat" %}}

1. Navigate to your machine's **CONFIGURE** tab.

2. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component or service**.
   Start typing `filtered-camera` and select **camera / filtered-camera** from the results.
   Click **Add module**.

3. Name your filtering camera something like `objectfilter-cam` and click **Create**.

4. Paste the following into the attributes field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "camera": "my_webcam",
     "vision": "yolo",
     "window_seconds": 3,
     "objects": {
       "NO-Hardhat": 0.5
     }
   }
   ```

   If you named your detector something other than "yolo," edit the `vision_services` value accordingly.
   You can also edit the confidence threshold.
   If you change it to `0.6` for example, the `filtered-camera` camera will only return labeled bounding boxes when the vision model indicates at least 60% confidence that the object is a hard hat or a person without a hard hat.

5. Click **Save** in the top right corner of the screen to save your changes.

{{% /expand%}}

## Configure data capture and sync

Viam's built-in [data management service](/data-ai/capture-data/capture-sync/#configure-data-capture-and-sync-for-individual-resources) allows you to, among other things, capture images and sync them to the cloud.

Configure data capture on the `filtered-camera` camera to capture images of detections or classifications:

1. First, you need to add the data management service to your machine to make it available to capture data on your camera.

   Navigate to your machine's **CONFIGURE** tab.

   Click the **+** (Create) button next to your main part in the left-hand menu and select **Component or service**.
   Type "data" and click **data management / RDK**.
   Name your data management service `data-manager` and click **Create**.

   Leave all the default data service attributes as they are and click **Save** in the top right corner of the screen to save your changes.

2. Now you're ready to enable data capture on your detector camera.
   Locate the `objectfilter-cam` panel.

3. Click **Add method**.
   Click the **Type** dropdown and select **ReadImage**.
   Set the capture frequency to `0.2` images per second (equivalent to one image every 5 seconds).
   You can always change the frequency to suit your use case.
   Set the **MIME type** to `image/jpeg`.

## Set up alerts

[Triggers](/data-ai/data/advanced/alert-data/) allow you to send webhook requests or email notifications when certain events happen.

You can use the **Data has been synced to the cloud** (`part_data_ingested`) trigger to send alerts whenever an image with an anomaly detection is synced to the cloud from your object filter camera.

Set up the trigger with a webhook or with Viam's built-in email alerts which sends a generic email letting you know that data has been synced.

### Configure a trigger on your machine

Now it's time to configure a trigger so that you get an email when a person is not wearing a hard hat.

Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
Click the **+** (Create) button in the left side menu and select **Trigger**.

Name the trigger and click **Create**.

Select trigger **Type** as **Data has been synced to the cloud** and **Data Types** as **Binary (image)**.

{{<imgproc src="/tutorials/helmet/trigger.png" resize="x300" declaredimensions=true alt="The trigger created with data has been synced to the cloud as the type and binary (image) as the data type." class="shadow" >}}

To configure notifications, either

- add a webhook and enter the URL of your custom cloud function
- add an email address to use Viam's built-in email notifications

For both options also configure the time between notifications.

Click **Save** in the top right corner of the screen to save your changes.

{{< readfile "/static/include/webhooks.md" >}}

## Test the whole system

You've built all the pieces of the system and connected them together.
Now it's time to test the whole thing.

Make sure `viam-server` is running on your machine.
Run your camera in front of what you're detecting and wait for an anomaly to appear.
Wait a couple of minutes for the email to arrive in your inbox.
Congratulations, you've successfully built your anomaly detection monitor!

## Troubleshooting

### Test the vision service

To see the detections or classifications occurring in real time and verify if their confidence level reaches the threshold you have set, you can navigate to the vision service card and expand the **TEST** panel.
