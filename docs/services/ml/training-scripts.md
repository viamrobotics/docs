---
title: "Training scripts"
linkTitle: "Training scripts"
weight: 10
type: "docs"
description: "The Viam registry hosts custom Python ML training scripts, which you can use to train machine learning models."
no_list: true
icon: true
images: ["/services/icons/ml.svg"]
modulescript: true
date: "2024-09-03"
# updated: ""  # When the content was last entirely checked
---

The Viam registry hosts custom Python ML training scripts, which you can use to train machine learning models.
You can upload your own training script by following the guide to [Create custom training scripts](/how-tos/create-custom-training-scripts/).

You can search the available ML training scripts from the Viam registry here:

{{<trainingscripts>}}

## API

To submit training jobs programmatically, use the [ML Training client API](/appendix/apis/ml-training-client/), which supports the following methods:

{{< readfile "/static/include/app/apis/generated/mltraining-table.md" >}}

## Next steps

Follow one of these guides to write your own custom training script or to train models with training scripts:

{{< cards >}}
{{% card link="/how-tos/deploy-ml/" %}}
{{% card link="/how-tos/create-custom-training-scripts/" %}}
{{< /cards >}}
