---
title: "Cloudslam Wrapper Modular Resource"
linkTitle: "CloudSLAM"
weight: 70
type: "docs"
description: "Configure a Simultaneous Localization And Mapping (SLAM) service that runs in the cloud using Viam."
tags: ["slam", "services"]
icon: true
images: ["/services/icons/slam.svg"]
aliases:
  - "/services/slam/cloudslam/"
  - "/services/slam/cloud-slam/"
  - "/mobility/slam/cloudslam-wrapper/"
# SMEs: John N.
---

## What is cloudslam

SLAM Algorthims can have varying levels of resource requirements in order to run effectively. `Cartographer` in particular can require a significant amount of CPU resources to build and manage large maps. In order to better support running SLAM on resource limited machines, Viam provides a service to run SLAM algorithms on machines in the cloud as well as management of the maps generated in their location.

Cloudslam can be used with both a live machine or with previously captured data in your `location`. In [live mode](#mapping-with-a-live-machine-online-mode) using the [data management service](/services/data/) and the [cloudslam-wrapper](https://github.com/viam-modules/cloudslam-wrapper) module, Viam takes your LiDAR camera and movement sensor data from your local machine and sends it to the cloudslam server. The cloudslam server will then process that data and produce a map that can then be used on any machine in your `location`. When using an [offline machine](#using-previously-captured-data-offline-mode), users can select data from specific sensors in a period of time to build a map with.

Users can view and delete maps built in their `location` by going to the [SLAM library](#the-slam-library-page), which provides a summary of active jobs in their location as well as a list of all maps built in that location.

If you have your own SLAM algorithm that we do not currently support or if you built a map on your local machine already and want to skip running cloudslam, you can [upload a locally built map](#uploading-a-locally-built-map) to your `location` using the cloudslam-wrapper module.

{{% alert title="About Pricing" color="info" %}}

Running `cloudslam` incurs cost for Data Management, Cloud Data Upload, and Cloud Data Egress. Currently, you incur no cost for compute.
See Viam's [Pricing](https://www.viam.com/product/pricing) for more information.

{{% /alert %}}

### supported algorithms

Currently cloudslam only supports the [cartographer module](../cartographer) as a SLAM algorithm.

## the SLAM Library page

On the robots page in the [Viam app](https://app.viam.com/robots), change the tab from **Machines** to **SLAM Library**. From here, you can find:

1.  A list of all maps generated in that location. The list shows the name and version of the map, which machine was used for mapping, and when the map was created. You can also view previous versions of a map, if a map has been updated multiple times.
    ![offline mapping available maps](/services/slam/offline-mapping-available-maps.png)

2.  You can create or update a map using a previously collected dataset by clicking the **Make new map** on the top right and specify a map name or click **Update map** next to an existing map. See [using previously captured data](#using-previously-captured-data-offline-mode) for more information on how to do this!

3.  A table showing active and failed cloudslam sessions. The table highlights the name of the map, which robot is currently mapping, and whether the map is in progress or has failed. The table can also be used to stop active mapping sessions.
    ![offline mapping maps computing table](/services/slam/offline-mapping-maps-computing-table.png)

4.  You can view maps in more detail in a dynamic pointcloud viewer by selecting the `View Map` button on one
    ![slam library view map](/services/slam/slam-library-view-map.png)

5.  You can delete maps by clicking on the trash can icon in the upper right-hand corner of a map's card.

## Mapping with a live machine (Online Mode)

You can configure the [cloudslam-wrapper](https://github.com/viam-modules/cloudslam-wrapper) module and data capture on your machine to run SLAM in the cloud.

### Requirements

To use cloudslam on a live machine, the following requirements must be met:

1.  A cloudslam supported algorithm must be configured on the machine. Currently this is only the [cartographer module](../cartographer). Please configure a supported algorithm on the machine before continuing.

2.  A location owner API Key or higher. See [Add an API key](/cloud/rbac/#api-keys) to learn how to create a key!

### Configuration

1. Enable data capture and configure your `cloudslam-wrapper` SLAM service:

{{< tabs name="Create new map">}}
{{% tab name="Config Builder" %}}

1. Add the data management service to your machine:

   Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
   Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
   Choose `Data Management` as the type and either use the suggested name or specify a name for your data management service, for example `data_manager-1`.
   Click **Create**.

   On the panel that appears, you can manage the capturing and syncing functions.
   You can also specify the **directory**, the sync **interval**, and any **tags** to apply to captured data.
   See the [data management service](/services/data/) for more information.

2. Enable data capture for your camera, and for your movement sensor if you would like to use IMU data, odometry data, or both:

   Find the component's card on your machine's **CONFIGURE** tab.
   Click `Add Method`, then specify the method type and the capture frequency.

   - For the required LiDAR camera, choose the `NextPointCloud` method.
     Set the capture frequency.
     `5 Hz` is a good starting place for most applications.

     {{<imgproc src="/services/slam/rplidar-capture.png" resize="x1100" declaredimensions=true alt="An R P lidar camera configured in the Viam app config builder with next point cloud configured for capture at 5 Hz." >}}

   - To capture data from one or more movement sensors:

{{< tabs name="Movement sensor options" >}}
{{% tab name="IMU only" %}}

For an IMU, choose the `AngularVelocity` and `LinearAcceleration` methods and set the capture frequency.
`20 Hz` is a good starting place for most applications.

{{<imgproc src="/services/slam/imu-capture.png" resize="x1100" declaredimensions=true alt="An IMU configured in the Viam app config builder with angular velocity and linear acceleration both configured for capture at 20 Hz." >}}

{{% /tab %}}
{{% tab name="Odometry only" %}}

For a movement sensor that supports odometry, choose the `Position` and `Orientation` methods and set the capture frequency.
`20 Hz` is a good starting place for most applications.

{{<imgproc src="/services/slam/odometer-capture.png" resize="x1100" declaredimensions=true alt="A wheeled odometer configured in the Viam app config builder with position and orientation both configured for capture at 20 Hz." >}}

{{% /tab %}}
{{% tab name="Both (merged)" %}}

For a `merged` movement sensor, choose all four methods (`AngularVelocity`, `LinearAcceleration`, `Position`, and `Orientation`) and set the capture frequency.
`20 Hz` is a good starting place for most applications.
You _do not_ need to configure data capture on the individual IMU and odometer.

{{<imgproc src="/services/slam/merged-capture.png" resize="x1100" declaredimensions=true alt="An IMU configured in the Viam app config builder with angular velocity, linear acceleration, position, and orientation all configured for capture at 20 Hz." >}}

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Tip" color="tip" >}}
Note that [Data Capture](/services/data/capture/) continuously monitors and captures your machine’s sensor data while the machine is running. To avoid incurring charges while not in use, [turn off data capture for your sensors](/services/data/capture/) once you have finished your SLAM session.
{{< /alert >}}

3. Set up the `cloudslam-wrapper` module on your machine:

   Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).

   Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
   Select **SLAM**, then select `cloudslam-wrapper`.
   You can also search for "cloudslam".

   Click **Add module**, give your service a name of your choice, then click **Create**.

   In the resulting `SLAM` service configuration pane, add the following **Attributes**:

   ```json
   {
     "slam_service": "<slam-service-name>",
     "api_key": "<location-api-key>",
     "api_key_id": "<location-api-key-id>",
     "organization_id": "<organization_id>",
     "location_id": "<location_id>",
     "machine_id": "<machine_id>"
   }
   ```

   where

   - `slam_service` is the name of the slam service that you want to run with cloudslam
   - `api_key` and `api_key_id` are for the location owner API key described in the [requirements](#requirements)
   - `organization_id`, `location_id`, and `machine_id` describe which location & organization you want to run cloudslam in. These are needed so we can fully tie the map you make to the machine running cloudslam.

4. (Optional) configure the `cloudslam-wrapper` to use updating mode.
   If you want cloudslam to update a `slam_map` rather than create a new map, do the following:

   - configure the `slam_map` on your wrapped SLAM service
   - add a `machine_part_id` to your `cloudslam-wrapper` config.

   This informs the module to use the configured `slam_map` on your machine.

5. Configure Cartographer to use cloudslam.

   In your `cartographer` config card, click the **{}** button to switch to advanced views and set the `use_cloud_slam` field to **true**. This setting disables local mapping to limit cpu usage in favor of using cloudslam.

{{% /tab %}}
{{% tab name="JSON Example" %}}

This example JSON configuration:

- adds the `viam:rplidar`, `viam:cartographer`, and `viam:cloudslam-wrapper` modules
- configures the `viam:slam:cartographer`, `viam:cloudslam-wrapper:cloudslam`, and the [data management](/services/data/) services
- adds a `viam:lidar:rplidar` camera with data capture configured

  <br>

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "rplidar",
      "namespace": "rdk",
      "type": "camera",
      "model": "viam:lidar:rplidar",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "NextPointCloud",
                "capture_frequency_hz": 5,
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
  "services": [
    {
      "name": "carto",
      "namespace": "rdk",
      "type": "slam",
      "model": "viam:slam:cartographer",
      "attributes": {
        "enable_mapping": true,
        "use_cloud_slam": true,
        "existing_map": "",
        "camera": {
          "data_frequency_hz": "5",
          "name": "rplidar"
        }
      }
    },
    {
      "name": "data_manager-1",
      "namespace": "rdk",
      "type": "data_manager",
      "attributes": {
        "capture_dir": "",
        "capture_disabled": false,
        "sync_disabled": false,
        "tags": [],
        "additional_sync_paths": [],
        "sync_interval_mins": 0.1
      }
    },
    {
      "name": "cloudslam",
      "namespace": "rdk",
      "type": "slam",
      "model": "viam:cloudslam-wrapper:cloudslam",
      "attributes": {
        "slam_service": "carto",
        "api_key": "<location-api-key>",
        "api_key_id": "<location-api-key-id>",
        "organization_id": "<organization_id>",
        "location_id": "<location_id>",
        "machine_id": "<machine_id>",
        "machine_part_id": "<machine-part-id>"
      }
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.16"
    },
    {
      "type": "registry",
      "name": "viam_cartographer",
      "module_id": "viam:cartographer",
      "version": "0.3.45"
    },
    {
      "type": "registry",
      "name": "viam_cloudslam-wrapper",
      "module_id": "viam:cloudslam-wrapper",
      "version": "0.0.3"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

For more information about the configuration attributes, see [Attributes](#attributes).

### Running cloudslam

Navigate to the **CONTROL** tab on your machine's page. A few things should be happening:

- (optional) change the refresh frequency on the `cartographer` card to **Manual Refresh**. Since we want to use cloudslam, we do not need to refresh the underlying SLAM algorithm's map.
- the `cloudslam-wrapper` card should be displaying its default map. this will look something like
  ![default cloudslam wrapper map](/services/slam/cloudslam-module-live-default.png)

To start the mapping session, do the following:

1. Scroll down to the **DoCommand** card
2. Select your `cloudslam-wrapper` service name from the **Selected component** dropdown
3. In the **Input** section, enter the following command:

```json
{ "start": "<MAPPING-SESSION-NAME>" }
```

where `<MAPPING-SESSION-NAME> is the name you want to give the map you wish to generate. 4. Click the **Execute** button.
If everything is configured correctly, you should recieve a success message. The DoCommand card should look something like:
![cloudslam wrapper docommand start](/services/slam/cloudslam-module-docommand-start.png)

5. After roughly 1 minute, your map should appear on the `cloudslam-wrapper` card. The displayed map will now update roughly every 5 seconds with the current progress of the mapping session. You can now build your map using cloudslam! Please review our [tips](../#slam-mapping-best-practices) in order to help make a good map!
   ![cloudslam wrapper map mapping](/services/slam/cloudslam-module-live-withmap.png)

### Stopping cloudslam

To Stop a cloudslam mapping session, do the following:

1. Scroll down to the **DoCommand** card
2. Select your `cloudslam-wrapper` service name from the **Selected component** dropdown
3. In the **Input** section, enter the following command:

```json
{ "start": "<MAPPING-SESSION-NAME>" }
```

You do not need to specify the map name or job id here, as the module should already be aware of any active mapping sessions for the machine

4. Click the **Execute** button.
   If everything is configured correctly, you should recieve a success message. The DoCommand card should look something like:
   ![cloudslam wrapper docommand start](/services/slam/cloudslam-module-docommand-stop.png)

and thats all! You can view the final map in the `cloudslam-wrapper` card, or view the map in the [SLAM library](#the-slam-library-page)

## using previously captured data (Offline mode)

You can specify a range of **previously captured** LiDAR and optional IMU data to create a map or update an existing map in the cloud.
You can browse your previously captured data from the **Data** page under the **Point clouds** tab (for LiDAR data) and **Sensors** tab (for IMU data).

### Requirements

To create a map, you must have already captured LiDAR data in the location in which you would like to create the map.

The following example shows the previously-captured LiDAR data under the **Point clouds** tab for a machine named `test`.
Selecting a row opens a pane to the right that contains more information, such as the `Machine ID` of the machine the component belongs to:

{{<imgproc src="/services/slam/offline-mapping-pointcloud-data.png" resize="1200x" declaredimensions=true alt="UI showing captured point clouds">}}

Example of previously captured IMU data:

{{<imgproc src="/services/slam/offline-mapping-imu-data.png" resize="1200x" declaredimensions=true alt="UI showing captured sensor data">}}

### Create or update a map

Navigate to the **SLAM library** tab on your location page, and click **Make new map** on the top right and specify a map name or click **Update map** next to an existing map.

1. Enter the **Machine name**, **Camera name**, and optionally the **Movement Sensor name** of the components whose previously captured data you want to use to create or update a map.
   If your machine has been deleted, you can alternatively specify the [**machine ID**](/appendix/apis/fleet/#find-machine-id).
2. Select the timeframe of the data you'd like to use.
3. At the bottom, you can see the total number of PCD files and movement sensor data points that will be processed.
4. Click **Generate map**.

{{<imgproc src="/services/slam/offline-mapping-generate-map.png" resize="1200x" declaredimensions=true alt="UI for creating a new map from captured data">}}

### Ending a session with previously captured data

Unlike in `Online` mode, you cannot see the map being created while the slam session is in progress, but similar to when creating or updating a map in `Online` mode, you can see that your cloud slam session is in progress from your **Location** page's **SLAM library** tab.
When all the data has been processed (or 45 minutes have passed, whichever occurs first), the map will be saved to your **Location** page's **SLAM library** tab.

## uploading a locally built map

If you want to skip using cloudslam and build the map on your local machine, the [cloudslam-wrapper](https://github.com/viam-modules/cloudslam-wrapper) module also allows you to upload that locally built map to your **Location**. This lets you share that map accross robots on within your fleet easily.

This feature can also be used with SLAM algorithms that cloudslam does not currently support. As long as the algorithm implements the SLAM API, you can upload your maps.

### Requirements

1.  A SLAM algorithm must be configured on the machine. This algorithm does **not** need to be supported by cloudslam to work.

2.  A location owner API Key or higher. See [Add an API key](/cloud/rbac/#api-keys) to learn how to create a key!

### Configuration

1.  Add the `cloudslam-wrapper` module to your machine. You do not need data management configured on the machine. Configuring the module should not affect any currently running local SLAM maps. Add the following **Attributes**:

````json
 {
 "slam_service": "<slam-service-name>",
 "api_key": "<location-api-key>",
 "api_key_id": "<location-api-key-id>",
 "organization_id": "<organization_id>",
 "location_id": "<location_id>",
 "machine_id": "<machine_id>",
 "machine_part_id": "<machine_part_id>",
 }
 ```
### Upload the map

Navigate to the **CONTROL** tab on your machine's page.

1. Scroll down to the **DoCommand** card
2. Select your `cloudslam-wrapper` service name from the **Selected component** dropdown
3. In the **Input** section, enter the following command:

```json
{"save-local-map": "<MAP-NAME>"}
````

where `<MAP-NAME> is the name you want to give the map you wish to generate. 4. Click the **Execute** button. If everything is configured correctly, you should recieve a success message. The DoCommand card should look something like:
![cloudslam wrapper docommand local upload](/services/slam/cloudslam-module-docommand-local-upload.png)

and thats all! You can view the map in the [SLAM library](#the-slam-library-page)!

## Attributes

The following attributes are available for `viam:cloudslam-wrapper:cloudslam`

<!-- prettier-ignore -->
| Name    | Type   | Required?    | Description |
| ------- | ------ | ------------ | ----------- |
| `slam_service` | string | **Required** | Name of the SLAM Service on the machine to use with cloudslam        |
| `api_key` | string | **Required**     | [location owner API key](/cloud/rbac/#api-keys) needed to use cloudslam apis        |
| `api_key_id` | string | **Required**     | location owner API key id        |
| `organization_id` | string | **Required**     | id string for your [organization](/cloud/organizations/)        |
| `location_id` | string | **Required**     | id string for your [location](/cloud/locations/)        |
| `machine_id` | string | **Required**     | id string for your [machine](/appendix/apis/fleet/#find-machine-id)        |
| `machine_part_id` | string | Optional     | optional id string for the [machine part](/appendix/apis/fleet/#find-machine-id). Used for local package creation and updating mode       |
| `viam_version` | string | Optional     | optional string to identify which version of viam-server to use with cloudslam. Defaults to `stable`        |
| `slam_version` | string | Optional     | optional string to identify which version of cartographer to use with cloudslam. Defaults to `stable`         |
| `camera_freq_hz` | float | Optional     | set the expected capture frequency for your camera/lidar components. Defaults to `5`        |
| `movement_sensor_freq_hz` | float | Optional     | set the expected capture frequency for your movement sensor components. Defaults to `20`        |
