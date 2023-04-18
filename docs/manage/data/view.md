---
title: "View and Filter Data"
linkTitle: "View Data"
weight: 38
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Aaron Casas
---

After the Data Management Service synchronizes the uploaded data in Viam, you can view it on the [**DATA** page in the Viam cloud](https://app.viam.com/data/view).

![Images, files, and sensors tabs](../img/tabs.png)

The **DATA** page shows:

- **IMAGES**: PNG or JPEG files
- **FILES**: binary data like point cloud data
- **SENSOR DATA**: tabular sensor counts (like gantry position)

If you click on an image or a file, a **Details** panel appears on the right with capture metadata.

![Images, files, and sensors tabs](../img/data_view.png)

## Filter Data

On the [**DATA** page in the Viam app](https://app.viam.com/data/view), you can filter data in the left **FILTERING** panel.

For example, if you specify `Rover Rental` for location and click **SEARCH**, you can see all data captured on robots that belong to your `Rover Rental` location.

## Delete Data

You can delete image or file data from the [Viam app](https://app.viam.com).
To delete image data, click on an image in the **IMAGES** subtab and click on **DELETE SELECTED**.
To delete a file, click on the file  in the **FILES** subtab and click the **Delete** icon.

You can also delete data using the [Viam CLI](../../cli).

## Next Steps

To export your captured data from the cloud, see [Export Data](../export).

You can use cloud image data to [train machine learning models](../../ml/train-model) within Viam.

For a comprehensive tutorial on data management, see [Intro to Data Management](../../../tutorials/services/data-management-tutorial).
