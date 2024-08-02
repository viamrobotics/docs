---
title: "Write and deploy code to control your machine"
linkTitle: "Control code for your machine"
weight: 10
type: "docs"
description: "Write code to control machines and run it on the machine or remotely."
images: ["/general/code.png"]
imageAlt: "Code sample"
tags: ["components", "configuration"]
---

Once you have configured a machine, start writing code to perform actions with the {{< glossary_tooltip term_id="component" text="components" >}} or {{< glossary_tooltip term_id="service" text="services" >}} of a {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{< alert title="In this page" color="tip" >}}

1. [Write code to control your machine](#write-code-to-control-your-machine)
2. [Run your code](#run-your-code)

{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/tzJf0XfUCmA">}}

## Write code to control your machine

{{< table >}}
{{% tablestep link="/sdks/" %}}
**1. Install an SDK**

Write a program to control your smart machine using the programming language of your choice.
Viam has [SDKs](/sdks/) for Python, Golang, C++, TypeScript, and Flutter.

The easiest way to get started is to copy the auto-generated boilerplate code from the **Code sample** page of the **CONNECT** tab on your machine's page in the Viam app.
You can run this code directly on the machine or from a separate computer; it then connects to the machine using API keys.

Viam's APIs are standardized across all models of a given component or service.
This means you can test and change hardware without changing code.

After configuring your resource, navigate to your machine's **CONNECT** tab.
Click on any of the listed languages and follow the instructions to install the SDK.

To install your preferred Viam SDK on your Linux or macOS development machine or [single-board computer](/components/board/), run one of the following commands in your terminal:

{{< tabs >}}
{{% tab name="Python" %}}

If you are using the Python SDK, [set up a virtual environment](/sdks/python/python-venv/) to package the SDK inside before running your code, avoiding conflicts with other projects or your system.

For macOS (both Intel `x86_64` and Apple Silicon) or Linux (`x86`, `aarch64`, `armv6l`), run the following commands:

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
pip install viam-sdk
```

Windows is not supported.
If you are using Windows, use the [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) and install the Python SDK using the preceding instructions for Linux.
For other unsupported systems, see [Installing from source](https://python.viam.dev/#installing-from-source).

If you intend to use the [ML (machine learning) model service](/services/ml/), use the following command instead, which installs additional required dependencies along with the Python SDK:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
```

{{< alert title="Info" color="info" >}}
The TypeScript SDK currently only supports building web browser apps.
{{< /alert >}}

{{% /tab %}}
{{% tab name="C++" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{% tab name="Flutter" %}}

```sh {class="command-line" data-prompt="$"}
flutter pub add viam_sdk
```

{{% /tab %}}
{{< /tabs >}}
{{% /tablestep %}}
{{% tablestep link="/appendix/apis/" %}}
**2. Copy the connection code**

Then copy and run the sample code to connect to your machine.

The sample code will show you how to authenticate and connect to a machine, as well as some of the methods you can use on your configured components and services.
{{% /tablestep %}}
{{% tablestep link="/appendix/apis/" %}}
**3. Use component and service APIs**

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}} has a standardized API that you can access with an SDK (software development kit) in your preferred programming language.
For example, you can send the same [`SetPower` command](/components/motor/#setpower) to any kind of motor, using any of the available SDKs.

See [component APIs](/appendix/apis/#component-apis) and [service APIs](/appendix/apis/#service-apis) for a full list of available API methods.

{{% /tablestep %}}
{{< /table >}}

## Run your code

There are three different ways you can run code to control your machine:

{{< table >}}
{{% tablestep link="/sdks/#run-code" %}}
**1. Run code remotely or on your machine**

You can run the code to control your machine on any computer where you have an SDK installed.

If the computer that `viam-server` runs on has enough compute power, you can also configure your machine to run your code as a managed process whenever it boots.
See [Processes](/configure/processes/#configure-a-process) for more information.

{{% /tablestep %}}
{{% tablestep link="/use-cases/create-module/" %}}
**2. (Recommended) Wrap your code in a module**

Once you have written code to control your machine and tested it, you can then wrap your custom functionality by [creating a module](/use-cases/create-module/).
In wrapping your code into a module, you will be able to:

- deploy it across one or more machines
- use it in {{< glossary_tooltip term_id="fragment" text="fragments" >}}
- version it

You can package any files, code, or executable into a module.
When you add a module to your machine's configuration, the entrypoint defined for the module is run which can start your code.

If the code you have written augments what a component does, such as, for example, adding an overlay to a camera stream, create your own camera model inside your module and amend the API methods to have your custom functionality.
For an example of this, see the [facial-detection module](https://github.com/viam-labs/facial-detection) which wraps its logic into a custom vision service.

If your functionality does not conform to existing API types such as the motor or camera API, you can [use a generic API to wrap your code](https://docs.viam.com/use-cases/create-module/#choose-an-api-to-implement-in-your-model).

For more information, see [How to create and deploy a new module](/use-cases/create-module/).

{{% /tablestep %}}
{{< /table >}}

## Next steps

To see full sample projects, that configure and control machines, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{< /cards >}}
