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

{{< how-to-expand "Capture data" "4" "BEGINNER-FRIENDLY" "" "data-platform-capture" >}}
{{< cards >}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{% card link="/data-ai/capture-data/upload-other-data/" noimage="true" %}}
{{% card link="/data-ai/capture-data/filter-before-sync/" noimage="true" %}}
{{% card link="/data-ai/capture-data/conditional-sync/" noimage="true" %}}
{{% card link="/data-ai/capture-data/lorawan/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Work with data" "4" "BEGINNER-FRIENDLY" "" "data-platform-work" >}}
{{< cards >}}
{{% card link="/data-ai/data/query/" noimage="true" %}}
{{% card link="/data-ai/data/visualize/" noimage="true" %}}
{{% card link="/data-ai/data/alert-data/" noimage="true" %}}
{{% card link="/data-ai/data/export/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Train an ML model" "5" "INTERMEDIATE" "" "data-platform-ai" >}}
{{< cards >}}
{{% card link="/data-ai/train/create-dataset/" noimage="true" %}}
{{% card link="/data-ai/train/capture-annotate-images/" noimage="true" %}}
{{% card link="/data-ai/train/train-tf-tflite/" noimage="true" %}}
{{% card link="/data-ai/train/train/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Infer with ML models" "4" "INTERMEDIATE" "" "data-platform-ai" >}}
{{< cards >}}
{{% card link="/data-ai/ai/deploy/" noimage="true" %}}
{{% card link="/data-ai/ai/run-inference/" noimage="true" %}}
{{% card link="/data-ai/ai/alert/" noimage="true" %}}
{{% card link="/data-ai/ai/act/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

</div>
