---
title: "Collect images or sensor data in 3 minutes"
linkTitle: "Collect data (3 min)"
type: "docs"
images: ["/get-started/quickstarts/collect-data.png"]
description: "Use Viam to gather images or sensor data from your machine."
imageAlt: "The data icon"
authors: []
languages: []
viamresources: ["data_manager", "sensor"]
platformarea: ["data"]
no_list: true
cost: "0"
resource: "quickstart"
aliases:
  - /get-started/quickstarts/collect-data/
  - /get-started/collect-data/
languages: []
viamresources: [
    "camera",
    "sensor",
    "data_manager",
  ]
level: "Beginner"
date: "2024-07-31"
# updated: ""  # When the tutorial was last entirely checked
cost: "0" # Approximate cost in USD - Only specify number
---

In this guide you'll capture and sync sensor or image data from a machine.

{{< alert title="You will learn" color="tip" >}}

- How to configure data capture and sync
- How to view captured data

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/LWblhDYWoEw">}}

## Requirements

You don't need to buy or own any hardware to complete this tutorial.
If you have the following components, you can follow along on your own hardware:

- A Linux, macOS or WSL computer which can run `viam-server` or an ESP32 which can run `viam-micro-server`.
- A sensor or a webcam: this could be the webcam on your laptop or any other webcam you can connect to your computer.

Make sure to connect your sensor or webcam to your computer.

{{% expand "No computer, camera, or sensor at hand?" %}}
No problem.
If you don't have a development machine or other computer that can run `viam-server`, use [Try Viam](https://app.viam.com/try) to borrow a rover free of cost online.
The rover already has `viam-server` installed and is configured with some components to test with, including a webcam.

Once you have borrowed a rover, go to the **CONFIGURE** tab of the machine, find the cameras and click on the **Test** panel at the bottom of each camera's configuration panel to test the camera stream.
You should have a front-facing camera and an overhead view of your rover.
Now you know what the rover can _perceive_.

If your rover is facing a wall, find the base configuration panel and click on its **Test** panel.
Use the controls to drive your rover to a different location.

Now that you have seen that the cameras on your Try Viam rover work, **continue with Step 4**.

