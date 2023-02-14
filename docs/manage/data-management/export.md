---
title: "Export data from Viam's data platform"
linkTitle: "Export Data"
weight: 40
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Aaron Casas
---

Prior to exporting data for the first time, verify that Go is installed.
Then, to export data:

1. Install the [Viam CLI](/manage/cli/) and [authenticate](/manage/cli/#authenticate).

2. Below the **SEARCH** button in the **FILTERING** panel, click **COPY EXPORT COMMAND** to copy the export command to the clipboard.

3. Paste the command into your terminal and press Enter.
   While the default command exports data to the directory location specified by the `--destination=.` flag, you can also specify an absolute directory path.

   The following command downloads all image data from December 2022 to `/tmp/dec22_robot`. The image data to  `/tmp/dec22_robot/data` and capture metadata to `/tmp/dec22_robot/metadata`

    ```bash
    viam data export \
    --component_type=camera \
    --org_ids=1cewfi124ewff \
    --data_type=binary \
    --mime_types=image/jpeg,image/png \
    --start=2022-12-01T05:00:00.000Z \
    --end=2023-01-01T05:00:00.000Z \
    --destination=/tmp/dec22_robot
    ```

You can see more information about exporting data in the [Viam CLI documentation](/manage/cli/#data).
