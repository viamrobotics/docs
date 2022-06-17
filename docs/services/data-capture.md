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

#### Component Method Configuration

You configure data capture for each method within a component.

| Name          | Description               | Data Type | Options   |
| ------------- | ------------- | ------------------------- | --------- |
| capture_dir   | Set the root directory for data storage | string | Arbitrary directory path |
| disabled | Disable capture for all components | bool | True, False |
| method | Component method to capture data from | string | Arm: GetJointPositions or GetEndPosition, Camera: NextPointCloud, Gantry: GetPosition or GetLengths |


#### Service Configuration 

| Name          | Description               | Data Type | Options   |
| ------------- | ------------------------- | --------- | ----------|
| capture_dir | The root directory under which captured data should | string | Arbitrary directory path |
| disabled | Disable capture for all components | bool | true, false |




