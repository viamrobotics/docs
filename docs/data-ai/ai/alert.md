---
linkTitle: "Alert on inferences"
title: "Alert on inferences"
weight: 60
layout: "docs"
type: "docs"
description: "Use machine learning and send alerts when an inference meets certain criteria."
date: "2025-10-10"
---

Triggers can send alerts in the form of email notifications or webhook requests when new data syncs to the cloud.

This guide shows you how to set up an alert system that notifies you when specific objects or classifications are detected in your camera feed.
The process involves three resources:

1. **Filtered Camera**: Filters images passed to the data management service
2. **Data Management**: Syncs filtered images to the cloud
3. **Triggers**: Sends alerts when data syncs

For example, a trigger could alert you when a camera feed detects an anomaly.

### Prerequisites

Before setting up alerts, you need:

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup-both.md" %}}

{{% /expand %}}

{{< expand "A configured camera and vision service." >}}

You'll need a working vision service that can detect objects or classifications.
The filtered camera will use this service to determine which images to capture.
Follow the instructions to [configure a camera](/operate/reference/components/camera/) and [run inference](/data-ai/ai/run-inference/).

{{< /expand >}}

## Configure a filtered camera

The [`filtered-camera`](https://app.viam.com/module/viam/filtered-camera) {{< glossary_tooltip term_id="module" text="module" >}} functions as a normal camera unless used with the data management service.
When you configure the data management service to capture and sync images from the camera, the camera will only pass images to the data management service if they meet the defined criteria.
The camera module takes a vision service and applies it to a camera feed using the generated predictions to filter the output for the data management service.

Configure the filtered camera module to capture images when specific predictions occur:

1. Navigate to your machine's **CONFIGURE** tab.

1. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component or service**.
   Start typing `filtered-camera` and select **camera / filtered-camera** from the results.
   Click **Add module**.

1. Name your filtering camera something like `objectfilter-cam` and click **Create**.

1. Paste a configuration into the attributes field:

   {{< tabs >}}
   {{% tab name="Template" %}}

   Replace the `<camera_name>` and `<vision_service_name>` values with the names of your camera and vision service.

   **Choose your detection type**:

   - For **object detection** (bounding boxes around objects): Use the `objects` configuration with the label you want to alert on and remove `classifications`
   - For **classification** (image-level labels): Use the `classifications` configuration with the label you want to alert on and remove `objects`

   The confidence threshold (0.0-1.0) determines how certain the vision model must be before capturing photos.
   For example, a confidence threshold of `0.6` only captures photos when the vision model is at least 60% sure that it has correctly identified the desired label.

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "camera": "<camera_name>",
     "vision_services": [
       {
         "vision": "<vision_service_name>",
         "classifications": { "<label>": 0.5 },
         "objects": { "<label>": 0.5 }
       }
     ]
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
     ]
   }
   ```

   {{% /tab %}}
   {{% /tabs %}}

1. Click **Save** in the top right corner of the screen to save your changes.

For more information, see the [`filtered-camera` module README](https://app.viam.com/module/viam/filtered-camera).

{{% alert title="Tip" color="tip" %}}
Viam provides a way to monitor detections, classifications, and confidence levels from a live vision service.
To view this information, navigate to the vision service card and expand the **TEST** panel.
You can use this to verify your confidence level configuration.
{{% /alert %}}

## Configure data capture and sync

The [data management service](/data-ai/capture-data/capture-sync/#configure-data-capture-and-sync-for-individual-resources) captures data and syncs it to the Viam cloud.
This step connects your filtered camera to the cloud so that detected images can trigger alerts.

Configure data capture on the `filtered-camera` resource to capture images of detections or classifications:

1. Add the data management service to your machine:

   Navigate to your machine's **CONFIGURE** tab.

   Click the **+** (Create) button next to your main part in the left-hand menu and select **Component or service**.
   Enter "data" and select **data management**.
   Name your data management service `data-manager` and click **Create**.

   Leave all the default data service attributes as they are and click **Save** in the top right corner of the screen to save your changes.

1. Enable data capture on your filtered camera:
   Locate the `objectfilter-cam` panel.

   Click **Add method**.
   Click the **Type** dropdown and select **ReadImage**.
   Set the capture frequency to `0.2` images per second (equivalent to one image every 5 seconds).
   You can adjust the frequency to suit your use case.
   Set the **MIME type** to `image/jpeg`.

## Configure a trigger on your machine

Triggers send webhook requests or email notifications when certain events happen:

- Your filtered camera captures an image when it detects the specified objects or classifications
- The data management service syncs that image to the cloud
- A trigger detects the sync event and sends your alert

Since the filtered camera only captures images that meet the specified criteria, it only syncs images when a label is identified.
Therefore, if you configure a filtered camera to capture images when an anomaly is detected, an image of the anomaly gets synced, a trigger fires, and an alert is sent.

Follow these steps to configure a trigger to alert when `filtered-camera` syncs an image:

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Trigger**.

1. Enter a name and click **Create**.

1. In the **Type** dropdown, select **Data has been synced to the cloud**.

1. In the **Data Types** dropdown, select **Binary (image)**.

   {{<imgproc src="/tutorials/helmet/trigger.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger created with 'Data has been synced to the cloud' as the type and 'Binary (image)' as the data type." class="shadow imgzoom" >}}

1. Add notification methods to the **Webhooks** or **Email** sub-panels:

   To add an email notification:

   1. Click **Add Email**.

      {{<imgproc src="/build/configure/trigger-configured-email.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger configured with an example email address." class="shadow imgzoom" >}}

   1. Add the email address you wish to be notified whenever this trigger fires.

   To add a webhook notification:

   1. Click **Add Webhook**.

      {{<imgproc src="/build/configure/trigger-configured.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger configured with an example webhook URL." class="shadow imgzoom" >}}

   1. Add the URL of your cloud function.
   1. Write your cloud function to process the [webhook data](/data-ai/reference/triggers-configuration/#webhook-attributes).
      Use your cloud function to process data or interact with external APIs, such as Twilio, PagerDuty, or Zapier.

1. Configure the notification frequency (for example, maximum one alert per hour).

1. Click **Save** in the top right corner of the screen to save your configuration.

## Testing

1. **Verify your setup**:

   - Make sure `viam-server` is running on your machine
   - Confirm your vision service is working by checking the **TEST** panel
   - Ensure your filtered camera configuration matches your vision service's output labels

2. **Test the detection**:

   - Present the camera with an object or situation that should trigger the alert
   - Watch the vision service **TEST** panel to confirm detections are occurring
   - Check that the confidence levels meet your threshold

3. **Monitor the data flow**:
   - The data management service attempts to get an image from the filtered camera based on the configured capture interval
   - Once the data management service captures an image, the image will sync when the next sync interval is reached
   - At this point you will receive your email or webhook alert

### Troubleshooting

#### No alerts received?

1. Check the **LOGS** tab
1. Check that your vision service is detecting objects with sufficient confidence
1. Verify your filtered camera configuration matches the vision service output
1. Ensure the data management service is capturing images (check the data tab)
1. Confirm your trigger configuration is correct

#### Too many alerts?

If you're getting too many false positives, increase your confidence threshold in the filtered camera configuration.

If you receive too many alerts and want to limit them to once per hour maximum, adjust the notification frequency in your trigger settings.
