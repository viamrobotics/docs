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
However, if you want to upload a batch of data manually from somewhere else either on your machine or on your personal computer or mobile device, you have several options:

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

3. If you want to upload just one file:

   If you want to upload all the files in a folder:

## Sync data with the `sync` method

The Viam Golang SDK includes a data service API with a [`sync`](/data/#sync) method.

## Upload images with the Viam mobile app

Upload images as machine data straight from your phone, skipping the normal data capture and cloud synchronization process, through the [Viam mobile app](/fleet/#the-viam-mobile-app).
This is useful if you want to capture images for training machine learning models on the go.

1. Select **Home** on the mobile app, choose your organization, and select a location and machine.
2. Click the menu button marked "**...**" in the upper right corner.
3. Click **Upload Images**.
4. Select each image you want to upload, and click **Add**.

With regard to metadata, these images are associated with the machine part you selected, and aren't associated with a component or method.
