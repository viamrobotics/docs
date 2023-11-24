---
title: "Data Management"
linkTitle: "Data Management"
weight: 40
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Access data captured by the robot's components and train image classification and object detection models on the data."
aliases:
  - /manage/data-management/
  - /services/data-management/
  - /manage/data/
menuindent: true
# SME: Alexa Greenberg
---

Data Management is built into Viam.

![Data is captured on the robot, uploaded to the cloud, and then deleted off local storage.](/data/data_management.png)

Once you have captured and synced data, you can:

{{< cards >}}
{{% card link="/data/view/" %}}
{{% card link="/data/dataset/" %}}
{{% card link="/data/query/" %}}
{{% card link="/data/export/" %}}
{{< /cards >}}

<br>

## Requirements

You must configure data capture and cloud synchronization with the [Data Management Service](/build/configure/services/data/) to be able to view, label, and export data.

## Next steps

For a comprehensive tutorial on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{< /cards >}}
