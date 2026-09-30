---
title: Service
capabilities: ["glossary", "docs"]
id: service
short_description: Software packages that give a machine higher-level capabilities such as SLAM, computer vision, motion planning, and data collection. Some are built into viam-server, and others come from modules.
aliases:
  - /dev/reference/glossary/service/
---

Services are software packages that give a machine higher-level capabilities such as simultaneous localization and mapping (SLAM), computer vision, motion planning, and data collection.

Some services are built into `viam-server`.
Others are provided by {{< glossary_tooltip term_id="module" text="modules" >}}, either from the Viam registry or written by you.

Each service is typed by a proto API, such as the [service proto definitions](https://github.com/viamrobotics/api/tree/main/proto/viam/service).

For more information, see [Service APIs](/reference/apis/#service-apis).
