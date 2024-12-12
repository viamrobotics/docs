---
linkTitle: "Integrate other hardware"
title: "Integrate other hardware"
weight: 30
layout: "docs"
type: "docs"
no_list: true
description: "Add support for more hardware to the Viam ecosystem."
---

If your hardware is not [already supported](../supported-hardware/) by an existing {{< glossary_tooltip term_id="module" text="module" >}}, you can create a new module to add support for it.
You can keep the module private or share it with your organization or the public.
You can use built-in tools to manage versioning and deployment to machines as you iterate on your module.

{{% alert title="In this page" color="info" %}}

1. [Design your module](#design-your-module)
1. [Write your module](#write-your-module)
1. [Test your module locally](#test-your-module-locally)
1. [Upload your module](#upload-your-module)

{{% /alert %}}
{{% alert title="See also" color="info" %}}

- [Write a module for microcontrollers (to use alongside viam-micro-server)](./micro-module/)
- [Hello World guide to writing a module with Python or Go](./hello-world-module/)
- [Write a module with C++](./cpp-module/)
- [Update and manage modules](./manage-modules/)

{{% /alert %}}

## Design your module

### Write a test script (optional)

You can think of a module as a packaged wrapper around some script, that takes the functionality of the script and maps it to a standardized API for use within the Viam ecosystem.
Start by finding or writing a test script to check that you can connect to and control your hardware from your computer, perhaps using the manufacturer's API or other low-level code.

### Choose an API

Decide exactly what functionality you want your module to provide in terms of inputs and outputs.
With this in mind, look through the [component APIs](/dev/reference/apis/#component-apis) and choose one that fits your use case.

For example, if you just need to get readings or other data and don't need any other endpoints, you could use the [sensor API](/dev/reference/apis/components/sensor/), which contains only the `GetReadings` method (as well as the methods that all Viam resources implement: `Reconfigure`, `DoCommand`, `GetResourceName`, and `Close`).

### Decide on configuration attributes and dependencies

Make a list of required and optional attributes for users to configure when adding your module to a machine.
For example, if users will need to configure things such as a path from which to access data, or a pin to which a device is wired, you'll need to add these attributes to the `Validate` and `Reconfigure` functions when you write the module.

{{< expand "Explicit versus implicit dependencies" >}}

Some modules require that other modules start first.
For example, a mobile robotic base might need its motors to start up before the overall base module initializes.
If your use case requires that things initialize in a specific order, you have two options:

- Explicit dependencies: Require that a user list the names of all resources that must start before a given component in the `depends_on` field of the component's configuration.
  - Useful when dependencies are optional.
- Implicit dependencies: Instead of explicitly using the `depends_on` field, require users to configure a named attribute (for example `"left-motor": "motor1"`), and write your module with that attribute as a dependency.
  Note that most named attributes are _not_ dependencies; you need to specify a resource as not only an attribute but also a dependency for it to be initialized first.
  See code examples below.
  - This is the preferred method when dependencies are required, because implicit dependencies make it more clear what needs to be configured, they eliminate the need for the same attribute to be configured twice, and they make debugging easier.

{{< /expand >}}

## Write your module

### Generate stub files

The easiest way to generate the files for your module is to use the [Viam CLI](/cli/):

1. Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

   {{< expand "Install the Viam CLI and authenticate" >}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate
   ```

1. Follow the prompts.
   Find more information in the following table:

<!--prettier-ignore-->
| Prompt | Description |
| -------| ----------- |
| Module name | The module name describes the module or the family of devices it supports. It is generally the same as the name of the GitHub repo where you will put your module code. |
| Language | The language for the module. |
| Visibility | Choose `Private` to share only with your organization, or `Public` to share publicly with all organizations. If you are testing, choose `Private`. |
| Namespace/Organization ID | In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page. Find the **Public namespace** and copy that string. |
| Resource to add to the module (API) | The [component API](/appendix/apis/#component-apis) your module will implement. |
| Model name | Name your component model based on what it supports, for example, if it supports a model of ultrasonic sensor called “XYZ Sensor 1234” you could call your model `XYZ_1234` or similar. |
| Enable cloud build | You can select `No` if you will always build the module yourself before uploading it. If you select `Yes` and push the generated files (including the <file>.github</file> folder) and create a release of the format `vX.X.X`, the module will build and upload to the Viam registry and be available for all Viam-supported architectures without you needing to build for each architecture. |
| Register module | Select `Yes` unless you are creating a local-only module for testing purposes and do not intend to upload it. |

The generator will create a folder containing stub files for your modular sensor component.
In the next section, you'll customize some of the generated files to support your sensor.

### Implement the component API

## Test your module locally

## Upload your module
