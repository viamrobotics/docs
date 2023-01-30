---
title: "Viam CLI"
linkTitle: "CLI"
weight: 99
type: "docs"
description: "Manage and control your robots from the command line."
---

The Viam CLI (command line interface) tool enables you to manage your robots across organizations and locations from the command line.
The CLI lets you:

* Retrieve organization and location information
* Manage robot fleet data and logs
* Control robots by issuing component and service commands.

For example, this CLI command moves a servo to the 75 degree position:

``` bash
viam robot part run --robot 82c608a-1be9-46a5 --organization "Robot's Org" \
--location myLoc --part "myrobot-main" --data '{"name": "myServo", "angle_deg":75}' \
viam.component.servo.v1.ServoService.MoveRequest
```

## Install

If you have [Go installed](https://go.dev/doc/install), you can install the Viam CLI with the 'go install' command:

``` bash
go install go.viam.com/rdk/cli/cmd@latest
```

To confirm `viam` is installed and ready to use, issue the *viam* command from your terminal.
If you see help instructions, everything is correctly installed.
If you do not see help instructions, add your local go *bin/* directory to your `PATH` variable. If you use `bash` as your shell, you can use the following command:

``` bash
echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

{{% alert title="Tip" color="tip" %}}
If you are using a shell other than bash, you may need to modify the above command.
{{% /alert %}}

## Authenticate

Once you have successfully installed the Viam CLI, you need to authenticate your device for CLI usage with your Viam app account before you can control your robots with the CLI.
Do this by issuing the command:

``` bash
viam auth
```

This will open a new browser window with a prompt to start the authentication process.
If a browser window does not open, the CLI will present a URL for you to manually open in your browser.
Follow the instructions to complete the authentication process.

A successfully authenticated session is valid for 24 hours, unless you explicitly [log out](#logout).

## Manage your robots with the Viam CLI

With the Viam CLI installed and authenticated, you can use it to issue commands to your robot fleet.
All Viam CLI commands use the following format:

viam [global options] command [command options] [arguments...]

|        parameter     |       description      |
| ----------- | ----------- |
| [global options](#global-options)      | *optional* - list of flags that apply for commands      |
| [command](#commands)  | *required* - the specific CLI command to run        |
| command options   | *required for some commands*  - the operation to run for the specified command.     |
| arguments   | *required for some commands* - the arguments for the specified command operation. Some commands take positional arguments, some named arguments .     |

### CLI help

The Viam CLI has a built-in help system that lists all available commands. You can access it at any time by issuing the command:

``` bash
viam help
```

You can also access contextual help by passing `help` as a command option for any CLI command, for example:

``` bash
viam organizations help
```

## Commands

### auth

The *auth* command helps you authorize your device for CLI usage.  See [Authenticate](#authenticate)

#### synopsis

``` bash
viam auth
viam auth print-access-token
```

#### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| print-access-token      | prints the access token the CLI uses during an authenticated CLI session      | - |
| help      | return help      | - |

### data

The *data* command allows you to manage robot data.
This includes exporting data in the format of your choice and deleting selected data.
All data management commands can target specifically filtered data from across your robot fleet.

#### synopsis

``` bash
viam data export --destination=<output path> --data-type=<output data type> [...named args]
viam data delete [...named args]
```

Examples:

``` bash
# export tabular data to /home/robot/data for org abc, location 123
viam data export --destination=/home/robot/data --data_type=tabular \
--org_ids=abc --location_ids=123

# export binary data from all orgs and locations, component name myComponent
viam data export --destination=/home/robot/data --data_type=tabular \
--component_name myComponent
```

#### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| export      | export data in a specified format to a specified location  | - |
| delete      | delete data  | - |
| help      | return help      | - |

##### named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| --destination      | output directory for downloaded data       |export|true |
| --data_type     |  data type to be downloaded: either binary or tabular   |export|true |
| --component_name      | filter by specified component name  |export, delete| false |
| --component_type     | filter by specified component type       |export, delete|false |
| --component_model   | filter by specified component model       |export, delete|false |
| --start      | ISO-8601 timestamp indicating the start of the interval       |export, delete|false |
| --end      | ISO-8601 timestamp indicating the end of the interval       |export, delete|false |
| --location_ids      | filter by specified location id (accepts comma-separated list)       |export, delete|false |
| --method       | filter by specified method       |export, delete|false |
| --mime_types      | filter by specified MIME type (accepts comma-separated list)       |export, delete|false |
| --org_ids     | filter by specified organizations id (accepts comma-separated list)       |export, delete|false |
| --parallel      | number of download requests to make in parallel, with a default value of 10       |export, delete|false |
| --part_id      | filter by specified part id      |export, delete|false |
| --part_name     | filter by specified part name       |export, delete|false |
| --robot_id     | filter by specified robot id       |export, delete|false |
| --robot_name      | filter by specified robot name       |export, delete|false |
| --tags      | filter by specified tag (accepts comma-separated list)       |export, delete|false |

### locations

The *locations* command lists all locations that the authenticated session has access to, grouped by organization.
Results can be filtered by organization.

#### synopsis

``` bash
viam locations list [<organization id>]
```

#### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| list      | list all locations (name and id) that the authenticated session has access to, grouped by organization  | **organization id** : return results for specified organization only |
| help      | return help      | - |

### logout

The `logout` command ends an authenticated CLI session

#### synopsis

``` bash
viam logout
```

### organizations

The *organizations* command lists all organizations that the authenticated session belongs to.

#### synopsis

``` bash
viam organizations list
```

#### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| list      | list all organizations (name and id) that the authenticated session belongs to    | - |
| help      | return help      | - |

### robot

The *robot* command allows you to manage your robot fleet.
This includes:

* Retrieving robot and robot part status
* Retrieving robot and robot part logs
* Controlling a robot by issuing component and service commands
* Accessing your robot via secure shell (when this feature is enabled)

#### synopsis

``` bash
viam robot status --organization=<org name> --location=<location name> --robot=<robot id>
viam robot logs --organization=<org name> --location=<location name> --robot=<robot id> [...named args]
viam robot part status --organization=<org name> --location=<location name> --robot=<robot id>
viam robot part run --organization=<org name> --location=<location name> --robot=<robot id> [--stream] --data <meth>
viam robot part shell --organization=<org name> --location=<location name> --robot=<robot id>
```
##### examples

``` bash
# get robot status
viam robot status  --robot 82c608a-1be9-46a5-968d-bad3a8a6daa --organization "Robot's Org" --location myLoc

# stream error level logs from a robot part
viam robot part logs --robot 82c608a-1be9-46a5-968d-bad3a8a6daa \
--organization "Robot's Org" --location myLoc --part "myrover-main" --tail true

# stream classifications from a robot part every 500 milliseconds from the Viam vision service with classifier "stuff_detector"
viam robot part run --robot 82c608a-1be9-46a5-968d-bad3a8a6daa \
--organization "Robot's Org" --location myLoc --part "myrover-main" --stream 500ms \
--data '{"name": "vision", "camera_name": "cam", "classifier_name": "stuff_detector", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

#### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| status      | retrieve robot status for a specified robot  | - |
| logs      | retrieve logs for a specified robot | - |
| part      | manage a specified robot part  | status, run, logs, shell (see [part positional arguments](#part---positional-arguments)) |
| help      | return help      | - |

##### part - positional arguments

|        argument     |       description
| ----------- | ----------- | -----------
| status     | retrieve robot status for a specified robot part  
| run     |  run a component or service command, optionally at a specified interval.  For commands that return data in their response, you can use this to stream data.
| logs     |  get logs for the specified robot part
| shell     |  access a robot part securely via secure shell.  This feature must be enabled.
| help      | return help

##### named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| --organization      | organization name that the robot belongs to       |status, logs, part|true |
| --location     |  location name that the robot belongs to    |status, logs, part|true |
| --robot      |  robot id for which the command is being issued   |status, logs, part|true |
| --errors      |  boolean, return only errors (default: false)   |logs|false |
| --part      |  part name for which the command is being issued    |logs|false |
| --tail     |  tail (stream) logs, boolean(default false)    |part(logs)|false |
| --stream      |  if specified, the interval in which to stream the specified data, e.g. 100ms or 1s    |part(run)|false |
| --data      |  command data for the command being request to run (see [data argument](#part-run---stream-and---data-arguments))   |part(run)|true |

##### part run --stream and --data arguments

Issuing the *part* command with the *run* positional argument allows you to run component and service (resource) commands for a selected robot part.

The --data parameter is required and you must specify both:

* Method arguments in JSON format
* A resource method (in the form of the protobuf package and method path)

The format of what is passed to the --data argument is:

``` bash
'{"arg1": "val1"}' <protobuf path>
```

The protobuf path for the Viam package and method can be found in the [Viam api package](https://github.com/viamrobotics/api/tree/main/proto/viam)

For example:

``` bash {linenos=false}
'{"name": "vision", "camera_name": "cam", "classifier_name": "my_classifier", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

The `--stream` argument, when included in the CLI command prior to the `--data` command will streams data back at the specified interval.

### robots

The *robots* command lists all robots that the authenticated session has access to, filtered by organization and location.

#### synopsis

``` bash
viam robots list
```

#### command options

|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| list      | list all robots (name and id) that the authenticated session has access to in the specified organization and location  |- |
| help      | return help|-|

##### named arguments

|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| --organization     | organization name to filter by       |list|true |
| --location    |  location name to filter by   |list|true |

### whoami

The *whoami* command returns the Viam user for an authenticated CLI session, or "Not logged in" if there is no authenticated session.

#### synopsis

``` bash
viam whoami
```

## Global options

You can pass global options after the *viam* CLI keyword with any command.

|        global option     |       description |
| ----------- | ----------- |
| --debug | enable debug logging (default: false) |
