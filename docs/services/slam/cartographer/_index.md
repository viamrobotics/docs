---
title: "Cartographer Integrated Library"
linkTitle: "cartographer"
weight: 70
type: "docs"
description: "Configure a SLAM service with the Cartographer library."
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

[Cartographer](https://github.com/cartographer-project) performs dense SLAM using LIDAR data.

## Requirements

Install the binary required to utilize the `cartographer` library on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/carto_grpc_server http://packages.viam.com/apps/slam-servers/carto_grpc_server-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/carto_grpc_server
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install carto-grpc-server
```

{{% /tab %}}
{{< /tabs >}}

## Configuration
