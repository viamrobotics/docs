---
title: "Upload Data"
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
However, if you want to upload a batch of data manually from somewhere else either on your machine, or from your personal computer or mobile device, you have several options:

- Run a Python script to upload files from a folder using the data client API `file_upload_from_path` method.
- Run a Golang script calling the data management service `sync` method.
- Upload images from your mobile device using the Viam mobile app.

## Upload data with a Python script

You can use the Viam Python SDK's data client API [`file_upload_from_path`](/build/program/apis/data-client/#fileuploadfrompath) method to upload each file you'd like to upload from your computer to the Viam cloud.

1. Install the [Viam Python SDK](https://python.viam.dev/) by running the following command on the computer from which you want to upload data:

   ```sh {class="command-line" data-prompt="$"}
   pip-install viam-sdk
   ```

2. Create a Python script file in a directory of your choice and [add code to establish a connection](/build/program/apis/data-client/#establish-a-connection) from your computer to your [Viam app](https://app.viam.com) {{< glossary_tooltip term_id="location" text="location" >}} or individual {{< glossary_tooltip term_id="part" text="machine part" >}}.

3. To upload just one file, make a call to the `file_upload_from_path` method according to [the data client API documentation](/build/program/apis/data-client/#fileuploadfrompath).
   The following example code could be placed inside the `main()` function (or a function called from `main()`):

   ```python {class="line-numbers linkable-line-numbers"}
   await data_client.file_upload_from_path(
     part_id="abcdefg-1234-abcd-5678-987654321xyzabc",
     tags=["cat", "animals", "brown"],
     filepath="/Users/Artoo/my_cat_photos/brown-cat-on-a-couch.jpeg"
   )
   ```

   To upload all the files in a directory, you can use the same [`file_upload_from_path`](/build/program/apis/data-client/#fileuploadfrompath) method inside a `for` loop, for example:

   ```python {class="line-numbers linkable-line-numbers"}
   import os # Add this package up at the top with your other imports

   my_data_directory = "/Users/Artoo/my_cat_photos"

   for file_name in os.listdir(my_data_directory):
     await data_client.file_upload_from_path(
       part_id="abcdefg-1234-abcd-5678-987654321xyzabc",
       tags=["cat", "animals", "brown"],
       filepath=os.path.join(my_data_directory, file_name)
     )
   ```

4. Save and run your code.
   View your uploaded data in your [**DATA** page in the Viam app](https://app.viam.com/data/view).

## Sync data with the `sync` method

The Viam Golang SDK includes a data service API with a [`sync`](/data/#sync) method that syncs all the data from your machine to the cloud.
The [cloud sync tools](/data/cloud-sync/) sync data automatically according to how you configure cloud sync, but if you prefer to sync programatically, you can instead run a script that calls the `sync` method.

The following steps assume you already have a [data capture service configured](/data/capture/#add-the-data-management-service).
If you want to use the `sync` API method as the only way to sync data, you should toggle sync off in your data service config (`"sync_disabled": true` in raw JSON).

1. Install the [Viam Go SDK](https://github.com/viamrobotics/rdk/tree/main/robot/client).

2. Create a Go script file in a directory of your choice.
   Go to your machine's **Code sample** tab in the [Viam app](https://app.viam.com) and click **Golang**.
   Copy the code from that tab into your script file to establish a connection from your computer to your machine's instance in the Viam app.

3. Add the required import to the list of imports at the top of your script:

   ```go {class="line-numbers linkable-line-numbers"}
   import (
     "go.viam.com/rdk/services/datamanager"
   )
   ```

4. In your `main()` function (or in a function called from `main`), call [the `sync` method as documented](/data/#sync).
   For example:

   ```go {class="line-numbers linkable-line-numbers"}
   // Get the data management service from your machine
   // Use the name of the data service you configured on your machine in place of "my_data_service"
   data, err := datamanager.FromRobot(robot, "my_data_service")

   // Sync data stored on the machine to the cloud.
   err := data.Sync(context.Background(), nil)
   ```

5. Save, compile, and run your code.
   View your uploaded data in your [**DATA** page in the Viam app](https://app.viam.com/data/view).

## Upload images with the Viam mobile app

Upload images as machine data straight from your phone, skipping the normal data capture and cloud synchronization process, through the [Viam mobile app](/fleet/#the-viam-mobile-app).
This is useful if you want to capture images for training machine learning models on the go.

1. Select **Home** on the mobile app, choose your organization, and select a location and machine.
2. Click the menu button marked "**...**" in the upper right corner.
3. Click **Upload Images**.
4. Select each image you want to upload, and click **Add**.

With regard to metadata, these images are associated with the machine part you selected, and aren't associated with a component or method.
