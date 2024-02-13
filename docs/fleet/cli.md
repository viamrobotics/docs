---
title: "Viam CLI"
linkTitle: "CLI"
weight: 99
type: "docs"
no_list: true
description: "Manage and control your machines from the command line."
aliases:
  - "/build/program/cli"
  - /manage/cli/
---

The Viam CLI (command line interface) tool enables you to manage your machines and {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} across organizations and locations from the command line.
The CLI lets you:

- Retrieve [organization](/fleet/organizations/) and location information
- Manage [machine fleet](/fleet/) data and logs
- Control machines by issuing component and service commands
- Upload and manage [modular resources](/registry/) in the Viam registry

For example, this CLI command moves a servo to the 75 degree position:

```sh {class="command-line" data-prompt="$"}
viam robots part run --robot 82c608a-1be9-46a5 --organization "Robot's Org" \
--location myLoc --part "myrobot-main" --data '{"name": "myServo", "angle_deg":75}' \
viam.component.servo.v1.ServoService.MoveRequest
```

## Install

You can download the Viam CLI executable using one of the options below.
Select the tab for your platform and architecture.
If you are on Linux, you can use the `uname -m` command to determine your system architecture.

{{< tabs >}}
{{% tab name="macOS" %}}

To download the Viam CLI on a macOS computer, run the following commands:

