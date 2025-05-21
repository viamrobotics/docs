---
title: "Single Page Apps"
linkTitle: "Single Page Apps"
weight: 45
no_list: true
type: docs
icon: true
description: "Create and deploy single page applications hosted by Viam."
---

Viam Single Page Apps allow you to upload a single page application and access it via a dedicated URL (`appname.publicnamespace.viamapps.com`), with hosting, authentication, and boilerplate logic handled for you. This feature enables you to create custom web interfaces for your machines without having to manage the infrastructure for hosting and authentication.

## Overview

With Viam Single Page Apps, you can:

- Host shared logic for users to choose an organization, location, and single machine
- Render your application once a user has selected a machine
- Store robot owner API key and secret in browser storage
- Proxy requests through the viamapps.com domain to maintain same-origin across pages
- Authenticate users via FusionAuth
- Create and upload apps using the modules framework

## Requirements

To use Viam Single Page Apps, you need:

- A module with a public visibility setting
- A properly configured `meta.json` file with application information
- A built single page application with an HTML entry point

## Creating a Single Page App

### 1. Build your application

Build your single page application using your preferred framework (React, Vue, Angular, etc.). Your application should be built and ready for deployment, with all assets compiled into a distributable format.

### 2. Configure your module's meta.json

Add the `applications` field to your module's `meta.json` file to define your single page app:

```json
{
  "module_id": "your-namespace:your-module",
  "visibility": "public",
  "url": "https://github.com/your-org/your-repo",
  "description": "Your module description",
  "models": [
    {
      "api": "rdk:component:base",
      "model": "your-namespace:your-module:your-model"
    }
  ],
  "entrypoint": "run.sh",
  "applications": [
    {
      "name": "your-app-name",
      "type": "web",
      "entrypoint": "dist/index.html"
    }
  ]
}
```

The `applications` field is an array of application objects with the following properties:

| Property | Type | Description |
| --- | --- | --- |
| `name` | string | The name of your application, which will be used in the URL (`name.publicnamespace.viamapps.com`) |
| `type` | string | The type of application (currently only `"web"` is supported) |
| `entrypoint` | string | The path to the HTML entry point for your application |

#### Entrypoint examples

The `entrypoint` field specifies the path to your application's entry point. Here are some examples:

- `"dist/index.html"` - Static content rooted at the `dist` directory
- `"dist/foo.html"` - Static content rooted at the `dist` directory, with `foo.html` as the entry point
- `"dist/"` - Static content rooted at the `dist` directory (assumes `dist/index.html` exists)
- `"dist/bar/foo.html"` - Static content rooted at `dist/bar` with `foo.html` as the entry point

### 3. Upload your module

Package your module with your application included and upload it to the Viam Registry:

```bash
viam module build local
viam module upload module.tar.gz
```

## Accessing your Single Page App

Once your module with the application configuration is uploaded and approved, your application will be available at:

```
https://your-app-name.your-public-namespace.viamapps.com
```

Users will be prompted to authenticate with their Viam credentials before accessing your application.

## Application Flow

1. User navigates to `your-app-name.your-public-namespace.viamapps.com`
2. User authenticates with Viam credentials
3. User selects an organization, location, and machine
4. User is redirected to `your-app-name.your-public-namespace.viamapps.com/machine/{machine-id}`
5. Your application is rendered with access to the selected machine

## API Changes

The Single Page Apps feature introduces the following API changes:

### App Object

```protobuf
message App {
  string name = 1;
  string type = 2;
  string entrypoint = 3;
}
```

### UpdateModuleRequest

```protobuf
message UpdateModuleRequest {
  string module_id = 1;
  Visibility visibility = 2;
  string url = 3;
  string description = 4;
  repeated Model models = 5;
  string entrypoint = 6;
  optional string first_run = 7;
  repeated App apps = 8;
}
```

### GetAppContentRequest/Response

```protobuf
message GetAppContentRequest {
  string public_namespace = 1;
  string name = 2;
}

message GetAppContentResponse {
  string url = 1;
}
```

## Limitations

- Single Page Apps currently only support single-machine applications
- All modules with apps must have public visibility
- There is no versioning or separate deploy step; the page will always render the latest version
- Browsers with cookies disabled are not supported

## Security Considerations

- Customer apps are stored in GCS buckets that are publicly available on the internet
- Avoid uploading sensitive information in your application code or assets
- API keys and secrets are stored in the browser's localStorage or sessionStorage

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