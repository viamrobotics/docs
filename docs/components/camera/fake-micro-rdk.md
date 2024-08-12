---
title: "Configure a Fake Camera (Micro-RDK)"
linkTitle: "fake"
weight: 20
type: "docs"
description: Configure a camera to use for testing."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/fake/"
component_description: "A camera model for testing."
micrordk_component: true
# SMEs: Matt Perez, micro-RDK team
---

A `fake` camera in the micro-RDK is a camera model for testing.
The camera always returns the same image, which is an image of a circle and a diamond.

You can optionally specify a height and width.

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `fake` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of a fake camera in the Viam app config builder.](/components/camera/configure-fake.png)

Edit the attributes as applicable to your camera, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "fake",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

## View the camera stream

Once your camera is configured, go to the **CONTROL** tab, and click on the camera's dropdown menu.
Then toggle the camera view to ON.
You will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

{{< imgproc src="/components/camera/fake-view.png" alt="Fake Camera View" resize="600x" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
