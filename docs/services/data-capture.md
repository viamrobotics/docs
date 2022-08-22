---
title: Data Capture Service Documentation
summary: Explanation of the data capture service, its configuration, its functionality, and its interfaces.
authors:
    - Matt Dannenberg
date: 2022-05-19
---
# Data Manager 
The data manager service supports capturing data from any component at a pre-defined frequency.

The capture runs in the background and can be set as high as 15kHz, depending on the component.
If a robot is restarted (with the same config), capture resumes automatically.

The service also supports syncing captured data to the Viam Cloud at a predefined frequency or on-demand via the Sync() endpoint. Synchronization runs in the background, and if a robot is restarted (with the same config), synchronization at a predefined frequency will automatically continue. 


#### Coming Soon
- Data Processing for ML model training
- Model to Robot Deployment


## Hardware Requirements
The data manager service supports all of the hardware components on a given robot.
Below are some example use cases across different types of hardware: 

- A tomato picking gantry has a depth camera that captures images of crops on the vine.
The point cloud data is sent to Viam's cloud platform every 30Hz.
- An autonomous delivery base has a GPS that captures its coordinate locations.
These coordinate locations are sent to the Viam platform every 15kHZ.

## Configuration

To use the data capture service, the user must add this service to the robot's configuration, which is available through the robot's configuration tab in the [Viam App (https://app.viam.com)](https://app.viam.com).

The following configuration parameters are available to you: 

### Component Method Configuration

You must configure data capture for each method within a component.

<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Data Type</th>
        <th>Options</th>
    </tr>
    <tr>
        <td>capture_frequency_hz</td>
        <td>Frequency at which to capture data.</td>
        <td>int</td>
        <td>1-1000 when capture enabled.</td>
    </tr>
    <tr>
        <td>capture_disabled</td>
        <td>Disable capture for all components</td>
        <td>bool</td>
        <td>True, False</td>
    </tr>
    <tr>
        <td>method</td>
        <td>Component method to capture data from</td>
        <td>string</td>
        <td>Arm: GetJointPositions or GetEndPosition, <br>Camera: NextPointCloud, <br>Gantry: GetPosition or GetLengths</td>
    </tr>
</table>
<p class="Mycaption" ><em>Figure 1: The Viam App's Component Tab Capture Configuration.</em>
<img src="../img/data-cap-cap-config.png" width="600" /></p>


### Service Configuration 

<p class="Mycaption" ><em>Figure 2: The Viam App's Data Management Panel.</em>
<img src="../img/data-cap-dm-panel.png" width="600" /></p>

### Data Capture Attributes

<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Data Type</th>
        <th>Options</th>
    </tr>
    <tr>
        <td>capture_dir</td>
        <td>The root directory under <br>which captured data should be stored.</td>
        <td>string</td>
        <td>Arbitrary directory path</td>
    </tr>
    <tr>
        <td>capture_disabled</td>
        <td>Disable capture for all components</td>
        <td>bool</td>
        <td>true, false</td>
    </tr>
    <tr>
        <td>sync_disabled</td>
        <td>Disable sync for all components</td>
        <td>bool</td>
        <td>true, false</td>
    </tr>
        <tr>
        <td>sync_interval_mins</td>
        <td>Frequency of syncing to cloud</td>
        <td>int</td>
        <td>-</td>
    </tr>
            <tr>
        <td>additional_sync_paths</td>
        <td>Any arbitrary files to sync to the cloud,<br> in addition to what has been captured<br> via capture service configuration</td>
        <td>string array</td>
        <td>List of files and/or<br> directories on robot</td>
    </tr>      
</table>

### Example Configuration

The following are examples of the data capture configurations for two arms and a camera:

````JSON
{
   "components": [
   {
       "model": "ur",
       "name": "arm1",
       "type": "arm",
       "service_config": [
           {
               "type": "data_manager",
               "attributes": {
                   "capture_methods": [
                       {
                           "method": "GetJointPositions",
                           "capture_frequency_hz": 1000
                       },
                       {
                           "method": "GetEndPosition",
                           "capture_frequency_hz": 1000
                       }
                   ]
               }
           }
       ]
   },
{
       "model": "ur",
       "name": "arm2",
       "type": "arm",
       "service_config": [
           {
               "type": "data_manager",
               "attributes": {
                   "capture_methods": [
                       {
                           "method": "GetJointPositions",
                           "capture_frequency_hz": 1000
                       },
                       {
                           "method": "GetEndPosition",
                           "capture_frequency_hz": 1000
                       }
                   ]
               }
           }
       ]
   },
   {
       "model": "camera",
       "name": "camera1",
       "type": "single_stream",
       "service_config": [
           {
               "type": "data_manager",
               "attributes": {
                   "capture_methods": [
                       {
                           "method": "NextPointCloud",
                           "capture_frequency_hz": 10
                       }
                   ]
               }
           }
       ]
   },
   "services": [
      {
          "type": "data_manager",
          "attributes": {
              "capture_dir": "capture"
          }
      }
   ]
}

````

## Accessing the Data
Before being synced to the cloud, the data data for each part of your robot is written to a file within your configured capture_dir. If capture_dir is set to `capture` and you are capturing data from the above arms and camera, the pathspec and data file names are: 

* capture/arm/arm1/{START_TIMESTAMP}
* capture/arm/arm2/{START_TIMESTAMP}
* capture/camera/camera1/{START_TIMESTAMP}

Each of these files store encoded <a href="https://developers.google.com/protocol-buffers" target="_blank">protocol buffer</a>[^pbf] timestamped messages.
[^pbf]:Protocol Buffers: <a href="https://developers.google.com/protocol-buffers" target="_blank">https://developers.google.com/protocol-buffers</a>

### Syncing the Data to the Cloud

#### Service Configuration

##### Attributes

<table style="width:70% word-wrap:break-word" >
    <tr>
        <td>Name</td>
        <td>Description</td>
        <td>Data Type</td>
        <td>Options</td>
    </tr>
    <tr>
        <td>sync_interval_mins</td>
        <td>How often to sync data to the cloud,<br> in minutes.</td>
        <td>int</td>
        <td>[1, inf]</td>
    </tr>
    <tr>
        <td>additional_sync_paths</td>
        <td>Any arbitrary files to sync to the cloud,<br> in addition to what has been captured<br> via capture service configuration.</td>
        <td>string array</td>
        <td>List of files and/or<br> directories on robot</td>
    </tr>
    <tr>
        <td>sync_disabled</td>
        <td>Disable sync for all components</td>
        <td>bool</td>
        <td>True, false</td>
    </tr>
</table>