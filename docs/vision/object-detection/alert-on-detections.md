---
linkTitle: "Alert on detections"
title: "Alert on detections"
weight: 60
layout: "docs"
type: "docs"
description: "Send email or webhook alerts when your vision service detects specific objects or classifications."
aliases:
  - /vision/alert/
  - /vision/how-to/alert-on-detections/
  - /data-ai/ai/alert/
  - /vision/alert-on-detections/
date: "2026-04-14"
---

You want to be notified when your camera detects something specific: a person in a restricted area, a missing hard hat, or an anomaly on a production line. This guide shows you how to connect your vision service to Viam's trigger system so you receive an email or webhook whenever a detection occurs. No custom code is required.

## Concepts

### The alert pipeline

The alert system chains three resources together:

1. **Filtered camera**: a camera module that only passes images to the data management service when specific detections or classifications are present.
2. **Data management service**: captures images from the filtered camera and syncs them to the Viam cloud.
3. **Trigger**: fires when new data syncs, sending an email or webhook notification.

Because the filtered camera only passes images that match your criteria, every synced image represents a detection event. The trigger fires on each sync, turning data events into alerts.

### Filtered camera behavior

The [`filtered-camera`](https://app.viam.com/module/viam/filtered-camera) module wraps an existing camera and applies a vision service as a filter. It functions as a normal camera for live viewing and API calls. The filtering only affects what gets captured by the data management service.

You configure the filter with:

- **A label**: the detection or classification class name to look for (such as "Person" or "NO-Hardhat").
- **A confidence threshold** (0.0-1.0): the minimum confidence score required. Only images where the model meets this threshold are captured.

### Alert frequency

Triggers support a configurable alert frequency to prevent alert fatigue. For example, you can limit alerts to a maximum of one per hour even if detections occur continuously.

## Steps

### 1. Configure a filtered camera

Add the filtered camera module to your machine:

1. Navigate to your machine's **CONFIGURE** tab.
2. Click **+** and select **Configuration block**.
3. In the search field, type `filtered-camera` and select the matching result.
4. Click **Add component**, name the component `objectfilter-cam`, and click **Add component** again to confirm. The module is installed automatically.
5. Add configuration attributes:

   {{< tabs >}}
   {{% tab name="Template" %}}

   Replace `<camera_name>` and `<vision_service_name>` with the names of your camera and vision service. Choose either `objects` (for bounding-box detections) or `classifications` (for image-level labels) and remove the other.

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

   This example uses a YOLOv8 model named `yolo` to detect workers without hard hats:

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
   {{< /tabs >}}

6. Click **Save**.

For a fuller walkthrough that combines the filtered camera with an ML detector, see [Filter images at the edge](/data/filter-at-the-edge/#use-a-filtered-camera-with-ml). The [`filtered-camera` module README](https://app.viam.com/module/viam/filtered-camera) has the raw attribute reference.

{{% alert title="Tip" color="tip" %}}
To verify your confidence threshold, expand the **TEST** panel on your vision service card, select the right camera in the **Camera** dropdown, and observe the confidence levels for live detections.
{{% /alert %}}

### 2. Configure data capture and sync

Add the data management service to capture and sync filtered images:

1. Click **+** and select **Configuration block**.
2. In the search field, type `data management` and select the matching result.
3. Click **Add component**, name the service `data-manager`, and click **Add component** again to confirm.
4. Leave the default attributes and click **Save**.

Enable data capture on the filtered camera:

1. Locate the `objectfilter-cam` panel.
2. Click the **Data Capture** button.
3. Set **Method** to **GetImages**.
4. Set **Frequency (hz)** to `0.2` (one image every 5 seconds). Adjust as needed for your use case.

### 3. Configure a trigger

Add a trigger to send alerts when filtered images sync:

1. Click **+** in the left sidebar and select **Trigger**.
2. Enter a name and click **Create**.
3. Set **Type** to **Data has been synced to the cloud**.
4. Set **Data Types** to **Binary (image)**.

   {{<imgproc src="/tutorials/helmet/trigger.png" resize="x600" style="width: 500px" declaredimensions=true alt="The trigger configured with 'Data has been synced to the cloud' as the type and 'Binary (image)' as the data type." class="shadow imgzoom" >}}

5. Add notification methods. The following options live in the **ALERT OPTIONS** and **WEBHOOKS** sections of the trigger card:

   **Email specific addresses**: Toggle on and add email addresses. Each row has its own **Alert frequency**.

   **Email all machine owners**: Toggle on. Set the **Alert frequency** for the all-owners row.

   **Webhook**: In the **WEBHOOKS** section click **Add Webhook**, enter the URL of your cloud function, and implement logic to process the [webhook payload](/reference/triggers/#webhook-attributes). Use this to integrate with external services like Twilio, PagerDuty, or Zapier.

6. Set each **Alert frequency** you enabled (for example, maximum one alert per hour).
7. Click **Save**.

## Try it

1. Point your camera at an object your model recognizes and wait for the capture interval to pass.
2. Check the **TEST** panel on your vision service to confirm detections are occurring with sufficient confidence.
3. Navigate to the **DATA** tab and verify that images are syncing.
4. Check your email or webhook endpoint for the alert.

## Troubleshooting

{{< expand "No alerts received" >}}

- Check the **LOGS** tab for errors from the filtered camera or data management service.
- Verify your vision service detects objects with confidence above your threshold using the **TEST** panel.
- Confirm the label in your filtered camera config exactly matches the vision service output (case-sensitive).
- Check the **DATA** tab to see if images are being captured and synced.
- Verify trigger configuration: correct type (data synced), correct data type (binary/image), and valid notification settings.

{{< /expand >}}

{{< expand "Too many alerts" >}}

- Increase the confidence threshold in the filtered camera configuration to reduce false positives.
- Lower the data capture frequency (for example, from `0.2` to `0.1` images per second).
- Increase the alert frequency limit in the trigger settings (for example, maximum one per hour).

{{< /expand >}}

{{< expand "Images syncing but no trigger fires" >}}

- Confirm the trigger is configured with **Data has been synced to the cloud** as the type.
- Check that **Binary (image)** is selected as the data type.
- Verify that at least one notification method (email or webhook) is configured.

{{< /expand >}}

## What's next

- [Act on detections](/vision/object-detection/act-on-detections/): build a module that responds to vision results in real time.
- [Triggers reference](/reference/triggers/): full documentation for trigger types, webhook payloads, and configuration options.
- [Capture and sync data](/data/capture-sync/capture-and-sync-data/): learn more about configuring data capture and sync intervals.
