---
title: "Authenticate end users with OAuth"
linkTitle: "OAuth"
weight: 60
layout: "docs"
type: "docs"
description: "Create a branded login screen for your application."
images: ["/operate/oauth.png"]
date: "2025-01-22"
---

You can use Viam to manage your user authentication.
This guide will show you how to create a branded login screen.

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

You must have [owner permissions](/manage/manage/rbac/#organization-settings-and-roles) on the organization.

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
| `--org-id` |  The organization ID that is tied to the OAuth application. | **Required** |
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
