---
title: "Advanced Modular Resources"
linkTitle: "Advanced Modules"
type: docs
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Some usage may require you to define new APIs or deploy custom components in non-standard ways."
aliases:
  - /program/extend/
  - /modular-resources/advanced/
  - /registry/advanced/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
toc_hide: true
---

Some use cases may require advanced considerations when designing or deploying modular resources.
Depending on your needs, you may wish to define an entirely new resource API, deploy a custom component using a server on a {{< glossary_tooltip term_id="remote-part" text="remote" >}} {{< glossary_tooltip term_id="part" text="part" >}}, or design a custom ML model.

## New APIs

The [component APIs](/dev/reference/apis/#component-apis) and [service APIs](/dev/reference/apis/#service-apis) provide a standard interface for controlling common hardware components and higher level functionality.
If your use case aligns closely with an existing API, you should use that API to program your new resource.

If you want to use most of an existing API but need just a few other functions, you can use the `DoCommand` endpoint together with [extra parameters](/dev/reference/sdks/use-extra-params/) to add custom functionality to an existing resource API.

Or, if your resource does not fit into an existing resource API, you can use one of the following:

- If you are working with a component that doesn't fit into any of the existing [component APIs](/dev/reference/apis/#component-apis), you can use the [generic component](/operate/reference/components/generic/) to build your own component API.
- If you are designing a service that doesn't fit into any of the existing [service APIs](/dev/reference/apis/#service-apis), you can use the [generic service](/dev/reference/apis/services/generic/) to build your own service API.

Both generic resources use the [`DoCommand`](/dev/reference/apis/components/generic/#docommand) endpoint to enable you to make arbitrary calls as needed for your resource.

Alternatively, you can also [define a new resource API](/operate/reference/advanced-modules/create-subtype/) if none of the above options are a good fit for your use case.

## Custom components as remotes

Running {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} on the computer directly connected to your components is the preferred way of managing and controlling custom components.

However, if you are unable to use modular resources because you need to host `viam-server` on a non-Linux system or have an issue with compilation, you may need to [implement a custom component and register it on a server configured as a remote](/operate/reference/advanced-modules/custom-components-remotes/) on your machine.

## Package and deploy using Docker

In rare cases, you may need to package and deploy a module using Docker.
Use cases for this include:

- Your module has complex system dependencies that cannot be easily installed on a machine.
- You have a large bundle and want to use layer caching to reduce the size of the download.
- You have specific security requirements that are difficult to meet with the default module deployment.

If you choose to deploy your module using Docker, we recommend creating a "first run" script or binary to run any necessary setup steps.

{{% expand "Click for first run script instructions" %}}

1. Create a tarball that contains:

   - The module's entrypoint script or binary
   - A <file>meta.json</file>
   - A first run script or binary that will be executed during the setup phase, for example:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     #!/usr/bin/env bash

     if [[ -n "$VIAM_TEST_FAIL_RUN_FIRST" ]]; then
         echo "Sorry, I've failed you."
         exit 1
     fi

     docker pull mongo:6

     cat << EOF
     -------------------------------------
     The setup script ran successfully!
     -------------------------------------
     EOF

     exit 0
     ```

   [This example Makefile on GitHub](https://github.com/viam-labs/wifi-sensor/blob/7823b6ad3edcbbbf20b06c34b3181453f5f3f078/Makefile) builds a module binary and bundles it along with a <file>meta.json</file> and first run script.<br><br>

1. Edit the <file>meta.json</file> to include a `first_run` field that points to the first run script or binary.

   ```json
   {
     ...
     "first_run": "first_run.sh"
   }
   ```

1. Configure your module on your machine in the same way as you would for a regular module.
   The first run script will execute once when `viam-server` receives a new configuration.
   It will only execute once per module or per version of the module.

1. (Optional) After a first run script runs successfully, Viam adds a marker file with a `.first_run_succeeded` suffix in the module’s data directory on disk.
   It has the location and form: `/root/.viam/packages/data/module/<MODULE_ID>-<VERSION>-<ARCH>.first_run_succeeded`.
   If you want to force a first run script to run again without changing the configured module or module version, you can do so by deleting this file.

1. (Optional) By default, a first run script will timeout after 1 hour.
   This can be adjusted by adding a `first_run_timeout` to the module’s configuration.
   For example, `"first_run_timeout": "5m"` will lower the script timeout to 5 minutes.

{{% /expand %}}

## Design a custom ML model

When working with the [ML model service](/dev/reference/apis/services/ml/), you can deploy an [existing model](/data-ai/ai/deploy/) or [train your own model](/data-ai/ai/train/).

However, if you are writing your own {{< glossary_tooltip term_id="module" text="module" >}} that uses the ML model service together with the [vision service](/dev/reference/apis/services/vision/), you can also [design your own ML model](/data-ai/reference/mlmodel-design/) to better match your specific use case.
