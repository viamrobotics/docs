---
title: Data Capture Service Documentation
summary: Explanation of the data capture service, its configuration, its functionality, and its interfaces.
authors:
    - Matt Dannenberg
date: 2022-05-19
---
# Data Manager 
The data manager service supports capturing data from any component at a pre-defined frequency. 

The capture runs in the background and can be set up to 15kHz, depending on the component. If a robot is restarted (with the same config), capture will automatically continue. 

#### Coming Soon
- Cloud Synchronization
- Data Processing for ML model training
- Model to Robot Deployment


## Hardware Requirements
The data manager service supports all of the hardware components on a given robot. Below are some example use cases across different types of hardware: 

- A tomato picking gantry has a depth camera that captures images of crops on the vine. The point cloud data is sent to Viam's cloud platform every 30Hz
- An autonomous delivery base has a GPS that captures its coordinate locations. These coordinate locations are sent to the Viam platform every 15kHZ

## Configuration

In order to use the data capture service, a user needs to add this service to the robots configuration, which is available through the configuration tab of your robot. 

The following configuration parameters are available to you: 

#### General Attributes

| Name          | Config Entry  | Description               | Data Type | Options   |
| ------------- | ------------- | ------------------------- | --------- | ----------|
| capture_dir   | attributes    | Root directory under which captured data is stored | string | Arbitrary directory path

#### Component Attributes

| Name          | Config Entry  | Description               | Data Type | Options   |
| ------------- | ------------- | ------------------------- | --------- | ----------|
| capture_frequency_hz   | component_ attributes    | Frequency at which to capture data | int | Arbitrary directory path | 1-1000 when capture enabled. 0 to disable capture for that robot component |
| method | component_attributes | Component method to capture data from | string | Arm:GetJointPositions or GetEndPosition, Camera: NextPointCloud, Gantry: GetPosition or GetLengths |






