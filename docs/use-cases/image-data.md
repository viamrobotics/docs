---
title: "Capture and sync image data"
linkTitle: "Capture and sync image data"
weight: 20
type: "docs"
description: "Capture image data from a camera on your machine and sync that data to the cloud."
---

You can use the data management service to capture images from a camera on your machine and sync those images to the cloud.
Once you have synced your images, you can view them in the Viam app, filter your images using common search criteria, or export them to other machines.

For example, you might add the data management service to multiple machines to be able to sync captured images from each of them to the Viam app so that you can search across all images from one interface.

<table>
  <tr>
    <th>{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
      <b>1. Configure a camera</b><br><br>
      <p>First, <a href="/fleet/machines/#add-a-new-robot">create a robot</a> if you haven't yet.</p>
      <p>Then <a href="/build/configure/components/camera/">add a camera component</a>, such as a <a href="/build/configure/components/camera/webcam/">webcam</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
      <b>2. Configure the data management service</b><br><br>
      <p>Next, <a href="/data/">add the data management service</a> to be able to configure how your camera captures and stores images.</p>
      <p>Then configure <a href="/data/capture/">data capture</a> and <a href="/data/cloud-sync/">cloud sync</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
      <b>3. Capture data</b><br><br>
      <p>With data management configured, <a href="/data/capture/#configure-data-capture-for-individual-components">capture image data from a camera on your machine</a>. Captured data is automatically synced to the cloud after a short delay.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
      <b>4. View data in the Viam app</b><br><br>
      <p>Once you have synced images, you can <a href="/data/view/">view those images in the Viam app</a> from the <b>Data</b> tab.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
      <b>5. Filter data by common search criteria</b><br><br>
      <p>You can <a href="/data/view/#filter-data">filter synced images in the Viam app</a> using the **Filtering** menu under the <b>Data</b> tab in the Viam app, using search criteria such as robot name, location, date range, or component name.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
      <b>6. Export data</b><br><br>
      <p>You can also <a href ="/data/export/">export your data from the Viam app to a deployed machine, or to any computer.</p>
    </th>
  </tr>
</table>

## Next steps

{{< cards >}}
{{% card link="/data/query/" %}}
{{% card link="/ml/" %}}
{{% card link="/tutorials/" %}}
{{< /cards >}}
