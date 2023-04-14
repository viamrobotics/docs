---
title: "ORB-SLAM3 Integrated Library"
linkTitle: "ORB-SLAM3"
weight: 70
type: "docs"
description: "Configure a SLAM service with the ORB-SLAM3 library."
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

ORB-SLAM3 performs sparse SLAM using monocular or RGB-D images.

{{% alert title="Note" color="note" %}}
While ORB-SLAM3 does support the use of monocular cameras, for best results it is recommended that you use an RGB-D camera.
{{% /alert %}}

### Requirements

Install the binary required to utilize `ORB-SLAM3` on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{< /tab >}}
{{% tab name="Linux x86_64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/orb_grpc_server http://packages.viam.com/apps/slam-servers/orb_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/orb_grpc_server
```

{{% /tab %}}
{{< /tabs >}}

### Configuration
