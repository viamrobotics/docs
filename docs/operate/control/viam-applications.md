---
title: "Create a Viam application"
linkTitle: "Create a Viam application"
weight: 5
layout: "docs"
type: "docs"
description: "Create and deploy a custom web interface for your machines without managing hosting infrastructure and authentication."
videos: ["/spa.webm", "/spa.mp4"]
videoAlt: "Logging into a viam application."
images: ["/spa.gif"]
---

Create and deploy a custom web interface for your machines without managing hosting infrastructure and authentication.
Once deployed, your application is accessible from a dedicated URL (`appname_publicnamespace.viamapplications.com`), and Viam handles hosting and authentication.

Users log in and the application then renders your custom interface for interacting with the user's machines.
You can choose to build an application that can access and operate a single-machine or multiple machines.

## Requirements

{{< expand "Install the Viam CLI and authenticate." >}}
Install the Viam CLI using the option below that matches your system architecture:

{{< readfile "/static/include/how-to/install-cli.md" >}}

Then authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}

{{< /expand >}}

## Build a custom web interface

You can build a custom web interface to access your machines using your preferred framework like React, Vue, Angular, or others.

{{< table >}}
{{% tablestep start=1 %}}
**Access machines from your application**

When logging into a Viam application, Viam stores an access token in the user's browser.
For single-machine applications, Viam stores an access token and several machine-specific cookies.

Access the data from the browser's cookies and use it to make API calls:

{{< tabs >}}
{{% tab name="Single-machine application" %}}

```ts {class="line-numbers linkable-line-numbers" data-line=""}
import * as VIAM from "@viamrobotics/sdk";
import Cookies from "js-cookie";

let apiKeyId = "";
let apiKeySecret = "";
let host = "";
let machineId = "";

async function main() {
  const opts: VIAM.ViamClientOptions = {
    serviceHost: "https://app.viam.com",
    credentials: {
      type: "api-key",
      payload: apiKeySecret,
      authEntity: apiKeyId,
    },
  };

  const client = await VIAM.createViamClient(opts);
  const machine = await client.appClient.getRobot(machineId);
}

document.addEventListener("DOMContentLoaded", async () => {
  // Extract the machine identifier from the URL
  let machineCookieKey = window.location.pathname.split("/")[2];
  ({
    apiKey: { id: apiKeyId, key: apiKeySecret },
    machineId: machineId,
    hostname: host,
  } = JSON.parse(Cookies.get(machineCookieKey)!));

  main().catch((error) => {
    console.error("encountered an error:", error);
  });
});
```

{{% /tab %}}
{{% tab name="Multi-machine application" %}}

```ts {class="line-numbers linkable-line-numbers" data-line=""}
import * as VIAM from "@viamrobotics/sdk";
import Cookies from "js-cookie";

let access_token = "";
// optionally specify a fragmentID to use with the listMachineSummaries API call
let fragmentID = "";

async function main() {
  const opts: VIAM.ViamClientOptions = {
    serviceHost: "https://app.viam.com",
    credentials: {
      type: "access-token",
      payload: access_token,
    },
  };

  const client = await VIAM.createViamClient(opts);
  const locationSummaries = await client.appClient.listMachineSummaries("", [
    fragmentID,
  ]);
}

document.addEventListener("DOMContentLoaded", async () => {
  const userTokenRawCookie = Cookies.get("userToken")!;
  const startIndex = userTokenRawCookie.indexOf("{");
  const endIndex = userTokenRawCookie.indexOf("}");
  const userTokenValue = userTokenRawCookie.slice(startIndex, endIndex + 1);
  access_token = JSON.parse(userTokenValue).access_token;

  main().catch((error) => {
    console.error("encountered an error:", error);
  });
});
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure routing**

{{< tabs >}}
{{% tab name="Single-machine application" %}}

When using your deployed application, static files will be accessible at `https://your-app-name_your-public-namespace.viamapplications.com/machine/<machineHostname>/`.

{{% /tab %}}
{{% tab name="Multi-machine application" %}}

When using your deployed application, static files will be accessible at `https://your-app-name_your-public-namespace.viamapplications.com/`.

{{% /tab %}}
{{< /tabs >}}

If your HTML file loads other files, use relative paths to ensure your files are accessible.

