---
title: "Create a custom web interface"
linkTitle: "Create a custom web interface"
weight: 11
no_list: true
type: docs
description: "Create and deploy custom web interfaces for your machines as single-page applications without managing hosting and authentication."
---

Create and deploy custom web interfaces for your machines as single-page applications without managing hosting and authentication.
Once deployed, apps are accessible from a dedicated URL (`appname_publicnamespace.viamapplications.com`) and hosting and authentication is handled for you.

When opening an app, users log in and then select a machine they have access to.
Then your app is rendered and ready for use.

{{<imgproc src="/operate/spa.png" resize="400x" declaredimensions=true alt="App screen asking for the org, location, and machine." class="imgzoom shadow">}}

## Requirements

{{< expand "Install the Viam CLI and authenticate." >}}
Install the Viam CLI using the option below that matches your system architecture:

{{< readfile "/static/include/how-to/install-cli.md" >}}

Then authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}

{{< /expand >}}

## Create a single page app

{{< table >}}
{{% tablestep number=1 %}}

**Build your application** using your preferred framework like React, Vue, Angular, or others.
While you're developing use any machine's credentials.
For deploying your app you must add code to read the machine API key from your browsers local storage:

```ts {class="line-numbers linkable-line-numbers" data-line=""}
import Cookies from "js-cookie";

let apiKeyId = "";
let apiKeySecret = "";
let hostname = "";
let machineId = "";

machineId = window.location.pathname.split("/")[2];
({
  id: apiKeyId,
  key: apiKeySecret,
  hostname: hostname,
} = JSON.parse(Cookies.get(machineId)!));
```

{{% /tablestep %}}
{{% tablestep number=2 %}}

**Create a <FILE>meta.json</FILE>** file using this template:

{{< tabs >}}
{{% tab name="Template" %}}

```json
{
  "module_id": "your-namespace:your-module",
  "visibility": "public",
  "url": "https://github.com/your-org/your-repo",
  "description": "Your module description",
  "applications": [
    {
      "name": "your-app-name",
      "type": "single_machine",
      "entrypoint": "dist/index.html"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Example" %}}

```json
{
  "module_id": "acme:dashboard",
  "visibility": "public",
  "url": "https://github.com/acme/dashboard",
  "description": "An example dashboard for a fictitious company called Acme.",
  "applications": [
    {
      "name": "dashboard",
      "type": "single_machine",
      "entrypoint": "dist/index.html"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% expand "Click to view" %}}

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
|------|------|-----------|-------------|
| `module_id` | string | **Required** | The module ID, which includes the organization name and the module name. `module_id` uniquely identifies your module. |
| `visibility` | string | **Required** | Must be `"public"`. |
| `description` | string | **Required** | A description of your module and what it provides. |
| `url` | string | Optional | The URL of the GitHub repository containing the source code of the module. |
| `applications` | array | Optional | Objects that provide information about the [single page apps](/operate/reference/single-page-apps/) associated with the module. |
| `models` | array | Optional | Empty unless you are shipping the app alongside models. For information on how to add models, see [Integrate other hardware](/operate/get-started/other-hardware/). |

{{% /expand%}}

The `applications` field is an array of application objects with the following properties:

<!-- prettier-ignore -->
| Property     | Type   | Description |
| ------------ | ------ | ----------- |
| `name`       | string | The name of your application, which will be a part of the app's URL (`name_publicnamespace.viamapplications.com`). For more information on valid names see [](/operate/reference/naming-modules#valid-application-identifiers). |
| `type` | string | The type of application (currently only `"single_machine"` is supported). |
| `entrypoint` | string | The path to the HTML entry point for your application. The `entrypoint` field specifies the path to your application's entry point. For example: <ul><li><code>"dist/index.html"</code>: Static content rooted at the `dist` directory</li><li><code>"dist/foo.html"</code>: Static content rooted at the `dist` directory, with `foo.html` as the entry point</li><li><code>"dist/"</code>: Static content rooted at the `dist` directory (assumes `dist/index.html` exists)</li><li><code>"dist/bar/foo.html"</code>: Static content rooted at `dist/bar` with `foo.html` as the entry point</li></ul> |

{{% /tablestep %}}
{{% tablestep number=3 %}}
**Register your module** with Viam:

{{< tabs >}}
{{% tab name="Template" %}}

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam module create --name="app-name" --public-namespace="namespace"
```

{{% /tab %}}
{{% tab name="Example" %}}

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam module create --name="air-quality" --public-namespace="naomi"
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep number=4 %}}

**Package your static files and your <FILE>meta.json</FILE> file and upload them** to the Viam Registry:

```sh {class="command-line" data-prompt="$" data-output="3-10"}
tar -czvf module.tar.gz <static-website-files> meta.json
viam module upload module.tar.gz --platform=any --version=0.0.1
```

For subsequent updates run these commands again with an updated version number.

{{% /tablestep %}}
{{< /table >}}

## Accessing your Single Page App

After uploading your module with the application configuration, your application will be available at:

```
https://your-app-name_your-public-namespace.viamapplications.com
```

Users will be prompted to authenticate with their Viam credentials before accessing your application:

1. User navigates to `your-app-name_your-public-namespace.viamapplications.com`
1. User authenticates with Viam credentials
1. User selects an organization, location, and machine
1. User is redirected to `your-app-name_your-public-namespace.viamapplications.com/machine/{machine-id}`
1. Your application is rendered with access to the selected machine

## Example

For an example see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).

## Limitations

- Single page apps currently only support single-machine applications
- All modules with apps must have public visibility
- There is no separate deploy step; the page will always render the latest version
- Browsers with cookies disabled are not supported

## Security Considerations

- Customer apps are stored in GCS buckets that are publicly available on the internet
- Avoid uploading sensitive information in your application code or assets
- API keys and secrets are stored in the browser's localStorage or sessionStorage
- Single page apps authenticate users with FusionAuth
