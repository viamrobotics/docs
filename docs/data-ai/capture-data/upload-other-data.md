---
linkTitle: "Upload data"
title: "Upload data to Viam"
images: ["/services/icons/data-folder.svg"]
weight: 60
layout: "docs"
type: "docs"
languages: ["python"]
viamresources: ["data_manager"]
aliases:
  - /data/upload/
  - /services/data/upload/
  - /how-tos/upload-data/
  - /data-ai/ai/advanced/upload-external-data/
  - /data-ai/ai/advanced/
  - /data-ai/train/upload-external-data/
date: "2024-12-04"
updated: "2025-09-11"
description: "Upload data to Viam from your local computer or mobile device using the data client API, Viam CLI, or Viam mobile app."
---

When you configure the data management service, Viam automatically uploads data from the default directory `~/.viam/capture` and any directory you configured.
If you want to upload data from another directory or source, you can also:

- [Sync a batch of data from another directory](#sync-data-from-another-directory)
- [Upload data with SDKs](#upload-data-with-sdks)
- [Upload images with the Viam mobile app](#upload-images-with-the-viam-mobile-app)

## Sync data from another directory

Typically, you configure the data management service to [capture and sync data from your machine at regular intervals](/data-ai/capture-data/capture-sync/).
However, you can also use the data management service to sync data from a folder.
This can be a dataset you wish to upload once or data that is periodically written to a folder on your system.

### Prerequisites

{{% expand "A running machine connected to Viam" %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

### Instructions

{{% alert title="Data will be removed from the device once uploaded to Viam" color="caution" %}}

If you do not want the data deleted from your machine, copy the data to a new folder and sync that folder instead so that your local copy remains.

{{% /alert %}}

{{< table >}}
{{% tablestep start=1 %}}
**Add the data management service**

On your machine's **CONFIGURE** tab, click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.

Select the `data management` service and click **Create**.
On the data management panel, you can see the configuration options.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.

{{% /tablestep %}}
{{% tablestep %}}
**Configure sync from the additional folder**

In the **Additional paths**, enter the full path to the directory with the data you want to upload, for example, `/Users/Artoo/my_cat_photos`.
All of the data in the folder will be synced, so be sure that you want to upload all of the contents of the folder before saving your configuration.

Toggle **Syncing** to on (green) if it isn't already on.

Click **Save** in the top right corner of the page.

{{<imgproc src="/services/data/data-sync-temp.png" resize="x1100" declaredimensions=true alt="Data service configured as described." style="width: 600px" class="shadow imgzoom" >}}

{{% /tablestep %}}
{{% tablestep %}}
**Confirm that your data uploaded**

Navigate to your [**DATA** page](https://app.viam.com/data/view) and confirm that your data appears there.
If you don't see your files yet, wait a few moments and refresh the page.

{{% /tablestep %}}
{{< /table >}}

## Upload data with SDKs

You can use the [Data Client API](/dev/reference/apis/data-client/) to upload files to the Viam Cloud.

Unlike when using the data management service, using the [`FileUploadFromPath`](/dev/reference/apis/data-client/#fileuploadfrompath) method uploads the files even if they already exist in the cloud.
In other words, it duplicates data if you run it multiple times.

Also unlike data sync, this method _does not_ delete data from your device.

### Instructions

{{< table >}}
{{% tablestep start=1 %}}
**Get API key**

Go to your organization's setting page and create an API key for a {{< glossary_tooltip term_id="part" text="machine part" >}}, {{< glossary_tooltip term_id="part" text="machine" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="organization" text="organization" >}}.

{{% /tablestep %}}
{{% tablestep %}}
**Upload a file from a path**

Use the [`FileUploadFromPath`](/dev/reference/apis/data-client/#fileuploadfrompath) method to upload a file.

You must provide a {{< glossary_tooltip term_id="part" text="machine part" >}} ID to associate data with.

{{< tabs >}}
{{< tab name="Python" >}}

To upload just one file, make a call to [`file_upload_from_path`](/dev/reference/apis/data-client/#fileuploadfrompath):

{{< read-code-snippet file="/static/include/examples-generated/upload-single-file.snippet.upload-single-file.py" lang="py" class="line-numbers linkable-line-numbers" data-line="31-38" >}}

{{% /tab %}}
{{< tab name="Go" >}}

{{< read-code-snippet file="/static/include/examples-generated/upload-single-file.snippet.upload-single-file.go" lang="go" class="line-numbers linkable-line-numbers" data-line="33-40" >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Run your code**

Save and run your code once.
Running your code more than once will duplicate the data.

{{% /tablestep %}}
{{% tablestep %}}
**Confirm that your data uploaded**

Navigate to your [**DATA** page](https://app.viam.com/data/view) and confirm that your data appears there.

{{% /tablestep %}}
{{< /table >}}

## Upload images with the Viam mobile app

Upload images as machine data straight from your phone, skipping the normal data capture and cloud synchronization process, through the [Viam mobile app](/manage/troubleshoot/teleoperate/default-interface/#viam-mobile-app).
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
{{% tablestep start=1 %}}
**Navigate to your machine**

In the Viam mobile app, select an organization by clicking on the menu icon in the top left corner.

Tap the **Locations** tab and select a location, then select the machine you want your data to be associated with.

{{% /tablestep %}}
{{% tablestep %}}
**Upload images**

Tap the menu button marked "**...**" in the upper right corner.
Tap **Upload Images**.

Select each image you want to upload, then tap **Add**.

The uploaded images metadata will contain the machine part you selected.
However, the uploaded images will not be associated with a component or method.

{{% /tablestep %}}
{{< /table >}}

## Next steps

If you uploaded a dataset for machine learning, continue to [create a dataset](/data-ai/train/create-dataset/).
