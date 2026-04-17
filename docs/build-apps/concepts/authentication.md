---
linkTitle: "Authentication"
title: "Authenticating Viam client apps"
weight: 20
layout: "docs"
type: "docs"
description: "The credential types a Viam client app uses and when to use each. Covers API keys, access tokens, and hosted-app credential injection."
date: "2026-04-10"
---

A Viam client application proves its identity to the machine or to the Viam cloud through a credential. The SDK supports two credential types: API keys for service-identity access and access tokens for user-identity access. Hosted Viam Applications inject credentials into the browser automatically through cookies.

This page uses TypeScript SDK names for the specific APIs. The Flutter SDK supports the same credential types through `RobotClientOptions.withApiKey` and `Viam.withAccessToken`; see [Flutter setup](/build-apps/setup/flutter/).

## API keys

An API key is the default credential for a client app. You create the key in the Viam app, scope it to what it should be allowed to access, and pass it to the SDK at connection time.

An API key has two pieces: an **ID** (the `authEntity` field in the SDK) and a **secret** (the `payload` field). Both are required for every connection. The secret is shown only at creation time; if you lose it, rotate the key to generate a new secret.

```typescript
const machine = await VIAM.createRobotClient({
  host: "my-robot-main.xxxx.viam.cloud",
  credentials: {
    type: "api-key",
    authEntity: process.env.API_KEY_ID,
    payload: process.env.API_KEY,
  },
  signalingAddress: "https://app.viam.com:443",
});
```

API keys have three possible scopes:

| Scope        | Access                           | When to use                                                                                               |
| ------------ | -------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Machine      | One machine                      | Your app talks to a specific machine you control, and you want the smallest blast radius if the key leaks |
| Location     | All machines in a location       | Your app needs to talk to several machines that share a location, such as a warehouse deployment          |
| Organization | All machines in the organization | Your app needs broad fleet access, such as a fleet-management dashboard or a data-querying service        |

Create and manage API keys in [Admin and access](/organization/access/).

## Access tokens

An access token represents a user, not a service. Where an API key is one identity that never changes, an access token is the identity of whoever is currently logged in.

Hosted Viam Applications create access tokens through the Viam OAuth flow when a user logs in. Your app code reads the token from a browser cookie and passes it to `createViamClient` to make requests scoped to what that user is allowed to see. There is no API for creating access tokens yourself; they only come from the OAuth flow.

Access tokens are useful when the same app shows different data to different users, and they are the only credential type you use in a hosted Viam Application.

## Hosted Viam Applications: credential injection

When you deploy a web app to Viam Applications, the Viam platform handles authentication. The behavior depends on the application type you declared in `meta.json`.

**Single-machine application.** Users log into your app through Viam's OAuth flow. Viam selects a machine (either the one specified in the URL or one picked through the fragment-filtered machine picker) and writes machine-specific credentials into a browser cookie: the API key, the API key ID, and the machine hostname. Your app code reads the cookie and passes the credentials to `createRobotClient`.

**Multi-machine application.** Users log into your app the same way. Viam writes a user access token into a browser cookie. Your app code reads the cookie and passes the token to `createViamClient`, then uses the resulting `AppClient` to enumerate the machines the user has access to and connect to each one.

In both cases, the Viam Applications platform manages the cookie lifecycle: login, token refresh, and logout all happen without your app code touching the credential directly.

See [Deploy a Viam application](/build-apps/hosting/deploy/) for the deployment workflow and [the hosting platform reference](/build-apps/hosting/hosting-reference/) for the cookie format.

## Where to put credentials in self-hosted apps

For apps you host yourself, not on Viam Applications:

- Store API keys in environment variables, not in source code.
- In development, use a `.env` file and add `.env` to `.gitignore`.
- In production, use your platform's secret management: Vercel environment variables, AWS Secrets Manager, Kubernetes secrets, or similar.
- Never commit an API key to a public repository. If you do, rotate the key immediately.

For apps on Viam Applications, you do not store credentials; Viam injects them through cookies at runtime.

## Robot secrets

Robot secrets are a legacy credential type from earlier versions of Viam. They still work for backward compatibility. Use API keys instead in new apps.
