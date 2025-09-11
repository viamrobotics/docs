---
linkTitle: "Export data"
title: "Export data"
weight: 40
description: "Download data from Viam using the data client API or the CLI."
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: true
images: ["/services/icons/data-capture.svg"]
aliases:
  - /manage/data/export/
  - /data/export/
  - /services/data/export/
  - /how-tos/export-data/
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "cli"]
date: "2024-12-03"
---

You can download machine data from cloud storage to your computer with the Viam CLI.

If you prefer to manage your data with code, see the [data client API documentation](/dev/reference/apis/data-client/).

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
{{% tablestep start=1 %}}
**Filter the data you want to download**

Navigate to the [**DATA**](https://app.viam.com/data/view) page.

Use the filters on the left side of the page to filter only the data you wish to export.

{{% /tablestep %}}
{{% tablestep %}}
**Copy the export command from the DATA page**

In the upper right corner of the **DATA** page, click the **Export** button.

Click **Copy export command**.
This copies the command, including your org ID and the filters you selected, to your clipboard.

{{% /tablestep %}}
{{% tablestep %}}
**Run the command**

Run the copied command in a terminal:

```sh {class="command-line" data-prompt="$"}
viam data export --org-ids=<org-id> --data-type=<binary|tabular> --mime-types=<mime types> --destination=.
```

This command uses the Viam CLI to download the data onto your computer based on the search criteria you select in the web UI.

By default, the command creates two new directories named `data` and `metadata` in the current directory and downloads the specified data into the `data` folder and metadata, like bounding box information and labels, in JSON format into the `metadata` folder.
If you want to store the data in a different location, change the specified folder with the [`--destination` flag](/dev/tools/cli/#named-arguments).

Once the command has finished running and downloading the data, you can view and use the data locally.

Since data is downloaded in parallel, the order is not guaranteed.
Sort your folder by filename in order to see them in chronological order.

{{% /tablestep %}}
{{< /table >}}<br>

You can see more information about exporting data in the [Viam CLI documentation](/dev/tools/cli/#data).
