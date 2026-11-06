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

## Who a policy applies to

Owners and operators have machine-wide permission: they can call every method on every resource of the machine, and an access policy never limits them.
A member has no machine-wide permission.
A member can call only the methods that a grant allows, on the resources the grant names, plus the methods needed to connect if the grant turns on basic connection, described below.

To let a user or API key make specific calls, give it the **Member** role, then name it in a grant.
A grant that names anyone who isn't a member is ignored.
A policy has no effect until the machine has a member: a machine with no members gets no rules from the app, so no one is restricted.
See [Role-based access control](/organization/rbac/) for how roles are assigned.

## How a call is evaluated

`viam-server` checks every request from a client against the compiled rules.
Find the row that describes the caller and the call:

<!-- prettier-ignore -->
| Situation | Result |
| --------- | ------ |
| The caller is unauthenticated. | Denied. |
| The caller has its own entry that grants the method on the resource. | Allowed. |
| The caller has its own entry that doesn't grant the method on the resource. | Denied. |
| The caller has no entry of its own. | Denied. |
| The method acts on the machine as a whole instead of one resource, such as `StopAll`. | Allowed only if a grant lists `_machine` as its resource. `_machine` is a placeholder for the machine itself, not a real resource. |

A denied call fails with a `PermissionDenied` error, and `viam-server` logs an `unauthorized request` warning that names the method, the resource, and the caller.
If a change to the rules removes a caller's access, `viam-server` also closes that caller's open video streams.
`viam-server` always allows the calls that handle authentication, WebRTC signaling, and gRPC reflection, whatever the rules say.

## Define an access policy

{{< alert title="Caution" color="caution" >}}
Access policies need `viam-server` v1.14.0 or later.
On an older version, the app sends the machine no rules, so nothing is enforced and a Member API key has full access to the machine.
The app warns you when a part runs an older version.
Upgrade `viam-server` before you rely on a policy.
{{< /alert >}}

Add an `access_policy` section at the top level of the machine's JSON configuration, next to `components` and `services`.
It holds a list of grants.
Each grant gives a set of subjects permission to call a set of methods on a set of resources:

