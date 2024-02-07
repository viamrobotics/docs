---
title: "Upload and Export Data"
linkTitle: "Upload and Export Data"
description: "Download data from and upload data to the Viam app from your local computer using the data client API, Viam CLI, or Viam mobile app."
weight: 40
type: "docs"
tags: ["data management", "cloud", "sync"]
aliases:
  - /manage/data/export/
# SME: Alexa Greenberg
---

Download machine data to or upload data from your computer with the Viam CLI or data client API.
Also, upload images to the cloud directly through the Viam mobile app.

## Export data with the Viam CLI

To export your synced data using the Viam CLI, first [install the Viam CLI](/fleet/cli/#install) and [authenticate](/fleet/cli/#authenticate) to Viam.

Then, to export data from the data management service in the cloud:

1. Navigate to the [**DATA** page in the Viam app](https://app.viam.com/data/view).
2. Below the **SEARCH** button in the **Filtering** panel, click **Copy Export Command** to copy the export command to the clipboard.

   ![The 'copy export command' button from the Viam app.](/data/copy_command.png)

3. Run the copied command in a terminal:

   ```sh {class="command-line" data-prompt="$"}
   viam data export --org-ids=<org-id> --data-type=binary --mime-types=<mime types> --destination=.
   ```

   This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

   By default, the command creates a new directory named `data` in the current directory and downloads the specified data.
   If you want to store the data in a different location, change the specified folder with the [`--destination` flag](/fleet/cli/#named-arguments).

   Once the command has finished running and downloading the data, you can view and use the data locally.

   Since data is downloaded in parallel, the order is not guaranteed.
   Sort your folder by filename in order to see them in chronological order.

You can see more information about exporting data in the [Viam CLI documentation](/fleet/cli/#data).

## Manage data with the data client API

A set of methods using the data client API for managing data, including export, batch delete, tag, and upload functions, are provided in the [Python SDK](https://python.viam.dev).

The following methods are supported by the data client API:

{{< readfile "/static/include/services/apis/data-client.md" >}}

Click on the method name for more information.

## Upload images with the Viam mobile app

Upload images as machine data straight from your phone, skipping the normal data capture and cloud synchronization process, through the [Viam mobile app](/fleet/#the-viam-mobile-app).
This is useful if you want to capture images for training machine learning models on the go.

1. Select **Home** on the mobile app, choose your organization, and select a location and machine.
2. Then, click the menu button **...** in the upper right corner.
3. Click **Upload Images**.
4. Then, select each image you want to upload, and click **Add**.

As for metadata, these images are associated with this machine part you selected, and aren't associated with a component or method.

## Next steps

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).
