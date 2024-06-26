---
title: "Collect data in 2 minutes"
linkTitle: "Collect data in 2 minutes"
type: "docs"
weight: 20
cost: 75
images: ["/platform/data.svg"]
description: "Use Viam to gather images or sensor data from your machine."
---

Follow this guide to start collecting images or sensor data from your machine using the [data management service](/services/data/):

![The Viam app DATA page showing sensor data from an air quality sensor.](/get-started/quickstarts/data-page.png)

## Requirements

- A Linux or macOS computer:
  - A single-board computer (SBC) such as a Raspberry Pi, OR
  - A laptop or desktop
- A camera or a sensor.
  Options:
  - The webcam built into your computer
  - A USB webcam plugged into your computer or SBC
  - A sensor (such as a temperature sensor) wired to your single-board computer's GPIO pins

## Instructions

Select a tab below to collect images from a camera, or to collect readings from a sensor:

{{< tabs >}}
{{% tab name="Collect camera images" %}}

{{< expand "Step 1: Create a machine" >}}

Go to the Viam app and [add a new machine](/cloud/machines/#add-a-new-machine).

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}
{{%expand "Step 2: Install viam-server" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer and connect it to the Viam app.

{{% /expand%}}
{{< expand "Step 3: Configure a camera" >}}

1. From the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com/), click the **+** icon next to your machine part in the left-hand menu and select **Component**.

2. Select the `camera` type, then select the `webcam` model.

3. Enter a name or use the suggested name for your camera and click **Create**.

4. Click the **Save** button in the top right corner of the page to save your config.

5. Go to the **CONTROL** tab and expand the camera's remote control card to test the camera stream.
   If you don't see an image stream, you need to [configure the `video_path` attribute](/components/camera/webcam/#using-video_path).

For more detailed information, including optional attribute configuration, see the [`webcam` docs](/components/camera/webcam/).

{{< /expand >}}
{{< expand "Step 4: Configure data capture on the camera" >}}

1. Return to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com/).
   Locate the configuration card for your camera.

2. Click the **Add method** button.
   When the **Create data management service** prompt pops up, click to add the service to your machine.
   Leave the default settings.

3. Scroll back up to your camera config card.
   In the **Data capture** section:

   - Click the **Method** dropdown and select **ReadImage**.

   - Set the frequency to `0.1` to capture an image every 10 seconds.

   - Set the MIME type to `image/png`.

For more detailed information on data capture, see [Configure Data Capture](/services/data/capture/).
For more on the camera API, see [Camera Component](/components/camera/#getimage).

{{< /expand >}}
{{< expand "Step 5: View the captured image data" >}}

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

{{% /expand%}}
{{< expand "Step 3: Configure a board" >}}

Then, [add a board component](/components/board/), such as a [Raspberry Pi board](/components/board/pi/).

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

{{< /expand >}}

{{< expand "Step 4: Configure a sensor" >}}

[Add a sensor component](/components/sensor/), such as a [gpio motor](/components/motor/gpio/).
Ensure your sensor and board are properly connected.

![The CONFIGURE tab of the Viam app populated with a configured gpio motor.](/components/motor/gpio-config-ui.png)

{{< /expand >}}

{{< expand "Step 5: Choose how you will control the motor" >}}

You can control your motor directly from the Viam app, using the mobile app, or programmatically.

### Option 1: Control from the app

Navigate to your machine's **CONTROL** tab in the Viam app and use the **Power %** slider to set the motor's speed.
Use the **Backwards** and **Forwards** buttons to change the direction.

{{<gif webm_src="/get-started/quickstarts/motor-control.webm" mp4_src="/get-started/quickstarts/motor-control.mp4" alt="Using the slider, Backwards, and Forwards buttons on the Viam app to control the direction and speed of a configured motor" class="aligncenter"  min-height="750px">}}

### Option 2: Control from the mobile app

You can use [the Viam mobile app](/fleet/#the-viam-mobile-app) to control your motor's speed and direction directly from your smart device.

Open the Viam mobile app and log in to your account.
Select the location where your machine is assigned.
Choose your machine from the list and use the mobile interface to adjust the motor settings.

Select the location that your machine is assigned to from the **Locations** tab.

{{<gif webm_src="/get-started/quickstarts/mobile-app-motor-control.webm" mp4_src="/get-started/quickstarts/mobile-app-motor-control.mp4" alt="Using an example machine on the Viam mobile app to set the direction and speed of a configured motor using the slider on the user interface" max-height="50px" max-width="200px" class="HELLO aligncenter">}}

### Option 3: Control programmatically

You can use the following code to control the motor's speed and direction using your preferred SDK.
Find your machine's API key and address on your machine's **CONNECT** tab.

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

## Next steps

Now that you have made a motor move, explore other components, or related servies:

{{< cards >}}
{{% card link="/components/" %}}
{{% card link="/services/navigation/" %}}
{{% card link="/services/SLAM/" %}}
{{< /cards >}}

To see motors in real-world projects, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/confetti-bot/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/configure/configure-rover/" %}}
{{< /cards >}}
