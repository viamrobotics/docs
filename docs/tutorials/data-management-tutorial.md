---
title: "An Introduction to Using Viam's Data Management Service"
linkTitle: "Intro to Data Management"
weight: 60
type: "docs"
description: "Configure data capture and cloud sync, filter and view captured data, and export your data."
tags: ["data management", "data", "services", "try viam"]
# SMEs: Alexa Greenberg, Natalia Jacobowitz
---

One key feature of Viam is [Data Management](/manage/data-management/), which helps you manage data on your robot every step of the way, from capturing component data on your robot, to managing your data securely in the cloud.

Viam's Data Management Service has two distinct parts: [data capture](#add-the-data-management-service) and [cloud sync](#enable-cloud-sync).

**Data capture** allows you to capture data for specific components on your robot running Viam.
You can choose the components, corresponding methods, and the frequency of the data capture all within the Viam app.

**Cloud sync** runs in the background and uploads your robot's captured data to Viam's cloud at a defined frequency.
Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your robot has low network bandwidth.
It also manages syncing data from your robot to the Viam app and deletes the captured data from your robot after a successful sync.
Plus, your data is encrypted in transit and at rest in the cloud, so it is always protected.

Data capture is frequently used with data sync.
However, if you want to manage your robot's captured data yourself, it's possible to enable data capture for components on your robot, but disable data sync.

In this tutorial, we will cover how to use Data Management, including capturing camera data, syncing that data from your robot to the cloud to be able to view and filter through it, and downloading it to your computer.

### Requirements

