---
title: "Monitor Job Site Helmet Usage with Computer Vision"
linkTitle: "Helmet Monitor"
type: "docs"
description: "Get a text or email if people are not wearing hard hats, and track data over time."
videos: ["/tutorials/helmet/hardhat.webm", "/tutorials/helmet/hardhat.mp4"]
images: ["/tutorials/helmet/hardhat-data.png"]
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
Luckily, you can address this problem using Viam's integrated [data capture](/data/capture/), [computer vision](/ml/vision/), and [webhooks](/build/configure/#webhooks), along with a hard hat detection model.

Through this tutorial you will build a system to look out for you and your team, sending an email notification when someone isn't wearing a hard hat.

{{<gif webm_src="/tutorials/helmet/hardhat.webm" mp4_src="/tutorials/helmet/hardhat.mp4" alt="A man without a hard hat is detected and labeled as No-Hardhat. Then he puts on a hard hat and a bounding box labeled Hardhat appears. He gives a thumbs-up to the camera." class="alignleft" max-width="250px">}}

First, you'll set up and test the computer vision functionality.
Next, you'll set up data capture to pull images of people without hard hats into the cloud.
Then, you'll write a serverless function capable of sending email notifications.
Finally, you'll configure a webhook to trigger the serverless function when someone isn't wearing a hard hat.

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

Plug your webcam into your computer.

