---
linkTitle: "React Native setup"
title: "React Native setup"
weight: 40
layout: "docs"
type: "docs"
description: "Set up a project for building a Viam mobile app using React Native specifically. For new cross-platform apps, prefer Flutter."
date: "2026-04-10"
---

Set up a project for building a Viam mobile app using React Native specifically. **If you do not already have a React Native codebase, prefer [Flutter](/build-apps/setup/flutter/) for new cross-platform apps; React Native is here for teams whose existing apps are React Native.** This page covers the project scaffolding, the Viam SDK install, six runtime polyfill packages, a custom XHR-based gRPC transport, a Metro bundler configuration fix for a dependency version conflict, and platform permissions on Android and iOS. For the connection patterns your app will actually use, see [Connect to a machine](/build-apps/tasks/connect-to-machine/).

{{< alert title="Expo is not supported" color="caution" >}}
The Viam TypeScript SDK does not work with Expo (neither Expo Go nor development builds). You must use the React Native CLI. If your project uses Expo, you cannot add the Viam SDK without ejecting to a bare workflow.
{{< /alert >}}

## Prerequisites

- The React Native CLI environment for your development platform ([React Native environment setup](https://reactnative.dev/docs/environment-setup))
- Xcode for iOS targets, Android Studio for Android targets
- A configured Viam machine
- The machine's address, an API key, and an API key ID

Get the credentials from the machine's **CONNECT** tab in the Viam app. Click **CONNECT**, select **TypeScript**, toggle **Include API key** on, and copy the `host`, `authEntity`, and `payload` values.

## Create a project

```sh {class="command-line" data-prompt="$"}
npx @react-native-community/cli@latest init MyViamApp
cd MyViamApp
```

## Install the SDK and dependencies

The Viam SDK needs six runtime packages in addition to itself:

```sh {class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk \
  fast-text-encoding \
  react-native-fast-encoder \
  react-native-fetch-api \
  react-native-url-polyfill \
  react-native-webrtc \
  web-streams-polyfill
```

After the install completes, run `pod install` for iOS:

```sh {class="command-line" data-prompt="$"}
cd ios && pod install && cd ..
```

## Add polyfill files

The SDK expects browser-style globals (`TextEncoder`, `fetch`, `Headers`, `Request`, `Response`, `ReadableStream`, WebRTC APIs) that React Native does not provide natively. The polyfill files from the SDK example repo register these globals before the SDK initializes.

Create `polyfills.native.ts` in your project root with the contents from the [SDK example's `polyfills.native.ts`](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/examples/react-native/polyfills.native.ts). The file is stable and you can copy it as-is.

Also create `polyfills.ts` (no-op fallback for web builds) with the contents from [the SDK example's `polyfills.ts`](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/examples/react-native/polyfills.ts).

## Add the custom gRPC transport

React Native's `fetch` does not support the streaming and binary-body semantics that Connect's default gRPC-web transport requires. The SDK example provides an XHR-based transport that works around this. Copy it from the SDK example:

Create `transport.ts` in your project root with the contents from [the SDK example's `transport.ts`](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/examples/react-native/transport.ts). Do not modify it. The transport implementation is verbose (roughly 350 lines) and stable; treating it as a copy-and-forget dependency is the intended approach.

## Update metro.config.js

`react-native` and `react-native-webrtc` depend on conflicting versions of `event-target-shim`. Metro's default resolver picks the wrong one, which causes runtime errors. Tell Metro to resolve `event-target-shim` inside `react-native-webrtc` using its own nested version:

```js
const { getDefaultConfig } = require("@react-native/metro-config");
const resolveFrom = require("resolve-from");

const config = getDefaultConfig(__dirname);

config.resolver.resolveRequest = (context, moduleName, platform) => {
  if (
    moduleName.startsWith("event-target-shim") &&
    context.originModulePath.includes("react-native-webrtc")
  ) {
    return {
      filePath: resolveFrom(context.originModulePath, moduleName),
      type: "sourceFile",
    };
  }
  return context.resolveRequest(context, moduleName, platform);
};

module.exports = config;
```

Save this as `metro.config.js` in your project root, replacing whatever `react-native init` generated.

## Add Android permission

React Native apps targeting Android need the `ACCESS_NETWORK_STATE` permission for WebRTC. Add it to `android/app/src/main/AndroidManifest.xml` inside the top-level `<manifest>` element:

```xml
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## Register polyfills and transport in App.tsx

Replace the contents of `App.tsx` with:

```tsx
import * as VIAM from "@viamrobotics/sdk";
import { polyfills } from "./polyfills";
polyfills();

import { GrpcWebTransportOptions } from "@connectrpc/connect-web";
import { createXHRGrpcWebTransport } from "./transport";

// @ts-expect-error -- globalThis.VIAM is not in standard types
globalThis.VIAM = {
  GRPC_TRANSPORT_FACTORY: (opts: GrpcWebTransportOptions) => {
    return createXHRGrpcWebTransport(opts);
  },
};

import React, { useEffect, useState } from "react";
import { SafeAreaView, Text, StyleSheet } from "react-native";

// Replace these with the values from your machine's CONNECT tab.
// For a production app, use react-native-config or a secure store
// instead of hardcoding credentials in source.
const HOST = "my-robot-main.xxxx.viam.cloud";
const API_KEY_ID = "your-api-key-id";
const API_KEY = "your-api-key-secret";

function App(): React.JSX.Element {
  const [status, setStatus] = useState("Connecting...");

  useEffect(() => {
    async function connect() {
      try {
        const machine = await VIAM.createRobotClient({
          host: HOST,
          credentials: {
            type: "api-key",
            authEntity: API_KEY_ID,
            payload: API_KEY,
          },
          signalingAddress: "https://app.viam.com:443",
        });
        const resources = await machine.resourceNames();
        setStatus(`Connected. Found ${resources.length} resources.`);
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        setStatus(`Connection failed: ${msg}`);
      }
    }
    connect();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.text}>{status}</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  text: { fontSize: 18 },
});

export default App;
```

**The order of imports in this file matters.** The polyfills and the transport factory assignment must run before any SDK call. If you move the `polyfills()` call or the `globalThis.VIAM` assignment below the React imports, or import any SDK submodule before them, the SDK will fail to initialize.

## Run the app

```sh {class="command-line" data-prompt="$"}
npm run ios
# or
npm run android
```

The app builds, launches on the selected simulator or device, and shows:

```text
Connected. Found N resources.
```

where `N` is the number of components and services on your machine.

If you see `Connection failed:`, the most common causes are:

- **Polyfills imported out of order.** The `polyfills()` call and the `globalThis.VIAM` assignment must appear before any other code that touches the SDK, including React imports if you reference SDK types in them.
- **`metro.config.js` not applied.** Metro caches aggressively. Stop the Metro bundler and run `npm start -- --reset-cache` after editing `metro.config.js`.
- **Android permission missing.** Confirm `ACCESS_NETWORK_STATE` is in `AndroidManifest.xml` and rebuild the Android app.
- **iOS pods out of date.** Run `cd ios && pod install && cd ..` again after any native dependency change.
- **Using Expo.** If you started from an Expo project, none of this setup will work. You must use a bare React Native project.

## Next

- [Connect to a machine](/build-apps/tasks/connect-to-machine/) for the connection patterns your app will actually use
- [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for reconnection and UI indicators
- [The SDK's `ReactNative.md`](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/ReactNative.md) for deeper detail on the polyfills, the transport, and the Android environment variables needed for the Android build
