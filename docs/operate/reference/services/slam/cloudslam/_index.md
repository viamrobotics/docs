---
title: "CloudSLAM Wrapper Modular Resource"
linkTitle: "CloudSLAM"
weight: 70
type: "docs"
description: "Configure a Simultaneous Localization And Mapping (SLAM) service that runs in the cloud using Viam."
tags: ["slam", "services"]
icon: true
images: ["/services/icons/slam.svg"]
date: "2022-01-01"
aliases:
  - /services/slam/cloudslam/
# updated: ""  # When the content was last entirely checked
# SMEs: John N.
---

SLAM Algorithms can have varying levels of resource requirements in order to run effectively.
`Cartographer` in particular can require a significant amount of CPU resources to build and manage large maps.
In order to better support running SLAM on resource limited machines, Viam provides a service to run SLAM algorithms for machines in the cloud as well as management of the maps generated in their location.

CloudSLAM can be used with both a live machine or with previously captured data in your location.
In [live mode](#mapping-with-a-live-machine-online-mode) using the [data management service](/data-ai/capture-data/capture-sync/) and the [cloudslam-wrapper](https://github.com/viam-modules/cloudslam-wrapper) module, Viam takes your LiDAR camera and movement sensor data from your local machine and sends it to the cloudslam server.
The CloudSLAM server will then process that data and produce a map that can then be used on any machine in your location.
When using an [offline machine](#using-previously-captured-data-offline-mode), you can select data from specific sensors over a period of time to build a map with.

You can view and delete maps built in a location by going to the [SLAM library](#the-slam-library-page), which provides a summary of active jobs in the location as well as a list of all maps built in that location.

If you have your own SLAM algorithm that we do not currently support or if you built a map on your local machine already and want to skip running CloudSLAM, you can [upload a locally built map](#upload-a-locally-built-map) to your location using the `cloudslam-wrapper` module.

{{% alert title="About Pricing" color="info" %}}

Running `cloudslam` incurs cost for Data Management, Cloud Data Upload, and Cloud Data Egress. Currently, you incur no cost for compute.
See Viam's [Pricing](https://www.viam.com/product/pricing) for more information.

{{% /alert %}}

### Supported algorithms

Currently CloudSLAM only supports the [cartographer module](../cartographer/) as a SLAM algorithm.

## The SLAM library page

You can see details about the available maps from your machine's **Location** page by clicking **View SLAM library**.
From here, you can find:

1.  A list of all maps generated in that location. The list shows the name and version of the map, which machine was used for mapping, and when the map was created. You can also view previous versions of a map, if a map has been updated multiple times.
    ![offline mapping available maps](/services/slam/offline-mapping-available-maps.png)

2.  You can create or update a map using a previously collected dataset by clicking the **Make new map** on the top right and specify a map name or click **Update map** next to an existing map. See [using previously captured data](#using-previously-captured-data-offline-mode) for more information on how to do this.

3.  A table showing active and failed CloudSLAM sessions.
    The table highlights the name of the map, which machine is currently mapping, and whether the map is in progress or has failed.
    You can also use the table view to stop active mapping sessions.
    ![offline mapping maps computing table](/services/slam/offline-mapping-maps-computing-table.png)

4.  You can view maps in more detail in a dynamic pointcloud viewer by selecting the `View Map` button on one
    ![slam library view map](/services/slam/slam-library-view-map.png)

5.  You can delete maps by clicking on the trash can icon in the upper right-hand corner of a map's card.

## Mapping with a live machine (Online Mode)

To run SLAM in the cloud, configure the [`cloudslam-wrapper`](https://app.viam.com/module/viam/cloudslam-wrapper) module and data capture on your machine.

### Requirements

To use CloudSLAM on a live machine, you must meet the following requirements:

1. A cloudslam supported algorithm must be configured on the machine. Currently only the [cartographer module](../cartographer/) is supported.
   Please configure a supported algorithm on the machine before continuing.

2. A location owner [API key](/manage/manage/access/) or higher.

### Configuration

To use CloudSLAM you must enable data capture and configure your `cloudslam-wrapper` SLAM service:

{{< alert title="Tip: Managing Data Capture" color="tip" >}}
Note that when the [data management service](/data-ai/capture-data/capture-sync/) is enabled, it continuously monitors and syncs your machine’s sensor data while the machine is running.
To avoid incurring charges while not in use, [turn off data capture for your sensors](/data-ai/capture-data/capture-sync/#stop-data-capture-or-data-sync) once you have finished your SLAM session.
{{< /alert >}}

{{< tabs name="Create new map">}}
{{% tab name="Config Builder" %}}

1. Add the data management service to your machine:

   Navigate to the **CONFIGURE** tab of your machine's page.
   Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
   Choose **Data Management** as the type and either use the suggested name or specify a name for your data management service, for example `data_manager-1`.
   Click **Create**.

   On the panel that appears, you can manage the capturing and syncing functions.
   You can also specify the **directory**, the sync **interval**, and any **tags** to apply to captured data.
   See the [data management service](/data-ai/capture-data/capture-sync/) for more information.

2. Enable data capture for your camera, and for your movement sensor if you would like to use IMU data, odometry data, or both:

   Find the component's card on your machine's **CONFIGURE** tab.
   Click **Add Method**, then select the method type and specify the capture frequency.

   - For the required LiDAR camera, choose the `NextPointCloud` method.
     Then set the capture frequency.
     `5 Hz` is a good starting place for most applications.

     {{<imgproc src="/services/slam/rplidar-capture.png" resize="x1100" declaredimensions=true alt="An R P lidar camera configured with next point cloud configured for capture at 5 Hz." class="shadow"  >}}

   - To capture data from one or more movement sensors:

{{< tabs name="Movement sensor options" >}}
{{% tab name="IMU only" %}}

For an IMU, choose the `AngularVelocity` and `LinearAcceleration` methods and set the capture frequency.
`20 Hz` is a good starting place for most applications.

{{<imgproc src="/services/slam/imu-capture.png" resize="x1100" declaredimensions=true alt="An IMU configured with angular velocity and linear acceleration both configured for capture at 20 Hz." class="shadow" >}}

{{% /tab %}}
{{% tab name="Odometry only" %}}

For a movement sensor that supports odometry, choose the `Position` and `Orientation` methods and set the capture frequency.
`20 Hz` is a good starting place for most applications.

{{<imgproc src="/services/slam/odometer-capture.png" resize="x1100" declaredimensions=true alt="A wheeled odometer configured with position and orientation both configured for capture at 20 Hz." class="shadow" >}}

{{% /tab %}}
{{% tab name="Both (merged)" %}}

For a `merged` movement sensor, choose all four methods (`AngularVelocity`, `LinearAcceleration`, `Position`, and `Orientation`) and set the capture frequency.
`20 Hz` is a good starting place for most applications.
You _do not_ need to configure data capture on the individual IMU and odometer.

{{<imgproc src="/services/slam/merged-capture.png" resize="x1100" declaredimensions=true alt="An IMU configured with angular velocity, linear acceleration, position, and orientation all configured for capture at 20 Hz." class="shadow" >}}

{{% /tab %}}
{{< /tabs >}}
<br>

3. Set up the `cloudslam-wrapper` module on your machine:

   Navigate to the **CONFIGURE** tab of your machine's page.

   Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
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

   - `slam_service` is the name of the slam service that you want to run with cloudslam.
   - `api_key` and `api_key_id` are for the location owner API key described in the [requirements](#requirements).
   - `organization_id`, `location_id`, and `machine_id` describe which location and organization you want to run cloudslam in. These are needed so we can fully tie the map you make to the machine running cloudslam.

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
- configures the `viam:slam:cartographer`, `viam:cloudslam-wrapper:cloudslam`, and the [data management](/data-ai/capture-data/capture-sync/) services
- adds a `viam:lidar:rplidar` camera with data capture configured

  ```json {class="line-numbers linkable-line-numbers"}
  {
    "components": [
      {
        "name": "rplidar",
        "api": "rdk:component:camera",
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
        "api": "rdk:service:slam",
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
        "api": "rdk:service:data_manager",
        "model": "rdk:builtin:builtin",
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
        "api": "rdk:service:slam",
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

### Running CloudSLAM

Navigate to the **CONTROL** tab on your machine's page. Then check the following things:

- (optional) change the refresh frequency on the `cartographer` card to **Manual Refresh**. Since you want to use CloudSLAM, you do not need to refresh the underlying SLAM algorithm's map.
- the `cloudslam-wrapper` card should be displaying its default map.

To start the mapping session, do the following:

1. Scroll down to the **DoCommand** card
2. Select your `cloudslam-wrapper` service name from the **Selected component** dropdown

3. In the **Input** section, enter the following command:

   ```json
   { "start": "<MAPPING-SESSION-NAME>" }
   ```

   where `<MAPPING-SESSION-NAME>` is the name you want to give the map you wish to generate.

4. Click the **Execute** button.

   If everything is configured correctly, you should receive a success message.
   The DoCommand card should look something like:
   ![cloudslam wrapper docommand start](/services/slam/cloudslam-module-docommand-start.png)

5. After roughly 1 minute, your map should appear on the `cloudslam-wrapper` card. The displayed map will now update roughly every 5 seconds with the current progress of the mapping session.

You have now successfully built your map using CloudSLAM.
Please review the [tips](../#slam-mapping-best-practices) for making good maps.
![cloudslam wrapper map mapping](/services/slam/cloudslam-module-live-withmap.png)

### Stopping cloudslam

To stop a CloudSLAM mapping session, do the following:

1. Scroll down to the **DoCommand** card
2. Select your `cloudslam-wrapper` service name from the **Selected component** dropdown
3. In the **Input** section, enter the following command:

   ```json
   { "stop": "" }
   ```

   You do not need to specify the map name or job ID here, as the module is already aware of any active mapping sessions for the machine.

4. Click the **Execute** button.
   If everything is configured correctly, you will receive a success message.
   The DoCommand card should look something like:
   ![cloudslam wrapper docommand start](/services/slam/cloudslam-module-docommand-stop.png)

Once completed, you can view the final map in the `cloudslam-wrapper` card, or view the map in the [SLAM library](#the-slam-library-page).

## Using previously captured data (Offline mode)

You can specify a range of **previously captured** LiDAR and optional IMU data to create a map or update an existing map in the cloud.
You can browse your previously captured data from the **Data** page under the **Point clouds** tab (for LiDAR data) and **Sensors** tab (for IMU data).

### Requirements

To create a map, you must have already captured LiDAR data in the location in which you would like to create the map.

The following example shows the previously-captured LiDAR data under the **Point clouds** tab for a machine named `test`.
Selecting a row opens a pane to the right that contains more information, such as the Machine ID of the machine the component belongs to:

{{<imgproc src="/services/slam/offline-mapping-pointcloud-data.png" resize="1200x" declaredimensions=true alt="UI showing captured point clouds">}}

Example of previously captured IMU data:

{{<imgproc src="/services/slam/offline-mapping-imu-data.png" resize="1200x" declaredimensions=true alt="UI showing captured sensor data">}}

### Create or update a map

From your machine's **Location** page, click **View SLAM library**, and click **Make new map** on the top right and specify a map name or click **Update map** next to an existing map.

1. Enter the **Machine name**, **Camera name**, and optionally the **Movement Sensor name** of the components whose previously captured data you want to use to create or update a map.
   If your machine has been deleted, you can alternatively specify the [**machine ID**](/dev/reference/apis/fleet/#find-machine-id).
2. Select the timeframe of the data you'd like to use.
3. At the bottom, you can see the total number of PCD files and movement sensor data points that will be processed.
4. Click **Generate map**.

{{<imgproc src="/services/slam/offline-mapping-generate-map.png" resize="1200x" declaredimensions=true alt="UI for creating a new map from captured data">}}

### End a session with previously captured data

Unlike in `Online` mode, you cannot see the map being created while the slam session is in progress, but similar to when creating or updating a map in `Online` mode, you can see that your cloud slam session is in progress from your **Location** page by clicking **View SLAM library**.
When all the data has been processed (or 45 minutes have passed, whichever occurs first), the map will be saved to your location's **SLAM library**.
You can see details about the it from your machine's **Location** page by clicking **View SLAM library**.

## Upload a locally built map

If you want to skip using CloudSLAM and build the map on your local machine, the [`cloudslam-wrapper`](https://app.viam.com/module/viam/cloudslam-wrapper) module also allows you to upload a locally built map to your **Location**.
This lets you share locally built maps across machines in a location easily.

This feature can also be used with SLAM algorithms that CloudSLAM does not currently support. As long as the algorithm implements the SLAM API, you can upload your maps.

### Requirements

- A SLAM algorithm must be configured on the machine. This algorithm does **not** need to be supported by cloudslam to work.

- A location owner API Key or higher. See [Add an API key](/manage/manage/access/) to learn how to create a key!

### Configuration

Add the `cloudslam-wrapper` module to your machine.
You do **not** need data management configured on the machine.
Configuring the module will not affect any currently running local SLAM maps.
Add the following **Attributes**:

```json
{
  "slam_service": "<slam-service-name>",
  "api_key": "<location-api-key>",
  "api_key_id": "<location-api-key-id>",
  "organization_id": "<organization_id>",
  "location_id": "<location_id>",
  "machine_id": "<machine_id>",
  "machine_part_id": "<machine_part_id>"
}
```

### Upload the map

Navigate to the **CONTROL** tab on your machine's page.

1. Scroll down to the **DoCommand** card
2. Select your `cloudslam-wrapper` service name from the **Selected component** dropdown
3. In the **Input** section, enter the following command:

   ```json
   { "save-local-map": "<MAP-NAME>" }
   ```

   where `<MAP-NAME>` is the name you want to give the map you wish to generate. 4. Click the **Execute** button.
   If everything is configured correctly, you should receive a success message.
   The DoCommand card should look something like:

   ![cloudslam wrapper docommand local upload](/services/slam/cloudslam-module-docommand-local-upload.png)

   Once completed, you can view the final map in the [SLAM library](#the-slam-library-page).

## Attributes

The following attributes are available for `viam:cloudslam-wrapper:cloudslam`

<!-- prettier-ignore -->
| Name    | Type   | Required?    | Description |
| ------- | ------ | ------------ | ----------- |
| `slam_service` | string | **Required** | The name of the SLAM Service on the machine to use with cloudslam. |
| `api_key` | string | **Required** | An [API key](/manage/manage/access/) with location owner or higher permission. |
| `api_key_id` | string | **Required** | The associated API key ID with the API key. |
| `organization_id` | string | **Required** | The organization ID of your [organization](/dev/reference/glossary/#organization). |
| `location_id` | string | **Required** | The location ID of your [location](/dev/reference/glossary/#location). |
| `machine_id` | string | **Required** | The machine ID of your [machine](/dev/reference/apis/fleet/#find-machine-id). |
| `machine_part_id` | string | Optional | The machine part ID of your [machine part](/dev/reference/apis/fleet/#find-machine-id). Used for local package creation and updating mode. |
| `viam_version` | string | Optional | The version of viam-server to use with CloudSLAM. Defaults to `stable`. |
| `slam_version` | string | Optional | The version of cartographer to use with CloudSLAM. Defaults to `stable`. |
| `camera_freq_hz` | float | Optional | The expected capture frequency for your camera/lidar components. Defaults to `5`. |
| `movement_sensor_freq_hz` | float | Optional | The expected capture frequency for your movement sensor components. Defaults to `20`. |
