---
title: "Configure a Fake Camera (Micro-RDK)"
linkTitle: "fake (Micro-RDK)"
weight: 20
type: "docs"
description: Configure a camera to use for testing."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - /components/camera/fake-micro-server/
component_description: "A camera model for testing."
micrordk_component: true
toc_hide: true
# SMEs: Matt Perez, Micro-RDK team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a circle inside a diamond.

{{< alert title="Software requirements" color="note" >}}
To use this model, you must follow the [Set up an ESP32 guide](/operate/install/setup-micro/#build-and-flash-custom-firmware), which enables you to install and activate the ESP-IDF.
When you create a new project with `cargo generate`, select the option to include camera module traits when prompted.
Finish building and flashing custom firmware, then return to this guide.
{{< /alert >}}

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `fake` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of a fake camera.](/components/camera/configure-fake.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "fake",
  "api": "rdk:component:camera",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

## View the camera stream

Once your camera is configured, expand the **TEST** section on the configuration pane.
You will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

{{< imgproc src="/components/camera/fake-micro-server-view.png" alt="Fake Camera Micro Server View" resize="400x" class="shadow"  >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/camera.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}
