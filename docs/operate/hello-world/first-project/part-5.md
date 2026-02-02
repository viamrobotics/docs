---
linkTitle: "Part 5: Productize"
title: "Part 5: Productize"
weight: 50
layout: "docs"
type: "docs"
description: "Build a monitoring dashboard for your inspection system using Viam's Teleop interface."
date: "2025-01-30"
aliases:
  - /operate/hello-world/first-project/part-6/
---

**Goal:** Build a dashboard to monitor your inspection system.

**Skills:** Creating Teleop workspaces, configuring dashboard widgets, writing MQL aggregation pipelines.

**Time:** ~10 min

## What You'll Build

You've built a working inspection system—but monitoring it requires navigating through the Viam app's configuration and data tabs. In this section, you'll create a dedicated dashboard that shows everything at a glance: live camera feeds and defect trends over time.

Viam's Teleop interface lets you create custom monitoring dashboards. You'll add widgets for camera streams and time series graphs that use MQL aggregation pipelines to analyze your detection data.

## 5.1 Create a Workspace

A workspace is a custom dashboard view for your machines.

1. In the Viam app, go to **Fleet** → **Teleop**
2. Click **+ Create workspace**
3. Replace the placeholder name with `inspection`
4. In **Select location**, choose `Home` (or your location name)
5. In **Select machine**, choose `inspection-station-1`

{{<imgproc src="/tutorials/first-project/teleop-workspaces.png" resize="x1100" declaredimensions=true alt="Teleop workspaces page showing the Create workspace button." class="imgzoom shadow">}}

You now have an empty workspace ready for widgets.

## 5.2 Add a Camera Stream Widget

Add a live video feed from your inspection camera.

1. Click **+ Add widget**
2. Select **Camera Stream**
3. Click the pencil icon to configure
4. Set **Camera name** to `inspection-cam`
5. Set **Refresh type** to `Live`
6. Click **Save**

You should see the live feed from your inspection camera with cans passing on the conveyor belt.

## 5.3 Add a Defects Per Minute Widget

Now you'll create a time series graph showing how many defective cans are detected per minute. This requires a custom MQL aggregation pipeline to filter for failures and count them in time buckets.

**Recall the data structure** from Part 4—each detection looks like:

```json
{
  "component_name": "inspector-service",
  "time_received": "2026-02-02T02:23:27.326Z",
  "data": {
    "docommand_output": {
      "label": "FAIL",
      "confidence": 0.965815
    }
  }
}
```

You'll write MQL stages that filter for `FAIL` labels and count them per minute.

**Create the widget:**

1. Click **+ Add widget**
2. Select **Time Series**
3. Click the pencil icon to configure
4. Set **Title** to `Defective cans per minute`
5. Set **Time range (min)** to `60`
6. Set **Refetch rate (sec)** to `60`
7. Leave **Y axis lower bound** and **Y axis upper bound** as `auto`

**Configure the line:**

8. Set **Resource name** to `inspector-service`
9. Set **Capture method** to `DoCommand`
10. Set **Title** to `Defects`
11. For **Window method**, select **Custom query**

**Add the MQL stages:**

The custom query method lets you write MongoDB aggregation pipeline stages. You need three stages: match, group, and project.

12. In **Custom MQL Stages**, add a `$match` stage to filter for failures only:

    ```json
    {
      "$match": {
        "data.docommand_output.label": "FAIL"
      }
    }
    ```

13. Click **+ Add stage** and add a `$group` stage to count failures per 60-second bucket:

    ```json
    {
      "$group": {
        "_id": {
          "$dateTrunc": {
            "date": "$time_received",
            "unit": "second",
            "binSize": 60
          }
        },
        "value": {
          "$sum": 1
        }
      }
    }
    ```

14. Click **+ Add stage** and add a `$project` stage to format the output:

    ```json
    {
      "$project": {
        "time": "$_id",
        "value": true
      }
    }
    ```

15. Click **Save**

The graph now shows the count of defective cans detected in each minute.

