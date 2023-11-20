---
title: "Export Data"
linkTitle: "Export Data"
description: "Export data from the data management service."
weight: 40
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Devin Hilly
---

First, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam.

Then, to export data from the data management service in the cloud:

1. Navigate to the [**DATA** page in the Viam app](https://app.viam.com/data/view).
2. Below the **SEARCH** button in the **Filtering** panel, click **Copy Export Command** to copy the export command to the clipboard.

   ![The 'copy export command' button from the Viam app.](/manage/data/copy_command.png)

3. Run the copied command in a terminal:

   ```sh {class="command-line" data-prompt="$"}
   viam data export --org-ids=<org-id> --data-type=binary --mime-types=<mime types> --destination=.
   ```

   This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

   By default, the command creates a new directory named `data` in the current directory and downloads the specified data.
   If you want to store the data in a different location, change the specified folder with the [`--destination` flag](../../cli/#named-arguments).

   Once the command has finished running and downloading the data, you can view and use the data locally.

   Since data is downloaded in parallel, the order is not guaranteed.
   Sort your folder by filename in order to see them in chronological order.

You can see more information about exporting data in the [Viam CLI documentation](/manage/cli/#data).

## Next Steps

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see [Capture Data and Train a Model](/tutorials/services/data-mlmodel-tutorial/).
