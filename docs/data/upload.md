---
title: "Upload a Batch of Data"
linkTitle: "Upload Data"
description: "Upload data to the Viam app from your local computer or mobile device using the data client API, Viam CLI, or Viam mobile app."
weight: 40
type: "docs"
tags: ["data management", "cloud", "sync"]
image: "/services/icons/data-capture.svg"
imageAlt: "Upload data to the Viam app"
images: ["/services/icons/data-capture.svg"]
# SME: Alexa Greenberg
---

If you configured [data capture](/data/capture/) on your machine, data is automatically uploaded to the Viam cloud from the directory and at the interval you specified.
However, if you want to upload a batch of data once from somewhere else, either from a different place on your machine or from your personal computer or mobile device, you have several options:

- Configure the path to your directory in the Viam app, wait for the files to sync, then delete the path.
  This option requires that you have `viam-server` installed on the machine.
- Run a Python script to upload files from a folder using the data client API `file_upload_from_path` method.
  You can do this on a computer that doesn't have `viam-server` installed on it.
- Upload images from your mobile device using the Viam mobile app.

## Sync a batch of data from another directory

{{% alert title="Note" color="note" %}}

This method of uploading data will delete the data from your machine once it is uploaded to the cloud.

If you do not want the data deleted from your machine, copy the data to a new folder and sync that folder instead so that your local copy remains.

{{% /alert %}}

Typically, you configure the data service to sync data from your machine at regular intervals indefinitely.
However, if you already have a cache of data you'd like to use with Viam, you can temporarily modify your configuration to sync a batch of data and then revert your config changes after the data is uploaded.
The following steps assume you already have a machine with [`viam-server` installed and connected to the Viam app](/get-started/installation/):

1. Put the data you want to sync in a directory on your machine.
   All of the data in the folder will be synced, so be sure that you want to upload all of the contents of the folder.
2. If you haven't already, [add the data management service to your machine's config.](/data/capture/#add-the-data-management-service)
3. Navigate to your data management card within the **Services** subtab of your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com).
4. Next to **Additional paths**, click **Add pathway**.
   Enter the full path to the directory where the data you want to upload is stored, for example, `/Users/Artoo/my_cat_photos`.
5. Toggle **Syncing** to on (green).

   {{<imgproc src="/data/data-sync-temp.png" resize="x1100" declaredimensions=true alt="Data service configured in the Viam app as described." >}}

6. Click the **Save** button in the top right corner of the page.
7. Navigate to your [**DATA** page in the Viam app](https://app.viam.com/data/view) and confirm that your data appears there.
   If you don't see your files yet, wait a few moments and refresh the page.
8. Once the data has uploaded, navigate back to your data service config.
   You can now delete the additional path you added.
   You can also turn off **Syncing** unless you have other directories you'd like to continue to sync from.

## Upload data with Python

You can use the Viam Python SDK's data client API [`file_upload_from_path`](/build/program/apis/data-client/#fileuploadfrompath) method to upload one or more files from your computer to the Viam cloud.

{{% alert title="Note" color="note" %}}

Unlike data sync, using the `file_upload_from_path` API method uploads all the data even if that data already exists in the cloud.
In other words, it duplicates data if you run it multiple times.

Also unlike data sync, this method _does not_ delete data from your device.

{{% /alert %}}

1. Install the [Viam Python SDK](https://python.viam.dev/) by running the following command on the computer from which you want to upload data:

   ```sh {class="command-line" data-prompt="$"}
   pip install viam-sdk
   ```

2. Create a Python script file in a directory of your choice and [add code to establish a connection](/build/program/apis/data-client/#establish-a-connection) from your computer to your [Viam app](https://app.viam.com) {{< glossary_tooltip term_id="location" text="location" >}} or individual {{< glossary_tooltip term_id="part" text="machine part" >}}.

3. Use the `file_upload_from_path` method to upload your data, depending on whether you are uploading one or multiple files:

   - To upload just one file, make a call to `file_upload_from_path` according to [the data client API documentation](/build/program/apis/data-client/#fileuploadfrompath).
     The following example code could be placed inside the `main()` function (or a function called from `main()`):

     ```python {class="line-numbers linkable-line-numbers"}
     await data_client.file_upload_from_path(
       # The ID of the machine part the file should be associated with
       part_id="abcdefg-1234-abcd-5678-987654321xyzabc",
       # Any tags you want to apply to this file
       tags=["cat", "animals", "brown"],
       # Path to the file
       filepath="/Users/Artoo/my_cat_photos/brown-cat-on-a-couch.png"
     )
     ```

   - To upload all the files in a directory, you can use the same [`file_upload_from_path`](/build/program/apis/data-client/#fileuploadfrompath) method inside a `for` loop, for example:

     ```python {class="line-numbers linkable-line-numbers"}
     import os # Add this package at the top of your program
                      # with your other imports

     my_data_directory = "/Users/Artoo/my_cat_photos"

     for file_name in os.listdir(my_data_directory):
       await data_client.file_upload_from_path(
         part_id="abcdefg-1234-abcd-5678-987654321xyzabc",
         tags=["cat", "animals", "brown"],
         filepath=os.path.join(my_data_directory, file_name)
       )
     ```

4. Save and run your code once.
   Running your code more than once will duplicate the data.
   View your uploaded data in your [**DATA** page in the Viam app](https://app.viam.com/data/view).

## Upload images with the Viam mobile app

Upload images as machine data straight from your phone, skipping the normal data capture and cloud synchronization process, through the [Viam mobile app](/fleet/#the-viam-mobile-app).
This is useful if you want to capture images for training machine learning models on the go.

1. Select an organization clicking on the menu icon in the top left corner and tapping an organization.
2. Tap the **Locations** tab and tap on a location and then on a machine.
3. Click the menu button marked "**...**" in the upper right corner.
4. Click **Upload Images**.
5. Select each image you want to upload, and click **Add**.

The uploaded images metadata will contain the machine part you selected.
However, the uploaded images will not be associated with a component or method.
