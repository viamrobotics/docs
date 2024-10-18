---
title: "Extend Viam with Models from the Viam Registry"
linkTitle: "Registry"
weight: 600
type: "docs"
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Add additional models of components and services or ML models from the Viam Registry, or extend Viam by creating new modular resources."
images: ["/platform/registry.svg"]
no_list: true
aliases:
  - "/build/program/extend/modular-resources/"
  - "/extend/modular-resources/"
  - "/extend/"
  - "/build/program/extend/modular-resources/key-concepts/"
  - "/modular-resources/key-concepts/"
  - "/modular-resources/"
menuindent: true
---

<br>
{{<imgproc src="/platform/registry.svg" class="aligncenter" resize="x900" declaredimensions=true alt="Representation of the Viam registry, some modules within it, and a rover they support." style="width:350px" >}}
<br>

The [Viam registry](https://app.viam.com/registry) is the storage and distribution system for:

{{< cards >}}
{{% manualcard link="#modular-resources" %}}

**Modular resources** that add capabilities to your machine beyond what is built into `viam-server`

{{% /manualcard %}}
{{% manualcard link="/services/ml/ml-models/" %}}

**ML models** to deploy with machine applications like computer vision

{{% /manualcard %}}
{{% manualcard link="/services/ml/training-scripts/" %}}

**Training scripts** to train and produce ML models in the Viam cloud for custom machine learning

{{% /manualcard %}}
{{< /cards >}}
