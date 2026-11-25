---
linkTitle: "Node.js setup"
title: "Node.js setup"
weight: 20
layout: "docs"
type: "docs"
description: "Set up a project for running Viam SDK code from a Node.js process: a backend service, a CLI tool, or another Node app that talks to a Viam machine."
capabilities: ["sdks"]
diataxis: how-to
date: "2026-04-10"
---

Set up a project for running Viam SDK code from a Node.js process: a backend service that supports a web app frontend, a CLI tool, or another Node app that talks to a Viam machine. Node.js requires extra setup compared to the browser because Node does not provide WebRTC natively: you register a WebRTC polyfill and plug in a Node-compatible gRPC transport before calling any SDK function. For the connection patterns your app will actually use, see [Connect to a machine](/build-apps/tasks/connect-to-machine/).

## Prerequisites

- Node.js 20 or later
- A configured Viam machine
- The machine's host address, an API key, and an API key ID

Get the three credentials from the machine's **CONNECT** tab in the Viam app: go to the machine's page, click **CONNECT**, select **Server-side TS**, and toggle **Include API key** on. Copy the `host`, `authEntity` (API key ID), and `payload` (API key) from the generated code sample.

## Create a project

```sh {class="command-line" data-prompt="$"}
mkdir my-viam-node-app
cd my-viam-node-app
npm init -y
npm pkg set type=module
```

Setting `"type": "module"` makes Node treat `.js` and `.ts` files as ES modules, which the example script needs for `import` and top-level `await`.

## Install the SDK and dependencies

Node.js needs three runtime packages:

- `@viamrobotics/sdk` — the Viam SDK
- `@connectrpc/connect-node@^1.7.0` — the Node-compatible gRPC transport
- `node-datachannel` — a WebRTC implementation for Node

Install everything at once:

```sh {class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk "@connectrpc/connect-node@^1.7.0" node-datachannel
npm install --save-dev tsx typescript @types/node
```

`tsx` runs TypeScript files directly and loads `.env` files, so you do not need a separate build step or env loader.

## Configure environment variables

Create a `.env` file in your project root:

```text
HOST=my-robot-main.xxxx.viam.cloud
API_KEY_ID=your-api-key-id
API_KEY=your-api-key-secret
```

Replace the three values with what you copied from the **CONNECT** tab.

Add `.env` to your `.gitignore`:

```sh {class="command-line" data-prompt="$"}
echo ".env" >> .gitignore
```

## Verify the connection

Create `src/main.ts`:

```ts
import * as VIAM from "@viamrobotics/sdk";
import * as wrtc from "node-datachannel/polyfill";
import * as connectNode from "@connectrpc/connect-node";

// Register a Node-compatible gRPC transport.
(globalThis as any).VIAM = {
  GRPC_TRANSPORT_FACTORY: (opts: any) =>
    connectNode.createGrpcTransport({ httpVersion: "2", ...opts }),
};

// Register WebRTC polyfills on the global object.
for (const key in wrtc) {
  (globalThis as any)[key] = (wrtc as any)[key];
}

const host = process.env.HOST;
const apiKeyId = process.env.API_KEY_ID;
const apiKey = process.env.API_KEY;

if (!host || !apiKeyId || !apiKey) {
  throw new Error("HOST, API_KEY_ID, and API_KEY must all be set in .env");
}

try {
  const machine = await VIAM.createRobotClient({
    host,
    credentials: {
      type: "api-key",
      authEntity: apiKeyId,
      payload: apiKey,
    },
    signalingAddress: "https://app.viam.com:443",
  });

  const resources = await machine.resourceNames();
  console.log(`Connected. Found ${resources.length} resources:`);
  for (const resource of resources) {
    console.log(`- ${resource.name} (${resource.subtype})`);
  }

  await machine.disconnect();
  process.exit(0);
} catch (err) {
  console.error("Connection failed:", err);
  process.exit(1);
}
```

Two blocks in this file are specific to Node.js and do not appear in a browser app:

**The WebRTC polyfill loop.** The SDK expects browser WebRTC APIs (`RTCPeerConnection`, `RTCDataChannel`, and so on) on the global object. Node does not provide these natively, so `node-datachannel/polyfill` installs them before any SDK code runs.

**The custom gRPC transport factory.** The SDK's default gRPC transport targets browsers. Node needs an HTTP/2 transport, which is what `@connectrpc/connect-node`'s `createGrpcTransport` provides. The `globalThis.VIAM.GRPC_TRANSPORT_FACTORY` hook lets you plug in an alternative transport.

Both must run before you call `createRobotClient`. ES `import` statements are hoisted, so the SDK is loaded first, but it reads the transport factory and the WebRTC globals when it connects, so registering them at the top of the file is enough. If you move the registration to a module that runs after the connection call, the SDK fails to connect.

## Run the script

Add a `start` script to `package.json`:

```json
{
  "scripts": {
    "start": "tsx --env-file=.env src/main.ts"
  }
}
```

Run it:

```sh {class="command-line" data-prompt="$"}
npm start
```

You should see:

```text
Connected. Found N resources:
- my-arm (arm)
- my-camera (camera)
...
```

where `N` is the number of components and services on your machine, followed by the name and type of each one.

If the script hangs or errors, the most common causes are:

- **`Failed to connect via all methods`, or a hang with no output.** The WebRTC polyfill or the transport factory is not registered before `createRobotClient` runs, or the machine is offline. Check the order in your script and confirm the machine is online in the Viam app.
- **`Top-level await is currently not supported with the "cjs" output format`.** The project is a CommonJS project. Run `npm pkg set type=module`.
- **Polyfills registered too late.** The polyfill loop and transport factory must run before the first call into the SDK. If you split them into a separate module that is imported after the SDK, the SDK initializes without them.
- **`.env` not loaded.** The `tsx --env-file=.env` flag loads the file. If you run the script a different way (`node`, `ts-node`, a bundler), use `dotenv` or your runtime's env loader instead.
- **Wrong transport.** If you see `Unsupported HTTP version` or similar, confirm that `@connectrpc/connect-node` is installed and the transport factory is registered on `globalThis.VIAM`.
- **Wrong `@connectrpc/connect-node` version.** The SDK depends on the Connect-ES v1 API. An unpinned install resolves to the incompatible v2 line and fails when the SDK tries to connect, in some cases with `TypeError: Cannot read properties of undefined (reading 'typeName')`. Pin it to `^1.7.0`, as in the install command above.

## Next

- [Connect to a machine](/build-apps/tasks/connect-to-machine/) for the connection patterns your app will actually use
- [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for reconnection and UI indicators
- [The SDK's `Node.md`](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/Node.md) for deeper detail on the polyfill and transport setup
