---
linkTitle: "Hosting reference"
title: "Viam Applications hosting platform reference"
weight: 30
layout: "docs"
type: "docs"
description: "URL patterns, cookie structure, caching behavior, and limits for the Viam Applications hosting platform."
date: "2026-04-10"
---

Reference for the runtime behavior of the Viam Applications hosting platform. For the deployment workflow, see [Deploy a Viam application](./deploy/). For the `meta.json` schema that configures the application, see [the meta.json applications reference](./meta-json-reference/).

## URL pattern

Every Viam Application is served at:

```text
https://{name}_{namespace}.viamapplications.com
```

- `{name}` is the `name` field from the application's `meta.json` entry.
- `{namespace}` is the public namespace of the organization that owns the module.

Example: an application named `dashboard` in the `acme` namespace is served at `https://dashboard_acme.viamapplications.com`.

Internal Viam environments use `viamapps.dev` instead of `viamapplications.com`, but the `{name}_{namespace}` pattern is the same.

## Authentication flow

All Viam Applications require the user to be logged into Viam. The first visit to an application's URL redirects through Viam's OAuth flow; after login, the user lands on the application with credentials in browser cookies.

For single-machine applications, the flow includes a machine selection step if the application has `fragmentIds` that match more than one machine in the user's fleet, or if the user accesses the base URL without a specific machine in the path.

## Cookies

Viam injects credentials into browser cookies after login. Your application code reads the cookies and passes the credentials to the SDK.

### Single-machine applications

A single-machine application receives one cookie per machine the user has selected. The cookie name is the machine ID, and its value is a JSON object with the following shape:

```json
{
  "apiKey": {
    "id": "api-key-id",
    "key": "api-key-secret"
  },
  "id": "api-key-id",
  "key": "api-key-secret",
  "credentials": {
    "type": "api-key",
    "payload": "api-key-secret",
    "authEntity": "api-key-id"
  },
  "hostname": "machine-main.xxxx.viam.cloud",
  "machineId": "machine-uuid",
  "timestamp": 1712620800
}
```

The `credentials` object is structured for direct use with `createRobotClient`:

```ts
import * as VIAM from "@viamrobotics/sdk";
import Cookies from "js-cookie";

const pathParts = window.location.pathname.split("/");
const machineId = pathParts[2]; // from URL like /machine/{id}/...

const cookieValue = JSON.parse(Cookies.get(machineId)!);

const machine = await VIAM.createRobotClient({
  host: cookieValue.hostname,
  credentials: cookieValue.credentials,
  signalingAddress: "https://app.viam.com:443",
});
```

The `id` and `key` top-level fields are duplicates of `apiKey.id` and `apiKey.key` retained for backwards compatibility. New code should use either `apiKey` or `credentials` directly.

### Multi-machine applications

A multi-machine application receives one cookie named `userToken` containing the logged-in user's OAuth access token. The cookie value is a JSON object representing the full `oauth2.Token`:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "refresh_token": "...",
  "expiry": "2026-04-10T12:00:00Z"
}
```

Read the `access_token` field and pass it to `createViamClient` as an access-token credential:

```ts
import * as VIAM from "@viamrobotics/sdk";
import Cookies from "js-cookie";

const userTokenRaw = Cookies.get("userToken")!;
const { access_token } = JSON.parse(userTokenRaw);

const client = await VIAM.createViamClient({
  credentials: {
    type: "access-token",
    payload: access_token,
  },
});
```

Use the resulting `ViamClient` to enumerate and connect to specific machines. See [Connect to the Viam cloud](../tasks/connect-to-cloud/).

## Cookie lifecycle

Machine cookies in single-machine applications have a 30-day maximum age. The platform refreshes them automatically when the user visits the application after 75% of the maximum age has elapsed (approximately 22.5 days). Users who return within the refresh window stay logged in without re-authenticating.

User tokens in multi-machine applications follow the underlying OAuth token lifecycle: the platform refreshes access tokens through the standard OAuth refresh flow without user interaction. The `userToken` cookie is updated with the new access token when it is refreshed.

## Caching

The hosting platform caches your app's files with the following `Cache-Control` behavior:

| Content type                                     | Cache-Control header                  | Behavior                                                                    |
| ------------------------------------------------ | ------------------------------------- | --------------------------------------------------------------------------- |
| HTML files (entrypoint and any `.html`)          | `no-cache, no-store, must-revalidate` | Never cached in browser or CDN. Every request hits the latest version.      |
| All other static assets (CSS, JS, images, fonts) | `private, max-age=86400`              | Cached in the user's browser for 24 hours. Not cached in shared CDN layers. |

The server also maintains a short-lived in-memory cache (approximately 5 minutes) of each application's blob path and entrypoint lookup, to avoid hitting the module registry database on every request. This cache invalidates automatically within a few minutes of an upload, so new versions go live within minutes of `viam module upload` completing.

If you see stale JavaScript or CSS after an upload, the cause is almost always your browser cache, not the platform cache. Hard-reload the page (Ctrl+Shift+R or Cmd+Shift+R) or open the application in an incognito window.

## Storage and delivery

Uploaded application tarballs are extracted to Google Cloud Storage under a path of the form `{namespace}/{app-name}/{version}/`. The hosting server proxies user requests to GCS through an authenticated reverse proxy. The proxy:

- Strips the `/machine/{machineId}/` prefix from the URL before forwarding, for single-machine applications.
- Injects a `<base href>` tag into HTML responses so relative asset paths resolve correctly under the prefix-stripped path.
- Sets the cache headers described above.
- Sets machine or user cookies on the response where applicable.

Application authors do not interact with GCS directly; all uploads go through `viam module upload`.

## Versioning

Viam Applications always serve the latest uploaded version for a given `name` + namespace combination. There is no URL parameter, header, or manifest field for selecting a specific version.

To release a new version, upload with a higher semver `--version`. The registry rejects duplicate version numbers.

To roll back, upload the previous code under a new, higher version number. There is no direct "revert" operation.

## Limits

- **Public visibility required.** The module hosting the application must have `visibility: public` in `meta.json`. Private modules cannot host applications.
- **Static files only.** Viam Applications does not execute server-side code. No serverless functions, no backend endpoints, no API routes. The hosted content is HTML, JS, CSS, images, and other static assets only. Your browser-side application logic can be arbitrarily dynamic.
- **Cookies required.** Users whose browsers block cookies cannot log into Viam Applications.
- **One application per URL.** Each `name`+namespace combination serves a single application. Multiple applications with the same name in the same namespace are not allowed.

## Related

- [Deploy a Viam application](./deploy/) for the package-and-upload workflow
- [meta.json applications schema](./meta-json-reference/) for the application configuration
- [Authentication](../concepts/authentication/) for the credential injection model
