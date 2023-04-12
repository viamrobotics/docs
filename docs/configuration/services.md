---
title: "Services"
linkTitle: "Services"
weight: 20
type: "docs"
no_list: true
description: "Services are the software that runs on your robot."
tags: ["manage", "services"]
---

[Services](/services/) are built-in software packages that make it easier to add complex capabilities such as motion planning or object detection to your robot.

For services, the `type` specifies which of the Viam services you want to use on your robot, such as the Vision Service or the Motion Service.

The `name` serves as an identifier when accessing the resource from your code, as well as when configuring other resources that are dependent on that resource.
You can choose any unique name for a service.

The other aspects of configuring a service are highly specific to the type of service.
See the [services documentation](/services/) for more information.
