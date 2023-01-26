---
title: "An Introduction to Using Viam's Data Management Service"
linkTitle: "Intro to Data Management"
weight: 60
type: "docs"
description: "Learn how to use Viam's Data Management service including configuring data capture and sync, filtering and viewing captured data, and exporting your data locally."
tags: ["data management", "data", "services", "try viam"]
# SMEs: Alexa Greenberg, Natalia Jacobowitz, Joe Karlsson
---

## Introduction

One key feature of Viam is the included [Data Management service](/services/data-management/), which helps you manage data on your robot every step of the way, from capturing component data on your robot, to managing your data securely in the cloud.

Viam's Data Management service has two distinct parts: [data capture](#enabling-data-capture-with-the-data-management-service) and [data sync](#enabling-cloud-sync-on-the-data-management-service).

**Data capture** allows you to capture data for specific components on your robot running Viam.
You can choose the components, corresponding methods, and the frequency of the data capture all within the Viam app.

**Data synchronization** runs in the background and uploads your robot's captured data to Viam's cloud at a predefined frequency.
Data sync is designed to be resilient and to preserve your data even during a network outage or if your robot has low network bandwidth.
It also manages syncing data from your robot to the Viam app and deletes the captured data from your robot after a successful sync.
Plus, your data is encrypted in transit and at rest in the cloud, so you can be sure that your data is protected while using data sync with Viam.

Data capture is frequently used with data sync.
However, if you want to manage your robot's captured data yourself, it's possible to enable data capture for components on your robot, but disable data sync.

In this tutorial, we will cover the basics of using Viam's Data Management service including capturing camera data, syncing that data from your robot to the cloud to be able to view and filter through it, and downloading it locally.

### Prerequisites

We recommend that you use the <a href="https://app.viam.com/try" target="_blank">Try Viam Rover</a> as a quick way to get started and to try out Viam's Data Manager.
You can learn more about the Try Viam experience at [/try-viam/](/try-viam/), and you can sign up for a 15 minute reservation slot at <a href="https://app.viam.com/try" target="_blank">app.viam.com/try</a>.

{{% alert title="Note" color="note" %}}

You do not need to use a Viam Rover to follow along with this tutorial.
Viam's Data Management features will work on any robot running Viam.
If you are using your own robot, be sure that you have Viam installed on your robot.
The data management setup process will be mostly the same, but you will need to substitute your robot's components.

{{% /alert %}}

