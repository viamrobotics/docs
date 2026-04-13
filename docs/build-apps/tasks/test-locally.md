---
linkTitle: "Test against a local machine"
title: "Test against a local machine"
weight: 80
layout: "docs"
type: "docs"
description: "Develop a Viam client app against a real machine without deploying. Covers direct local-network connections and the viam module local-app-testing CLI."
date: "2026-04-10"
---

Develop your Viam client app against a real machine without deploying to production on every change. There are two ways: open a direct connection to the machine from your local dev server, or use the `viam module local-app-testing` CLI to emulate the Viam Applications hosting environment.

For the CLI command name: `viam module local-app-testing` is grouped under `viam module` because Viam Applications are distributed through the same module registry. It has nothing to do with building server-side modules. Treat the `module` in the command name as an artifact of the registry plumbing.

## Which approach to use

- **Direct connection** if your app does not need cookie-based credential injection. You use the same connection code you would use in production, with the credentials in a local `.env` file. Simplest for single-machine browser apps and for Flutter apps.
- **`local-app-testing` CLI** if your app is a hosted Viam Application that reads credentials from browser cookies. The CLI emulates the cookie injection that Viam Applications does in production, so your app code can use the same cookie-reading logic in development.

## Direct connection

Run your local dev server with credentials in a `.env` file. Your app calls `createRobotClient` or `RobotClient.atAddress` with the credentials from the file.

See [App scaffolding](./setup/) for the platform-specific setup pages, which all use this pattern in their connection verification step. The setup pages are the canonical reference for this approach.

### Local-network connections

If the machine is on the same network as your dev server, you can skip the cloud signaling service and connect directly over the local network. Restart `viam-server` with the `-no-tls` flag, then set `signalingAddress` to the machine's local address instead of `https://app.viam.com:443`:

```ts
const machine = await VIAM.createRobotClient({
  host: "my-robot-main.xxxx.viam.cloud",
  credentials: {
    type: "api-key",
    authEntity: process.env.API_KEY_ID,
    payload: process.env.API_KEY,
  },
  signalingAddress: "http://my-robot.local:8080",
});
```

Local-network connections eliminate the cloud round trip and are useful for latency-sensitive testing. See the [connectivity reference](/dev/reference/sdks/connectivity/#connect-over-local-network-or-offline) for the exact `viam-server` flags and local hostname setup.

## `viam module local-app-testing` CLI

The `local-app-testing` CLI proxies your local dev server and injects the same cookies that the Viam Applications hosting platform injects in production. This lets you test an app that reads credentials from cookies without deploying to the registry on every change.

The CLI has two modes, matching the two Viam Application types:

- **Single-machine mode** (pass `--machine-id`). The CLI fetches an API key for the specified machine from the Viam backend and writes a machine-specific cookie that your app reads.
- **Multi-machine mode** (omit `--machine-id`). The CLI uses the user access token from your current `viam login` session and writes it as a cookie, so your app sees the same credential shape it would see in a deployed multi-machine Viam Application.

### Start your dev server

Run your app's dev server as you normally would. For a Vite-based web app:

```sh {class="command-line" data-prompt="$"}
npx vite
```

Vite prints a URL, typically `http://localhost:5173`. Leave this running.

### Start the local-app-testing server

In a second terminal, run the CLI:

{{< tabs >}}
{{% tab name="Single-machine" %}}

```sh {class="command-line" data-prompt="$"}
viam login
viam module local-app-testing \
  --app-url http://localhost:5173 \
  --machine-id YOUR-MACHINE-ID
```

Get `YOUR-MACHINE-ID` from the machine's page in the Viam app. The CLI:

1. Fetches an API key for the machine from the Viam backend.
2. Fetches the machine's FQDN from its main part.
3. Starts an HTTP server on `http://localhost:8012`.
4. Opens your browser to `http://localhost:8012/start`, which sets the cookies and redirects to your dev server through the proxy.

{{% /tab %}}
{{% tab name="Multi-machine" %}}

```sh {class="command-line" data-prompt="$"}
viam login
viam module local-app-testing --app-url http://localhost:5173
```

Without `--machine-id`, the CLI runs in multi-machine mode and uses the access token from your `viam login` session. Do not pass an API key profile for multi-machine mode; the CLI needs a user access token, not a service-identity API key. The CLI:

1. Reads your current access token from the local CLI config.
2. Starts an HTTP server on `http://localhost:8012`.
3. Opens your browser to `http://localhost:8012/start`, which sets the user-token cookie and redirects to your dev server.

{{% /tab %}}
{{< /tabs >}}

### Develop against the running machine

Edit your source files in the dev server project. Hot reload, browser refresh, and all the development features of your chosen tooling work the same way they would without the proxy. The cookies persist across reloads, so you do not need to re-run the CLI after every source change.

Stop the local-app-testing server with `Ctrl+C` when you are done. The dev server can keep running.

## Firefox WebRTC localhost workaround

Firefox blocks WebRTC connections from `localhost` due to a network interface enumeration restriction. If you use Firefox for development, you have two options.

The simplest option is to use Chrome, Edge, or another Chromium-based browser for local testing. WebRTC works from `localhost` in those browsers without any configuration.

If you need Firefox specifically, add a local hostname to your `/etc/hosts` file and run your dev server bound to that hostname instead of `localhost`:

```sh {class="command-line" data-prompt="$"}
sudo bash -c 'echo "127.0.0.1  dev.local" >> /etc/hosts'
```

Then start your dev server with the hostname. For Vite:

```sh {class="command-line" data-prompt="$"}
npx vite --host dev.local
```

Open `http://dev.local:5173` in Firefox. WebRTC works because the URL is no longer `localhost`.

To remove the hostname later:

```sh {class="command-line" data-prompt="$"}
sudo sed -i '' '/dev.local/d' /etc/hosts
```

(On Linux, drop the empty `''` argument to `sed -i`.)

## Troubleshooting

- **Port 8012 already in use.** The CLI hardcodes port 8012. If another process owns it, stop that process first.
- **"No access token found" in multi-machine mode.** Run `viam login` (not `viam login api-key`) to obtain a user access token. Service-identity API keys do not grant user-level access.
- **Cookies not set in the browser.** The CLI redirects the browser to `/start` on first run, which is where the cookies are written. If you navigate directly to a proxied path before visiting `/start`, the cookies are missing. Close the tab and reopen from the terminal link, or navigate to `http://localhost:8012/` manually.

## Next

- [Deploy a Viam application](./hosting/deploy/) for packaging and uploading your app once local testing is complete
- [Connectivity reference](/dev/reference/sdks/connectivity/) for local-network and offline connection details
