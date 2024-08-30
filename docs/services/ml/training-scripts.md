---
title: "Custom training scripts"
linkTitle: "Training scripts"
weight: 10
type: "docs"
description: "The Viam registry hosts custom Python ML training scripts, which you can use to train machine learning models."
no_list: true
icon: true
images: ["/services/icons/ml.svg"]
modulescript: true
---

The Viam registry hosts custom Python ML training scripts, which you can use to train machine learning models.
You can upload your own training script by following the guide to [Train a Model with a Custom Python Training Script](/how-tos/create-custom-training-scripts/).

You can search the available ML training scripts from the Viam registry here:

<div id="searchboxScripts"></div>
<p>
<div id="searchstatsScripts"></div></p>
<div class="training-scripts" id="">
  <div class="modellistheader">
    <div class="name">Script</div>
    <div>Description</div>
  </div>
<div id="hitsScripts" class="modellist">
</div>
<div id="paginationScripts"></div>
</div>
<noscript>
    <div class="alert alert-caution" role="alert">
        <h4 class="alert-heading">Javascript</h4>
        <p>Please enable javascript to see and search ML custom training scripts.</p>
    </div>
</noscript>

## API

To submit training jobs programmatically, use the [ML Training client API](/appendix/apis/ml-training-client/), which supports the following methods:

{{< readfile "/static/include/app/apis/generated/mltraining-table.md" >}}

## Next steps

Follow one of these guides to write your own custom training script or to train models with training scripts:

{{< cards >}}
{{% card link="/how-tos/create-custom-training-scripts/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< /cards >}}
