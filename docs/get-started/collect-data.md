---
title: "Collect images or sensor data in 3 minutes"
linkTitle: "Collect data (3 min)"
type: "docs"
images: ["/platform/data.svg"]
description: "Use Viam to gather images or sensor data from your machine."
imageAlt: "The data icon"
authors: []
weight: 40
languages: []
viamresources: ["data_manager", "sensor"]
no_list: true
level: "Beginner"
date: "2024-07-31"
cost: "0"
resource: "quickstart"
aliases:
  - /get-started/quickstarts/collect-data/
---

Follow this guide to start collecting images or sensor data from your machine using the [data management service](/services/data/).

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/zjoa8Mdx4zM">}}

## Requirements

- A Linux or macOS computer:
  - A single-board computer (SBC) such as a Raspberry Pi, OR
  - A laptop or desktop
- A camera or a sensor.
  Options:
  - The webcam built into your computer
  - A USB webcam connected to your computer or SBC
  - A sensor (such as a temperature sensor) wired to your single-board computer's GPIO pins

{{% expand "No computer or camera at hand?" %}}
No problem.
Use [Try Viam](https://app.viam.com/try) to rent a rover online which is already configured with some components to test with.
If you are using a Try Viam rover **start with Step 4** on the **Collect camera images** tab.
{{% /expand%}}

## Instructions

Select a tab below to collect images from a camera or readings from a sensor:

{{< tabs >}}
{{% tab name="Collect camera images" %}}

{{< expand "Step 1: Create a machine" >}}

Go to the Viam app and [add a new machine](/cloud/machines/#add-a-new-machine).

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}
{{% expand "Step 2: Install viam-server" %}}

Navigate to the **CONFIGURE** tab on your machine's page in the [Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer and connect it to the Viam app.

![The Viam app DATA page showing sensor data from an air quality sensor.](/get-started/quickstarts/collect-data/setup-button.png)

{{% /expand %}}
{{< expand "Step 3: Configure a camera" >}}

{{< gif webm_src="/how-tos/configure-webcam.webm" mp4_src="/how-tos/configure-webcam.mp4" alt="The process described below." max-width="550px" class=aligncenter >}}

1. From the **CONFIGURE** tab on your machine's page in [the Viam app](https://app.viam.com/), click the **+** icon next to your machine part and select **Component**.
   Select the `camera` type and add the `webcam` model.

1. Click the **Save** button in the top right corner of the page to save your config.

1. Click on the **Test** panel at the bottom of the camera configuration panel to test the camera stream.
   If you don't see an image stream, [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).

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

For more detailed information on data capture, see [Configure Data Capture](/services/data/capture/).
For more on the camera API, see [Camera Component](/components/camera/#getimage).

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

{{< /expand >}}

{{% /tab %}}
{{% tab name="Collect sensor readings" %}}

{{< expand "Step 1: Create a machine" >}}

Go to the Viam app and [add a new machine](/cloud/machines/#add-a-new-machine).

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}
{{%expand "Step 2: Install viam-server" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer and connect it to the Viam app.

![The Viam app DATA page showing sensor data from an air quality sensor.](/get-started/quickstarts/collect-data/setup-button.png)

{{% /expand%}}
{{< expand "Step 3: Configure a board" >}}

Most sensors need to be wired to the pins of a single-board computer such as a [Raspberry Pi](/components/board/pi/).
Add a board component to your config:

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

{{% alert title="Important" color="note" %}}
If your sensor uses I<sup>2</sup>C, SPI, or serial port communication, you need to enable that type of communication in your board's settings.
For example, if you are using a Raspberry Pi, SSH to it and [enable serial communication in `raspi-config`](/installation/prepare/rpi-setup/#enable-communication-protocols).
{{% /alert %}}

{{< /expand >}}

{{< expand "Step 4: Configure a sensor" >}}

1. Search the [supported sensor models](/components/sensor/#available-models) for a model of sensor that is compatible with your sensor hardware.
   For example, if you have a Sensirion SHT3x-DIS temperature and humidity sensor, you should use the [`sensirion-sht3xd`](https://docs.viam.com/components/sensor/sensirion-sht3xd/) model of sensor.

   Once you determine which model to use, add it to your machine's configuration:

1. From the **CONFIGURE** tab on your machine's page in [the Viam app](https://app.viam.com/), click the **+** icon next to your machine part and select **Component**.
   Select the `sensor` type and add your sensor model.

   {{<imgproc src="/get-started/quickstarts/collect-data/config-sensor.png" resize="x1100" declaredimensions=true alt="The dropdown showing all sensor models." style="max-width:550px" >}}

1. Add required attributes, such as information about how the sensor is connected to the board.
   You can find information on these attributes by clicking the name of your sensor model in the [available models list](/components/sensor/#available-models).

1. Click the **Save** button in the upper right corner of the page to save your configuration.

1. Click on the **Test** panel at the bottom of the configuration panel of the sensor.
   Click **Get readings** to confirm you are getting readings.
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

For more detailed information on data capture, see [Configure Data Capture](/services/data/capture/).
For more on the sensor API, see [Sensor Component](/components/sensor/#getreadings).

{{< /expand >}}
{{< expand "Step 6: View the captured sensor data" >}}

Click on the **...** menu of the camera component and click on **View captured data**.
This takes you to the data tab.

![View captured data option in the component menu](/get-started/quickstarts/collect-data/sensor-capt-data.png)

If you do not see data from your sensor, try waiting a minute and refreshing the page to allow time for the readings to be captured and then synced to the app at the interval you configured.

{{< /expand >}}
{{< expand "Step 6: Stop data capture" >}}

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your sensor's configuration, toggle the switch to **Off**.

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

## Next steps

Now that you have captured data, you could use this data to train you own Machine Learning model with the Viam platform.

This concludes our guided path for getting to know the Viam platform.

To learn more about the viam platform, dive into the How-to Guides which provide instructions for common tasks and workflows, check out tutorials for projects, or learn more in the Platform Referecen documentation:

{{< cards >}}
{{% card link="/use-cases/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/platform/" %}}
{{< /cards >}}
