---
linkTitle: "Alert on inferences"
title: "Alert on inferences"
weight: 60
layout: "docs"
type: "docs"
description: "Use triggers to send email notifications when inferences are made."
---

At this point, you should have already set up and tested [computer vision functionality](/data-ai/ai/run-inference/).
On this page, you'll learn how to use triggers to send alerts in the form of email notifications or webhook requests when certain detections or classifications are made.

You will build a system that can monitor camera feeds and detect situations that require review.
In other words, this system performs anomaly detection.
Whenever the system detects an anomaly, it will send an email notification.

First, you'll set up data capture and sync to record images with the anomaly and upload them to the cloud.
Next, you'll configure a trigger to send email notifications or webhook requests when the anomaly is detected.

### Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "A configured camera and vision service. Click to see instructions." >}}

Follow the instructions to [configure a camera](/operate/reference/components/camera/) and [run inference](/data-ai/ai/run-inference/).

{{< /expand >}}

## Configure a filtered camera

Your physical camera is working and your vision service is set up.
Now you will pull them together to filter out only images where an inference is made with the [`filtered-camera`](https://app.viam.com/module/erh/filtered-camera) {{< glossary_tooltip term_id="module" text="module" >}}.
This camera module takes the vision service and applies it to your webcam feed, filtering the output so that later, when you configure data management, you can save only the images that contain people without hard hats rather than all images the camera captures.

Configure the camera module with classification or object labels according to the labels your ML model provides that you want to alert on.
Follow the instructions in the [`filtered-camera` module readme](https://github.com/erh/filtered_camera).
For example, if using the YOLOv8 model (named `yolo`) for hardhat detection, you would configure the module like the following:

{{% expand "Instructions for configuring the filtered-camera module to detect people without a hardhat" %}}

1. Navigate to your machine's **CONFIGURE** tab.

2. Click the **+** (Create) button next to your main part in the left-hand menu and select **Component**.
   Start typing `filtered-camera` and select **camera / filtered-camera** from the results.
   Click **Add module**.

3. Name your filtering camera something like `objectfilter-cam` and click **Create**.

4. Paste the following into the attributes field:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "camera": "my_webcam",
     "vision": "yolo",
     "window_seconds": 3,
     "objects": {
       "NO-Hardhat": 0.5
     }
   }
   ```

   If you named your detector something other than "yolo," edit the `vision_services` value accordingly.
   You can also edit the confidence threshold.
   If you change it to `0.6` for example, the `filtered-camera` camera will only return labeled bounding boxes when the vision model indicates at least 60% confidence that the object is a hard hat or a person without a hard hat.

5. Click **Save** in the top right corner of the screen to save your changes.

{{% /expand%}}

## Configure data capture and sync

Viam's built-in [data management service](/services/data/) allows you to, among other things, capture images and sync them to the cloud.

Configure data capture on the `filtered-camera` camera to capture images of detections or classifications:

1. First, you need to add the data management service to your machine to make it available to capture data on your camera.

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

You can use the **Data has been synced to the cloud** trigger to send alerts whenever an image with an anomaly detection is synced to the cloud from your object filter camera.

You can set up the trigger with a serverless function which sends you a customized email or with Viam's built-in email alerts which sends a generic email letting you know that data has been synced.

If you wish to use Viam's built-in email alerts, skip ahead to [Configure a trigger on your machine](#configure-a-trigger-on-your-machine).
To set up a serverless function, continue reading.

### Create a serverless function

Before you configure a trigger on your machine, you need to create a serverless function for the trigger to call.
A serverless function is a simple script that is hosted by a service such as [Google Cloud Functions](https://cloud.google.com/functions) or [AWS Lambda](https://aws.amazon.com/pm/lambda).
You don't need to host it on your machine; instead, it is always available and runs only when an event triggers it.

#### Set up your cloud function scaffold

You can use Google Cloud Functions and write your function in Python.
If you are new to cloud functions, you may find [this getting started guide](https://cloud.google.com/functions/docs/console-quickstart) useful.

1. Create a Google Cloud (GCP) account.
2. Create a project, then search for **Cloud Functions** in the Google Cloud console search bar.
3. Click **CREATE FUNCTION**.
4. Choose `1st gen` as the **Environment**.
5. Give your function a name.
6. Choose your region.
7. For trigger type, choose `HTTP`.
8. Click **NEXT**.
9. For **Runtime**, choose `Python 3.8`.
10. Click **Deploy**.
    The demo function won't do anything exciting yet; keep going through the next few sections before testing it.

#### Configure email credentials

To write a function that sends an email, you need a service that can send emails.
You can use [SendGrid](https://sendgrid.com) (which has a free tier) to make configuration of your email notifications simpler.
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

   {{<imgproc src="/tutorials/helmet/email-received.png" resize="x600" declaredimensions=true alt="The email, opened in a web email client." style="width: 400px" >}}

   If you don't see an email, check your spam folder.
   If you still don't see an email, make sure your SendGrid account is fully set up (2FA enabled, email confirmed) and that your email API key is [correctly configured](#configure-email-credentials).

### Configure a trigger on your machine

Now it's time to configure a trigger so that you get an email when a person is not wearing a hard hat.

Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
Click the **+** (Create) button in the left side menu and select **Trigger**.

Name the trigger and click **Create**.

Select trigger **Type** as **Data has been synced to the cloud** and **Data Types** as **Binary (image)**.

{{<imgproc src="/tutorials/helmet/trigger.png" resize="x300" declaredimensions=true alt="The trigger created with data has been synced to the cloud as the type and binary (image) as the data type." >}}

To configure notifications, either

- add a webhook and enter the URL of your custom cloud function, if you created one
- add an email address to use Viam's built-in email notifications

For both options also configure the time between notifications.

Click **Save** in the top right corner of the screen to save your changes.

## Test the whole system

You've built all the pieces of the system and connected them together.
Now it's time to test the whole thing.

Make sure `viam-server` is running on your machine.
Run your camera in front of what you're detecting and wait for an anomaly to appear.
Wait a couple of minutes for the email to arrive in your inbox.
Congratulations, you've successfully built your anomaly detection monitor!

## Troubleshooting

### Test the vision service

To see the detections or classifications occurring in real time and verify if their confidence level reaches the threshold you have set, you can navigate to the vision service card and expand the **TEST** panel.
