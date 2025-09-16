---
linkTitle: "Alert on inferences"
title: "Alert on inferences"
weight: 60
layout: "docs"
type: "docs"
description: "Use machine learning and send alerts when an inference meets certain criteria."
---

Triggers can send alerts in the form of email notifications or webhook requests when a new data is synced to the cloud.
If you then configure a filtered camera or another modular resource that uploads data only when a specific detection or classification is made, you get a notification.

For example, a trigger could alert you when a camera feed detects an anomaly.

### Prerequisites

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "A configured camera and vision service." >}}

Follow the instructions to [configure a camera](/operate/reference/components/camera/) and [run inference](/data-ai/ai/run-inference/).

{{< /expand >}}

## Configure a filtered camera

You can use a camera and vision service to sync only images where an inference is made with the [`filtered-camera`](https://app.viam.com/module/viam/filtered-camera) {{< glossary_tooltip term_id="module" text="module" >}}.
This camera module takes the vision service and applies it to your webcam feed, filtering the output.
With this filtering, you can save only images that contain people who match your filtering criteria.

Configure the camera module with classification or object labels according to the labels your ML model provides that you want to alert on.

Complete the following steps to configure your module:

1. Navigate to your machine's **CONFIGURE** tab.

1. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component or service**.
   Start typing `filtered-camera` and select **camera / filtered-camera** from the results.
   Click **Add module**.

1. Name your filtering camera something like `objectfilter-cam` and click **Create**.

1. Paste a configuration into the attributes field:

   {{< tabs >}}
   {{% tab name="Template" %}}

   Replace the `<vision-service-name>` and `<confidence-threshold>` placeholders with values for your use case:

   ```json {class="line-numbers linkable-line-numbers"}
   {
      "camera": "<your_camera_name>",
      "vision_services": [
         {
               "vision": <first_vision_service>,
               "classifications": ...,
               "objects": ...
         },
         {
               "vision": <second_vision_service>,
               "classifications": ...,
               "objects": ...
         }
      ],
      "window_seconds": <time_window_for_capture>,
   }
   ```

   {{% /tab %}}
   {{% tab name="Example: Hard hat detection" %}}
   For example, if using the YOLOv8 model (named `yolo`) for hard hat detection as demonstrated in the [Monitor Helmet Usage tutorial](/tutorials/projects/helmet/):

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "camera": "my_webcam",
     "vision_services": [
       {
         "vision": "yolo",
         "objects": {
           "NO-Hardhat": 0.6
         }
       }
     ],
     "window_seconds": 3
   }
   ```

   {{% /tab %}}
   {{% /tabs %}}

   The confidence threshold determines the minimum level of certainty required from the vision model to sync data.
   For example, a confidence threshold of `0.6` syncs data only when the vision model is at least 60% sure that it has correctly identified the desired object type.

1. Click **Save** in the top right corner of the screen to save your changes.

For more information, see the [`filtered-camera` module README](https://app.viam.com/module/viam/filtered-camera).

{{% alert title="Tip" color="tip" %}}
Viam provides a way to monitor detections, classifications, and confidence levels from a live vision service.
To view this information, navigate to the vision service card and expand the **TEST** panel.
You can use this to verify your confidence level configuration.
{{% /alert %}}

## Configure data capture and sync

The [data management service](/data-ai/capture-data/capture-sync/#configure-data-capture-and-sync-for-individual-resources) can capture images and sync them to the Viam cloud.

Configure data capture on the `filtered-camera` camera to capture images of detections or classifications:

1. First, add the data management service to your machine.

   Navigate to your machine's **CONFIGURE** tab.

   Click the **+** (Create) button next to your main part in the left-hand menu and select **Component or service**.
   Enter "data" and select **data management**.
   Name your data management service `data-manager` and click **Create**.

   Leave all the default data service attributes as they are and click **Save** in the top right corner of the screen to save your changes.

1. Now you're ready to enable data capture on your detector camera.
   Locate the `objectfilter-cam` panel.

1. Click **Add method**.
   Click the **Type** dropdown and select **ReadImage**.
   Set the capture frequency to `0.2` images per second (equivalent to one image every 5 seconds).
   You can always change the frequency to suit your use case.
   Set the **MIME type** to `image/jpeg`.

## Set up alerts

Triggers send webhook requests or email notifications when certain events happen.

You can use the **Data has been synced to the cloud** (`part_data_ingested`) trigger type to send alerts whenever an image syncs to the cloud from your filtered camera.
Because the filter only syncs images that contain an anomaly, this trigger sends an alert when an anomaly occurs.

### Configure a trigger on your machine

Follow these steps to configure a trigger to alert when `filtered-camera` syncs an image:

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Trigger**.

1. Enter a name and click **Create**.

1. In the **Type** dropdown, select **Data has been synced to the cloud**.

1. In the **Data Types** dropdown, select **Binary (image)**.

   {{<imgproc src="/tutorials/helmet/trigger.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger created with data has been synced to the cloud as the type and binary (image) as the data type." class="shadow imgzoom" >}}

1. To add a notification method, add an entry to the **Webhooks** or **Email** sub-panels:

   To add an email notification:

   1. Click **Add Email**.

      {{<imgproc src="/build/configure/trigger-configured-email.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger configured with an example email." class="shadow imgzoom" >}}

   1. Add the email you wish to be notified whenever this trigger is triggered.
   1. Configure the time between notifications.

   To add a webhook notification:

   1. Click **Add Webhook**.

      {{<imgproc src="/build/configure/trigger-configured.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger configured with an example URL." class="shadow imgzoom" >}}

   1. Add the URL of your cloud function.
   1. Configure the time between notifications.
   1. Write your cloud function to process the [webhook](/data-ai/reference/triggers-configuration/#webhook-attributes).
      Use your cloud function to process data or interact with any external API, including Twilio, PagerDuty, or Zapier.

1. Configure the time between notifications.

1. Click **Save** in the top right corner of the screen to save your configuration.

## Test the whole system

You've built all the pieces of the system and connected them together.
Now it's time to test the whole thing.

Make sure `viam-server` is running on your machine.
Run the camera and wait for an anomaly to appear.
Within a few minutes of the anomaly, you should see your email or webhook alert.
Congratulations, you've successfully built your anomaly detection monitor!
