---
title: "Fine-grained permissions"
linkTitle: "Fine-grained permissions"
weight: 22
layout: "docs"
type: "docs"
no_list: true
description: "Define which API methods a user or API key can call on specific resources of a machine."
capabilities: ["org-management"]
diataxis: how-to
date: "2026-10-14"
---

[Roles](/organization/rbac/) decide who can reach a machine.
An access policy decides which API methods a user or API key with the **Member** role can call on which resources of that machine.
For example, you can let one API key read images from a camera and nothing else.

You define a policy in your machine's configuration.
Viam compiles it into rules that `viam-server` enforces on every request from a client.
A denied call fails with a `PermissionDenied` error, and `viam-server` logs an `unauthorized request` warning.

## Who a policy applies to

Owners and operators have machine-wide permission: they can call every method on every resource of the machine, and an access policy never limits them.
A member has no machine-wide permission.
A member can call only the methods that a grant allows, on the resources the grant names.

A member can't call anything on a machine until a grant allows it.
To let a user or API key make specific calls, give it the **Member** role, then name it in a grant.
A grant that names anyone who isn't a member is ignored.
See [Role-based access control](/organization/rbac/) for how roles are assigned.

## How a call is evaluated

`viam-server` checks every request from a client against the compiled rules.
Find the row that describes the caller and the call:

<!-- prettier-ignore -->
| Situation | Result |
| --------- | ------ |
| The caller is unauthenticated. | Denied. |
| The caller is listed in more than one entry. | Denied for every call. `viam-server` logs an error until you fix the configuration. |
| The caller has its own entry that grants the method on the resource. | Allowed. |
| The caller has its own entry that doesn't grant the method on the resource. | Denied. |
| The caller has no entry of its own. | Denied. |
| The method acts on the machine as a whole instead of one resource, such as `GetMachineStatus`. | Allowed only if a grant lists `_machine` as its resource. `_machine` is a placeholder for the machine itself, not a real resource. |
| An entry has an unknown subject `type`. | The entry is ignored, and `viam-server` logs a warning. |

A denied call fails with a `PermissionDenied` error, and `viam-server` logs an `unauthorized request` warning that names the method, the resource, and the caller.
If a change to the rules removes a caller's access, `viam-server` also closes that caller's open video streams.

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
| `subjects[].id` | The API key ID (not the key itself), or the user ID. The subject must hold the **Member** role for the grant to take effect. |
| `resources` | Resource names the methods may be called on, such as `cam1`. Use `_machine` for methods that don't address a single resource, such as `RobotService` methods. Use `*` for every resource. |
| `allowed_methods` | Fully qualified method names, such as `/viam.component.camera.v1.CameraService/GetImages`. Use `/viam.component.camera.v1.CameraService/*` for every method of one service, or `*` for every method. |
| `notes` | Optional free text explaining why the grant exists. Ignored when the policy is compiled. |

A wildcard must be a whole segment.
`cam*` and `/viam.component.camera.v1.CameraService/Get*` are rejected when you save.
A grant needs at least one subject and one resource, and a field the section doesn't define is rejected, so a typo fails at save instead of silently doing nothing.

Besides the methods a member's grants allow, every member can call a small baseline set of methods that `viam-server` needs to accept a connection.

### Find a method name

A method name is the proto package, the service, and the method, written `/<package>.<Service>/<Method>`.
Find them in the [Viam API package](https://github.com/viamrobotics/api/tree/main/proto/viam): open the component or service folder, then the resource's `.proto` file.

For example, `camera.proto` declares `package viam.component.camera.v1`, `service CameraService`, and `rpc GetImages`, which gives `/viam.component.camera.v1.CameraService/GetImages`.

#### Exceptions

Two sets of methods don't follow the component and service pattern:

- Machine-level methods use `viam.robot.v1.RobotService`, such as `/viam.robot.v1.RobotService/GetMachineStatus`. Their resource in a grant is `_machine`.
- Video streaming uses `proto.stream.v1.StreamService`.

### Machines with more than one part

Each part of a machine has its own configuration, and each part can have its own access policy.
A part's policy decides what that part's own `viam-server` allows.

Callers usually reach a sub-part's resources through the machine's main part, and the main part checks those calls against its own policy, not the sub-part's.
To let a member call a sub-part's resource through the main part, put the grant in the main part's access policy.
In that grant, name the resource by its plain name, such as `cam2`, or as `<sub-part>:<name>`.

<!-- TODO(verify, DOCS-4936): multi-part behavior is read from the activation PR's code (app#13426, `renderUserPermissions`), not tested. Test plan: "Cloud, multi-part" in the description of PR 5429, including whether a forwarded call is checked against the sub-part's policy. Ask the engineers before describing how the two policies interact. -->

<!-- TODO(verify, DOCS-4936): everything in this section is unverified until it runs on a flag-enabled org. Test plan: "Cloud, single part" in the description of PR 5429. The compiler (app#13423) and activation (app#13426) had not merged when this was drafted. Delete this comment when those items pass. -->

## Define permissions in a local configuration file

If you run `viam-server` from a local configuration file instead of managing the machine in the Viam app, you write the rules `viam-server` enforces directly, in the `auth` section of the file.
Requires `viam-server` v1.8.0 or later.

This format is for local configuration files.
If you manage the machine in the Viam app, define an [access policy](#define-an-access-policy) instead.
The app rejects a configuration that sets `auth.user_permissions` directly, because it generates that section from the access policy.

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
Leave out the `id` of a `default` entry.
Resources and methods work as in an access policy, except that `user_permissions` takes exact names only: it has no wildcards.

Roles are part of the Viam app, so they don't decide who can connect to a machine run from a local file.
The `auth.handlers` section does.
An `api-key` handler maps each API key ID to its key, and `keys` lists the IDs that may connect.
An `api-key-id` entry in `user_permissions` matches one of those IDs:

```json
{
  "auth": {
    "handlers": [
      {
        "type": "api-key",
        "config": {
          "<API-KEY-ID>": "<API-KEY>",
          "keys": ["<API-KEY-ID>"]
        }
      }
    ]
  }
}
```

[How a call is evaluated](#how-a-call-is-evaluated) applies here, with two additions.
A `default` entry covers any authenticated caller that has no entry of its own:

<!-- prettier-ignore -->
| Situation | Result |
| --------- | ------ |
| The `user_permissions` list is empty or absent. | Allowed. Anyone who can connect to the machine is unrestricted. |
| The caller has no entry, and the `default` entry grants the method on the resource. | Allowed. |
| The caller has no entry, and there is no `default` entry or it doesn't grant the call. | Denied. |

A caller's own entry replaces the `default` entry, it doesn't add to it.
The Viam app's access policy has no `default` entry.

<!-- TODO(verify, DOCS-4936): the handler sample comes from a code comment in RDK config.go and the ID match from authorization.go, neither tested live. Test plan: "Local config file" in the description of PR 5429. -->

<!-- TODO(DOCS-4936): content from the closed docs PR 5389 not carried over yet. (1) Where to find the IDs a grant needs: an API key ID from the API keys page, a user ID from the `user_id` field of `ListOrganizationMembers` (`GetUserIDByEmail` is Viam-staff only). (2) A caution that app pages such as the CONTROL tab connect as your user, so a member opening them needs grants for the methods those pages call; the `unauthorized request` logs list them. (3) The claim that calls from modules running on the machine aren't checked, which was never verified. -->
