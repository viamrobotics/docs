---
title: "Introduction to the Data Management Service"
linkTitle: "Intro to Data Management"
type: "docs"
description: "Configure data capture and cloud sync, filter and view captured data, and export your data."
image: "/tutorials/data-management/image1.png"
imageAlt: "The data page of the Viam app showing a gallery of the images captured from the Viam Rover."
images: ["/tutorials/data-management/image1.png"]
aliases:
  - "/tutorials/data-management-tutorial/"
  - "/tutorials/data-management/"
  - "/manage/data-management/data-management-tutorial/"
tags: ["data management", "data", "services", "try viam"]
authors: []
languages: []
viamresources: ["data_manager", "camera"]
level: "Intermediate"
date: "2023-02-08"
# updated: ""
cost: "0"
no_list: true
weight: 4
# SMEs: Alexa Greenberg, Natalia Jacobowitz
---

In this tutorial, we will cover how to use Data Management, including capturing camera data, syncing that data from your robot to the cloud, viewing and filtering synced data, and downloading it to your computer.

## Data Management

One key feature of Viam is [Data Management](/manage/data/), which helps you manage data on your robot every step of the way, from capturing component data on your robot, to managing your data securely in the cloud.

Viam's data management service has two distinct parts: data capture and cloud sync.

**Data capture** allows you to capture data from specific components on your robot running Viam.
You can choose the components, corresponding methods, and the frequency of the data capture all within the Viam app.

**Cloud sync** runs in the background and uploads your robot's captured data to Viam's cloud at a defined frequency.
Cloud sync is designed to be resilient and to preserve your data even during a network outage or if your robot has low network bandwidth.
It also manages syncing data from your robot to the Viam app and deletes the captured data from your robot after a successful sync.
Plus, your data is encrypted in transit and at rest in the cloud, so it is always protected.

Data capture is frequently used with data sync.
However, if you want to manage your robot's captured data yourself, it's possible to enable data capture for components on your robot, but disable data sync.

## Requirements

1. **A rented or owned robot**

   Viam's Data Management features will work on any robot running Viam.
   To follow along with this tutorial, you can use one of your own robots, or you can [rent a rover](https://app.viam.com/try) and use it to try out Viam's Data Manager without having to configure your own hardware.

   To learn more about the Try Viam experience, see [Try Viam](/try-viam/).

   {{% alert title="Tip" color="tip" %}}

If you are using your own robot, be sure that you have [`viam-server` installed](/installation/) on your robot.
The data management setup process will be mostly the same, but you will need to substitute your robot's components.

    {{% /alert %}}

1. **Go**

   To use the [data export feature](#export-captured-data), you need to have the <a href="https://go.dev/dl/" target="_blank">Go binary</a> installed on your local development computer.
   We suggest that you install this before your reservation starts to maximize your time with your rover.

## Add the data management service

First, you need to add and configure the data management service to capture data and store it at a specified location.
To enable the data capture on your robot, do the following:

1. On your robot's **Config** page, navigate to the **Services** tab.
2. At the bottom of the page, create a service.
   Choose `Data Management` as the type and specify `viam-data-manager` as the name for your instance of the data management service.
   This service syncs data from your robot to the Viam app in the cloud.
3. Then click **Create Service**.
4. On the panel that appears, you can manage the capturing and syncing functions individually.
   The data management service captures data every 0.1 minutes in the <file>~/.viam/capture</file> directory by default.

   You can leave the default settings as they are.
   Click **Save Config** at the bottom of the window.

![Data Management Card](/tutorials/data-management/data-manager.png)

For more detailed information see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).

## Configure data capture for a component

With the Data Management service added, you can now configure data capture for specific components on your robot running Viam.
You can choose the components, corresponding methods, and the frequency of the data capture all within the Viam app.

{{% alert title="Tip" color="tip" %}}

We're enabling data capture from a camera for this tutorial, but you can enable data capture on most [Viam components](/components/).
This allows you to capture not just image data, but sensor data, robot state data, and so on.

{{% /alert %}}

To enable image data capture for a camera component, follow these steps:

1.  Navigate to the **Components** tab on your robot's **Config** page.
2.  Scroll down to the camera component.
    If you are using a Viam Rover, the camera is named `cam`.
    The camera component has a section labeled **Data Capture Configuration**.
3.  Click `Add Method` to enable data capture for this camera.

    - Set the **Type** to "ReadImage" and the **Frequency** to `0.333`.
      This will capture an image from the camera roughly once every 3 seconds.
      Feel free to adjust the frequency if you want the camera to capture more or less image data.

      {{< alert title="Caution" color="caution" >}}

Avoid configuring data capture to higher rates than your hardware can handle, as this leads to performance degradation.

      {{< /alert >}}

    - Select the MIME type you want to capture.
      Select `image/jpeg` data for this tutorial.

4.  Click **Save Config** at the bottom of the window.

Now your image data will be saved locally on your robot in <file>~/.viam/capture</file>, or whatever directory you configured the captured data from your data management service to be saved to.

![Screenshot from the Viam app showing the data capture settings used for this tutorial.](/tutorials/data-management/image5.png)

{{% alert title="Tip" color="tip" %}}

If you are following along using your own robot, you can confirm that your data is being captured locally.
On your robot, navigate to the <file>~/.viam/capture</file> directory and check for files being created in real-time.

{{% /alert %}}

For more detailed information see [Configure Data Capture](/services/data/configure-data-capture/#configure-data-capture-for-individual-components) and [Configure Cloud Sync](/services/data/configure-cloud-sync/).

## View and filter captured data

Now that you have data capture enabled for a camera on your Viam Rover, you can see the images from your robot in the Viam app.

- Head over to the [**DATA** page](https://app.viam.com/data/view).

- Select `Rover Rental` as the **Location**, and click **SEARCH**.
  If you have data capture set up correctly, you will see the captured images from your rover's camera.

![The data page of the Viam app showing a gallery of the images captured from the Viam Rover.](/tutorials/data-management/image1.png)

For more detailed information see [View and Filter Data](/manage/data/view/).

## Export captured data

You've successfully saved data from your robot in the cloud.
Now, let's export that image data from the Viam app onto your local computer.

First, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam.

Then, to export data from the data management service in the cloud:

1. Navigate to the [**DATA** page in the Viam app](https://app.viam.com/data/view).
2. Below the **SEARCH** button in the **Filtering** panel, click **Copy Export Command** to copy the export command to the clipboard.

   ![The "copy export command" button from the Viam app.](/tutorials/data-management/image4.png)

3. Run the copied command in a terminal:

   ```sh {class="command-line" data-prompt="$"}
   viam data export --org_ids=<org_id> --data_type=binary --mime_types=<mime_types> --destination=.
   ```

   This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.

   Once the command has finished running and downloading the data, you can view and use the data locally in a new directory named <file>data</file>.

   Since images are downloaded in parallel, some may be out of order.
   Sort your folder by filename to see them in chronological order.

For more detailed information see [Export Data](/manage/data/export/).

## Next steps

In this tutorial, you have learned how to use Data Management to capture camera data, sync that data from your robot to the cloud, and view and export the data.

You can now set up data management for your robots to track your robot's usage over time, build dashboards to visualize the data from your robot, or train machine learning models to detect hand gestures or objects.

{{< snippet "social.md" >}}
