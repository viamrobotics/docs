---
title: "Create a custom web interface"
linkTitle: "Create a custom web interface"
weight: 11
no_list: true
type: docs
description: "Create and deploy single page applications on the Viam platform."
---

With single page apps you can create and deploy custom web interfaces for your machines that use a single HTML page.
Single page apps are accessible from a dedicated URL (`appname.publicnamespace.viamapps.com`) and hosting and authentication is handled for you.

When opening an app, users log in and then select a machine they have access to.
Then your app is rendered and ready for use.

TODO: Example GIF

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

**Build your single page application** using your preferred framework like React, Vue, Angular, or others.
Your application should be built and ready for deployment, with all assets compiled into a distributable format.

TODO: cover dev process
TODO: how do you connect to the machine / how do you access the api key?

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
      "type": "web",
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
      "type": "web",
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
| Property     | Type   | Description                                                                                       |
| ------------ | ------ | ------------------------------------------------------------------------------------------------- |
| `name`       | string | The name of your application, which will be a part of the app's URL (`name.publicnamespace.viamapps.com`). For more information on valid names see [](/operate/reference/naming-modules). |
| `type` | string | The type of application (currently only `"web"` is supported). |
| `entrypoint` | string | The path to the HTML entry point for your application. The `entrypoint` field specifies the path to your application's entry point. For example: <ul><li><code>"dist/index.html"</code>: Static content rooted at the `dist` directory</li><li><code>"dist/foo.html"</code>: Static content rooted at the `dist` directory, with `foo.html` as the entry point</li><li><code>"dist/"</code>: Static content rooted at the `dist` directory (assumes `dist/index.html` exists)</li><li><code>"dist/bar/foo.html"</code>: Static content rooted at `dist/bar` with `foo.html` as the entry point</li></ul> |

{{% /tablestep %}}
{{% tablestep number=3 %}}

**Package your app into a module and upload it** to the Viam Registry:

TODO: first command doesn't make sense

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam module build local
viam module upload module.tar.gz
```

TODO: the upload command requires platform & version - is that no longer the case?

For subsequent updates you can use:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam module update
```

{{% /tablestep %}}
{{< /table >}}

## Accessing your Single Page App

Once your module with the application configuration is uploaded, your application will be available at:

TODO: any extra steps?

```
https://your-app-name.your-public-namespace.viamapps.com
```

Users will be prompted to authenticate with their Viam credentials before accessing your application:

1. User navigates to `your-app-name.your-public-namespace.viamapps.com`
1. User authenticates with Viam credentials
1. User selects an organization, location, and machine
1. User is redirected to `your-app-name.your-public-namespace.viamapps.com/machine/{machine-id}`
1. Your application is rendered with access to the selected machine

## Limitations

- Single page apps currently only support single-machine applications
- All modules with apps must have public visibility
- There is no versioning or separate deploy step; the page will always render the latest version
- Browsers with cookies disabled are not supported

## Security Considerations

- Customer apps are stored in GCS buckets that are publicly available on the internet
- Avoid uploading sensitive information in your application code or assets
- API keys and secrets are stored in the browser's localStorage or sessionStorage
- Single page apps authenticate users with FusionAuth

## Example

Here's a complete example of creating and uploading a simple React application as a Viam Single Page App:

```bash
# Create a new React app
npx create-react-app my-viam-app
cd my-viam-app

# Build the app
npm run build

# Create a module with the app
viam module create --name my-viam-app --public-namespace your-namespace

# Edit meta.json to add the application configuration
# Add the following to meta.json:
# "visibility": "public",
# "applications": [
#   {
#     "name": "my-app",
#     "type": "web",
#     "entrypoint": "build/index.html"
#   }
# ]

# Copy the build directory to the module directory
cp -r build/ path/to/module/

# Build and upload the module
viam module build local
viam module upload module.tar.gz
```

After the module is approved, your application will be available at `https://my-app.your-public-namespace.viamapps.com`.
