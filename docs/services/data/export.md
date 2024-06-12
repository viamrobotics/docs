---
title: "Export Data"
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
# SME: Alexa Greenberg
---

Download machine data to your computer with the Viam CLI or data client API.

## Export data with the Viam CLI

To export your synced data using the Viam CLI, first [install the Viam CLI](/cli/#install) and [authenticate](/cli/#authenticate) to Viam.

Then, to export data from the data management service in the cloud:

1. Navigate to the [**DATA** page in the Viam app](https://app.viam.com/data/view).
2. Below the **SEARCH** button in the **Filters** panel, click **Copy Export Command** to copy the export command to the clipboard.

   ![The 'copy export command' button from the Viam app.](/services/data/copy_command.png)

3. Run the copied command in a terminal:

   ```sh {class="command-line" data-prompt="$"}
   viam data export --org-ids=<org-id> --data-type=binary --mime-types=<mime types> --destination=.
   ```

   This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

   By default, the command creates two new directories named `data` and `metadata` in the current directory and downloads the specified data into the `data` folder and metadata, like bounding box information and labels, in JSON format into the `metadata` folder.
   If you want to store the data in a different location, change the specified folder with the [`--destination` flag](/cli/#named-arguments).

   Once the command has finished running and downloading the data, you can view and use the data locally.

   Since data is downloaded in parallel, the order is not guaranteed.
   Sort your folder by filename in order to see them in chronological order.

You can see more information about exporting data in the [Viam CLI documentation](/cli/#data).

## Manage data with the data client API

A set of methods using the data client API for managing data, including export, batch delete, tag, and upload functions, are provided in the [Python SDK](https://python.viam.dev).

The following methods are supported by the data client API:

{{< readfile "/static/include/services/apis/data-client.md" >}}

Click on the method name for more information.

## Next steps

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).
