---
title: "Program a Robot"
linkTitle: "Program Robots"
childTitleEndOverwrite: "Program Robots"
description: "Use the SDK of your preferred language to write code to control your robots."
weight: 50
simple_list: false
type: docs
images: ["/img/code.png"]
---

Viam offers software development kits (SDKs) in popular languages which

- Streamline connection, authentication, and encryption against a server using {{< glossary_tooltip term_id="webrtc" >}}
- Enable you to interface with robots without calling the `viam-server` [gRPC APIs for robot controls](https://github.com/viamrobotics/api) directly

![Diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client.](img/sdks/image1.png)

Use the SDK of your preferred language to write code to control your robots.

Viam currently offers SDKs for the following languages:

- [Python SDK](https://python.viam.dev/)
- [Go SDK](https://pkg.go.dev/go.viam.com/rdk)
- [TypeScript SDK](https://ts.viam.dev/)
- [C++ SDK (alpha)](https://cpp.viam.dev/)
- [Flutter SDK (alpha)](https://github.com/viamrobotics/viam-flutter-sdk)

Click on the links above to read more about installation and usage of each SDK.

## Install an SDK

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip install viam-sdk
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go install go.viam.com/rdk/robot/client@latest
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install --save @viamrobotics/sdk
```

{{% /tab %}}
{{% tab name="C++" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{< /tabs >}}
{{% tab name="Flutter" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-flutter-sdk#viam-flutter-sdk).

{{% /tab %}}
{{< /tabs >}}
