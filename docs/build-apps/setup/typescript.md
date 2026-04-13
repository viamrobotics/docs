---
linkTitle: "TypeScript setup"
title: "TypeScript setup"
weight: 10
layout: "docs"
type: "docs"
description: "Set up a project for building a Viam web app with TypeScript: a custom dashboard, an operator interface, or any other browser-based app that talks to a Viam machine."
date: "2026-04-10"
---

Set up a project for building a Viam web app with TypeScript: a custom dashboard, an operator interface, or any other browser-based app that talks to a Viam machine. This page covers the project scaffolding with [Vite](https://vitejs.dev/) and the Viam TypeScript SDK install. For the connection patterns your app will actually use, see [Connect to a machine](../../tasks/connect-to-machine/).

## Prerequisites

- Node.js 20 or later
- A configured Viam machine
- The machine's host address, an API key, and an API key ID

Get all three credentials from the machine's **CONNECT** tab in the Viam app: go to the machine's page, click **CONNECT**, select **TypeScript**, and toggle **Include API key** on. Copy the `host`, `authEntity` (the API key ID), and `payload` (the API key) from the generated code sample.

## Create a project

Create a directory for your project and initialize `package.json`.

```sh {class="command-line" data-prompt="$"}
mkdir my-viam-app
cd my-viam-app
npm init -y
```

Open `package.json` and add `"type": "module"` so Node treats `.js` files as ES modules:

```json
{
  "name": "my-viam-app",
  "type": "module",
  "version": "1.0.0"
}
```

## Install the SDK and Vite

```sh {class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
npm install --save-dev vite typescript
```

## Configure environment variables

Create a `.env` file in your project root:

```text
VITE_HOST=my-robot-main.xxxx.viam.cloud
VITE_API_KEY_ID=your-api-key-id
VITE_API_KEY=your-api-key-secret
```

Replace the three values with what you copied from the **CONNECT** tab. Vite exposes environment variables prefixed with `VITE_` to browser code through `import.meta.env`. See [the Vite env docs](https://vitejs.dev/guide/env-and-mode.html) for details.

Add `.env` to your `.gitignore` so you do not accidentally commit credentials:

```sh {class="command-line" data-prompt="$"}
echo ".env" >> .gitignore
```

## Create the HTML entry point

Create `index.html` in your project root:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My Viam App</title>
  </head>
  <body>
    <div id="status"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

## Verify the connection

Create `src/main.ts`:

```ts
import * as VIAM from "@viamrobotics/sdk";

const statusEl = document.getElementById("status") as HTMLDivElement;

async function main() {
  statusEl.textContent = "Connecting...";
  try {
    const machine = await VIAM.createRobotClient({
      host: import.meta.env.VITE_HOST,
      credentials: {
        type: "api-key",
        authEntity: import.meta.env.VITE_API_KEY_ID,
        payload: import.meta.env.VITE_API_KEY,
      },
      signalingAddress: "https://app.viam.com:443",
    });
    const resources = await machine.resourceNames();
    statusEl.textContent = `Connected. Found ${resources.length} resources.`;
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    statusEl.textContent = `Connection failed: ${msg}`;
  }
}

main();
```

This connects to your machine, fetches the list of configured resources, and shows the count in the page.

## Run the dev server

```sh {class="command-line" data-prompt="$"}
npx vite
```

Vite prints a local URL, typically `http://localhost:5173`. Open it in a browser. You should see:

```text
Connected. Found N resources.
```

where `N` is the number of components and services configured on your machine. If the page shows `Connection failed:` followed by an error, check that the three values in your `.env` file match the **CONNECT** tab exactly, including the `https://` in the host if the generated sample includes one.

If you use Firefox for development, see the [Firefox WebRTC localhost workaround](../../tasks/test-locally/#firefox-webrtc-localhost-workaround) on the Test against a local machine page. Firefox blocks WebRTC connections from `localhost`, so you need a small `/etc/hosts` adjustment to develop locally.

## Next

- [Connect to a machine](../../tasks/connect-to-machine/) for the connection patterns your app will actually use, including language tabs for Flutter
- [Handle connection state](../../tasks/handle-connection-state/) for reconnection and UI indicators
- [Stream video](../../tasks/stream-video/) for displaying camera feeds
