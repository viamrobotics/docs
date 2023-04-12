---
title: "Robot Development Kit"
linkTitle: "Robot Development Kit"
weight: 1
type: "docs"
description: "The RDK is the open-source, on-robot portion of the Viam platform, that provides `viam-server` and the Go SDK."
tags: ["server", "rdk"]
---

{{< alert title="Tip" color="tip" >}}
For an overview of the Viam platform, see [Viam in 3 minutes](/viam/).
{{< /alert >}}

Viam’s Robot Development Kit (RDK) RDK is the [open-source](https://github.com/viamrobotics/rdk), on-robot portion of the Viam platform, that provides `viam-server` and the Go SDK.

## `viam-server`

_viam-server_ is responsible for:

- All gRPC and WebRTC communication
- Connecting robots to the cloud
- Loading and managing connections to hardware [components](/components/)
- Running built-in [services](/services/)
- Managing configured processes
- Connecting to other parts of your robot

## Next Steps

{{< cards >}}
  {{% card link="/program/sdk-as-client/" size="small" %}}
  {{% card link="/program/extend/" size="small" %}}
  {{% card link="/internals/micro-rdk/" size="small" %}}
{{< /cards >}}
