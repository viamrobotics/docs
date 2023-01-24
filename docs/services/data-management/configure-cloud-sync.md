---
title: "Configure Cloud Sync"
linkTitle: "Configure Cloud Sync"
weight: 30
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Aaron Casas
---

Before you can configure [cloud sync](../#cloud-sync), you must [add the Data Management Service](../configure-data-capture/#add-the-data-management-service).

To enable cloud sync, navigate to the Services tab on your robot configuration page and enable `Syncing` for your [Data Management Service](../).

By default, the Data Management Service syncs data to Viam's cloud every 5 minutes. To change the sync interval, specify an interval in minutes in the interval field.

The JSON configuration for the Data Management Service is:

```json
{
  "components": [ ],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 5,
        "capture_dir": "/.viam/capture"
      }
    }
  ]
}
```

## Sync files from another directory

You may have additional files you want to sync to the cloud from your robot.
For example, there may be components on your robot which are not controlled by Viam that are collecting data locally on your robot.
Or there may be a set of logs indicating the status of the robot at different points in time.
To include these types of files in cloud sync, click `ADD PATHWAY` in the Data Management Service panel and specify the directory where your files are located on your robot.
Once you save the configuration, the Data Management Service begins syncing the files in the specified folder at the interval configured for the service. To avoid syncing files that are still being written to, the Data Management Service only syncs files that haven't been modified in the previous 10 seconds.

{{< alert title="Caution" color="caution" >}}
If a robot does not write to a file for 10 seconds, the Data Management Service syncs the file and deletes it.
{{< /alert >}}

{{< alert title="Info" color="tip" >}}
Currently, if the internet becomes unavailable and the sync is interrupted mid-file, the service resumes sync from the beginning of the file. This is only applicable for files in a directory added as an additional sync path.
{{< /alert >}}

In the example pictured here, the Data Management Service syncs the configured component data from `/tmp/capture` as well as all files in `/logs` every 5 minutes.

![service config example](../../img/data-service-config.png)

The JSON configuration for this example is:

```json
{
  "components": [ ],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 5,
        "capture_dir": "/.viam/capture",
        "sync_disabled": false,
        "additional_sync_paths": [
          "/logs"
        ]
      }
    }
  ]
}
```
