---
linkTitle: "Manage your fleet"
title: "Manage your fleet with the CLI"
weight: 60
layout: "docs"
type: "docs"
description: "Monitor machines, view logs, access remote shells, and deploy software from the command line."
---

Monitor machine status, stream logs, connect to remote machines with a shell, copy files, and deploy software packages across your fleet.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

To find your organization ID and location IDs:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

```sh {class="command-line" data-prompt="$"}
viam locations list
```

To find machine IDs and part IDs:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --location=<location-id>
```

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine=<machine-id>
```

## List and monitor machines

List all machines in a location:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --location=<location-id>
```

List all machines across your organization:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --all
```

Check the status of a specific machine:

```sh {class="command-line" data-prompt="$"}
viam machines status --machine=<machine-id>
```

## View logs

Stream logs from a machine:

```sh {class="command-line" data-prompt="$"}
viam machines logs --machine=<machine-id>
```

Stream logs from a specific part:

```sh {class="command-line" data-prompt="$"}
viam machines part logs --part=<part-id>
```

Show only errors:

```sh {class="command-line" data-prompt="$"}
viam machines part logs --part=<part-id> --errors
```

Follow logs in real time:

```sh {class="command-line" data-prompt="$"}
viam machines part logs --part=<part-id> --tail
```

## Shell into a machine

Open an interactive shell on a remote machine part.
The connection uses Viam's secure WebRTC channel, not direct SSH. The machine must have a shell service configured.

```sh {class="command-line" data-prompt="$"}
viam machines part shell --part=<part-id>
```

## Copy files to and from machines

File copy uses the same secure connection as shell access, not SSH or SCP.
Use the `machine:` prefix for remote paths.

Copy a file to a machine:

```sh {class="command-line" data-prompt="$"}
viam machines part cp --part=<part-id> local-file.txt machine:/home/user/
```

Copy a file from a machine:

```sh {class="command-line" data-prompt="$"}
viam machines part cp --part=<part-id> machine:/home/user/remote-file.txt ./
```

Copy a directory recursively:

```sh {class="command-line" data-prompt="$"}
viam machines part cp --part=<part-id> -r ./local-dir machine:/home/user/
```

Preserve file permissions and timestamps:

```sh {class="command-line" data-prompt="$"}
viam machines part cp --part=<part-id> -r --preserve ./local-dir machine:/home/user/
```

## Create a tunnel

Forward a local port to a port on a remote machine.
This is useful for accessing web UIs, databases, or other services running on machines that are not directly reachable from your network.

```sh {class="command-line" data-prompt="$"}
viam machines part tunnel \
  --part=<part-id> \
  --local-port=8080 \
  --destination-port=8080
```

## Run component and service methods

Call a gRPC method on a component or service directly from the CLI, like `curl` for Viam's API:

```sh {class="command-line" data-prompt="$"}
viam machines part run \
  --part=<part-id> \
  --data='{"name": "my-sensor"}' \
  rdk.component.sensor.v1.SensorService.GetReadings
```

Stream results at an interval:

```sh {class="command-line" data-prompt="$"}
viam machines part run \
  --part=<part-id> \
  --stream=500ms \
  --data='{"name": "my-camera"}' \
  rdk.component.camera.v1.CameraService.GetImage
```

## Deploy software packages

Upload a package to the Viam registry for deployment to machines:

```sh {class="command-line" data-prompt="$"}
viam packages upload \
  --path=./my-package.tar.gz \
  --name=my-control-logic \
  --version=1.0.0 \
  --type=ml_model
```

Export a package:

```sh {class="command-line" data-prompt="$"}
viam packages export --type=ml_model
```

## Export diagnostics

Export FTDC (Full-Time Diagnostic Data Capture) metrics from a machine:

```sh {class="command-line" data-prompt="$"}
viam machines part get-ftdc --part=<part-id>
```

Parse an FTDC file locally:

```sh {class="command-line" data-prompt="$"}
viam parse-ftdc --path=./ftdc-data
```

## Create API keys for machines

Create an API key scoped to a specific machine:

```sh {class="command-line" data-prompt="$"}
viam machines api-key create --machine-id=<machine-id>
```

The CLI prints the key ID and key value. Save both immediately; the key value is only shown once.

```sh {class="command-line" data-prompt="$" data-output="1-3"}
Successfully created key:
Key ID: abcdef12-3456-7890-abcd-ef1234567890
Key Value: your-secret-key-value
```

## Related pages

- [Monitor machine status](/monitor/monitor/) for monitoring with the Viam app
- [Troubleshoot](/monitor/troubleshoot/) for debugging machine issues
- [Deploy software](/fleet/deploy-software/) for deploying with fragments
- [CLI reference](/dev/tools/cli/#machines-alias-robots-and-machine) for the complete `machines` command reference