1. **A rented or owned robot**

   Viam's Data Management features will work on any robot running Viam.
   To follow along with this tutorial, you can use one of your own robots or you can [rent a rover](https://app.viam.com/try) and use it to try out Viam's Data Manager without having to configure your own hardware.

   To learn more about the Try Viam experience, see [Try Viam](/try-viam/).

    {{% alert title="Note" color="note" %}}

If you are using your own robot, be sure that you have [`viam-server` installed](/installation/) on your robot.
The data management setup process will be mostly the same, but you will need to substitute your robot's components.

    {{% /alert %}}

1. **Go**

    To use the [data export feature](#export-captured-data), you need to have the <a href="https://go.dev/dl/" target="_blank">Go binary</a> installed on your local development computer.
    We suggest that you install this before your reservation starts to maximize your time with your rover.

## Add the Data Management Service

First, you need to add and configure the Data Management Service to capture data and store it at a specified location.
To enable the data capture on your robot, do the following:

1. On your robot's **CONFIG** page, navigate to the **SERVICES** tab.
2. At the bottom of the page, create a service.
   Choose `Data Management` as the type and specify `viam-data-manager` as the name for your instance of the Data Management Service.
   This service syncs data from your robot to the Viam app in the cloud.
3. Then click **Create Service**.
4. On the panel that appears, you can manage the capturing and syncing functions individually.
   The Data Management Service captures data every 5 minutes in the <file>/.viam/capture</file> directory by default.

   Set the **Interval** to **1** min.
   You can leave the default directory in which your captured data is stored on-robot.
   By default, it saves it to the <file>/.viam/capture</file> directory on your robot.
5. Click **Save Config** at the bottom of the window.

![Screenshot from the Data Management Service showing the Data Capture option enabled and the cloud sync option disabled.](../img/data-management/image3.png)

For more detailed information see [Add the Data Management Service](../../manage/data-management/configure-data-capture/#add-the-data-management-service).

## Configure data capture for a component

With data capture enabled, you can now configure data capture for specific components on your robot running Viam.
You can choose the components, corresponding methods, and the frequency of the data capture all within the Viam app.

{{% alert title="Tip" color="tip" %}}

We're enabling data capture from a camera for this tutorial, but you can enable data capture on most [Viam components](/components/).
This allows you to capture not just image data, but sensor data, robot state data, and so on.

{{% /alert %}}

To enable image data capture for a camera component, follow these steps:

1. Navigate to the **COMPONENTS** tab on your robot's **CONFIG** page.
2. Scroll down to the camera component.
   (On the Viam Rover, the camera is named `cam`.)
   The camera component has a section labeled **Data Capture Configuration**.
3. Click `Add Method` to enable data capture for this camera.

   - Set the **Type** to "ReadImage" and the **Frequency** to `0.333`.
     This will capture an image from the camera roughly once every 3 seconds.
     Feel free to adjust the frequency if you want the camera to capture more or less image data.
   - You should also select the MIME type that you want to capture.
     For this tutorial, we are capturing `image/jpeg` data.

4. Click **Save Config** at the bottom of the window.

Now your image data will be saved locally on your robot in <file>/.viam/capture</file>, or whatever directory you configured the captured data from your Data Management Service to be saved to.

![Screenshot from the Viam app showing the data capture settings used for this tutorial.](../img/data-management/image5.png)

{{% alert title="Tip" color="tip" %}}

If you are following along using your own robot, you can confirm that your data is being captured locally.
On your robot, navigate to the <file>/.viam/capture</file> directory and check for files being created in real-time.

{{% /alert %}}

For more detailed information see [Configure Data Capture](../../manage/data-management/configure-data-capture/#configure-data-capture-for-individual-components).

## Enable cloud sync

Enabling cloud sync allows you to securely access all your robot's data in the Viam app in the cloud.
To enable cloud sync on your robot, do the following:

- Navigate to the **CONFIG** tab, then select **SERVICES**.
- Navigate to [the Data Management Service you created above](#add-the-data-management-service).
- In the **Cloud Sync** section, enable **Syncing**.
- Click **Save Config** at the bottom of the window.

![Screenshot from the Data Management Service showing the Data Capture and the cloud sync option enabled.](../img/data-management/image2.png)

Now the data that you capture locally will sync automatically with the Viam app in the cloud.

For more detailed information see [Configure Cloud Sync](../../manage/data-management/configure-cloud-sync/).

## View and filter captured data

Now that you have data capture enabled for a camera on your Viam Rover, you can see the images from your robot in the Viam app.

- Head over to the [**DATA** page](https://app.viam.com/data/view).

- Select `Rover Rental` as the **Location**, and click **SEARCH**.
  If you have data capture set up correctly, you will see the captured images from your rover's camera.

![The data page of the Viam app showing a gallery of the images captured from the Viam Rover.](../img/data-management/image1.png)

For more detailed information see [View and Filter Data](../../manage/data-management/view/).

## Export captured data

You've successfully saved data from your robot in the cloud.
Now, let's export that image data from the Viam app onto your local computer.

To export data from Viam:

1. First, install the [Viam CLI](/manage/cli) and [authenticate](/manage/cli/#authenticate):

   ```sh
   go install go.viam.com/rdk/cli/cmd@latest
   viam auth
   ```

2. Head back to the [**DATA** page in the Viam app](https://app.viam.com/data/view).
3. Below the **SEARCH** button in the **FILTERING** panel, click **COPY EXPORT COMMAND** to copy the export command to the clipboard.

   ![The "copy export command" button from the Viam app.](../img/data-management/image4.png)

4. Run the copied command in a terminal:

   ```sh
   go run go.viam.com/rdk/cli/viam data export --org_ids=<org_id> --data_type=binary --mime_types=<mime_types> --destination=.
   ```

   This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

   Once the command has finished running and downloading the data, you can view and use the data locally in a new directory named <file>data</file>.

   Since images are downloaded in parallel, some may be out of order.
   Sort your folder by filename in order to see them in chronological order.

For more detailed information see [Export Data](../../manage/data-management/export/).

## Next steps

In this tutorial, you have learned how to use Data Management to capture camera data, sync that data from your robot to the cloud, and view and export the data.

You can now set up data management for your robots to track your robot's usage over time, build dashboards to visualize the data from your robot, or train machine learning models to detect hand gestures or objects.

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, head over to the <a href="https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw" target="_blank">Viam Community Slack</a>.
