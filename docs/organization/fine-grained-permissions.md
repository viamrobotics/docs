---
title: "Fine-grained permissions"
linkTitle: "Fine-grained permissions"
weight: 22
layout: "docs"
type: "docs"
no_list: true
draft: true
description: "Limit which API methods a user or API key can call on specific resources of a machine."
capabilities: ["org-management"]
diataxis: how-to
date: "2026-10-14"
---

[Roles](/organization/rbac/) decide who can reach a machine.
An access policy decides which API methods a user or API key can call on which resources of that machine.
For example, you can let one API key read images from a camera and nothing else.

You define a policy in your machine's configuration.
Viam compiles it into rules that `viam-server` enforces on every request from a client.
A denied call fails with a `PermissionDenied` error, and `viam-server` logs an `unauthorized request` warning.

## How a call is evaluated

`viam-server` checks every request from a client against the compiled rules.
Find the row that describes the caller and the call:

<!-- prettier-ignore -->
| Situation | Result |
| --------- | ------ |
| The rules list is empty or absent. | Allowed. Every caller is unrestricted. |
| The caller is unauthenticated, and the list has any entry. | Denied. |
| The caller is listed in more than one entry. | Denied for every call. `viam-server` logs an error until you fix the configuration. |
| The caller has its own entry that grants the method on the resource. | Allowed. |
| The caller has its own entry that doesn't grant the method on the resource. | Denied. A caller's own entry replaces the `default` entry, it doesn't add to it. |
| The caller has no entry, and a `default` entry grants the method on the resource. | Allowed. |
| The caller has no entry, and there is no `default` entry or it doesn't grant the call. | Denied. |
| The method addresses no named resource, such as a `RobotService` method. | Only grants on `_machine` match. |
| An entry has an unknown subject `type`. | The entry is ignored, and `viam-server` logs a warning. |

A denied call fails with a `PermissionDenied` error, and `viam-server` logs an `unauthorized request` warning that names the method, the resource, and the caller.
If a change to the rules removes a caller's access, `viam-server` also closes that caller's open video streams.

Only local configuration files can contain a `default` entry.
An access policy in the Viam app names users and API keys only.

## Define an access policy

Add an `access_policy` section at the top level of the machine's JSON configuration, next to `components` and `services`.
It holds a list of grants.
Each grant gives a set of subjects permission to call a set of methods on a set of resources:

```json
{
  "access_policy": {
    "grants": [
      {
        "subjects": [{ "type": "api-key-id", "id": "<API-KEY-ID>" }],
        "resources": ["cam1"],
        "allowed_methods": [
          "/viam.component.camera.v1.CameraService/GetImages"
        ],
        "notes": "Image viewer key reads cam1 only."
      }
    ]
  }
}
```

<!-- prettier-ignore -->
| Field | Description |
| ----- | ----------- |
| `subjects[].type` | `api-key-id` for an API key, or `app-user-id` for a Viam user. |
| `subjects[].id` | The API key ID (not the key itself), or the user ID. |
| `resources` | Resource names the methods may be called on, such as `cam1`. Use `_machine` for methods that don't address a single resource, such as `RobotService` methods. Use `*` for every resource. |
| `allowed_methods` | Fully qualified method names, such as `/viam.component.camera.v1.CameraService/GetImages`. Use `/viam.component.camera.v1.CameraService/*` for every method of one service, or `*` for every method. |
| `notes` | Optional free text explaining why the grant exists. Ignored when the policy is compiled. |

A wildcard must be a whole segment.
`cam*` and `/viam.component.camera.v1.CameraService/Get*` are rejected when you save.
A grant needs at least one subject and one resource, and a field the section doesn't define is rejected, so a typo fails at save instead of silently doing nothing.

Don't set `auth.user_permissions` yourself.
Viam generates it from `access_policy`, and the app rejects a configuration that includes it.

<!-- TODO(verify, DOCS-4936): that the app never compiles a default entry from an access policy (the table's last note), behavior when a caller has no matching grant, owner and operator exemption, how grants from fragments combine, and whether resource names are checked at save. Confirm against APP-17820 and a flag-enabled org before removing draft: true. -->

## Define permissions in a local configuration file

If you run `viam-server` from a local configuration file instead of managing the machine in the Viam app, you write the rules `viam-server` enforces directly, in the `auth` section of the file.
Requires `viam-server` v1.8.0 or later.

Add a `user_permissions` list.
Each entry has a `user` and a list of `permissions`:

```json
{
  "auth": {
    "user_permissions": [
      {
        "user": { "type": "api-key-id", "id": "<API-KEY-ID>" },
        "permissions": [
          {
            "resources": ["cam1"],
            "allowed_methods": [
              "/viam.component.camera.v1.CameraService/GetImages"
            ]
          }
        ]
      },
      {
        "user": { "type": "default" },
        "permissions": [
          {
            "resources": ["_machine"],
            "allowed_methods": ["/viam.robot.v1.RobotService/GetMachineStatus"]
          }
        ]
      }
    ]
  }
}
```

The `user` types are `api-key-id`, `app-user-id`, and `default`.
Use `default` for any authenticated caller that has no entry of its own, and leave out its `id`.
Resources and methods work as in an access policy, except that `user_permissions` takes exact names only: it has no wildcards.

`viam-server` applies the list as follows:

- If `user_permissions` is empty or absent, every caller is unrestricted.
- Once it has any entry, a caller can call only the methods its own entry grants.
  A caller with no entry gets the `default` entry's permissions, or none if there is no `default` entry.
- Unauthenticated connections are fully restricted.
- If a user appears in more than one entry, `viam-server` logs an error and fully restricts that user until you fix the configuration.
  An entry with an unknown `type` is ignored with a warning.
- Calls that address no named resource, such as `RobotService` methods, match only grants on `_machine`.

<!-- TODO(verify, DOCS-4936): how a caller authenticates against a local config so its API key ID matches an entry, which connection-plumbing methods are exempt from checks, and the no-wildcard claim against a shipped release. -->
