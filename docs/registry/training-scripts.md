---
title: "Training Scripts"
linkTitle: "Training Scripts"
weight: 30
type: "docs"
description: "The Viam registry hosts custom Python ML training scripts, which you can use to train machine learning models."
no_list: true
icon: true
images: ["/services/icons/ml.svg"]
modulescript: true
aliases:
  - /services/ml/training-scripts/
date: "2024-10-20"
# updated: ""  # When the content was last entirely checked
---

The Viam registry hosts custom Python ML training scripts, which you can use to train machine learning models.

{{< alert title="In this page" color="note" >}}
{{% toc %}}
{{< /alert >}}

## Training scripts in the registry

{{<trainingscripts>}}

## API

To submit training jobs programmatically, use the [ML Training client API](/appendix/apis/ml-training-client/), which supports the following methods:

{{< readfile "/static/include/app/apis/generated/mltraining-table.md" >}}

## Next steps

Follow one of these guides to write your own custom training script or to train models with training scripts:

{{< cards >}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{% card link="/how-tos/create-custom-training-scripts/" %}}
{{< /cards >}}
