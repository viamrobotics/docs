---
title: "Arm API"
linkTitle: "Arm"
weight: 5
type: "docs"
description: "Give commands to your arm components for linear motion planning."
icon: true
images: ["/icons/components/arm.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/components/arm/
# updated: ""  # When the content was last entirely checked
---

The arm API allows you to give commands to your [arm components](/operate/reference/components/arm/) for linear motion planning with self-collision prevention.
If you want the arm to avoid obstacles, or you want to plan complex motion in an automated way, use the [motion API](/dev/reference/apis/services/motion/).

The arm component supports the following methods:

{{< readfile "/static/include/components/apis/generated/arm-table.md" >}}

## API

{{< readfile "/static/include/components/apis/generated/arm.md" >}}
