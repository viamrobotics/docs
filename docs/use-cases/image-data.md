---
title: "Capture and sync image data"
linkTitle: "Capture and sync image data"
weight: 20
type: "docs"
images: ["/app/ml/collect.svg"]
description: "Capture image data from a camera on your machine and sync that data to the cloud."
---

You can use the data management service to capture images from a camera on your machine and sync those images to the cloud.
Once you have synced your images, you can view them in the Viam app, filter your images using common search criteria, or export them to other machines.

For example, you might add the data management service to multiple machines to be able to sync captured images from each of them to the Viam app so that you can search across all images from one interface.

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
**1. Configure a camera**

First, [create a machine](/app/fleet/machines/#add-a-new-machine) if you haven't yet.

Then [add a camera component](/machine/components/camera/), such as a [webcam](/machine/components/camera/webcam/).

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/machine/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**2. Configure the data management service**

Next, [add the data management service](/app/data/) to be able to configure how your camera captures and stores images.

Then configure [data capture](/app/data/capture/) and [cloud sync](/app/data/cloud-sync/).

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/machine/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
**3. Capture data**

With data management configured, [capture image data from a camera on your machine](/app/data/capture/#configure-data-capture-for-individual-components). Captured data is automatically synced to the cloud after a short delay.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**4. View data in the Viam app**

Once you have synced images, you can [view those images in the Viam app](/app/data/view/) from the **Data** tab.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/app/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**5. Filter data by common search criteria**

You can [filter synced images in the Viam app](/app/data/view/#filter-data) using the **Filters** menu under the **Data** tab in the Viam app, using search criteria such as machine name, location, date range, or component name.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/machine/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**6. Export data**

You can also [export your data from the Viam app](/app/data/export/) to a deployed machine, or to any computer.

{{< /tablestep >}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/app/data/query/" %}}
{{% card link="/app/ml/" %}}
{{% card link="/tutorials/" %}}
{{< /cards >}}
