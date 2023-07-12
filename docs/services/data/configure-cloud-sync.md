---
title: "Configure Cloud Sync"
linkTitle: "Configure Cloud Sync"
description: "Configure cloud sync to automatically capture data in the Viam app."
weight: 35
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Aaron Casas
---

Before you can configure [cloud sync](../#cloud-sync), you must [add the Data Management Service](../configure-data-capture/#add-the-data-management-service).

To enable cloud sync, navigate to the **Services** tab on your robot's **Config** tab and enable **Syncing** for your [Data Management Service](../).
Click **Save Config** at the bottom of the window.

Now the data that you capture will sync automatically with the Viam app in the cloud.

![data capture configuration](../../../tutorials/img/data-management/data-manager.png)

By default, the Data Management Service syncs data to Viam's cloud every 0.1 minutes, that is every 6 seconds.
To change the sync interval, specify an interval in minutes in the interval field.

{{%expand "Click to view the JSON configuration for the Data Management Service" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [ ],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": ""
      }
    }
  ]
}
```

{{< alert title="Info" color="info" >}}
If `capture_dir` is unspecified, `viam-server` will use the default directory at <file>~/.viam/capture</file>.
{{< /alert >}}

{{% /expand%}}

### Pause sync

You can pause Cloud Sync at any time by navigating to the **Services** tab on your robot's **Config** tab and disabling **Syncing** for your [Data Management Service](../).
If you have captured data that you do not want to sync, delete the data on the robot before resuming Cloud Sync.
To delete the data locally, `ssh` into your robot and delete the data in the directory where you capture data.

## Sync files from another directory

You may have additional files you want to sync to the cloud from your robot.
For example, there may be components on your robot which are not controlled by Viam that are collecting data locally on your robot.
Or there may be a set of logs indicating the status of the robot at different points in time.
To include these types of files in cloud sync, click `ADD PATHWAY` in the Data Management Service panel and specify the directory where your files are located on your robot.
Once you save the configuration, the Data Management Service begins syncing the files in the specified folder at the interval configured for the service.
To avoid syncing files that are still being written to, the Data Management Service only syncs files that haven't been modified in the previous 10 seconds.

{{< alert title="Caution" color="caution" >}}
If a robot does not write to a file for 10 seconds, the Data Management Service syncs the file and deletes it.
{{< /alert >}}

{{< alert title="Info" color="tip" >}}
Currently, if the internet becomes unavailable and the sync is interrupted mid-file, the service resumes sync from the beginning of the file.
This is only applicable for files in a directory added as an additional sync path.
{{< /alert >}}

In the example pictured here, the Data Management Service syncs the configured component data from `/tmp/capture` as well as all files in `/logs` every 5 minutes.

{{< imgproc src="/services/data/data-service-config.png" alt="service config example" resize="1000x" declaredimensions=true >}}

{{%expand "Click to view the JSON configuration for this example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [ ],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 5,
        "capture_dir": "",
        "sync_disabled": false,
        "additional_sync_paths": [
          "/logs"
        ]
      }
    }
  ]
}
```

{{% /expand%}}

## Next Steps

To view your captured data in the cloud, see [View Data](../../../manage/data/view/).

For a comprehensive tutorial on data management, see [Intro to Data Management](../../../tutorials/services/data-management-tutorial/).
