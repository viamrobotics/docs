---
linkTitle: "Overview"
title: "Viam hosting"
weight: 1
layout: "docs"
type: "docs"
description: "Host a browser-based Viam app on Viam Applications with built-in authentication, credential injection, and a dedicated URL."
date: "2026-04-13"
---

Viam Applications is a hosting service for browser-based apps built with the TypeScript SDK or any frontend framework that produces HTML, JavaScript, and CSS. You upload your app's build output to the Viam registry, and Viam serves it at `{name}_{namespace}.viamapplications.com`.

Viam Applications is one of five [deployment options](/build-apps/overview/#deployment-options) for SDK-based apps. It works by serving your app's files (HTML, JavaScript, CSS) to a web browser. The browser downloads the files and runs the JavaScript locally. This means Viam Applications works for apps built with TypeScript, React, Vue, Svelte, or any other framework that compiles to files a browser can run. It does not work for Python, Go, or C++ apps, which run as processes on a server or workstation and need their own hosting; see the long-running service and local execution rows in the [deployment options table](/build-apps/overview/#deployment-options).

Viam Applications handles three things that you would otherwise build yourself:

- **Authentication.** Users log in through Viam's OAuth flow. You do not implement a login page, manage tokens, or integrate an identity provider.
- **Credential delivery.** After login, Viam stores an authentication credential in a browser cookie that your app reads to connect to machines. For single-machine apps, this is a machine-scoped API key. For multi-machine apps, this is the user's OAuth access token. The cookie is scoped to the app's domain and set with `SameSite=Strict`.
- **Hosting and TLS.** Viam serves your app over HTTPS at a dedicated URL. You do not configure a web server, provision a certificate, or manage a CDN.

## Two application types

Viam Applications supports two types, declared in your `meta.json`:

**Single-machine.** The app operates on one machine at a time. After login, Viam presents a machine picker (optionally filtered by fragment) and delivers a machine-scoped API key and hostname to the browser. Your app reads the credential from the cookie and passes it to the SDK. Use this when your app is a control interface or dashboard for a specific device.

**Multi-machine.** The app can access any machine the logged-in user has permissions for. After login, Viam delivers the user's OAuth access token to the browser. Your app reads the token from the cookie and passes it to the SDK to enumerate machines across the organization and connect to each one. Use this when your app is a fleet dashboard or a multi-device management tool.

## What's in this section

- [Deploy a Viam application](/build-apps/hosting/deploy/) walks through packaging your app, configuring `meta.json`, and uploading to the registry.
- [meta.json applications schema](/build-apps/hosting/meta-json-reference/) is the field-by-field reference for the `applications` array that declares your app's type, entrypoint, fragment filters, and branding.
- [Hosting platform reference](/build-apps/hosting/hosting-reference/) documents the URL pattern, cookie structure, caching behavior, and limits.

## Constraints

- Viam Applications hosts browser-based apps only. It serves your files from storage and does not execute any server-side code: no serverless functions, no backend endpoints, no API routes.
- Viam always serves the latest uploaded version. There is no version selection or rollback UI; to roll back, upload the previous code under a new version number.
- Cookies are required. Browsers with cookies disabled cannot use Viam Applications.
