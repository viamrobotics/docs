---
title: "Monitor Job Site Helmet Usage with Computer Vision"
linkTitle: "Helmet Monitor"
type: "docs"
description: "Get an email alert if people are not wearing hard hats."
videos: ["/tutorials/helmet/hardhat.webm", "/tutorials/helmet/hardhat.mp4"]
images: ["/tutorials/helmet/hardhat.gif"]
videoAlt: "A man without a hard hat is detected and labeled as No-Hardhat. Then he puts on a hard hat and a bounding box labeled Hardhat appears. He gives a thumbs-up to the camera."
tags: ["tutorial"]
authors: [Jessamy Taylor]
languages: []
viamresources: ["camera", "data_manager", "mlmodel", "vision"]
level: "Intermediate"
date: "2024-03-05"
cost: 120
---

{{<imgproc src="/tutorials/helmet/ppe-hooks.png" resize="x300" declaredimensions=true alt="Hard hats and neon reflective vests on hooks." class="alignright" style="max-width: 350px">}}

We all know personal protective equipment (PPE) helps keep us safe, but sometimes we need a reminder to use it consistently.
Luckily, you can address this problem using Viam's integrated [data capture](/services/data/capture/), [computer vision](/services/vision/), and [triggers](/configure/triggers/), along with a hard hat detection model.

By following this tutorial you will build a system to look out for you and your team, sending an email notification when someone isn't wearing a hard hat.

{{<gif webm_src="/tutorials/helmet/hardhat.webm" mp4_src="/tutorials/helmet/hardhat.mp4" alt="A man without a hard hat is detected and labeled as No-Hardhat. Then he puts on a hard hat and a bounding box labeled Hardhat appears. He gives a thumbs-up to the camera." class="alignleft" max-width="250px">}}

First, you'll set up and test the computer vision functionality that can detect people wearing a hard hat and wearing no hard hat.
Next, you'll set up data capture and sync to record images of people without hard hats and upload them to the cloud.
Then, you'll write a serverless function capable of sending email notifications.
Finally, you'll configure a trigger to trigger the serverless function when someone isn't wearing a hard hat.

{{< alert title="Learning Goals" color="info" >}}

After completing this tutorial, you will:

- know how the ML model service and the vision service work together
- be able to use the ML model service and the vision service on a machine with an existing model to interpret the world around the machine
- be able to use data capture and triggers to set up notifications based on a machine's perception of the world around it

{{< /alert >}}

## Requirements

### Required hardware

- A camera such as a standard USB webcam.
  You can also test the hard hat detection system using the webcam built into your laptop.
- A computer capable of running [`viam-server`](/get-started/installation/).
  You can use a personal computer running macOS or Linux, or a single-board computer (SBC) running 64-bit Linux.

### Optional hardware

If you want to set up your camera far away from your personal computer, you can use a webcam plugged into a single-board computer, powered by batteries.
You could mount your machine in a stationary location like on a pole, or you could mount it on a rover.
This tutorial covers the software side; you can get creative with the hardware.

Note that your machine must be connected to the internet for data sync and email notifications to work.

### Required software

