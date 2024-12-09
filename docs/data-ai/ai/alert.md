---
linkTitle: "Alert on inferences"
title: "Alert on inferences"
weight: 60
layout: "docs"
type: "docs"
no_list: true
description: "TODO"
---

You can use triggers to send webhooks when certain inferences are made.
For an example of this, see the [Helmet Monitoring tutorial](/tutorials/projects/helmet/).

<!-- todo: intro more generally focused on alerts -->

On this page, you'll learn how to use triggers to send alerts in the form of email notifications when certain detections are made.

You will build a system that can monitor camera feeds and detect situations that require review.
In other words, this system performs anomaly detection.
Whenever the system detects an anomaly, it will send an email notification.

First, you'll set up and test the computer vision functionality.
Next, you'll set up data capture and sync to record images with the anomaly and upload them to the cloud.
Finally, you'll configure a trigger to send email notifications when the anomaly is detected.

## Requirements

### Required hardware

- A camera such as a standard USB webcam.
  You can also test the anomaly detection system using the webcam built into your laptop.
- A computer capable of running [`viam-server`](/installation/viam-server-setup/).
  You can use a personal computer running macOS or Linux, or a single-board computer (SBC) running 64-bit Linux.

### Optional hardware

If you want to set up your camera far away from your personal computer, you can use a webcam plugged into a single-board computer, powered by batteries.
You could mount your machine in a stationary location like on a pole, or you could mount it on a rover.
This tutorial covers the software side; you can get creative with the hardware.

Note that your machine must be connected to the internet for data sync and email notifications to work.

### Required software

