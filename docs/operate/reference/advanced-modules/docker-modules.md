---
title: "Deploy a module using Docker"
linkTitle: "Docker Modules"
weight: 300
type: "docs"
tags: ["extending viam", "modular resources"]
description: "Deploy a module using Docker."
no_list: true
date: "2025-04-10"
# updated: ""  # When the content was last entirely checked
---

In rare cases, you may need to package and deploy a module using Docker.
Use cases for this include:

- Your module has complex system dependencies that cannot be easily installed on a machine.
- You use a large container image and some layers are already used by your machine which means layer caching can reduce the size of the download.
- You have specific security requirements that are difficult to meet with the default module deployment.

If you choose to deploy your module using Docker, we recommend creating a "first run" script or binary to run any necessary setup steps.
Note this is _not_ recommended for modules that do not use Docker, as it adds unnecessary complexity.

## Use a `first_run` script or binary

1. Create a tarball that contains:

   - The module's entrypoint script or binary, for example:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     #!/bin/bash
     exec docker run <YOUR_CONTAINER_IMAGE> <YOUR_CONTAINER_OPTIONS>
     ```

   - A [<file>meta.json</file>](/operate/modules/advanced/metajson/)
   - A first run script or binary that will be executed during the setup phase, for example:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     #!/usr/bin/env bash

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

1. Configure your module on your machine in the same way you would configure a regular module.
   The first run script will execute once when `viam-server` receives a new configuration.
   It will only execute once per module or per version of the module.<br><br>

1. (Optional) After a first run script runs successfully, Viam adds a marker file in the module's data directory.
   The marker file path format is of the form `unpackedModDir + FirstRunSuccessSuffix`.
   For example, `.viam/packages/data/module/abcd1234-abcd-abcd-abcd-abcd12345678-viam-rtsp-0_1_0-linux-amd64/bin.first_run_succeeded`.

   If you want to force a first run script to run again without changing the configured module or module version, you can do so by deleting this file.<br><br>

1. (Optional) By default, a first run script will timeout after 1 hour.
   This can be adjusted by adding a `first_run_timeout` to the module's configuration.
   For example, `"first_run_timeout": "5m"` will lower the script timeout to 5 minutes.
