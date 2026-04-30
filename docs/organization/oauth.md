---
title: "Authenticate end users with OAuth"
linkTitle: "OAuth"
weight: 30
layout: "docs"
type: "docs"
description: "Create a branded login screen for your application."
images: ["/operate/oauth.png"]
date: "2025-01-22"
---

If you are building a product on Viam, you can set up branded authentication for your end users.
This guide shows you how to create a branded login screen using Viam's OAuth integration, which is built on [FusionAuth](https://fusionauth.io/).

{{< alert title="Note" color="note" >}}
This feature is for authenticating **your product's end users**, not for signing into the Viam app itself.
{{< /alert >}}

{{<imgproc src="/operate/oauth.png" resize="1000x" declaredimensions=true alt="Example Oauth login screen" style="width:600px" class="imgzoom shadow">}}

## Prerequisites

{{< table >}}
{{% tablestep start=1 %}}
**Add the logo** to be displayed on the login screen for your organization.
Your logo can be up to 200KB in size and must be in PNG format.

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organization logo set --logo-path=logo.png --org-id=<org-id>
Successfully set the logo for organization <org-id> to logo at file-path: logo.png
```

You must have [owner permissions](/organization/rbac/#organization-settings-and-roles) on the organization.

{{% /tablestep %}}
{{% tablestep %}}
**The support email** that will be shown when Viam sends emails to users on your behalf for email verification, password recovery, and other account related emails.

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organization support-email set --support-email=support@logoipsum.com --org-id=<org-id>
Successfully set support email for organization "<org-id>" to "support@logoipsum.com"
```

{{% /tablestep %}}
{{< /table >}}

## Set up auth app

{{< table >}}
{{% tablestep start=1 %}}
**Enable the authentication service** for your organization:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organization auth-service enable --org-id=<org-id>
enabled auth service for organization "<org-id>":
```

{{% /tablestep %}}
{{% tablestep %}}
**Create an OAuth application** for your organization:

```sh {class="command-line" data-prompt="$" data-output="6-10"}
viam organization auth-service oauth-app create --client-authentication=required \
    --client-name="OAuth Test App" --enabled-grants="password, authorization_code" \
    --logout-uri="https://logoipsum.com/logout" --origin-uris="https://logoipsum.com,http://localhost:3000" \
    --pkce=not_required --redirect-uris="https://logoipsum.com/oauth-redirect,http://localhost:3000/oauth-redirect" \
    --url-validation=allow_wildcards --org-id=<org-id>
Successfully created OAuth app OAuth Test App with client ID <client-id> and client secret <secret-token>
```

{{% expand "Click to view more information about arguments." %}}

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--client-authentication` | The client authentication policy for the OAuth application. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_pkce`. Default: `unspecified`. | **Required** |
| `--client-name` | The name for the OAuth application. | **Required** |
| `--enabled-grants` | Comma-separated enabled grants for the OAuth application. Options: `unspecified`, `refresh_token`, `password`, `implicit`, `device_code`, `authorization_code`. | **Required** |
| `--logout-uri` | The logout uri for the OAuth application. | **Required** |
| `--org-id` | The organization ID that is tied to the OAuth application. | **Required** |
| `--origin-uris` | Comma-separated origin URIs for the OAuth application. | **Required** |
| `--pkce` | Proof Key for Code Exchange (PKCE) for the OAuth application. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_client_authentication`. Default: `unspecified`. | **Required** |
| `--redirect-uris` | Comma-separated redirect URIs for the OAuth application. | **Required** |
| `--url-validation` | URL validation for the OAuth application. Options: `unspecified`, `exact_match`, `allow_wildcards`. Default: `unspecified`. | **Required** |

{{% /expand%}}

{{% /tablestep %}}
{{% tablestep %}}
**See OAuth app**:

```sh {class="command-line" data-prompt="$" data-output="2-5,7-20"}
viam organization auth-service oauth-app list --org-id=<org-id>
OAuth apps for organization "<org-id>":

 - <client-id>

viam organization auth-service oauth-app read --org-id=<org-id> --client-id=<client-id>
OAuth config for client ID <client-id>:

Client Authentication: required
PKCE (Proof Key for Code Exchange): not_required
URL Validation Policy: allow_wildcards
Logout URL: https://logoipsum.com/logout
Redirect URLs: https://logoipsum.com/oauth-redirect, http://localhost:3000/oauth-redirect
Origin URLs: https://logoipsum.com, http://localhost:3000
Enabled Grants: authorization_code, password
```

{{% /tablestep %}}
{{< /table >}}

The generated client ID is unique to your OAuth app and linked to your organization.
You can update any value after setup using `viam organization auth-service oauth-app update`.

## Designate a login client ID

If you want invite links to use a custom login screen instead of Viam's default, designate which of your registered OAuth apps drives the flow.

1. In the top nav, click your organization's name to open the organization dropdown.
1. Click **Settings**.
1. Scroll to **White Labeling** and find **Login client ID**. The field appears once you have at least one OAuth app registered, and its help text lists the valid client IDs.
1. Enter the client ID of one of your registered OAuth apps and click **Save**.

The client ID must match one of your registered OAuth apps. The OAuth app's redirect URI list must include Viam's invite redirect URI; this is added automatically when you create the OAuth app, so you only need to add it manually if you've removed it.

When **Login client ID** is set, organization invite links route users to the FusionAuth login screen for the designated OAuth app, which uses that app's own branding. When the field is empty, invite links route users to Viam's default login screen, which displays your organization's logo if you've uploaded one through the same **White Labeling** section.

**Behavior change.** Before this setting existed, organizations with any registered OAuth app had the first one used automatically as the login client. That fallback no longer exists. If you want a branded invite login flow, set **Login client ID** explicitly.

## Use the generated client ID and secret in your app

Your authentication is built on top of FusionAuth.
To continue, use the generated client secret and client ID with the [Fusion Auth SDKs](https://fusionauth.io/docs/sdks/).

For a quick example, see [Get started with FusionAuth in 5 minutes](https://github.com/FusionAuth/fusionauth-example-5-minute-guide).

{{< alert title="Base URL" color="tip" >}}

When using the client ID and client secret, the base URL for your OAuth application is `https://auth.viam.com`.

{{< /alert >}}

## FAQ

### Can I customize my login screen further?

If you need further customization, please [contact us](mailto:support@viam.com).