If you are planning on following along with and using the [data export feature to download data captured from your robot locally](#exporting-captured-data-from-the-viam-app), you will also need to install the <a href="https://go.dev/dl/" target="_blank">Golang binary</a> on your local development computer.
We suggest that you install this before your reservation starts to maximize your time with your rover.

## Enabling data capture with the Data Management service

First, you'll want to configure Viam's Data Management service so you can specify the location on the robot to store data.
You will also enable data capture for your robot, and in the next step, you will configure data capture for a camera component on your robot.
To enable the data capture on your robot, do the following:

- Under the **CONFIG** tab, select **SERVICES**, and navigate to **Create Service**.
Here, you will add a service so your robot can sync data to the Viam app in the cloud.

- For "type", select "Data Manager" from the drop-down, and give your service a name.
We used "viam_data_manager" for this tutorial.

- Be sure that Data Capture is enabled and cloud sync is disabled (for now).
Enabling data capture here will allow you to capture data from your robot's components.
You can leave the default directory in which your captured data is stored on-robot.
By default, it saves it to the <file>/.viam/capture</file> directory on your robot.

![Screenshot from the Data Management service showing the Data Capture option enabled and the cloud sync option disabled.](../img/data-management/image3.png)

- Click **Save Config** at the bottom of the window.

## Configuring data capture for a component

With data capture enabled, you can now configure data capture for specific components on your robot running Viam. You can choose the components, corresponding methods, and the frequency of the data capture all within the Viam app.

{{% alert title="Note" color="note" %}}

We're enabling data capture from a camera for this tutorial, but did you know that you can enable data capture on most [Viam components](/components/)? This allows you to capture not just image data, but sensor data, robot state data, etc.

{{% /alert %}}

To enable image data capture for a camera component you will need to do the following:

- Go to <a href="https://app.viam.com/robot" target="_blank">the robot page in the Viam app</a> and select your robot.

- Go to the **COMPONENTS** tab for your robot and scroll down to the camera component.
(On the Viam Rover, the camera is named "cam.")

- You will find a section labeled "Data Capture Configuration".
Click the "Add Method" button to enable data capture for this camera.

- Set the **Type** to "ReadImage" and the **Frequency** to "0.333".
This will capture an image from the camera roughly once every 3 seconds.
Feel free to adjust the frequency if you want the camera to capture more or less image data.

- You should also select the Mime Type that you want to capture.
For this tutorial, we are capturing "image/jpeg" data.

![Screenshot from the Viam app showing the data capture settings used for this tutorial.](../img/data-management/image5.png)

- Click **Save Config** at the bottom of the window.

Now your image data will be saved locally on your robot to the <file>/.viam/capture</file> directory (or wherever you configured your captured data to be saved in your Data Management service).

{{% alert title="Tip" color="tip" %}}

If you are following along using your own robot, you can actually confirm that your data is being captured locally.
On your robot, navigate to the <file>/.viam/capture</file> directory and you will see data being captured in real-time.

{{% /alert %}}

Now that you have set up data capture for a camera, you will enable cloud sync so you can securely access all your robot's data in the Viam app in the cloud.

## Enabling cloud sync on the Data Management service

To enable the cloud sync on your robot, you will need to do the following:

- Go to the **CONFIG** tab, then select **SERVICES**.

- Navigate to [the Data Management service you created above](#enabling-data-capture-with-the-data-management-service).

- Under the "cloud sync" section, toggle "syncing" to enable.

![Screenshot from the Data Management service showing the Data Capture and the cloud sync option enabled.](../img/data-management/image2.png)

- Click **Save Config** at the bottom of the window.

Now the data that you captured locally will sync automatically with the Viam app in the cloud.
In the next step, you will be able to review all your data using the Viam app.

## Viewing and filtering captured data on the Viam app

Now that you have data capture enabled for a camera on your Viam Rover, you can go and review the images from your robot.

- Head over to the **Data** page at <a href="https://app.viam.com/data/view?tab=images" target="_blank">app.viam.com/data</a>.

- Select "Rover Rental" from the **Location** drop-down menu, and click search.
If you have data capture set up correctly, you should be able to see the captured images from your rover's camera.

![The data page of the Viam app showing a gallery of the images captured from the Viam Rover.](../img/data-management/image1.png)

## Exporting captured data from the Viam app

You've successfully saved data from your robot into the cloud with Viam's Data Management service.
Now, let's export that image data from the Viam's Data Management service in the cloud and onto your local computer.

To export data from Viam, you will need to do the following:

On your computer, initialize a new Go module in a new directory. You can do this by running the following in your terminal:

```bash
mkdir viam-rover-data-capture && cd viam-rover-data-capture
go mod init viam-rover
```

Next you will need to install the Viam CLI:

```bash
go get go.viam.com/rdk/cli/cmd
```

Once you have the Viam CLI installed, you will need to authenticate with Viam. You can do this by running the following command and following the prompts in your terminal:

```bash
go run go.viam.com/rdk/cli/cmd auth
```

Once you are authenticated with your Viam account, you will be able to run your export command.
Head back to the **DATA** page in the Viam app at <a href="https://app.viam.com/data/view?tab=images" target="_blank">app.viam.com/data</a> and click the **COPY EXPORT COMMAND** button.

![A red box highlights the "copy export command" button from the Viam app with an image gallery of captured images from the Viam Rover on the right.](../img/data-management/image4.png)

This command uses the Viam CLI to download the data locally onto your computer based on the search criteria you select in the Viam app.
Once the command has finished running and downloading the images, you should be able to view and use the data locally in a new directory named `data`.
Since images are downloaded in parallel, some may be out of order.
Sort your folder by filename in order to see them in chronological order.

## Next steps

In this tutorial, we showed you how to set up and use Viam's Data Management service on a robot so you can configure data capture and data sync for a camera component.
We also discussed how you can filter and view your captured image data in the Viam app.
And finally, we showed you how you can export your data synced with the Viam cloud locally.

You are now ready to take your own robots to the next level using Viam's Data Management service.
You could add the Data Manager on your own robot and use the data you collect to train a machine learning model to detect hand gestures or objects.
You could use your data to track your robot's usage over time, and even build dashboards to visualize the data from your robot.

If you are ready to start building your own robots with Viam, you should pick up a Raspberry Pi and try building one of Viam's introductory robots on the [tutorials page in our documentation](/tutorials/).
You can also purchase your very own Viam Rover at <a href="https://www.viam.com/resources/rover" target="_blank">viam.com/resources/rover</a>.

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, head over to the <a href="https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw" target="_blank">Viam Community Slack</a>.
