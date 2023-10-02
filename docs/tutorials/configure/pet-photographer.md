---
title: "Pet Photographer: Filter Data Captures"
linkTitle: "Pet Photographer"
type: "docs"
description: "Use the filter modular component in the Viam app to photograph your pet in their collar."
tags: ["vision", "filter", "camera", "detector", "services"]
aliases:
    - /tutorials/pet-photographer
    - /tutorials/filter-modular-component
authors: [ "Sky Leilani" ]
languages: []
viamresources: [ "vision", "camera" ]
level: "Beginner"
date: "2023-09-17"
# updated: ""
cost: "0"
no_list: true
weight: 3
---

Smart machines are an integral part of our daily lives.
From our phones to traffic lights, these machines rely on their ability to process and respond to data.
However, as the amount of data collected by these devices continues to grow, it becomes important to not only to process it, but also to organize and manage it effectively.

This tutorial will guide you through using the color filter module to selectively capture and synchronize image data with [Viam's cloud](/services/data/#cloud-sync).

While the color filter selects image data from a camera, these same principles can be applied to various components, including [sensors](https://github.com/viam-labs/modular-filter-examples/tree/main/sensorfilter).
The filter modular component allows you to increase the precision of your model's [data capture](/services/data/#data-capture) and determine which readings to store.
This can help you to avoid sifting through unwanted data captures and ensures that only the data you're interested in is in Viam's cloud.

## Hardware Requirements

For this tutorial you'll need the following hardware components:

- A computer
- A webcam or external camera
- A blue/green collar for increased precision _(optional)_

## Set up

After you [create and connect](https://docs.viam.com/manage/fleet/robots/#add-a-new-robot) to your robot, here's how to get started:

- Install the [Go binary](https://go.dev/dl/) on your local development computer.

- Update [`viam-server`](/installation/manage/#update-viam-server).
If you don't already have `viam-server` installed, follow [these directions](/installation/#install-viam-server) to install the most recent, stable version.

- Clone the [Viam modular filter](https://github.com/viam-labs/modular-filter-examples) examples onto your robot's computer:

   ```{class="command-line" data-prompt="$"}
   git clone https://github.com/viam-labs/modular-filter-examples.git
   ```

### Configure the source code

This tutorial makes use of [Viam's color filter example](https://github.com/viam-labs/modular-filter-examples/tree/main/colorfilter). However, you can modify the filter's source code or write your own filter for different components using [this guide](/extend/modular-resources/create/).

Navigate to the `modular-filter-examples/colorfilter/module` directory in your terminal, and run the following command:

```{class="command-line" data-prompt="$"}
go build
```

This command will compile the source code in the colorfilter/module directory and generate an executable with the same name as the module, which is 'colorfilter'.

{{< alert title="Tip" color="tip" >}}
Go to the `colorfilter/module` directory of the color filter module you cloned and get the absolute path to your `colorfilter` module for later use by running:

```{class="command-line" data-prompt="$"}
realpath colorfilter 
```

{{< /alert >}}

Read [this guide](https://docs.viam.com/extend/modular-resources/configure/#configure-a-local-module) for more information on configuring a local module.

### Set up camera

Navigate to your robot's page on the app and click on the **Config** tab.

Add your robot's camera as a component by clicking **Create component** in lower-left corner of the page and typing in 'webcam' or specific the model you're using.

![A photo of the webcam component named 'cam'](/tutorials/pet-photographer/webcam-component.png)

For more information about the Camera component, you can refer to [this page](/components/camera/).

## Add services

After you've finished setting up, add a [vision service](/services/vision/detection) for color detection and a [data management service](/services/data/) for storing your filtered images.

### Vision service to detect color

This tutorial uses the color of my dogs collar, `#43A1D0` or `rgb(67, 161, 208)` (blue).

**Hex color #43A1D0**: {{<imgproc src="/tutorials/pet-photographer/43a1d0.png" resize="90x" declaredimensions=true alt="A color swatch for the color of example subject's collar">}}

Navigate to your robot's **Config** tab on the [Viam app](https://app.viam.com/robots) and configure your [vision service color detector](/services/vision/detection/):

{{< tabs >}}
{{% tab name="Builder" %}}

1. Click the **Services** subtab and click **Create service** in the lower-left corner.

1. Select the `Vision` type, then select the `Color Detector` model.

1. Enter `my_color_detector` as the name for your detector and click **Create**.

1. In the vision service panel, click the color selection box to set the color to be detected.
   For this tutorial, set the color to the color of your pet, or use a blue/green collar or ribbon to increase the precision of your filter.

1. Then, set **Hue Tolerance** to `0.06` and **Segment Size px** to `100`.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to blue, the hue tolerance set to 0.06, and the segment size set to 100.](/tutorials/pet-photographer/vision-service.png)

For more detailed information see [Configure a color detector](/services/vision/detection/#configure-a-color_detector).

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "my_color_detector",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 100,
      "detect_color": "#43a1d0",
      "hue_tolerance_pct": 0.06
    }
  },
  ... // Other services
]
```

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
    "services": [
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
]
```

Click **Save Config** and head back to the Builder mode.

{{% /tab %}}
{{< /tabs >}}

## Configure the color filter camera

Before you can interact with the vision and data management services, you must configure your camera to filter color and store photos to Viam's cloud.

### Add local module

Select the **Modules** subtab in the **Config** panel to upload the local color filter module to your robot's system in the Viam app.

In the **Add local module** section, enter the name of your module (`colorfilter`) along with the absolute path to the filter's executable and click **Add module**.
Then, click **Save config**.

![A color filter module that has been added.](/tutorials/pet-photographer/add-colorfilter-module.png)

### Add colorfilter component

1. Click the **Components** subtab and click **Create component**.

1. Then, select the `local modular resource` type from the list.

   {{<imgproc src="extend/modular-resources/configure/add-local-module-list.png" resize="300x" declaredimensions=true alt="The add a component modal showing the list of components to add with 'local modular resource' shown at the bottom">}}

1. On the next screen:

   - Select the select [camera](/components/camera/), from the drop down menu.
   - Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of your modular resource's [model](/extend/modular-resources/key-concepts/#models), `example:camera:colorfilter`.
   - Enter a name for this instance of your modular resource.
     This name must be different from the module name.

   {{<imgproc src="/tutorials/pet-photographer/add-colorfilter-module-create.png" resize="400x" declaredimensions=true alt="The add a component model showing the create a module step for a local color filter module">}}

1. Click **Create** to create the modular resource component.

1. Copy the following JSON configuration into the Attributes section:

```json {class="line-numbers linkable-line-numbers"}
 {
   "vision_service": "my_color_detector",
   "actual_cam": "actualcam"
 }
```

![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam](/tutorials/pet-photographer/colorfiltercam-component-attributes.png)

### Configure data capture

To add data capture for the colorfilter camera, click **Add Method** in the **Data Capture configuration** section of your color filter camera component.
Toggle the **Type** dropdown menu, select **ReadImage**, and set the **Frequency** of the capture to `0.1`.
Then, click **Save config**.

![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam as well as the data capture configuration capture set capture ReadImage at 0.1 frequency](/tutorials/pet-photographer/colorfiltercam-component.png)

### Test your color filter camera

To test that your color filter camera is capturing and filtering images properly, navigate to the **Control** tab on your robot's page.

On the **colorfiltercam**'s panel, toggle **view colorfiltercam** to view your camera's live feed.
Test the filter by getting a blue colored item and moving it in frame.

![Kimbo in camera live feed]()

Then, go to the **Data** tab to view pictures that contain the blue colored item.

![Data tab contents from colorfiltercam]()

## Photograph your pet

To photograph your own pet, put them in a blue or green collar and set up your camera to point at an area they go to frequently.
When you check the **Data** tab, you'll only see pictures of your adorable pet.

## Next steps

{{< cards >}}
  {{% card link="/tutorials/services/try-viam-color-detection.md" %}}
{{< /cards >}}
