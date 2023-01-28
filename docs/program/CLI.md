---
title: "Command Line Tool"
linkTitle: "Command Line Tool"
weight: 99
type: "docs"
description: "Manage and control your robots from the command line."
---

The Viam CLI (command line interface) tool enables you to manage all your robots across organizations and locations from the command line.
The CLI lets you:

* Retrieve organization and location information
* Manage robot fleet data and logs
* Control robots by issuing component and service commands.

## Install

Currently, the Viam CLI is included [with the RDK open-source repository](https://github.com/viamrobotics/rdk/tree/main/cli).

To use the CLI, first clone the Viam RDK repository with git:

``` bash
git clone https://github.com/viamrobotics/rdk.git
```

Then, from the root of the repository, run the following command to install the CLI:

``` bash
go build -o ~/go/bin/viam cli/cmd/main.go
```

Now, issue the *viam* command from your terminal.
You should see help instructions returned.  If you do not, it is likely that your local go *bin/* path needs to be made available in your environment.
Do this by running:

``` bash
echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

Note that if you are using a shell other than bash, you may need to modify the above command.

## Authenticate

Once you have successfully installed the Viam CLI, you need to authenticate your device for CLI usage with your Viam app account before you can control your robots with the CLI.
Do this by issuing the command:

``` bash
viam auth
```

This will open a new browser window with a prompt to start the authentication process.
If a browser window does not open, the CLI will present a URL for you to manually open in your browser.

<img src="/program/img/cli/auth_start.png"  style="border:1px solid" alt="Viam CLI auth process." title="Viam CLI auth process." width="300" />

After you click confirm, you will be prompted to sign up for Viam if you have not, or sign in if you have an account and are not yet signed in.
After you have successfully been confirmed as logged-in, you will get a success screen, and can now use the Viam CLI.
Your authentication session will be valid for 24 hours, unless you explicitly [log out](#logout).

<img src="/program/img/cli/auth_end.png"  style="float;right;border:1px solid" alt="Viam CLI auth process complete." title="Viam CLI auth process complete." width="300" />

## Manage your robots with the Viam CLI

All Viam CLI calls use the following format:

**viam [global options] command [command options] [arguments...]**

|        parameter     |       description      |
| ----------- | ----------- |
| global options      | *optional* - list of flags that apply for commands      |
| command   | *required* - the specific CLI command to run        |
| command options   | *required for some commands*  - the operation to run for the specified command.     |
| arguments   | *required for some commands* arguments for the specified command operation. Some commands take positional arguments, some named arguments      |

The Viam CLI has a built-in help system that lists all available commands.  It can be accessed at any time by issuing the command:

```
viam help
```

Help can be accessed by passing it as a command option for CLI command, for example:

```
viam organizations help
```

### Commands

#### auth

The *auth* command prompts the user to authorize their device for CLI usage.  See [Authenticate](#authenticate)

##### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| print-access-token      | prints the access token the CLI will use during an authenticated CLI session      | - |
| help      | return help      | - |

#### logout

The *logout* command ends an authenticated CLI session

##### command options

None available.

#### whoami

The *whoami* command returns the Viam user for an authenticated CLI session, or "Not logged in" if there is not an authenticated session.

##### command options

None available.

#### organizations

The *organizations* command lists all organizations that the authenticated user belongs to.

##### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| list      | list all organizations (name and id) that the authenticated user belongs to    | - |
| help      | return help      | - |

#### locations

The *locations* command lists all locations that the authenticated user has access to, grouped by organization.
Results can be filtered by organization.

##### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| list      | list all locations (name and id) that the authenticated user has access to, grouped by organization  | **organization id** : return results for specified organization only |
| help      | return help      | - |

#### data

The *data* command allows you to manage robot data.
This includes exporting data in the format of your choice and deleting selected data.
All data management commands can target specifically filtered data from across your robot fleet.

##### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| export      | export data in a specified format to a specified location  | - |
| delete      | delete data  | - |
| help      | return help      | - |

###### named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| --destination *value*     | output directory for downloaded data       |export|true |
| --data_type *value*     |  data type to be downloaded: either binary or tabular   |export|true |
| --component_name *value*     | filter by specified component name  |export, delete| false |
| --component_type *value*    | filter by specified component type       |export, delete|false |
| --component_model *value*     | filter by specified component model       |export, delete|false |
| --start *value*     | ISO-8601 timestamp indicating the start of the interval       |export, delete|false |
| --end *value*     | ISO-8601 timestamp indicating the end of the interval       |export, delete|false |
| --location_ids *value*     | filter by specified location id (accepts comma-separated list)       |false |
| --method *value*      | filter by specified method       |export, delete|false |
| --mime_types *value*     | filter by specified MIME type (accepts comma-separated list)       |export, delete|false |
| --org_ids *value*     | filter by specified organizations id (accepts comma-separated list)       |export, delete|false |
| --parallel *value*     | number of download requests to make in parallel, with a default value of 10       |export, delete|false |
| --part_id *value*     | filter by specified part id      |export, delete|false |
| --part_name *value*     | filter by specified part name       |export, delete|false |
| --robot_id *value*     | filter by specified robot id       |export, delete|false |
| --robot_name *value*     | filter by specified robot name       |export, delete|false |
| --tags *value*     | filter by specified tag (accepts comma-separated list)       |export, delete|false |

#### robots

The *robots* command lists all robots that the authenticated user has access to, filtered by organization and location.

##### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| list      | list all robots (name and id) that the authenticated user has access to in the specified organization and location  |- |
| help      | return help|-|

###### named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| --organization *value*     | organization name to filter by       |list|true |
| --location *value*     |  location name to filter by   |list|true |

#### robot

The *robot* command allows you to manage your robot fleet.
This includes:

* Retrieving robot and robot part status
* Retrieving robot and robot part logs
* Controlling a robot by issuing component and service commands
* Accessing your robot via secure shell (when this feature is enabled)

##### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| status      | retrieve robot status for a specified robot  | - |
| logs      | retrieve logs for a specified robot | - |
| part      | manage a specified robot part  | status, run, shell (see [part positional arguments](#part---positional-arguments)) |
| help      | return help      | - |

###### part - positional arguments

|        argument     |       description
| ----------- | ----------- | -----------
| status     | retrieve robot status for a specified robot part  
| run     |  run a component or service command, optionally at a specified interval.  For commands that return data in their response, this can be thus be used to stream data at this interval
| shell     |  access a robot part securely via secure shell.  This feature must be enabled.
| help      | return help

###### named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| --organization *value*     | organization name that the robot belongs to       |status,logs,part|true |
| --location *value*     |  location name that the robot belongs to    |status,logs,part|true |
| --robot *value*     |  robot id for which the command is being issued   |status,logs,part|true |
| --errors *value*     |  boolean, return only errors (default: false)   |logs|true |
| --part *value*     |  part name for which the command is being issued    |logs|true |
| --data *value*     |  command data for the command being request to run (see [data argument](#part-run---data-argument))   |part(run)|true |
| --stream *value*     |  part name for which the command is being issued    |part(run)|true |

###### part run - data argument

Issuing the *part* command with the *run* positional argument allows you to run component and service (resource) commands for a selected robot part.

It is required that you specify both the resource command (in the form of the protobuf API command) and the arguments for the specified resource command in JSON format with the *--data* argument.  The format of what is passed to the --data argument is:

```bash
'{"arg1": "val1"}' <protobuf uri>
```

For example:

```
'{"name": "vision", "camera_name": "cam", "classifier_name": "my_classifier", "n":1}' proto.api.service.vision.v1.VisionService.GetClassificationsFromCamera
```
