---
linkTitle: "Set up custom push notifications"
title: "Set up custom push notifications"
weight: 22
layout: "docs"
type: "docs"
description: "Route trigger push notifications to your own mobile app instead of the Viam mobile app."
---

By default, push notification triggers deliver to the Viam mobile app (`com.viam.viammobile`).
To route notifications to a custom mobile app instead, you upload your app's Firebase credentials to Viam, register each user device, import an authorizing fragment on the machine, and reference your custom application ID in the trigger config.

This page covers the end-to-end setup.
For the `notifications` config schema, see [Trigger configuration](/reference/triggers/).

## When to use a custom app

Use a custom application ID when you ship your own mobile app to operators (white-label or embedded experience), want a separate notification stream from `com.viam.viammobile`, or want notifications to appear in an app branded for your fleet.

If the Viam mobile app meets your needs, set `application` to `com.viam.viammobile` in the trigger config and skip this page.

## Prerequisites

- A Firebase project with Firebase Cloud Messaging (FCM) enabled.
- A mobile app (Flutter, native iOS or Android, or web) that you build and distribute.
- Organization owner access on the Viam organization that will own the trigger.
- The Viam CLI installed and authenticated. See [`viam login`](/cli/reference/#login).

## 1. Register your Firebase service account with Viam

Viam mints OAuth2 access tokens for FCM on your behalf using your Firebase service account credentials.

### Download the service account JSON

1. Open the [Firebase Console](https://console.firebase.google.com/) and select your project.
1. Click **Settings**, then click the **Service accounts** tab.
1. Click **Generate New Private Key**, then click **Generate Key** to confirm.
1. Save the downloaded JSON file. Treat it like a password.

The file you need is the Firebase Admin SDK service account JSON, not `google-services.json` or `GoogleService-Info.plist`.
Those are client-side configs and will not work here.

### Upload the credentials to Viam

```sh {class="command-line" data-prompt="$"}
viam organizations firebase-config set \
  --org-id <your-org-id> \
  --app-id <your-app-id> \
  --firebase-config-path ./service-account.json
```

- `--app-id` is your mobile app's package name (for example `com.example.myapp`).
  It must match the package name your client app uses to register devices.
- The JSON is stored encrypted in Viam's database and is never returned by any read API.

To confirm the upload, read back the registered application ID:

```sh {class="command-line" data-prompt="$"}
viam organizations firebase-config read --org-id <your-org-id>
```

### Constraints

- One Firebase config per organization.
  To rotate to a different `--app-id`, delete the existing one first with `viam organizations firebase-config delete --org-id <your-org-id> --app-id <existing-app-id>`.
- Uploading with the same `--app-id` overwrites the stored JSON silently.
- The JSON is not parsed at upload time.
  A malformed file uploads successfully but fails at first push send.
  See [Troubleshoot](#troubleshoot).

For the full CLI reference, see [`organizations firebase-config`](/cli/reference/#organizations-firebase-config-set).

## 2. Register device tokens from your mobile app

Each user device must call `UploadDevicePushToken` so Viam knows where to deliver pushes for that user.
Without this step, triggers fire but no notification reaches the user.

The Viam mobile app does this automatically.
For a custom app, you must wire it in.

### Flutter

The Flutter SDK exposes three methods on the app client:

```dart
await viam.appClient.uploadDevicePushToken(appId, deviceUuid, deviceToken);
await viam.appClient.deleteDevicePushToken(appId, deviceUuid);
final tokens = await viam.appClient.getDevicePushTokens(appId);
```

Call `uploadDevicePushToken` after the user grants notification permission and on every FCM token refresh.
A periodic re-upload at app startup defends against missed refresh events; pick a cadence that fits your app.
Call `deleteDevicePushToken` on logout.

### Other languages

The Python, TypeScript, Go, and C++ SDKs do not yet expose `UploadDevicePushToken`.
Call the AppService RPCs directly through gRPC.
See the proto definitions in [`app.proto`](https://github.com/viamrobotics/api/blob/main/proto/viam/app/v1/app.proto):

- `UploadDevicePushToken(app_id, device_token, device_uuid)`
- `DeleteDevicePushToken(app_id, device_uuid)`
- `GetDevicePushTokens(app_id)`

### Required fields

<!-- prettier-ignore -->
| Field | What to send |
| ----- | ------------ |
| `app_id` | Your mobile app's package name, the same value used with `firebase-config set`. |
| `device_token` | The FCM registration token for the device. Flutter apps obtain this from `FirebaseMessaging.instance.getToken()`. iOS apps call `getAPNSToken()` first; FCM normalizes both. |
| `device_uuid` | A stable identifier for the device, so Viam does not accumulate duplicate registrations across re-uploads. The Viam mobile app uses `android.id` (from the `device_info_plus` Flutter package) on Android and `identifierForVendor` on iOS; pick whatever stable identifier fits your platform. |

User identity comes from the authenticated Viam session on the call, so there is no `user_id` parameter.

### Token lifecycle

- Tokens are stored per `(user_id, app_id)`.
  A user can have parallel tokens for `com.viam.viammobile` and a custom app, and only the matching set receives any given push.
- Viam prunes dead tokens automatically when FCM reports "not registered."
  No server-side cleanup is required for stale tokens.
- Calling `DeleteDevicePushToken` on logout is still recommended so a shared device does not receive notifications for the previous user.

## 3. Authorize the machine

When a trigger fires with a non-Viam `application`, Viam verifies that the machine imports at least one fragment owned by the same organization that registered the Firebase config.
This check runs at send time.
If it fails, the trigger fires, but no notification is delivered.

To authorize a machine for your custom app:

1. [Create a fragment](/hardware/fragments/#save-your-own-configurations) owned by the organization that uploaded the Firebase config.
   The fragment does not need to contain the trigger config; any fragment owned by that organization satisfies the check.
1. On the machine's **CONFIGURE** tab, click **+**, select **Configuration block**, search for your fragment, and click **Add fragment**.

`com.viam.viammobile` is exempt from this check.
Triggers targeting the Viam mobile app work on any machine the recipient owns or operates.

## 4. Configure the trigger

Add a `notifications` entry with `type: "push"` and your custom `application`:

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "low-battery-alert",
    "event": {
      "type": "conditional_data_ingested",
      "conditional": {
        "data_capture_method": "sensor:battery-monitor:Readings",
        "conditions": {
          "evals": [
            { "operator": "lt", "value": { "battery_pct": 20 } }
          ]
        }
      }
    },
    "notifications": [
      {
        "type": "push",
        "value": "operator@example.com",
        "application": "com.example.myapp",
        "seconds_between_notifications": 600
      }
    ]
  }
]
```

- `value` is either a specific email address or `all_machine_owners`.
- The recipient must be a machine owner or operator and must have accepted push notification permissions in your mobile app.

For all `notifications` fields, see [Trigger configuration](/reference/triggers/).

## 5. Verify and troubleshoot

Fire the trigger by creating the condition (sync matching data, take the machine offline, etc.) and confirm the notification arrives on a device that registered a token for the recipient and `app_id`.

### Troubleshoot

<!-- prettier-ignore -->
| Symptom | Likely cause | Where to check |
| ------- | ------------ | -------------- |
| Trigger fires but no notification arrives | The machine does not import a fragment owned by the app's organization | Machine logs show `trigger push notification failed: app authorization check`. Import an owning-org fragment on the machine. |
| Trigger fires but recipient is not notified | Recipient is not a machine owner or operator, or has not accepted push permissions | Machine logs show `recipient is not a robot owner or operator`. Grant the role, or change the recipient. |
| Notification sends but device receives nothing | No device token registered for that user and `app_id` | Confirm the app called `UploadDevicePushToken` after permission grant. |
| First push fails with unmarshal error | The uploaded JSON is malformed or is the wrong file (client config rather than service account) | Re-download the service account JSON from **Settings → Service accounts** and re-run `firebase-config set`. |

### Notification payload

Viam attaches the following data fields to every trigger-sent push, available to your app's notification handler:

- `event_type`
- `robot_part_id`
- `machine_name`
- `part_name`
- `app_id`

Use these to route the user to the relevant machine or part inside your app when they tap the notification.
