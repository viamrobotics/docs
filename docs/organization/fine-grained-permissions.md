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

<!-- TODO(verify, DOCS-4936): behavior when a caller has no matching grant, owner and operator exemption, how grants from fragments combine, and whether resource names are checked at save. Confirm against APP-17820 and a flag-enabled org before removing draft: true. -->
