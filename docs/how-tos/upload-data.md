---
title: "Upload a batch of data"
linkTitle: "Upload a batch of data"
description: "Upload data to the Viam app from your local computer or mobile device using the data client API, Viam CLI, or Viam mobile app."
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: true
languages: ["python"]
viamresources: ["data_manager"]
platformarea: ["data"]
level: "Beginner"
date: "2024-09-05"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
images: ["/services/icons/data-folder.svg"]
aliases:
  - /data/upload/
  - /services/data/upload/
---

If you configured the [data management service](/services/data/), Viam automatically uploads data from the configured directory to the cloud, at the interval you specified.
However, if you want to upload a batch of data once from somewhere else, either from a different directory on your machine or from your personal computer or mobile device, you have several options using the Viam app, the data client API, or the Viam mobile app.

{{% alert title="In this page" color="tip" %}}

- [Sync a batch of data from another directory](#sync-a-batch-of-data-from-another-directory) by configuring the path to the directory as an additional sync path in a machine's data management service.
  This requires the data to be on a machine running `viam-server`.
- [Upload data with the Python SDK](#upload-data-with-python) by running a Python script to upload files from a folder.
  You can do this on a computer that doesn't have `viam-server` installed on it.
- [Upload images with the Viam mobile app](#upload-images-with-the-viam-mobile-app) from your mobile device.

{{% /alert %}}

## Sync a batch of data from another directory

Typically, you configure the data service to sync data from your machine at regular intervals indefinitely.
However, if you already have a cache of data you'd like to use with Viam, you can temporarily modify your configuration to sync a batch of data and then revert your config changes after the data is uploaded.

### Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

{{< expand "Enable data capture and sync on your machine." >}}

Add the [data management service](/services/data/):

On your machine's **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.

{{< /expand >}}

### Instructions

{{% alert title="Note" color="note" %}}

This method of uploading data will delete the data from your machine once it is uploaded to the cloud.

If you do not want the data deleted from your machine, copy the data to a new folder and sync that folder instead so that your local copy remains.

{{% /alert %}}

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/services/icons/data-folder.svg" class="fill alignleft" style="width: 120px" declaredimensions=true alt="Folder" >}}
**1. Organize your data**

Put the data you want to sync in a directory on your machine.
All of the data in the folder will be synced, so be sure that you want to upload all of the contents of the folder.

{{% /tablestep %}}
{{% tablestep %}}
**2. Configure sync from the additional folder**

In the **Additional paths**, enter the full path to the directory where the data you want to upload is stored, for example, `/Users/Artoo/my_cat_photos`.

Toggle **Syncing** to on (green) if it isn't already on.

{{<imgproc src="/services/data/data-sync-temp.png" resize="x1100" declaredimensions=true alt="Data service configured in the Viam app as described." >}}

Click **Save** in the top right corner of the page.

{{% /tablestep %}}
{{% tablestep %}}
**3. Confirm that your data uploaded**

Navigate to your [**DATA** page in the Viam app](https://app.viam.com/data/view) and confirm that your data appears there.
If you don't see your files yet, wait a few moments and refresh the page.

{{% /tablestep %}}
{{% tablestep %}}
**4. Remove the folder path**

Once the data has uploaded, navigate back to your data service config.
You can now delete the additional path you added.
You can also turn off **Syncing** unless you have other directories you'd like to continue to sync from.
{{% /tablestep %}}
{{< /table >}}

## Upload data with Python

You can use the Python data client API [`file_upload_from_path`](/appendix/apis/data-client/#fileuploadfrompath) method to upload one or more files from your computer to the Viam cloud.

{{% alert title="Note" color="note" %}}

Unlike data sync, using the `file_upload_from_path` API method uploads all the data even if that data already exists in the cloud.
In other words, it duplicates data if you run it multiple times.

Also unlike data sync, this method _does not_ delete data from your device.

{{% /alert %}}

### Prerequisites

{{< expand "Install the Viam Python SDK" >}}

Install the [Viam Python SDK](https://python.viam.dev/) by running the following command on the computer from which you want to upload data:

```sh {class="command-line" data-prompt="$"}
pip install viam-sdk
```

{{< /expand >}}

### Instructions

{{< table >}}
{{% tablestep link="/appendix/apis/data-client/#establish-a-connection" %}}
**1. Get API key**

Go to your organization's setting page and create an API key for your individual {{< glossary_tooltip term_id="part" text="machine part" >}}, {{< glossary_tooltip term_id="part" text="machine" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="organization" text="organization" >}}.

{{% /tablestep %}}
{{% tablestep link="/appendix/apis/data-client/" %}}
**2. Add a `file_upload_from_path` API call**

Create a Python script and use the `file_upload_from_path` method to upload your data, depending on whether you are uploading one or multiple files:

{{< tabs >}}
{{< tab name="Upload a single file" >}}

To upload just one file, make a call to [`file_upload_from_path`](/appendix/apis/data-client/#fileuploadfrompath).

{{< expand "Click this to see example code" >}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client
    await data_client.file_upload_from_path(
      # The ID of the machine part the file should be associated with
      part_id="abcdefg-1234-abcd-5678-987654321xyzabc",
      # Any tags you want to apply to this file
      tags=["cat", "animals", "brown"],
      # Path to the file
      filepath="/Users/Artoo/my_cat_photos/brown-cat-on-a-couch.png"
    )

    viam_client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{< /expand >}}

{{% /tab %}}
{{< tab name="Upload all files in a directory" >}}

To upload all the files in a directory, you can use the [`file_upload_from_path`](/appendix/apis/data-client/#fileuploadfrompath) method inside a `for` loop.

{{< expand "Click this to see example code" >}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import os

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client
    # Specify directory from which to upload data
    my_data_directory = "/Users/Artoo/my_cat_photos"

    for file_name in os.listdir(my_data_directory):
        await data_client.file_upload_from_path(
          part_id="abcdefg-1234-abcd-5678-987654321xyzabc",
          tags=["cat", "animals", "brown"],
          filepath=os.path.join(my_data_directory, file_name)
        )

    viam_client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/icons/data-cloud-sync.svg" class="fill alignleft" style="width: 150px" declaredimensions=true alt="Cloud connection">}}
**3. Run your code**

Save and run your code once.
Running your code more than once will duplicate the data.
View your uploaded data in your [**DATA** page in the Viam app](https://app.viam.com/data/view).

{{% /tablestep %}}
{{< /table >}}

## Upload images with the Viam mobile app

Upload images as machine data straight from your phone, skipping the normal data capture and cloud synchronization process, through the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app).
This is useful if you want to capture images for training machine learning models on the go.

### Prerequisites

{{< expand "Download the Viam mobile app and sign into your Viam account" >}}

Install the mobile app from the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) or [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

<a href="https://apps.apple.com/vn/app/viam-robotics/id6451424162" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/a470b65d-1b97-412f-9f97-daf902f2f053" width="200px" alt="apple store icon" class="center-if-small" >
</a>

<a href="https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/6ebd6960-08c5-41d4-81f9-42293fbfdfd4" width="200px" alt="google play store icon" class="center-if-small" >
</a>

{{< /expand >}}

### Instructions

{{< table >}}
{{% tablestep link="/services/data/" %}}
**1. Navigate to your machine**

In the Viam mobile app, select an organization by clicking on the menu icon in the top left corner and tapping an organization.

Tap the **Locations** tab and select a location, then select the machine you want your data to be associated with.

{{% /tablestep %}}
{{% tablestep %}}
**2. Upload images**

Tap the menu button marked "**...**" in the upper right corner.
Tap **Upload Images**.

Select each image you want to upload, then tap **Add**.

The uploaded images metadata will contain the machine part you selected.
However, the uploaded images will not be associated with a component or method.

{{% /tablestep %}}
{{< /table >}}

## Next steps

Now that you have a batch of data uploaded, you can train an ML model on it.
Or, if you want to collect and upload data _not_ in a batch, see Capture and Sync Image Data.

{{< cards >}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/how-tos/image-data/" %}}
{{< /cards >}}