{{% /tablestep %}}
{{< /table >}}

## Local development

For developing your application on localhost:

1. Run your web server. Take note of its port number for the next step.
1. Run the following commands specifying the address where your app is running on localhost and a machine to test on.

   {{< tabs >}}
   {{% tab name="Single-machine application" %}}

   The command will proxy your local app and open a browser window and navigate to `http://localhost:8012/machine/<machineHostname>` for the machine provided with --machine-id.

{{< tabs >}}
{{% tab name="Template" %}}

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam login
viam module local-app-testing --app-url http://localhost:<PORT-YOUR-WEB-SERVER-IS-ON> --machine-id <MACHINE-ID>
```

{{% /tab %}}
{{% tab name="Example" %}}

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam login
viam module local-app-testing --app-url http://localhost:3000 --machine-id a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Multi-machine application" %}}

The command will proxy your local app and open a browser window and navigate to `http://localhost:8012/`.

{{< tabs >}}
{{% tab name="Template" %}}

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam login
viam module local-app-testing --app-url http://localhost:<PORT>
```

{{% /tab %}}
{{% tab name="Example" %}}

```sh {class="command-line" data-prompt="$" data-output="3-10"}
viam login
viam module local-app-testing --app-url http://localhost:3000
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

## Deploy your web interface

To deploy your web interface with Viam, you must create a FILE>meta.json</FILE> file and package it with yoru web application as a module.

{{< table >}}
{{% tablestep start=1 %}}

**Create a <FILE>meta.json</FILE>** file for your module using this template.

