---
linkTitle: "Part 2: Data Capture"
title: "Part 2: Data Capture"
weight: 20
layout: "docs"
type: "docs"
description: "Configure automatic image capture and cloud sync for your inspection system."
date: "2025-01-30"
---

**Goal:** Configure and use a machine to cloud data capture pipeline.

**Skills:** Data capture configuration, cloud sync, browsing captured data.

**Time:** ~10 min

For inspection applications such as this one, monitoring defect detection is important both to ensure production line health and product quality.
You want to ensure the vision model is detecting a very high percentage of defects and quickly detect any problems.
In addition, it's important to collect production training data to improve defect detection models over time.

In this part of the tutorial, you'll configure continuous data capture to support these goals.
To do this, you'll use Viam's built-in data capture and cloud sync.
Once enabled, data capture services run automatically in the background.
Data gets buffered locally, synced to the cloud at an interval you configure, and is then available for review in the Viam app.

## 2.1 Configure Data Capture

**Include the data service in your machine configuration:**

1. Click **+** next to **inspection-station-1-main** in the **Configure** tab
2. Click **Component or service**
3. Select **data management**
4. Name it `data-service`
5. Click **Create**
6. **Save** your updated machine configuration

The default configuration options for the data service are correct for our application so we can move on to capturing data from the vision service.

**Enable data capture on the vision service:**

1. Click `vision-service` in your machine configuration
2. Find the **Data capture** section and click **Add method**
3. Select the method to capture: `CaptureAllFromCamera`
4. Set **Frequency (hz)** to `0.5` (every 2 seconds)
5. Set **Camera name** to `inspection-cam`
6. **Save** your configuration

**Verify it's working:**

1. In the **Data capture** section of the `vision-service` configuration panel you should now see a collapsible component labeled **Latest capture** with a day and time specified
2. Click on **Latest capture** and view the most recent image captured

Your machine is now capturing detection results and images every 2 seconds and syncing them to the Viam cloud application. Once synced to the cloud, the data is removed from your machine to free up storage.

{{< alert title="Tip" color="tip" >}}
Click **JSON** in the Configure tab to see how data capture settings appear in the raw configuration. Each component and service with data capture enabled has a `service_configs` entry containing `capture_methods`.
{{< /alert >}}

## 2.2 View Captured Data

Up to this point in the tutorial, you've focused on configuring your machine.
To view the data you are now capturing, you will need to open the data user interface in Viam.
Find the main Viam menu that includes: **Fleet**, **Data**, and **Registry** at the top of the page.
Right click on **Data** to open in a separate tab.

**View captured data:**

1. Review the grid of images captured from your work cell
2. Click on an image to see the detection results for that image
3. Click on a few other images to see how detection results vary for cans labeled `PASS` versus `FAIL`

{{<imgproc src="/tutorials/first-project/data-tab-images.png" resize="x1100" declaredimensions=true alt="Data tab showing a grid of captured images from the inspection camera.">}}

**Verify the data includes:**

- **Detection results**—Each row shows label (PASS/FAIL) and confidence score
- **Camera images**—Click any row to see the image that was analyzed
- **Timestamps**—When each capture occurred
- **Machine ID**—Which machine captured it (matters when you have multiple stations)

**Filter the data:**

1. Click **Filter** and select your machine: `inspection-station-1`
2. Set time range to "Last hour"
3. You can also filter by component to see only vision service results or only camera images

This captured data serves multiple purposes:

- **Compliance**—Auditable record of every inspection
- **Quality trends**—"FAIL rate increased 20% this week"
- **Model improvement**—Export images of cans to retrain your ML model
- **Incident review**—"Show me all FAILs from Tuesday's shift"

## 2.3 Summary

Data capture is now running in the background:

- Captures images with detection overlays
- Syncs to cloud automatically
- Available for visual review and filtering

This foundation records everything your vision pipeline sees. In Part 3, you'll write custom control logic to act on detections. Later, you'll configure tabular data capture to enable SQL queries on detection results.

{{< alert title="Checkpoint" color="success" >}}
Your system captures every detection as an image. Data syncs to the cloud where you can browse, filter, and review results.
{{< /alert >}}

**[Continue to Part 3: Control Logic →](../part-3/)**
