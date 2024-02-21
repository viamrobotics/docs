---
title: "View and Filter Data"
linkTitle: "View Data"
description: "View and filter data on the DATA page in the Viam Cloud."
weight: 38
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: "/ml/collect.svg"
imageAlt: "View images"
images: ["/ml/collect.svg"]
aliases:
  - /manage/data/view/
# SME: Alexa Greenberg
---

After the data management service synchronizes the uploaded data in Viam, you can view it on the [**DATA** page in the Viam app](https://app.viam.com/data/view).

![Images, files, and sensors tabs](/data/tabs.png)

The **DATA** page displays data from all resources you are an owner of within the {{< glossary_tooltip term_id="organization" text="organization" >}} you are currently authenticated to.
This includes data from any locations shared with your organizations.
For more information on who can do what with data, see [Permissions](/fleet/rbac/#permissions).

The **DATA** page shows data about:

- **Images**: PNG or JPEG files
- **Point clouds**: collections of points in 3D space
- **Files**: binary data like .mov files
- **Sensors**: tabular sensor counts (like gantry position)

If you click on an image or a file, a **Details** panel appears on the right with capture metadata.

![Data view with an image selected](/data/data_view.png)

## Filter data

On the [**DATA** page in the Viam app](https://app.viam.com/data/view), you can filter data in the left **Filtering** panel.
You can filter by several categories including machine name, location, or timestamp range.

For example, if you specify `Rover Rental` for location and click **SEARCH**, you can see all data captured on machines that belong to your `Rover Rental` location.

You can also filter data using the [Viam Python SDK](https://python.viam.dev/).
For example, you could use the [`BinaryDataByFilter`](/build/program/apis/data-client/#binarydatabyfilter) or [`TabularDataByFilter`](/build/program/apis/data-client/#tabulardatabyfilter) methods to filter binary data or tabular data respectively.

To query your data using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} instead, see [Query Data using SQL / MQL](/data/query/).

## Delete data

You can delete image or file data from the [Viam app](https://app.viam.com).
To delete image data, click on an image in the **Images** subtab and click on **DELETE SELECTED**.
To delete a file, click on the file in the **Files** subtab and click the **Delete** icon.

To delete all image, file, or sensor data respectively, click on **DELETE ALL** in the top right corner.

{{< alert title="Tip" color="tip" >}}
If you need to delete many images that are from a specific time frame or machine, you can apply a [filter](#filter-data) and then click **DELETE ALL**.
{{< /alert >}}

![Data view with no image selected showing the Delete all button](/data/delete_all.png)

You can also delete data using the [Viam CLI](/fleet/cli/).

## Next steps

To export your captured data from the cloud, see [Export Data](../export/).

If you have synced tabular data, such as [sensor](/components/sensor/) readings, you can [query that data with SQL or MQL](../query/) from the Viam app or a MQL-compatible client.
If you have synced images, you can use those images to [train machine learning models](/ml/train-model/) within the Viam app.

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).
