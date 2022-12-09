---
title: "Data Management"
linkTitle: "Data Management"
weight: 99
type: "docs"
description: "A guide to Viam's data ingestion and management tooling."
# SME: Alexa Greenberg
---

## Data Capture and Synchronization to the Cloud

The data management service supports capturing data from any component at a predefined frequency and syncing it with Viam's data platform.

An example use case is a tomato picking gantry with a depth camera that captures images of crops on the vine.
The image and point cloud data is collected at 10Hz.
The gantry position is collected at 1kHz.
All data is uploaded to Viam's cloud platform every minute.

Once data is synchronized to the cloud, it is deleted from the robot, allowing for a data flywheel of continuous capture without running out of memory.

You can find detailed information in the [data management service](../../services/data-management/) documentation.

## Viewing Data in Viam's Data Platform

After the data management service synchronizes the uploaded data in Viam, you can view it within the Viam app. Refer to [Data Management](https://app.viam.com/data) for further information.

Image (e.g, jpeg and png) data is viewable in the **Images** tab, files and any other binary (e.g, point cloud data) is viewable in the **Files** tab, and tabular sensor (e.g, gantry position) counts are viewable the **Sensors** tab.

Clicking on a single image or file shows a **Details** panel on the right with capture metadata.

You can filter on data in the left **Filtering** panel.
For example, if you specify "kitchen1" for Location, "camera" for Component Type, and click **Search**, you will see all camera data that has been captured on any robots that belong to your "kitchen1" location.

## Exporting Data from Viam's Data Platform

Below the **Search** button in the **Filtering** panel, you can click **Copy Export Command** to export data.
Make sure you have Go installed, then paste the copied command into your terminal.

While the default command exports data to the directory location specified by the `--destination=.` flag, you can also specify an absolute path directory.

The following example downloads all image data from December 2022 to `/tmp/dec22_robot`

```bash
go run go.viam.com/rdk/cli/cmd data
--component_type=camera
--org_ids=1cewfi124ewff
--data_type=binary
--mime_types=image/jpeg,image/png
--start=2022-12-01T05:00:00.000Z
--end=2023-01-01T05:00:00.000Z
--destination=/tmp/dec22_robot
```

Running the data command with the arguments provided above would download data to `/tmp/dec22_robot/data` and capture metadata to `/tmp/dec22_robot/metadata`.

## Coming Soon

- Data processing for ML model training
- ML model to robot deployment
