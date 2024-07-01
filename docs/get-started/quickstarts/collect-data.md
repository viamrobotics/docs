---
title: "Collect images or sensor data in 2 minutes"
linkTitle: "Collect data in 2 minutes"
type: "docs"
weight: 20
cost: 75
images: ["/platform/data.svg"]
description: "Use Viam to gather images or sensor data from your machine."
---

Follow this guide to start collecting images or sensor data from your machine using the [data management service](/services/data/).

## Requirements

- A Linux or macOS computer:
  - A single-board computer (SBC) such as a Raspberry Pi, OR
  - A laptop or desktop
- A camera or a sensor.
  Options:
  - The webcam built into your computer
  - A USB webcam connected to your computer or SBC
  - A sensor (such as a temperature sensor) wired to your single-board computer's GPIO pins

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

1. From the **CONFIGURE** tab on your machine's page in [the Viam app](https://app.viam.com/), click the **+** icon next to your machine part in the left-hand menu and select **Component**.

2. Select the `camera` type, then select the `webcam` model.

3. Enter a name or use the suggested name for your camera and click **Create**.

4. Click the **Save** button in the top right corner of the page to save your config.

5. Go to the **CONTROL** tab and expand the camera's remote control card to test the camera stream.
   If you don't see an image stream, [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).

For more detailed information, including optional attribute configuration, see the [`webcam` docs](/components/camera/webcam/).

{{< /expand >}}
{{< expand "Step 4: Configure data capture on the camera" >}}

{{<gif webm_src="/how-tos/capture-images.webm" mp4_src="/how-tos/capture-images.mp4" alt="The process described below." max-width="600px" class="aligncenter" >}}

1. Return to the **CONFIGURE** tab on your machine's page in [the Viam app](https://app.viam.com/).
   Locate the configuration card for your camera.

2. Click the **Add method** button.
   When the **Create data management service** prompt appears, click to add the service to your machine.
   Leave the default settings.

3. Scroll back up to your camera config card.
   In the **Data capture** section:

   - Click the **Method** dropdown and select **ReadImage**.

   - Set the frequency to `0.1` to capture an image every 10 seconds.

   - Set the MIME type to `image/jpeg`.

For more detailed information on data capture, see [Configure Data Capture](/services/data/capture/).
For more on the camera API, see [Camera Component](/components/camera/#getimage).

{{< /expand >}}
{{< expand "Step 5: View the captured image data" >}}

![The Data tab in the upper-left corner of the screen.](/get-started/quickstarts/collect-data/data-tab-navigation.png)

In the upper banner of the [Viam app](https://app.viam.com/), click **DATA** to see the captured images displayed.
If you do not see images from your camera, try waiting a minute and refreshing the page to allow time for the images to be captured and then synced to the app at the interval you configured.

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
For example, if you are using a Raspberry Pi, SSH to it and [enable serial communication in `raspi-config`](/get-started/prepare/rpi-setup/#enable-communication-protocols).
{{% /alert %}}

{{< /expand >}}

{{< expand "Step 4: Configure a sensor" >}}

1. Search the [supported sensor models](/components/sensor/#supported-models) for a model of sensor that is compatible with your sensor hardware.
   For example, if you have a Sensirion SHT3x-DIS temperature and humidity sensor, you should use the [`sensirion-sht3xd`](https://docs.viam.com/components/sensor/sensirion-sht3xd/) model of sensor.

   Once you determine which model to use, add it to your machine's configuration:

1. From the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com/), click the **+** icon next to your machine part in the left-hand menu and select **Component**.

1. Select the `sensor` type, then select the model that matches your hardware.

   {{<imgproc src="/get-started/quickstarts/collect-data/config-sensor.png" resize="x1100" declaredimensions=true alt="The dropdown showing all sensor models." style="max-width:550px" >}}

1. Enter a name or use the suggested name for your sensor and click **Create**.

1. Add required attributes, such as information about how the sensor is connected to the board.
   You can find information on these attributes by clicking the name of your sensor model in the [supported models list](/components/sensor/#supported-models).

1. Click the **Save** button in the upper right corner of the page to save your configuration.

1. Go to the **CONTROL** tab and expand the sensor's remote control card to test the sensor.
   Click **Get readings**.
   If you don't see the latest reading from the sensor, check that your sensor is properly wired to the board, and that the type of communication the sensor uses is enabled on the board (if applicable).

   {{< imgproc src="/get-started/quickstarts/collect-data/get-readings-control-tab.png" resize="x1100" declaredimensions=true alt="The sensor card on the Control tab with some air quality readings." style="max-width:600px" >}}

{{% alert title="Important" color="note" %}}
If your sensor uses I<sup>2</sup>C, SPI, or serial port communication, you need to enable that type of communication in your board's settings.
For example, if you are using a Raspberry Pi, SSH to it and [enable serial communication in `raspi-config`](/get-started/prepare/rpi-setup/#enable-communication-protocols).
{{% /alert %}}

{{< /expand >}}
{{< expand "Step 5: Configure data capture on the sensor" >}}

{{< gif webm_src="/how-tos/capture-sensor-readings.webm" mp4_src="/how-tos/capture-sensor-readings.mp4" alt="The process described below." max-width="600px" class="aligncenter" >}}

1. Return to the **CONFIGURE** tab on your machine's page in [the Viam app](https://app.viam.com/).
   Locate the configuration card for your sensor.

2. Click the **Add method** button.
   When the **Data management service missing** alert appears, click **Create data management service** to add the service to your machine.
   Leave the default settings.

3. Scroll back up to your sensor configuration card.
   In the **Data capture** section:

   - Click the **Method** dropdown and select **Readings**.

   - Set the frequency to `0.05` to capture a sensor reading once every 20 seconds.

For more detailed information on data capture, see [Configure Data Capture](/services/data/capture/).
For more on the sensor API, see [Sensor Component](/components/sensor/#getreadings).

{{< /expand >}}
{{< expand "Step 6: View the captured sensor data" >}}

![The Viam app Data tab showing sensor data from an air quality sensor.](/get-started/quickstarts/collect-data/data-page.png)

In the upper banner of the [Viam app](https://app.viam.com/), click **DATA** to see the captured sensor data displayed.
If you do not see data from your sensor, try waiting a minute and refreshing the page to allow time for the readings to be captured and then synced to the app at the interval you configured.

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

## Next steps

Now that you have captured data, try training a computer vision model on your images, or query your sensor data:

{{< cards >}}
{{% card link="/use-cases/deploy-ml/" %}}
{{% card link="/use-cases/sensor-data-query/" %}}
{{< /cards >}}

To see data capture in real-world projects, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
