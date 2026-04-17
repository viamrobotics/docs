---
linkTitle: "Python setup"
title: "Python setup"
weight: 50
layout: "docs"
type: "docs"
description: "Set up a project for writing a Viam app in Python: a control script, a backend service, a data pipeline, or any other Python program that talks to a Viam machine."
date: "2026-04-13"
---

Set up a project for writing a Viam app in Python: a control script, a backend service, a data pipeline, or any other Python program that talks to a Viam machine. For the connection patterns your app will actually use, see [Connect to a machine](/build-apps/tasks/connect-to-machine/).

## Prerequisites

- Python 3.9 or later
- A configured Viam machine
- The machine's address, an API key, and an API key ID

Get the three credentials from the machine's **CONNECT** tab in the Viam app: go to the machine's page, click **CONNECT**, select **Python**, and toggle **Include API key** on. Copy the address, API key, and API key ID from the generated code sample.

## Create a project

Create a directory for your project and set up a virtual environment:

```sh {class="command-line" data-prompt="$"}
mkdir my-viam-app
cd my-viam-app
python3 -m venv .venv
source .venv/bin/activate
```

## Install the SDK

```sh {class="command-line" data-prompt="$"}
pip install viam-sdk
```

Pre-built binaries are available for macOS (Intel and Apple Silicon) and Linux (x86_64, aarch64, armv6l). On Windows, WebRTC is not supported natively; use WSL or connect with `disable_webrtc=True` in the dial options.

If you need the ML model service, install with the optional dependency:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

## Configure credentials

Create a `.env` file in your project root:

```text
MACHINE_ADDRESS=my-robot-main.xxxx.viam.cloud
API_KEY_ID=your-api-key-id
API_KEY=your-api-key-secret
```

Replace the three values with what you copied from the **CONNECT** tab.

Add `.env` to your `.gitignore`:

```sh {class="command-line" data-prompt="$"}
echo ".env" >> .gitignore
```

Install `python-dotenv` to load the file:

```sh {class="command-line" data-prompt="$"}
pip install python-dotenv
```

## Verify the connection

Create `main.py`:

```python
import asyncio
import os

from dotenv import load_dotenv
from viam.robot.client import RobotClient

load_dotenv()


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ["API_KEY"],
        api_key_id=os.environ["API_KEY_ID"],
    )
    machine = await RobotClient.at_address(os.environ["MACHINE_ADDRESS"], opts)

    print(f"Connected. Found {len(machine.resource_names)} resources.")

    await machine.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```sh {class="command-line" data-prompt="$"}
python main.py
```

You should see:

```text
Connected. Found N resources.
```

where `N` is the number of components and services on your machine.

All Viam Python SDK methods are async. Your app code runs inside `asyncio.run()` and uses `await` for every SDK call. Always call `machine.close()` when done to release the connection.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'viam'`.** Confirm the virtual environment is activated (`source .venv/bin/activate`) and that you installed the SDK inside it.
- **Connection hangs on Windows.** WebRTC is not supported on native Windows. Either use WSL, or pass `disable_webrtc=True` in your `DialOptions` to fall back to direct gRPC.
- **Credentials wrong.** Compare the three values in `.env` to the **CONNECT** tab output.

## Next

- [Connect to a machine](/build-apps/tasks/connect-to-machine/) for the connection patterns your app will actually use
- [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for reconnection and status indicators
- [The Python SDK reference](https://python.viam.dev/) for per-component API details
