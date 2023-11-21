---
title: "Data Management"
linkTitle: "Data Management"
weight: 40
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Access data captured by the robot's components and train image classification and object detection models on the data."
aliases:
  - "/manage/data-management/"
# SME: Alexa Greenberg
---

Data Management is built into Viam.

![Data is captured on the robot, uploaded to the cloud, and then deleted off local storage.](/manage/data/data_management.png)

Once you have captured and synced data, you can:

{{< cards >}}
{{% card link="/manage/data/view/" %}}
{{% card link="/manage/data/dataset/" %}}
{{% card link="/manage/data/export/" %}}
{{< /cards >}}

<br>

## Requirements

You must configure data capture and cloud synchronization with the [Data Management Service](/services/data/) to be able to view, label, and export data.

## Next steps

For a comprehensive tutorial on data capture, synchronization, and accessing captures data, see the following tutorial:

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{< /cards >}}