- [`viam-server`](/installation/viam-server-setup/)
- [`objectfilter-camera`](https://github.com/felixreichenbach/objectfilter-camera) {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}
- Python 3.8

## Set up your monitor

Get your hardware ready and connected to the Viam platform:

Plug your webcam into your computer.
Then, make sure your computer (whether it's a personal computer or an SBC) is connected to adequate power, and turn it on.

{{% snippet "setup.md" %}}

## Configure the camera and computer vision

### Configure your physical camera

Configure your [webcam](/components/camera/webcam/) so that your machine can get the video stream from the camera:

1. On the [Viam app](https://app.viam.com), navigate to your machine's page.
   Check that the part status dropdown in the upper left of the page, next to your machine's name, reads "Live"; this indicates that your machine is turned on and that its instance of `viam-server` is in contact with the Viam app.

2. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component**.
   Start typing "webcam" and select **camera / webcam**.
   Give your camera a name.
   This guide uses the name `my_webcam` in all example code.
   Click **Create**.

3. Click the **video path** dropdown and select the webcam you'd like to use for this project from the list of suggestions.

4. Click **Save** in the top right corner of the screen to save your changes.

### Test your physical camera

To test your camera, go to the **CONTROL** tab and click to expand your camera's panel.

Toggle **View `my_webcam`** to the "on" position.
The video feed should display.
If it doesn't, double-check that your config is saved correctly, and check the **LOGS** tab for errors.

### Find a model and configure an ML model service

You must use an object detection model to use the `objectfilter` module.
You can use an object detection ML model from the registry or train one yourself with Viam's built-in tools for [TFLite](/data-ai/ai/train-tflite/) or with another framework using a [custom training script](/data-ai/ai/train/).

Before you can run an computer vision service on your machine, you usually need to configure an ML model service to deploy the module.

{{% alert title="Note" color="note" %}}
This is not the case when the functionality to deploy the ML model is bundled into the vision service, for example with the [`YOLOv8`](https://app.viam.com/module/viam-labs/YOLOv8) {{< glossary_tooltip term_id="module" text="module" >}}.

If you are using one of those modular vision services, you can move on to [Configure a vision service](#configure-a-vision-service).
{{% /alert %}}

What model of ML model service you use depends on the framework of the computer vision model you want to use, like TFLite, Tensorflow, or ONNX.

To configure an ML model service, [add the ML model service](/data-ai/reference/ml/) and [deploy the model](/data-ai/ai/deploy/).

### Configure a vision service

Now it is time to add computer vision by configuring the [vision service](/services/vision/) on your machine.

If you are using an ML model service, you will probably want to use the `mlmodel` computer vision model.
Follow the instructions to [configure an `mlmodel` vision service](/data-ai/reference/vision/mlmodel/).
However, the [Viam registry](https://app.viam.com/registry) also provides many modules of vision service that you could use.
For example, if you were to configure hard hat detection with a YOLOv8 model, you would use the `yolov8` module (without an ML model service):

{{% expand "instructions for configuring a YOLOv8 module" %}}

Viam's built-in [`mlmodel` vision service](/services/vision/mlmodel/) works with Tensor Flow Lite models, but since the hard hat detection uses a YOLOv8 model, we will use a {{< glossary_tooltip term_id="module" text="module" >}} from the [modular resource registry](/registry/) that augments Viam with YOLOv8 integration.
The [YOLOv8 module](https://github.com/viam-labs/YOLOv8) enables you to use any [YOLOv8 model](https://huggingface.co/models?other=yolov8) with your Viam machines.

1. Navigate to your machine's **CONFIGURE** tab.

2. Click the **+** (Create) button next to your main part in the left-hand menu and select **Service**.
   Start typing `yolo` and select **vision / yolov8** from the registry options.
   Click **Add module**.

3. Give your vision service a name, for example `yolo`, and click **Create**.

4. In the attributes field of your new vision service, paste the following JSON:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "model_location": "keremberke/yolov8n-hard-hat-detection"
   }
   ```

   This tells the vision service where to look for [the hard hat detection model](https://huggingface.co/keremberke/yolov8s-hard-hat-detection) we are using for this tutorial.

   Your vision service config should now resemble the following:

   {{<imgproc src="/tutorials/helmet/model-location.png" resize="x1100" declaredimensions=true alt="The vision service configured in the Viam app per the instructions." >}}

5. Click **Save** in the top right corner of the screen to save your changes.

{{% /expand%}}

With the vision service configured, you can view the inferences provided on the **CONTROL** tab of the Viam app or get them programmatically using the [vision service API](/data-ai/reference/vision-client/).

### Configure the `objectfilter` module

Now, your physical camera is working and the vision service is set up.
Now you will pull them together to filter out only images where an inference is made with the [`objectfilter`](https://app.viam.com/module/felixr/object-filter) {{< glossary_tooltip term_id="module" text="module" >}}.
This camera module takes the vision service and applies it to your webcam feed.
It outputs a stream with bounding boxes around the inferences in your camera's view so that you can see the detector working.
This module also filters the output so that later, when you configure data management, you can save only the images that contain people without hard hats rather than all images the camera captures.

Configure the module with `"labels"` according to the labels your ML model provides that you want to alert on.
Set the `"filter_data"` attribute to `true` so that later, when you configure data capture on this camera, only images that have one or more of the labels will be captured and sent to the cloud.
For example, if using the YOLOv8 model (named `yolo`) for hardhat detection, you would configure the module like the following:

{{% expand "instructions for configuring the objectfilter module for detecting people without a hardhat" %}}

1. Navigate to your machine's **CONFIGURE** tab.

2. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component**.
   Start typing `objectfilter` and select **camera / objectfilter** from the results.
   Click **Add module**.

3. Name your filtering camera something like `objectfilter-cam` and click **Create**.

4. Paste the following into the attributes field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "filter_data": true,
     "camera": "my_webcam",
     "vision_services": ["yolo"],
     "labels": ["NO-Hardhat"],
     "confidence": 0.5,
     "display_boxes": true
   }
   ```

   If you named your detector something other than "yolo," edit the `vision_services` value accordingly.
   You can also edit the confidence threshold.
   If you change it to `0.6` for example, the `objectfilter` camera will only return labeled bounding boxes when the vision model indicates at least 60% confidence that the object is a hard hat or a person without a hard hat.

   Your `objectfilter` camera configuration should now resemble the following:

   {{<imgproc src="/tutorials/helmet/filtercam-config.png" resize="x1100" declaredimensions=true alt="The detector_cam config panel in the Viam app." >}}

5. Click **Save** in the top right corner of the screen to save your changes.

{{% /expand%}}

### Test the detector

Now that the detector is configured, it's time to test it!

1. Navigate to the **CONTROL** tab.

2. Click the **objectfilter_cam** panel to open your detector camera controls.

3. Toggle **View objectfilter_cam** to the "on" position.
   This displays a live feed from your webcam with detection bounding boxes overlaid on it.

For example, if detecting the presence of hard hats:

{{<imgproc src="/tutorials/helmet/no-hard-hat1.png" resize="x1100" declaredimensions=true alt="A person with no hard hat on, with a bounding box labeled No-Hardhat around her head." >}}

## Configure data capture and sync

Viam's built-in [data management service](/services/data/) allows you to, among other things, capture images and sync them to the cloud.

Configure data capture on the `objectfilter` camera to capture images of detections:

1. First, you need to add the data service to your machine to make it available to capture data on your camera.

   Navigate to your machine's **CONFIGURE** tab.

   Click the **+** (Create) button next to your main part in the left-hand menu and select **Service**.
   Type "data" and click **data management / RDK**.
   Name your data management service `data-manager` and click **Create**.

   Leave all the default data service attributes as they are and click **Save** in the top right corner of the screen to save your changes.

2. Now you're ready to enable data capture on your detector camera.
   Locate the `objectfilter-cam` panel.

3. Click **Add method**.
   Click the **Type** dropdown and select **ReadImage**.
   Set the capture frequency to `0.2` images per second (equivalent to one image every 5 seconds).
   You can always change the frequency to suit your use case.
   Set the **MIME type** to `image/jpeg`.

## Set up alerts

[Triggers](/configure/triggers/) allow you to send webhook requests or email notifications when certain events happen.

You can use the **Data has been synced to the cloud** trigger to send email alerts whenever an image with an anomaly detection is synced to the cloud from your object filter camera.

### Configure a trigger on your machine

Now it's time to configure a trigger so that you get an email when a person is not wearing a hard hat.

Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
Click the **+** (Create) button in the left side menu and select **Trigger**.

Name the trigger and click **Create**.

Select trigger **Type** as **Data has been synced to the cloud** and **Data Types** as **Binary (image)**.

{{<imgproc src="/tutorials/helmet/trigger.png" resize="x300" declaredimensions=true alt="The trigger created with data has been synced to the cloud as the type and binary (image) as the data type." >}}

To configure notifications, add an email address.
Also configure the time between notifications.

Click **Save** in the top right corner of the screen to save your changes.

## Test the whole system

You've built all the pieces of the system and connected them together.
Now it's time to test the whole thing.

Make sure `viam-server` is running on your machine.
Run your camera in front of what you're detecting and wait for an anomaly to appear.
Wait a couple of minutes for the email to arrive in your inbox.
Congratulations, you've successfully built your anomaly detection monitor!

## Next steps

{{< cards >}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}