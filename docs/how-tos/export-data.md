---
title: "How to export data"
linkTitle: "Export Data"
description: "Download data from the Viam app to your local computer using the data client API or the Viam CLI."
weight: 45
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: true
images: ["/services/icons/data-capture.svg"]
aliases:
  - /manage/data/export/
  - /data/export/
  - /services/data/export/
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "cli"]
level: "Beginner"
date: "2024-09-13"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You can download machine data from cloud storage to your computer with the Viam CLI or data client API.

{{% alert title="In this page" color="tip" %}}

- [Export data with the Viam CLI](#export-data-with-the-viam-cli)
- [Manage data with the data client API](#manage-data-with-the-data-client-api)

{{% /alert %}}

## Prerequisites

{{< expand "Install the Viam CLI and authenticate." >}}
[Install the Viam CLI](/cli/#install), then [authenticate your session with Viam](/cli/#authenticate).
{{< /expand >}}

## Export data with the Viam CLI

To export your synced data using the Viam CLI:

{{< table >}}
{{% tablestep %}}
**1. Filter the data you want to download**

Navigate to the [**DATA** page in the Viam app](https://app.viam.com/data/view).

Use the filters on the left side of the page to filter only the data you wish to export.

{{% /tablestep %}}
{{% tablestep %}}
**2. Copy the export command from the DATA page**

In the upper right corner of the **DATA** page, click the **Export** button.

Click **Copy export command**.
This copies the command, including your org ID and the filters you selected, to your clipboard.

{{% /tablestep %}}
{{% tablestep link="/cli/#data" %}}
**3. Run the command**

Run the copied command in a terminal:

```sh {class="command-line" data-prompt="$"}
viam data export --org-ids=<org-id> --data-type=<binary|tabular> --mime-types=<mime types> --destination=.
```

This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

By default, the command creates two new directories named `data` and `metadata` in the current directory and downloads the specified data into the `data` folder and metadata, like bounding box information and labels, in JSON format into the `metadata` folder.
If you want to store the data in a different location, change the specified folder with the [`--destination` flag](/cli/#named-arguments).

Once the command has finished running and downloading the data, you can view and use the data locally.

Since data is downloaded in parallel, the order is not guaranteed.
Sort your folder by filename in order to see them in chronological order.

{{% /tablestep %}}
{{< /table >}}<br>

You can see more information about exporting data in the [Viam CLI documentation](/cli/#data).

## Manage data with the data client API

You can also use the [data client API](/appendix/apis/data-client/) to upload and export data to and from the Viam app.
This API includes a set of methods for managing data, including export, batch delete, tag, upload, and many more.

## Next steps

Other how-to guides for using and querying data include:

{{< cards >}}
{{% card link="/how-tos/image-data/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{% card link="/how-tos/sensor-data-query-sdk/" %}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{< /cards >}}
