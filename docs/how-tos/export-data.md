---
title: "Export data"
linkTitle: "Export Data"
description: "Download data from the Viam app using the data client API or the Viam CLI."
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
languages: []
---

You can download machine data from cloud storage to your computer with the Viam CLI.

If you prefer to manage your data with code, see the [data client API documentation](/appendix/apis/data-client/).

{{% alert title="In this page" color="tip" %}}

- [Export data with the Viam CLI](#export-data-with-the-viam-cli)

{{% /alert %}}

## Prerequisites

{{< expand "Install the Viam CLI and authenticate." >}}
Install the Viam CLI using the option below that matches your system architecture:

{{< readfile "/static/include/how-to/install-cli.md" >}}

Then authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}

{{< /expand >}}

## Export data with the Viam CLI

To export your data from the cloud using the Viam CLI:

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

This command uses the Viam CLI to download the data onto your computer based on the search criteria you select in the Viam app.

By default, the command creates two new directories named `data` and `metadata` in the current directory and downloads the specified data into the `data` folder and metadata, like bounding box information and labels, in JSON format into the `metadata` folder.
If you want to store the data in a different location, change the specified folder with the [`--destination` flag](/cli/#named-arguments).

Once the command has finished running and downloading the data, you can view and use the data locally.

Since data is downloaded in parallel, the order is not guaranteed.
Sort your folder by filename in order to see them in chronological order.

{{% /tablestep %}}
{{< /table >}}<br>

You can see more information about exporting data in the [Viam CLI documentation](/cli/#data).

## Next steps

Other how-to guides for using and querying data include:

{{< cards >}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/how-tos/sensor-data-visualize/" %}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{< /cards >}}
