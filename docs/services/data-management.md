---
title: "Data Management Service"
linkTitle: "Data Management"
weight: 10
type: "docs"
description: "Explanation of the data management service, its configuration and its functionality."
---
The data management service supports capturing data from any component at a predefined frequency and syncing it to Viam's data platform.


## Hardware Requirements
The data management service supports all of the hardware components on a given robot.
Below are some example use cases across different types of hardware: 

- A tomato picking gantry has a depth camera that captures images of crops on the vine.
The point cloud data is collected at 30Hz and sent to Viam's cloud platform every minute.
- An autonomous delivery base has a GPS that captures its coordinate locations.
These coordinate locations are collected at 15kHz and sent to the Viam platform every hour.


## Data Capture
Capture runs in the background.
If a robot is restarted with the same config, capture will automatically continue.


## Data Sychronization to the Cloud
Synchronization runs in the background and is uploaded to Viam's cloud at a predefined frequency.
Files are streamed such that if the internet connection gets interrupted or a robot restarts in the middle of a file upload, synchronization will resume from where it left off mid-file.
If a robot is restarted with the same config, synchronization will automatically continue.
If upload fails, the service will exponentially retry uploading it for up to an hour.

You can also upload any arbitrary files that are not generating via Viam's Data Capture by setting the directories in `additional_sync_paths` in the service configuration.
The example in the next section uploads any new files in `/tmp/my_text_files` on a scheduled interval.

Once a file is synced to Viam's cloud, it is deleted locally off of the robot.

## Service Configuration

In order to use the data management service, you need to add the service to the robot's configuration.
If you're using the "Config > Services" tab on Viam, you'll see that adding a data management service gives you to option to enable capture and syncing.

This example has capture enabled that is writing to `/tmp/capture` on the robot, syncing from that directory every 10 minutes, and additionally syncing any files in `/tmp/my_text_files`

![service config example](../img/data-service-config.png)

In raw JSON, this looks like:
```
"services": [
    {
        "name": "data_manager",
        "type": "data_manager",
        "attributes": {
            "capture_disabled": false,
            "sync_disabled": false,
            "capture_dir": "/tmp/capture",
            "sync_interval_mins": 10,
            "additional_sync_paths": [
                "/tmp/my_text_files"
            ]
        }
    }
}
```

#### Component Method Configuration

You can configure data capture for each method within a component.
If you're using the "Config > Components" tab on Viam, you'll see that a component that has a capturable method will have the option "Data Capture Configuration > Add Method."

Clicking "Add Method" allows you to pick the method name and capture frequency.
You may capture as many methods off of one component as you'd like.
Each method has an "on/off" toggle to enable or disable capture and a "delete" icon to remove it from the configuration.

After adding configuration for the methods, make sure to click the "Save Config" button.

![component config example](../img/data-service-component-config.png)