{{< alert title="How the pipeline works" color="info" >}}

- **$match** filters to only FAIL detections
- **$group** buckets data into 60-second intervals and counts documents in each bucket
- **$project** renames `_id` to `time` (required format for the graph)

<!-- prettier-ignore -->
{{< /alert >}}

## 5.4 Add a Confidence Trend Widget

Add another time series showing the average confidence of failure detections over time. This helps you monitor model performance—if confidence drops, you may need to retrain.

1. Click **+ Add widget**
2. Select **Time Series**
3. Click the pencil icon to configure
4. Set **Title** to `Confidence`
5. Set **Time range (min)** to `60`
6. Set **Refetch rate (sec)** to `60`
7. Set **Y axis lower bound** to `0`
8. Set **Y axis upper bound** to `1`

**Configure the line:**

9. Set **Resource name** to `inspector-service`
10. Set **Capture method** to `DoCommand`
11. Set **Title** to `FAIL confidence`
12. For **Window method**, select **Custom query**

**Add the MQL stages:**

13. Add a `$match` stage:

    ```json
    {
      "$match": {
        "data.docommand_output.label": "FAIL"
      }
    }
    ```

14. Click **+ Add stage** and add a `$group` stage that averages confidence:

    ```json
    {
      "$group": {
        "_id": {
          "$dateTrunc": {
            "date": "$time_received",
            "unit": "second",
            "binSize": 60
          }
        },
        "value": {
          "$avg": {
            "$convert": {
              "input": "$data.docommand_output.confidence",
              "to": "double",
              "onError": "$data.docommand_output.confidence"
            }
          }
        }
      }
    }
    ```

15. Click **+ Add stage** and add a `$project` stage:

    ```json
    {
      "$project": {
        "time": "$_id",
        "value": true
      }
    }
    ```

16. Click **Save**

The graph shows average confidence for failure detections over time.

{{< alert title="Why use $convert?" color="info" >}}
The `$convert` operator ensures the confidence value is treated as a number for averaging. The `onError` fallback handles any edge cases where conversion fails.
{{< /alert >}}

## 5.5 Arrange Your Dashboard

Drag widgets to create a useful layout:

1. Click and drag the grid icon in the top-left corner of each widget
2. Position the camera stream on the right for real-time monitoring
3. Stack the time series graphs on the left to compare defect counts and confidence trends

Your dashboard now provides a complete view of your inspection system:

- **Live video** showing the inspection in progress
- **Defects per minute** tracking production quality
- **Confidence trend** monitoring model performance

{{<imgproc src="/tutorials/first-project/finished-dashboard.png" resize="x1100" declaredimensions=true alt="Finished dashboard showing Defective cans per minute graph, Confidence graph, and live camera stream." class="imgzoom shadow">}}

## 5.6 Summary

You've created a monitoring dashboard using MQL aggregation pipelines:

1. **Created a workspace** for your inspection station
2. **Added a camera stream** for live video monitoring
3. **Built a defects graph** using $match → $group (count) → $project
4. **Built a confidence graph** using $match → $group (average) → $project

The same MQL pipeline pattern—filter, aggregate, project—can be adapted for other metrics: pass rate, throughput, detection latency, or any data your system captures.

{{< alert title="Going further" color="tip" >}}
For fully custom dashboards with your own branding, you can build web applications using Viam's TypeScript SDK. The SDK provides access to the same data through `tabularDataByMQL()` and `tabularDataBySQL()` methods.
{{< /alert >}}

## Congratulations

You've completed the tutorial. Here's what you built:

1. **Vision Pipeline**—Camera, ML model, and vision service detecting defects
2. **Data Capture**—Automatic recording and cloud sync of images and detections
3. **Control Logic**—Custom inspector module exposing detection through DoCommand
4. **Module Deployment**—Packaged and deployed to run autonomously
5. **Productize**—Monitoring dashboard with real-time analytics

You've gone from an empty machine to a production-ready inspection system with monitoring—patterns that apply to any Viam application.

**[← Back to Overview](../)** to review what you learned.