Viam uses the <FILE>meta.json</FILE> file to add some customizations to the authentication screen of your application and to display it in the Viam Registry.

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
      "type": "single_machine|multi_machine",
      "entrypoint": "dist/index.html",
      "fragmentIds": [],
      "logoPath": "static/logo.png",
      "customizations": {
        "machinePicker": {
          "heading": "Heading to display on branded authentication page",
          "subheading": "Subheading to display on branded authentication page"
        }
      }
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
  "description": "An example dashboard for a fictitious air quality company called acme.",
  "applications": [
    {
      "name": "dashboard",
      "type": "single_machine",
      "entrypoint": "dist/index.html",
      "fragmentIds": [],
      "logoPath": "static/logo.png",
      "customizations": {
        "machinePicker": {
          "heading": "Air monitoring dashboard",
          "subheading": "Sign in and select your devices to view your air quality metrics in a dashboard."
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

This file specifies the contents of the module.
It is required for your module.

{{% expand "Click to view more information on attributes." %}}

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
|------|------|-----------|-------------|
| `module_id` | string | **Required** | The module ID, which includes the organization name and the module name. `module_id` uniquely identifies your module. |
| `visibility` | string | **Required** | Must be `"public"`. |
| `description` | string | **Required** | A description of your module and what it provides. |
| `url` | string | Optional | The URL of the GitHub repository containing the source code of the module. |
| `applications` | array | Optional | Objects that provide information about the [applications](/operate/control/viam-applications/) associated with the module. |
| `models` | array | Optional | Empty unless you are shipping the app alongside models. For information on how to add models, see [Support hardware and software](/operate/modules/support-hardware/). |

{{% /expand%}}

The `applications` field is an array of application objects with the following properties:

<!-- prettier-ignore -->
| Property     | Type   | Description |
| ------------ | ------ | ----------- |
| `name`       | string | The name of your application, which will be a part of the application's URL (`name_publicnamespace.viamapplications.com`). For more information on valid names see [Valid application identifiers](/operate/modules/advanced/naming-modules/#valid-application-identifiers). |
| `type` | string | The type of application: `"single_machine"` or `"multi_machine"`. Whether the application can access and operate one machine or multiple machines. |
| `entrypoint` | string | The path to the HTML entry point for your application. The `entrypoint` field specifies the path to your application's entry point. For example: <ul><li><code>"dist/index.html"</code>: Static content rooted at the `dist` directory</li><li><code>"dist/foo.html"</code>: Static content rooted at the `dist` directory, with `foo.html` as the entry point</li><li><code>"dist/"</code>: Static content rooted at the `dist` directory (assumes `dist/index.html` exists)</li><li><code>"dist/bar/foo.html"</code>: Static content rooted at `dist/bar` with `foo.html` as the entry point</li></ul> |
| `fragmentIds` | []string | Specify the fragment or fragments that a machine must contain to be selectable from the machine picker screen. Only for single machine applications. |
| `logoPath` | string | The URL or the relative path to the logo to display on the machine picker screen for a single machine application. |
| `customizations` | object | Override the branding heading and subheading to display on the authentication screen for single machine applications: <ul><li>`heading`: Override the heading. May not be longer than 60 characters. </li><li>`subheading` Override the subheading. May not be longer than 256 characters.</li></ul> Example: `{ "heading": "Air monitoring dashboard", "subheading": "Sign in and select your devices to view your air quality metrics in a dashboard" }`. |

{{% /tablestep %}}
{{% tablestep %}}
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
{{% tablestep %}}

To deploy your application with Viam you must package your static files and your <FILE>meta.json</FILE> file as a module and upload them to the Viam Registry:

```sh {class="command-line" data-prompt="$" data-output="3-10"}
tar -czvf module.tar.gz <static-website-files> meta.json
viam module upload --upload=module.tar.gz --platform=any --version=0.0.1
```

For subsequent updates run these commands again with an updated version number.

{{% /tablestep %}}
{{< /table >}}

## Access your application

After uploading your module with the application configuration, your application will be available at:

```txt
https://your-app-name_your-public-namespace.viamapplications.com
```

Users will be prompted to authenticate with their Viam credentials before accessing your application:

1. User navigates to `your-app-name_your-public-namespace.viamapplications.com`.
1. User authenticates with Viam credentials.
1. For single-machine applications, the user selects an organization, location, and machine and is redirected to `your-app-name_your-public-namespace.viamapplications.com/machine/<machineHostname>`.
   For multi-machine applications, the user is redirected to `your-app-name_your-public-namespace.viamapplications.com/`.
1. Your application is rendered with access to the selected machine.
   The credentials for that one machine are provided in the cookies.

{{< tabs >}}
{{% tab name="Single-machine application example" %}}

{{<gif webm_src="/spa.webm" mp4_src="/spa.mp4" alt="Login screen with machine selection" max-width="500px">}}

{{% /tab %}}
{{% tab name="Multi-machine application example" %}}

{{<gif webm_src="/air-quality-loading.webm" mp4_src="/air-quality-loading.mp4" alt="Login screen" max-width="500px">}}

{{% /tab %}}
{{< /tabs >}}

## Examples

- For a multi-machine TypeScript application see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).

- For a single-machine React application that shows camera feeds for a machine, see [Viam Camera Viewer](https://github.com/viam-labs/viam-camera-viewer).

## Limitations

- All modules with applications must have public visibility.
- The page will always render the latest version.
- Browsers with cookies disabled are not supported.
- Viam applications serve static files.
  If you are building an application with server-side rendering or need other back-end capabilities, Viam applications is not the right choice.

## Security considerations

- Customer applications are stored publicly on the internet, so avoid uploading sensitive information in your application code or assets.
- API keys and secrets are stored in the browser's cookies.
- Users authenticate with FusionAuth.

## FAQ

### Can I use a custom domain?

Viam does not currently support using custom domains (for example: `app.mycustomdomain.com/machine/<machineHostname>`) to serve your Viam application.
You can, however, redirect from your domain to your Viam application (`app.mycustomdomain.com` -> `your-app-name_your-public-namespace.viamapplications.com`).
You can configure a redirect (HTTP 301) on your web server or hosting provider from `app.mycustomdomain.com/*` to `your-app-name_your-public-namespace.viamapplications.com/*`.

### How can I add external API keys?

You can store API keys for use with Viam apps as part of robot metadata:

{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.py" lang="py" class="line-numbers linkable-line-numbers" data-line="39-41" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.go" lang="go" class="line-numbers linkable-line-numbers" data-line="50-52" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="37-39" >}}

{{% /tab %}}
{{< /tabs >}}

Then you can access these API keys from within your app:

```ts {class="line-numbers linkable-line-numbers"}
const metadata = await appClient.getRobotMetadata("<YOUR-MACHINE-ID>");
const key = metadata.TEST_API_KEY;
```
