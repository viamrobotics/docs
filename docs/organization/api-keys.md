---
linkTitle: "Manage API keys"
title: "Manage API keys"
weight: 25
layout: "docs"
type: "docs"
no_list: true
description: "Create, rotate, and manage API keys for programmatic access to your organization, locations, and machines."
---

API keys provide programmatic access to your Viam resources.
Each API key is scoped to a specific level of the [resource hierarchy](/organization/overview/) and assigned a role, so you can control exactly what it can access.

Use API keys to authenticate SDK connections, CLI scripts, and automated workflows.

## Choose the right scope

Every API key is scoped to an organization, location, or machine, and assigned an Owner or Operator role.
Follow the principle of least privilege: grant the narrowest scope that lets the key do its job.

| Use case                                 | Recommended scope   |
| ---------------------------------------- | ------------------- |
| SDK connection to one machine            | Machine, Operator   |
| Automated deployment script for one site | Location, Owner     |
| CI/CD pipeline for module uploads        | Organization, Owner |
| Monitoring dashboard for a location      | Location, Operator  |

For details on what each role can do, see [Permissions](/organization/rbac/).

## Create an API key

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Navigate to the level where you want to create the key:
   - **Organization**: Click the organization name in the top navigation bar, then **Settings**. Find the **API keys** section.
   - **Machine**: Navigate to the machine's page and click the **CONNECT** tab.
1. Click **Generate key** or **Add key**.
1. Give the key a descriptive name (for example, `production-deploy-script` or `warehouse-monitoring`).
1. Copy the key and key ID immediately. You will not be able to see the key again.

{{% /tab %}}
{{% tab name="CLI" %}}

Create a key at the organization, location, or machine level:

```sh {class="command-line" data-prompt="$" data-output="2-3"}
viam organizations api-key create --org-id <org-id> --name "deploy-pipeline"
Key ID: xxxx-xxxx
Key: xxxx-xxxx-xxxx
```

```sh {class="command-line" data-prompt="$" data-output="2-3"}
viam locations api-key create --location-id <location-id> --name "warehouse-monitoring"
Key ID: xxxx-xxxx
Key: xxxx-xxxx-xxxx
```

```sh {class="command-line" data-prompt="$" data-output="2-3"}
viam machines api-key create --machine-id <machine-id> --name "arm-control"
Key ID: xxxx-xxxx
Key: xxxx-xxxx-xxxx
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
from viam.app.app_client import APIKeyAuthorization
from viam.app.viam_client import ViamClient

client = await ViamClient.create_from_dial_options(...)
api_key, api_key_id = await client.app_client.create_key(
    org_id="<org-id>",
    authorizations=[
        APIKeyAuthorization(
            role="owner",
            resource_type="location",
            resource_id="<location-id>"
        )
    ],
    name="warehouse-monitoring"
)
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Important" color="note" >}}
Store your API key securely.
Viam does not store the key value after creation.
If you lose it, you must rotate or create a new key.
{{< /alert >}}

## List API keys

{{< tabs >}}
{{% tab name="Python" %}}

```python
keys = await client.app_client.list_keys(org_id="<org-id>")
for key in keys:
    print(f"{key.api_key_id}: {key.name}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
keys, err := client.ListKeys(ctx, "<org-id>")
for _, key := range keys {
    fmt.Printf("%s: %s\n", key.APIKeyID, key.Name)
}
```

{{% /tab %}}
{{< /tabs >}}

## Rotate a key

Key rotation lets you generate a new key value while keeping the same authorizations.
This is useful for periodic credential rotation or when a key may have been exposed.

To rotate without downtime:

1. Create a new key with the same scope and role.
1. Update all consumers (scripts, SDK connections) to use the new key.
1. Verify the new key works.
1. Delete the old key.

You can also rotate in place with the SDK, which generates a new key value and invalidates the old one immediately:

{{< tabs >}}
{{% tab name="Python" %}}

```python
new_key, new_key_id = await client.app_client.rotate_key(id="<api-key-id>")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
newKey, newKeyID, err := client.RotateKey(ctx, "<api-key-id>")
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Caution" color="caution" >}}
`rotate_key` invalidates the old key immediately.
Any consumer still using the old key will lose access.
For zero-downtime rotation, use the create-then-delete approach instead.
{{< /alert >}}

## Rename a key

Give a key a more descriptive name:

```go
err := client.RenameKey(ctx, "<api-key-id>", "new-descriptive-name")
```

{{< alert title="Note" color="note" >}}
`RenameKey` is currently available in the Go SDK only.
{{< /alert >}}

## Delete a key

{{< tabs >}}
{{% tab name="Python" %}}

```python
await client.app_client.delete_key(id="<api-key-id>")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err := client.DeleteKey(ctx, "<api-key-id>")
```

{{% /tab %}}
{{< /tabs >}}

## Use an API key

### SDK connection

Use an API key to connect to a machine from your code:

```python
from viam.robot.client import RobotClient

opts = RobotClient.Options.with_api_key(
    api_key="<your-api-key>",
    api_key_id="<your-api-key-id>"
)
robot = await RobotClient.at_address("<machine-address>", opts)
```

### CLI authentication

Authenticate the CLI with an API key:

```sh {class="command-line" data-prompt="$"}
viam login api-key --key-id <key-id> --key <key>
```

To manage multiple API keys, use CLI profiles:

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name production --key-id <key-id> --key <key>
```

See [CLI authentication](/organization/overview/#cli-authentication) for more details.

## Best practices

- **Name keys descriptively.** Include the purpose and scope: `production-deploy-ci`, `warehouse-3-monitoring`, `dev-testing`.
- **Use the narrowest scope possible.** A script that only reads sensor data from one machine should use a machine-scoped Operator key, not an org-scoped Owner key.
- **Rotate keys periodically.** Use the create-then-delete pattern to avoid downtime.
- **Revoke keys when people leave.** List all keys with `list_keys` and delete any associated with departed team members.
- **Do not commit keys to version control.** Use environment variables or secret management tools.
