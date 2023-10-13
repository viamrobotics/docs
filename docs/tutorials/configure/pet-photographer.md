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

## Prepare to import subtype's API into your main program

To ensure that your custom API is properly integrated into the Viam app, you must import the camera's API into your main program and register them with your chosen SDK, follow these steps:

In this example, the camera's API is defined in the <file>[camera.go](https://github.com/viamrobotics/rdk/blob/585384d853267308243e69367da1d0649a0a91f5/components/camera/camera.go)</file> file in the RDK on Viam's Github.

When developing your `module` directory's <file>main.go</file> or <file>main.py</file> file, reference this file.

## Create your filter module

A filter module can be written for use with various components and situations, but in this example it is being authored to filter image data from the camera component by color.
The code for this colorfilter camera model (<file>[color_filter.go](https://github.com/viam-labs/modular-filter-examples/blob/main/colorfilter/color_filter.go)</file>)/(<file>[color_filter.py](https://github.com/viam-labs/modular-filter-examples/blob/main/colorfilter/color_filter.py)</file>) and module entry point file (<file>[main.go](https://github.com/viam-labs/modular-filter-examples/blob/main/colorfilter/module/main.go)</file>) is sourced from the full modular filter examples available on the [Viam GitHub](https://github.com/viam-labs/modular-filter-examples/tree/main).

### Include required methods

In order to code a new filter resource model, you must implement the required methods outlined in the <file>[client.go](https://github.com/viamrobotics/rdk/components/camera/client.go)</file> file in the corresponding resource's directory.
In this case, the `rdk/components/camera` directory.

Provide this as a file inside of your `colorfilter` module directory to serve as your module's client interface, <file>color_filter.go</file> or <file>color_filter.py</file>.

- Name your model with all lowercase letters for optimal performance with Viam's SDKs.

For more information on adding the required methods to your module's file, see [Code a new resource model](/modular-resources/create/#code-a-new-resource-model).

### Include required filter data management check

When creating your own filter module, it's required to check whether the data management service is the caller of the filtering to prevent unwanted effects on the filter state.
You can achieve this by examining the `extra` data passed to your filter function.

The approach for checking this varies depending on the programming language used to configure your camera:

- The Go configured camera looks for a flag called `fromDM` in the context (`ctx`) using `ctx.Value(data.`**`FromDM`**`ContextKey{})` to figure out if data management triggered the filter, rather than using `extra`.
- For the Python configured camera, the SDK simplifies this process by exposing the utility function `from_dm_from_extra`, which handles the check for you.
- For other programming languages, similar utility functions will be exposed to help you check the caller of your filter function.
  Not all collector functions receive the `extra` data parameter, so the method for checking may vary based on the specific function and language.

- If the boolean is true, the function will call the vision service to get detections and return the image if the color is detected, otherwise, they raise `data.ErrNoCaptureToStore` or `NoCaptureToStoreError()`.

{{< alert title="Tip" color="tip" >}}

It's important to include these operations and the `data.ErrNoCaptureToStore` or `NoCaptureToStoreError()` error types to avoid unintentional impacts to the filter state.

{{< /alert >}}

{{< tabs name="Color Filter Code">}}
{{% tab name="Python"%}}

```python {class="line-numbers linkable-line-numbers"}
async def get_image(self, mime_type: str = "", \*, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, \*\*kwargs) -> Image.Image:
"""Filters the output of the underlying camera"""
img = await self.actual_cam.get_image()
if from_dm_from_extra(extra):
detections = await self.vision_service.get_detections(img)
if len(detections) == 0:
raise NoCaptureToStoreError()

          return img
```

{{% /tab %}}
{{% tab name="Go"%}}

```go {class="line-numbers linkable-line-numbers"}
// Next contains the filtering logic and returns select data from the underlying camera.
func (fs filterStream) Next(ctx context.Context) (image.Image, func(), error) {
if ctx.Value(data.FromDMContextKey{}) != true {
// If not data management collector, return underlying stream contents without filtering.
return fs.cameraStream.Next(ctx)
}

    // Only return captured image if it contains a certain color set by the vision service.
    img, release, err := fs.cameraStream.Next(ctx)
    if err != nil {
      return nil, nil, errors.New("could not get next source image")
    }
    detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
    if err != nil {
      return nil, nil, errors.New("could not get detections")
    }

    if len(detections) == 0 {
      return nil, nil, data.ErrNoCaptureToStore
    }

    return img, release, err

}
```

{{% /tab %}}
{{< /tabs >}}

### Configure your camera

Navigate to your robot's page on the app and click on the **Config** tab.

Add your robot's [camera](/components/camera/) as a component by clicking **Create component** in the lower-left corner of the page and typing in 'webcam'.
Select the `webcam` model and type in 'cam' as the name for your camera.
Then click create.

Your robot's config page now has a panel for your camera.
To select the camera the robot should use, click on the **video path** field.
If your robot is connected, you will see a selection of available cameras.
Select the camear you want to use, then click **Save config**

![An instance of the webcam component named 'cam'](/tutorials/pet-photographer/webcam-component.png)

## Add services

After you've finished setting up your robot's camera, add a [vision service](/services/vision/detection/) for color detection and a [data management service](/services/data/) for storing your filtered images:

### Vision service to detect color

This tutorial uses the color of my dogs collar, `#43A1D0` or `rgb(67, 161, 208)` (blue), but you can use a different color that matches your pet or a distinctly colored item on your pet.

**Hex color #43A1D0**: {{<imgproc src="/tutorials/pet-photographer/43a1d0.png" resize="90x" declaredimensions=true alt="A color swatch for the color of example subject's collar">}}

Navigate to your robot's **Config** tab on the [Viam app](https://app.viam.com/robots) and configure your [vision service color detector](/services/vision/detection/):

{{< tabs >}}
{{% tab name="Builder" %}}

1. Click the **Services** subtab and click **Create service** in the lower-left corner.

1. Select the `Vision` type, then select the `Color Detector` model.

1. Enter `my_color_detector` as the name for your detector and click **Create**.

1. In the vision service panel, click the color selection box to set the color to be detected.
   For this tutorial, set the color to the color of your pet, or use a blue collar or ribbon to increase the precision of your filter.

1. Then, set **Hue Tolerance** to `0.06` and **Segment Size px** to `100`.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to blue, the hue tolerance set to 0.06, and the segment size set to 100.](/tutorials/pet-photographer/vision-service.png)

For more detailed information see [Configure a color detector](/services/vision/detection/#configure-a-color_detector).

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
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
