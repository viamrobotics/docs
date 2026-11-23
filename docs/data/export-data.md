---
linkTitle: "Export data"
title: "Export data"
weight: 50
layout: "docs"
type: "docs"
description: "Download data from Viam from the DATA page, with the CLI, or with the data client API."
capabilities: ["data-storage"]
diataxis: how-to
tags: ["data management", "cloud", "sync"]
aliases:
  - /data/export/export-data/
  - /data/export-data/
  - /data-ai/data/export/
  - /manage/data/export/
date: "2024-12-03"
updated: "2026-11-07"
---

You can download machine data to your computer from the **DATA** page or with the Viam CLI.

If you prefer to manage your data with code, see the [data client API documentation](/reference/apis/data-client/).

To export a dataset of sequences, see [Export a sequence dataset](/train/create-a-dataset/#export-a-sequence-dataset).

## Download selected items from the DATA page

To download a few images or files:

1. Go to the [**DATA**](https://app.viam.com/data/all) page and open the **Images**, **Media**, **Files**, or **Point clouds** tab.
1. Select the items to download, or click **Select all** to select every item loaded on the tab.
1. Click the **Download** button. Its label names what you selected, for example **Download 3 images**.

A single item downloads as its own file.
Several items download together as one `.tar.gz` archive, which your browser builds in memory, so leaving or refreshing the page cancels the download.
A multi-item download is limited to 500MB in total, and no file in it can be larger than 500MB.
If a selection is over the limit, the **Download** button is disabled; hover over it to see why.
To download a larger file, select it on its own.
To download more data than that, use the CLI as described below.
If some items in a multi-item download can't be fetched, the archive is saved without them, and a warning says how many were left out.

Images download at full resolution, named `<machine>_<component>_<capture time>` with the image's extension.
Other files keep their file name, or use their binary data ID if they don't have one.
If two items in an archive have the same name, later ones get a numbered suffix: `_1`, `_2`, and so on.

## Export data with the Viam CLI

To export your data from the cloud using the Viam CLI, first install and authenticate the CLI:

{{< expand "Install the Viam CLI and authenticate" >}}
Install the Viam CLI using the option below that matches your system architecture:

{{< readfile "/static/include/how-to/install-cli.md" >}}

Then authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}

{{< /expand >}}

Then export the data:

{{< table >}}
{{% tablestep start=1 %}}
**Filter the data you want to download**

Navigate to the [**DATA**](https://app.viam.com/data/all) page.

Use the filters on the left side of the page to filter the data you wish to export.

{{% /tablestep %}}
{{% tablestep %}}
**Copy the export command from the DATA page**

With no items selected, click the **Export** button in the upper right corner of the **DATA** page.

Click **Copy export command**.
This copies the command, including your org ID and the filters you selected, to your clipboard.

{{% /tablestep %}}
{{% tablestep %}}
**Run the command**

Run the copied command in a terminal:

{{< tabs >}}
{{% tab name="Binary data" %}}

```sh {class="command-line" data-prompt="$"}
viam data export binary filter --org-ids=<org-id> --destination=.
```

By default, the command creates two new directories named `data` and `metadata` in the destination directory.
It downloads binary files into the `data` folder and metadata (bounding box information, labels) in JSON format into the `metadata` folder.

Since data is downloaded in parallel, the order is not guaranteed to be chronological.
Sort your files by filename to see them in chronological order.

{{% /tab %}}
{{% tab name="Tabular data" %}}

```sh {class="command-line" data-prompt="$"}
viam data export tabular --destination=. --part-id=<part-id> --resource-name=<resource-name> --resource-subtype=<resource-subtype> --method=<method>
```

The tabular export command writes a single `data.ndjson` file in [NDJSON](https://github.com/ndjson/ndjson-spec) (newline-delimited JSON) format to the destination directory.

{{% /tab %}}
{{< /tabs >}}

If you want to store the data in a different location, change the destination with the [`--destination` flag](/cli/).

{{% /tablestep %}}
{{< /table >}}

You can see more information about exporting data in the [Viam CLI documentation](/cli/).