If you have a computer that can run `viam-server` but no physical sensor, you can use the [`viam:viam-sensor:telegrafsensor`](https://app.viam.com/module/viam/viam-telegraf-sensor) model which measures computer performance metrics.
{{% /expand%}}

## Instructions

Select a tab below to collect images from a camera or readings from a sensor:

{{< tabs >}}
{{% tab name="Collect camera images" %}}

{{< expand "Step 1: Create a machine" >}}

Go to the [Viam app](https://app.viam.com) and add a new machine by providing a name in the **New machine** field and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}
{{% expand "Step 2: Install viam-server or viam-micro-server" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page.
If you are using a microcontroller, install `viam-micro-server`.
Otherwise, install `viam-server`.
Wait for your device to connect to the Viam app.

![The Viam app DATA page showing sensor data from an air quality sensor.](/get-started/quickstarts/collect-data/setup-button.png)

{{% /expand %}}
{{< expand "Step 3: Configure a camera" >}}

{{< gif webm_src="/how-tos/configure-webcam.webm" mp4_src="/how-tos/configure-webcam.mp4" alt="The process described below." max-width="550px" class=aligncenter >}}

1. From the **CONFIGURE** tab on your machine's page in the [Viam app](https://app.viam.com/), click the **+** icon next to your machine part and select **Component**.
   Select the `camera` type and add the `webcam` model.

1. Click the **Save** button in the top right corner of the page to save your config.

1. Click on the **Test** panel at the bottom of the camera configuration panel to test the camera stream.
   If you don't see an image stream, [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).
   By default your camera stream refreshes once every second.
   You can change the refresh frequency to **Live** in the dropdown menu at the top of the **Test** panel.

For more detailed information, including optional attribute configuration, see the [`webcam` docs](/components/camera/webcam/).

{{< /expand >}}
{{< expand "Step 4: Configure data capture on the camera" >}}

{{<gif webm_src="/how-tos/capture-images.webm" mp4_src="/how-tos/capture-images.mp4" alt="The process described below." max-width="600px" class="aligncenter" >}}

1. Click the **Add method** button in the camera's configuration card.
   When the **Create data management service** prompt appears, click to add the service to your machine.
   Leave the default settings.

1. Scroll back up to your camera config card.
   In the **Data capture** section:

   - Click the **Method** dropdown and select **ReadImage**.

   - Set the frequency to `0.1` to capture an image every 10 seconds.

   - Set the MIME type to `image/jpeg`.

1. Click the **Save** button in the top right corner of the page to save your config.

For more detailed information, see [data management service](/services/data/).

{{< /expand >}}
{{< expand "Step 5: View the captured image data" >}}

Click on the **...** menu of the camera component and click on **View captured data**.
This takes you to the data tab.

![View captured data option in the component menu](/get-started/quickstarts/collect-data/cam-capt-data.png)

If you do not see images from your camera, try waiting a minute and refreshing the page to allow time for the images to be captured and then synced to the app at the interval you configured.

{{< /expand >}}
{{< expand "Step 6: Stop data capture" >}}

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your camera's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

{{< /expand >}}

{{% /tab %}}
{{% tab name="Collect sensor readings" %}}

{{< expand "Step 1: Create a machine" >}}

Add a new machine in the [Viam app](https://app.viam.com).

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}
{{% expand "Step 2: Install viam-server or viam-micro-server" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page.
If you are using a microcontroller, install `viam-micro-server`.
Otherwise, install `viam-server`.
Wait for your device to connect to the Viam app.

![The Viam app with the setup button.](/get-started/quickstarts/collect-data/setup-button.png)

{{% /expand%}}
{{< expand "Step 3: Configure a board" >}}

Most sensors need to be wired to the pins of a SBC such as a Raspberry Pi.

If you are not using a single-board computer (SBC), move on to step 4.

If you are using a SBC, make sure you have installed `viam-server` on the SBC.
Then add a [board component](/components/board/#configuration) to your config for your SBC.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

{{% alert title="Important" color="note" %}}
If your sensor uses I<sup>2</sup>C, SPI, or serial port communication, you need to enable that type of communication in your board's settings.
For example, if you are using a Raspberry Pi, SSH to it and [enable serial communication in `raspi-config`](/installation/prepare/rpi-setup/#enable-communication-protocols).
{{% /alert %}}

{{< /expand >}}

{{< expand "Step 4: Configure a sensor" >}}

Search the [sensor models](/components/sensor/#configuration) for a model of sensor that is compatible with your sensor hardware.
For example, if you have a Sensirion SHT3x-DIS temperature and humidity sensor, you should use the [`sensirion-sht3xd`](https://github.com/viam-modules/sensirion/) model of sensor.

If you don't have a physical sensor that can be wired to the pins of a SBC, you can use the [`viam:viam-sensor:telegrafsensor`](https://app.viam.com/module/viam/viam-telegraf-sensor) model which measures computer performance metrics.

Once you determine which model to use, add it to your machine's configuration:

1. From the **CONFIGURE** tab on your machine's page in the [Viam app](https://app.viam.com/), click the **+** icon next to your machine part and select **Component**.
   Select the `sensor` type and add your sensor model.

   {{<imgproc src="/get-started/quickstarts/collect-data/config-sensor.png" resize="x1100" declaredimensions=true alt="The dropdown showing all sensor models." style="width:550px" >}}

1. Add required attributes, such as information about how the sensor is connected to the board.
   You can find information on these attributes by clicking the name of your sensor model in the [available models list](/components/sensor/#configuration).

1. Click the **Save** button in the upper right corner of the page to save your configuration.

1. Click on the **Test** panel at the bottom of the configuration panel of the sensor to confirm you are getting readings.
   If you don't see the latest reading from the sensor, check that your sensor is properly wired to the board, and that the type of communication the sensor uses is enabled on the board (if applicable).

{{% alert title="Important" color="note" %}}
If your sensor uses I<sup>2</sup>C, SPI, or serial port communication, you need to enable that type of communication in your board's settings.
For example, if you are using a Raspberry Pi, SSH to it and [enable serial communication in `raspi-config`](/installation/prepare/rpi-setup/#enable-communication-protocols).
{{% /alert %}}

{{< /expand >}}
{{< expand "Step 5: Configure data capture on the sensor" >}}

{{< gif webm_src="/how-tos/capture-sensor-readings.webm" mp4_src="/how-tos/capture-sensor-readings.mp4" alt="The process described below." max-width="600px" class="aligncenter" >}}

1. On the sensor's configuration card, find the **Data capture** area and click the **Add method** button.
   When the **Data management service missing** alert appears, click **Create data management service** to add the service to your machine.
   Keep the default settings.

1. Scroll back up to your sensor configuration card.
   In the **Data capture** section:

   - Click the **Method** dropdown and select **Readings**.

   - Set the frequency to `0.05` to capture a sensor reading once every 20 seconds.

1. Click the **Save** button in the top right corner of the page to save your config.

For more detailed information, see [data management service](/services/data/).

{{< /expand >}}
{{< expand "Step 6: View the captured sensor data" >}}

Click on the **...** menu of the sensor component and click on **View captured data**.
This takes you to the data tab.

![View captured data option in the component menu](/get-started/quickstarts/collect-data/sensor-capt-data.png)

If you do not see data from your sensor, try waiting a minute and refreshing the page to allow time for the readings to be captured and then synced to the app at the interval you configured.

{{< /expand >}}
{{< expand "Step 7: Stop data capture" >}}

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your sensor's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

## Next steps

Now that you have captured data, you could use this data to [train your own Machine Learning model](/how-tos/train-deploy-ml/) with the Viam platform.

To learn more about the Viam platform, dive into the [How-to Guides](/how-tos/) which provide instructions for common tasks and workflows, check out [Tutorials](/tutorials/) for projects, or learn more in the [Platform Reference](/platform/) documentation:

{{< cards >}}
{{% card link="/how-tos/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/platform/" %}}
{{< /cards >}}
