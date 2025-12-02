---
title: "Viam CLI"
linkTitle: "CLI"
weight: 10
type: "docs"
no_list: true
description: "Manage and control your machines from the command line."
aliases:
  - "/build/program/cli"
  - /manage/cli/
  - /fleet/cli/
  - /cli/
images: ["/platform/cli.png"]
date: "2024-08-23"
# updated: ""  # When the content was last entirely checked
---

The Viam CLI (command line interface) tool enables you to manage your machines and {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} across organizations and locations from the command line.
The CLI lets you:

- Retrieve [organization](/dev/reference/glossary/#organization) and location information
- Manage fleet data and logs
- Control machines by issuing component and service commands
- Upload and manage modular resources in the [registry](https://app.viam.com/registry/)

For example, this CLI command moves a servo to the 75 degree position:

```sh {class="command-line" data-prompt="$"}
viam machines part run --machine 82c608a-1be9-46a5 --organization 123 \
--location myLoc --part "mymachine-main" --data '{"name": "myServo", "angle_deg":75}' \
viam.component.servo.v1.ServoService.MoveRequest
```

## Install

You can download the Viam CLI using one of the options below.
Select the tab for your platform and architecture.
If you are on Linux, you can use the `uname -m` command to determine your system architecture.

{{< tabs >}}
{{% tab name="macOS" %}}

To download the Viam CLI on a macOS computer, run the following commands:

```sh {class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Linux aarch64" %}}

To download the Viam CLI on a Linux computer with the `aarch64` architecture, run the following commands:

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

To download the Viam CLI on a Linux computer with the `amd64` (Intel `x86_64`) architecture, run the following commands:

```sh {class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod a+rx /usr/local/bin/viam
```

You can also install the Viam CLI using [brew](https://brew.sh/) on Linux `amd64` (Intel `x86_64`):

```sh {class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Windows" %}}

[Download the binary](https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-windows-amd64.exe) and run it directly to use the Viam CLI on a Windows computer.

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

You can authenticate your CLI session using a personal access token, a profile, or an organization, location, or machine part API key.

- To authenticate your CLI session using a personal access token:

  ```sh {class="command-line" data-prompt="$"}
  viam login
  ```

  This will open a new browser window with a prompt to start the authentication process.
  If a browser window does not open, the CLI will present a URL for you to manually open in your browser.
  Follow the instructions to complete the authentication process.

- To authenticate your CLI session using an organization, location, or machine part API key:

  ```sh {class="command-line" data-prompt="$"}
  viam login api-key --key-id <api-key-id> --key <organization-api-key-secret>
  ```

  {{< alert title="Note" color="note" >}}
  To use an organization, location, or machine part API key to authenticate, you can create one from the organization's settings page or authenticate with a personal access token and then [create an organization API key](#create-an-organization-api-key), a [location](#create-a-location-api-key), or a [machine part API key](#create-a-machine-part-api-key).
  {{< /alert >}}

An authenticated session is valid for 24 hours, unless you explicitly [log out](#logout).

After the session expires or you log out, you must re-authenticate to use the CLI again.

## CLI profiles

You can also authenticate your CLI session with profiles which allow you to switch between using different privileges.
To create a profile, run the following command:

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name=default --key-id=<api-key-id> --key=<api-key>
```

To use a profile to authenticate a command, pass the `--profile` flag.
By default, the Viam CLI does not use a profile.
To use a specific profile by default, set the environment variable `VIAM_CLI_PROFILE_NAME` to the profile name.

### Create an organization API key

To use an API key to authenticate your CLI session, you must create one.
You can do this from the organization's settings page or with the CLI.

1. First, [authenticate](#authenticate) your CLI session.

1. Then, run the following command to create a new organization API key:

   ```sh {class="command-line" data-prompt="$"}
   viam organizations api-key create --org-id <org-id> --name <key-name>
   ```

   Where:

   - `org-id` is your organization ID.
     You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/).
   - `key-name` is an optional name for your API key.

The command will return a `key id` and a `key value`.
You will need both to authenticate.

{{% alert title="Important" color="note" %}}
Keep these key values safe.
By default, new organization API keys are created with **Owner** permissions, giving the key full read and write access to all machines within your organization.
You can change an API key's permissions on the organizations page by clicking the **Show details** link next to your API key.
{{% /alert %}}

Once created, you can use the organization API key to authenticate future CLI sessions or to [use the SDKs](/dev/reference/sdks/).
To switch to using an organization API key for authentication right away, [logout](#logout) then log back in using `viam login api-key`.

An organization can have multiple API keys.

### Create a location API key

To use an location API key to authenticate your CLI session, you must first create one:
You can do this from the organization's settings page or with the CLI.

1. First, [authenticate](#authenticate) your CLI session.
   If you don't already have a location API key created, authenticate using a personal access token, an [organization API key](#create-an-organization-api-key), or a [machine part API key](#create-a-machine-part-api-key).

1. Then, run the following command to create a new location API key:

   ```sh {class="command-line" data-prompt="$"}
   viam locations api-key create --location-id <location-id> --org-id <org-id> --name <key-name>
   ```

   Where:

   - `location-id` is your location ID.
     You can find your location ID by running `viam locations list` or by visiting your [fleet's page](https://app.viam.com/robots).
   - `org-id` is an optional organization ID to attach the key to.
     You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/).
     If only one organization owns the location, you can omit the parameter.
     If multiple organizations own the location, you must specify the `org-id` explicitly.
   - `key-name` is an optional name for your API key.
     If omitted, a name will be auto-generated based on your login info and the current time.

The command will return a `key id` and a `key value`.
You will need both to authenticate.

{{% alert title="Important" color="note" %}}
Keep these key values safe.
By default, new location API keys are created with **Owner** permissions, giving the key full read and write access to all machines within your location.
You can change an API key's permissions on the organizations page by clicking the **Show details** link next to your API key.
{{% /alert %}}

Once created, you can use the location API key to authenticate future CLI sessions or to [connect to machines with the SDK](/dev/reference/sdks/).
To switch to using a location API key for authentication right away, [logout](#logout) then log back in using `viam login api-key`.

A location can have multiple API keys.

### Create a machine part API key

To use a machine part API key to authenticate your CLI session, you must first create one:
You can do this from the organization's settings page or with the CLI.

1. First, [authenticate](#authenticate) your CLI session.
   If you don't already have a machine part API key created, authenticate using a personal access token, an [organization API key](#create-an-organization-api-key), or a [location API key](#create-a-location-api-key).

1. Then, run the following command to create a new machine part API key:

   ```sh {class="command-line" data-prompt="$"}
   viam machines api-key create --machine-id <machine-id> --org-id <org-id> --name <key-name>
   ```

   Where:

   - `machine-id` is your machine's ID.
     You can find your machine ID by running `viam machines list`, or by clicking the **...** button in the upper-right corner of your machine's page, and selecting **Copy machine ID**.
   - `org-id` is an optional organization ID to attach the key to.
     You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page.
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

Once created, you can use the machine part API key to authenticate future CLI sessions or to [connect to your machine with the SDK](/dev/reference/sdks/).
To switch to using a machine part API key for authentication right away, [logout](#logout) then log back in using `viam login api-key`.

A location can have multiple API keys.

## Manage your machines with the Viam CLI

With the Viam CLI [installed](#install) and [authenticated](#authenticate), you can use it to issue commands to your machine fleet or manage custom modules.
All Viam CLI commands use the following format:

```sh {class="command-line" data-prompt="$"}
viam [global options] command [command options] [arguments...]
```

<!-- prettier-ignore -->
| Parameter | Description |
| --------- | ----------- |
| [Global options](#global-options) | _optional_ - list of flags that apply for commands. |
| [Command](#commands) | _required_ - the specific CLI command to run. |
| Command options | _required for some commands_  - the operation to run for the specified command. |
| Arguments | _required for some commands_ - the arguments for the specified command operation. Some commands take positional arguments, some named arguments. |

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

### `data`

The `data` command allows you to manage machine data.
With it, you can export data in a variety of formats, delete data, add or remove tags from all data that matches a given filter, or configure a database user to enable querying synced data directly in the cloud.

```sh {class="command-line" data-prompt="$"}
viam data export binary filter --destination=<output path> [...named args]
viam data export binary ids --destination=<output path> [...named args]
viam data export tabular --destination=<destination> --part-id=<part-id> --resource-name=<resource-name> --resource-subtype=<resource-subtype> --method=<method> [other options]
viam data delete binary --org-ids=<org-ids> --start=<timestamp> --end=<timestamp> [...named args]
viam data delete tabular --org-ids=<org-ids> --start=<timestamp> --end=<timestamp> [...named args]
viam data database configure --org-id=<org-id> --password=<db-user-password>
viam data database hostname --org-id=<org-id>
viam data tag ids add --tags=<tags> --binary-data-ids=<binary_ids>
viam data tag ids remove --tags=<tags> --binary-data-ids=<binary_ids>
viam data tag filter add --tags=<tags> [...named args from filter]
viam data tag filter remove --tags=<tags> [...named args from filter]
```

Examples:

```sh {class="command-line" data-prompt="$"}
# export binary data from the specified org with mime types image/jpeg and image/png to /home/robot/data
viam data export binary filter --mime-types=image/jpeg,image/png --org-ids=12345678-eb33-123a-88ec-12a345b123a1 --destination=/home/robot/data

# export tabular data to /home/robot/data for specified part id with resource name my_movement_sensor, subtype movement_sensor and method Readings
viam data export tabular --part-id=e1234f0c-912c-1234-a123-5ac1234612345 --resource-name=my_movement_sensor --resource-subtype=rdk:component:movement_sensor --method=Readings --destination=/home/robot/data

# delete binary data of mime type image/jpeg in an organization between a specified timestamp
viam data delete binary --org-ids=123 --mime-types=image/jpeg --start 2024-08-20T14:10:34-04:00 --end 2024-08-20T14:16:34-04:00

# configure a database user for the Viam organization's MongoDB Atlas Data
# Federation instance, in order to query tabular data
viam data database configure --org-id=abc --password=my_password123

# get the hostname to access a MongoDB Atlas Data Federation instance
viam data database hostname --org-id=abc

# add tags to all data that matches the given ids in the current organization
viam data tag ids add --tags=new_tag_1,new_tag_2,new_tag_3 --binary-data-ids=123,456

# remove tags from all data that matches the given ids in the current organization
viam data tag ids remove --tags=new_tag_1,new_tag_2,new_tag_3 --binary-data-ids=123,456

# add tags to all data that matches a given filter
viam data tag filter add --tags=new_tag_1,new_tag_2 --location-ids=012 --machine-name=cool-machine --org-ids=84842  --mime-types=image/jpeg,image/png

# remove tags from all data that matches a given filter
viam data tag filter remove --tags=new_tag_1 --location-ids=012 --machine-name=cool-machine --org-ids=84842  --mime-types=image/jpeg,image/png
```

Viam currently only supports deleting approximately 500 files at a time.
To delete more data iterate over the data with a shell script:

```sh {class="command-line" data-prompt="$"}
# deleting one hour of image data
for i in {00..59}; do
  viam data delete binary --org-ids=<org-id> --mime-types=image/jpeg,image/png --start=2024-05-13T11:00:00.000Z --end=2024-05-13T11:${i}:00.000Z
done
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `export tabular` | Export tabular or sensor data to a specified location in the <file>.ndjson</file> output format. You can copy this from the UI with a filter. See [Copy `export` command](#copy-export-command). | - |
| `export binary` | Export binary or image data to a specified location. Binary data will be downloaded in the original output it was specified as. You can copy this from the UI with a filter. See [Copy `export` command](#copy-export-command). | `ids`, `filter` |
| `tag` | Add or remove tags from data matching the IDs or filter. | `ids`, `filter` |
| `database configure` | Create a new database user for the Viam organization's MongoDB Atlas Data Federation instance, or change the password of an existing user. See [Configure data query](/data-ai/data/query/#configure-data-query). | - |
| `database hostname` | Get the MongoDB Atlas Data Federation instance hostname and connection URI. See [Configure data query](/data-ai/data/query/#configure-data-query). | - |
| `delete binary` | Delete binary data from the Viam Cloud. | - |
| `delete tabular` | Delete tabular data from the Viam Cloud. | - |
| `--help` | Return help | - |

##### Positional arguments: `tag`

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `filter` | `add` or `remove` images or tags from a dataset using a filter. See [Using the `filter` argument](#using-the-filter-argument).|
| `ids` | `add` or `remove` images or tags from a dataset by specifying one or more binary data IDs as a comma-separated list. See [Using the `ids` argument](#using-the-ids-argument).|
| `--help` | Return help |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--destination` | Output directory for downloaded data. | `export tabular`, `export binary` | **Required** |
| `--component-name` | Filter by specified component name. | `export binary`, `delete`, `tag filter`| Optional |
| `--component-type` | Filter by specified component type. | `export binary`, `delete`, `tag filter` | Optional |
| `--component-model` | Filter by specified component model. | `export`, `delete`| Optional |
| `--delete-older-than-days` | Number of days, 0 means all data will be deleted. | `delete` | Optional |
| `--timeout` | Number of seconds to wait for file downloads. Default: `30`. | `export binary` | Optional|
| `--start` | ISO-8601 timestamp indicating the start of the interval. | `export binary`, `export tabular`, `delete`, `dataset`, `tag filter`| Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | `export binary`, `export tabular`, `delete`, `dataset`, `tag filter`| Optional |
| `--binary-data-ids` | Binary data IDs to add or remove tags from. | `export binary ids`, `tag ids` | **Required** |
| `--location-ids` | Filter by specified location ID (accepts comma-separated list). See [Using the `ids` argument](#using-the-ids-argument) for instructions on retrieving these values. | `export binary`, `delete`, `tag filter`| Optional |
| `--method` | Filter by specified method. | `export binary`, `export tabular`, `delete`, `tag filter`| Optional |
| `--mime-types` | Filter by specified MIME type (accepts comma-separated list). | `export binary`, `delete`, `tag filter`|false |
| `--org-ids` | Filter by specified organizations ID (accepts comma-separated list). See [Using the `ids` argument](#using-the-ids-argument) for instructions on retrieving these values. | `export binary`, `delete`, `tag filter`| Optional |
| `--parallel` | Number of download requests to make in parallel, with a default value of 10. | `export binary`, `delete`, `dataset export` | Optional |
| `--part-id` | Filter by specified part ID. | `export binary`, `export tabular`, `delete`, `tag filter`| Optional, **Required** for `export tabular` |
| `--part-name` | Filter by specified part name. | `export binary`, `delete`, `tag filter`| Optional |
| `--machine-id` | Filter by specified machine ID. | `export binary`, `delete`, `tag filter` | Optional |
| `--machine-name` | Filter by specified machine name. | `export binary`, `delete`, `tag filter`| Optional |
| `--tags` | Filter by (`export`, `delete`) or add (`tag`) specified tag (accepts comma-separated list). |`export binary`, `delete`, `tag ids`, `tag filter` | Optional |
| `--filter-tags` | Filter tags. Options: `'tagged'`, `'untagged'`, or a comma-separated list of tags for all data matching any of the tags. | `tag filter` | Optional |
| `--bbox-labels` | String labels corresponding to bounding boxes within images. | `tag filter`, `export binary` | Optional |
| `--chunk-limit` | Maximum number of results per download request (tabular data only). | `tag filter` | Optional |
| `--org-id` | The organization ID for the database user. | `database configure` | **Required** |
| `--password` | Password for the database user being configured. | `database configure` | **Required** |
| `--resource-name` | Resource name. Sometimes called "component name". | `export tabular` | **Required** |
| `--resource-subtype` | Resource {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet" >}}. | `export tabular` | **Required** |

### `datapipelines`

The `datapipelines` command provides access to data pipelines for processing machine data with {{< glossary_tooltip term_id="mql" text="MQL" >}} queries.
Data pipelines help you optimize query performance for frequently accessed complex data transformations.

```sh {class="command-line" data-prompt="$"}
viam datapipelines create --org-id=<org-id> --name=<name> --schedule=<schedule> --mql=<mql-query> --data-source-type=<type> --enable-backfill=False
viam datapipelines update --id=<pipeline-id> --name=<name> --schedule=<schedule> --mql=<mql-query> [--data-source-type=<type>]
viam datapipelines list --org-id=<org-id>
viam datapipelines describe --id=<pipeline-id>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# create a new data pipeline with standard data source type (default)
viam datapipelines create --org-id=123 --name="Daily Sensor Summary" --schedule="0 9 * * *" --data-source-type=standard --mql='[{"$match": {"component_name": "sensor-1"}}]' --enable-backfill=False

# create a data pipeline with hot storage data source type for faster access
viam datapipelines create --org-id=123 --name="Real-time Analytics" --schedule="*/5 * * * *" --data-source-type=hotstorage --mql='[{"$match": {"component_name": "camera-1"}}]' --enable-backfill=False

# disable a pipeline
viam datapipelines disable --id=abc123

# enable a pipeline
viam datapipelines enable --id=abc123

# list all data pipelines in an organization
viam datapipelines list --org-id=123

# get detailed information about a specific data pipeline
viam datapipelines describe --id=abc123

# delete a data pipeline
viam datapipelines delete --id=abc123
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `create` | Create a new data pipeline. | - |
| `describe` | Get detailed information about a specific data pipeline. | - |
| `delete` | Delete a data pipeline. | - |
| `enable` | Resume executing a disabled data pipeline. | - |
| `disable` | Stop executing a data pipeline without deleting it. | - |
| `list` | List all data pipelines in an organization. | - |
| `--help` | Return help. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--org-id` | ID of the organization that owns the data pipeline. | `create`, `list` | **Required** |
| `--name` | Name of the data pipeline. | `create` | **Required** for `create` |
| `--schedule` | Cron schedule that expresses when the pipeline should run, for example `0 9 * * *` for daily at 9 AM. | `create` | **Required** for `create` |
| `--mql` | MQL (MongoDB Query Language) query as a JSON string for data processing. You must specify either `--mql` or `--mql-path` when creating a pipeline. | `create` | Optional |
| `--mql-path` | Path to a JSON file containing the MQL query for the data pipeline. You must specify either `--mql` or `--mql-path` when creating a pipeline. | `create` | Optional |
| `--data-source-type` | Data source type for the pipeline. Options: `standard` (default), `hotstorage`. `standard` provides typical analytics storage; `hotstorage` offers faster access for real-time processing. | `create` | **Required** for `create` |
| `--id` | ID of the data pipeline to describe, or delete. | `enable`, `delete`, `describe`, `disable` | **Required** |
| `--enable-backfill` | Enable the data pipeline to run over organization's historical data. Default: `false`. | `create` | **Required** |

### `dataset`

The `dataset` command allows you to manage machine data in datasets.
With it, you can add or remove images from a dataset, export data from a dataset, or filter a dataset by tags.

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=<name>
viam dataset rename --dataset-id=<dataset-id> --name=<name>
viam dataset list --org-id=<org-id>
viam dataset list --dataset-ids=<dataset-ids>
viam dataset delete --dataset-id=<dataset-id>
viam dataset export --destination=<output-directory> --dataset-id=<dataset-id>
viam dataset data add filter --dataset-id=<dataset-id> [...named args]
viam dataset data remove filter --dataset-id=<dataset-id> [...named args]
viam dataset data add ids --dataset-id=<dataset-id>  --binary-data-ids=<binary-data-ids>
viam dataset data remove ids --dataset-id=<dataset-id> --binary-data-ids=<binary-data-ids>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# create a new dataset
viam dataset create --org-id=123 --name=MyDataset

# rename dataset 123 from MyDataset to MyCoolDataset
viam dataset rename --dataset-id=123 --name=MyCoolDataset

# show dataset information for all datasets within a specified org
viam dataset list --org-id=123

# show dataset information for the specified dataset IDs
viam dataset list --dataset-ids=123,456

# delete the specified dataset
viam dataset delete --dataset-id=123

# export dataset abc to output directory ./dataset/example in two folders called "data" and "metadata"
viam dataset export --destination=./dataset/example --dataset-id=abc

# add images tagged with the "example" tag between January and October of 2023 to dataset abc
viam dataset data add filter --dataset-id=abc --location-ids=123 --org-ids=456 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example

# remove images tagged with the "example" tag between January and October of 2023 to dataset abc
viam dataset data remove filter --dataset-id=abc --location-ids=123 --org-ids=456 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example

# add images with binary data IDs aaa and bbb in the org 123 and location 456 to dataset abc
viam dataset data add ids --dataset-id=abc --binary-data-ids=aaa,bbb

# remove images with binary data IDs aaa and bbb in the org 123 and location 456 from dataset abc
viam dataset data remove ids --dataset-id=abc --binary-data-ids=aaa,bbb
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `create` | Create a new dataset. | - |
| `rename` | Rename an existing dataset. | - |
| `list` | List dataset information from specified IDs or for an org ID. | - |
| `delete` | Delete a dataset. | - |
| `data add` | Add new images to an existing dataset by binary data ID or add images that match a specified [filter](#using-the-filter-argument). | `ids`, `filter` |
| `data remove` | Remove images from an existing dataset by binary data ID or remove images that match a specified [filter](#using-the-filter-argument). | `ids`, `filter` |
| `export` | Download all the data from a dataset. | - |
| `--help` | Return help. | - |

##### Positional arguments

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `filter` | `add` or `remove` images from a dataset using a filter. See [Using the `filter` argument)](#using-the-filter-argument).|
| `ids` | `add` or `remove` images from a dataset by specifying one or more binary data IDs as a comma-separated list. See [Using the `ids` argument)](#using-the-ids-argument).|
| `--help` | Return help. |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--dataset-id` | Dataset to perform an operation on. To retrieve the ID, navigate to your dataset's page, click **…** in the left-hand menu, and click **Copy dataset ID** | `rename`, `delete`, `data add`, `data remove`, `export` | **Required** |
| `--dataset-ids` | Dataset IDs of datasets to be listed. To retrieve these IDs, navigate to your dataset's page, click **…** in the left-hand menu, and click **Copy dataset ID** | `list` | Optional |
| `--destination` | Output directory for downloaded data. | `export` | **Required** |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | `data add`, `data remove` | Optional |
| `--binary-data-ids` | The binary data IDs of the files to perform an operation on. | `data add ids`, `data remove ids` | **Required** |
| `--include-jsonl` | Set to `true` to include JSON Lines files for local testing. |`export`| Optional |
| `--name` | The name of the dataset to create or rename. | `create`, `rename` | **Required** |
| `--org-id` | Organization ID of the organization the dataset belongs to. | `create`, `data add`, `list` | **Required** |
| `--org-ids` | Organization IDs of the organizations to filter data on. | `data add filter`, `data remove filter` | Optional |
| `--parallel` | Number of download requests to make in parallel, with a default value of 100. | `export` | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | `data add`, `data remove` | Optional |
| `--tags` | Filter by specified tag (accepts comma-separated list). | `data add`, `data remove` | Optional |
| `--bbox-labels` | Filter data on bounding box labels. Accepts comma-separated list. | `data add filter`, `data remove filter` | Optional |
| `--component-name` | Filter data on component name. | `data add filter`, `data remove filter` | Optional |
| `--component-type` | Filter data on component type. | `data add filter`, `data remove filter` | Optional |
| `--location-ids` | Filter data on location IDs. Accepts comma-separated list. | `data add filter`, `data remove filter` | Optional |
| `--machine-id` | Filter data on machine ID. | `data add filter`, `data remove filter` | Optional |
| `--machine-name` | Filter data on machine name. | `data add filter`, `data remove filter` | Optional |
| `--method` | Filter data on capture method. | `data add filter`, `data remove filter` | Optional |
| `--mime-types` | Filter data on MIME types. Accepts comma-separated list. | `data add filter`, `data remove filter` | Optional |
| `--part-id` | Filter data on part ID. | `data add filter`, `data remove filter` | Optional |
| `--part-name` | Filter data on part name. | `data add filter`, `data remove filter` | Optional |

##### Using the `ids` argument

When you use the `viam dataset data add` and `viam dataset data remove` commands, you specify images to add or remove using their binary data IDs as a comma-separated list.
For example, the following command adds three images specified by their binary data IDs to the specified dataset:

```sh {class="command-line" data-prompt="$"}
viam dataset data add ids --binary-data-ids=abc,123 --dataset-id=abc
```

The following command tags two images specified by their binary data IDs with three tags:

```sh {class="command-line" data-prompt="$"}
viam data tag ids add --tags=new_tag_1,new_tag_2,new_tag_3 --binary-data-ids=123,456
```

To find your organization's ID, run `viam organization list` or navigate to your organization's **Settings** page in the [Viam app](https://app.viam.com/).
Find **Organization ID** and click the copy icon.

To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) of the **DATA** tab and select a dataset.
Click **...** in the left-hand menu and click **Copy dataset ID**.

To find a location ID, run `viam locations list` or visit your [fleet's page](https://app.viam.com/robots) and copy the **Location ID**.

To find the binary data ID of a given image, navigate to the [**DATA** tab](https://app.viam.com/data/view) and select your image.
The **Binary Data ID** is shown under the **DETAILS** subtab that appears on the right.

You cannot use filter arguments such as `--start` or `--end` with the `ids` argument.

##### Using the `filter` argument

When you use the `viam dataset data add`, `viam dataset data remove` or `viam data tag` commands, you can optionally `filter` by common search criteria to `add` or `remove` a specific subset of images based on a search filter.
For example, the following command adds all images captured between January 1 and October 1, 2023, that have the `example` tag applied, to the specified dataset:

```sh {class="command-line" data-prompt="$"}
viam dataset data add filter --dataset-id=abc --org-ids=123 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example
```

The following command adds `"new_tag_1"` and `"new_tag_2"` to all images of type `"image/jpeg"` or `"image/png"` captured by the machine named `"cool-machine"` in organization `8484` and location `012`:

```sh {class="command-line" data-prompt="$"}
viam data tag filter add --tags=new_tag_1,new_tag_2 --location-ids=012 --machine-name=cool-machine --org-ids=84842  --mime-types=image/jpeg,image/png
```

To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) under the **DATA** tab and select a dataset.
Click **...** in the left-hand menu and click **Copy dataset ID**.

To find a location ID, run `viam locations list` or visit your [fleet's page](https://app.viam.com/robots) and copy from **Location ID**.

###### Copy `export` command

You can also have the filter parameters generated for you using the **Filters** pane of the **DATA** tab.
Navigate to the [**DATA** tab](https://app.viam.com/data/view), make your selections from the search parameters under the **Filters** pane (such as robot name, start and end time, or tags), and click the **Copy export command** button.
A `viam data export` command string will be copied to your clipboard that includes the search parameters you selected.
Removing the `viam data export` string, you can use the same filter parameters (such as `--start`, `--end`, etc) with your `viam data database add filter`, `viam data database remove filter`, or `viam data tag filter` commands, except you _must_ exclude the data type `binary` and `tabular` subcommands and `--destination` flags, which are specific to `viam data export`.

You cannot use the `--binary-data-ids` argument when using `filter`.

See [Create a dataset](/data-ai/train/create-dataset/) for more information.

### `infer`

The `infer` command enables you to run [cloud inference](/data-ai/ai/run-inference/#cloud-inference) on data. Cloud inference runs in the cloud, instead of on a local machine.

```sh {class="command-line" data-prompt="$" data-output="2-18"}
viam infer --binary-data-id <binary-data-id> --model-name <model-name> --model-org-id <org-id-that-owns-model> --model-version "2025-04-14T16-38-25" --org-id <org-id-that-executes-inference>
Inference Response:
Output Tensors:
  Tensor Name: num_detections
    Shape: [1]
    Values: [1.0000]
  Tensor Name: classes
    Shape: [32 1]
    Values: [...]
  Tensor Name: boxes
    Shape: [32 1 4]
    Values: [...]
  Tensor Name: confidence
    Shape: [32 1]
    Values: [...]
Annotations:
Bounding Box Format: [x_min, y_min, x_max, y_max]
  No annotations.
```

#### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--binary-data-id` | The binary data ID of the image you want to run inference on.  | **Required** |
| `--model-name` | The name of the model that you want to run in the cloud. | **Required** |
| `--model-version` | The version of the model that you want to run in the cloud. To find the latest version string for a model, visit the [registry page](https://app.viam.com/registry?type=ML+Model) for that model. You can find the latest version string in the **Version history** section, for instance "2024-02-16T12-55-32". Pass this value as a string, using double quotes. | **Required** |
| `--org-id` | The organization ID of the organization that will run the inference.  | **Required** |
| `--model-org-id` | The organization ID of the organization that owns the model. | **Required** |

### `locations`

The `locations` command allows you to manage the [locations](/manage/reference/organize/) that you have access to.
With it, you can list available locations, filter locations by organization, or create a new location API key.

```sh {class="command-line" data-prompt="$"}
viam locations list [<organization id>]
viam locations api-key create --location-id=<location-id>
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `list` | List all locations (name and id) that the authenticated session has access to, grouped by organization | **organization id** : (_optional_) return results for specified organization only. |
| `api-key` | Work with an API key for your location. | `create` |
| `--help` | Return help. | - |

##### Positional arguments: `api-key`

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `create` | Create an API key for a specific location. |
| `--help` | Return help. |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--location-id` | The location to create an API key for. | `api-key` | **Required** |
| `--name` | The name of the API key. | `api-key` | Optional |
| `--org-id` | The organization ID to attach the key to. | `api-key` | Optional |

### `login`

The `login` command allows you to authorize your device for CLI usage.

```sh {class="command-line" data-prompt="$"}
viam login
viam login api-key --key-id=<api-key-uuid> --key=<api-key-secret-value>
viam login print-access-token
```

Use `viam login` to authenticate using a personal access token, or `viam login api-key` to authenticate using an API key.
See [Authenticate](#authenticate).

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `api-key` | Authenticate to Viam using an organization, location, or machine part API key. | - |
| `print-access-token` | Prints the access token used to authenticate the current CLI session. | - |
| `--no-browser` | Authenticate in a headless environment by preventing the opening of the default browser during login (default: `false`). | - |
| `--help` | Return help. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--key-id` | The `key id` (UUID) of the API key. | `api-key` | **Required** |
| `--key` | The `key value` of the API key. | `api-key` | **Required** |

### `logout`

The `logout` command ends an authenticated CLI session.

```sh {class="command-line" data-prompt="$"}
viam logout
```

### `machines` (alias `robots` and `machine`)

The `machines` command allows you to manage your machine fleet.
This includes:

- Listing all machines that you have access to, filtered by organization and location.
- Creating API keys to grant access to a specific machine
- Retrieving machine and machine part status
- Retrieving machine and machine part logs
- Controlling a machine by issuing component and service commands
- Accessing your machine with a secure shell (when this feature is enabled)
- Copy files from and to machines
- Enter an interactive terminal on your machines

```sh {class="command-line" data-prompt="$"}
viam machines list
viam machines status --machine=<machine id>
viam machines logs --machine=<machine id> [...named args]
viam machines api-key create --machine-id=<machine id> --org-id=<org id> --name=<key name>
viam machines part list --machine=<machine id>
viam machines part logs --machine=<machine id> --part=<part id> [...named args]
viam machines part status --machine=<machine id>
viam machines part run --machine=<machine id> [--stream] --data <method>
viam machines part shell --machine=<machine id> --part=<part id>
viam machines part restart --machine=<machine id> --part=<part id>
viam machines part cp --part=<part id> <file name> machine:/path/to/file
```

Examples:

```sh {class="command-line" data-prompt="$"}
# list all machines in an organization, in all locations
viam machines list --all --organization=12345

# get machine status
viam machines status  --machine=123

# create an API key for a machine
viam machines api-key create --machine-id=123 --name=MyKey

# stream logs from a machine
viam machines logs --machine=123

# list machine parts
viam machines part list --machine=123

# stream logs from a machine part
viam machines part logs --part=myrover-main --tail=true

# stream classifications from a machine part every 500 milliseconds from the Viam Vision Service with classifier "stuff_detector"
viam machines part run --part=myrover-main --stream=500ms \
--data='{"name": "vision", "camera_name": "cam", "classifier_name": "stuff_classifier", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera

# restart a part of a specified machine
viam machines part restart --part=123

# tunnel connections to the specified port on a machine part
viam machines part tunnel --part=123 --destination-port=1111 --local-port 2222

# Copy a single file to a machine:
viam machines part cp --part=123 my_file machine:/home/user/

# Recursively copy a directory to a machine:
viam machines part cp --part=123 -r my_dir machine:/home/user/

# Copy multiple files to a machine with recursion and keep original permissions and metadata for the files:
viam machines part cp --part=123 -r -p my_dir my_file machine:/home/user/some/existing/dir/

# Copy a single file from a machine to a local destination:
viam machines part cp --part=123 machine:my_file ~/Downloads/

# Recursively copy a directory from a machine to a local destination:
viam machines part cp --part=123 -r machine:my_dir ~/Downloads/

# Copy multiple files from the machine to a local destination with recursion and keep original permissions and metadata for the files:
viam machines part cp --part=123 -r -p machine:my_dir machine:my_file ~/some/existing/dir/

# Download FTDC data from a part to a local directory:
viam machines part get-ftdc --part=123 ~/some/existing/dir/
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `list` | List all machines that the authenticated session has access to in a specified organzation or location. Defaults to first organization and location alphabetically. | - |
| `api-key` | Work with an API key for your machine. | `create` (see [positional arguments: api-key](#positional-arguments-api-key)) |
| `status` | Retrieve machine status for a specified machine. | - |
| `logs` | Retrieve logs for a specified machine. | - |
| `part` | Manage a specified machine part. | `list`, `status`, `run`, `logs`, `shell`, `restart`, `tunnel`, `get-ftdc`, `cp` (see [positional arguments: part](#positional-arguments-part)). To use the `part shell` and `part cp` commands, you must add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json). The `ViamShellDanger` fragment contains the latest version of the shell service, which you must add to your machine before copying files or using the shell. Once downloaded you can use the `viam parse-ftdc` command to inspect the data. |
| `--help` | Return help. | - |

##### Positional arguments: `api-key`

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `create` | Create an API key for a specific machine. |
| `--help` | Return help. |

##### Positional arguments: `part`

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `list` | List machine parts. |
| `status` | Retrieve machine status for a specified machine part. |
| `run` | Run a component or service command, optionally at a specified interval. For commands that return data in their response, you can use this to stream data. |
| `logs` | Get logs for the specified machine or machine part. |
| `shell` | Access a machine part securely using a secure shell to execute commands. To use this feature you must add the [`ViamShellDanger` fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json). The `ViamShellDanger` fragment contains the latest version of the shell service, which you must add to your machine before copying files or using the shell. |
| `restart` | Restart a machine part. |
| `cp` | Copy files to and from a machine part. To use this feature you must add the [`ViamShellDanger` fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json), which contains the shell service, to your machine. Once added you can use `cp` in a similar way to the Linux `scp` command to copy files to and from machines. |
| `tunnel` | Tunnel connections to a specified port on a machine part. You must explicitly enumerate ports to which you are allowed to tunnel in your machine's JSON config. See [Tunnel to a machine part](/manage/fleet/system-settings/#configure-network-settings-for-tunneling). |
| `get-ftdc` |  Download FTDC data from a machine part. To use this feature you must add the [`ViamShellDanger` fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json). The `ViamShellDanger` fragment contains the latest version of the shell service, which you must add to your machine before copying files or using the shell. <br> Organization and location are required flags if using name (rather than ID) for the part. <br> If [target] is not specified then the FTDC data will be saved to the current working directory. <br> Note: There is no progress meter while copying is in progress.|
| `--help` | Return help. |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--part` | Part ID for which the command is being issued. | `part` | **Required** |
| `--machine` | Machine ID or name for which the command is being issued. If machine name is used instead of ID, `--organization` and `--location` are required. | `status`, `logs` | **Required** |
| `--location` | ID of the location that the machine belongs to or to list machines in. | `list`, `status`, `logs`, `part` | Optional |
| `--organization` | ID of the organization that the machine belongs to or to list machines in. | `list`, `status`, `logs`, `part` | Optional |
| `--all` | List all machines in the organization. Overrides `--location` flag. Default: `false` | `list` | Optional |
| `--errors` | Boolean, return only errors (default: false). | `logs` | Optional |
| `--levels` | Filter logs by levels (debug, info, warn, error). Accepts multiple inputs in comma-separated list. | `logs` | Optional |
| `--tail` | Tail (stream) logs, boolean(default false). | `part logs` | Optional |
| `--keyword` | Filter logs by keyword. | `logs` | Optional |
| `--start` | Filter logs to include only those after the start time. Time format example: `2025-01-13T21:30:00Z` (ISO-8601 timestamp in RFC3339). | `logs` | Optional |
| `--end` | Filter logs to include only those before the end time. Time format example: `2025-01-13T21:35:00Z` (ISO-8601 timestamp in RFC3339). | `logs` | Optional |
| `--count` | The number of logs to fetch. | `logs` | Optional |
| `--format` | THe file format for the output file. Options: `text` or `json`. | `logs` | Optional |
| `--output` | The path to the output file to store logs in. | `logs` | Optional |
| `--stream` | If specified, the interval in which to stream the specified data, for example, 100ms or 1s. | `part run` | Optional |
| `--data` | Command data for the command being request to run (see [data argument](#using-the---stream-and---data-arguments)). | `part run` | **Required** |
| `--machine-id` | The ID of the machine to create an API key for. | `api-key` | **Required** |
| `--name` | The optional name of the API key. | `api-key` | Optional |
| `--recursive`, `-r` | Recursively copy files. Default: `false`. | `part cp` | Optional |
| `--preserve`, `-p` | Preserve modification times and file mode bits from the source files. Default: `false`. | `part cp` | Optional |
| `--destination-port` | The port on a machine part to tunnel to. | `part tunnel` | **Required** |
| `--local-port` | The local port from which to tunnel. | `part tunnel` | **Required** |

##### Using the `--stream` and `--data` arguments

Issuing the `part` command with the `run` positional argument allows you to run component and service (resource) commands for a selected machine part.

The `--data` parameter is required and you must specify both:

- Method arguments in JSON format
- A resource method (in the form of the {{< glossary_tooltip term_id="protobuf" text="protobuf" >}} package and method path)

The format of what is passed to the `--data` argument is:

```sh {class="command-line" data-prompt="$"}
'{"arg1": "val1"}' <protobuf path>
```

You can find the protobuf path for the Viam package and method in the [Viam API package](https://github.com/viamrobotics/api/tree/main/proto/viam) by navigating to the component or service directory and then clicking on the resource file. The protobuf path is the package name.

For example:

```sh {class="command-line" data-prompt="$"}
'{"name": "vision", "camera_name": "cam", "classifier_name": "my_classifier", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

The `--stream` argument, when included in the CLI command prior to the `--data` command, will stream data back at the specified interval.

### `metadata`

The `metadata` command allows you to read organization, location, machine, and machine part metadata.

```sh {class="command-line" data-prompt="$"}
viam metadata read --part-id=<part-id>
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `read` | Read organization, location, machine, and machine part metadata. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--location-id` | The ID of the location to read metadata from. | `read` | Optional |
| `--machine-id` | The ID of the machine to read metadata from. | `read` | Optional |
| `--org-id` | The ID of the org to read metadata from. | `read` | Optional |
| `--part-id` | The ID of the part to read metadata from. | `read` | Optional |

### `module`

The `module` command allows to you to work with {{< glossary_tooltip term_id="module" text="modules" >}}.
This includes:

- Generating stub files for a new module
- Creating metadata for a {{< glossary_tooltip term_id="resource" text="modular resource" >}}
- Uploading a new module to the [registry](https://app.viam.com/registry)
- Uploading a new version of your module to the [registry](https://app.viam.com/registry)
- Updating an existing module in the Viam Registry
- Updating a module's metadata file based on models it provides
- Building your module for different architectures using cloud runners
- Building a module locally and running it on a target device. Rebuilding & restarting if already running.
- Downloading a module package from the registry

See [Update and manage modules you created](/operate/modules/advanced/manage-modules/) for more information.

If you update and release your module as part of a continuous integration (CI) workflow, you can also
[automatically upload new versions of your module on release](/operate/modules/advanced/manage-modules/#update-automatically-from-a-github-repo-with-cloud-build) using a GitHub Action.

```sh {class="command-line" data-prompt="$"}
viam module generate
viam module create --name=<module-name> [--org-id=<org-id> | --public-namespace=<namespace>]
viam module update [--module=<path to meta.json>]
viam module update-models --binary=<binary> [...named args]
viam module build start --version=<version> [...named args]
viam module build local --module=<path to meta.json> [arguments...]
viam module build list [command options] [arguments...]
viam module build logs --id=<id> [...named args]
viam module reload [...named args]
viam module upload --version=<version> --platform=<platform> [--org-id=<org-id> | --public-namespace=<namespace>] [--module=<path to meta.json>] <module-path> --tags=<tags>
viam module download [command options]
viam module local-app-testing --app-url http://localhost:3000
```

{{% alert title="Note" color="note" %}}
If you are writing your module using Python, you must have Python version 3.11 or newer installed on your computer for the `viam module generate` command to work.
{{% /alert %}}

{{% hiddencontent %}}

The `viam module generate` command can generate code for the following resource types:

Components:

- Arm component
- Audio input component
- Base component
- Board component
- Camera component
- Encoder component
- Gantry component
- Generic component
- Gripper component
- Input component
- Motor component
- Movement sensor component
- Pose tracker component
- Power sensor component
- Sensor component
- Servo component

Services:

- Generic service
- MLModel service
- Motion service
- Navigation service
- SLAM service
- Vision service

{{% /hiddencontent %}}

Examples:

```sh {class="command-line" data-prompt="$"}
# auto-generate stub files for a new modular resource by following prompts
viam module generate

# generate metadata for and register a module named 'my-module' using your organization's public namespace:
viam module create --name=my-module --public-namespace=my-namespace

# generate metadata for and register a module named "my-module" using your organization's organization ID:
viam module create --name=my-module --org-id=abc

# update an existing module
viam module update --module=./meta.json

# update a module's metadata file based on models it provides
viam module update-models --binary=./packaged-module.tar.gz --module=./meta.json

# initiate a cloud build for a public GitHub repo
viam module build start --version "0.1.2"

# initiate a cloud build for a private GitHub repo
viam module build start --version "0.1.2" --token ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD

# initiate a build locally without running a cloud build job
viam module build local

# list all in-progress builds and their build status
viam module build list

# initiate a build and return the build logs as soon as completed
viam module build logs --wait --id=$(viam module build start --version "0.1.2")

# build a module and run it on target machine
viam module reload --part-id e1234f0c-912c-1234-a123-5ac1234612345

# build and configure a module running on your local machine without shipping a tarball.
viam module reload-local --local

# restart a running module
viam module restart --id viam:python-example-module

# upload a new or updated custom module to the Viam Registry:
viam module upload --version=1.0.0 --platform=darwin/arm64 packaged-module.tar.gz --tags=distro:ubuntu,os_version:20.04,codename:focal,cuda:true,cuda_version:11,jetpack:5

# download a module package from the registry to the current directory
viam module download --id=acme:my-module

# download a module package from the registry to a specific directory
viam module download --id=acme:my-module --destination=/path/to/download/directory

# download a specific version of a module package for a specific platform
viam module download --id=acme:my-module --version=1.0.0 --platform=linux/amd64

# proxy your local Viam application and open a browser window and navigate to `http://localhost:8012/
viam module local-app-testing --app-url http://localhost:3000
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `generate` | Generate a new module with stub files and a <file>meta.json</file> file. Recommended when starting a new module. | - |
| `create` | Generate a <file>meta.json</file> file and register the metadata with the Viam registry. Recommended when you already have working module code. | - |
| `update` | Update your module's metadata and documentation in the Viam registry. Updates are based on changes to [<file>meta.json</file>](/operate/modules/advanced/metajson/) and <file>README.md</file>. Viam automatically runs `update` when you `upload` your module, as well as when you trigger a cloud build with Viam's default build action. | - |
| `update-models` | Update the module's metadata file with the models it provides. | - |
| `upload` | Validate and upload a new or existing custom module on your local filesystem to the Viam Registry. See [Upload validation](#upload-validation) for more information. | **module-path** : specify the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code. |
| `reload` | Build a module in the cloud and run it on a target marchine. Rebuild and restart if it is already running. The module is loaded to <FILE>~/.viam/packages-local/namespace_module-name_from_reload-module.tar.gz</FILE> on the target machine. | - |
| `reload-local` | Build a module locally and run it on a target machine. Rebuild and restart if it is already running. The module is loaded to <FILE>~/.viam/packages-local/namespace_module-name_from_reload-module.tar.gz</FILE> on the target machine. | - |
| `restart` | Restart a running module. | - |
| `build start` | Start a module build in a cloud runner using the build step in your [`meta.json` file](/operate/modules/advanced/metajson/). See [Using the `build` subcommand](#using-the-build-subcommand). | - |
| `build local` | Start a module build locally using the build step in your [`meta.json` file](/operate/modules/advanced/metajson/). See [Using the `build` subcommand](#using-the-build-subcommand). | - |
| `build list` | List the status of your cloud module builds. See [Using the `build` subcommand](#using-the-build-subcommand). | - |
| `build logs` | Show the logs from a specific cloud module build. See [Using the `build` subcommand](#using-the-build-subcommand). | - |
| `download` | Download a module package from the registry. | - |
| `local-app-testing` | Test your viam application locally. This will stand up a local proxy at `http://localhost:8012` to simulate the Viam application server. | - |
| `--help` | Return help. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--binary` | The binary for the module to run. The binary has to work on the OS or processor of the device. | `update-models` | **Required** |
| `--count` | Number of cloud builds to list, defaults to displaying all builds | `build list` | Optional |
| `--cloud-config` | The location of the <FILE>viam.json</FILE> file which contains the machine ID to lookup the part-id. Alternative to `--part-id`. Default: `/etc/viam.json` | `reload`, `reload-local`, `restart` | Optional |
| `--destination` | Output directory for downloaded package (default: `.`) | `download` | Optional |
| `--force` | Skip local validation of the packaged module, which may result in an unusable module if the contents of the packaged module are not correct. | `upload` | Optional |
| `--home` | Specify home directory for a remote machine where `$HOME` is not the default `/root`. | `reload`, `reload-local` | Optional |
| `--id` | For `build`, the build ID to list or show logs for, as returned from `build start`. For `reload`, `reload-local`, `restart`, and `download`, the module ID (`namespace:module-name` or `org-id:module-name`). | `build list`, `build logs`, `reload`, `reload`, `reload-local`, `restart`, `download` | Optional |
| `--local` | Use if the target machine is localhost, to run the entrypoint directly rather than transferring a bundle. Default: `false`. | `reload`, `reload-local` | Optional |
| `--module` | The path to the [`meta.json` file](/operate/modules/advanced/metajson/) for the module, if not in the current directory. | `update`, `upload`, `build`, `reload`, `reload-local` | Optional |
| `--model-name` | If passed, creates a resource in the part config with the given model triple. Use with `--resource-name`. Default: Creates no new resource. | `reload`, `reload-local` | Optional |
| `--no-build` | Skip build step. Default: `false`. | `reload-local` | Optional |
| `--no-progress` | Hide progress of the file transfer. Default: `false`. | `reload`, `reload-local` | Optional |
| `--part-id` | Part ID of the machine part. Required if running on a remote device. | `reload`, `reload-local`, `restart` | Optional |
| `--path` | The path to the root of the git repo to build. Default: `.` | `reload` | Optional |
| `--resource-name` | If passed, creates a new resource with the given resource name. Use with `--model-name`. Default: Creates no new resource. | `reload`, `reload-local` | Optional |
| `--resource-subtype` | The API to implement with the modular resource. For example, `motor`. We recommend _not_ using this option and instead following the prompts after running the command. | `generate` | Optional |
| `--resource-type` | Whether the new resource is a component or a service. For example, `component`. We recommend _not_ using this option and instead following the prompts. | `generate` | Optional |
| `--local-only` |  Create a meta.json file for local use, but don't create the module on the backend (default: `false`). | `create` | Optional |
| `--name` | The name of the module. For example: `hello-world`. | `create`, `reload-local`, `restart` | Optional |
| `--org-id` | The organization ID to associate the module to. See [Using the `--org-id` argument](#using-the---org-id-and---public-namespace-arguments). | `create`, `upload` | **Required** |
| `--public-namespace` | The namespace to associate the module to. See [Using the `--public-namespace` argument](#using-the---org-id-and---public-namespace-arguments). | `create`, `upload` | **Required** |
| `--platform` | The architecture of your module binary. See [Using the `--platform` argument](#using-the---platform-argument). | `upload`, `build logs`, `download` | **Required** for `upload` |
| `--platforms` | List of platforms to cloud build for. Default: `build.arch` in <file>meta.json</file>. | `build start` | Optional |
| `--ref` | Git reference to clone when building your module. This can be a branch name or a commit hash. Default: `main`. | `build start` | Optional |
| `--tags` | Comma-separated list of platform tags that determine to which platforms this binary can be deployed. Examples: `distro:debian,distro:ubuntu, os_version:22.04,os_codename:jammy`. For a machine to use an uploaded binary, all tags must be satisfied as well as the `--platform` field. <ul><li>`distro`: Distribution. You can find this in `/etc/os-release`. `"debian"` or `"ubuntu"`.</li><li>`os_version`:  Operating System version. On Linux, you can find this in `/etc/os-release`. Example for linux: `22.04`. On Mac, run `sw_vers --productVersion` and use the major version only. Example for mac: `14`.</li><li>`codename`: The operating system codename. Find this in `/etc/os-release`. For example: `"bullseye"`, `"bookworm"`, or `"jammy"`.</li><li>`cuda`: Whether using CUDA compiler. Run `nvcc --version`. For example: `"true"`.</li><li>`cuda_version`: The CUDA compiler version. Run `nvcc --version`. For example: `"11"` or `"12"`.</li><li>`jetpack`: Version of the NVIDIA JetPack SDK. Run `apt-cache show nvidia-jetpack`. For example: `"5"`.</li><li>`pi`: Version of the Raspberry Pi: `"4"` or `"5"`.</li><li>`pifull`: Compute module or model number, for example `cm5p` or `5B`.</li></ul> | `upload` | Optional |
| `--token` | GitHub token with repository **Contents** read access, and **Actions** read and write access. Required for private repos, not necessary for public repos. | `build start` | Optional |
| `--upload` | The path to the upload. | `upload` | Optional |
| `--version` | The version of your module to set for this upload or download. For `download`, defaults to `latest`. See [Using the `--version` argument](#using-the---version-argument). | `upload`, `download` | **Required** for `upload` |
| `--workdir` | Use this to indicate that your <file>meta.json</file> is in a subdirectory of your repo. `--module` flag should be relative to this. Default: `.` | `build start`, `reload`, `reload-local` | Optional |
| `--wait` | Wait for the build to finish before outputting any logs. | `build logs` | Optional |
| `--app-url` | The url where local app is running, including port number. For example `http://localhost:5000`. | `local-app-testing` | **Required** |
| `--machine-id` | The machine ID of the machine you want to test with. You can get your machine ID on the [Fleet page](https://app.viam.com/fleet/machines). | `local-app-testing` | Optional |

##### Using the `--org-id` and `--public-namespace` arguments

All of the `module` commands accept either the `--org-id` or `--public-namespace` argument.

- Use the `--public-namespace` argument to supply the [namespace of your organization](/operate/modules/advanced/metajson/#create-a-namespace-for-your-organization).
  This will upload your module to the Viam Registry and share it with other users.
- Use the `--org-id` to provide your organization ID instead, This will upload your module privately within your organization.

You may use either argument for the `viam module create` command, but must use `--public-namespace` for the `update` and `upload` commands when uploading as a public module (`"visibility": "public"`) to the Viam Registry.

##### Using the `--platform` argument

The `--platform` argument accepts one of the following architectures:

<!-- prettier-ignore -->
| Architecture | Description | Common use case |
| ------------ | ----------- | --------------- |
| `any` | Any supported OS running any supported architecture. | Suitable for most Python modules that do not require OS-level support (such as platform-specific dependencies). |
| `any/amd64` | Any supported OS running the `amd64` architecture. | Suitable for most Docker-based modules on `amd64`. |
| `any/arm64` | Any supported OS running the `arm64` (`aarch64`) architecture. | Suitable for most Docker-based modules on `arm64`. |
| `linux/any` | Linux machines running any architecture. | Suitable for Python modules that also require Linux OS-level support (such as platform-specific dependencies). |
| `darwin/any` | macOS machines running any architecture. | Suitable for Python modules that also require macOS OS-level support (such as platform-specific dependencies). |
| `linux/amd64` | Linux machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on Linux `amd64`. |
| `linux/arm64` | Linux machines running the `arm64` (`aarch64`) architecture, such as the Raspberry Pi. | Suitable for most C++ or Go modules on Linux `arm64`. |
| `linux/arm32v7`| Linux machines running the `arm32v7` architecture. | Suitable for most C++ or Go modules on Linux `arm32v7`. |
| `linux/arm32v6`| Linux machines running the `arm32v6` architecture. | Suitable for most C++ or Go modules on `arm32v6`. |
| `darwin/amd64` | macOS machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on macOS `amd64`. |
| `darwin/arm64` | macOS machines running the `arm64` architecture, such as Apple Silicon. | Suitable for most C++ or Go modules on macOS `arm64`. |
| `windows/amd64` | Windows machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on Windows `amd64`. |

For information on which of these platforms are supported for cloud build, see [Supported platforms for automatic updates](/operate/modules/advanced/manage-modules/#supported-platforms-for-automatic-updates).

You can use the `uname -m` command on your computer or board to determine its system architecture.

The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.

If you specify a platform that includes `any` (such as `any`, `any/amd64`, or `linux/any`), a machine that deploys your module will select the _most restrictive_ architecture from the ones you have provided for your module.
For example, if you upload your module with support for `any/amd64` and then also upload with support for `linux/amd64`, a machine running the `linux/amd64` architecture deploys the `linux/amd64` distribution, while a machine running the `darwin/amd64` architecture deploys the `any/amd64` distribution.

The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.

If you are using the `build logs` command, the `--platform` argument instead restricts the logs returned by the command to only those build jobs that match the specified platform.

##### Using the `--version` argument

The `--version` argument accepts a valid [semver 2.0](https://semver.org/) version (example: `1.0.0`).
You set an initial version for your custom module with your first `viam module upload` command for that module, and can later increment the version with subsequent `viam module upload` commands.

{{% alert title="Important" color="note" %}}
You cannot upload multiple distributions for the same architecture with the same version number.
You can delete the distribution files for a version, but you must increment to a new version number to upload a new distribution.
{{% /alert %}}

Once your module is uploaded, users can select which version of your module to use on their machine from your module's page on the Viam Registry.
Users can choose to pin to a specific patch version, permit upgrades within major release families or only within minor releases, or permit continuous updates.

When you `update` a module configuration and then `upload` it, the `entrypoint` for that module defined in the [`meta.json` file](/operate/modules/advanced/metajson/) is associated with the specific `--version` for that `upload`.
Therefore, you are able to change the `entrypoint` file from version to version, if desired.

##### Upload validation

When you `upload` a module, the command performs basic validation of your module to check for common errors.
The following criteria are checked for every `upload`:

- The module must exist on the filesystem at the path provided to the `upload` command.
- The entry point file specified in the [`meta.json` file](/operate/modules/advanced/metajson/) must exist on the filesystem at the path specified.
- The entry point file must be executable.
- If the module is provided to the `upload` command as a compressed archive, the archive must have the `.tar.gz` or `.tgz` extension.

See [Create a module](/operate/modules/support-hardware/) and [Update and manage modules you created](/operate/modules/advanced/manage-modules/) for a detailed walkthrough of the `viam module` commands.

##### Using the `build` subcommand

You can use the `module build start` or `module build local` commands to build your custom module according to the build steps in your <file>meta.json</file> file:

- Use `build start` to build or compile your module on a cloud build host that might offer more platform support than you have access to locally.
- Use `build local` to quickly test that your module builds or compiles as expected on your local hardware.

To configure your module's build steps, add a `build` object to your [`meta.json` file](/operate/modules/advanced/metajson/) like the following:

<!-- Developers can either have a single build file for all platforms, or platform specific files: -->

<!-- { {< tabs >}}
{ {% tab name="Single Build File" %}} -->

```json {class="line-numbers linkable-line-numbers"}
"build": {
  "setup": "./setup.sh",                  // optional - command to install your build dependencies
  "build": "./build.sh",                  // command that will build your module
  "path" : "dist/archive.tar.gz",         // optional - path to your built module
                                          // (passed to the 'viam module upload' command)
  "arch" : ["linux/amd64", "linux/arm64"] // architecture(s) to build for
}
```

{{% expand "Click to view example setup.sh" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /expand %}}

{{%expand "Click to view example build.sh (with setup.sh)" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand %}}

{{% expand "Click to view example build.sh (without setup.sh)" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand%}}

<!-- { {% /tab %}} -->
<!-- { {% tab name="Platform Specific" %}}

```json {class="line-numbers linkable-line-numbers"}
"build": {
  "path" : "dist/archive.tar.gz",               // optional - path to your built module
                                                // (passed to the 'viam module upload' command)
  "arch": {
        "linux/arm64": {
          "build": "./build-linux-arm64.sh" // command that will build your module
        },
        "darwin/arm64": {
          "build": "./build-darwin-arm64.sh" // command that will build your module
        }
      } // architecture(s) to build for
}
```

{ {%expand "Click to view example build-linux-arm64.sh" %}}

```sh { class="command-line"}
#!/bin/bash
set -e

sudo apt-get install -y python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{ {% /expand%}}

{ {%expand "Click to view example build-darwin-arm64.sh" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
set -e

brew install python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{ {% /expand%}}

{{ % /tab %}}
{ {< /tabs >}} -->

For example, the following extends the `my-module` <file>meta.json</file> file using the single build file approach, adding a new `build` object to control its build parameters when used with `module build start` or `module build local`:

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/<my-repo-name>/my-module",
  "description": "An example custom module.",
  "models": [
    {
      "api": "rdk:component:generic",
      "model": "acme:demo:my-model",
      "markdown_link": "README.md#configure-a-my-model",
      "short_description": "An example model that supports something."
    }
  ],
  "build": {
    "setup": "./setup.sh",
    "build": "./build.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  },
  "entrypoint": "<PATH-TO-EXECUTABLE>"
}
```

When you initiate a build job using either `start` or `local`, the command returns the build ID of your job.
Provide that build ID to the `module build logs` command to show the relevant build logs for that build.

For example, use the following to initiate a build, and return the build logs as soon as it completes:

```sh {class="command-line" data-prompt="$"}
viam module build logs --wait --id=$(viam module build start --version "0.1.2")
```

To list all in-progress builds and their build status, use the following command:

```sh {class="command-line" data-prompt="$"}
viam module build list
```

### `organizations`

The `organizations` command allows you to list the organizations your authenticated session has access to, and to create a new organization API key.

```sh {class="command-line" data-prompt="$"}
viam organizations list
viam organizations api-key create --org-id=<org-id> [--name=<key-name>]
viam organizations support-email [get|set] --org-id=<org-id> --support-email=<support-email>
viam organizations logo set --org-id=<org-id> --logo-path=<logo-path>
viam organization auth-service [enable|disable] --org-id=<org-id>
viam organization auth-service oauth-app [create|update] --client-authentication [required|unspecified|not_required|not_required_when_using_pkce] \
    --client-name <client-name> --enabled-grants [password|unspecified|refresh_token|implicit|device_code|authorization_code] \
    --logout-uri=https://logoipsum.com --origin-uris=https://logoipsum.com \
    --pkce=[required|not_required|unspecified] --redirect-uris=https://logoipsum.com/callback \
    --url-validation=[allow_wildcards|unspecified|exact_match] --org-id=<org-id>
viam organization auth-service oauth-app [list] --org-id=<org-id>
viam organization auth-service oauth-app [read|delete] --org-id=<org-id> --client-id=<client-id>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# list all the organizations that you are currently authenticated to
viam organizations list

# create a new organization API key in org 123
viam organizations api-key create --org-id=123 --name=my-key
```

See [create an organization API key](#create-an-organization-api-key) for more information.

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `list` | List all organizations (name, ID, and [namespace](/operate/modules/advanced/metajson/#create-a-namespace-for-your-organization)) that the authenticated session has access to. | - |
| `api-key create` | Create a new organization API key. | - |
| `support-email get` | Get the support email for an organization. | - |
| `support-email set` | Set the support email for an organization. | - |
| `logo set` | Upload the logo for an organization from a local file. | - |
| `billing-service get-config` | Get the billing service config for an organization. | - |
| `billing-service` | Enable, update, or disable the billing service for an organization. | `enable`, `update`, `disable` |
| `auth-service` | Enable or disable auth-service for OAuth applications. Disabling the auth-service does not delete your OAuth token, it will just take off the custom branding. | `enable`, `disable` |
| `auth-service oauth-app` | List, create, update, read, or delete OAuth applications. | `create`, `update`, `list`, `read`, `delete` |
| `--help` | Return help. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--org-id` | The organization to perform the command on. | `api-key`, `support-email get`, `support-email set`, `logo set`, `billing-service get-config`, `billing-service enable`, `billing-service update`, `billing-service disable`, `auth-service enable`, `auth-service disable`, `auth-service oauth-app create`, `auth-service oauth-app update` `auth-service oauth-app list`, `auth-service oauth-app read`, `auth-service oauth-app delete`. | **Required** |
| `--name` | The optional name for the organization API key. If omitted, a name will be auto-generated based on your login info and the current time. |`api-key` | Optional |
| `--support-email` | The support email to set for the organization. | `support-email get`, `support-email set` | **Required** |
| `--logo-path` | The support email to set for the organization. | `logo set` | **Required** |
| `--address` | The stringified billing address that follows the pattern: line1, line2 (optional), city, state, zipcode. | `billing-service enable`, `billing-service update` | **Required** |
| `--client-id` | The client ID of the OAuth application. | `auth-service oauth-app read`, `auth-service oauth-app delete`, `auth-service oauth-app update` | **Required** |
| `--client-authentication` | The client authentication policy for the OAuth application. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_pkce`. Default: `unspecified`. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--client-name` | The name for the OAuth application. | `auth-service oauth-app create`, `auth-service oauth-app update`| **Required** |
| `--enabled-grants` | Comma-separated enabled grants for the OAuth application. Options: `unspecified`, `refresh_token`, `password`, `implicit`, `device_code`, `authorization_code`. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--logout-uri` | The logout uri for the OAuth application. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--org-id` |  The organization ID that is tied to the OAuth application. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--origin-uris` | Comma-separated origin URIs for the OAuth application. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--pkce` | Proof Key for Code Exchange (PKCE) for the OAuth application. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_client_authentication`. Default: `unspecified`. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--redirect-uris` | Comma-separated redirect URIs for the OAuth application. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |
| `--url-validation` | URL validation for the OAuth application. Options: `unspecified`, `exact_match`, `allow_wildcards`. Default: `unspecified`. | `auth-service oauth-app create`, `auth-service oauth-app update` | **Required** |

### `packages`

The `packages` command allows you to upload packages to the Viam Cloud or export packages from the Viam Cloud.
For example, you can use this command to download ML models or modules from the registry.

```sh {class="command-line" data-prompt="$"}
viam packages upload --org-id=<org-id> --name=<package-name> --version=<version> --type=<type> --upload=<path-to-package.tar.gz> --model-framework=<framework>
viam packages export --org-id=<org-id> --name=<package-name> --version=<version> --type=<type> --destination=<path-to-export-destination>
```

Examples:

```sh {class="command-line" data-prompt="$"}
viam packages upload --org-id=123 --name=MyMLModel --version=1.0.0 --type=ml_model --upload=./the_package.tar.gz --model-framework=tensorflow
viam packages export --org-id=123 --name=MyMLModel --version=latest --type=ml_model --destination=.
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `upload` | Upload a package to the Viam Cloud. | - |
| `export` | Download a package from the Viam Cloud. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | -------- |
| `--org-id` | The organization ID of the package. | `upload`, `export` | **Required** |
| `--name` | The name of the package. | `upload`, `export` | **Required** |
| `--version` | The version of the package or `latest` | `upload`, `export` | **Required** |
| `--type` | The type of the package: `ml_model`, `archive`, `module`, `slam_map`, or `unspecified`. | `upload`, `export` | **Required** |
| `--upload` | The path to the package for upload. Executable or zipped tar with the `.tar.gz` extension. | `upload` | **Required** |
| `--model-framework` | The framework for an uploaded `ml_model`. Valid options: `unspecified`, `tflite`, `tensorflow`, `pytorch`, or `onnx`. | `upload` | **Required** |
| `--model-type` | The type of the model. Valid options: `unspecified`, `single_label_classification`, `multi_label_classification`, `object_detection`. | `upload` | **Required** |
| `--destination` | The output directory for downloaded package. | `export` | **Required** |

### `parse-ftdc`

The `parse-ftdc` command allows you to parse an FTDC file and open a REPL with extra options to inspect the data.

```sh {class="command-line" data-prompt="$"}
viam machines part get-ftdc --part=<part-id> ftdc-data
viam parse-ftdc --path ftdc-tmp/<part-id>/viam-server-<date>-<time>.ftdc
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `--help` | Return help. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--path` | The absolute file path to the FTDC file. | **Required** |

### `profiles`

The `profiles` command allows you to manage different CLI authentication profiles, so you can easily switch between API key authentications (for example authentication to one organization versus another).

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name=<name-of-profile-to-add> --key-id=<API-key-ID> --key=<API-key>
viam profiles update --profile-name=<name-of-profile-to-update> --key-id=<API-key-ID> --key=<API-key>
viam profiles list
viam profiles remove --profile-name=<name-of-profile-to-remove>
```

Examples:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
# Add a new profile for authentication (throws error if profile already exists)
viam profiles add --profile-name=mycompany --key-id=54321zyx --key=123abcd1234

# Update an existing profile for authentication, or add it if it doesn't exist
viam profiles update --key=123abcd1234 --key-id=54321zyx --profile-name=mycompany

# List all existing profiles by name
viam profiles list

# Remove a profile
viam profiles remove --profile-name=mycompany

# Example of using a profile to see a list of machines available to that profile
viam --profile=mycompany machines list
```

See [create an organization API key](#create-an-organization-api-key) for more information.

{{% alert title="Tip" color="tip" %}}
You can set a default profile by using the `VIAM_CLI_PROFILE_NAME` environment variable.
{{% /alert %}}

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `add` | List all existing profiles by name. | - |
| `update` | Update an existing profile for authentication, or add it if it doesn't exist. | - |
| `list` | List all existing profiles by name. | - |
| `remove` | Remove a profile. | - |
| `--help` | Return help. | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--profile-name` | Name of the profile to add, update, or remove. | `add`, `update`, `remove` | **Required** |
| `--key-id` | The `key id` (UUID) of the API key. | `add`, `update` | **Required** |
| `--key` | The `key value` of the API key. | `api-key`, `update` | **Required** |

### `training-script`

Manage training scripts for [custom ML training](/data-ai/train/train/).

```sh {class="command-line" data-prompt="$"}
viam training-script upload --framework=<framework> --org-id=<org-id> --path=<path-to-script> --script-name=<script-name> --type=<type>
viam training-script update --org-id=<org-id> --script-name=<script-name> --visibility=<visibility>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# upload a single label classification script in the tflite framework to organization 123
viam training-script upload --framework=tflite --org-id=123 --path=. --script-name=MyCustomTrainingScript --type=single_label_classification

# update MyCustomTrainingScript with public visibility
viam training-script update --org-id=123 --script-name=MyCustomTrainingScript --visibility=public --description="A single label classification training script"
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `upload` | Upload ML training script to the registry | - |
| `update` | Update visibility of ML training script in registry | - |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--path` | The path to ML training scripts for upload. | `upload` | **Required** |
| `--org-id` | The organization ID to host the scripts in. You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/). | `upload`, `update` | **Required** |
| `--script-name` | Name of the ML training script to update or upload. | `upload`, `update` | **Required** |
| `--visibility` | Visibility of the registry item, can be `public`, `private`, or `draft`. | `update` | **Required** |
| `--version` | Version of the ML training script to upload. | `upload` | Optional |
| `--description` | Description of the ML training script. | `update` | Optional |
| `--framework` | Framework of the ML training script to upload, can be `tflite`, `tensorflow`, `pytorch`, or `onnx`. | `upload` | Optional |
| `--url` | URL of GitHub repository associated with the training script. | `upload` | Optional |
| `--type` | Task type of the ML training script to upload, can be `single_label_classification`, `multi_label_classification`, or `object_detection`. | `upload` | Optional |
| `--draft` | Indicate draft mode, drafts are not viewable in the registry. | `upload` | Optional |

### `train`

Use a training script to train an ML model on data.

```sh {class="command-line" data-prompt="$"}
viam train submit managed --dataset-id=<dataset-id> --model-org-id=<model-org-id> --model-name=<model-name> --model-type=<model-type> --model-labels=<model-labels> [...named args]
viam train submit custom from-registry --dataset-id=<dataset-id> --org-id=<org-id> --model-name=<model-name> --script-name=<script-name> --version=<version> --args=<arg-key>=<arg-value> [...named args]
viam train submit custom with-upload --dataset-id=<dataset-id> --org-id=<org-id> --model-name=<model-name> --path=<path> --script-name=<script-name> --args=<arg-key>=<arg-value> [...named args]
viam train get --job-id=<job-id>
viam train logs --job-id=<job-id>
viam train cancel --job-id=<job-id>
viam train list --org-id=<org-id> --job-status=<job-status>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# submit training job on data in Viam Cloud with a Viam-managed training script
viam train submit managed --dataset-id=456 --model-org-id=123 --model-name=MyCoolClassifier --model-type=single_label_classification --model-labels=1,2,3

# submit custom training job with an existing training script in the Registry on data in Viam Cloud
viam train submit custom from-registry --dataset-id=<INSERT DATASET ID> --org-id=<INSERT ORG ID> --model-name=MyRegistryModel --model-version=2 --version=1 --script-name=mycompany:MyCustomTrainingScript  --args=num_epochs=3,model_type=multi_label

# submit custom training job with an uploaded training script on data in Viam Cloud
viam train submit custom with-upload --dataset-id=<INSERT DATASET ID> --model-org-id=<INSERT ORG ID> --model-name=MyRegistryModel --model-type=single_label_classification --model-version=2 --version=1 --path=<path-to-tar.gz> --script-name=mycompany:MyCustomTrainingScript --args=num_epochs=3,labels="'green_square blue_star'"

# get a training job from Viam Cloud based on training job ID
viam train get --job-id=123

# get training job logs from Viam Cloud based on training job ID
viam train logs --job-id=123

# cancel training job in Viam Cloud based on training job ID
viam train cancel --job-id=123

# list training jobs in Viam Cloud based on organization ID and job status
viam train list --org-id=123 --job-status=completed
```

#### Command options

<!-- prettier-ignore -->
| Command option | Description | Positional arguments |
| -------------- | ----------- | -------------------- |
| `submit` | Submits training job on data in the Viam Cloud. | `managed`, `custom` |
| `get` | Gets a training job from the Viam Cloud based on training job ID. | - |
| `logs` | Gets the logs of a training job from the Viam Cloud based on training job ID. | - |
| `cancel` | Cancels training job in the Viam Cloud based on training job ID. | - |
| `list` | Lists training jobs in Viam Cloud based on organization ID and job status. | - |

##### Positional arguments: `submit`

<!-- prettier-ignore -->
| Argument | Description | Positional Arguments |
| -------- | ----------- | -------------------- |
| `managed` | Submits training job on data in the Viam Cloud with a Viam-managed training script. | - |
| `custom` | Submits custom training job on data in the Viam Cloud. | `from-registry`, `with-upload` |

##### Position arguments: `submit custom`

<!-- prettier-ignore -->
| Argument | Description |
| -------- | ----------- |
| `from-registry` | Submit custom training job with an existing training script in the registry on data in the Viam Cloud. |
| `with-upload` | Upload a draft training script and submit a custom training job on data in the Viam Cloud. |

##### Named arguments

<!-- prettier-ignore -->
| Argument | Description | Applicable commands | Required? |
| -------- | ----------- | ------------------- | --------- |
| `--dataset-id` | The ID of the dataset to train on. To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) of the **DATA** tab and select a dataset. Click **...** in the left-hand menu and click **Copy dataset ID**. | `submit managed`, `submit custom from-registry`, `submit custom with-upload` | **Required** |
| `--model-org-id` | The organization ID to train and save the ML model in. You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/). | `submit managed`, `submit custom with-upload` | **Required** |
| `--org-id` | The organization ID to train and save the ML model in or list training jobs from. You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/). | `submit custom from-registry`, `list` | **Required** |
| `--model-name` | The name of the ML model. | `submit managed`, `submit custom from-registry`, `submit custom with-upload` | **Required** |
| `--model-type` | Type of model to train. Can be one of `single_label_classification`, `multi_label_classification`, `object_detection`, or `unspecified`. | `submit managed`, `submit custom with-upload` | **Required**, Optional |
| `--model-framework` | The framework of model to train. Options: `tflite`, `tensorflow` | `submit managed` | Optional |
| `--model-labels` | Labels to train on. These will either be classification or object detection labels. | `submit managed` | **Required** |
| `--model-version` | Set the version of the submitted model. Defaults to current timestamp if unspecified. | `submit managed`, `submit custom from-registry`, `submit custom with-upload` | **Required** |
| `--script-name` | The registry name of the ML training script to use for training. If uploading, this sets the name. | `submit custom from-registry`, `submit custom with-upload` | **Required** |
| `--version` | The version of the ML training script to use for training. | `submit custom from-registry`, `submit custom with-upload` | **Required** |
| `--path` | The path to the ML training script to upload. | `submit custom with-upload` | **Required** |
| `--job-id` | The ID of the training job to get or cancel. You can retrieve this value with `train list`. | `get`, `logs`, `cancel` | **Required** |
| `--job-status` | Training status to filter for. Can be one of `canceled`, `canceling`, `completed`, `failed`, `in_progress`, `pending`, or `unspecified`. | `list` | **Required** |
| `--framework` | Framework of the ML training script to upload, can be `tflite`, `tensorflow`, `pytorch`, or `onnx`. | `submit custom with-upload` | Optional |
| `--args` | Pass custom comma-separated arguments to the training script. Example: `num_epochs=3,model_type=multi_label`. To include whitespace, enclose the value with whitespace in single and double quotes. Example: `num_epochs=3,labels="'green_square blue_star'"`. | `submit custom from-registry`, `submit custom with-upload` | Optional |

### `version`

The `version` command returns the version of the Viam CLI.
To update to the latest version of the CLI, run the [installation steps](#install) again to download and install the latest version.

```sh {class="command-line" data-prompt="$"}
viam version
```

### `whoami`

The `whoami` command returns the Viam user for an authenticated CLI session, or "Not logged in" if there is no authenticated session.

```sh {class="command-line" data-prompt="$"}
viam whoami
```

## Global options

You can pass global options after the `viam` CLI keyword with any command.

<!-- prettier-ignore -->
| Global option | Description |
| ------------- | ----------- |
| `--debug` | Enable debug logging. Default: `false`. |
| `--disable-profiles`, `disable-profile` | Disable usage of [profiles](#profiles), falling back to default (false) behavior. Default: `false`. |
| `--help`, `-h` | Show help. Default: `false`. |
| `--profile` | Specify a particular [profile](#profiles) for the current command. |
| `--quiet`, `-q` | Suppress warnings. Default: `false` |
