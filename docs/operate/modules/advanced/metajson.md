---
title: "meta.json reference"
linkTitle: "meta.json reference"
weight: 40
layout: "docs"
type: "docs"
description: "Reference for the meta.json file, module naming, models, and applications."
aliases:
  - /operate/modules/create-module/metajson/
  - /operate/reference/naming-modules/
  - /operate/modules/other-hardware/naming-modules/
  - /operate/modules/advanced/module-naming/
date: "2025-11-11"
---

The <file>meta.json</file> file is a JSON file that describes your {{< glossary_tooltip term_id="module" text="module" >}}.
It contains information about the module, such as its name, version, and the resource {{< glossary_tooltip term_id="model" text="models" >}} it provides.

The <file>meta.json</file> file has the following fields:

{{< readfile "/static/include/metajson.md" >}}

## Applications

{{< readfile "/static/include/applications.md" >}}

### Valid application identifiers

If your module includes a [Viam application](/operate/control/viam-applications/), you need to define the application name in your module's [`meta.json`](/operate/modules/advanced/metajson/) file.
Application names have the following requirements:

- Application names must be all-lowercase.
- Application names may only use alphanumeric (`a-z` and `0-9`) and hyphen (`-`) characters.
- Application names may not start or end with a hyphen.
- Application names must be unique within your organization's namespace.

The URL for accessing your Viam app will contain your application name:

```txt
https://app-name_your-public-namespace.viamapps.com
```

For example, if your organization namespace is `acme` and your application name is `dashboard`, your application will be accessible at:

```txt
https://dashboard_acme.viamapps.com
```

## Create a namespace for your organization

When uploading modules to the Viam Registry, you must set a unique namespace for your organization to associate your module with.

To create a new namespace for your organization, click on the org's **Settings** in the top right of the navigation bar, then click the **Set a public namespace** button.
Enter a name or use the suggested name for your namespace, and then click **Set namespace**.
A namespace may only contain letters, numbers, and the dash (`-`) character.

## Update a namespace for your organization

You can change your organization's namespace on your organization settings page:

1. Navigate to your organization settings page using the dropdown in the upper right corner of the web UI.
1. Click the **Rename** button next to your current namespace.
1. Enter the new namespace name in the field that appears.
1. Click **Rename** to confirm the change.
1. For each module your organization owns, update the module code and <file>meta.json</file> to reflect the new namespace.
1. (Recommended) Update the `model` field in the configuration of any machines that use the module to use the new namespace.
   Machine configurations that reference the old namespace will continue to work, but we recommend updating them to use the new namespace to avoid confusion.

When you rename a namespace, Viam reserves the old namespace for backwards compatibility and you cannot reuse it.
