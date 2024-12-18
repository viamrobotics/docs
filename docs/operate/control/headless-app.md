---
linkTitle: "Create a headless app"
title: "Create a headless app"
weight: 30
layout: "docs"
type: "docs"
no_list: true
description: "Run control logic on a machine."
---

To write control logic for your machine that will run without a user interface, you can use the Python SDK or the Go SDK.
Both SDKs include similar methods to hit standard component and service API endpoints, so choose the language you feel most comfortable scripting in.

{{% alert title="In this page" color="tip" %}}

1. [Install an SDK](#install-an-sdk)
1. [Authenticate your script to your machine with API keys](#authenticate-your-script)
1. [Write your control script](#write-your-control-script)
1. [Run your script](#run-your-script)

{{% /alert %}}

## Install an SDK

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

Run the following command to install the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk):

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{< /tabs >}}

## Authenticate your script

## Write your control script

### Examples

## Run your script

### Test by running it manually

### Configure your script to run as an automatic process
