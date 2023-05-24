---
title: "Export Data"
linkTitle: "Export Data"
weight: 40
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Aaron Casas
---

First, install the [Viam CLI](/manage/cli) and [authenticate](/manage/cli/#authenticate).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go install go.viam.com/rdk/cli/viam@latest
viam auth
```

To export data from the Data Management Service in the cloud:

1. Navigate to the [**DATA** page in the Viam app](https://app.viam.com/data/view).
2. Below the **SEARCH** button in the **Filtering** panel, click **Copy Export Command** to copy the export command to the clipboard.

   ![The "copy export command" button from the Viam app.](../img/copy_command.png)

3. Run the copied command in a terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   go run go.viam.com/rdk/cli/viam data export --org_ids=<org_id> --data_type=binary --mime_types=<mime_types> --destination=.
   ```

   This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

   By default, the command creates a new directory named `data` in the current directory and downloads the specified data.
   If you want to store the data in a different location, change the specified folder with the [`--destination` flag](../../cli/#named-arguments).

   Once the command has finished running and downloading the data, you can view and use the data locally.

   Since data is downloaded in parallel, the order is not guaranteed.
   Sort your folder by filename in order to see them in chronological order.

You can see more information about exporting data in the [Viam CLI documentation](/manage/cli/#data).

## Next Steps

For a comprehensive tutorial on data management, see [Intro to Data Management](../../../tutorials/services/data-management-tutorial).