Make sure your computer (whether it's a personal computer or an SBC) is connected to adequate power, and turn it on.

If you haven't already, [install `viam-server`](/get-started/installation/) on the computer you're using for this project, and set up the connection between your machine and the [Viam app](https://app.viam.com).

## Configure the camera and computer vision

### Configure your physical camera

Configure your [webcam](/components/camera/webcam/) so that your machine knows where to pull images from:

1. On the [Viam app](https://app.viam.com), navigate to your machine's page.
   Check that the **Last online** indicator reads "Live"; this indicates that your machine is turned on and that its instance of `viam-server` is in contact with the Viam app.

2. Click **Create component** in the lower-left corner of the page.
   Start typing "webcam" and select **camera / webcam**.
   Give your camera a name.
   This tutorial uses the name `my_webcam` in all example code.
   Click **Create**.

3. Click the **video path** dropdown and select the webcam you'd like to use for this project from the list of suggestions.

4. At the bottom of the screen, click **Save config**.

### Test your physical camera

To test your camera, go to the **Control** tab and click to expand your camera's panel.

Toggle **View `my_webcam`** to the "on" position.
The video feed should display.
If it doesn't, double-check that your config is saved correctly, and check the **Logs** tab for errors.

### Configure the vision service

Now that you know the camera is properly connected to your machine, it is time to add computer vision by configuring the [vision service](/ml/vision/) on your machine.
Viam's built-in [`mlmodel` vision service](/ml/vision/mlmodel/) works with Tensor Flow Lite models, but since this tutorial uses a YOLOv8 model, we will use a {{< glossary_tooltip term_id="module" text="module" >}} from the [modular resource registry](/registry/) that augments Viam with YOLOv8 integration:

1. Navigate to the **Services** subtab of your machine's **Config** tab.

2. Click **Create service**.
   Start typing `yolo` and select **vision / yolov8** from the registry options.
   Click **Add module**.
   You can find more details about this module in [its readme](https://github.com/viam-labs/YOLOv8).

3. Give your vision service a name, for example `yolo`, and click **Create**.

4. In the **Attributes** box of your new vision service, paste the following JSON:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "model_location": "keremberke/yolov8n-hard-hat-detection"
   }
   ```

   This tells the vision service where to look for [the hard hat detection model](https://huggingface.co/keremberke/yolov8s-hard-hat-detection) we are using for this tutorial.

   Your vision service config should now resemble the following:

   {{<imgproc src="/tutorials/helmet/model-location.png" resize="x1100" declaredimensions=true alt="The vision service configured in the Viam app per the instructions." >}}

5. Click **Save config** at the bottom of the screen.

### Configure the `objectfilter` module

The physical camera is working and the vision service is set up.
Now you will pull them together with the [`objectfilter`](https://app.viam.com/module/felixreichenbach/object-filter) {{< glossary_tooltip term_id="module" text="module" >}}.
This module takes a vision service (in this case, your hard hat detector) and applies it to your webcam feed.
It outputs a stream with bounding boxes around the hard hats (and people without hard hats) in your camera's view so that you can see the detector working.
This module also filters the output so that later, when you configure data management, you can save only the images that contain people without hard hats.

1. Navigate to the **Components** subtab of your machine's **Config** tab.

2. Click **Create component**.
   Start typing `objectfilter` and select **camera / objectfilter** from the results.

3. Name your filtering camera something like `objectfilter-cam` and click **Create**.

4. Paste the following into the attributes box:

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

   If you named your detector something other than "yolo," edit the `detector_name` line accordingly.
   You can also edit the confidence threshold.
   If you change it to `0.2` for example, you will see detections of over 20% confidence.

   Setting the `filter_data` attribute to `true` means that later, when you configure data capture on this camera, only images that contain one or more of the labels will be captured.

   Your `objectfilter` camera configuration should now resemble the following:

   {{<imgproc src="/tutorials/helmet/filtercam-config.png" resize="x1100" declaredimensions=true alt="The detector_cam config panel in the Viam app." >}}

5. Click **Save config** at the bottom of the screen.

### Test the detector

Now that the detector is configured, it's time to test it!

1. Navigate to the **Control** tab.

2. Click the **objectfilter_cam** panel to open your detector camera controls.

3. Toggle **View objectfilter_cam** to the "on" position.
   This displays a live feed from your webcam with detection bounding boxes overlaid on it.

4. The detector can recognize humans with and without hard hats on.
   Try positioning yourself in front of the camera without anything on your head, and then with a helmet on, and watch the bounding boxes appear.

   {{<imgproc src="/tutorials/helmet/no-hard-hat1.png" resize="x1100" declaredimensions=true alt="A person with no hard hat on, with a bounding box labeled No-Hardhat around her head." >}}

## Configure data capture and sync

Viam's built-in [data management service](/data/) allows you to, among other things, capture images and sync them to the cloud.
Configure data capture on the `objectfilter` camera to capture images of people without hard hats:

1. First, you need to add the data service to your machine to make it available to capture data on your camera.

   Navigate to the **Services** subtab of your machine's **Config** tab.

   Click **Create service**.
   Type "data" and click **data management / RDK**.
   Name your data management service `data-manager` and click **Create**.

   Leave all the default data service attributes as they are and click **Save config**.

2. Now you're ready to enable data capture on your detector camera.
   Navigate to the **Components** subtab.
   Locate the `objectfilter-cam` panel.

3. Click **Add method**.
   Click the **Type** dropdown and select **ReadImage**.
   Set the capture frequency to `0.2` images per second (equivalent to one image every 5 seconds).
   You can always change the frequency to suit your use case.

   {{<imgproc src="/tutorials/helmet/datacapture-config.png" resize="x1100" declaredimensions=true alt="The objectfilter cam configured with data capture set to read images at 0.2 hertz. Mime type is left at the default image/jpeg." >}}

### Test data capture and sync

To make sure the detector camera is capturing and syncing labeled images:

1. Position yourself in front of your webcam for 30 seconds or so to let it capture a few images of a person without a hard hat on.

2. Navigate to your [**DATA** page](https://app.viam.com/data/view?view=images) in the Viam app.
   You should see some images with bounding boxes on them.
   If you do not, try refreshing the page.

   {{<imgproc src="/tutorials/helmet/synced-data.png" resize="x1000" declaredimensions=true alt="The data manager page in the Viam app, displaying three images of a person with a bounding box labeled NO-Hardhat around her face." >}}

3. You can also try this with a hard hat on your head.

   {{<imgproc src="/tutorials/helmet/hardhat-data.png" resize="x1000" declaredimensions=true alt="The data manager page in the Viam app, displaying three images of a person with a bounding box labeled NO-Hardhat around her face." >}}

### Modify the detector config to sync only images without hard hats

Until now, you've been identifying people without hard hats as well as people with hard hats.
Now that you have verified that the detector and data sync are working, modify your config so that only images with people _without_ hard hats are captured:

1. Navigate to your `objectfilter-cam` card on the **Config** tab.

2. Delete the `"Hardhat",` line from the `"labels"` array.

3. Click **Save config**.

## Set up email notifications

[Webhooks](https://en.wikipedia.org/wiki/Webhook) are a way to trigger a custom function to run when a certain event happens.
For the purposes of this project, you will use a webhook to run a function that sends you an email when an image of someone without a hard hat is uploaded to the cloud.

Before you configure a webhook on your machine, you need to create a serverless function for the webhook to call.

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

To write a function that sends an email, you need to configure credentials to authenticate to the sending email account.
For this project we used [SendGrid](https://sendgrid.com) (which has a free tier) to make configuration of your email notifications simpler:

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

1. Copy and paste the following code into your cloud function source code `main.py` file:

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

The webhook you will configure with Viam invokes the function with an HTTP request.
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

### Configure a webhook on your machine

Now it's time to configure a [webhook](/build/configure/#webhooks) on your machine to trigger the email cloud function when a person is not wearing a hard hat.
Since you configured data to sync only when an image of a person without a hard hat is captured, configuring the webhook to trigger each time an image is synced to the cloud will produce the desired result.

Configure a webhook as follows:

1. Navigate to the **Config** tab of your machine.
   Toggle the **Mode** to **Raw JSON**.

2. Paste the following JSON template into your raw JSON config.
   `"webhooks"` is a top-level section like `"components"`, `"services"`, or any of the other config sections.

   ```json {class="line-numbers linkable-line-numbers"}
     "webhooks": [
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
   Once you've done this, the `url` line should resemble, for example, `"url": "https://us-east1-blah-blah-123456.cloudfunctions.net/hat-email"`.

4. Click **Save config**.

## Test the whole system

You've built all the pieces of the system and connected them together.
Now it's time to test the whole thing.

Make sure `viam-server` is running on your machine.
Position yourself, without a hard hat, in front of your camera.
Wait a couple of minutes for the email to arrive in your inbox, then celebrate your success when it does!
Great work!

## Next steps

Here are some ways you could expand on this project:

- Mount a camera on a rover and either drive it manually using remote control, or use the motion and navigation services to plan paths for the rover.
  Or, mount cameras in multiple places.

- Change your cloud function to send a different kind of notification, or trigger some other action.
  For an example demonstrating how to configure text notifications, see the [Detect a Person and Send a Photo tutorial](/tutorials/projects/send-security-photo/).

- Use a different existing model or [train your own](/ml/train-model/), to detect and send notifications about something else such as [forklifts](https://huggingface.co/keremberke/yolov8m-forklift-detection).

{{< cards >}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{% card link="/ml/train-model/" %}}
{{% card link="/tutorials/configure/scuttlebot/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
