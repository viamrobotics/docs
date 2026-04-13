---
linkTitle: "Deploy a Viam application"
title: "Deploy a Viam application"
weight: 10
layout: "docs"
type: "docs"
description: "Package your app with meta.json and upload it to Viam Applications for hosting with built-in authentication and credential injection."
date: "2026-04-10"
---

Package your client app and upload it to Viam Applications, Viam's hosting service for web apps. Once uploaded, your app is served at `{appname}_{namespace}.viamapplications.com` with authentication and machine-credential injection handled by the platform.

Viam Applications are distributed through the Viam module registry, which is why the CLI commands live under `viam module`. This has nothing to do with building server-side modules; the `module` in the command name is an artifact of the registry plumbing.

## Prerequisites

- A built client app. Any bundler output that produces HTML, JavaScript, and CSS works: a Vite `dist/` directory, a Create React App `build/` directory, a Flutter web build, and so on. See [TypeScript setup](../setup/typescript/) for a minimal Vite starting point.
- The [Viam CLI](/cli/) installed and authenticated (`viam login`).
- A public namespace for your organization. Set this in the [organization settings](/organization/) if you have not already. Viam Applications require a public namespace because the app's URL uses it.

## Create the module registry entry

First-time setup only. Each Viam Application is represented as a module in the Viam registry. Create the registry entry:

```sh {class="command-line" data-prompt="$"}
viam module create --name my-app --public-namespace your-namespace
```

This creates a `meta.json` in your current directory with a `module_id` of `your-namespace:my-app` and `visibility: private`. You will change the visibility and add the `applications` field in the next step.

## Configure meta.json

Edit `meta.json` to declare the application. The generated file needs two changes:

1. Change `visibility` from `private` to `public`. Viam Applications require public visibility.
2. Add an `applications` array describing the app.

A complete `meta.json` for a single-machine browser app:

```json
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "your-namespace:my-app",
  "visibility": "public",
  "applications": [
    {
      "name": "my-app",
      "type": "single_machine",
      "entrypoint": "dist/index.html"
    }
  ]
}
```

Key fields in the `applications` entry:

- `name` — appears in the URL as `{name}_{namespace}.viamapplications.com`. Lowercase alphanumeric and hyphens only. Must be unique within your namespace.
- `type` — `single_machine` or `multi_machine`. Single-machine apps pick one machine and inject that machine's credentials. Multi-machine apps inject a user access token and let the app enumerate machines.
- `entrypoint` — path to the HTML entry point, relative to the uploaded archive's root. For a Vite build, this is typically `dist/index.html`.

See [the meta.json applications reference](./meta-json-reference/) for all available fields, including `fragmentIds`, `logoPath`, and `customizations`.

## Build your app

Run your bundler to produce the static output. For Vite:

```sh {class="command-line" data-prompt="$"}
npm run build
```

Confirm the output directory contains an `index.html` and all its asset files. The path you put in `entrypoint` must match what the build produces.

## Package and upload

Create a tarball of everything you want to serve, including `meta.json`:

```sh {class="command-line" data-prompt="$"}
tar -czvf module.tar.gz meta.json dist/
```

Adjust the tar command to include whatever directories your build produced. The `meta.json` must be at the root of the archive.

Upload to the registry:

```sh {class="command-line" data-prompt="$"}
viam module upload --upload module.tar.gz --platform any --version 0.0.1
```

Use `--platform any` for Viam Applications. Static web apps are platform-independent; the `any` platform tag tells the registry to serve the same archive to every user regardless of operating system.

The `--version` flag is required and must be a semver string. You cannot reuse a version number, so each upload needs a higher version than the last.

## Verify the deployment

Your app is now live at:

```text
https://{name}_{namespace}.viamapplications.com
```

Replace `{name}` with the `name` field from your `meta.json` and `{namespace}` with your organization's public namespace. Open the URL in a browser. You should see:

1. A redirect to the Viam login flow.
2. After login, for a single-machine app: the machine picker (if the app has no fragment filter) or the app itself (if the URL targets a specific machine).
3. For a multi-machine app: your app loads directly with the user access token already in cookies.

If the app does not load, check:

- **The `applications` array in the uploaded `meta.json`**. If the registry sees no applications, no URL is assigned. Re-upload with the correct field after fixing `meta.json`.
- **The `entrypoint` path.** The path is relative to the archive root. If `meta.json` is at the root and your HTML is at `dist/index.html`, the entrypoint should be `dist/index.html`, not `/dist/index.html` or `index.html`.
- **The namespace.** The URL uses your organization's public namespace, not the organization name or ID. Confirm the public namespace in the [organization settings](/organization/).

## Release updates

To release a new version of your app, rebuild and re-upload with a higher version number:

```sh {class="command-line" data-prompt="$"}
npm run build
tar -czvf module.tar.gz meta.json dist/
viam module upload --upload module.tar.gz --platform any --version 0.0.2
```

Viam Applications always serve the latest uploaded version. There is no staging step and no version selection in the URL.

To roll back, upload the previous code under a new, higher version number. The registry rejects duplicate version numbers, so you cannot reuse an older one.

## Next

- [meta.json applications reference](./meta-json-reference/) for the full schema
- [Hosting platform reference](./hosting-reference/) for URL patterns, cookie structure, caching behavior, and limits
- [Test against a local machine](../tasks/test-locally/) for iterating on your app before each upload
