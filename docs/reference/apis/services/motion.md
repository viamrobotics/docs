---
title: "Motion service API"
linkTitle: "Motion"
weight: 60
type: "docs"
description: "Give commands to move a machine's components from one location or pose to another."
icon: true
images: ["/icons/components/arm.svg"]
date: "2022-01-01"
aliases:
  - /dev/reference/apis/services/motion/
  - /appendix/apis/services/motion/
# updated: ""  # When the content was last entirely checked
---

The motion service API allows you to give commands to your [motion service](/reference/apis/services/motion/) for moving a mobile robot based on a SLAM map or GPS coordinates or for moving a machine's components from one pose to another.

The motion service supports the following methods:

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

## API

{{< readfile "/static/include/services/apis/generated/motion.md" >}}
