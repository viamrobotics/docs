---
title: "Capture and sync image data"
linkTitle: "Capture and sync image data"
weight: 20
type: "docs"
description: "Capture image data from a camera on your machine and sync that data to the cloud."
---

You can use the data management service to capture images from a connected camera on your machine and sync those images to the cloud.
Once you have synced your images, you can view them in the Viam app, filter your images using common search criteria, or export them to other machines.

For example, you might configure data capture for a camera on your machine and sync captured images to the Viam app, to be able to view them from anywhere.

<table>
  <tr>
    <th>{{<imgproc src="/icons/components/camera.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
      <b>1. Configure a camera</b><br><br>
      <p>First, <a href="/manage/fleet/machines/#add-a-new-robot">create a robot</a> if you haven't yet.</p>
      <p>Then, <a href="/build/configure/components/camera/">add a camera component</a>, such as a <a href="/build/configure/components/camera/webcam/">webcam</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/build/configure/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
      <b>2. Configure the data management service</b><br><br>
      <p>Then, add the <a href="/data/">data management service</a>, and configure <a href="/data/capture/">data capture</a> and <a href="/data/cloud-sync/">cloud sync</a>.</p>
      <p>Add the <a href="/data/">data management service</a> to your machine, to be able to configure how your camera captures and stores images. then configure <a href="/data/capture/">data capture</a> and <a href="/data/cloud-sync/">cloud sync</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/icons/components/sensor.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Collect data">}}
      <b>2. Capture data</b><br><br>
      <p>Then, <a href="/data/capture/#configure-data-capture-for-individual-components">capture tabular data from a component on your machine</a>, such as a sensor. Captured data is automatically synced to the cloud after a short delay.
      <br><br>You can <a href="/data/view/">view your data in the Viam app</a> from the <b>Data</b> tab.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/build/configure/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
      <b>3. View data in the Viam app</b><br><br>
      <p>You can <a href="/data/view/">view your data in the Viam app</a> from the <b>Data</b> tab.
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/build/configure/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
      <b>4. Filter data by common search criteria</b><br><br>
      <p>If you prefer, you can also <a href ="/data/query/#query-tabular-data-directly-from-a-compatible-client">query your directly from an MQL-compatible client</a>, such as <code>mongosh</code> or MongoDB Compass, using SQL or MQL.</p></p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/build/configure/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
      <b>5. Export data</b><br><br>
      <p>If you prefer, you can also <a href ="/data/query/#query-tabular-data-directly-from-a-compatible-client">query your directly from an MQL-compatible client</a>, such as <code>mongosh</code> or MongoDB Compass, using SQL or MQL.</p></p>
    </th>
  </tr>
</table>

## Next steps

{{< cards >}}
{{% card link="/data/query/" %}}
{{% card link="/ml/" %}}
{{% card link="/tutorials/" %}}
{{< /cards >}}
