---
linkTitle: "AI and Data"
title: "Work with Data and AI"
weight: 250
layout: "docs"
type: "docs"
no_list: true
noedit: true
open_on_desktop: true
overview: true
notoc: true
description: "Sync and store sensor data, images, and any other binary or timeseries data. Then use ML and AI to turn your data into insights and action."
---

Viam's data and AI capabilities enable you to capture and sync or upload data, build a dataset, train and deploy ML models, and run inference with computer vision.
Then, you can act or alert on inferences.
You can also monitor your machines through teleop, power your application logic, or analyze historical data trends.

<div class="img-overlay-wrap aligncenter">
  <img src="../platform/platform-all.svg" alt="Platform diagram" id="fleet-platform-all" class="aligncenter overview" style="width:800px;height:auto">
  <img src="../platform/platform-data-capture.svg" alt="Platform diagram with data capture elements highlighted" class="aligncenter overlay" id="data-platform-capture" style="width:800px;height:auto" loading="lazy" >
  <img src="../platform/platform-data-work.svg" alt="Platform diagram with data usage elements highlighted" class="aligncenter overlay" id="data-platform-work" style="width:800px;height:auto" loading="lazy" >
  <img src="../platform/platform-data-ai.svg" alt="Platform diagram with AI elements highlighted" class="aligncenter overlay" id="data-platform-ai" style="width:800px;height:auto" loading="lazy" >
</div>

<div class="hoveraction">

{{< how-to-expand "Get started" "4" "BEGINNER-FRIENDLY" "" "data-platform-capture" >}}
{{< cards >}}
{{% card link="/data-ai/get-started/quickstart/" noimage="true" %}}
{{% card link="/data-ai/get-started/capture-images/" noimage="true" %}}
{{% card link="/data-ai/get-started/create-training-dataset/" noimage="true" %}}
{{% card link="/data-ai/get-started/annotate-images/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Process data" "7" "INTERMEDIATE" "" "data-platform-work" >}}
{{< cards >}}
{{% card link="/data-ai/edge/capture-sync/" noimage="true" %}}
{{% card link="/data-ai/edge/filter-before-sync/" noimage="true" %}}
{{% card link="/data-ai/edge/conditional-sync/" noimage="true" %}}
{{% card link="/data-ai/cloud/query/" noimage="true" %}}
{{% card link="/data-ai/cloud/visualize/" noimage="true" %}}
{{% card link="/data-ai/react/alert-data/" noimage="true" %}}
{{% card link="/data-ai/cloud/export/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Integrate AI" "8" "INTERMEDIATE" "" "data-platform-ai" >}}
{{< cards >}}
{{% card link="/data-ai/train/train-tflite/" noimage="true" %}}
{{% card link="/data-ai/train/train/" noimage="true" %}}
{{% card link="/data-ai/train/deploy/" noimage="true" %}}
{{% card link="/data-ai/infer/run-inference/" noimage="true" %}}
{{% card link="/data-ai/react/alert/" noimage="true" %}}
{{% card link="/data-ai/react/act/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

</div>
