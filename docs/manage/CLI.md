---
title: "Viam CLI"
linkTitle: "CLI"
weight: 99
type: "docs"
no_list: true
description: "Manage and control your robots from the command line."
aliases:
    - "/program/cli"
---

The Viam CLI (command line interface) tool enables you to manage your robots and modular resources across organizations and locations from the command line.
The CLI lets you:

* Retrieve [organization](/manage/fleet/organizations/) and location information
* Manage [robot fleet](/manage/fleet/) data and logs
* Control robots by issuing component and service commands
* Upload and manage [modular resources](/extend/modular-resources/) in the Viam Registry

For example, this CLI command moves a servo to the 75 degree position:

```sh {class="command-line" data-prompt="$"}
viam robot part run --robot 82c608a-1be9-46a5 --organization "Robot's Org" \
--location myLoc --part "myrobot-main" --data '{"name": "myServo", "angle_deg":75}' \
viam.component.servo.v1.ServoService.MoveRequest
```

## Install

You can download the Viam CLI executable using one of the options below.
Select the tab for your platform and architecture.

{{% alert title="Tip" color="tip" %}}
You can use the `uname -m` command to determine your system architecture.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

To download the Viam CLI on a Linux computer with the `aarch64` architecture, run the following commands:

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

To download the Viam CLI on a Linux computer with the `amd64` (Intel `x86_64`) architecture, run the following commands:

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="macOS arm64" %}}

To download the Viam CLI on a macOS computer with the `arm64` (Apple Silicon) architecture, run the following commands:

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-darwin-arm64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="macOS x86_64" %}}

To download the Viam CLI on a macOS computer with the `amd64` (Intel `x86_64`) architecture, run the following commands:

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-darwin-amd64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Source" %}}

