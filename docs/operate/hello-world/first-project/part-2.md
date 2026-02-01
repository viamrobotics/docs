---
linkTitle: "Part 2: Data Capture"
title: "Part 2: Data Capture"
weight: 20
layout: "docs"
type: "docs"
description: "Configure automatic data sync and alerts for your inspection system."
date: "2025-01-30"
---

**Goal:** Configure and use a machine to cloud data capture pipeline.

**Skills:** Data capture configuration, triggers and alerts, querying captured data.

**Time:** ~15 min

For inspection applications such as this one, monitoring defect detection is important both to ensure production line health and product quality.
You want to ensure the vision model is detecting a very high percentage of defects and quickly detect any problems either with defect detection or with the production line generally.
In addition, it's important to collect production training data to iteratively improve defect detection.

In this part of the tutorial, you'll configure continuous data capture to support these goals.
To do this, you'll use Viam's built-in data capture and cloud sync.
Once enabled, data capture services run automatically in the background.
Data gets buffered locally, synced to the cloud at an interval you configure, and is then made available for review and analysis through SQL or the MongoDB query language.

## 2.1 Configure Data Capture

**Enable data capture on the vision service:**

1. In the **Config** tab, click the `can-classifier` vision service
2. Find the **Data capture** section
3. Toggle **Enable data capture** to on
4. Set the capture frequency: `2` seconds
5. Select the method to capture: `GetDetectionsFromCamera`
6. Click **Save**

[SCREENSHOT: Vision service data capture configuration]

**Also capture camera images:**

You want the raw images alongside detection results—so you can review what the model saw and use images to improve your model later.

1. Find the `inspection-cam` camera in your config
2. Expand **Data capture**
3. Toggle **Enable data capture** to on
4. Set frequency: `2` seconds (matching the vision service)
5. Click **Save config**

[SCREENSHOT: Camera data capture configuration]

**Verify it's working:**

1. In the config, find `can-classifier` and click **Test** at the bottom of its card
2. You should see a capture indicator showing data is being recorded

The machine is now capturing detection results and images every 2 seconds—whether or not you're connected.

## 2.2 Add Machine Health Alert

Get notified if your inspection station goes offline. This is a simple trigger—no code required.

**Create the trigger:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine in the left sidebar
3. Select **Trigger**
4. Name it `offline-alert`
5. Click **Create**

**Configure the trigger:**

1. For **Type**, select `Part is offline`
2. Toggle **Email all machine owners** to on (or add specific email addresses)
3. Set **Minutes between notifications** to `5` (so you don't get spammed)
4. Click **Save config**

[SCREENSHOT: Offline trigger configuration]

That's it. If your inspection station loses connection for any reason—network issues, power loss, viam-server crash—you'll get an email.

{{< alert title="Other triggers" color="tip" >}}
You can also create triggers for "Part is online" (useful for knowing when a machine comes back) or "Data synced" (fires when data reaches the cloud). For detection-based alerts, see [Part 6](../part-6/).
{{< /alert >}}

## 2.3 View and Query Data

Viam automatically syncs captured data to the cloud and removes it from the machine to free up storage. No additional configuration required.

**Check the data:**

1. In the Viam app, click **Data** in the left sidebar (at the organization level, not the machine)
2. Wait 1-2 minutes for initial sync
3. You should see detection results and images appearing

[SCREENSHOT: Data tab showing captured detections]

**Verify the data includes:**

- **Detection results**—Each row shows label (PASS/FAIL) and confidence score
- **Camera images**—Click any row to see the image that was analyzed
- **Timestamps**—When each capture occurred
- **Machine ID**—Which machine captured it (matters when you have multiple stations)

**Filter the data:**

1. Click **Filter** and select your machine: `inspection-station-1`
2. Set time range to "Last hour"
3. You can also filter by component to see only vision service results or only camera images

[SCREENSHOT: Data tab with filters applied]

**Query with SQL or MQL:**

For more complex queries, use the **Query** page:

1. In the Viam app, click **Data** then **Query**
2. Select **SQL** or **MQL** as your query language
3. Try a simple query to find all failures:

```sql
SELECT time_received, data
FROM readings
WHERE component_name = 'can-classifier'
  AND data LIKE '%FAIL%'
ORDER BY time_received DESC
LIMIT 10
```

[SCREENSHOT: Query page with results]

This is powerful for incident investigation: "Show me all FAIL detections from the last hour" or "How many cans failed on Tuesday's shift?"

This data serves multiple purposes:

- **Compliance**—Auditable record of every inspection
- **Quality trends**—"FAIL rate increased 20% this week"
- **Model improvement**—Export images of cans to retrain your ML model
- **Incident review**—"Show me all FAILs from Tuesday's shift"

## 2.4 Summary

Data capture is now running in the background:

- Captures every detection and camera image
- Syncs to cloud automatically
- Queryable for analytics and compliance
- Alerts you when the machine goes offline

This foundation records everything your vision pipeline sees. In Part 3, you'll write custom control logic to act on detections.

{{< alert title="Checkpoint" color="success" >}}
Your system records every detection automatically. Data syncs to the cloud where you can query it and build dashboards.
{{< /alert >}}

**[Continue to Part 3: Control Logic →](../part-3/)**
