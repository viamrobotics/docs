---
title: "Data Management"
linkTitle: "Data Management"
weight: 20
type: "docs"
tags: ["data", "data management", "services"]
# SME: Alexa Greenberg
---

The Data Management Service captures data from one or more components and securely syncs it to Viam's data platform. You can configure the frequency individually for each component. The service is designed for flexibility and efficiency while preventing data loss, data duplication, and other data management issues.

The service has two parts: [Data Capture](#data-capture) and [Cloud Sync](#cloud-sync).

## Data Capture

Viam's Data Management Service captures data from one or more components locally on the robot's disk. The process runs in the background and, by default, stores data in the `/.viam/capture` directory.

For more information, see [Data Capture](../../services/data-management/#data-capture).

## Cloud Sync

Viam's Data Management Service securely syncs the specified data at the user-defined frequency to Viam's data platform.

For more information, see [Cloud Sync](../../services/data-management/#cloud-sync).

## Viewing Data in Viam's Data Platform

After the Data Management Service synchronizes the uploaded data in Viam, you can view it within the Viam app at [https://app.viam.com/data/view](https://app.viam.com/data/view).

Image (e.g, jpeg and png) data is viewable in the **IMAGES** tab, files and any other binary (e.g, point cloud data) is viewable in the **FILES** tab, and tabular sensor (e.g, gantry position) counts are viewable the **SENSOR DATA** tab.

Clicking on a single image or file shows a **Details** panel on the right with capture metadata.

You can filter on data in the left **FILTERING** panel.
For example, if you specify "kitchen1" for Location, "camera" for Component Type, and click **SEARCH**, you will see all camera data that has been captured on any robots that belong to your "kitchen1" location.

## Exporting Data from Viam's Data Platform

Prior to exporting data for the first time, verify that Go is installed. Then to export data:

1. Below the **SEARCH** button in the **FILTERING** panel, click **COPY EXPORT COMMAND** to copy the export command to the clipboard.

2. Paste the command into your terminal and press Enter.
While the default command exports data to the directory location specified by the `--destination=.` flag, you can also specify an absolute directory path.
The following example downloads all image data from December 2022 to `/tmp/dec22_robot`.

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

Running the `data` command with the arguments provided above would download data to `/tmp/dec22_robot/data` and capture metadata to `/tmp/dec22_robot/metadata`.

Note: before you run an export command for the first time, you must authenticate to app.viam.com using the following command:

```bash
go run go.viam.com/rdk/cli/cmd auth
```

## Coming Soon

- Data processing for ML model training
- ML model to robot deployment