If you have [Go installed](https://go.dev/doc/install), you can build the Viam CLI directly from source using the `go install` command:

```sh {class="command-line" data-prompt="$"}
go install go.viam.com/rdk/cli/viam@latest
```

To confirm `viam` is installed and ready to use, issue the *viam* command from your terminal.
If you see help instructions, everything is correctly installed.
If you do not see help instructions, add your local <file>go/bin/*</file> directory to your `PATH` variable.
If you use `bash` as your shell, you can use the following command:

```sh {class="command-line" data-prompt="$"}
echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

{{% /tab %}}
{{< /tabs >}}

To later update the Viam CLI tool, you can use the steps above to reinstall the latest version.

## Authenticate

Once you have successfully installed the Viam CLI, you need to authenticate your device for CLI usage with your Viam app account before you can control your robots with the CLI.
Do this by issuing the command:

```sh {class="command-line" data-prompt="$"}
viam login
```

This will open a new browser window with a prompt to start the authentication process.
If a browser window does not open, the CLI will present a URL for you to manually open in your browser.
Follow the instructions to complete the authentication process.

{{% alert title="Info" color="info" %}}
An authenticated session is valid for 24 hours, unless you explicitly [log out](#logout).

After the session expires or you log out, you must re-authenticate to use the CLI again.
{{% /alert %}}

## Manage your robots with the Viam CLI

With the Viam CLI [installed](#install) and [authenticated](#authenticate), you can use it to issue commands to your robot fleet or manage custom modules.
All Viam CLI commands use the following format:

```sh {class="command-line" data-prompt="$"}
viam [global options] command [command options] [arguments...]
```

|        parameter     |       description      |
| ----------- | ----------- |
| [global options](#global-options)      | *optional* - list of flags that apply for commands      |
| [command](#commands)  | *required* - the specific CLI command to run        |
| command options   | *required for some commands*  - the operation to run for the specified command.     |
| arguments   | *required for some commands* - the arguments for the specified command operation. Some commands take positional arguments, some named arguments.     |

See the list of [commands](#commands) below.

### CLI help

The Viam CLI has a built-in help system that lists all available commands.
You can access it at any time by issuing the command:

```sh {class="command-line" data-prompt="$"}
viam help
```

You can also access contextual help by passing `help` as a command option for any CLI command, for example:

```sh {class="command-line" data-prompt="$"}
viam organizations help
```

## Commands

### `data`

The `data` command allows you to manage robot data.
With it, you can export data in the format of your choice or delete specified data.
You can filter the data this command operates on.

```sh {class="command-line" data-prompt="$"}
viam data export --destination=<output path> --data-type=<output data type> [...named args]
viam data delete [...named args]
```

Examples:

```sh {class="command-line" data-prompt="$"}
# export tabular data to /home/robot/data for org abc, location 123
viam data export --destination=/home/robot/data --data_type=tabular \
--org-ids=abc --location-ids=123

# export binary data from all orgs and locations, component name myComponent
viam data export --destination=/home/robot/data --data-type=binary \
--component-name myComponent
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `export`      | export data in a specified format to a specified location  | - |
| `delete`      | delete data  | - |
| `help`      | return help      | - |

##### Named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--destination`      | output directory for downloaded data       |`export`|true |
| `--data-type`     |  data type to be downloaded: either binary or tabular   |`export`|true |
| `--component-name`      | filter by specified component name  |`export`, `delete`| false |
| `--component-type`     | filter by specified component type       |`export`, `delete`|false |
| `--component-model`   | filter by specified component model       |`export`, `delete`|false |
| `--start`      | ISO-8601 timestamp indicating the start of the interval       |`export`, `delete`|false |
| `--end`      | ISO-8601 timestamp indicating the end of the interval       |`export`, `delete`|false |
| `--location-ids`      | filter by specified location id (accepts comma-separated list)       |`export`, `delete`|false |
| `--method`       | filter by specified method       |`export`, `delete`|false |
| `--mime-types`      | filter by specified MIME type (accepts comma-separated list)       |`export`, `delete`|false |
| `--org-ids`     | filter by specified organizations id (accepts comma-separated list)       |`export`, `delete`|false |
| `--parallel`      | number of download requests to make in parallel, with a default value of 10       |`export`, `delete`|false |
| `--part-id`      | filter by specified part id      |`export`, `delete`|false |
| `--part-name`     | filter by specified part name       |`export`, `delete`|false |
| `--robot-id`     | filter by specified robot id       |`export`, `delete`|false |
| `--robot-name`      | filter by specified robot name       |`export`, `delete`|false |
| `--tags`      | filter by specified tag (accepts comma-separated list)       |`export`, `delete`|false |

### `locations`

The `locations` command lists all locations that the authenticated session has access to, grouped by organization.
You can filter results by organization.

```sh {class="command-line" data-prompt="$"}
viam locations list [<organization id>]
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `list`      | list all locations (name and id) that the authenticated session has access to, grouped by organization  | **organization id** : return results for specified organization only |
| `help`      | return help      | - |

### `login`

The `login` command helps you authorize your device for CLI usage. See [Authenticate](#authenticate).

```sh {class="command-line" data-prompt="$"}
viam login
viam login print-access-token
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `print-access-token`      | prints the access token the CLI uses during an authenticated CLI session      | - |
| `help`      | return help      | - |

### `logout`

The `logout` command ends an authenticated CLI session

```sh {class="command-line" data-prompt="$"}
viam logout
```

### module

The `module` command allows to you to manage custom modules.
This includes:

* Creating a new custom modular resource on your local filesystem
* Updating an existing module with new changes
* Uploading a new module to the Viam Registry
* Updating an existing module in the Viam Registry

```sh {class="command-line" data-prompt="$"}
viam module create --organization=<org name> --name <module-id>
viam module update --organization=<org name> --name <module-id>
viam module upload --organization=<org name> --name <module-id> --platform <platform> --version <version> --module meta.json <packaged-module.tar.gz>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# create a new module named 'my-module' in organization 'abc':
viam module create --organization='abc' --name 'my-module'

# update the existing 'my-module' module with new changes to meta.json:
viam module update --organization='abc' --name 'my-module'

# upload a new or updated custom module 'my-module' to the Viam Registry:
viam module upload --organization='abc' --platform "darwin/amd64" --version "1.0.0-rc1" --module meta.json packaged-module.tar.gz
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `create`    | create a new custom module on your local filesystem  | - |
| `update`    | update an existing custom module on your local filesystem with recent changes to <file>meta.json</file> | - |
| `upload`    | upload a new or existing custom module on your local filesystem to the Viam Registry |
| `help`      | return help      | - |

##### Named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--organization`      | organization name that the robot belongs to       |`create`, `update`, `upload`|true |
| `--name`     |  name of the custom module to be created, updated, or uploaded    |`create`, `update`|true |
| `--platform`      |  the platform to encode the resulting module binary as   |`upload`|true |
| `--version`      |  the version of your module to set for this upload  |`upload`|true |
| `--module`      |  the payload of the module to upload, including the <file>meta.json</file> configuration file and the packaged module as a `tar.gz` file    |`upload`|true |

##### Custom module creation workflow example

To upload a new module to the Viam Registry, you need to `create` it with a new name, `update` it with your customized changes, and `upload` it to the Viam Registry.
The following example demonstrates this workflow for an example module `my-first-module`:

```sh {class="command-line" data-prompt="$"}
## Create a new module 'my-first-module' locally, which creates a placeholder `meta.json` file on the local filesystem:
viam module create --name 'my-first-module' --org_id 'abc'
## Edit the newly-created meta.json file with the custom module-specific configuration:
vi meta.json
## Update the module with the new configuration:
viam module update --name 'my-first-module' --org_id 'abc'
## Upload the new custom module to the Viam Registry:
viam module upload --org_id 'abcbacbacbacbacbacbacbac' --platform "darwin/amd64" --version "1.0.0" --module meta.json packaged-module.tar.gz
```

To later make changes to the module, the workflow is similar:

```sh {class="command-line" data-prompt="$"}
## Edit the same meta.json file from the previous workflow with the new configuration:
vi meta.json
## Update the module with the new configuration:
viam module update --name 'my-first-module' --org_id 'abc'
## Upload the new custom module to the Viam Registry:
viam module upload --org_id 'abcbacbacbacbacbacbacbac' --platform "darwin/amd64" --version "1.0.1" --module meta.json packaged-module.tar.gz
```

### organizations

The *organizations* command lists all organizations that the authenticated session belongs to.

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `list`      | list all organizations (name and id) that the authenticated session belongs to    | - |
| `help`      | return help      | - |

### `robot`

The `robot` command allows you to manage your robot fleet.
This includes:

* Retrieving robot and robot part status
* Retrieving robot and robot part logs
* Controlling a robot by issuing component and service commands
* Accessing your robot with a secure shell (when this feature is enabled)

```sh {class="command-line" data-prompt="$"}
viam robot status --organization=<org name> --location=<location name> --robot=<robot id>
viam robot logs --organization=<org name> --location=<location name> --robot=<robot id> [...named args]
viam robot part status --organization=<org name> --location=<location name> --robot=<robot id>
viam robot part run --organization=<org name> --location=<location name> --robot=<robot id> [--stream] --data <meth>
viam robot part shell --organization=<org name> --location=<location name> --robot=<robot id>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# get robot status
viam robot status  --robot 82c608a-1be9-46a5-968d-bad3a8a6daa --organization "Robot's Org" --location myLoc

# stream error level logs from a robot part
viam robot part logs --robot 82c608a-1be9-46a5-968d-bad3a8a6daa \
--organization "Robot's Org" --location myLoc --part "myrover-main" --tail true

# stream classifications from a robot part every 500 milliseconds from the Viam Vision Service with classifier "stuff_detector"
viam robot part run --robot 82c608a-1be9-46a5-968d-bad3a8a6daa \
--organization "Robot's Org" --location myLoc --part "myrover-main" --stream 500ms \
--data '{"name": "vision", "camera_name": "cam", "classifier_name": "stuff_detector", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `status`      | retrieve robot status for a specified robot  | - |
| `logs`      | retrieve logs for a specified robot | - |
| `part`      | manage a specified robot part  | `status`, `run`, `logs`, `shell` (see [positional arguments: part](#positional-arguments-part)) |
| `help`      | return help      | - |

##### Positional arguments: `part`

|        argument     |       description
| ----------- | ----------- | -----------
| `status`     | retrieve robot status for a specified robot part
| `run`     |  run a component or service command, optionally at a specified interval. For commands that return data in their response, you can use this to stream data.
| `logs`     |  get logs for the specified robot part
| `shell`     |  access a robot part securely using a secure shell. This feature must be enabled.
| `help`      | return help

##### Named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--organization`      | organization name that the robot belongs to       |`status`, `logs`, `part`|true |
| `--location`     |  location name that the robot belongs to    |`status`, `logs`, `part`|true |
| `--robot`      |  robot id for which the command is being issued   |`status`, `logs`, `part`|true |
| `--errors`      |  boolean, return only errors (default: false)   |`logs`|false |
| `--part`      |  part name for which the command is being issued    |`logs`|false |
| `--tail`     |  tail (stream) logs, boolean(default false)    |`part logs`|false |
| `--stream`      |  if specified, the interval in which to stream the specified data, for example, 100ms or 1s    |`part run`|false |
| `--data`      |  command data for the command being request to run (see [data argument](#using-the---stream-and---data-arguments))   |`part run`|true |

##### Using the `--stream` and `--data` arguments

Issuing the `part` command with the `run` positional argument allows you to run component and service (resource) commands for a selected robot part.

The `--data` parameter is required and you must specify both:

* Method arguments in JSON format
* A resource method (in the form of the {{< glossary_tooltip term_id="protobuf" text="protobuf" >}} package and method path)

The format of what is passed to the `--data` argument is:

```sh {class="command-line" data-prompt="$"}
'{"arg1": "val1"}' <protobuf path>
```

You can find the protobuf path for the Viam package and method in the [Viam api package](https://github.com/viamrobotics/api/tree/main/proto/viam) by navigating to the component or service directory and then clicking on the resource file. The protobuf path is the package name.

For example:

```sh {class="command-line" data-prompt="$"}
'{"name": "vision", "camera_name": "cam", "classifier_name": "my_classifier", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

The `--stream` argument, when included in the CLI command prior to the `--data` command, will stream data back at the specified interval.

### `robots`

The `robots` command lists all robots that the authenticated session has access to, filtered by organization and location.

```sh {class="command-line" data-prompt="$"}
viam robots list
```

#### Command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `list`      | list all robots (name and id) that the authenticated session has access to in the specified organization and location  |- |
| `help`      | return help|-|

##### Named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--organization`     | organization name to filter by       |list|true |
| `--location`    |  location name to filter by   |list|true |

### `whoami`

The `whoami` command returns the Viam user for an authenticated CLI session, or "Not logged in" if there is no authenticated session.

```sh {class="command-line" data-prompt="$"}
viam whoami
```

## Global options

You can pass global options after the `viam` CLI keyword with any command.

|        global option     |       description |
| ----------- | ----------- |
| `--debug` | enable debug logging (default: false) |
