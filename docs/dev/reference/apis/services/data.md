---
title: "Data management service API"
linkTitle: "Data management"
weight: 10
type: "docs"
description: "Give commands to your data management service to sync data stored on the machine it is deployed on to the cloud."
icon: true
images: ["/icons/components/arm.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/services/data/
# updated: ""  # When the content was last entirely checked
---

The data management service API allows you to sync data stored on the machine it is deployed on to the cloud.

The [data management service](/data-ai/capture-data/capture-sync/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/data_manager-table.md" >}}

The data client API supports a separate set of methods that allow you to upload and export data to and from Viam.
For information about that API, see [Data Client API](/dev/reference/apis/data-client/).

## API

{{< readfile "/static/include/services/apis/generated/data_manager.md" >}}
