---
linkTitle: "Overview"
title: "Build apps"
weight: 1
layout: "docs"
type: "docs"
description: "Build software that uses a Viam SDK to talk to your machines and the Viam cloud, from web dashboards to long-running backend services."
date: "2026-04-10"
---

A Viam app is software that uses a Viam SDK to talk to a machine or to the Viam cloud. It runs outside `viam-server`: in a browser, on a phone, on a server, or on a laptop. Viam apps come in many shapes: a browser dashboard, a Flutter app on a kiosk, a Python service that polls sensors, a Go program that orchestrates a fleet.

The line between an app and a [module](/build-modules/) is where the code runs. A module runs inside `viam-server` and extends it with new components or services. An app runs outside `viam-server` and uses the SDK to talk to it.

This section covers building apps: setup for each language, connection and authentication, streaming video, querying captured data, controlling components, and deployment.

## What the SDK does

The Viam SDKs handle the connection details for you. They open the transport (WebRTC where appropriate, gRPC otherwise), manage sessions for safety, and reconnect automatically when the network drops. You write business logic; the SDK handles the wire.

## Deployment options

A Viam app can be distributed and run in five different ways. Most apps fit cleanly into one of these shapes; a few combine two (a long-running service plus a web frontend, for example).

| Deployment               | What it is                                                                                                                                                                                                                                                                                                        | Typical platform                                                                  |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Viam Applications**    | A web app hosted by Viam at `{name}_{namespace}.viamapplications.com`. Auth and machine credentials are injected automatically. No server-side code execution. Always serves the latest uploaded version.                                                                                                         | Browser (TypeScript or any frontend framework)                                    |
| **Self-hosted web app**  | A web app you serve yourself: Vercel, Netlify, S3, GitHub Pages, your own server. You handle TLS, auth, credentials, and the domain. You get full control of versioning, server-side functions, and anything else your hosting platform supports.                                                                 | Browser (TypeScript or any frontend framework)                                    |
| **Distributed binary**   | A native app you build and ship through an app store, an installer, or an internal channel. The user installs it on their device and opens it from their home screen or desktop.                                                                                                                                  | Flutter (iOS, Android, Linux, macOS, web, Windows) or React Native (iOS, Android) |
| **Long-running service** | A daemon that runs continuously on a server, container, or edge device. No UI; it talks to one or more machines, processes data, triggers actions, exposes its own API, or integrates with other systems. Operated by ops tooling (systemd, Kubernetes, supervisord) rather than by a user clicking on something. | Python, Go, Node.js, C++                                                          |
| **Local execution**      | Code you run from your own laptop or terminal: a script, a notebook, a Flutter desktop build for development. Useful for prototyping, ad-hoc operations, debugging, or scripts you run by hand.                                                                                                                   | TypeScript, Python, Go, Flutter, Node.js, React Native, C++                       |

The platform column is a guide, not a constraint. Most platforms fit several deployment shapes (a Flutter app can be distributed as a binary or run locally for development; TypeScript can run in a browser or as a Node service).

## Viam hosting

If you are building a browser-based app, Viam can host it for you. Viam Applications serves your app at a dedicated URL with authentication and credential injection handled by the platform. See [Viam hosting](/build-apps/hosting/) for how it works, how to deploy, and the hosting platform details.

## Where to start

If you want **a quick operator interface and don't need to write code**, use [teleop workspaces](/monitor/teleop-workspaces/). They are widget-based and live in the monitor section.

If you want **a custom web dashboard or operator interface in a browser**, see [TypeScript setup](/build-apps/setup/typescript/) and the [single-machine dashboard tutorial](/build-apps/app-tutorials/tutorial-dashboard/).

If you want **one app that runs on phones, tablets, and desktops from a single codebase**, see [Flutter setup](/build-apps/setup/flutter/) and the [Flutter widget tutorial](/build-apps/app-tutorials/tutorial-flutter-app/).

If you want **a long-running service or script that talks to Viam without a UI**, pick your language: [Python](/build-apps/setup/python/), [Go](/build-apps/setup/go/), [Node.js](/build-apps/setup/node/), or [C++](/build-apps/setup/cpp/). The [Python monitoring service tutorial](/build-apps/app-tutorials/tutorial-monitoring-service/) walks through building one from scratch.

If you want **a dashboard that aggregates data across many machines**, see [Connect to the Viam cloud](/build-apps/tasks/connect-to-cloud/) and the [multi-machine fleet dashboard tutorial](/build-apps/app-tutorials/tutorial-fleet/).

If you want **Viam to host your web app**, see [Hosting](/build-apps/hosting/) and [Deploy a Viam application](/build-apps/hosting/deploy/).

If you are **coming from Foxglove, rosbridge, or a custom WebRTC stack**, read [How apps connect](/build-apps/concepts/how-apps-connect/) to understand Viam's connection model, then check the limits below.

## What build-apps does not cover

Some things that sound related live elsewhere or are not currently supported.

- **3D scene visualization inside a custom app.** Viam has a built-in 3D Scene tab on the machine page, but the SDKs do not expose 3D rendering primitives. If you need 3D in a custom app, bring your own library (three.js, react-three-fiber, Unity, Babylon) and plot Viam data into it.
- **Alarm aggregation for fleet dashboards.** Viam has alerts in the [monitor section](/monitor/alert/), but the SDKs do not provide alarm aggregation, deduplication, or severity ranking. Build that yourself.
- **Foxglove interop.** Viam does not support MCAP log import, Foxglove layout import, or embedding Foxglove panels.
- **Server-side code execution on Viam Applications.** Viam Applications serves your app's files from storage and does not execute any of your code server-side. No serverless functions, no backend endpoints, no API routes. Your app can be as dynamic and interactive as you want in the browser; Viam just does not run server-side logic on your behalf. For that, host a backend service yourself (the long-running service deployment shape above).
- **Version pinning and rollback for hosted apps.** Viam Applications always serves the latest uploaded version. To roll back, upload the previous code under a new version number.
- **Modules.** Code that runs _inside_ `viam-server` to extend it with new component types, services, or logic is a module, not an app. See [Build and deploy modules](/build-modules/) for that path.

## See also

- [Teleop workspaces](/monitor/teleop-workspaces/) for no-code custom control interfaces built from widgets
- [SDK reference](/dev/reference/sdks/) for TypeScript, Flutter, Python, Go, and C++ API documentation
- [Connectivity reference](/dev/reference/sdks/connectivity/) for sessions, WebRTC behavior, and local-network connections
- [Admin and access](/organization/) for creating API keys and managing organization access