- [`viam-server`](/get-started/installation/)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/), integrated with Viam using the [YOLOv8 modular service](https://github.com/viam-labs/YOLOv8)
- [YOLOv8 Hard Hat Detection model](https://huggingface.co/keremberke/yolov8s-hard-hat-detection)
- [`objectfilter-camera`](https://github.com/felixreichenbach/objectfilter-camera) {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}
- [Google Cloud Functions](https://cloud.google.com/functions)
- Python 3.8
- [SendGrid](https://sendgrid.com/en-us)

## Set up your helmet monitor

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
   This tutorial uses the name `my_webcam` in all example code.
   Click **Create**.

3. Click the **video path** dropdown and select the webcam you'd like to use for this project from the list of suggestions.

4. Click **Save** in the top right corner of the screen to save your changes.

### Test your physical camera

To test your camera, go to the **CONTROL** tab and click to expand your camera's panel.

Toggle **View `my_webcam`** to the "on" position.
The video feed should display.
If it doesn't, double-check that your config is saved correctly, and check the **LOGS** tab for errors.

### Configure the vision service

Now that you know the camera is properly connected to your machine, it is time to add computer vision by configuring the [vision service](/services/vision/) on your machine.
Viam's built-in [`mlmodel` vision service](/services/vision/mlmodel/) works with Tensor Flow Lite models, but since this tutorial uses a YOLOv8 model, we will use a {{< glossary_tooltip term_id="module" text="module" >}} from the [modular resource registry](/registry/) that augments Viam with YOLOv8 integration.
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

### Configure the `objectfilter` module

The physical camera is working and the vision service is set up.
Now you will pull them together with the [`objectfilter`](https://app.viam.com/module/felixreichenbach/object-filter) {{< glossary_tooltip term_id="module" text="module" >}}.
This module takes a vision service (in this case, your hard hat detector) and applies it to your webcam feed.
It outputs a stream with bounding boxes around the hard hats (and people without hard hats) in your camera's view so that you can see the detector working.
This module also filters the output so that later, when you configure data management, you can save only the images that contain people without hard hats rather than all images the camera captures.

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
     "labels": ["Hardhat", "NO-Hardhat"],
     "confidence": 0.5,
     "display_boxes": true
   }
   ```

   If you named your detector something other than "yolo," edit the `vision_services` value accordingly.
   You can also edit the confidence threshold.
   If you change it to `0.6` for example, the `objectfilter` camera will only return labeled bounding boxes when the vision model indicates at least 60% confidence that the object is a hard hat or a person without a hard hat.

   Setting the `filter_data` attribute to `true` means that later, when you configure data capture on this camera, only images that have one or more of the labels will be captured and sent to the cloud.
   For testing purposes, leave both labels in the array for now.
   We will remove the `"Hardhat"` label from the configuration later so that the camera only captures and saves images when someone **isn't** wearing a hard hat.

   Your `objectfilter` camera configuration should now resemble the following:

   {{<imgproc src="/tutorials/helmet/filtercam-config.png" resize="x1100" declaredimensions=true alt="The detector_cam config panel in the Viam app." >}}

5. Click **Save** in the top right corner of the screen to save your changes.

### Test the detector

Now that the detector is configured, it's time to test it!

1. Navigate to the **CONTROL** tab.

2. Click the **objectfilter_cam** panel to open your detector camera controls.

3. Toggle **View objectfilter_cam** to the "on" position.
   This displays a live feed from your webcam with detection bounding boxes overlaid on it.

4. The detector can recognize humans with and without hard hats on.
   Try positioning yourself in front of the camera without anything on your head, and then with a helmet on, and watch the bounding boxes appear.

   {{<imgproc src="/tutorials/helmet/no-hard-hat1.png" resize="x1100" declaredimensions=true alt="A person with no hard hat on, with a bounding box labeled No-Hardhat around her head." >}}

## Configure data capture and sync

Viam's built-in [data management service](/services/data/) allows you to, among other things, capture images and sync them to the cloud.
For this project, you will capture images of people without hard hats so that you can see who wasn't wearing one, and so that you can trigger notifications when these images are captured and synced.
Configure data capture on the `objectfilter` camera to capture images of people without hard hats:

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

   {{<imgproc src="/tutorials/helmet/datacapture-config.png" resize="x1100" declaredimensions=true alt="The objectfilter cam configured with data capture set to read images at 0.2 hertz. MIME type is set to image/jpeg." >}}

### Test data capture and sync

To make sure the detector camera is capturing and syncing labeled images:

1. Position yourself in front of your webcam for approximately 30 seconds to let it capture a few images of a person without a hard hat on.

2. Navigate to your [**DATA** page](https://app.viam.com/data/view?view=images) in the Viam app.
   You should see some images with bounding boxes on them.
   If you do not, try refreshing the page.

   {{<imgproc src="/tutorials/helmet/synced-data.png" resize="x1000" declaredimensions=true alt="The data manager page in the Viam app, displaying three images of a person with a bounding box labeled NO-Hardhat around her face." >}}

3. You can also try this with a hard hat on your head.

   {{<imgproc src="/tutorials/helmet/hardhat-data.png" resize="x1000" declaredimensions=true alt="The data manager page in the Viam app, displaying three images of a person with a bounding box labeled NO-Hardhat around her face." >}}

### Modify the detector config to sync only images without hard hats

Until now, you've been identifying people without hard hats as well as people with hard hats.
Now that you have verified that the detector and data sync are working, modify your config so that only images with people _without_ hard hats are captured:

1. Navigate to your `objectfilter-cam` card on the **CONFIGURE** tab.

2. Delete the `"Hardhat",` line from the `"labels"` array.

3. Click **Save** in the top right corner of the screen to save your changes.

## Set up email notifications

[Triggers](/configure/triggers/) allow you to trigger actions by sending an HTML request when a certain event happens.
In this case, you're going to set up a trigger to trigger a serverless function that sends you an email when an image of someone without a hard hat is uploaded to the cloud.

Before you configure a trigger on your machine, you need to create a serverless function for the trigger to call.

### Create a serverless function

A serverless function is a simple script that is hosted by a service such as [Google Cloud Functions](https://cloud.google.com/functions) or [AWS Lambda](https://aws.amazon.com/pm/lambda).
You don't need to host it on your machine; instead, it is always available and runs only when an event triggers it.

#### Set up your cloud function scaffold

For this project, we used Google Cloud Functions, and wrote our function in Python.
If you are new to cloud functions, you may find [this getting started guide](https://cloud.google.com/functions/docs/console-quickstart) useful.

1. Create a Google Cloud (GCP) account.
2. Create a project, then search for **Cloud Functions** in the Google Cloud console search bar.
3. Click **CREATE FUNCTION**.
4. Choose `1st gen` as the **Environment**.
5. Give your function a name.
   We called ours "hat-email."
6. Choose your region.
7. For trigger type, choose `HTTP`.
8. Click **NEXT**.
9. For **Runtime**, choose `Python 3.8`.
10. Click **Deploy**.
    The demo function won't do anything exciting yet; keep going through the next few sections before testing it.

#### Configure email credentials

To write a function that sends an email, you need a service that can send emails.
For this project we used [SendGrid](https://sendgrid.com) (which has a free tier) to make configuration of your email notifications simpler.
Follow these instructions to create a SendGrid account and configure the SendGrid API credentials for your Google Cloud Function:

1. [Enable SendGrid Email API](https://console.cloud.google.com/marketplace/details/sendgrid-app/sendgrid-email) through the Google Cloud Marketplace.
1. Create a SendGrid account and confirm your email.
1. Create a [SendGrid API key](https://docs.sendgrid.com/ui/account-and-settings/api-keys) with **Mail Send > Full Access** permissions.
1. Store your API key with the Google Cloud Function console:
   1. In the top banner of your console, click **Edit**.
   2. Click to expand **Runtime, build, connections and security settings**.
   3. Under **Runtime environment variables**, click **ADD VARIABLE**.
      For the name, enter `EMAIL_API_KEY`.
      For the value, paste the API key you generated with SendGrid.
   4. Click **NEXT**.

#### Write the cloud function code

SendGrid's [Email API Quickstart](https://docs.sendgrid.com/for-developers/sending-email/quickstart-python) contains more information about the functionality of the SendGrid API.
The following code is adapted from that example.

1. Copy and paste the following code into your cloud function source code `main.py` file and change the email address parameters `from_email` and `to_emails`:

   ```python {class="line-numbers linkable-line-numbers"}
   import functions_framework
   import os
   import sendgrid
   from sendgrid import SendGridAPIClient
   from sendgrid.helpers.mail import Mail, Email, To, Content
   from python_http_client.exceptions import HTTPError

   def email(request):

       sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('EMAIL_API_KEY'))

       message = Mail(
        # TODO: Change to the email you created the API key for
        from_email='youremailaddresstosendfrom@example.com',
        # TODO: Change to whichever email should receive the notification
        to_emails='youremailaddresstosendto@example.com',
        subject='Put on a helmet!',
        html_content='Hello!<br><br>Please remember to keep \
        hard hats on where required. Thank you! \
        <br><br>You can view captured images in \
        <a href="https://app.viam.com/data/view?view=images">\
        the DATA tab</a of the Viam app>.'
    )

       # Get a JSON-ready representation of the Mail object
       mail_json = message.get()

       # Send an HTTP POST request to /mail/send
       response = sg.client.mail.send.post(request_body=mail_json)
   ```

2. Edit the **Entry point** field from `hello_world` to `email` to match the function name.

3. Select <file>requirements.txt</file> (below <file>main.py</file> on the **SOURCE** console tab) and add the required dependencies:

   ```text {class="line-numbers linkable-line-numbers"}
   # Function dependencies, for example:
   # package>=version
   sendgrid
   functions-framework
   ```

#### Register an HTTP function

The trigger you will configure with Viam invokes the function with an HTTP request.
You can learn more about HTTP functions in [Google's Write HTTP functions guide](https://cloud.google.com/functions/docs/writing/write-http-functions).

You need to add `@functions_framework.http` at the top of your function to register the HTTP function, and you need to add a `return` statement at the bottom to return an HTTP response.
Your final code should look like this:

```python {class="line-numbers linkable-line-numbers" data-line="9,33"}
import functions_framework
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from python_http_client.exceptions import HTTPError


@functions_framework.http
def email(request):

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('EMAIL_API_KEY'))

    message = Mail(
        # Change to the email you created the API key for
        from_email='youremailaddresstosendfrom@example.com',
        # Change to whichever email should receive the notification
        to_emails='youremailaddresstosendto@example.com',
        subject='Put on a helmet!',
        html_content='Hello!<br><br>Please remember to keep \
        hard hats on where required. Thank you! \
        <br><br>You can view captured images in \
        <a href="https://app.viam.com/data/view?view=images">\
        the DATA tab</a of the Viam app>.'
    )

    # Get a JSON-ready representation of the Mail object
    mail_json = message.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)

    return 'Notification sent.'
```

Click **DEPLOY**.

For simplicity while developing and testing your code, you can [allow unauthenticated HTTP function invocation](https://cloud.google.com/functions/docs/securing/managing-access-iam#allowing_unauthenticated_http_function_invocation), though we recommend that you ultimately set up proper authentication for better security.

#### Test the cloud function

Now you can test the script:

1. Navigate to the **TRIGGER** tab in the Google Cloud console.

2. Click the copy button to copy the trigger URL.
   Paste it into a new browser window and hit your **Enter** key.
   The browser should display "Notification sent."
   If it displays an error, double-check your code, and double-check your [access authorization](https://cloud.google.com/functions/docs/securing/managing-access-iam).

3. Check your email inbox.

   {{<imgproc src="/tutorials/helmet/email-received.png" resize="x600" declaredimensions=true alt="The email, opened in a web email client." style="max-width: 400px" >}}

   If you don't see an email, check your spam folder.
   If you still don't see an email, make sure your SendGrid account is fully set up (2FA enabled, email confirmed) and that your email API key is [correctly configured](#configure-email-credentials).

### Configure a trigger on your machine

Now it's time to configure a [trigger](/configure/triggers/) on your machine to trigger the email cloud function when a person is not wearing a hard hat.
Since you configured data to sync only when an image of a person without a hard hat is captured, configuring the trigger to trigger each time an image is synced to the cloud will produce the desired result.

Configure a trigger as follows:

1. Navigate to the **CONFIGURE** tab of your machine.
   Select **JSON** mode in the left-hand menu.

2. Paste the following JSON template into your JSON config.
   `"triggers"` is a top-level section like `"components"`, `"services"`, or any of the other config sections.

   ```json {class="line-numbers linkable-line-numbers"}
     "triggers": [
       {
         "url": "<Insert your own cloud function URL>",
         "event": {
           "attributes": {
             "data_types": ["binary"]
           },
           "type": "part_data_ingested"
         }
       }
     ]
   ```

3. Replace the `url` value with your cloud function URL.
   You can get this URL by copying it from the **TRIGGER** tab in the cloud function console.
   Once you've done this, the `url` line should resemble, for example, `"url": "https://us-east1-example-string-123456.cloudfunctions.net/hat-email"`.

4. Click **Save** in the top right corner of the screen to save your changes.

## Test the whole system

You've built all the pieces of the system and connected them together.
Now it's time to test the whole thing.

Make sure `viam-server` is running on your machine.
Position yourself, without a hard hat, in front of your camera.
Wait a couple of minutes for the email to arrive in your inbox.
Congratulations, you've successfully built your hard hat monitor!

## Next steps

Here are some ways you could expand on this project:

- Mount a camera on a rover and either drive it manually using remote control, or use the motion and navigation services to plan paths for the rover.
  Or, mount cameras in multiple places.

- Change your cloud function to send a different kind of notification, or trigger some other action.
  For an example demonstrating how to configure text notifications, see the [Detect a Person and Send a Photo tutorial](/tutorials/projects/send-security-photo/).

- Use a different existing model or [train your own](/services/ml/train-model/), to detect and send notifications about something else such as [forklifts](https://huggingface.co/keremberke/yolov8m-forklift-detection) appearing in your camera stream.

{{< cards >}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{% card link="/services/ml/train-model/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
