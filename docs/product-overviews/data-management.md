---
title: "Data Management"
linkTitle: "Data Management"
weight: 99
type: "docs"
description: "A guide to Viam's data ingestion and management tooling."
# SME: Alexa Greenberg
---
## Data Capture and Synchronization to the Cloud
The data management service supports capturing data from any component at a predefined frequency and syncing it Viam's data platform.

An example use case is a tomato picking gantry with a depth camera that captures images of crops on the vine.
The image and point cloud data is collected at 10Hz.
The gantry position is collected at 1kHz.
All data is uploaded to Viam's cloud platform every minute.

Once data is synchronized to the cloud, it is deleted off of the robot, allowing for a data flywheel of continuous capture without running out of memory.

More detailed information in the [data management service documentation](../../services/data-management).

## Viewing Data in Viam's Data Platform

Once data has been synchronized to Viam's data platform, it is viewable in [Data Management](https://app.viam.com/data) within the Viam app.

Image (e.g. jpeg and png) data is viewable in the `Images` tab, files and any other binary (e.g. point cloud data) is viewable in the `Files` tab, and tabular sensor (e.g. gantry position) counts are viewable the `Sensors` tab.

Clicking on a single image or file shows a `Details` pane on the right with capture metadata.

You can filter on data in the left `Filtering` panel.
For example, if you specify "kitchen1" for Location, "camera" for Component Type, and click the "Search" button, you will see all camera data that has been captured on any robots that belong to your "kitchen1" location.

## Coming Soon
- Tool to export data from Viam's data platform
- Data processing for ML model training
- ML model to robot deployment