```{class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
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

You can also install the Viam CLI using [brew](https://brew.sh/) on Linux `amd64` (Intel `x86_64`):

```{class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Source" %}}

If you have [Go installed](https://go.dev/doc/install), you can build the Viam CLI directly from source using the `go install` command:

```sh {class="command-line" data-prompt="$"}
go install go.viam.com/rdk/cli/viam@latest
```

To confirm `viam` is installed and ready to use, issue the _viam_ command from your terminal.
If you see help instructions, everything is correctly installed.
If you do not see help instructions, add your local <file>go/bin/\*</file> directory to your `PATH` variable.
If you use `bash` as your shell, you can use the following command:

```sh {class="command-line" data-prompt="$"}
echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

{{% /tab %}}
{{< /tabs >}}

To later update the Viam CLI tool on Linux, use the steps above to reinstall the latest version.
to later update the Viam CLI tool on macOS, run `brew upgrade viam`.

## Authenticate

Once you have [installed the Viam CLI](#install), you must authenticate your CLI session with Viam in order to run CLI commands.

You can authenticate your CLI session using either a personal access token, or an organization, location, or machine part API key.
To use an organization API key to authenticate, you must first [create an organization API key](#create-an-organization-api-key).
Similarly, to authenticate using a location or machine part API key, you must first create a [location](#create-a-location-api-key) or [machine part API key](#create-a-machine-part-api-key).

- To authenticate your CLI session using a personal access token:

  ```sh {class="command-line" data-prompt="$"}
  viam login
  ```

  This will open a new browser window with a prompt to start the authentication process.
  If a browser window does not open, the CLI will present a URL for you to manually open in your browser.
  Follow the instructions to complete the authentication process.

- To authenticate your CLI session using an organization API key:

  ```sh {class="command-line" data-prompt="$"}
  viam login api-key --key-id <organization-api-key-uuid> --key <organization-api-key-secret-value>
  ```

  If you haven't already, [create an organization API key](#create-an-organization-api-key) to use this authentication method.

- To authenticate your CLI session using a location API key:

  ```sh {class="command-line" data-prompt="$"}
  viam login api-key --key-id <location-api-key-uuid> --key <location-api-key-secret-value>
  ```

  If you haven't already, [create a location API key](#create-a-location-api-key) to use this authentication method.

- To authenticate your CLI session using a machine part API key:

  ```sh {class="command-line" data-prompt="$"}
  viam login api-key --key-id <machine-part-api-key-uuid> --key <machine-part-api-key-secret-value>
  ```

  If you haven't already, [create a machine part API key](#create-a-machine-part-api-key) to use this authentication method.

An authenticated session is valid for 24 hours, unless you explicitly [log out](#logout).

After the session expires or you log out, you must re-authenticate to use the CLI again.

### Create an organization API key

To use an organization API key to authenticate your CLI session, you must first create one:

1. First, [authenticate](#authenticate) your CLI session.
   If your organization does not already have an organization API key created, authenticate using a personal access token or either a [location API key](#create-a-location-api-key) or [machine part API key](#create-a-machine-part-api-key).

1. Then, run the following command to create a new organization API key:

   ```sh {class="command-line" data-prompt="$"}
   viam organizations api-key create --org-id <org-id> --name <key-name>
   ```

   Where:

   - `org-id` is your organization ID.
     You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in [the Viam app](https://app.viam.com/).
   - `key-name` is an optional name for your API key.

The command will return a `key id` and a `key value`.
You will need both to authenticate.

{{% alert title="Important" color="note" %}}
Keep these key values safe.
By default, new organization API keys are created with **Owner** permissions, giving the key full read and write access to all robots within your organization.
You can change an API key's permissions from the Viam app on the [organizations page](/fleet/organizations/) by clicking the **Show details** link next to your API key.
{{% /alert %}}

Once created, you can use the organization API key to authenticate future CLI sessions or to [connect to robots with the SDK](/build/program/#authenticate)..
To switch to using an organization API key for authentication right away, [logout](#logout) then log back in using `viam login api-key`.

An organization can have multiple API keys.

### Create a location API key

To use an location API key to authenticate your CLI session, you must first create one:

1. First, [authenticate](#authenticate) your CLI session.
   If you don't already have a location API key created, authenticate using a personal access token, an [organization API key](#create-an-organization-api-key), or a [machine part API key](#create-a-machine-part-api-key).

1. Then, run the following command to create a new location API key:

   ```sh {class="command-line" data-prompt="$"}
   viam locations api-key create --location-id <location-id>
    --org-id <org-id> --name <key-name>
   ```

   Where:

   - `location-id` is your location ID.
     You can find your location ID by running `viam locations list` or by visiting your [robot fleet's page](https://app.viam.com/robots) in the Viam app.
   - `org-id` is an optional organization ID to attach the key to.
     You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in [the Viam app](https://app.viam.com/).
     If only one organization owns the location, you can omit the parameter.
     If multiple organizations own the location, you must specify the `org-id` explicitly.
   - `key-name` is an optional name for your API key.
     If omitted, a name will be auto-generated based on your login info and the current time.

The command will return a `key id` and a `key value`.
You will need both to authenticate.

{{% alert title="Important" color="note" %}}
Keep these key values safe.
By default, new location API keys are created with **Owner** permissions, giving the key full read and write access to all robots within your location.
You can change an API key's permissions from the Viam app on the [organizations page](/fleet/organizations/) by clicking the **Show details** link next to your API key.
{{% /alert %}}

Once created, you can use the location API key to authenticate future CLI sessions or to [connect to robots with the SDK](/build/program/#authenticate).
To switch to using a location API key for authentication right away, [logout](#logout) then log back in using `viam login api-key`.

A location can have multiple API keys.

### Create a machine part API key

To use a machine part API key to authenticate your CLI session, you must first create one:

1. First, [authenticate](#authenticate) your CLI session.
   If you don't already have a machine part API key created, authenticate using a personal access token, an [organization API key](#create-an-organization-api-key), or a [location API key](#create-a-location-api-key).

1. Then, run the following command to create a new machine part API key:

   ```sh {class="command-line" data-prompt="$"}
   viam robots api-key create --robot-id <robot-id> --org-id <org-id> --name <key-name>
   ```

   Where:

   - `robot-id` is your machine's ID.
     You can find your machine ID by running `viam robots list`.
   - `org-id` is an optional organization ID to attach the key to.
     You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in [the Viam app](https://app.viam.com/).
     If only one organization owns the robot, you can omit the parameter.
     If multiple organizations own the robot, you must specify the `org-id` explicitly.
   - `key-name` is an optional name for your API key.
     If omitted, a name will be auto-generated based on your login info and the current time.

The command will return a `key id` and a `key value`.
You will need both to authenticate.

{{% alert title="Important" color="note" %}}
Keep these key values safe.
Authenticating using a machine part API key gives the authenticated CLI session full read and write access to your machine.
{{% /alert %}}

Once created, you can use the machine part API key to authenticate future CLI sessions or to [connect to your machine with the SDK](/build/program/#authenticate).
To switch to using a machine part API key for authentication right away, [logout](#logout) then log back in using `viam login api-key`.

A location can have multiple API keys.

## Manage your machines with the Viam CLI

With the Viam CLI [installed](#install) and [authenticated](#authenticate), you can use it to issue commands to your machine fleet or manage custom modules.
All Viam CLI commands use the following format:

```sh {class="command-line" data-prompt="$"}
viam [global options] command [command options] [arguments...]
```

<!-- prettier-ignore -->
|        parameter     |       description      |
| ----------- | ----------- |
| [global options](#global-options)      | _optional_ - list of flags that apply for commands      |
| [command](#commands)  | _required_ - the specific CLI command to run        |
| command options   | _required for some commands_  - the operation to run for the specified command.     |
| arguments   | _required for some commands_ - the arguments for the specified command operation. Some commands take positional arguments, some named arguments.     |

See the list of [commands](#commands) below.

### CLI help

The Viam CLI has a built-in help system that lists all available commands.
You can access it at any time by issuing the command:

```sh {class="command-line" data-prompt="$"}
viam --help
```

You can also access contextual help by passing the `--help` flag as a command option for any CLI command, for example:

```sh {class="command-line" data-prompt="$"}
viam organizations --help
```

## Commands

### data

The `data` command allows you to manage machine data.
With it, you can export data in a variety of formats, delete specified data, add or remove images from a dataset and filter a dataset by tags, or configure a database user to enable querying synced tabular data directly in the cloud.

```sh {class="command-line" data-prompt="$"}
viam data export --destination=<output path> --data-type=<output data type> [...named args]
viam data delete [...named args]
viam data dataset add --dataset-id=<dataset-id> --file-ids=<file-id-or-ids> --location-id=<location-id> --org-id=<org-id> [...named args]
viam data dataset remove --dataset-id=<dataset-id> --file-ids=<file-id-or-ids> --location-id=<location-id> --org-id=<org-id> [...named args]
viam data database configure --org-id=<org-id> --password=<db-user-password>
viam data database hostname --org-id=<org-id>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# export tabular data to /home/robot/data for org abc, location 123
viam data export --destination=/home/robot/data --data_type=tabular \
--org-ids=abc --location-ids=123

# export binary data from all orgs and locations, component name myComponent
viam data export --destination=/home/robot/data --data-type=binary \
--component-name myComponent

# add images tagged with the "example" tag between January and October of 2023 to dataset abc
viam data dataset add filter --dataset-id=abc --location-id=123 --org-id=123 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example

# configure a database user for the Viam organization's MongoDB Atlas Data
# Federation instance, in order to query tabular data
viam data database configure --org-id=abc --password=my_password123
viam data database hostname --org-id=abc
```

#### Command options

<!-- prettier-ignore -->
|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `export`      | export data in a specified format to a specified location  | - |
| `database configure`      | create a new database user for the Viam organization's MongoDB Atlas Data Federation instance, or change the password of an existing user. See [Configure data query](/data/query/#configure-data-query)  | - |
| `database hostname`      | get the MongoDB Atlas Data Federation instance hostname and database name. See [Configure data query](/data/query/#configure-data-query)  | - |
| `dataset add`      | add a new image to an existing dataset by its file id, or add a group of images by specifying a filter | `filter` |
| `dataset remove`      | remove an existing image from a dataset by its file id, or remove a group of images by specifying a filter | `filter` |
| `delete binary`      | delete binary data  | - |
| `delete tabular`      | delete tabular data  | - |
| `--help`      | return help      | - |

##### Positional arguments: `dataset`

<!-- prettier-ignore -->
| argument | description |
| ----------- | ----------- | ----------- |
| `filter`     | `add` or `delete` images from a dataset using a filter. See [Using the `filter` argument)](#using-the-filter-argument).|
| `ids`     | `add` or `delete` images from a dataset by specifying one or more file ids as a comma-separated list. See [Using the `ids` argument)](#using-the-ids-argument).|
| `--help`      | return help |

##### Named arguments

<!-- prettier-ignore -->
|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--destination`      | output directory for downloaded data       |`export`| true |
| `--data-type`     |  data type to be downloaded: either binary or tabular   |`export`| true |
| `--component-name`      | filter by specified component name  |`export`, `delete`| false |
| `--component-type`     | filter by specified component type       |`export`, `delete`| false |
| `--component-model`   | filter by specified component model       |`export`, `delete`| false |
| `--dataset-id`   | dataset to add or remove images from     |`dataset`| true |
| `--delete-older-than-days` | number of days, 0 means all data will be deleted | `delete` | false |
| `--start`      | ISO-8601 timestamp indicating the start of the interval       |`export`, `delete`, `dataset`| false |
| `--end`      | ISO-8601 timestamp indicating the end of the interval       |`export`, `delete`, `dataset`| false |
| `--file-ids` | file-ids to add or remove from a dataset       |`dataset`| true |
| `--location-id`      | location id for the file ids being added or removed from the specified dataset (only accepts one location id)       |`dataset`| true |
| `--location-ids`      | filter by specified location id (accepts comma-separated list)       |`export`, `delete`| false |
| `--method`       | filter by specified method       |`export`, `delete`| false |
| `--mime-types`      | filter by specified MIME type (accepts comma-separated list)       |`export`, `delete`|false |
| `--org-id` | org ID for the database user being configured (with `database`), or for the file ids being added or removed from the specified dataset (with `dataset`) | `database configure`, `database hostname`, `dataset` | true |
| `--org-ids`     | filter by specified organizations id (accepts comma-separated list)       |`export`, `delete`| false |
| `--parallel`      | number of download requests to make in parallel, with a default value of 10       |`export`, `delete`|false |
| `--part-id`      | filter by specified part id      |`export`, `delete`| false |
| `--part-name`     | filter by specified part name       |`export`, `delete`| false |
| `--robot-id`     | filter by specified robot id       |`export`, `delete`| false |
| `--robot-name`      | filter by specified robot name       |`export`, `delete`| false |
| `--tags`      | filter by specified tag (accepts comma-separated list)       |`export`, `delete`, `dataset`| false |
| `--password` | password for the database user being configured | `database configure` | true |

##### Using the `ids` argument

When you use the `viam dataset add` and `viam dataset remove` commands, you can specify the image to add or remove using its file id.
To work with multiple images at once, you can specify multiple file ids as a comma-separated list.
For example, the following adds three images specified by their file ids to the specified dataset:

```sh {class="command-line" data-prompt="$"}
viam data dataset add ids --dataset-id=abc --location-id=123 --org-id=123 --file-ids=abc,123,def
```

To find the dataset id of a given dataset, go to the [**Datasets** subtab](https://app.viam.com/data/datasets) under the **Data** tab on the Viam app and select a dataset.
The dataset id can be found in the URL of the Viam app window when viewing a given dataset, following the `?id=` portion of the URL, resembling `abcdef1234567890abcdef12`.

To find the file id of a given image, navigate to the [**Data** tab in the Viam app](https://app.viam.com/data/view) and select your image.
Its **File ID** is shown under the **Details** subtab that appears on the right.

You cannot use filter arguments, such as `--start` or `--end` when using `ids`.

See [Datasets](/data/dataset/#datasets) for more information.

##### Using the `filter` argument

When you use the `viam dataset add` and `viam dataset remove` commands, you can optionally `filter` by common search criteria to `add` or `remove` a specific subset of images based on a search filter.
For example, the following adds all images captured between January 1 and October 1, 2023, that have the `example` tag applied, to the specified dataset:

```sh {class="command-line" data-prompt="$"}
viam data dataset add filter --dataset-id=abc --org-ids=123 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example
```

To find the dataset id of a given dataset, go to the [**Datasets** subtab](https://app.viam.com/data/datasets) under the **Data** tab on the Viam app and select a dataset.
The dataset id can be found in the URL of the Viam app window when viewing a given dataset, following the `?id=` portion of the URL, resembling `abcdef1234567890abcdef12`.

You can also have the filter parameters generated for you using the **Filtering** pane of the **Data** tab.
Navigate to the [**Data** tab in the Viam app](https://app.viam.com/data/view), make your selections from the search parameters under the **Filtering** pane (such as robot name, start and end time, or tags), and click the **Copy export command** button.
A `viam data export` command string will be copied to your clipboard that includes the search parameters you selected.
You can use the same filter parameters (such as `--start`, `--end`, etc) with your `viam data database add filter` or `viam data database remove filter` commands, except you would exclude the `--data-type` and `--destination` flags, which are specific to `viam data export`.

You cannot use the `--file-ids` argument when using `filter`.

See [Datasets](/data/dataset/#datasets) for more information.

### locations

The `locations` command allows you to manage the [locations](/fleet/locations/) that you have access to.
With it, you can list available locations, filter locations by organization, or create a new location API key.

```sh {class="command-line" data-prompt="$"}
viam locations list [<organization id>]
```

#### Command options

<!-- prettier-ignore -->
|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `list`      | list all locations (name and id) that the authenticated session has access to, grouped by organization  | **organization id** : return results for specified organization only |
| `api-key`   |  work with an api-key for your location | `create` |
| `--help`      | return help      | - |

##### Positional arguments: `api-key`

<!-- prettier-ignore -->
| argument | description |
| ----------- | ----------- | ----------- |
| `create`     | create an API key for a specific location |
| `--help`      | return help |

##### Named arguments

<!-- prettier-ignore -->
| argument | description | applicable commands | required |
| ----------- | ----------- | ----------- | ----------- |
| `--location-id`      | the location to create an API key for |`api-key` | true |
| `--name`     |  the name of the API key    |`api-key` | false |
| `--org-id`      |  the organization ID to attach the key to  |`api-key` | false |

### `login`

The `login` command helps you authorize your device for CLI usage. See [Authenticate](#authenticate).

```sh {class="command-line" data-prompt="$"}
viam login
viam login api-key --key-id <api-key-uuid> --key <api-key-secret-value>
viam login print-access-token
```

Use `viam login` to authenticate using a personal access token, or `viam login api-key` to authenticate using an organization API key.
If you haven't already, you must [create an organization API key](#create-an-organization-api-key) first in order to authenticate using one.

#### Command options

<!-- prettier-ignore -->
|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `api-key`      | authenticate to Viam using an organization, location, or machine part API key      | create |
| `print-access-token`      | prints the access token used to authenticate the current CLI session      | - |
| `--help`      | return help      | - |
| `--disable-browser-open` | authenticate in a headless environment by preventing the opening of the default browser during login (default: false) | - |

##### Named arguments

<!-- prettier-ignore -->
|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--key-id`    | the `key id` (UUID) of the API key | `api-key` | true |
| `--key`    | the `key value` of the API key | `api-key` | true |

### logout

The `logout` command ends an authenticated CLI session.

```sh {class="command-line" data-prompt="$"}
viam logout
```

### module

The `module` command allows to you to manage custom {{< glossary_tooltip term_id="module" text="modules" >}}
This includes:

- Creating a new custom {{< glossary_tooltip term_id="resource" text="modular resource" >}}
- Uploading a new module to the [Viam registry](https://app.viam.com/registry)
- Updating an existing module in the Viam registry

```sh {class="command-line" data-prompt="$"}
viam module create --name <module-id> [--org-id <org-id> | --public-namespace <namespace>]
viam module update [--module <path to meta.json>]
viam module upload --version <version> --platform <platform> [--org-id <org-id> | --public-namespace <namespace>] [--module <path to meta.json>] <module-path>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# generate metadata for a module named 'my-module' using your organization's public namespace:
viam module create --name 'my-module' --public-namespace 'my-namespace'

# generate metadata for a module named 'my-module' using your organization's organization ID:
viam module create --name 'my-module' --org-id 'abc'

# update an existing module:
viam module update

# upload a new or updated custom module to the Viam registry:
viam module upload --version "1.0.0" --platform "darwin/arm64" packaged-module.tar.gz
```

See [Upload a custom module](/registry/upload/#upload-a-custom-module) and [Update an existing module](/registry/upload/#update-an-existing-module) for a detailed walkthrough of the `viam module` commands.

If you update and release your module as part of a continuous integration (CI) workflow, you can also
[automatically upload new versions of your module on release](/registry/upload/#update-an-existing-module-using-a-github-action) using a GitHub Action.

#### Command options

<!-- prettier-ignore -->
|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `create`    | generate new metadata for a custom module on your local filesystem  | - |
| `update`    | update an existing custom module on your local filesystem with recent changes to the [`meta.json` file](#the-metajson-file) | - |
| `upload`    | validate and upload a new or existing custom module on your local filesystem to the Viam registry. See [Upload validation](#upload-validation) for more information | **module-path** : specify the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code |
| `build start`    | start a module build in a cloud runner using the build step in your [`meta.json` file](#the-metajson-file). See [Using the `build` subcommand](#using-the-build-subcommand) | - |
| `build local`    | start a module build locally using the build step in your [`meta.json` file](#the-metajson-file). See [Using the `build` subcommand](#using-the-build-subcommand) | - |
| `build list`    | list the status of your cloud module builds. See [Using the `build` subcommand](#using-the-build-subcommand) | - |
| `build logs`    | show the logs from a specific cloud module build. See [Using the `build` subcommand](#using-the-build-subcommand) | - |
| `--help`      | return help      | - |

##### Named arguments

<!-- prettier-ignore -->
|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--count`    | number of cloud builds to list, defaults to displaying all builds | `build list` | false |
| `--force`    | skip local validation of the packaged module, which may result in an unusable module if the contents of the packaged module are not correct | `upload` | false |
| `--id`    | the build ID to list or show logs for, as returned from `build start` | `build list`, `build logs` | false |
| `--module`     |  the path to the [`meta.json` file](#the-metajson-file) for the custom module, if not in the current directory | `update`, `upload`, `build` | false |
| `--name`     |  the name of the custom module to be created | `create` | true |
| `--org-id`      | the organization ID to associate the module to. See [Using the `--org-id` argument](#using-the---org-id-and---public-namespace-arguments) | `create`, `upload` | true |
| `--public-namespace`      | the [namespace](/fleet/organizations/#create-a-namespace-for-your-organization) to associate the module to. See [Using the `--public-namespace` argument](#using-the---org-id-and---public-namespace-arguments) | `create`, `upload` | true |
| `--platform`      |  the architecture of your module binary. See [Using the `--platform` argument](#using-the---platform-argument) | `upload`, `build logs` | true |
| `--version`      |  the version of your module to set for this upload. See [Using the `--version` argument](#using-the---version-argument)  | `upload` | true |
| `--wait`      |  wait for the build to finish before outputting any logs  | `build logs` | false |

##### Using the `--org-id` and `--public-namespace` arguments

All of the `module` commands accept either the `--org-id` or `--public-namespace` argument.

- Use the `--public-namespace` argument to supply the [namespace](/fleet/organizations/#create-a-namespace-for-your-organization) of your organization, suitable for uploading your module to the Viam registry and sharing with other users.
- Use the `--org-id` to provide your organization ID instead, suitable for sharing your module privately within your organization.

You may use either argument for the `viam module create` command, but must use `--public-namespace` for the `update` and `upload` commands when uploading as a public module (`"visibility": "public"`) to the Viam registry.

##### Using the `--platform` argument

The `--platform` argument accepts one of the following architectures:

<!-- prettier-ignore -->
|  Architecture  | Description | Common use case |
| -------------- | ----------- | --------------- |
| `any`          | Any supported OS running any supported architecture. | Suitable for most Python modules that do not require OS-level support (such as platform-specific dependencies). |
| `any/amd64`    | Any supported OS running the `amd64` architecture. | Suitable for most Docker-based modules on `amd64`. |
| `any/arm64`    | Any supported OS running the `arm64` (`aarch64`) architecture. | Suitable for most Docker-based modules on `arm64`. |
| `linux/any`    | Linux machines running any architecture. | Suitable for Python modules that also require Linux OS-level support (such as platform-specific dependencies). |
| `darwin/any`   | macOS machines running any architecture. | Suitable for Python modules that also require macOS OS-level support (such as platform-specific dependencies). |
| `linux/amd64`  | Linux machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on Linux `amd64`. |
| `linux/arm64`  | Linux machines running the `arm64` (`aarch64`) architecture, such as the Raspberry Pi. | Suitable for most C++ or Go modules on Linux `arm64`. |
| `linux/arm32v7`| Linux machines running the `arm32v7` architecture. | Suitable for most C++ or Go modules on Linux `arm32v7`. |
| `linux/arm32v6`| Linux machines running the `arm32v6` architecture. | Suitable for most C++ or Go modules on `arm32v6`. |
| `darwin/amd64` | macOS machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on macOS `amd64`. |
| `darwin/arm64` | macOS machines running the `arm64` architecture, such as Apple Silicon. | Suitable for most C++ or Go modules on macOS `arm64`. |

You can use the `uname -m` command on your computer or board to determine its system architecture.

The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.

If you specify a platform that includes `any` (such as `any`, `any/amd64`, or `linux/any`), a machine that deploys your module will select the _most restrictive_ architecture from the ones you have provided for your module.
For example, if you upload your module with support for `any/amd64` and then also upload with support for `linux/amd64`, a machine running the `linux/amd64` architecture deploys the `linux/amd64` version, while a machine running the `darwin/amd64` architecture deploys the `any/amd64` version.

The Viam registry page for your module displays the platforms your module supports for each version you have uploaded.

If you are using the `build logs` command, the `--platform` argument instead restricts the logs returned by the command to only those build jobs that match the specified platform.

##### Using the `--version` argument

The `--version` argument accepts a valid [semver 2.0](https://semver.org/) version (example: `1.0.0`).
You set an initial version for your custom module with your first `viam module upload` command for that module, and can later increment the version with subsequent `viam module upload` commands.

Once your module is uploaded, users can select which version of your module to use on their machine from your module's page on the Viam registry.
Users can choose to pin to a specific patch version, permit upgrades within major release families or only within minor releases, or permit continuous updates.

When you `update` a module configuration and then `upload` it, the `entrypoint` for that module defined in the [`meta.json` file](#the-metajson-file) is associated with the specific `--version` for that `upload`.
Therefore, you are able to change the `entrypoint` file from version to version, if desired.

##### Upload validation

When you `upload` a module, the command performs basic validation of your module to check for common errors.
The following criteria are checked for every `upload`:

- The module must exist on the filesystem at the path provided to the `upload` command.
- The entry point file specified in the [`meta.json` file](#the-metajson-file) must exist on the filesystem at the path specified.
- The entry point file must be executable.
- If the module is provided to the `upload` command as a compressed archive, the archive must have the `.tar.gz` or `.tgz` extension.

##### The `meta.json` file

When uploading a custom module, the Viam registry tracks your module's metadata in a `meta.json` file.
This file is created for you when you run the `viam module create` command, with the `module_id` field pre-populated based on the `--name` you provided to `create`.
If you later make changes to this file, you can register those changes with the Viam registry by using the `viam module update` command.

The `meta.json` file includes the following configuration options:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Inclusion</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>module_id</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>The name of the module, including its <a href="/fleet/organizations/#create-a-namespace-for-your-organization">namespace</a></td>

  </tr>
  <tr>
    <td><code>visibility</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>Whether the module is accessible only to members of your <a href="/fleet/organizations/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can change this setting later using the <code>viam module update</code> command.<br><br>Default: <code>private</code></td>
  </tr>
  <tr>
    <td><code>url</code></td>
    <td>string</td>
    <td>Optional</td>
    <td>The URL of the GitHub repository containing the source code of the module.</td>
  </tr>
  <tr>
    <td><code>description</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>A description of your module and what it provides.</td>
  </tr>
  <tr>
    <td><code>models</code></td>
    <td>object</td>
    <td><strong>Required</strong></td>
    <td>A list of one or more {{< glossary_tooltip term_id="model" text="models" >}} provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair.</td>
  </tr>
  <tr>
    <td><code>entrypoint</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>The name of the file that starts your module program. This can be a compiled executable, a script, or an invocation of another program. If you are providing your module as a single file to the <code>upload</code> command, provide the path to that single file. If you are providing a directory containing your module to the <code>upload</code> command, provide the path to the entry point file contained within that directory.</td>
  </tr>
</table>

For example, the following represents the configuration of an example `my-module` module in the `acme` namespace:

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/acme-co-example/my-module",
  "description": "An example custom module.",
  "models": [
    {
      "api": "rdk:component:generic",
      "model": "acme:demo:my-model"
    }
  ],
  "entrypoint": "run.sh"
}
```

{{% alert title="Important" color="note" %}}
If you are publishing a public module (`"visibility": "public"`), the [namespace of your model](/registry/#naming-your-model-namespacerepo-namename) must match the [namespace of your organization](/fleet/organizations/#create-a-namespace-for-your-organization).
In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
If the two namespaces do not match, the command will return an error.
{{% /alert %}}

See [Upload a custom module](/registry/upload/#upload-a-custom-module) and [Update an existing module](/registry/upload/#update-an-existing-module) for a detailed walkthrough of the `viam module` commands.

See [Modular resources](/registry/) for a conceptual overview of modules and the modular resource system at Viam.

##### Using the `build` subcommand

You can use the `module build start` or `module build local` commands to build your custom module according to the build steps you specify in your <file>meta.json</file> file:

- Use `build start` to build or compile your module on a cloud build host that might offer additional platform support than you have access to locally.
- Use `build local` to quickly test that your module builds or compiles as expected on your local hardware.

To configure your module's build steps, add a `build` object to your [`meta.json` file](#the-metajson-file), including the following:

```json {class="line-numbers linkable-line-numbers"}
"build": {
  "setup": "./setup.sh",                  // optional - command to install your build dependencies
  "build": "make module.tar.gz",          // command that will build your module
  "path" : "module.tar.gz",               // optional - path to your built module
                                          // (passed to the 'viam module upload' command)
  "arch" : ["linux/amd64", "linux/arm64"] // architecture(s) to build for
}
```

For example, the following extends the `my-module` <file>meta.json</file> file from the previous section with a new `build` object to control its build parameters when used with `module build start` or `module build local`:

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/acme-co-example/my-module",
  "description": "An example custom module.",
  "models": [
    {
      "api": "rdk:component:generic",
      "model": "acme:demo:my-model"
    }
  ],
  "build": {
    "setup": "setup.sh",
    "build": "make module.tar.gz",
    "path": "module.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  },
  "entrypoint": "run.sh"
}
```

When you initiate a build job using either `start` or `local`, the command returns the build ID of your job.
Provide that build ID to the `module build logs` command to show the relevant build logs for that build.

For example, use the following to initiate a build, and return the build logs as soon as it completes:

```sh {class="command-line" data-prompt="$"}
viam module build logs --wait --id $(viam module build start --version "0.1.2")
```

To list all in-progress builds and their build status, use the following command:

```sh {class="command-line" data-prompt="$"}
viam module build list
```

### organizations

The `organizations` command allows you to list the organizations your authenticated session belongs to, and to create a new organization API key.

```sh {class="command-line" data-prompt="$"}
viam organizations list
viam organizations api-key create --org-id <org-id> [--name <key-name>]
```

See [create an organization API key](#create-an-organization-api-key) for more information.

#### Command options

<!-- prettier-ignore -->
|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `list`      | list all organizations (name, id, and [namespace](/fleet/organizations/#create-a-namespace-for-your-organization)) that the authenticated session belongs to    | - |
| `api-key`      | create a new organization API key    |`create` |
| `--help`      | return help      | - |

##### Positional arguments: `api-key`

<!-- prettier-ignore -->
| argument | description |
| ----------- | ----------- | ----------- |
| `create`     | create an API key for an organization |
| `--help`      | return help |

##### Named arguments

<!-- prettier-ignore -->
| argument | description | applicable commands | required |
| ----------- | ----------- | ----------- | ----------- |
| `--org-id`      | the organization to create an API key for |`api-key` | true |
| `--name`     |  the optional name for the organization API key. If omitted, a name will be auto-generated based on your login info and the current time   |`api-key` | false |

### robots

The `robots` command allows you to manage your machine fleet.
This includes:

- Listing all machines that you have access to, filtered by organization and location.
- Creating API keys to grant access to a specific machine
- Retrieving machine and machine part status
- Retrieving machine and machine part logs
- Controlling a machine by issuing component and service commands
- Accessing your machine with a secure shell (when this feature is enabled)

```sh {class="command-line" data-prompt="$"}
viam robots list
viam robots status --organization=<org name> --location=<location name> --robot=<machine id>
viam robots logs --organization=<org name> --location=<location name> --robot=<machine id> [...named args]
viam robots part status --organization=<org name> --location=<location name> --robot=<machine id>
viam robots part run --organization=<org name> --location=<location name> --robot=<machine id> [--stream] --data <meth>
viam robots part shell --organization=<org name> --location=<location name> --robot=<machine id>
```

Examples:

```sh {class="command-line" data-prompt="$"}

# list all machines you have access to
viam robots list

# get machine status
viam robots status  --robot 82c608a-1be9-46a5-968d-bad3a8a6daa --organization "Robot's Org" --location myLoc

# stream error level logs from a machine part
viam robots part logs --robot 82c608a-1be9-46a5-968d-bad3a8a6daa \
--organization "Robot's Org" --location myLoc --part "myrover-main" --tail true

# stream classifications from a machine part every 500 milliseconds from the Viam Vision Service with classifier "stuff_detector"
viam robots part run --robot 82c608a-1be9-46a5-968d-bad3a8a6daa \
--organization "Robot's Org" --location myLoc --part "myrover-main" --stream 500ms \
--data '{"name": "vision", "camera_name": "cam", "classifier_name": "stuff_detector", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

#### Command options

<!-- prettier-ignore -->
|        command option     |       description      | positional arguments
| ----------- | ----------- | ----------- |
| `list`      | list all machines that the authenticated session has access to, filtered by organization and location.  | - |
| `api-key`   |  work with an api-key for your machine | `create` (see [positional arguments: api-key](#positional-arguments-api-key)) |
| `status`      | retrieve machine status for a specified machine  | - |
| `logs`      | retrieve logs for a specified machine | - |
| `part`      | manage a specified machine part  | `status`, `run`, `logs`, `shell` (see [positional arguments: part](#positional-arguments-part)) |
| `--help`      | return help      | - |

##### Positional arguments: `api-key`

<!-- prettier-ignore -->
| argument | description |
| ----------- | ----------- | ----------- |
| `create`     | create an API key for a specific machine |
| `--help`      | return help |

##### Positional arguments: `part`

<!-- prettier-ignore -->
|        argument     |       description |
| ----------- | ----------- | ----------- |
| `status`     | retrieve machine status for a specified machine part |
| `run`     |  run a component or service command, optionally at a specified interval. For commands that return data in their response, you can use this to stream data. |
| `logs`     |  get logs for the specified machine part |
| `shell`     |  access a machine part securely using a secure shell. This feature must be enabled. |
| `--help`      | return help |

##### Named arguments

<!-- prettier-ignore -->
|        argument     |       description | applicable commands | required
| ----------- | ----------- | ----------- | ----------- |
| `--organization`      | organization name that the machine belongs to       |`list`, `status`, `logs`, `part`|true |
| `--location`     |  location name that the machine belongs to    |`list`, `status`, `logs`, `part`|true |
| `--robot`      |  machine id for which the command is being issued   |`status`, `logs`, `part`|true |
| `--errors`      |  boolean, return only errors (default: false)   |`logs`|false |
| `--part`      |  part name for which the command is being issued    |`logs`|false |
| `--tail`     |  tail (stream) logs, boolean(default false)    |`part logs`|false |
| `--stream`      |  if specified, the interval in which to stream the specified data, for example, 100ms or 1s    |`part run`|false |
| `--data`      |  command data for the command being request to run (see [data argument](#using-the---stream-and---data-arguments))   |`part run`|true |
| `--robot-id`      | the machine to create an API key for |`api-key` | true |
| `--name`     |  the optional name of the API key    |`api-key` | false |
| `--org-id`      |  the optional organization ID to attach the key to  |`api-key` | false |

##### Using the `--stream` and `--data` arguments

Issuing the `part` command with the `run` positional argument allows you to run component and service (resource) commands for a selected machine part.

The `--data` parameter is required and you must specify both:

- Method arguments in JSON format
- A resource method (in the form of the {{< glossary_tooltip term_id="protobuf" text="protobuf" >}} package and method path)

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

### version

The `version` command returns the version of the Viam CLI.
To update to the latest version of the CLI, run the [installation steps](#install) again to download and install the latest version.

```sh {class="command-line" data-prompt="$"}
viam version
```

### whoami

The `whoami` command returns the Viam user for an authenticated CLI session, or "Not logged in" if there is no authenticated session.

```sh {class="command-line" data-prompt="$"}
viam whoami
```

## Global options

You can pass global options after the `viam` CLI keyword with any command.

<!-- prettier-ignore -->
|        global option     |       description |
| ----------- | ----------- |
| `--debug` | enable debug logging (default: false) |
