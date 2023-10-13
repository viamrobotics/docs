---
title: "Pet Photographer: Capture and Filter Images for Viam Cloud"
linkTitle: "Pet Photographer"
type: "docs"
description: "Use the filter modular component in the Viam app to photograph your pet in their collar."
tags: ["vision", "filter", "camera", "detector", "services"]
aliases:
  - /tutorials/pet-photographer
  - /tutorials/filter-modular-component
authors: ["Sky Leilani"]
languages: []
viamresources: ["vision", "camera"]
level: "Beginner"
date: "2023-09-17"
# updated: ""
cost: "0"
no_list: true
weight: 3
---

Smart machines are an integral part of our daily lives.
From our phones to traffic lights, these machines rely on their ability to process and respond to data.
However, as the amount of data collected by these devices continues to grow, it becomes important to not only process it, but also to organize and manage it effectively.

This tutorial will walk you through creating a filter module.
Specifically it will focus on writing and configuring a color filter module, and can serve as a reference when writing your own filter module for various components.

Creating a filter {{< glossary_tooltip term_id="module" text="module" >}} will enable you to selectively store data from your robot based on whether specified conditions have been met.
Once you've configure your robot for data capture and established the connection to [Viam's cloud](/services/data/#cloud-sync), the robot will use the [data management service](/services/data/) to regularly send data to the cloud.
However, before this data is stored in Viam's cloud, the filter module will process it, saving only the data that meets the specified criteria.

This functionality is versatile and applicable in various scenarios.
For example, you could program a bird feeder to periodically take pictures and store only pictures containing the distinctive red color that robins have.
You can also create a filter module to filter out blurry images, or configure a sensor to store data related to energy usage only when it exceeds predefined thresholds.

Let's take a practical example to illustrate how you can use a filter module effectively.
If you want to store images only when a specific color is detected:

1. Set up a webcam in a location where your pet is likely to appear in frame and use the data management service to periodically take pictures and sync them to the [Viam's cloud](/services/data/#cloud-sync).
2. Attach a colored object, like a blue collar, to your pet.
3. Set up the color filter module, which will process images and only store them if your pet and their easily identifiable colored object is present.

{{<imgproc src="/tutorials/pet-photographer/data-example.png" resize="700x" declaredimensions=true alt="Dog in blue collar in the camera's live feed">}}

While the color filter module you use in this tutorial selects image data from a camera, these same principles can be applied to various components, including for filtering [sensor](https://github.com/viam-labs/modular-filter-examples/tree/main/sensorfilter) data.

## Hardware Requirements

To recreate and test this color filter example, you'll need the following hardware components:

- A computer
- A webcam or external camera
- A colored object, like a blue collar for enhanced accuracy _(optional)_

{{< alert title="Tip" color="tip" >}}
In this tutorial, the camera is configured to identify and filter images with the color blue, as it is less common in many environments, including mine.
If your pet already has a distinct color that is different from their environment, you can also configure your camera to use that color to identify pictures of your pet.
{{< /alert >}}

## Set up

Here's how to get started:

1. Install [Go](https://go.dev/dl/) on your robot's computer.

1. [Create and connect](https://docs.viam.com/manage/fleet/robots/#add-a-new-robot) to your robot.

1. Update [`viam-server`](/installation/manage/#update-viam-server).
   If you don't already have `viam-server` installed, follow [these directions](/installation/#install-viam-server) to install the most recent, stable version.
   Your viam-server must be version 0.8.0 or higher to access the filtering functionality.

### Create your filter module

A filter module can be written for use with various components and situations, but in this example it is being authored to filter image data from the camera component by color.

## Prepare to code your filter module

In order to code a new resource model, you must first locate your resource subtype's **client** interface APIs in the Viam RDK.
These APIs are organized by colon-delimited-triplet identifiers, in the form of `namespace:type:subtype`.

In this example, the resource subtype being used is the camera.
To adhere to the Viam RDK's client interface API for the specific subtype, you need to implement the required methods outlined in the <file>[client.go](https://github.com/viamrobotics/rdk/components/camera/client.go)</file> file in the `rdk/components/camera` directory.
Provide this as a file inside of your `colorfilter` module directory to serve as your module's client interface, <file>color_filter.go</file> or <file>color_filter.py</file>.

## Prepare to import subtype's API into your main program

To ensure that your custom API is properly integrated into the Viam app, you must import the camera's API into your main program and register them with your chosen SDK, follow these steps:

In this example, the camera's API is defined in the <file>[camera.go](https://github.com/viamrobotics/rdk/blob/585384d853267308243e69367da1d0649a0a91f5/components/camera/camera.go)</file> file in the RDK on Viam's Github.

When developing your `module` directory's <file>main.go</file> or <file>main.py</file> file, reference this file.

## Code a new resource model

### Code a new resource model

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) [(rdk:service:base)](/extend/modular-resources/key-concepts/#models) as a new model, `"mybase"`, using the model family `acme:demo:mybase`.

For more information see [Naming your model](/extend/modular-resources/key-concepts/#naming-your-model).

The Go code for the custom model (<file>mybase.go</file>) and module entry point file (<file>main.go</file>) is adapted from the full demo modules available on the [Viam GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources).

{{% alert title="Naming module models" color="tip" %}}

Name your model with all lowercase letters for optimal performance with Viam's SDKs.
For example, `mycolorfilter` or `my-color-filter`.

{{% /alert %}}

{{< tabs name="Sample SDK Code">}}
{{% tab name="Python"%}}
{{% /tab %}}
{{% tab name="Go"%}}
{{% /tab %}}
{{< /tabs >}}

Click **Save Config** and head back to the **Builder** mode.

### Data management service to collect images

To enable data capture on your robot, add and configure the [data management service](/services/data/) to capture and store data on your robot's computer.

{{< tabs >}}
{{% tab name="Builder" %}}

1. At the bottom-left of the page, click **Create service**.
1. Choose `Data Management` as the type and name your instance of the data manager `dm`.
   This service syncs data from your robot to the Viam app in the cloud.
1. Select **Create**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data every 0.1 minutes in the <file>~/.viam/capture</file> directory.

   You can leave the default settings as they are.
   Click **Save Config** at the bottom of the window.

   ![An instance of the data management service named "dm". The cloud sync and capturing options are toggled on and the directory is empty. The interval is set to 0.1](/tutorials/pet-photographer/data-management-services.png)

   For more detailed information see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).
   {{% /tab %}}
   {{% tab name="JSON Template" %}}
   Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
    {
      "name": "dm",
      "type": "data_manager",
      "namespace": "rdk",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": []
      }
    },
  ... // Vision and other services
```

Click **Save Config** and head back to the **Builder** mode.

{{% /tab %}}
{{< /tabs >}}

## Configure the color filter camera

With the vision and data management services configured, you can now configure your camera to filter by color and store photos to Viam's cloud.

### Configure the module's executable

You cloned the example code for the [modular filter examples](https://github.com/viam-labs/modular-filter-examples/) when [setting up](#set-up).
This tutorial makes use of [Viam's color filter example](https://github.com/viam-labs/modular-filter-examples/tree/main/colorfilter).

{{< alert title="Tip" color="tip" >}}
To filter image data based on another constraint, modify the filter's source code.
You can also write your own filter for different components using [this guide](/extend/modular-resources/create/).
{{< /alert >}}

Navigate to the `modular-filter-examples/colorfilter/module` directory on your robot's terminal and run the following command:

```{class="command-line" data-prompt="$"}
go build
```

This command compiles the source code in the colorfilter/module directory and generates an executable with the same name as the module, which is 'colorfilter'.

Next, go to the <file>colorfilter/module</file> directory within the color filter module you cloned and get the absolute path to your `colorfilter` module for later use by running:

```sh {class="command-line" data-prompt="$"}
realpath colorfilter
```

Read [Configure a local module](https://docs.viam.com/extend/modular-resources/configure/#configure-a-local-module) for more information on configuring a local module.

### Add local module

When configuring the color filter module for your robot in the Viam app, you must provide the absolute path to the color filter module on the robot's computer.
This ensures that the Viam app knows where to find the module for remote access.

To do this, follow these steps:

1. Select the **Modules** subtab in the **Config** panel to configure the local color filter module for your robot's system in the Viam app.
1. You identified your `colorfilter` module's path with `realpath` when you [configured your modules executable](#configure-the-modules-executable).
   In the **Add local module** section, enter the name of your module (`colorfilter`) along with the filter's executable and click **Add module**.
1. Then, click **Save config**.

![A color filter module that has been added.](/tutorials/pet-photographer/add-colorfilter-module.png)

### Add colorfilter component

1. Click the **Components** subtab and click **Create component**.

1. Then, select the `local modular resource` type from the list.

   {{<imgproc src="extend/modular-resources/configure/add-local-module-list.png" resize="300x" declaredimensions=true alt="The add a component modal showing the list of components to add with 'local modular resource' shown at the bottom">}}

1. On the next screen:

   1. Select the camera from the drop down menu.
   1. Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of your modular resource's [model](/extend/modular-resources/key-concepts/#models), `example:camera:colorfilter`.
   1. Enter a name for this instance of your modular resource.
      This name must be different from the module name.

   {{<imgproc src="/tutorials/pet-photographer/add-colorfilter-module-create.png" resize="400x" declaredimensions=true alt="The add a component model showing the create a module step for a local color filter module">}}

1. Click **Create** to create the modular resource component.

1. Copy the following JSON configuration into the **Attributes** section:

```json {class="line-numbers linkable-line-numbers"}
{
  "vision_service": "my_color_detector",
  "actual_cam": "cam"
}
```

![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam](/tutorials/pet-photographer/colorfiltercam-component-attributes.png)

### Configure data capture

To add data capture for the colorfilter camera, click **Add Method** in the **Data Capture configuration** section of your color filter camera component.
Toggle the **Type** dropdown menu, select **ReadImage**, and set the **Frequency** of the capture to `0.1`.
Then, click **Save config**.

![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam as well as the data capture configuration capture set capture ReadImage at 0.1 frequency](/tutorials/pet-photographer/colorfiltercam-component.png)

## Test your color filter camera

To test that your color filter camera is capturing and filtering images properly, navigate to the **Control** tab on your robot's page.

On the **colorfiltercam**'s panel, toggle **view colorfiltercam** to view your camera's live feed.
Test the filter by moving a blue colored item within the camera's field of view.
Then, go to the **Data** tab to view pictures that contain the blue colored item.

![Filtered data tab contents from colorfiltercam showing only photos of dog with blue collar](/tutorials/pet-photographer/data-capture.png)

## Next steps

Your pet photographer is now set up.
Place it in an area your pet frequently visits and don't forget to attach the colored object to your pet.
Then, check the [**Data** tab](/manage/data/view/)

If you want to learn more about data management or detection, you may enjoy one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/services/try-viam-color-detection.md" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" %}}
{{% card link="/tutorials/projects/guardian/" %}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{< /cards >}}