```json
{
  "access_policy": {
    "grants": [
      {
        "name": "Image viewer",
        "subjects": [{ "type": "api-key-id", "id": "<API-KEY-ID>" }],
        "basic_connection": true,
        "permissions": [
          {
            "resources": ["cam1"],
            "allowed_methods": [
              "/viam.component.camera.v1.CameraService/GetImages"
            ]
          }
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
| `name` | Optional label for the grant. A name must be unique within the policy. |
| `subjects[].type` | `api-key-id` for an API key, or `app-user-id` for a Viam user. |
| `subjects[].id` | The API key ID (not the key itself), or the user ID. The subject must hold the **Member** role for the grant to take effect. |
| `basic_connection` | Set to `true` to give the grant's subjects the methods a client needs to connect to the machine and read its status. Without it, an SDK can't connect. |
| `permissions[].resources` | Resource names the methods may be called on, such as `cam1`. Use `_machine` for methods that don't address a single resource, such as `RobotService` methods. Use `*` for every resource. |
| `permissions[].allowed_methods` | Fully qualified method names, such as `/viam.component.camera.v1.CameraService/GetImages`. Use `/viam.component.camera.v1.CameraService/*` for every method of one service, or `*` for every method. |
| `notes` | Optional free text explaining why the grant exists. Ignored when the policy is compiled. |

A grant can have several `permissions`, each with its own resources and methods.
A resource, `*`, or `_machine` can appear in only one permission of a grant.
A wildcard must be a whole segment: `cam*` and `/viam.component.camera.v1.CameraService/Get*` are rejected when you save.
A field the section doesn't define is rejected too, so a typo fails at save instead of silently doing nothing.
A grant with no subjects or no permissions saves, but grants nothing.

Set `basic_connection` to `true` on a grant for every member, or the member can't connect.
A member named in no grant can't call anything.
Resource names aren't checked when you save, so a mistyped name saves and grants nothing.

If a member's SDK can't connect and reports only a generic connection error, check the machine's logs for `unauthorized request` warnings.
The warning names the method and the key.
The usual cause is a member in no grant, or a grant without basic connection.

### Cameras

Streaming video from a camera uses methods on the stream service, not the camera service.
When a grant allows methods on a camera, Viam also gives its subjects the stream methods that camera needs, so you don't grant them: `AddStream`, `RemoveStream`, `GetStreamOptions`, and `SetStreamOptions` on the camera, and `ListStreams` on `_machine`.
That means a member who can read images from a camera can also add and remove that camera's streams and change their options.

A vision service can read from every camera it's configured with.
Granting a member methods on a vision service can expose camera images that no camera grant allows, for example through `CaptureAllFromCamera`, and a `*` method grant includes it.

### Find a method name

A method name is the proto package, the service, and the method, written `/<package>.<Service>/<Method>`.
Find them in the [Viam API package](https://github.com/viamrobotics/api/tree/main/proto/viam): open the component or service folder, then the resource's `.proto` file.

For example, `camera.proto` declares `package viam.component.camera.v1`, `service CameraService`, and `rpc GetImages`, which gives `/viam.component.camera.v1.CameraService/GetImages`.

Copy the `package` line exactly as written, because it doesn't always match the folder path.
For example, `stream.proto` is in the `viam` folder but declares `package proto.stream.v1`.

### Machines with more than one part

Each part of a machine has its own configuration, and each part can have its own access policy.
A part's policy decides what that part's own `viam-server` allows.

Callers usually reach a sub-part's resources through the machine's main part, and the main part checks those calls against its own policy, not the sub-part's.
A sub-part's policy applies only to calls made directly to the sub-part.

To let a member call a sub-part's resource through the main part, put the grant in the main part's access policy and name the resource by its plain name, such as `cam2`.
Don't use the `<sub-part>:<name>` form for a sub-part: it saves, and the editor warns that it can't find the resource, but it never matches a call.
The main part's policy editor doesn't list a sub-part's resources, so add that grant in JSON mode.
Because a sub-part's policy doesn't limit what the main part forwards, control access to a sub-part's resources in the main part's policy.

<!-- TODO(verify, DOCS-4936): the multi-part behavior above was observed on one test machine on 2026-11-06 (viam-server v1.15.0, a main part and a sub-part): a member with a grant only in the main part's policy reached the sub-part's camera through the main part and could not connect directly to the sub-part. A grant on `<sub-part>:<name>` also saved and compiled but matched nothing, since the main part exposes the sub-part's resources by plain name. Still open: two parts with the same resource name, a remote configured by hand with a prefix, and a fragment imported with a prefix. Test plan: "Cloud, multi-part" in the description of PR 5429. -->

<!-- TODO(verify, DOCS-4936): everything in this section is unverified until it runs on a flag-enabled org (the flag is on in the viam-dev org). Test plan: "Cloud, single part" in the description of PR 5429. The schema is read from the app's data/access_policy.go on main as of 2026-11-06. Version behavior, from the app source (access_policy_render.go) and seen in the app UI on 2026-11-06: a part below viam-server v1.14.0, or with an unknown version, is sent no rules and stays unrestricted, and the Create API key form warns that a Member key then has full access until the part is upgraded. The Caution at the top of this section states that minimum and warning; still unchecked is that a v1.14.0 release candidate counts as too old. Delete this comment when the items pass. -->

## Define permissions in a local configuration file

If you run `viam-server` from a local configuration file instead of managing the machine in the Viam app, you write the rules `viam-server` enforces directly, in the `auth` section of the file.
Requires `viam-server` v1.8.0 or later.

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
          },
          {
            "resources": ["_machine"],
            "allowed_methods": [
              "/viam.robot.v1.RobotService/ResourceNames",
              "/viam.robot.v1.RobotService/ResourceRPCSubtypes",
              "/viam.robot.v1.RobotService/StartSession",
              "/viam.robot.v1.RobotService/SendSessionHeartbeat",
              "/viam.robot.v1.RobotService/GetMachineStatus",
              "/proto.stream.v1.StreamService/ListStreams"
            ]
          }
        ]
      },
      {
        "user": { "type": "default" },
        "permissions": [
          {
            "resources": ["_machine"],
            "allowed_methods": [
              "/viam.robot.v1.RobotService/ResourceNames",
              "/viam.robot.v1.RobotService/ResourceRPCSubtypes",
              "/viam.robot.v1.RobotService/StartSession",
              "/viam.robot.v1.RobotService/SendSessionHeartbeat",
              "/viam.robot.v1.RobotService/GetMachineStatus",
              "/proto.stream.v1.StreamService/ListStreams"
            ]
          }
        ]
      }
    ]
  }
}
```

The `user` types are `api-key-id`, `app-user-id`, and `default`.
Leave out the `id` of a `default` entry.

To give the same permissions to several users, list them in `users` instead of `user`.
If an entry has both, only `users` applies.
A user can appear in only one entry, counting both fields.
`users` needs `viam-server` v1.14.0 or later: an older version skips an entry that has only `users`.

Resources and methods work as in an access policy, except that `user_permissions` takes exact names only: it has no wildcards.
See [Find a method name](#find-a-method-name) for how to look up exact names.

The `_machine` permissions in the example list the six methods a client needs to connect to the machine and read its status.
The SDKs call `ResourceNames`, `ResourceRPCSubtypes`, `StartSession`, and `SendSessionHeartbeat` automatically when they connect.
The Viam app adds all six for members, but a local file doesn't, so include them in every entry whose caller needs to connect.

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

[How a call is evaluated](#how-a-call-is-evaluated) applies here, with these additions.
A `default` entry covers any authenticated caller that has no entry of its own:

<!-- prettier-ignore -->
| Situation | Result |
| --------- | ------ |
| The `user_permissions` list is empty or absent. | Allowed. Anyone who can connect to the machine is unrestricted. |
| The caller is listed in more than one entry. | Denied for every call. `viam-server` logs an error until you fix the configuration. |
| An entry has an unknown `user` type. | The entry is ignored, and `viam-server` logs a warning. |
| The caller has no entry, and the `default` entry grants the method on the resource. | Allowed. |
| The caller has no entry, and there is no `default` entry or it doesn't grant the call. | Denied. |

A caller's own entry replaces the `default` entry, it doesn't add to it.
The Viam app's access policy has no `default` entry.

<!-- TODO(verify, DOCS-4936): the handler sample comes from a code comment in RDK config.go and the ID match from authorization.go, neither tested live, and neither is the claim that an entry without the six connection methods stops an SDK from connecting. Test plan: "Local config file" in the description of PR 5429. -->

<!-- TODO(DOCS-4936): content from the closed docs PR 5389 not carried over yet. (1) Where to find the IDs a grant needs: an API key ID from the API keys page, a user ID from the `user_id` field of `ListOrganizationMembers` (`GetUserIDByEmail` is Viam-staff only). (2) A caution that app pages such as the CONTROL tab connect as your user, so a member opening them needs grants for the methods those pages call; the `unauthorized request` logs list them. (3) The claim that calls from modules running on the machine aren't checked, which was never verified. -->
