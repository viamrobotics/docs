---
linkTitle: "Administer your organization"
title: "Administer your organization with the CLI"
weight: 70
layout: "docs"
type: "docs"
description: "Manage API keys, OAuth, billing, and organization settings from the command line."
---

Create and manage API keys, configure OAuth authentication for end users, and set up white-label billing for your organization.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

To find your organization ID:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

To find location IDs:

```sh {class="command-line" data-prompt="$"}
viam locations list
```

To find machine IDs:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --all
```

## Manage locations

List all locations in your organization:

```sh {class="command-line" data-prompt="$"}
viam locations list
```

If you belong to multiple organizations, specify which one:

```sh {class="command-line" data-prompt="$"}
viam locations list --organization=<org-id>
```

If you have set a default organization with `viam defaults set-org`, the CLI uses it automatically.

## Manage API keys

### Organization API key

Create an API key with organization-level access.
Organization keys have the `organization_owner` role with full read and write access to every resource in the organization.

```sh {class="command-line" data-prompt="$"}
viam organizations api-key create --org-id=<org-id> --name=my-org-key
```

The CLI prints the key ID and key value. Save both immediately; the key value is only shown once.

```sh {class="command-line" data-prompt="$" data-output="1-3"}
Successfully created key:
Key ID: abcdef12-3456-7890-abcd-ef1234567890
Key Value: your-secret-key-value
```

### Location API key

Create an API key scoped to a specific location.
Location keys have the `location_owner` role.

```sh {class="command-line" data-prompt="$"}
viam locations api-key create --location-id=<location-id> --name=my-location-key
```

### Machine API key

Create an API key scoped to a single machine.
Machine keys have the `robot_owner` role.

```sh {class="command-line" data-prompt="$"}
viam machines api-key create --machine-id=<machine-id>
```

## Set up OAuth

OAuth setup is CLI-only. There is no web UI for these operations.

### Enable the auth service

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service enable --org-id=<org-id>
```

### Set branding

```sh {class="command-line" data-prompt="$"}
viam organizations logo set --org-id=<org-id> --logo-path=./logo.png
```

```sh {class="command-line" data-prompt="$"}
viam organizations support-email set --org-id=<org-id> --support-email=support@example.com
```

### Create an OAuth application

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service oauth-app create \
  --org-id=<org-id> \
  --client-name=my-app \
  --client-authentication=unspecified \
  --url-validation=exact_match \
  --pkce=required \
  --enabled-grants=authorization_code \
  --redirect-uris=https://example.com/callback \
  --logout-uri=https://example.com/logout \
  --origin-uris=https://example.com
```

On success, the CLI prints the client ID and client secret.
Save both values immediately; you need the client ID for subsequent commands.

### Manage OAuth applications

List all OAuth applications:

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service oauth-app list --org-id=<org-id>
```

Get details on a specific application:

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service oauth-app read \
  --org-id=<org-id> \
  --client-id=<client-id>
```

Update an application:

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service oauth-app update \
  --org-id=<org-id> \
  --client-id=<client-id> \
  --client-name=updated-name
```

Delete an application:

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service oauth-app delete \
  --org-id=<org-id> \
  --client-id=<client-id>
```

### Disable the auth service

```sh {class="command-line" data-prompt="$"}
viam organizations auth-service disable --org-id=<org-id>
```

## Configure white-label billing

Billing service setup is CLI-only.

Enable billing.
The address format is `"line1, line2 (optional), city, state, zipcode"`:

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service enable --org-id=<org-id> --address="123 Main St, Springfield, IL, 62704"
```

Get billing configuration:

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service get-config --org-id=<org-id>
```

Update billing:

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service update --org-id=<org-id> --address=<billing-address>
```

Disable billing:

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service disable --org-id=<org-id>
```

## Related pages

- [Manage access](/organization/access/) for role-based access control in the Viam app
- [Authenticate end users with OAuth](/organization/oauth/) for OAuth setup details
- [White-labeled billing](/organization/billing/) for billing fragment configuration
- [CLI reference](/cli/) for the complete `organizations` command reference
